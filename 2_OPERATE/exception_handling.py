"""Exception-handling facade for the 2_OPERATE simulation pipeline.

``SimulationExceptionHandler`` mirrors the error-handling contract used by
``plan_Simulation.py`` (which calls ``handle_simulation_error`` on the
handler instance). It logs the failure and returns a fail-closed results
dictionary so the pipeline can degrade gracefully.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SimulationExceptionHandler:
    """Handles simulation errors and produces a fail-closed results payload."""

    def handle_simulation_error(self, error: Exception) -> dict[str, Any]:
        """Log an exception and return a fail-closed results dictionary.

        The returned dictionary marks the run as failed and carries the error
        message; consumers (e.g. the data logger) can persist it.
        """
        logger.error("Simulation failed: %s", error, exc_info=True)
        return {
            "step_count": 0,
            "num_agents": 0,
            "mean_reward": 0.0,
            "final_reward": 0.0,
            "total_pheromone": 0.0,
            "early_terminated": False,
            "failed": True,
            "error": str(error),
        }
