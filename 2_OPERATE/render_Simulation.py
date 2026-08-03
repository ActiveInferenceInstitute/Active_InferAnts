import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
import logging  # Added for logging purposes

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class Entity:
    x: float
    y: float

class SimulationRenderer:
    def __init__(self, simulation_environment: Any, nests: List[Entity], agents: List[Entity]):
        self.simulation_environment = simulation_environment
        self.nests = nests
        self.agents = agents
        self.fig, self.ax = plt.subplots(figsize=(14, 12))
        self.colormap = self._create_custom_colormap()
        self._configure_plot_environment()
        self.animation: Optional[animation.FuncAnimation] = None
        logging.info("SimulationRenderer initialized successfully.")
    
    def _create_custom_colormap(self) -> LinearSegmentedColormap:
        """Create a custom colormap for the simulation.

        Returns
        -------
        LinearSegmentedColormap
            The custom colormap created from the defined color list.
        """
        colors = ['#FFFFFF', '#E6F3FF', '#ADD8E6', '#4169E1', '#000080', '#191970']  # Enhanced gradient: White to midnight blue
        logging.debug("Creating custom colormap.")
        return LinearSegmentedColormap.from_list("custom_blue", colors, N=256)
    
    def _configure_plot_environment(self) -> None:
        """Set up the plot environment for the simulation."""
        try:
            self.ax.set_xlim(0, self.simulation_environment.width)
            self.ax.set_ylim(0, self.simulation_environment.height)
            self.ax.set_title('Advanced Ant Colony Optimization Simulation', fontsize=20, fontweight='bold')
            self.ax.set_xlabel('X Coordinate', fontsize=16)
            self.ax.set_ylabel('Y Coordinate', fontsize=16)
            self.ax.grid(True, linestyle='--', alpha=0.7)
            self.ax.set_facecolor('#F0F0F0')  # Light gray background
            self.fig.set_facecolor('#E8E8E8')  # Slightly darker gray for figure background
            logging.info("Plot environment configured.")
        except AttributeError as e:
            logging.error(f"Error configuring plot environment: {e}")
            raise
    
    def _plot_entities(self, entities: List[Entity], color: str, label: str, marker: str = 'o', size: int = 50) -> None:
        """Plot entities on the simulation environment.

        Parameters
        ----------
        entities : List[Entity]
            The list of entities to plot.
        color : str
            Color of the entities.
        label : str
            Label for the entities.
        marker : str, optional
            Marker style, by default 'o'.
        size : int, optional
            Size of the markers, by default 50.
        """
        positions = [(entity.x, entity.y) for entity in entities]
        if positions:
            x, y = zip(*positions)
            self.ax.scatter(x, y, c=color, label=label, alpha=0.8, edgecolors='w', marker=marker, s=size, zorder=3)
            logging.debug(f"Plotted {label} with color {color}.")
    
    def _plot_pheromone_trails(self) -> None:
        """Plot pheromone trails as a heatmap with enhanced visualization."""
        pheromone_levels = self.simulation_environment.get_pheromone_levels()
        heatmap = self.ax.imshow(pheromone_levels, cmap=self.colormap, alpha=0.6, 
                                 extent=[0, self.simulation_environment.width, 0, self.simulation_environment.height],
                                 interpolation='gaussian', zorder=1)
        colorbar = self.fig.colorbar(heatmap, ax=self.ax, label='Pheromone Intensity', pad=0.02)
        colorbar.ax.tick_params(labelsize=12)
        colorbar.set_label('Pheromone Intensity', fontsize=14, fontweight='bold')
    
    def _refresh_environment(self, frame: Optional[int] = None) -> List[plt.Artist]:
        """Refresh the environment for the next frame or step."""
        self.ax.clear()
        self._configure_plot_environment()
        self._plot_pheromone_trails()
        
        if frame is not None:
            self.ax.set_title(f'Advanced Ant Colony Optimization - Step: {frame}', fontsize=20, fontweight='bold')
        
        self._plot_entities(self.nests, 'red', 'Nests', marker='s', size=100)
        self._plot_entities(self.agents, 'black', 'Ants', marker='^', size=80)
        
        legend = self.ax.legend(loc='upper right', fontsize=14, framealpha=0.9, edgecolor='black')
        legend.get_frame().set_facecolor('#F0F0F0')
        
        return self.ax.get_children()
    
    def initialize_environment(self) -> None:
        """(Re)initialize the plot environment.

        Called by the executor before the simulation loop; clears any stale
        artists so a fresh run starts from a clean figure.
        """
        logging.debug("SimulationRenderer.initialize_environment called.")
        self._refresh_environment()

    def refresh_visualization(self, step: Optional[int] = None) -> List[plt.Artist]:
        """Refresh the current visualization for the given step.

        Public wrapper around :meth:`_refresh_environment` used by the
        executor's per-step loop.
        """
        return self._refresh_environment(step)

    def visualize_post_simulation(self, simulation_results: Dict[str, Any]) -> None:
        """Render the post-simulation analysis view.

        Public wrapper around :meth:`render_post_simulation` used by the
        executor's conclusion phase.
        """
        self.render_post_simulation(simulation_results)

    def animate_simulation(self, steps: int) -> animation.FuncAnimation:
        """Animate the simulation over a given number of steps."""
        self.animation = animation.FuncAnimation(self.fig, self._refresh_environment, frames=steps, interval=200, blit=True)
        plt.tight_layout()
        return self.animation
    
    def render_post_simulation(self, simulation_results: Dict[str, Any]) -> None:
        """Visualize the results after the simulation has concluded."""
        self._refresh_environment()
        self.ax.set_title('Post-Simulation Analysis', fontsize=20, fontweight='bold')
        
        if 'best_path' in simulation_results:
            path = simulation_results['best_path']
            x, y = zip(*path)
            self.ax.plot(x, y, 'g-', linewidth=3, label='Best Path', alpha=0.8, zorder=2)
        
        if 'convergence' in simulation_results:
            convergence_data = simulation_results['convergence']
            ax2 = self.ax.twinx()
            ax2.plot(convergence_data, 'r--', label='Convergence', linewidth=2)
            ax2.set_ylabel('Convergence Metric', color='r', fontsize=16, fontweight='bold')
            ax2.tick_params(axis='y', labelcolor='r', labelsize=12)
            ax2.spines['right'].set_color('r')
        
        if 'performance_metrics' in simulation_results:
            metrics = simulation_results['performance_metrics']
            self._add_performance_textbox(metrics)
        
        handles, labels = self.ax.get_legend_handles_labels()
        handles2, labels2 = ax2.get_legend_handles_labels() if 'convergence' in simulation_results else ([], [])
        self.ax.legend(handles + handles2, labels + labels2, loc='upper left', fontsize=14, framealpha=0.9, edgecolor='black')
        
        plt.tight_layout()
        plt.show()
    
    def _add_performance_textbox(self, metrics: Dict[str, float]) -> None:
        """Add a textbox with performance metrics to the plot."""
        text_box = "\n".join([f"{k.replace('_', ' ').title()}: {v:.2f}" for k, v in metrics.items()])
        self.ax.text(0.02, 0.98, text_box, transform=self.ax.transAxes, fontsize=12,
                     verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def save_animation(self, filename: str, fps: int = 30, dpi: int = 300) -> None:
        """Save the animation to a file.

        Parameters
        ----------
        filename : str
            The name of the file to save the animation.
        fps : int, optional
            Frames per second, by default 30.
        dpi : int, optional
            Dots per inch, by default 300.
        """
        try:
            if self.animation:
                self.animation.save(filename, fps=fps, dpi=dpi, writer='ffmpeg')
                logging.info(f"Animation saved as {filename}.")
            else:
                logging.warning("No animation to save. Run animate_simulation first.")
        except Exception as e:
            logging.error(f"Failed to save animation: {e}")
            raise
    
    def plot_performance_over_time(self, performance_data: Dict[str, List[float]]) -> None:
        """Plot various performance metrics over time."""
        fig, ax = plt.subplots(figsize=(14, 8))
        for metric, values in performance_data.items():
            ax.plot(values, label=metric.replace('_', ' ').title(), linewidth=2)
        
        ax.set_xlabel('Simulation Step', fontsize=16)
        ax.set_ylabel('Metric Value', fontsize=16)
        ax.set_title('Performance Metrics Over Time', fontsize=20, fontweight='bold')
        ax.legend(loc='best', fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.tick_params(axis='both', which='major', labelsize=12)
        
        plt.tight_layout()
        plt.show()
    
    def plot_heatmap(self, data: np.ndarray, title: str) -> None:
        """Plot a heatmap of the given data."""
        fig, ax = plt.subplots(figsize=(12, 10))
        heatmap = ax.imshow(data, cmap='viridis', interpolation='nearest')
        ax.set_title(title, fontsize=20, fontweight='bold')
        colorbar = fig.colorbar(heatmap, ax=ax)
        colorbar.set_label('Intensity', fontsize=16)
        ax.set_xlabel('X Coordinate', fontsize=16)
        ax.set_ylabel('Y Coordinate', fontsize=16)
        plt.tight_layout()
        plt.show()
    
    def plot_path_comparison(self, paths: List[List[Tuple[float, float]]], labels: List[str]) -> None:
        """Plot a comparison of multiple paths."""
        fig, ax = plt.subplots(figsize=(12, 10))
        for path, label in zip(paths, labels):
            x, y = zip(*path)
            ax.plot(x, y, '-', linewidth=2, label=label)
        
        ax.set_title('Path Comparison', fontsize=20, fontweight='bold')
        ax.set_xlabel('X Coordinate', fontsize=16)
        ax.set_ylabel('Y Coordinate', fontsize=16)
        ax.legend(fontsize=14)
        ax.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
