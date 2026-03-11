# External Interfaces & APIs

REST APIs, knowledge management services, and external interfaces. This phase exposes Active Inference capabilities to external consumers.

## Modules

| Module | Description |
|---|---|
| `Knowledge_API.py` | FastAPI knowledge management service — multi-database backend (PostgreSQL via SQLAlchemy, MongoDB, Redis, Neo4j, Elasticsearch), pydantic validation, API key authentication, background tasks |
| `MetaInformAnt_API.py` | FastAPI meta-information service — process tracking, agent management, performance metrics, health checks, pydantic validation with `HttpUrl` |

## Usage

```bash
# Start Knowledge API (port 8000)
python3 6_API/Knowledge_API.py

# Interactive docs at http://localhost:8000/api/docs
```

## Key Endpoints

### Knowledge API
- `POST /api/knowledge/` — Create knowledge entry
- `GET /api/knowledge/{source}` — Retrieve by source
- `PUT /api/knowledge/{source}` — Update
- `DELETE /api/knowledge/{source}` — Delete
- `GET /api/knowledge/` — List all

### MetaInformAnt API
- Process tracking and monitoring
- Agent management and control
- Performance metrics and health checks

## Pipeline Position

```
5_FOLLOWUP → [6_API] → External consumers
```

- **Input**: Follow-up actions and refined data from `5_FOLLOWUP`
- **Output**: REST API responses for external clients and integrations

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [5_FOLLOWUP](../5_FOLLOWUP/README.md)
