# Knowledge API

FastAPI-based knowledge management service with multi-database backend.

## Technology Stack

| Component | Technology |
|-----------|-----------|
| Framework | FastAPI |
| RDBMS | PostgreSQL (via SQLAlchemy) |
| Document Store | MongoDB (pymongo + motor async) |
| Cache | Redis (aioredis) |
| Graph DB | Neo4j (GraphDatabase driver) |
| Search | Elasticsearch (async client) |
| Auth | API Key (via `APIKeyHeader`) |
| Caching | aiocache with JSON serialization |

## Authentication

All mutating endpoints require an API key via the `X-API-Key` header.

```python
from fastapi.security import APIKeyHeader
api_key_header = APIKeyHeader(name="X-API-Key")
```

## Key Features

- CORS middleware enabled
- Auto-generated OpenAPI/Swagger documentation
- Background task processing via `BackgroundTasks`
- LRU-cached configuration loading
- Pydantic model validation with custom validators

## Source

[`6_API/Knowledge_API.py`](../6_API/Knowledge_API.py)
