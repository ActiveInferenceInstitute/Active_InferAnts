"""Simulation execution for the 2_OPERATE pipeline.

``SimulationExecutor`` drives the plan → execute → render lifecycle: it asks
the planner for a simulation, runs the time-stepped loop with monitoring, and
concludes with a report. The class name and method surface follow the
original pipeline contract.
"""

import logging
import os
import sys
import time
from collections.abc import Callable
from typing import Any

# Path bootstrap so the flat 2_OPERATE modules and 1_PREPARE/configs resolve
# when this file is run directly from the repository root.
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _path in (
    os.path.dirname(os.path.abspath(__file__)),
    os.path.join(_REPO_ROOT, "1_PREPARE", "configs"),
):
    if _path not in sys.path:
        sys.path.insert(0, _path)

from data_logging import DataLogger  # noqa: E402
from error_handling import SimulationError, handle_simulation_error  # noqa: E402
from performance_monitor import PerformanceMonitor  # noqa: E402
from plan_Simulation import SimulationPlanner  # noqa: E402
from render_Simulation import SimulationRenderer  # noqa: E402
from report_generator import ReportGenerator  # noqa: E402


class SimulationExecutor:
    """Executes and manages the simulation lifecycle.

    Parameters
    ----------
    visualization_interval:
        Steps between optional per-agent visualizations (``None`` disables).
    pause_duration:
        Pause between simulation steps (seconds).
    log_level:
        Logging level for the executor's logger.
    output_dir:
        Directory for the generated report.
    """

    def __init__(
        self,
        visualization_interval: int | None = 100,
        pause_duration: float = 0.1,
        log_level: int = logging.INFO,
        output_dir: str = "simulation_output",
        max_steps: int | None = None,
    ) -> None:
        self.simulation: Any = None
        self.renderer: SimulationRenderer | None = None
        self.visualization_interval = visualization_interval
        self.pause_duration = float(pause_duration)
        self.data_logger = DataLogger(output_dir=output_dir)
        self.performance_monitor = PerformanceMonitor()
        self.report_generator = ReportGenerator()
        self.output_dir = output_dir
        self.max_steps = max_steps
        self.configure_logging(log_level)

    def configure_logging(self, log_level: int) -> None:
        """Configure the executor's logger."""
        logging.basicConfig(
            level=log_level,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(self.__class__.__name__)

    def initialize_simulation(self) -> None:
        """Initialize the simulation and its renderer via the planner."""
        try:
            planner = SimulationPlanner(seed=0)
            self.simulation = planner.create_simulation(max_steps=self.max_steps)
            self.renderer = SimulationRenderer(*self.simulation.get_visualization_parameters())
            self.data_logger.initialize(self.simulation)
            self.performance_monitor.start()
            self.logger.info("Simulation initialized successfully.")
        except Exception as e:
            handle_simulation_error(e, "Simulation initialization failed")

    def initialize_environment(self) -> None:
        """Initialize the simulation environment safely."""
        self._safely_execute(
            self.renderer.initialize_environment if self.renderer else lambda: None,
            "Environment initialization",
        )

    def perform_simulation(self) -> None:
        """Execute the simulation steps with monitoring."""
        if not self.simulation:
            raise SimulationError("Simulation not initialized")

        max_steps: int = self.simulation.environment.max_steps
        self.logger.info("Simulation commencing for %d steps.", max_steps)

        for step in range(max_steps):
            self._safely_execute(
                lambda s=step: self._execute_simulation_step(s),
                f"Step {step} execution",
            )

            if self.performance_monitor.should_adjust_parameters(step):
                self._adjust_simulation_parameters()

            if self.simulation.should_terminate_early():
                self.logger.info("Early termination condition met at step %d", step)
                break

    def _execute_simulation_step(self, step: int) -> None:
        """Execute a single simulation step."""
        if not self.simulation or not self.renderer:
            raise SimulationError("Simulation or renderer not initialized")

        self.simulation.progress()
        self.data_logger.log_step(step, self.simulation)

        if self.visualization_interval is not None and step % self.visualization_interval == 0:
            self._optional_visualization(step)

        self.renderer.refresh_visualization(step)
        time.sleep(self.pause_duration)

    def _optional_visualization(self, step: int) -> None:
        """Perform optional per-agent visualization at the configured interval.

        The situational-awareness visualizer expects agents with matrix
        attributes (``A_matrix``, ``B_matrix`` ...) that the ``active_infer_ants``
        agents do not carry; failures here are logged and non-fatal.
        """
        self.logger.info("Optional data visualization at step %d", step)
        try:
            from situational_Antwareness import ConcreteAgentVisualizer

            for agent in self.simulation.agents:
                visualizer = ConcreteAgentVisualizer(agent)
                visualizer.visualize()
        except Exception as e:  # noqa: BLE001 - optional visualization
            self.logger.warning("Optional visualization skipped: %s", e)

    def _adjust_simulation_parameters(self) -> None:
        """Adjust simulation parameters based on performance-monitor advice."""
        if self.simulation:
            new_params: dict[str, Any] = self.performance_monitor.suggest_parameter_adjustments()
            if new_params:
                self.simulation.update_parameters(new_params)
                self.logger.info("Adjusted simulation parameters: %s", new_params)

    def conclude_simulation(self) -> None:
        """Conclude the simulation by finalizing components and reporting."""
        if not self.simulation or not self.renderer:
            raise SimulationError("Simulation or renderer not initialized")

        self._safely_execute(
            lambda: self.renderer.visualize_post_simulation(self.simulation.aggregate_results()),
            "Simulation conclusion",
        )
        self.data_logger.finalize()
        self.performance_monitor.stop()
        self._generate_final_report()

    def _generate_final_report(self) -> None:
        """Generate and save the final simulation report."""
        report_data: dict[str, Any] = {
            "simulation_data": self.data_logger.generate_report(),
            "performance_metrics": self.performance_monitor.get_metrics(),
            "simulation_parameters": self.simulation.get_parameters() if self.simulation else {},
            "environment_state": self.simulation.environment.get_state() if self.simulation else {},
        }
        report: str = self.report_generator.generate_report(report_data)
        self.logger.info("Final simulation report generated.")
        self._save_report(report)

    def _save_report(self, report: str) -> None:
        """Save the simulation report to a file in the output directory."""
        os.makedirs(self.output_dir, exist_ok=True)
        report_file = os.path.join(self.output_dir, "simulation_report.txt")
        try:
            with open(report_file, "w") as file:
                file.write(report)
            self.logger.info("Simulation report saved to %s", report_file)
        except OSError as e:
            self.logger.error("Failed to save simulation report: %s", e)

    def run(self) -> None:
        """Run the complete simulation sequence."""
        self.logger.info("Simulation sequence initiation.")
        simulation_steps: list[tuple[str, Callable[[], None]]] = [
            ("Simulation initialization", self.initialize_simulation),
            ("Environment initialization", self.initialize_environment),
            ("Simulation execution", self.perform_simulation),
            ("Simulation conclusion", self.conclude_simulation),
        ]

        for description, step_function in simulation_steps:
            self.logger.info("%s in progress.", description)
            step_function()

    def _safely_execute(self, operation: Callable[[], None], description: str) -> None:
        """Execute a callable operation safely, handling exceptions."""
        try:
            operation()
        except Exception as e:
            handle_simulation_error(e, f"{description} failed")


def main() -> None:
    """Entry point for executing the simulation."""
    executor = SimulationExecutor()
    try:
        executor.run()
    except SimulationError as se:
        logging.critical("Simulation failed: %s", se, exc_info=True)
    except Exception as e:
        logging.critical("Unexpected error: %s", e, exc_info=True)
    finally:
        # Perform necessary cleanup.
        if executor.performance_monitor:
            executor.performance_monitor.stop()
        if executor.data_logger:
            executor.data_logger.finalize()


if __name__ == "__main__":
    main()
