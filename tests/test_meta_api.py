"""Tests for the MetaInformAnt API (engines + endpoints)."""

import time

import numpy as np
from fastapi.testclient import TestClient
from MetaInformAnt_API import (
    active_inference_update,
    app,
    federated_average_update,
)


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
        json={"data": {"f1": [1.0, 2.0], "f2": [3.0, 4.0]}, "learning_rate": 0.01, "epochs": 2},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "PROCESSING"


def test_health_check():
    client = TestClient(app)
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    assert r.json()["status"] == "healthy"
