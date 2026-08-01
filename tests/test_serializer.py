"""Tests for the restricted-unpickler security fix in Serializer."""

import pickle

import numpy as np
import pytest
from serializer import restricted_loads


def test_legit_dict_round_trips():
    payload = {"version": "2.0.0", "config": {"lr": 0.1}}
    assert restricted_loads(pickle.dumps(payload))["config"] == {"lr": 0.1}


def test_numpy_array_round_trips():
    arr = restricted_loads(pickle.dumps({"a": np.array([1, 2, 3])}))["a"]
    assert isinstance(arr, np.ndarray)
    assert arr.tolist() == [1, 2, 3]


def test_hostile_payload_is_rejected():
    class Evil:
        def __reduce__(self):
            import subprocess

            return (subprocess.Popen, (["echo", "pwned"],))

    with pytest.raises(pickle.UnpicklingError):
        restricted_loads(pickle.dumps(Evil()))


def test_hostile_datetime_global_is_rejected():
    # A payload referencing a class outside the allowlist (datetime) must be
    # rejected, proving globals are gated.
    import datetime

    with pytest.raises(pickle.UnpicklingError):
        restricted_loads(pickle.dumps(datetime.datetime(2026, 1, 1)))
