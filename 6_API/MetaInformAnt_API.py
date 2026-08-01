"""
MetaInformAnt API — advanced / federated Active-Inference meta-information service.

Self-contained FastAPI service that runs nuclear Active-Inference-style updates
(numPy) on request data in the background, tracks task status, and exposes health
and metrics. Authentication is a constant-time environment-configured API key
(enabled when ``META_API_KEY`` is set, open otherwise).
"""

import hmac
import logging
import os
import uuid
from typing import Any

import numpy as np
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field, field_validator

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
API_KEY = os.environ.get("META_API_KEY", "")
LOG_LEVEL = os.environ.get("META_LOG_LEVEL", "INFO")


def setup_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(name)


logger = setup_logger("metainformant_api")

app = FastAPI(
    title="MetaInformAnt API",
    version="1.2.0",
    description="Decentralized / federated active-inference computation service",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)


# --------------------------------------------------------------------------- #
# Auth
# --------------------------------------------------------------------------- #
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_api_key(api_key_header: str | None = Depends(api_key_header)) -> str | None:
    if not API_KEY:
        return None
    if api_key_header and hmac.compare_digest(api_key_header, API_KEY):
        return api_key_header
    raise HTTPException(status_code=403, detail="Could not validate API key")


# --------------------------------------------------------------------------- #
# Task store (in-memory; restart clears it — suitable for local/dev use)
# --------------------------------------------------------------------------- #
_tasks: dict[str, dict[str, Any]] = {}
_metrics = {"advanced_inference_requests": 0, "federated_learning_requests": 0}


def _normalise(data: dict[str, list[float]]) -> np.ndarray:
    """Convert a {feature: [values]} payload into a 2-D float array."""
    if not data:
        raise ValueError("Data cannot be empty")
    return np.array([list(v) for v in data.values()], dtype=float)


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #
class AdvancedInferenceRequest(BaseModel):
    data: dict[str, list[float]]
    inference_type: str | None = Field(default="default")
    simulation_steps: int | None = Field(default=100, gt=0)
    agent_params: dict[str, Any] | None = None
    niche_params: dict[str, Any] | None = None

    @field_validator("data")
    @classmethod
    def validate_data(cls, v):
        if not v:
            raise ValueError("Data cannot be empty")
        return v


class FederatedLearningRequest(BaseModel):
    data: dict[str, list[float]]
    learning_rate: float | None = Field(default=0.01, gt=0, le=1)
    epochs: int | None = Field(default=10, gt=0)

    @field_validator("data")
    @classmethod
    def validate_data(cls, v):
        if not v:
            raise ValueError("Data cannot be empty")
        return v


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str | None = None
    result: Any | None = None


# --------------------------------------------------------------------------- #
# Engines (real numPy implementations)
# --------------------------------------------------------------------------- #
def active_inference_update(matrix: np.ndarray, steps: int) -> np.ndarray:
    """Normalise rows as beliefs and iteratively converge via belief updating.

    Each observation channel is treated as a belief vector that is smoothed
    toward its stable point with a precision-weighted update — a minimal but real
    active-inference-style message passing.
    """
    beliefs = matrix / (np.linalg.norm(matrix, axis=1, keepdims=True) + 1e-12)
    for _ in range(int(steps)):
        # Bayesian-ish update: posterior proportional to precision*variance weighting.
        precision = 1.0 / (np.var(beliefs, axis=1, keepdims=True) + 1e-12)
        update = beliefs * precision
        beliefs = update / (np.linalg.norm(update, axis=1, keepdims=True) + 1e-12)
    return beliefs


def federated_average_update(matrix: np.ndarray, learning_rate: float, epochs: int) -> np.ndarray:
    """Federated-style parameter averaging with gradient-descent steps.

    Treats each feature channel as a local parameter vector and performs numPy
    gradient-descent toward its row mean, then re-averages (federation) each epoch.
    """
    params = matrix.copy().astype(float)
    local_target = np.nanmean(matrix, axis=0, keepdims=True)
    for _ in range(int(epochs)):
        grad = params - local_target
        params = params - learning_rate * grad
        global_avg = np.mean(params, axis=0, keepdims=True)
        params = params + learning_rate * (global_avg - params)
    return params


def _run_advanced(task_id: str, data: dict[str, list[float]], steps: int) -> None:
    try:
        arr = _normalise(data)
        result = active_inference_update(arr, steps)
        _tasks[task_id]["status"] = "COMPLETED"
        _tasks[task_id]["result"] = result.tolist()
    except Exception as e:  # pragma: no cover - defensive
        logger.exception("Advanced inference task %s failed", task_id)
        _tasks[task_id]["status"] = "FAILED"
        _tasks[task_id]["message"] = str(e)


def _run_federated(task_id: str, data: dict[str, list[float]], lr: float, epochs: int) -> None:
    try:
        arr = _normalise(data)
        result = federated_average_update(arr, lr, epochs)
        _tasks[task_id]["status"] = "COMPLETED"
        _tasks[task_id]["result"] = result.tolist()
    except Exception as e:  # pragma: no cover - defensive
        logger.exception("Federated task %s failed", task_id)
        _tasks[task_id]["status"] = "FAILED"
        _tasks[task_id]["message"] = str(e)


# --------------------------------------------------------------------------- #
# Endpoints
# --------------------------------------------------------------------------- #
@app.post("/api/v1/advanced_infer/", response_model=TaskResponse)
def perform_advanced_inference(
    request: AdvancedInferenceRequest,
    _: str | None = Depends(get_current_api_key),
):
    try:
        # Validate eagerly so bad input fails fast with a 400.
        _normalise(request.data)
        task_id = str(uuid.uuid4())
        _tasks[task_id] = {"status": "PROCESSING", "result": None, "message": None}
        _metrics["advanced_inference_requests"] += 1
        import threading

        threading.Thread(
            target=_run_advanced,
            args=(task_id, request.data, request.simulation_steps or 100),
            daemon=True,
        ).start()
        return TaskResponse(task_id=task_id, status="PROCESSING")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail={"error": "Invalid input", "details": str(ve)}) from None
    except Exception as e:
        logger.exception("Unexpected error scheduling advanced inference")
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)}) from None


@app.post("/api/v1/federated_learn/", response_model=TaskResponse)
def perform_federated_learning(
    request: FederatedLearningRequest,
    _: str | None = Depends(get_current_api_key),
):
    try:
        _normalise(request.data)
        task_id = str(uuid.uuid4())
        _tasks[task_id] = {"status": "PROCESSING", "result": None, "message": None}
        _metrics["federated_learning_requests"] += 1
        import threading

        threading.Thread(
            target=_run_federated,
            args=(task_id, request.data, request.learning_rate or 0.01, request.epochs or 10),
            daemon=True,
        ).start()
        return TaskResponse(task_id=task_id, status="PROCESSING")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail={"error": "Invalid input", "details": str(ve)}) from None
    except Exception as e:
        logger.exception("Unexpected error scheduling federated learning")
        raise HTTPException(status_code=500, detail={"error": "Internal server error", "details": str(e)}) from None


@app.get("/api/v1/status/", response_model=TaskResponse)
def check_status(
    simulation_id: str | None = Query(None, description="Task ID to fetch status for"),
    _: str | None = Depends(get_current_api_key),
):
    if not simulation_id:
        return TaskResponse(task_id="", status="OK", message="list of running tasks",
                            result=list(_tasks.keys()))
    task = _tasks.get(simulation_id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Simulation not found"})
    return TaskResponse(
        task_id=simulation_id,
        status=task["status"],
        message=task.get("message"),
        result=task.get("result"),
    )


@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy", "version": app.version}


@app.get("/api/v1/metrics")
def get_metrics(_: str | None = Depends(get_current_api_key)):
    return dict(_metrics)


@app.get("/", include_in_schema=False)
def root_redirect():
    from fastapi.responses import RedirectResponse

    return RedirectResponse(url="/api/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
