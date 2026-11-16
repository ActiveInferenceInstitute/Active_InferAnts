"""Tests for the Knowledge API (CRUD + status codes)."""


import pytest


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    from fastapi.testclient import TestClient

    with pytest.MonkeyPatch.context() as environment:
        path = tmp_path_factory.mktemp("knowledge") / "test.db"
        environment.setenv("KNOWLEDGE_DB_URL", f"sqlite:///{path}")
        environment.delenv("KNOWLEDGE_API_KEY", raising=False)
        for name in ("KNOWLEDGE_MONGO_URL", "KNOWLEDGE_REDIS_URL", "KNOWLEDGE_ES_URL", "KNOWLEDGE_NEO4J_URL"):
            environment.setenv(name, "")
        import Knowledge_API

        with TestClient(Knowledge_API.app) as test_client:
            yield test_client
        Knowledge_API.engine.dispose()


@pytest.fixture(autouse=True)
def clean_primary(client):
    import Knowledge_API as api

    with api.SessionLocal() as database:
        database.query(api.KnowledgeItem).delete()
        database.commit()
    yield
    with api.SessionLocal() as database:
        database.query(api.KnowledgeItem).delete()
        database.commit()



def test_full_crud_lifecycle(client):
    r = client.post(
        "/api/knowledge/", json={"source": "exp_a", "content": {"acc": 0.9}}
    )
    assert r.status_code == 201
    r = client.post("/api/knowledge/", json={"source": "exp_a", "content": {}})
    assert r.status_code == 409
    r = client.get("/api/knowledge/exp_a")
    assert r.status_code == 200
    assert r.json()["content"]["acc"] == 0.9
    r = client.put(
        "/api/knowledge/exp_a", json={"source": "exp_a", "content": {"acc": 0.95}}
    )
    assert r.status_code == 200
    assert client.get("/api/knowledge/exp_a").json()["content"]["acc"] == 0.95
    r = client.get("/api/knowledge/")
    assert r.status_code == 200 and len(r.json()) == 1
    assert client.get("/api/knowledge/missing").status_code == 404
    assert client.delete("/api/knowledge/exp_a").status_code == 200
    assert client.delete("/api/knowledge/exp_a").status_code == 404


def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"


def test_mismatched_identity_cannot_change_primary_or_secondary(client, monkeypatch):
    import Knowledge_API as api

    writes = []
    monkeypatch.setattr(api, "_sync_to_secondary", lambda clients, value: writes.append(value.model_dump()))
    assert client.post("/api/knowledge/", json={"source": "a", "content": {"value": 1}}).status_code == 201
    assert client.post("/api/knowledge/", json={"source": "b", "content": {"value": 2}}).status_code == 201
    response = client.put("/api/knowledge/a", json={"source": "b", "content": {"value": 3}})
    assert response.status_code == 400
    assert client.get("/api/knowledge/a").json()["content"] == {"value": 1}
    assert client.get("/api/knowledge/b").json()["content"] == {"value": 2}
    assert writes == [{"source": "a", "content": {"value": 1}}, {"source": "b", "content": {"value": 2}}]


def test_every_secondary_receives_the_committed_identity_and_delete(client, monkeypatch):
    import Knowledge_API as api

    class Collection:
        def __init__(self):
            self.values = {}

        def replace_one(self, query, payload, upsert):
            self.values[query["source"]] = dict(payload)

        def delete_one(self, query):
            self.values.pop(query["source"], None)

    class Redis(dict):
        def set(self, key, value):
            self[key] = value

        def delete(self, key):
            self.pop(key, None)

    class Search:
        def __init__(self):
            self.values = {}

        def index(self, *, index, id, document):
            self.values[(index, id)] = dict(document)

        def delete(self, *, index, id):
            self.values.pop((index, id), None)

    class Graph:
        def __init__(self):
            self.values = {}

        def session(self):
            return self

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def run(self, query, *, source, content=None):
            if query.startswith("MERGE "):
                self.values[source] = content
            elif query.startswith("MATCH "):
                self.values.pop(source, None)
            else:
                raise AssertionError("Unexpected graph operation")

    collection, redis, search, graph = Collection(), Redis(), Search(), Graph()
    clients = {
        "mongo": {api.config.MONGO_DB: {"knowledge_items": collection}},
        "redis": redis, "es": search, "neo4j": graph,
    }
    monkeypatch.setattr(api, "_get_clients", lambda: clients)
    assert client.post("/api/knowledge/", json={"source": "canonical", "content": {"value": 1}}).status_code == 201
    assert client.put("/api/knowledge/canonical", json={"source": "canonical", "content": {"value": 2}}).status_code == 200
    assert collection.values["canonical"]["content"] == {"value": 2}
    assert '"value": 2' in redis["knowledge:canonical"]
    assert search.values[(api.config.ES_INDEX, "canonical")]["content"] == {"value": 2}
    assert graph.values["canonical"] == str({"value": 2})
    assert client.delete("/api/knowledge/canonical").status_code == 200
    assert client.get("/api/knowledge/canonical").status_code == 404
    assert collection.values == {} and redis == {} and search.values == {} and graph.values == {}


def test_unavailable_secondaries_do_not_undo_committed_sql(client, monkeypatch):
    import Knowledge_API as api

    class Offline:
        def __getitem__(self, key):
            raise OSError("offline")

        def __getattr__(self, name):
            raise OSError("offline")

    monkeypatch.setattr(api, "_get_clients", lambda: dict.fromkeys(("mongo", "redis", "es", "neo4j"), Offline()))
    assert client.post("/api/knowledge/", json={"source": "sql-only", "content": {"value": 1}}).status_code == 201
    assert client.get("/api/knowledge/sql-only").json()["content"] == {"value": 1}
    assert client.delete("/api/knowledge/sql-only").status_code == 200
    assert client.get("/api/knowledge/sql-only").status_code == 404


def test_commit_time_source_conflict_is_409_and_session_is_reusable(client):
    import Knowledge_API as api
    from fastapi import HTTPException
    from sqlalchemy.orm import Session

    class RacingSession(Session):
        raced = False

        def commit(self):
            if not self.raced:
                self.raced = True
                with api.SessionLocal() as winner:
                    winner.add(api.KnowledgeItem(source="race", content={"winner": True}))
                    winner.commit()
            return super().commit()

    with RacingSession(bind=api.engine) as database:
        with pytest.raises(HTTPException) as failure:
            api.create_knowledge(api.KnowledgeBase(source="race", content={"loser": True}), db=database, _=None)
        assert failure.value.status_code == 409
        assert database.query(api.KnowledgeItem).filter_by(source="race").one().content == {"winner": True}
        database.add(api.KnowledgeItem(source="after-race", content={}))
        database.commit()
    assert client.get("/api/knowledge/after-race").status_code == 200


def test_unrelated_integrity_error_is_500_and_failed_write_is_rolled_back(client):
    import Knowledge_API as api
    from fastapi import HTTPException
    from sqlalchemy.orm import Session

    created = client.post("/api/knowledge/", json={"source": "existing", "content": {}})
    primary_id = created.json()["id"]

    class PrimaryKeyCollision(Session):
        injected = False

        def commit(self):
            if not self.injected:
                self.injected = True
                for item in self.new:
                    if isinstance(item, api.KnowledgeItem):
                        item.id = primary_id
            return super().commit()

    with PrimaryKeyCollision(bind=api.engine) as database:
        with pytest.raises(HTTPException) as failure:
            api.create_knowledge(api.KnowledgeBase(source="not-a-source-conflict", content={}), db=database, _=None)
        assert failure.value.status_code == 500
        assert database.query(api.KnowledgeItem).filter_by(source="not-a-source-conflict").first() is None
        database.add(api.KnowledgeItem(source="after-rollback", content={}))
        database.commit()
    assert client.get("/api/knowledge/after-rollback").status_code == 200


@pytest.mark.parametrize("operation", ["update", "delete"])
def test_failed_primary_mutation_rolls_back_before_any_secondary_effect(client, monkeypatch, operation):
    import Knowledge_API as api
    from fastapi import HTTPException

    assert client.post("/api/knowledge/", json={"source": "protected", "content": {"original": True}}).status_code == 201
    secondary = []
    monkeypatch.setattr(api, "_sync_to_secondary", lambda *args: secondary.append("write"))
    monkeypatch.setattr(api, "_delete_from_secondary", lambda *args: secondary.append("delete"))
    with api.engine.begin() as connection:
        connection.exec_driver_sql(
            f"CREATE TRIGGER mutation_abort BEFORE {operation.upper()} ON knowledge_items "
            "BEGIN SELECT RAISE(ABORT, 'controlled primary failure'); END"
        )
    try:
        with api.SessionLocal() as database:
            with pytest.raises(HTTPException) as failure:
                if operation == "update":
                    api.update_knowledge("protected", api.KnowledgeBase(source="protected", content={"new": True}), db=database, _=None)
                else:
                    api.delete_knowledge("protected", db=database, _=None)
            assert failure.value.status_code == 500
            assert database.query(api.KnowledgeItem).filter_by(source="protected").one().content == {"original": True}
        assert secondary == []
    finally:
        with api.engine.begin() as connection:
            connection.exec_driver_sql("DROP TRIGGER mutation_abort")
