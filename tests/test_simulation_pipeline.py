"""Integration tests for the 2_OPERATE simulation pipeline (M-4).

Verifies that the plan → execute → render pipeline is importable, seeded, and
runs end-to-end against the real ``active_infer_ants`` package and the
2_OPERATE support modules. Matplotlib runs under the Agg backend (set in
``conftest.py``).
"""

import os

import pytest
from computational_resources import estimate_computational_resources  # noqa: E402
from data_logging import DataLogger  # noqa: E402

# The flat 2_OPERATE modules are added to sys.path by conftest.py.
from environment import Environment, build_environment_from_config  # noqa: E402
from error_handling import SimulationError, handle_simulation_error  # noqa: E402
from exception_handling import SimulationExceptionHandler  # noqa: E402
from execute_Simulation import SimulationExecutor  # noqa: E402
from MetaInformAnt_Simulation import MetaInformAntSimulation  # noqa: E402
from performance_metrics import PerformanceTracker  # noqa: E402
from plan_Simulation import SimulationPlanner, SimulationSetup  # noqa: E402
from report_generator import ReportGenerator  # noqa: E402


@pytest.fixture()
def small_environment(tmp_path):
    return Environment(
        width=20,
        height=20,
        max_steps=10,
        num_food_sources=2,
        num_nests=1,
        pheromone_decay=0.01,
        seed=0,
    )


def test_environment_contract(small_environment):
    """The environment satisfies the renderer/executor contract."""
    env = small_environment
    assert env.width == 20
    assert env.height == 20
    assert env.max_steps == 10
    assert env.get_pheromone_levels().shape == (20, 20)
    assert env.get_state()["steps"] == 0
    env.deposit_pheromone(5, 5, 1.0)
    env.step()
    assert env.get_state()["steps"] == 1
    assert env.get_pheromone_levels()[5, 5] > 0


def test_simulation_runs_and_is_seeded(small_environment):
    """MetaInformAntSimulation runs and is reproducible for a fixed seed."""
    sim = MetaInformAntSimulation(
        num_agents=4,
        simulation_environment=small_environment,
        num_food_sources=2,
        num_nests=1,
        seed=0,
    )
    results = sim.run(max_steps=10)
    assert results["step_count"] == 10
    assert results["num_agents"] == 4
    assert 0.0 <= results["mean_reward"] <= 1.0
    assert results["early_terminated"] is False
    assert "environment" in results

    # Reproducibility: same seed -> same final positions.
    sim_b = MetaInformAntSimulation(
        num_agents=4,
        simulation_environment=Environment(20, 20, 10, 2, 1, seed=0),
        num_food_sources=2,
        num_nests=1,
        seed=0,
    )
    sim_b.run(max_steps=10)
    assert sim_b.positions == sim.positions


def test_planner_builds_simulation_and_aliases(tmp_path):
    """SimulationPlanner builds a runnable simulation; SimulationSetup aliases it."""
    planner = SimulationPlanner(seed=0)
    sim = planner.create_simulation(max_steps=8)
    results = sim.run(max_steps=8)
    assert results["step_count"] == 8
    assert SimulationSetup is SimulationPlanner
    # Visualization parameters match the renderer contract: (env, nests, agents).
    env, nests, agents = sim.get_visualization_parameters()
    assert env is sim.environment
    assert len(nests) >= 1
    assert len(agents) == sim.num_agents


def test_executor_runs_pipeline_end_to_end(tmp_path):
    """SimulationExecutor runs plan → execute → render and writes a report."""
    executor = SimulationExecutor(
        visualization_interval=None,
        pause_duration=0.0,
        output_dir=str(tmp_path),
        max_steps=10,
    )
    executor.run()
    assert executor.simulation is not None
    assert executor.simulation.step_count == 10
    report_file = os.path.join(str(tmp_path), "simulation_report.txt")
    assert os.path.exists(report_file)
    with open(report_file) as fh:
        assert "Active InferAnts — Simulation Report" in fh.read()


def test_support_modules(tmp_path):
    """The observability/error/report modules behave as documented."""
    logger = DataLogger(output_dir=str(tmp_path))
    logger.initialize(None)
    logger.log_step(0, None)
    assert logger.generate_report()["result_count"] == 1
    path = logger.save_results({"mean_reward": 0.5})
    assert os.path.exists(path)

    tracker = PerformanceTracker()
    metrics = tracker.calculate_metrics({"mean_reward": 0.5, "step_count": 3})
    assert metrics["mean_reward"] == 0.5
    agg = tracker.calculate_aggregate_metrics([{"mean_reward": 0.4}, {"mean_reward": 0.6}])
    assert agg["mean_of_mean_rewards"] == 0.5
    assert agg["num_runs"] == 2.0

    handler = SimulationExceptionHandler()
    failed = handler.handle_simulation_error(RuntimeError("boom"))
    assert failed["failed"] is True
    assert "boom" in failed["error"]

    report = ReportGenerator().generate_report({"section": {"k": 1}})
    assert "[section]" in report and "k: 1" in report

    estimate = estimate_computational_resources(
        num_agents=10,
        num_food_sources=2,
        num_nests=1,
        max_steps=5,
        parallel_execution={"ENABLED": True, "WORKER_COUNT": 2},
    )
    assert estimate["estimated_agent_steps"] == 50
    assert estimate["parallel_enabled"] is True


def test_error_handling_raises():
    """handle_simulation_error always re-raises as SimulationError."""
    with pytest.raises(SimulationError):
        handle_simulation_error(ValueError("bad"), "test context")


def test_build_environment_from_config():
    """The config-driven builder extracts the fields the grid needs."""
    settings = {"MAX_STEPS": 30, "NEST_COUNT": 2}
    env_config = {
        "GRID": {"WIDTH": 15, "HEIGHT": 25},
        "RESOURCE_ZONES": [{"TYPE": "food"}, {"TYPE": "water"}],
        "PHEROMONE_CONFIG": {"DECAY_RATE": 0.05},
    }
    env = build_environment_from_config(settings, env_config, seed=1)
    assert env.width == 15
    assert env.height == 25
    assert env.max_steps == 30
    assert len(env.food_sources) == 2
    assert env.pheromone_decay == 0.05
