# API Deployment

Deploying the Knowledge API and MetaInformAnt API.

## Prerequisites

```bash
pip install fastapi uvicorn pydantic sqlalchemy pymongo motor redis neo4j elasticsearch aiocache aioredis
```

## Database Setup

| Database | Required For | Default Connection |
|----------|-------------|-------------------|
| PostgreSQL | Relational data | `postgresql://localhost/activeinferants` |
| MongoDB | Document store | `mongodb://localhost:27017` |
| Redis | Caching | `redis://localhost:6379` |
| Neo4j | Graph database | `bolt://localhost:7687` |
| Elasticsearch | Full-text search | `http://localhost:9200` |

## Running

```bash
cd 6_API

# Knowledge API
uvicorn Knowledge_API:app --host 0.0.0.0 --port 8000 --reload

# MetaInformAnt API
uvicorn MetaInformAnt_API:app --host 0.0.0.0 --port 8001 --reload
```

## API Documentation

Once running, visit:
- Knowledge API: `http://localhost:8000/docs`
- MetaInformAnt API: `http://localhost:8001/docs`

## Authentication

Set the `X-API-Key` header on all mutating requests:

```bash
curl -H "X-API-Key: your-key" -X POST http://localhost:8000/knowledge
```
