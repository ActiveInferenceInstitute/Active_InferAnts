"""Tests for the Knowledge API (CRUD + status codes)."""

import os
import tempfile

import pytest


@pytest.fixture(scope="module")
def client():
    # Use an isolated temp SQLite so tests never touch a real DB.
    tmp = tempfile.mkdtemp()
    os.environ["KNOWLEDGE_DB_URL"] = "sqlite:///" + os.path.join(tmp, "test.db")
    os.environ.pop("KNOWLEDGE_API_KEY", None)
    # Import is deferred so the env var is set first.
    import Knowledge_API
    from fastapi.testclient import TestClient

    return TestClient(Knowledge_API.app)


def test_full_crud_lifecycle(client):
    r = client.post("/api/knowledge/", json={"source": "exp_a", "content": {"acc": 0.9}})
    assert r.status_code == 201
    r = client.post("/api/knowledge/", json={"source": "exp_a", "content": {}})
    assert r.status_code == 409
    r = client.get("/api/knowledge/exp_a")
    assert r.status_code == 200
    assert r.json()["content"]["acc"] == 0.9
    r = client.put("/api/knowledge/exp_a", json={"source": "exp_a", "content": {"acc": 0.95}})
    assert r.status_code == 200
    assert client.get("/api/knowledge/exp_a").json()["content"]["acc"] == 0.95
    r = client.get("/api/knowledge/")
    assert r.status_code == 200 and len(r.json()) == 1
    assert client.get("/api/knowledge/missing").status_code == 404
    assert client.delete("/api/knowledge/exp_a").status_code == 200
    assert client.delete("/api/knowledge/exp_a").status_code == 404


def test_health(client):
    assert client.get("/api/health").json()["status"] == "ok"
