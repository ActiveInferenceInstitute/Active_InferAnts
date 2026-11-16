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

## Admission and task state

Both computation routes require nonempty rectangular finite numeric matrices
before creating tasks or incrementing request metrics. Model/schema errors and
explicit matrix-admission errors are distinct rejection paths.

A worker publishes `COMPLETED` only after producing a shape-preserving finite
real result and finishing JSON-safe conversion. Failure publishes `FAILED`,
no result and an error message. Status readers receive one coherent terminal
projection.

Tasks and metrics are process-local/in-memory and disappear on restart.
These NumPy update endpoints are not durable distributed-job or
scientific-qualification services.

## Source

[`6_API/MetaInformAnt_API.py`](https://github.com/ActiveInferenceInstitute/Active_InferAnts/blob/main/6_API/MetaInformAnt_API.py)
