"""Performance-metric calculation for the 2_OPERATE simulation pipeline.

``PerformanceTracker`` computes summary metrics from simulation results and
aggregates across multiple runs. The class name and method surface match the
contract used by ``plan_Simulation.py``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class PerformanceTracker:
    """Computes performance metrics from simulation result dictionaries."""

    def calculate_metrics(self, results: dict[str, Any]) -> dict[str, float]:
        """Return scalar metrics extracted from a results dictionary."""
        metrics: dict[str, float] = {}
        for key in ("mean_reward", "final_reward", "total_pheromone"):
            value = results.get(key)
            if value is not None:
                try:
                    metrics[key] = float(value)
                except (TypeError, ValueError):
                    continue
        metrics["step_count"] = float(results.get("step_count", 0))
        return metrics

    def calculate_aggregate_metrics(self, all_results: list[dict[str, Any]]) -> dict[str, float]:
        """Return cross-run aggregates (mean of per-run means, run count)."""
        if not all_results:
            return {"num_runs": 0.0, "mean_of_mean_rewards": 0.0}
        per_run = [self.calculate_metrics(r) for r in all_results]
        means = [m.get("mean_reward", 0.0) for m in per_run if "mean_reward" in m]
        return {
            "num_runs": float(len(all_results)),
            "mean_of_mean_rewards": float(sum(means) / len(means)) if means else 0.0,
        }
