# API Deployment

Deploying the Knowledge API and MetaInformAnt API.

## Prerequisites

```bash
pip install -r requirements.txt
```

Both services also depend on the optional `[api]` extras for the multi-database
backends (`pymongo`, `redis`, `elasticsearch`, `neo4j`, `motor`, `aioredis`):

```bash
pip install -e ".[api]"
```

## Database Setup

The Knowledge API uses SQLAlchemy with SQLite by default
(`sqlite:///./knowledge.db`). Point it at PostgreSQL or another RDBMS via the
`KNOWLEDGE_DB_URL` environment variable.

| Store | Environment Variable | Default Connection |
|-------|---------------------|--------------------|
| Primary RDBMS | `KNOWLEDGE_DB_URL` | `sqlite:///./knowledge.db` (SQLite) |
| MongoDB (secondary) | `KNOWLEDGE_MONGO_URL` | `mongodb://localhost:27017/` |
| Redis (secondary) | `KNOWLEDGE_REDIS_URL` | `redis://localhost:6379/0` |
| Neo4j (secondary) | `KNOWLEDGE_NEO4J_URL` | `bolt://localhost:7687` |
| Elasticsearch (secondary) | `KNOWLEDGE_ES_URL` | `http://localhost:9200` |

Secondary stores are best-effort: if a store is unavailable, writes still
succeed in the primary database and a warning is logged.

## Running

```bash
cd 6_API

# Knowledge API
uvicorn Knowledge_API:app --host 0.0.0.0 --port 8000 --reload

# MetaInformAnt API
uvicorn MetaInformAnt_API:app --host 0.0.0.0 --port 8001 --reload
```

Each service can also be started directly: `python3 Knowledge_API.py`.

## API Documentation

Once running, visit:
- Knowledge API: `http://localhost:8000/api/docs`
- MetaInformAnt API: `http://localhost:8001/api/docs`

ReDoc is available at `/api/redoc` and the OpenAPI schema at `/api/openapi.json`.

## Authentication

Set `KNOWLEDGE_API_KEY` (Knowledge API) or `META_API_KEY` (MetaInformAnt API)
to enable API-key authentication. When set, mutating requests must carry the
key in the `X-API-Key` header:

```bash
curl -H "X-API-Key: your-secret-key" \
  -X POST http://localhost:8000/api/knowledge/ \
  -H "Content-Type: application/json" \
  -d '{"source": "demo", "content": {"note": "hello"}}'
```

When the key is unset, the service starts in open local/dev mode. Set the key
before deploying anywhere non-local.
