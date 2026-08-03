"""Summary visualization for the 2_OPERATE simulation pipeline.

``SimulationVisualizer`` produces static summary plots from results
dictionaries (reward trajectories, aggregate comparisons). The class name and
method surface match the contract used by ``plan_Simulation.py``.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)


class SimulationVisualizer:
    """Creates and saves summary plots from simulation results."""

    def __init__(self, output_dir: str = "simulation_output") -> None:
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def create_summary_plots(self, results: dict[str, Any]) -> str:
        """Save a summary plot for a single results dictionary.

        Returns the path of the saved figure. The plot is intentionally
        simple (matplotlib only) so it renders headless and in CI.
        """
        import matplotlib

        matplotlib.use("Agg", force=False)
        import matplotlib.pyplot as plt

        rewards = results.get("rewards", [])
        fig, ax = plt.subplots(figsize=(8, 4))
        if rewards:
            ax.plot(rewards, label="reward")
            ax.set_xlabel("step")
            ax.set_ylabel("reward")
        ax.set_title("Active InferAnts — simulation summary")
        ax.grid(True, linestyle="--", alpha=0.5)
        if rewards:
            ax.legend()
        path = os.path.join(self.output_dir, "simulation_summary.png")
        fig.savefig(path, dpi=120)
        plt.close(fig)
        logger.info("Summary plot saved to %s", path)
        return path

    def create_comparative_plots(self, all_results: list[dict[str, Any]]) -> str:
        """Save a comparison plot across multiple runs (mean reward per run)."""
        import matplotlib

        matplotlib.use("Agg", force=False)
        import matplotlib.pyplot as plt

        means = [float(r.get("mean_reward", 0.0)) for r in all_results if isinstance(r, dict)]
        fig, ax = plt.subplots(figsize=(8, 4))
        if means:
            ax.bar(range(len(means)), means)
            ax.set_xlabel("run")
            ax.set_ylabel("mean reward")
        ax.set_title("Active InferAnts — cross-run comparison")
        path = os.path.join(self.output_dir, "simulation_comparison.png")
        fig.savefig(path, dpi=120)
        plt.close(fig)
        logger.info("Comparison plot saved to %s", path)
        return path
