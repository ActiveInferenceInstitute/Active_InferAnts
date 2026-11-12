import csv
import json
import logging
from functools import lru_cache
from typing import Any, Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class CognitiveUtilities:
    """
    Provides cognitive utilities for field operators to analyze and interpret simulation data.
    Includes functions for behavioral analysis, cognitive load assessment, and decision support.
    """

    def __init__(
        self,
        simulation_data: Dict[str, Any],
        config: Dict[str, Any] = None,
        logger: logging.Logger = None,
    ) -> None:
        """
        Initializes the CognitiveUtilities with simulation data and optional configuration.

        Parameters
        ----------
        simulation_data : Dict[str, Any]
            The data generated from the simulation to be analyzed.
        config : Dict[str, Any], optional
            Configuration parameters for cognitive utilities, by default None.
        logger : logging.Logger, optional
            External logger for dependency injection, by default None.
        """
        self.simulation_data = simulation_data
        self.config = config or {"distance_threshold": 1000, "load_threshold": 50}
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.logger.info(
            "CognitiveUtilities initialized with simulation data and configuration."
        )
        self._validate_simulation_data()

    def _validate_simulation_data(self) -> None:
        """
        Validates the simulation data to ensure required fields are present.

        Raises
        ------
        ValueError
            If required data fields are missing or malformed.
        """
        required_agent_fields = {"id", "movements", "interactions"}
        agents = self.simulation_data.get("agents", [])
        for agent in agents:
            if not required_agent_fields.issubset(agent.keys()):
                self.logger.error(f"Agent data missing required fields: {agent}")
                raise ValueError(f"Agent data missing required fields: {agent}")
        self.logger.info("Simulation data validation passed.")

    @lru_cache(maxsize=1)
    def analyze_agent_behavior(self) -> Dict[str, Any]:
        """
        Analyzes the behavior patterns of agents within the simulation.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing behavioral metrics and insights.
        """
        self.logger.info("Starting agent behavior analysis.")
        agent_stats = {}
        agents = self.simulation_data.get("agents", [])
        for agent in agents:
            agent_id = agent.get("id")
            movements = agent.get("movements", [])
            total_distance = self._calculate_total_distance(movements)
            activity_levels = self._calculate_activity_levels(movements)
            agent_stats[agent_id] = {
                "total_distance": total_distance,
                "activity_levels": activity_levels,
            }
            self.logger.debug(
                f"Agent {agent_id}: Distance={total_distance}, Activity Levels={activity_levels}"
            )
        self.logger.info("Agent behavior analysis completed.")
        return agent_stats

    def _calculate_total_distance(self, movements: List[Tuple[float, float]]) -> float:
        """
        Calculates the total distance traveled based on movement coordinates.

        Parameters
        ----------
        movements : List[Tuple[float, float]]
            A list of (x, y) positions representing agent movements.

        Returns
        -------
        float
            The total distance traveled.
        """
        if not movements:
            return 0.0
        distance = 0.0
        for i in range(1, len(movements)):
            dx = movements[i][0] - movements[i - 1][0]
            dy = movements[i][1] - movements[i - 1][1]
            distance += np.sqrt(dx**2 + dy**2)
        return distance

    def _calculate_activity_levels(self, movements: List[Tuple[float, float]]) -> float:
        """
        Calculates the activity level based on the frequency of movements.

        Parameters
        ----------
        movements : List[Tuple[float, float]]
            A list of (x, y) positions representing agent movements.

        Returns
        -------
        float
            The activity level metric.
        """
        return len(movements)

    @lru_cache(maxsize=1)
    def evaluate_cognitive_load(self) -> Dict[str, float]:
        """
        Evaluates the cognitive load experienced by agents based on their interactions.

        Returns
        -------
        Dict[str, float]
            A dictionary mapping agent IDs to their cognitive load scores.
        """
        self.logger.info("Evaluating cognitive load for agents.")
        cognitive_load = {}
        agents = self.simulation_data.get("agents", [])
        for agent in agents:
            agent_id = agent.get("id")
            interactions = agent.get("interactions", [])
            load = self._compute_load(interactions)
            cognitive_load[agent_id] = load
            self.logger.debug(f"Agent {agent_id}: Cognitive Load={load}")
        self.logger.info("Cognitive load evaluation completed.")
        return cognitive_load

    def _compute_load(self, interactions: List[Dict[str, Any]]) -> float:
        """
        Computes cognitive load based on interactions.

        Parameters
        ----------
        interactions : List[Dict[str, Any]]
            A list of interaction events.

        Returns
        -------
        float
            The cognitive load score.
        """
        load = 0.0
        for interaction in interactions:
            load += interaction.get("complexity", 1.0)
        return load

    def generate_decision_support(self, agent_id: Any) -> Dict[str, Any]:
        """
        Provides decision support metrics and recommendations for a specific agent.

        Parameters
        ----------
        agent_id : Any
            The unique identifier of the agent.

        Returns
        -------
        Dict[str, Any]
            A dictionary containing decision support information.
        """
        self.logger.info(f"Generating decision support for Agent {agent_id}.")
        agent_data = next(
            (
                agent
                for agent in self.simulation_data.get("agents", [])
                if agent.get("id") == agent_id
            ),
            None,
        )
        if not agent_data:
            self.logger.error(f"Agent with ID {agent_id} not found.")
            return {}

        try:
            behavior = self.analyze_agent_behavior().get(agent_id, {})
            load = self.evaluate_cognitive_load().get(agent_id, 0.0)
        except Exception:
            self.logger.exception("Error during behavior or load analysis.")
            return {}

        recommendations = self._generate_recommendations(behavior, load)

        decision_support = {
            "agent_id": agent_id,
            "behavior_analysis": behavior,
            "cognitive_load": load,
            "recommendations": recommendations,
        }
        self.logger.info(f"Decision support generated for Agent {agent_id}.")
        return decision_support

    def _generate_recommendations(
        self, behavior: Dict[str, Any], load: float
    ) -> List[str]:
        """
        Generates recommendations based on behavior and cognitive load.

        Parameters
        ----------
        behavior : Dict[str, Any]
            The behavior analysis metrics.
        load : float
            The cognitive load score.

        Returns
        -------
        List[str]
            A list of recommendations.
        """
        recommendations = []
        distance_threshold = self.config.get("distance_threshold", 1000)
        load_threshold = self.config.get("load_threshold", 50)

        if behavior.get("total_distance", 0) > distance_threshold:
            recommendations.append(
                "Consider optimizing movement paths to reduce travel distance."
            )
        if load > load_threshold:
            recommendations.append("Review task complexity to manage cognitive load.")
        return recommendations

    def visualize_behavior_metrics(
        self,
        agent_stats: Dict[str, Any],
        save_path: str = None,
        metrics: List[str] = None,
    ) -> None:
        """
        Visualizes behavior metrics using matplotlib.

        Parameters
        ----------
        agent_stats : Dict[str, Any]
            The agent behavior statistics to visualize.
        save_path : str, optional
            Path to save the plot image, by default None.
        metrics : List[str], optional
            Specific metrics to display, by default None.
        """
        self.logger.info("Visualizing behavior metrics.")
        try:
            agents = list(agent_stats.keys())
            distances = [stats["total_distance"] for stats in agent_stats.values()]
            activity_levels = [
                stats["activity_levels"] for stats in agent_stats.values()
            ]

            fig, ax1 = plt.subplots(figsize=(10, 6))

            color = "tab:blue"
            ax1.set_xlabel("Agent ID")
            ax1.set_ylabel("Total Distance", color=color)
            ax1.bar(agents, distances, color=color, alpha=0.6, label="Total Distance")
            ax1.tick_params(axis="y", labelcolor=color)

            ax2 = ax1.twinx()
            color = "tab:red"
            ax2.set_ylabel("Activity Level", color=color)
            ax2.plot(
                agents, activity_levels, color=color, marker="o", label="Activity Level"
            )
            ax2.tick_params(axis="y", labelcolor=color)

            fig.tight_layout()
            plt.title("Agent Behavior Metrics")

            if save_path:
                plt.savefig(save_path)
                self.logger.info(f"Behavior metrics plot saved to {save_path}.")

            plt.show()
            self.logger.info("Behavior metrics visualization completed.")
        except Exception:
            self.logger.exception("Failed to visualize behavior metrics.")

    def visualize_cognitive_load_distribution(
        self, cognitive_load: Dict[str, float], save_path: str = None
    ) -> None:
        """
        Visualizes the distribution of cognitive load across agents using a histogram.

        Parameters
        ----------
        cognitive_load : Dict[str, float]
            The cognitive load scores for each agent.
        save_path : str, optional
            Path to save the plot image, by default None.
        """
        self.logger.info("Visualizing cognitive load distribution.")
        try:
            load_values = list(cognitive_load.values())
            plt.figure(figsize=(10, 6))
            plt.hist(load_values, bins=20, color="skyblue", edgecolor="black")
            plt.xlabel("Cognitive Load")
            plt.ylabel("Number of Agents")
            plt.title("Distribution of Cognitive Load Across Agents")

            if save_path:
                plt.savefig(save_path)
                self.logger.info(
                    f"Cognitive load distribution plot saved to {save_path}."
                )

            plt.show()
            self.logger.info("Cognitive load distribution visualization completed.")
        except Exception:
            self.logger.exception("Failed to visualize cognitive load distribution.")

    def summarize_cognitive_insights(
        self, agent_stats: Dict[str, Any], cognitive_load: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Summarizes cognitive insights for all agents.

        Parameters
        ----------
        agent_stats : Dict[str, Any]
            The agent behavior statistics.
        cognitive_load : Dict[str, float]
            The cognitive load scores for each agent.

        Returns
        -------
        Dict[str, Any]
            A summary of cognitive insights for each agent.
        """
        self.logger.info("Summarizing cognitive insights.")
        summary = {}
        for agent_id in agent_stats:
            summary[agent_id] = {
                "total_distance": agent_stats[agent_id]["total_distance"],
                "activity_levels": agent_stats[agent_id]["activity_levels"],
                "cognitive_load": cognitive_load.get(agent_id, 0.0),
                "recommendations": self._generate_recommendations(
                    agent_stats[agent_id], cognitive_load.get(agent_id, 0.0)
                ),
            }
        self.logger.info("Cognitive insights summary completed.")
        return summary

    def export_summary_to_json(self, summary: Dict[str, Any], file_path: str) -> None:
        """
        Exports the cognitive insights summary to a JSON file.

        Parameters
        ----------
        summary : Dict[str, Any]
            The cognitive insights summary.
        file_path : str
            The path to the JSON file to save the summary.
        """
        self.logger.info(f"Exporting summary to JSON file at {file_path}.")
        try:
            with open(file_path, "w") as f:
                json.dump(summary, f, indent=4)
            self.logger.info("Summary successfully exported to JSON.")
        except Exception:
            self.logger.exception("Failed to export summary to JSON.")

    def export_summary_to_csv(self, summary: Dict[str, Any], file_path: str) -> None:
        """
        Exports the cognitive insights summary to a CSV file.

        Parameters
        ----------
        summary : Dict[str, Any]
            The cognitive insights summary.
        file_path : str
            The path to the CSV file to save the summary.
        """
        self.logger.info(f"Exporting summary to CSV file at {file_path}.")
        try:
            with open(file_path, "w", newline="") as csvfile:
                fieldnames = [
                    "agent_id",
                    "total_distance",
                    "activity_levels",
                    "cognitive_load",
                    "recommendations",
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for agent_id, data in summary.items():
                    writer.writerow(
                        {
                            "agent_id": agent_id,
                            "total_distance": data["total_distance"],
                            "activity_levels": data["activity_levels"],
                            "cognitive_load": data["cognitive_load"],
                            "recommendations": "; ".join(data["recommendations"]),
                        }
                    )
            self.logger.info("Summary successfully exported to CSV.")
        except Exception:
            self.logger.exception("Failed to export summary to CSV.")

    def export_summary_to_excel(self, summary: Dict[str, Any], file_path: str) -> None:
        """
        Exports the cognitive insights summary to an Excel file.

        Parameters
        ----------
        summary : Dict[str, Any]
            The cognitive insights summary.
        file_path : str
            The path to the Excel file to save the summary.
        """
        self.logger.info(f"Exporting summary to Excel file at {file_path}.")
        try:
            data = []
            for agent_id, details in summary.items():
                data.append(
                    {
                        "Agent ID": agent_id,
                        "Total Distance": details["total_distance"],
                        "Activity Levels": details["activity_levels"],
                        "Cognitive Load": details["cognitive_load"],
                        "Recommendations": "; ".join(details["recommendations"]),
                    }
                )
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            self.logger.info("Summary successfully exported to Excel.")
        except Exception:
            self.logger.exception("Failed to export summary to Excel.")

    def load_config_from_file(self, config_path: str) -> None:
        """
        Loads configuration parameters from a JSON file.

        Parameters
        ----------
        config_path : str
            The path to the JSON configuration file.

        Raises
        ------
        FileNotFoundError
            If the configuration file does not exist.
        json.JSONDecodeError
            If the configuration file contains invalid JSON.
        """
        self.logger.info(f"Loading configuration from {config_path}.")
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
            self.config.update(config_data)
            self.logger.info("Configuration successfully loaded and updated.")
        except FileNotFoundError:
            self.logger.error(f"Configuration file {config_path} not found.")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in configuration file: {e}")
            raise

    def configure_logger(
        self,
        log_level: str = "INFO",
        log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    ) -> None:
        """
        Configures the logger with the specified log level and format.

        Parameters
        ----------
        log_level : str, optional
            The logging level (e.g., 'DEBUG', 'INFO'), by default 'INFO'.
        log_format : str, optional
            The logging format string, by default '%(asctime)s - %(name)s - %(levelname)s - %(message)s'.
        """
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            self.logger.error(f"Invalid log level: {log_level}")
            raise ValueError(f"Invalid log level: {log_level}")
        logging.basicConfig(level=numeric_level, format=log_format)
        self.logger.setLevel(numeric_level)
        self.logger.info(f"Logger configured to level {log_level}.")

    def reset_caches(self) -> None:
        """
        Clears the cached results of the analyze_agent_behavior and evaluate_cognitive_load methods.
        """
        self.analyze_agent_behavior.cache_clear()
        self.evaluate_cognitive_load.cache_clear()
        self.logger.info(
            "Caches for analyze_agent_behavior and evaluate_cognitive_load have been cleared."
        )

    def export_summary(
        self,
        summary: Dict[str, Any],
        json_path: str = None,
        csv_path: str = None,
        excel_path: str = None,
    ) -> None:
        """
        Exports the cognitive insights summary to various formats based on provided paths.

        Parameters
        ----------
        summary : Dict[str, Any]
            The cognitive insights summary.
        json_path : str, optional
            Path to save the JSON file, by default None.
        csv_path : str, optional
            Path to save the CSV file, by default None.
        excel_path : str, optional
            Path to save the Excel file, by default None.
        """
        if json_path:
            self.export_summary_to_json(summary, json_path)
        if csv_path:
            self.export_summary_to_csv(summary, csv_path)
        if excel_path:
            self.export_summary_to_excel(summary, excel_path)
