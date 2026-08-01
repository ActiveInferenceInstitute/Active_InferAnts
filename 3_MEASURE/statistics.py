import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional, Tuple
from scipy import stats
from dataclasses import dataclass
import os
from abc import ABC, abstractmethod
import logging  # Added for logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class SimulationSummary:
    total_agents: int
    total_food_sources: int
    total_nests: int
    total_food_collected: float
    simulation_steps: int
    average_energy: float
    energy_std_dev: float
    energy_median: float
    energy_min: float
    energy_max: float
    energy_skewness: float
    energy_kurtosis: float

class StatisticalAnalysis(ABC):
    @abstractmethod
    def compute_summary(self) -> Any:
        pass

    @abstractmethod
    def visualize(self, file_path: str) -> None:
        pass

class EnhancedSimulationStatistics(StatisticalAnalysis):  # Inherit from StatisticalAnalysis
    def __init__(self, simulation_results: pd.DataFrame):
        """
        Initializes the EnhancedSimulationStatistics with simulation results.

        Parameters:
        - simulation_results (pd.DataFrame): A DataFrame containing the simulation results.
        """
        self.results = simulation_results if isinstance(simulation_results, pd.DataFrame) else pd.DataFrame(simulation_results)
        self._validate_data()
        logging.info("EnhancedSimulationStatistics initialized successfully.")

    def _validate_data(self) -> None:
        """
        Validates the input data to ensure it contains the required columns and data types.
        Raises ValueError if the data is invalid.
        """
        required_columns = ['category', 'type', 'energy', 'food_collected', 'simulation_steps']
        missing_columns = [col for col in required_columns if col not in self.results.columns]
        if missing_columns:
            logging.error(f"Missing required columns: {missing_columns}")
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        valid_categories = {'agents', 'food_sources', 'nests'}
        if not set(self.results['category']).issubset(valid_categories):
            logging.error("Invalid categories found in the data.")
            raise ValueError("Invalid categories in the data")
        logging.info("Data validation passed.")

    def compute_summary(self) -> SimulationSummary:
        """
        Computes comprehensive summary statistics from the simulation results.

        Returns:
        - SimulationSummary: A dataclass containing summary statistics.
        """
        logging.info("Computing summary statistics.")
        return self.compute_summary_statistics()

    def visualize(self, file_path: str) -> None:
        """
        Generates and saves all relevant visualizations.

        Parameters:
        - file_path (str): The directory path to save the visualizations.
        """
        logging.info("Generating visualizations.")
        self.generate_comprehensive_report(file_path)

    def compute_summary_statistics(self) -> SimulationSummary:
        """
        Computes comprehensive summary statistics from the simulation results.

        Returns:
        - SimulationSummary: A dataclass containing summary statistics.
        """
        agents_data = self.results.query("category == 'agents'")
        nests_data = self.results.query("category == 'nests'")

        summary = SimulationSummary(
            total_agents=len(agents_data),
            total_food_sources=len(self.results.query("category == 'food_sources'")),
            total_nests=len(nests_data),
            total_food_collected=nests_data['food_collected'].sum(),
            simulation_steps=self.results['simulation_steps'].iloc[0],
            average_energy=agents_data['energy'].mean(),
            energy_std_dev=agents_data['energy'].std(),
            energy_median=agents_data['energy'].median(),
            energy_min=agents_data['energy'].min(),
            energy_max=agents_data['energy'].max(),
            energy_skewness=stats.skew(agents_data['energy']),
            energy_kurtosis=stats.kurtosis(agents_data['energy'])
        )
        logging.debug(f"Summary statistics: {summary}")
        return summary

    def compute_agent_type_statistics(self) -> pd.DataFrame:
        """
        Computes detailed statistics for each agent type.

        Returns:
        - pd.DataFrame: A DataFrame containing statistics for each agent type.
        """
        agent_stats = self.results.query("category == 'agents'").groupby('type')['energy'].agg([
            'count', 'mean', 'median', 'min', 'max', 'std',
            ('skewness', lambda x: stats.skew(x)),
            ('kurtosis', lambda x: stats.kurtosis(x))
        ])
        return agent_stats

    def visualize_agent_energy_distribution(self, file_path: str, agent_types: Optional[List[str]] = None) -> None:
        """
        Visualizes the distribution of agent energy, optionally for specific agent types.

        Parameters:
        - file_path (str): The file path to save the plot.
        - agent_types (Optional[List[str]]): List of agent types to include in the visualization.
        """
        agent_data = self.results.query("category == 'agents'")
        if agent_types:
            agent_data = agent_data[agent_data['type'].isin(agent_types)]

        plt.figure(figsize=(12, 8))
        sns.histplot(data=agent_data, x='energy', hue='type', kde=True, multiple="stack")
        plt.xlabel('Agent Energy', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.title('Agent Energy Distribution by Type', fontsize=16)
        plt.legend(title='Agent Type', title_fontsize='13', fontsize='11')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()

    def analyze_energy_trends(self) -> pd.DataFrame:
        """
        Analyzes energy trends over simulation steps.

        Returns:
        - pd.DataFrame: A DataFrame containing energy statistics for each simulation step.
        """
        energy_trends = self.results.query("category == 'agents'").groupby('simulation_steps')['energy'].agg([
            'mean', 'median', 'min', 'max', 'std',
            ('skewness', lambda x: stats.skew(x)),
            ('kurtosis', lambda x: stats.kurtosis(x))
        ])
        return energy_trends

    def visualize_energy_trends(self, file_path: str) -> None:
        """
        Visualizes energy trends over simulation steps.

        Parameters:
        - file_path (str): The file path to save the plot.
        """
        energy_trends = self.analyze_energy_trends()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)
        
        # Plot mean and median energy
        ax1.plot(energy_trends.index, energy_trends['mean'], label='Mean Energy')
        ax1.fill_between(energy_trends.index, 
                         energy_trends['mean'] - energy_trends['std'],
                         energy_trends['mean'] + energy_trends['std'],
                         alpha=0.3, label='Standard Deviation')
        ax1.plot(energy_trends.index, energy_trends['median'], label='Median Energy', linestyle='--')
        ax1.set_ylabel('Energy', fontsize=14)
        ax1.set_title('Agent Energy Trends Over Simulation', fontsize=16)
        ax1.legend(fontsize=12)
        ax1.grid(True, linestyle=':', alpha=0.7)
        
        # Plot skewness and kurtosis
        ax2.plot(energy_trends.index, energy_trends['skewness'], label='Skewness', color='green')
        ax2.plot(energy_trends.index, energy_trends['kurtosis'], label='Kurtosis', color='purple')
        ax2.set_xlabel('Simulation Steps', fontsize=14)
        ax2.set_ylabel('Value', fontsize=14)
        ax2.set_title('Energy Distribution Shape Over Simulation', fontsize=16)
        ax2.legend(fontsize=12)
        ax2.grid(True, linestyle=':', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()

    def analyze_food_collection(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Analyzes food collection trends and efficiency.

        Returns:
        - Tuple[pd.DataFrame, pd.DataFrame]: DataFrames containing food collection trends and efficiency statistics.
        """
        food_trends = self.results.query("category == 'nests'").groupby('simulation_steps')['food_collected'].sum().diff().fillna(0)
        food_trends = food_trends.to_frame(name='food_collected_per_step')
        
        agent_counts = self.results.query("category == 'agents'").groupby('simulation_steps').size()
        # Reindex the agent counts onto the food-trend index so the division below
        # can never produce NaN from misaligned index sets (steps present in one
        # grouping but not the other). Missing counts become 0.
        agent_counts = agent_counts.reindex(food_trends.index).fillna(0)
        food_efficiency = food_trends['food_collected_per_step'] / agent_counts.replace(0, np.nan)
        food_trends['collection_efficiency'] = food_efficiency.fillna(0)
        
        efficiency_stats = food_trends['collection_efficiency'].agg(['mean', 'median', 'std', 'min', 'max'])
        
        return food_trends, efficiency_stats

    def visualize_food_collection(self, file_path: str) -> None:
        """
        Visualizes food collection trends and efficiency.

        Parameters:
        - file_path (str): The file path to save the plot.
        """
        food_trends, _ = self.analyze_food_collection()
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16), sharex=True)
        
        ax1.plot(food_trends.index, food_trends['food_collected_per_step'], label='Food Collected')
        ax1.set_ylabel('Food Collected per Step', fontsize=14)
        ax1.set_title('Food Collection Trends', fontsize=16)
        ax1.legend(fontsize=12)
        ax1.grid(True, linestyle=':', alpha=0.7)
        
        ax2.plot(food_trends.index, food_trends['collection_efficiency'], label='Collection Efficiency', color='orange')
        ax2.set_xlabel('Simulation Steps', fontsize=14)
        ax2.set_ylabel('Food Collected per Agent', fontsize=14)
        ax2.set_title('Food Collection Efficiency', fontsize=16)
        ax2.legend(fontsize=12)
        ax2.grid(True, linestyle=':', alpha=0.7)
        
        plt.tight_layout()
        plt.savefig(file_path, dpi=300)
        plt.close()

    def generate_comprehensive_report(self, output_dir: str) -> None:
        """
        Generates a comprehensive report including all statistics and visualizations.

        Parameters:
        - output_dir (str): The directory to save the report files.
        """
        logging.info(f"Generating comprehensive report in {output_dir}.")
        os.makedirs(output_dir, exist_ok=True)

        try:
            # Generate summary statistics
            summary = self.compute_summary_statistics()
            summary_file = os.path.join(output_dir, 'summary_statistics.txt')
            with open(summary_file, 'w') as f:
                for field, value in summary.__dict__.items():
                    f.write(f"{field}: {value}\n")
            logging.info(f"Summary statistics saved to {summary_file}.")

            # Generate agent type statistics
            agent_stats = self.compute_agent_type_statistics()
            agent_stats_file = os.path.join(output_dir, 'agent_type_statistics.csv')
            agent_stats.to_csv(agent_stats_file)
            logging.info(f"Agent type statistics saved to {agent_stats_file}.")

            # Generate visualizations
            self.visualize_agent_energy_distribution(os.path.join(output_dir, 'agent_energy_distribution.png'))
            self.visualize_energy_trends(os.path.join(output_dir, 'energy_trends.png'))
            self.visualize_food_collection(os.path.join(output_dir, 'food_collection_trends.png'))
            logging.info("Visualizations generated and saved.")

            # Generate energy trends data
            energy_trends = self.analyze_energy_trends()
            energy_trends_file = os.path.join(output_dir, 'energy_trends.csv')
            energy_trends.to_csv(energy_trends_file)
            logging.info(f"Energy trends data saved to {energy_trends_file}.")

            # Generate food collection data
            food_trends, efficiency_stats = self.analyze_food_collection()
            food_trends_file = os.path.join(output_dir, 'food_collection_trends.csv')
            food_trends.to_csv(food_trends_file)
            efficiency_stats_file = os.path.join(output_dir, 'food_collection_efficiency_stats.csv')
            efficiency_stats.to_frame().to_csv(efficiency_stats_file)
            logging.info(f"Food collection data saved to {food_trends_file} and {efficiency_stats_file}.")

            logging.info(f"Comprehensive report generated in {output_dir}")
        except Exception as e:
            logging.error(f"Failed to generate comprehensive report: {e}")
            raise

# Example usage
# results = load_simulation_results(file_path)
# stats = EnhancedSimulationStatistics(results)
# stats.generate_comprehensive_report('simulation_report')
