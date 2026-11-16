"""Tests for the MetaInformAnt API (engines + endpoints)."""

import json
import threading
import time

import MetaInformAnt_API as meta
import numpy as np
import pytest
from fastapi.testclient import TestClient
from MetaInformAnt_API import (
    active_inference_update,
    app,
    federated_average_update,
)


@pytest.fixture(autouse=True)
def isolated_task_state(monkeypatch):
    monkeypatch.setattr(meta, "_tasks", {})
    monkeypatch.setattr(
        meta,
        "_metrics",
        {"advanced_inference_requests": 0, "federated_learning_requests": 0},
    )
    yield
    deadline = time.monotonic() + 3
    while (
        any(task["status"] == "PROCESSING" for task in meta._tasks.values())
        and time.monotonic() < deadline
    ):
        time.sleep(0.01)
    assert all(task["status"] != "PROCESSING" for task in meta._tasks.values())


def test_active_inference_update_makes_rows_unit_norm():
    out = active_inference_update(np.array([[1.0, 2.0], [3.0, 4.0]]), 20)
    norms = np.linalg.norm(out, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-6)


def test_federated_update_shape_preserved():
    out = federated_average_update(np.array([[1.0, 2.0], [3.0, 4.0]]), 0.01, 5)
    assert out.shape == (2, 2)
    assert np.all(np.isfinite(out))


def test_advanced_inference_lifecycle():
    client = TestClient(app)
    r = client.post(
        "/api/v1/advanced_infer/",
        json={"data": {"f1": [0.1, 0.2], "f2": [0.3, 0.4]}, "simulation_steps": 5},
    )
    assert r.status_code == 200
    task_id = r.json()["task_id"]
    assert r.json()["status"] == "PROCESSING"
    status = None
    for _ in range(50):
        rs = client.get(f"/api/v1/status/?simulation_id={task_id}")
        if rs.json()["status"] == "COMPLETED":
            status = "COMPLETED"
            break
        time.sleep(0.05)
    assert status == "COMPLETED"
    res = rs.json()["result"]
    assert len(res) == 2 and len(res[0]) == 2


def test_federated_learning_endpoint():
    client = TestClient(app)
    r = client.post(
        "/api/v1/federated_learn/",
        json={
            "data": {"f1": [1.0, 2.0], "f2": [3.0, 4.0]},
            "learning_rate": 0.01,
            "epochs": 2,
        },
    )
    assert r.status_code == 200
    assert r.json()["status"] == "PROCESSING"


def test_health_check():
    client = TestClient(app)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"


@pytest.mark.parametrize(
    "route", ["/api/v1/advanced_infer/", "/api/v1/federated_learn/"]
)
@pytest.mark.parametrize(
    "data",
    [
        {},
        {"x": []},
        {"x": [1.0], "y": [2.0, 3.0]},
        {"x": [float("nan")]},
        {"x": [float("inf")]},
        {"x": [float("-inf")]},
    ],
)
def test_invalid_matrix_is_rejected_before_task_or_metric_creation(route, data):
    with TestClient(app) as client:
        response = client.post(
            route,
            content=json.dumps({"data": data}),
            headers={"Content-Type": "application/json"},
        )
    assert response.status_code in (400, 422)
    assert meta._tasks == {}
    assert meta._metrics == {
        "advanced_inference_requests": 0,
        "federated_learning_requests": 0,
    }


@pytest.mark.parametrize(
    "worker,engine,arguments",
    [
        ("_run_advanced", "active_inference_update", (1,)),
        ("_run_federated", "federated_average_update", (0.1, 1)),
    ],
)
def test_completion_is_published_only_after_serialization(
    monkeypatch, worker, engine, arguments
):
    entered, release = threading.Event(), threading.Event()

    class DelayedSerialization(np.ndarray):
        def tolist(self):
            entered.set()
            if not release.wait(3):
                raise TimeoutError("test serialization barrier")
            return super().tolist()

    result = np.array([[1.0, 2.0]]).view(DelayedSerialization)
    monkeypatch.setattr(meta, engine, lambda *args: result)
    meta._tasks["coherent"] = {"status": "PROCESSING", "result": None, "message": None}
    thread = threading.Thread(
        target=getattr(meta, worker),
        args=("coherent", np.array([[1.0, 2.0]]), *arguments),
    )
    thread.start()
    try:
        assert entered.wait(3)
        with TestClient(app) as client:
            before = client.get("/api/v1/status/?simulation_id=coherent").json()
        assert before["status"] == "PROCESSING" and before["result"] is None
    finally:
        release.set()
        thread.join(3)
    assert not thread.is_alive()
    with TestClient(app) as client:
        response = client.get("/api/v1/status/?simulation_id=coherent")
    assert response.status_code == 200
    assert response.json()["status"] == "COMPLETED"
    assert response.json()["result"] == [[1.0, 2.0]]
    json.dumps(response.json(), allow_nan=False)


@pytest.mark.parametrize(
    "worker,engine,arguments",
    [
        ("_run_advanced", "active_inference_update", (1,)),
        ("_run_federated", "federated_average_update", (0.1, 1)),
    ],
)
@pytest.mark.parametrize(
    "bad_result",
    [
        np.array([[np.nan]]),
        np.array([[np.inf]]),
        np.array([[1.0, 2.0]]),
        np.array([[1.0j]]),
    ],
)
def test_invalid_engine_result_becomes_json_safe_failure(
    monkeypatch, worker, engine, arguments, bad_result
):
    monkeypatch.setattr(meta, engine, lambda *args: bad_result)
    meta._tasks["invalid"] = {"status": "PROCESSING", "result": None, "message": None}
    getattr(meta, worker)("invalid", np.ones((1, 1)), *arguments)
    with TestClient(app) as client:
        response = client.get("/api/v1/status/?simulation_id=invalid")
    assert response.status_code == 200
    assert response.json()["status"] == "FAILED"
    assert response.json()["result"] is None
    assert response.json()["message"]
    json.dumps(response.json(), allow_nan=False)
