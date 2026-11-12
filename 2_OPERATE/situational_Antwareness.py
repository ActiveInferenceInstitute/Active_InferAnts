import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import entropy


class AgentVisualizer(ABC):
    """
    Enhances situational awareness by visualizing the internal state of ActiveInferenceAgent or its subclasses.
    Integrates simulation, execution, and rendering contexts for a comprehensive overview, adhering to Active Inference best practices.
    """

    def __init__(self, agent: Any) -> None:
        self.agent = agent
        self.required_attrs: List[str] = [
            "position",
            "influence_factor",
            "agent_params",
            "A_matrix",
            "B_matrix",
            "C_matrix",
            "D_matrix",
            "G_matrix",
            "F_matrix",
        ]
        self.matrices: List[str] = [
            "A_matrix",
            "B_matrix",
            "C_matrix",
            "D_matrix",
            "G_matrix",
            "F_matrix",
        ]
        self.agent_specific_info: Dict[str, Tuple[str, Callable]] = {
            "ActiveNestmate": ("Nestmate Config", lambda agent: agent.nestmate_config),
            "ActiveColony": ("Colony Config", lambda agent: agent.colony_config),
            "ActiveForager": (
                "Foraging Strategy",
                lambda agent: agent.foraging_strategy,
            ),
            "ActiveDefender": (
                "Defense Capabilities",
                lambda agent: agent.defense_capabilities,
            ),
        }
        self.visualization_dir = "agent_visualizations"
        self._setup_visualization_directory()

    def _setup_visualization_directory(self) -> None:
        import os

        if not os.path.exists(self.visualization_dir):
            os.makedirs(self.visualization_dir)

    def check_agent_attributes(self) -> bool:
        missing_attrs = [
            attr for attr in self.required_attrs if not hasattr(self.agent, attr)
        ]
        if missing_attrs:
            logging.error(
                f"Agent is missing required attributes: {', '.join(missing_attrs)}"
            )
            return False
        return True

    def log_basic_info(self) -> None:
        logging.info(
            f"Position: {self.agent.position} - The current position of the agent in the environment"
        )
        logging.info(
            f"Influence Factor: {self.agent.influence_factor} - A measure of the agent's influence on its surroundings"
        )
        logging.info(
            f"Agent Parameters: {self.agent.agent_params} - A dictionary of agent-specific parameters"
        )

    def log_matrices_info(self) -> None:
        for matrix in self.matrices:
            mat = getattr(self.agent, matrix)
            logging.info(f"{matrix}: Shape {mat.shape}, Size {mat.size}")
            self._visualize_matrix(matrix, mat)
            self._analyze_matrix_properties(matrix, mat)

    def _visualize_matrix(self, matrix_name: str, matrix: np.ndarray) -> None:
        plt.figure(figsize=(12, 10))
        sns.heatmap(matrix, annot=True, cmap="viridis", fmt=".2f")
        plt.title(f"{matrix_name} Visualization")
        plt.savefig(f"{self.visualization_dir}/{matrix_name}_visualization.png")
        plt.close()

    def _analyze_matrix_properties(self, matrix_name: str, matrix: np.ndarray) -> None:
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        matrix_entropy = entropy(matrix.flatten())
        condition_number = np.linalg.cond(matrix)
        logging.info(f"{matrix_name} Analysis:")
        logging.info(f"  - Eigenvalues: {eigenvalues}")
        logging.info(f"  - Matrix Entropy: {matrix_entropy}")
        logging.info(f"  - Condition Number: {condition_number}")
        self._visualize_matrix_properties(
            matrix_name, eigenvalues, matrix_entropy, condition_number
        )

    def _visualize_matrix_properties(
        self,
        matrix_name: str,
        eigenvalues: np.ndarray,
        matrix_entropy: float,
        condition_number: float,
    ) -> None:
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 1, 1)
        plt.bar(range(len(eigenvalues)), np.abs(eigenvalues))
        plt.title(f"{matrix_name} Eigenvalue Magnitudes")
        plt.subplot(2, 1, 2)
        plt.bar(
            ["Entropy", "Condition Number"],
            [matrix_entropy, np.log10(condition_number)],
        )
        plt.title(f"{matrix_name} Properties")
        plt.tight_layout()
        plt.savefig(f"{self.visualization_dir}/{matrix_name}_properties.png")
        plt.close()

    def log_agent_specific_info(self) -> None:
        agent_type_name = type(self.agent).__name__
        if agent_type_name in self.agent_specific_info:
            info_title, info_extractor = self.agent_specific_info[agent_type_name]
            specific_info = info_extractor(self.agent)
            logging.info(
                f"{agent_type_name} Specific Information: {info_title}: {specific_info}"
            )
            self._visualize_agent_specific_info(agent_type_name, specific_info)

    def _visualize_agent_specific_info(self, agent_type: str, info: Any) -> None:
        plt.figure(figsize=(12, 8))
        if isinstance(info, dict):
            plt.bar(info.keys(), info.values())
        elif isinstance(info, (list, np.ndarray)):
            plt.plot(info)
        elif isinstance(info, str):
            plt.text(0.5, 0.5, info, ha="center", va="center", fontsize=12)
            plt.axis("off")
        plt.title(f"{agent_type} Specific Information Visualization")
        plt.savefig(f"{self.visualization_dir}/{agent_type}_specific_info.png")
        plt.close()

    @abstractmethod
    def integrate_situational_awareness(self) -> None:
        pass

    def visualize(self) -> None:
        logging.info("Starting visualization of agent internals and context.")
        if not self.check_agent_attributes():
            logging.error("Visualization aborted due to missing agent attributes.")
            return
        self.log_basic_info()
        self.log_matrices_info()
        total_variables = len(self.required_attrs) + sum(
            getattr(self.agent, matrix).size for matrix in self.matrices
        )
        logging.info(f"Total Number of Variables: {total_variables}")
        logging.info(
            f"Total Size of Variables: {sum(getattr(self.agent, matrix).size for matrix in self.matrices)}"
        )
        self.log_agent_specific_info()
        self.integrate_situational_awareness()
        self._generate_summary_report()
        self._visualize_agent_state_evolution()
        logging.info("Visualization process completed successfully.")

    def _generate_summary_report(self) -> None:
        report = f"""
        Agent Visualization Summary Report
        ==================================
        Agent Type: {type(self.agent).__name__}
        Position: {self.agent.position}
        Influence Factor: {self.agent.influence_factor}
        Total Variables: {len(self.required_attrs) + sum(getattr(self.agent, matrix).size for matrix in self.matrices)}
        Matrix Sizes:
        {self._get_matrix_sizes()}
        Agent-Specific Information:
        {self._get_agent_specific_summary()}
        """
        with open(f"{self.visualization_dir}/agent_visualization_report.txt", "w") as f:
            f.write(report)

    def _get_matrix_sizes(self) -> str:
        return "\n".join(
            [
                f"  - {matrix}: {getattr(self.agent, matrix).shape}"
                for matrix in self.matrices
            ]
        )

    def _get_agent_specific_summary(self) -> str:
        agent_type_name = type(self.agent).__name__
        if agent_type_name in self.agent_specific_info:
            info_title, info_extractor = self.agent_specific_info[agent_type_name]
            return f"  - {info_title}: {info_extractor(self.agent)}"
        return "  No specific information available for this agent type."

    def _visualize_agent_state_evolution(self) -> None:
        """Visualizes the evolution of the agent's state over time."""
        if hasattr(self.agent, "get_state_history"):
            state_history = self.agent.get_state_history()
            plt.figure(figsize=(14, 10))
            for key, values in state_history.items():
                plt.plot(values, label=key)
            plt.title("Agent State Evolution Over Time")
            plt.xlabel("Time Steps")
            plt.ylabel("State Values")
            plt.legend()
            plt.grid(True)  # Added grid for better readability
            plt.savefig(f"{self.visualization_dir}/agent_state_evolution.png")
            plt.close()
        else:
            logging.warning(
                "Agent does not have a 'get_state_history' method. Skipping state evolution visualization."
            )


class ConcreteAgentVisualizer(AgentVisualizer):
    def integrate_situational_awareness(self) -> None:
        try:
            from execute_Simulation import SimulationExecutor
            from plan_Simulation import SimulationSetup
            from render_Simulation import SimulationRenderer

            simulation_context = SimulationSetup()
            execution_context = SimulationExecutor()
            rendering_context = SimulationRenderer(
                simulation_context.simulation_environment, [], []
            )

            logging.info(
                f"Simulation Environment: {simulation_context.simulation_environment}"
            )
            logging.info(
                f"Execution Parameters: Visualization Frequency - {execution_context.visualization_frequency}, Sleep Duration - {execution_context.sleep_duration}"
            )
            logging.info(
                f"Rendering Context: {rendering_context.fig.canvas.get_default_filename()}"
            )

            self._visualize_environment(simulation_context.simulation_environment)
            self._analyze_environment_dynamics(
                simulation_context.simulation_environment
            )
        except ImportError as e:
            logging.warning(
                f"Could not integrate broader situational awareness due to missing modules: {str(e)}"
            )

    def _visualize_environment(self, environment: Any) -> None:
        plt.figure(figsize=(14, 12))
        env_state = environment.get_state()
        sns.heatmap(env_state, cmap="terrain", annot=False, cbar=True)
        plt.title("Simulation Environment Visualization")
        plt.savefig(f"{self.visualization_dir}/environment_visualization.png")
        plt.close()

    def _analyze_environment_dynamics(self, environment: Any) -> None:
        if hasattr(environment, "get_resource_distribution"):
            resource_distribution = environment.get_resource_distribution()
            self._visualize_resource_distribution(resource_distribution)

        if hasattr(environment, "get_agent_density"):
            agent_density = environment.get_agent_density()
            self._visualize_agent_density(agent_density)

    def _visualize_resource_distribution(
        self, resource_distribution: np.ndarray
    ) -> None:
        plt.figure(figsize=(12, 10))
        sns.heatmap(resource_distribution, cmap="YlGnBu", annot=False)
        plt.title("Resource Distribution in Environment")
        plt.savefig(f"{self.visualization_dir}/resource_distribution.png")
        plt.close()

    def _visualize_agent_density(self, agent_density: np.ndarray) -> None:
        plt.figure(figsize=(12, 10))
        sns.heatmap(agent_density, cmap="Reds", annot=False)
        plt.title("Agent Density in Environment")
        plt.savefig(f"{self.visualization_dir}/agent_density.png")
        plt.close()


def create_agent_visualizer(agent: Any) -> AgentVisualizer:
    """
    Factory method to create an instance of ConcreteAgentVisualizer.

    Args:
        agent (Any): The agent instance to visualize.

    Returns:
        AgentVisualizer: An instance of ConcreteAgentVisualizer.
    """
    try:
        visualizer = ConcreteAgentVisualizer(agent)
        logging.info("ConcreteAgentVisualizer instance created successfully.")
        return visualizer
    except Exception as e:
        logging.error(f"Failed to create AgentVisualizer: {e}")
        raise
