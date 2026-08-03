# Knowledge API

FastAPI-based knowledge management service with a SQL-first primary store and best-effort secondary stores.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| Primary store | SQLAlchemy (SQLite by default; set `KNOWLEDGE_DB_URL` for PostgreSQL or another RDBMS) |
| Document store | MongoDB via `pymongo` (best-effort secondary store) |
| Cache | Redis via `redis` (best-effort secondary store) |
| Graph DB | Neo4j via the `neo4j` driver (best-effort secondary store) |
| Search | Elasticsearch via the `elasticsearch` client (best-effort secondary store) |
| Auth | Optional API key via `APIKeyHeader` (`X-API-Key`) |
| Docs | Auto-generated OpenAPI at `/api/docs` (Swagger UI) and `/api/redoc` |

## Authentication

Authentication is **enabled only when `KNOWLEDGE_API_KEY` is set** in the
environment. When it is set, mutating endpoints require the key via the
`X-API-Key` header and the check uses a constant-time comparison:

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

## Key Features

- CORS middleware restricted to configured origins
- Auto-generated OpenAPI/Swagger documentation
- Best-effort synchronous write fan-out to secondary stores (writes never fail when a store is unavailable)
- Pydantic model validation with custom validators
- Graceful degradation when secondary stores are absent

## Source

[`6_API/Knowledge_API.py`](../../6_API/Knowledge_API.py)
