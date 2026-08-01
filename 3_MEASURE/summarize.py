import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import entropy
from typing import Dict, List, Any, Optional, Union
import seaborn as sns
from collections import Counter
import logging
from dataclasses import dataclass, field

@dataclass
class SimulationEntity:
    """
    Represents a simulation entity with various attributes.

    Attributes:
        energy (float): The energy level of the entity.
        type (str): The type of the entity.
        lifespan (int): The lifespan of the entity.
        distance_traveled (float): The distance traveled by the entity.
        food_collected (int): The amount of food collected by the entity.
    """
    energy: float = 0.0
    type: str = "default"
    lifespan: int = 0
    distance_traveled: float = 0.0
    food_collected: int = 0

@dataclass
class SimulationData:
    """
    Represents the simulation data containing agents, food sources, nests, and simulation steps.

    Attributes:
        agents (List[SimulationEntity]): List of simulation entities.
        food_sources (List[Dict[str, int]]): List of food sources with their amounts.
        nests (List[Dict[str, int]]): List of nests with their food collected and agent counts.
        simulation_steps (int): The number of simulation steps.
    """
    agents: List[SimulationEntity] = field(default_factory=list)
    food_sources: List[Dict[str, int]] = field(default_factory=list)
    nests: List[Dict[str, int]] = field(default_factory=list)
    simulation_steps: int = 0

class EnhancedSimulationSummary:
    """Class to generate a comprehensive summary of simulation results."""

    def __init__(self, simulation_results: Dict[str, Any]):
        """
        Initialize the EnhancedSimulationSummary with simulation results.

        Args:
            simulation_results (Dict[str, Any]): The raw simulation data.
        """
        self.data = SimulationData(
            agents=[SimulationEntity(**agent) for agent in simulation_results.get('agents', [])],
            food_sources=simulation_results.get('food_sources', []),
            nests=simulation_results.get('nests', []),
            simulation_steps=simulation_results.get('simulation_steps', 0)
        )
        self.logger = logging.getLogger(__name__)

    def generate_summary(self) -> Dict[str, Any]:
        """
        Generate a detailed summary of the simulation data.

        Returns:
            Dict[str, Any]: A dictionary containing summary statistics.
        """
        try:
            summary = {
                'total_agents': self._total_agents(),
                'total_food_sources': self._total_food_sources(),
                'total_nests': self._total_nests(),
                'average_agent_energy': self._average_agent_energy(),
                'total_food_collected': self._total_food_collected(),
                'simulation_steps': self.data.simulation_steps,
                'energy_statistics': self._energy_statistics(),
                'summary_by_agent_type': self._summary_by_agent_type(),
                'agents_entropy': self._agents_entropy(),
                'food_distribution': self._food_distribution(),
                'agent_lifespan': self._agent_lifespan(),
                'nest_efficiency': self._nest_efficiency(),
                'agent_movement': self._agent_movement()
            }
            return summary
        except ValueError as e:
            self.logger.error(f"Value error generating summary: {str(e)}")
            return {}
        except TypeError as e:
            self.logger.error(f"Type error generating summary: {str(e)}")
            return {}
        except Exception as e:
            self.logger.error(f"Unexpected error generating summary: {str(e)}")
            return {}

    def _total_agents(self) -> int:
        """
        Calculate the total number of agents in the simulation.

        Returns:
            int: The total number of agents.
        """
        return len(self.data.agents)

    def _total_food_sources(self) -> int:
        """
        Calculate the total number of food sources in the simulation.

        Returns:
            int: The total number of food sources.
        """
        return len(self.data.food_sources)

    def _total_nests(self) -> int:
        """
        Calculate the total number of nests in the simulation.

        Returns:
            int: The total number of nests.
        """
        return len(self.data.nests)

    def _average_agent_energy(self) -> float:
        """
        Calculate the average energy of all agents in the simulation.

        Returns:
            float: The average energy of agents.
        """
        return np.mean([agent.energy for agent in self.data.agents]) if self.data.agents else 0.0

    def _total_food_collected(self) -> int:
        """
        Calculate the total amount of food collected by all nests in the simulation.

        Returns:
            int: The total amount of food collected.
        """
        return sum(nest.get('food_collected', 0) for nest in self.data.nests)

    def _energy_statistics(self) -> Dict[str, float]:
        """
        Calculate various energy statistics for the agents in the simulation.

        Returns:
            Dict[str, float]: A dictionary containing energy statistics.
        """
        energies = [agent.energy for agent in self.data.agents]
        return {
            "mean_energy": np.mean(energies),
            "std_dev_energy": np.std(energies),
            "median_energy": np.median(energies),
            "min_energy": np.min(energies),
            "max_energy": np.max(energies)
        } if energies else {k: 0.0 for k in ["mean_energy", "std_dev_energy", "median_energy", "min_energy", "max_energy"]}

    def _summary_by_agent_type(self) -> Dict[str, Dict[str, Any]]:
        """
        Generate a summary of statistics for each agent type in the simulation.

        Returns:
            Dict[str, Dict[str, Any]]: A dictionary containing summary statistics by agent type.
        """
        summary = {}
        for agent in self.data.agents:
            summary.setdefault(agent.type, {'energy': [], 'count': 0, 'food_collected': 0})
            summary[agent.type]['energy'].append(agent.energy)
            summary[agent.type]['count'] += 1
            summary[agent.type]['food_collected'] += agent.food_collected
        
        for agent_type, stats in summary.items():
            stats['average_energy'] = np.mean(stats['energy']) if stats['energy'] else 0
            stats['efficiency'] = stats['food_collected'] / stats['count'] if stats['count'] else 0
        return summary

    def _agents_entropy(self) -> float:
        """
        Calculate the entropy of the agent-energy distribution in the simulation.

        Shannon entropy requires a valid probability distribution. scipy.stats.entropy
        interprets its input as probabilities, but raw energies (e.g. [10, 12, …]) are
        not normalized, so first normalise to a valid distribution.

        Returns:
            float: The entropy of agent energies (0 for a degenerate distribution).
        """
        energies = [agent.energy for agent in self.data.agents]
        if not energies:
            return 0.0
        energies = np.asarray(energies, dtype=float)
        total = np.sum(energies)
        if total <= 0:
            # No energy anywhere (or all-zero) → degenerate distribution, entropy 0.
            return 0.0
        distribution = energies / total
        return float(entropy(distribution))

    def _food_distribution(self) -> Dict[str, float]:
        """
        Calculate various food distribution statistics for the simulation.

        Returns:
            Dict[str, float]: A dictionary containing food distribution statistics.
        """
        food_amounts = [source.get('amount', 0) for source in self.data.food_sources]
        return {
            'total_food': sum(food_amounts),
            'average_food_per_source': np.mean(food_amounts),
            'max_food_in_source': max(food_amounts),
            'min_food_in_source': min(food_amounts)
        } if food_amounts else {k: 0.0 for k in ['total_food', 'average_food_per_source', 'max_food_in_source', 'min_food_in_source']}

    def _agent_lifespan(self) -> Dict[str, float]:
        """
        Calculate various lifespan statistics for the agents in the simulation.

        Returns:
            Dict[str, float]: A dictionary containing lifespan statistics.
        """
        lifespans = [agent.lifespan for agent in self.data.agents]
        return {
            'average_lifespan': np.mean(lifespans),
            'max_lifespan': max(lifespans),
            'min_lifespan': min(lifespans)
        } if lifespans else {k: 0.0 for k in ['average_lifespan', 'max_lifespan', 'min_lifespan']}

    def _nest_efficiency(self) -> Dict[str, float]:
        """
        Calculate various efficiency statistics for the nests in the simulation.

        Returns:
            Dict[str, float]: A dictionary containing efficiency statistics.
        """
        efficiencies = [nest.get('food_collected', 0) / nest.get('agents', 1) for nest in self.data.nests]
        return {
            'average_efficiency': np.mean(efficiencies),
            'max_efficiency': max(efficiencies),
            'min_efficiency': min(efficiencies)
        } if efficiencies else {k: 0.0 for k in ['average_efficiency', 'max_efficiency', 'min_efficiency']}

    def _agent_movement(self) -> Dict[str, float]:
        """
        Calculate various movement statistics for the agents in the simulation.

        Returns:
            Dict[str, float]: A dictionary containing movement statistics.
        """
        movements = [agent.distance_traveled for agent in self.data.agents]
        return {
            'average_movement': np.mean(movements),
            'max_movement': max(movements),
            'min_movement': min(movements)
        } if movements else {k: 0.0 for k in ['average_movement', 'max_movement', 'min_movement']}

def summarize_simulation(simulation_results: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a summary of the simulation results.

    Args:
        simulation_results (Dict[str, Any]): The raw simulation data.

    Returns:
        Dict[str, Any]: A dictionary containing summary statistics.
    """
    summary = EnhancedSimulationSummary(simulation_results)
    return summary.generate_summary()

def save_summary_to_file(summary: Dict[str, Any], file_path: str) -> None:
    """
    Save the summary to a text file.

    Args:
        summary (Dict[str, Any]): The summary data.
        file_path (str): The path to the output file.
    """
    try:
        with open(file_path, 'w') as file:
            for key, value in summary.items():
                file.write(f"{key}: {value}\n")
        logging.info(f"Summary saved to {file_path}")
    except IOError as e:
        logging.error(f"Error saving summary to file: {str(e)}")

def save_summary_to_csv(summary: Dict[str, Any], file_path: str) -> None:
    """
    Save the summary to a CSV file.

    Args:
        summary (Dict[str, Any]): The summary data.
        file_path (str): The path to the output CSV file.
    """
    try:
        pd.DataFrame.from_dict(summary, orient='index').to_csv(file_path, header=False)
        logging.info(f"Summary saved to CSV: {file_path}")
    except Exception as e:
        logging.error(f"Error saving summary to CSV: {str(e)}")

def plot_agent_energy_distribution(agents: List[SimulationEntity], file_path: str) -> None:
    """
    Plot the distribution of agent energies and save the plot to a file.

    Args:
        agents (List[SimulationEntity]): List of simulation entities.
        file_path (str): The path to the output plot file.
    """
    try:
        energies = [agent.energy for agent in agents]
        plt.figure(figsize=(10, 6))
        sns.histplot(energies, kde=True, color='skyblue', edgecolor='black')
        plt.title('Agent Energy Distribution')
        plt.xlabel('Energy')
        plt.ylabel('Frequency')
        plt.grid(axis='y', alpha=0.75)
        plt.savefig(file_path)
        plt.close()
        logging.info(f"Agent energy distribution plot saved to {file_path}")
    except Exception as e:
        logging.error(f"Error plotting agent energy distribution: {str(e)}")

def plot_agent_types(agents: List[SimulationEntity], file_path: str) -> None:
    """
    Plot the distribution of agent types and save the plot to a file.

    Args:
        agents (List[SimulationEntity]): List of simulation entities.
        file_path (str): The path to the output plot file.
    """
    try:
        agent_types = [agent.type for agent in agents]
        type_counts = Counter(agent_types)
        plt.figure(figsize=(10, 6))
        sns.barplot(x=list(type_counts.keys()), y=list(type_counts.values()))
        plt.title('Agent Types Distribution')
        plt.xlabel('Agent Type')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(file_path)
        plt.close()
        logging.info(f"Agent types distribution plot saved to {file_path}")
    except Exception as e:
        logging.error(f"Error plotting agent types: {str(e)}")

def plot_food_distribution(food_sources: List[Dict[str, int]], file_path: str) -> None:
    """
    Plot the distribution of food sources and save the plot to a file.

    Args:
        food_sources (List[Dict[str, int]]): List of food sources with their amounts.
        file_path (str): The path to the output plot file.
    """
    try:
        food_amounts = [source.get('amount', 0) for source in food_sources]
        plt.figure(figsize=(10, 6))
        sns.boxplot(y=food_amounts)
        plt.title('Food Distribution Across Sources')
        plt.ylabel('Food Amount')
        plt.savefig(file_path)
        plt.close()
        logging.info(f"Food distribution plot saved to {file_path}")
    except Exception as e:
        logging.error(f"Error plotting food distribution: {str(e)}")

def initialize_logging(log_level: Union[str, int] = logging.INFO):
    """
    Initialize logging with the specified level.

    Args:
        log_level (Union[str, int], optional): Logging level. Defaults to logging.INFO.
    """
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Example usage
if __name__ == "__main__":
    initialize_logging()
    
    simulation_results = {
        "agents": [
            {"energy": 10, "type": "worker", "lifespan": 100, "distance_traveled": 50, "food_collected": 2},
            {"energy": 12, "type": "scout", "lifespan": 120, "distance_traveled": 80, "food_collected": 1}
        ],
        "food_sources": [{"amount": 100}, {"amount": 150}, {"amount": 80}],
        "nests": [{"food_collected": 5, "agents": 10}, {"food_collected": 7, "agents": 8}],
        "simulation_steps": 1000
    }
    
    summary = summarize_simulation(simulation_results)
    save_summary_to_file(summary, "simulation_summary.txt")
    save_summary_to_csv(summary, "simulation_summary.csv")
    plot_agent_energy_distribution(SimulationData(**simulation_results).agents, "agent_energy_distribution.png")
    plot_agent_types(SimulationData(**simulation_results).agents, "agent_types_distribution.png")
    plot_food_distribution(simulation_results['food_sources'], "food_distribution.png")
