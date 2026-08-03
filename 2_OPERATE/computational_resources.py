"""Computational-resource estimation for the 2_OPERATE pipeline.

``estimate_computational_resources`` returns a rough, honest estimate of the
cost of a run based on the configured dimensions. It is advisory only: the
pipeline never hard-depends on these numbers.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


def estimate_computational_resources(
    num_agents: int,
    num_food_sources: int,
    num_nests: int,
    max_steps: int,
    parallel_execution: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Estimate the computational cost of a simulation run.

    The estimate counts agent-steps (the dominant loop) and adds a heuristic
    memory figure based on the pheromone grid. ``parallel_execution`` is
    reported through but does not change the arithmetic.
    """
    num_agents = max(0, int(num_agents))
    max_steps = max(0, int(max_steps))
    parallel_execution = parallel_execution or {}

    agent_steps = num_agents * max_steps
    estimate: dict[str, Any] = {
        "num_agents": num_agents,
        "num_food_sources": int(num_food_sources),
        "num_nests": int(num_nests),
        "max_steps": max_steps,
        "estimated_agent_steps": agent_steps,
        "estimated_grid_cells": max(1, 100 * 100),  # default grid; see environment.py
        "parallel_enabled": bool(parallel_execution.get("ENABLED", False)),
        "worker_count": int(parallel_execution.get("WORKER_COUNT", 1) or 1),
    }
    logger.debug("Computational resource estimate: %s", estimate)
    return estimate
