# MetaInformAnt API

FastAPI-based meta-information service for process tracking and agent management.

## Purpose

Provides meta-level information about Active Inference processes, agent states, and system-wide coordination.

## Key Features

- Real inference and federated engines running in background tasks (`/api/v1/advanced_infer/`, `/api/v1/federated_learn/`)
- Task status tracking (`/api/v1/status/`)
- System status, health, and metrics endpoints (`/api/v1/health`, `/api/v1/metrics`)
- Optional API-key authentication via the `X-API-Key` header (enabled when the API key environment variable is set)
- Auto-generated OpenAPI documentation at `/api/docs`

## Configuration

Configuration is read from environment variables:

| Variable | Default | Purpose |
|----------|---------|---------|
| `META_API_KEY` | *(empty)* | Enables API-key authentication when set |
| `META_LOG_LEVEL` | `INFO` | Logging level |

Authentication follows the same convention as the Knowledge API: when
`META_API_KEY` is unset the service runs in open local/dev mode.

## Source

[`6_API/MetaInformAnt_API.py`](../../6_API/MetaInformAnt_API.py)
