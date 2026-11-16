# Knowledge API

FastAPI-based knowledge management service with a SQL-first primary store and best-effort secondary stores.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Primary store | SQLAlchemy (SQLite by default; set `KNOWLEDGE_DB_URL` for PostgreSQL or another RDBMS) |
| Document store | MongoDB via `pymongo` (best-effort secondary store) |
| Secondary copy | Redis via `redis`: best-effort write copy, not a read-through cache |
| Graph DB | Neo4j via the `neo4j` driver (best-effort secondary store) |
| Search | Elasticsearch via the `elasticsearch` client (best-effort secondary store) |
| Auth | Optional API key via `APIKeyHeader` (`X-API-Key`) |
| Docs | Auto-generated OpenAPI at `/api/docs` (Swagger UI) and `/api/redoc` |

## Authentication

Authentication is enabled only when `KNOWLEDGE_API_KEY` is set. When enabled,
every knowledge CRUD/list route requires `X-API-Key`, checked with constant-time
comparison. Unconfigured mode is open local/development use.

```python
from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name="X-API-Key")
```

When it is unset, the service runs in open local/dev mode (no key required) so
it starts without extra configuration. Set `KNOWLEDGE_API_KEY` before
deploying anywhere non-local.

## Configuration

All configuration is read from `KNOWLEDGE_*` environment variables (see the
`Config` class in the source). Notable settings:

| Variable | Default | Purpose |
|----------|---------|---------|
| `KNOWLEDGE_DB_URL` | `sqlite:///./knowledge.db` | Primary SQLAlchemy database URL |
| `KNOWLEDGE_MONGO_URL` | `mongodb://localhost:27017/` | MongoDB secondary store |
| `KNOWLEDGE_REDIS_URL` | `redis://localhost:6379/0` | Redis secondary store |
| `KNOWLEDGE_ES_URL` | `http://localhost:9200` | Elasticsearch secondary store |
| `KNOWLEDGE_NEO4J_URL` | `bolt://localhost:7687` | Neo4j secondary store |
| `KNOWLEDGE_API_KEY` | *(empty)* | Enables API-key authentication when set |
| `KNOWLEDGE_ALLOW_ORIGINS` | `http://localhost:8000` | Comma-separated CORS origins (never `*`) |

## Execution and Consistency

Handlers, SQLAlchemy access and secondary clients are synchronous. SQL is the
authoritative primary; reads/lists query SQL only. Redis is not read as a cache.

Creates/updates commit SQL before best-effort secondary writes. Deletes commit
SQL before best-effort secondary removal. No distributed transaction, real-time
consistency, cache, retry or automatic-convergence guarantee is provided.

`PUT` body source must match the URL source; mismatch is 400 and renaming is
not implemented. Duplicate source creation, including a recognized commit-time
source uniqueness conflict, is 409. Unrelated database failures remain errors.
Failure paths roll back the current SQL transaction; rollback does not reverse
an already committed primary or secondary effect.

Secondary failures are logged and can leave absent/stale copies even when
primary mutation succeeds. SQL-only operation remains available without
optional stores. List uses `skip`/`limit` pagination; CORS remains restricted
to configured origins.

## Source

[`6_API/Knowledge_API.py`](https://github.com/ActiveInferenceInstitute/Active_InferAnts/blob/main/6_API/Knowledge_API.py)
