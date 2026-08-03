"""Simulation planning for the 2_OPERATE pipeline.

``SimulationPlanner`` (aliased as ``SimulationSetup`` for backward
compatibility) reads the configuration from ``1_PREPARE/configs``, builds the
simulation environment, and constructs a ``MetaInformAntSimulation`` — the
object the executor drives and the renderer plots.

The pipeline is wired to the real ``active_infer_ants`` package for the
agent-side API and to ``environment.py`` for the grid world. Randomness is
seeded explicitly (no unseeded ``np.random`` calls).
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any

import numpy as np

# Allow running from the repository root or from 2_OPERATE directly:
# ``import config`` / ``import metaconfig`` resolve to 1_PREPARE/configs.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _path in (
    os.path.join(_REPO_ROOT, "1_PREPARE", "configs"),
    os.path.dirname(os.path.abspath(__file__)),
):
    if _path not in sys.path:
        sys.path.insert(0, _path)

import metaconfig  # noqa: E402
from computational_resources import estimate_computational_resources  # noqa: E402
from data_logging import DataLogger  # noqa: E402
from environment import Environment, build_environment_from_config  # noqa: E402
from exception_handling import SimulationExceptionHandler  # noqa: E402
from MetaInformAnt_Simulation import MetaInformAntSimulation  # noqa: E402
from performance_metrics import PerformanceTracker  # noqa: E402
from visualization import SimulationVisualizer  # noqa: E402

import config  # noqa: E402  (1_PREPARE/configs/config.py)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Default random seed when none is supplied. Kept deterministic so runs are
# reproducible out of the box.
_DEFAULT_SEED = 0


class SimulationPlanner:
    """Plans and builds an Active InferAnts simulation from configuration.

    Parameters
    ----------
    config_path:
        Optional path to a JSON config; when omitted the module-level
        ``config``/``metaconfig`` dictionaries are used.
    seed:
        Random seed for environment and agent initialization. ``None`` uses
        ``_DEFAULT_SEED`` for reproducibility.
    """

    def __init__(self, config_path: str | None = None, seed: int | None = None) -> None:
        self.config_path = config_path
        self.seed = _DEFAULT_SEED if seed is None else int(seed)
        self.rng = np.random.default_rng(self.seed)

        self.simulation_environment: Environment | None = None
        self.agent_params: dict[str, Any] = {}
        self.niche_params: dict[str, Any] = {}
        self.parallel_execution: dict[str, Any] = {
            "ENABLED": False,
            "WORKER_COUNT": 1,
        }
        self.computational_load: dict[str, Any] = {}
        self.data_logger = DataLogger()
        self.visualizer = SimulationVisualizer()
        self.performance_tracker = PerformanceTracker()
        self.exception_handler = SimulationExceptionHandler()

        self.initialize_components()

    # ------------------------------------------------------------------ #
    # Component initialization
    # ------------------------------------------------------------------ #
    def initialize_components(self) -> None:
        """Initialize all planning components from configuration."""
        settings = config.SIMULATION_SETTINGS
        environment_config = config.ENVIRONMENT_CONFIG
        self.simulation_environment = build_environment_from_config(settings, environment_config, seed=self.seed)
        self.agent_params = self.get_agent_params()
        self.niche_params = self.get_niche_params()
        self.parallel_execution = self.get_parallel_execution_settings()
        self.computational_load = self.estimate_computational_load()
        logger.info(
            "Simulation planned: %d agents, %d steps max, %d nests, seed=%d",
            settings.get("AGENT_COUNT", 100),
            settings.get("MAX_STEPS", 500),
            settings.get("NEST_COUNT", 1),
            self.seed,
        )

    def get_agent_params(self) -> dict[str, Any]:
        """Return agent parameters from the meta configuration (if present).

        The meta configuration does not currently define ``AGENT_PARAMS``;
        fall back to the consolidated ant/colony config so the planner never
        assumes a key that is not there.
        """
        ant_colony = metaconfig.META_CONFIG.get("ANT_AND_COLONY", {})
        params = ant_colony.get("AGENT_PARAMS")
        if isinstance(params, dict):
            return dict(params)
        nestmate = config.ANT_AND_COLONY_CONFIG.get("NESTMATE", {})
        active_inference = nestmate.get("ACTIVE_INFERENCE", {})
        # Only pass parameters the agent API actually accepts.
        known = ("sensory_precision", "prior_precision", "learning_rate")
        return {k: v for k, v in active_inference.items() if k in known}

    def get_niche_params(self) -> dict[str, Any]:
        """Return niche parameters from the meta configuration (if present)."""
        ant_colony = metaconfig.META_CONFIG.get("ANT_AND_COLONY", {})
        params = ant_colony.get("NICHE_PARAMS")
        return dict(params) if isinstance(params, dict) else {}

    def get_parallel_execution_settings(self) -> dict[str, Any]:
        """Return validated parallel-execution settings from the config."""
        settings = dict(config.SIMULATION_SETTINGS.get("PARALLEL_EXECUTION", {}))
        enabled = bool(settings.get("ENABLED", False))
        worker_count = int(settings.get("WORKER_COUNT", 1) or 1)
        agent_count = int(config.SIMULATION_SETTINGS.get("AGENT_COUNT", 1))
        if enabled and worker_count > agent_count:
            logger.warning(
                "Worker count (%d) exceeds agent count (%d); clamping",
                worker_count,
                agent_count,
            )
            worker_count = max(1, agent_count)
        return {"ENABLED": enabled, "WORKER_COUNT": worker_count}

    def estimate_computational_load(self) -> dict[str, Any]:
        """Estimate the computational cost of the planned run."""
        settings = config.SIMULATION_SETTINGS
        return estimate_computational_resources(
            num_agents=int(settings.get("AGENT_COUNT", 100)),
            num_food_sources=len(config.ENVIRONMENT_CONFIG.get("RESOURCE_ZONES", [])),
            num_nests=int(settings.get("NEST_COUNT", 1)),
            max_steps=int(settings.get("MAX_STEPS", 500)),
            parallel_execution=self.parallel_execution,
        )

    # ------------------------------------------------------------------ #
    # Simulation construction
    # ------------------------------------------------------------------ #
    def create_simulation(self, max_steps: int | None = None) -> MetaInformAntSimulation:
        """Create and return a configured ``MetaInformAntSimulation``."""
        if self.simulation_environment is None:
            self.initialize_components()
        assert self.simulation_environment is not None
        if max_steps is not None:
            self.simulation_environment.max_steps = int(max_steps)

        settings = config.SIMULATION_SETTINGS
        simulation = MetaInformAntSimulation(
            num_agents=int(settings.get("AGENT_COUNT", 100)),
            simulation_environment=self.simulation_environment,
            num_food_sources=len(config.ENVIRONMENT_CONFIG.get("RESOURCE_ZONES", [])),
            num_nests=int(settings.get("NEST_COUNT", 1)),
            agent_params=self.agent_params,
            niche_params=self.niche_params,
            data_logger=self.data_logger,
            visualizer=self.visualizer,
            performance_tracker=self.performance_tracker,
            seed=self.seed,
        )
        logger.info("Simulation instance created (max_steps=%d).", self.simulation_environment.max_steps)
        return simulation

    # ------------------------------------------------------------------ #
    # Execution helpers (used by the __main__ flow)
    # ------------------------------------------------------------------ #
    def prepare_simulation(self, max_steps: int | None = None) -> MetaInformAntSimulation:
        """Prepare the simulation and log the estimated computational load."""
        logger.info("Preparing simulation with current configuration.")
        simulation = self.create_simulation(max_steps=max_steps)
        logger.info("Estimated computational load: %s", self.computational_load)
        return simulation

    def run_simulation(self, max_steps: int | None = None) -> dict[str, Any]:
        """Run a single simulation and return the results."""
        simulation = self.prepare_simulation(max_steps=max_steps)
        max_steps = max_steps or simulation.environment.max_steps
        logger.info("Starting simulation for %d steps.", max_steps)
        try:
            results = simulation.run(max_steps)
            logger.info("Simulation completed successfully.")
        except Exception as e:  # noqa: BLE001 - pipeline degrades gracefully
            logger.error("Simulation failed: %s", e, exc_info=True)
            results = self.exception_handler.handle_simulation_error(e)
        self.post_simulation_analysis(results)
        return results

    def post_simulation_analysis(self, results: dict[str, Any]) -> None:
        """Persist results, generate plots, and log performance metrics."""
        self.data_logger.save_results(results)
        self.visualizer.create_summary_plots(results)
        metrics = self.performance_tracker.calculate_metrics(results)
        logger.info("Performance metrics: %s", metrics)

    def run_multiple_simulations(self, num_simulations: int) -> list[dict[str, Any]]:
        """Run several simulations sequentially and return all results."""
        if self.parallel_execution.get("ENABLED"):
            logger.warning(
                "Parallel execution is configured but runs are executed "
                "sequentially by the planner; parallel orchestration is a "
                "future enhancement."
            )
        all_results: list[dict[str, Any]] = []
        for i in range(max(0, int(num_simulations))):
            logger.info("Starting simulation %d of %d", i + 1, num_simulations)
            all_results.append(self.run_simulation())
        return all_results


# Backward-compatible alias: earlier documentation referred to the planning
# class as ``SimulationSetup``.
SimulationSetup = SimulationPlanner


if __name__ == "__main__":
    setup = SimulationPlanner()
    num_simulations = int(config.SIMULATION_SETTINGS.get("NUM_SIMULATIONS", 1) or 1)
    if num_simulations > 1:
        results_all = setup.run_multiple_simulations(num_simulations)
        logger.info("Completed %d simulations.", num_simulations)
        setup.data_logger.save_multiple_results(results_all)
        setup.visualizer.create_comparative_plots(results_all)
        aggregate = setup.performance_tracker.calculate_aggregate_metrics(results_all)
        logger.info("Aggregate performance metrics: %s", aggregate)
    else:
        results = setup.run_simulation()
        logger.info("Simulation completed.")
