"""Tests for the 3_MEASURE correctness fixes."""

import importlib.util
import os

import numpy as np
import pandas as pd
import pytest

# NOTE: 3_MEASURE/statistics.py shadows the stdlib `statistics` module when the
# phase dir is on sys.path (which breaks seaborn's `from statistics import
# NormalDist`). Load it under a distinct module name to avoid the collision.
_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "3_MEASURE")


def _load(name, filename):
    spec = importlib.util.spec_from_file_location(
        name, os.path.join(_ROOT, filename)
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


categorization = _load("measure_categorization", "categorization.py")
summarize = _load("measure_summarize", "summarize.py")
statistics = _load("measure_statistics", "statistics.py")


# --- categorization.compute_colimit -----------------------------------------
def test_compute_colimit_stores_and_returns():
    c = categorization.CategoryTheoryAnalyzer()
    diagram = {"a": {1, 2}, "b": {2, 3}}
    result = c.compute_colimit(diagram)
    assert result == {1, 2, 3}
    assert c.colimits[str(diagram)] == {1, 2, 3}


def test_compute_colimit_dict_union():
    c = categorization.CategoryTheoryAnalyzer()
    result = c.compute_colimit({"a": {"x": 1}, "b": {"y": 2}})
    assert result == {"x": 1, "y": 2}


def test_compute_colimit_non_union_falls_back_to_pair():
    c = categorization.CategoryTheoryAnalyzer()
    result = c.compute_colimit({"a": 5, "b": "six"})
    assert result == (5, "six")


def test_compute_colimit_empty_raises():
    c = categorization.CategoryTheoryAnalyzer()
    with pytest.raises(ValueError):
        c.compute_colimit({})


# --- summarize entropy -------------------------------------------------------
def test_agents_entropy_is_normalised_shannon():
    s = summarize.EnhancedSimulationSummary(
        {"agents": [{"energy": 10.0}, {"energy": 10.0}, {"energy": 10.0}]}
    )
    # Uniform distribution -> maximum Shannon entropy for n=3: log(3).
    assert np.isclose(s._agents_entropy(), np.log(3), atol=1e-9)


def test_agents_entropy_degenerate_zero():
    s = summarize.EnhancedSimulationSummary({"agents": [{"energy": 0.0}, {"energy": 0.0}]})
    assert s._agents_entropy() == 0.0


# --- statistics alignment ----------------------------------------------------
def _frame():
    return pd.DataFrame(
        [
            {"category": "nests", "type": "nest", "simulation_steps": 1, "food_collected": 3, "energy": 0.0},
            {"category": "nests", "type": "nest", "simulation_steps": 2, "food_collected": 5, "energy": 0.0},
            {"category": "agents", "type": "worker", "simulation_steps": 1, "energy": 1.0, "food_collected": 0},
            # step 2 has NO agents -> the old code produced NaN for that step.
        ]
    )


def test_food_collection_no_nan_with_missing_agent_steps():
    st = statistics.EnhancedSimulationStatistics(_frame())
    food_trends, eff = st.analyze_food_collection()
    assert food_trends["collection_efficiency"].isna().sum() == 0
    assert np.isfinite(eff["mean"])


def test_food_collection_alignment_zero_fill():
    st = statistics.EnhancedSimulationStatistics(_frame())
    food_trends, _ = st.analyze_food_collection()
    # step 2 has food 2 (5-3) but no agents -> efficiency 0, not NaN.
    assert food_trends.loc[2, "collection_efficiency"] == 0
