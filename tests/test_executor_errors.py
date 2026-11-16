"""Required simulation failures propagate through cleanup and the script CLI."""

import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import matplotlib.pyplot as plt
import pytest
import execute_Simulation as execution
from environment import Environment
from error_handling import SimulationError
from MetaInformAnt_Simulation import MetaInformAntSimulation


@pytest.mark.parametrize("phase", ["initialization", "step", "report"])
def test_main_propagates_required_failures_and_cleans_owned_components(tmp_path, monkeypatch, phase):
    monkeypatch.chdir(tmp_path)
    environment = Environment(5, 5, max_steps=1, seed=0)
    simulation = MetaInformAntSimulation(1, environment, 1, 1, seed=0)
    failure = OSError(f"controlled {phase} failure")

    def create_simulation(**kwargs):
        if phase == "initialization":
            raise failure
        return simulation

    monkeypatch.setattr(execution, "SimulationPlanner", lambda **kwargs: SimpleNamespace(create_simulation=create_simulation))
    executor = execution.SimulationExecutor(visualization_interval=None, pause_duration=0, output_dir=str(tmp_path), max_steps=1)
    cleanup = []
    stop, finalize = executor.performance_monitor.stop, executor.data_logger.finalize

    def stopped():
        stop()
        cleanup.append("stop")

    def finalized():
        finalize()
        cleanup.append("finalize")

    monkeypatch.setattr(executor.performance_monitor, "stop", stopped)
    monkeypatch.setattr(executor.data_logger, "finalize", finalized)
    if phase == "step":
        def failed_progress():
            raise failure
        monkeypatch.setattr(simulation, "progress", failed_progress)
    if phase == "report":
        (tmp_path / "simulation_report.txt").mkdir()
    monkeypatch.setattr(execution, "SimulationExecutor", lambda: executor)
    with pytest.raises((SimulationError, OSError)):
        execution.main()
    assert cleanup == ["stop", "finalize"]
    if executor.renderer is not None:
        assert not plt.fignum_exists(executor.renderer.fig.number)
    if phase != "report":
        assert not (tmp_path / "simulation_report.txt").exists()


@pytest.mark.parametrize("blocked", [False, True])
def test_script_process_status_reflects_required_report_write(tmp_path, blocked):
    root = Path(__file__).resolve().parents[1]
    if blocked:
        (tmp_path / "simulation_report.txt").mkdir()
    code = """
import execute_Simulation as execution
import sys
original = execution.SimulationExecutor
execution.SimulationExecutor = lambda: original(
    visualization_interval=None, pause_duration=0,
    output_dir=sys.argv[1], max_steps=1,
)
execution.main()
"""
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join([str(root), str(root / "2_OPERATE"), str(root / "1_PREPARE" / "configs")])
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["MPLBACKEND"] = "Agg"
    result = subprocess.run([sys.executable, "-B", "-c", code, str(tmp_path)], cwd=tmp_path, env=environment, capture_output=True, text=True, timeout=30)
    if blocked:
        assert result.returncode != 0
        assert (tmp_path / "simulation_report.txt").is_dir()
    else:
        assert result.returncode == 0, result.stderr
        assert "Active InferAnts — Simulation Report" in (tmp_path / "simulation_report.txt").read_text()


def test_cleanup_failure_still_closes_figure_and_does_not_mask_primary_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    environment = Environment(5, 5, max_steps=1, seed=0)
    simulation = MetaInformAntSimulation(1, environment, 1, 1, seed=0)
    monkeypatch.setattr(execution, "SimulationPlanner", lambda **kwargs: SimpleNamespace(create_simulation=lambda **kwargs: simulation))
    executor = execution.SimulationExecutor(visualization_interval=None, pause_duration=0, output_dir=str(tmp_path), max_steps=1)
    (tmp_path / "simulation_report.txt").mkdir()
    finalized = []

    def stop():
        raise OSError("secondary cleanup failure")

    monkeypatch.setattr(executor.performance_monitor, "stop", stop)
    monkeypatch.setattr(executor.data_logger, "finalize", lambda: finalized.append(True))
    with pytest.raises(IsADirectoryError):
        executor.run()
    assert finalized == [True]
    assert not plt.fignum_exists(executor.renderer.fig.number)
