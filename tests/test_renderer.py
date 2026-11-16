"""Agg surface contracts for live positions, bounded artists, and ownership."""

import matplotlib.pyplot as plt
import numpy as np
from environment import Environment
from render_Simulation import Entity, SimulationRenderer


def test_refresh_uses_live_positions_without_growing_axes_or_artists():
    environment = Environment(6, 6, num_food_sources=0, num_nests=0, seed=0)
    environment.agent_positions = [(1, 1)]
    renderer = SimulationRenderer(environment, [Entity(0, 0)], [Entity(5, 5)])
    try:
        for step in range(15):
            environment.agent_positions[0] = (step % 6, (step + 1) % 6)
            environment.pheromone[0, 0] = step
            renderer.refresh_visualization(step)
            agents = [artist for artist in renderer.ax.collections if artist.get_label() == "Ants"]
            np.testing.assert_array_equal(agents[0].get_offsets(), [environment.agent_positions[0]])
            assert len(renderer.fig.axes) == 2
            assert len(renderer.ax.images) == 1
            assert len(renderer.ax.collections) == 2
        renderer.fig.canvas.draw()
    finally:
        renderer.close()


def test_repeated_post_views_release_owned_twin_axes_and_close_only_owned_figure():
    environment = Environment(6, 6, num_food_sources=0, num_nests=0, seed=0)
    environment.agent_positions = [(1, 1)]
    renderer = SimulationRenderer(environment, [Entity(0, 0)], [Entity(5, 5)])
    other = plt.figure()
    figure_number = renderer.fig.number
    try:
        for _ in range(3):
            renderer.render_post_simulation({"convergence": [0.1, 0.2], "best_path": [(0, 0), (1, 1)], "performance_metrics": {"reward": 1.0}})
            assert len(renderer.fig.axes) == 3
            assert len(renderer.ax.lines) == 1
            assert len(renderer.ax.texts) == 1
            renderer.refresh_visualization()
            assert len(renderer.fig.axes) == 2
            assert len(renderer.ax.lines) == 0 and len(renderer.ax.texts) == 0
        renderer.close()
        assert not plt.fignum_exists(figure_number)
        assert plt.fignum_exists(other.number)
    finally:
        renderer.close()
        plt.close(other)


def test_failed_post_plot_remains_owned_and_is_removed_on_refresh():
    environment = Environment(6, 6, num_food_sources=0, num_nests=0, seed=0)
    renderer = SimulationRenderer(environment, [], [])
    try:
        try:
            renderer.render_post_simulation({"convergence": [object()]})
        except (TypeError, ValueError):
            pass
        else:
            raise AssertionError("Invalid convergence input must fail")
        renderer.refresh_visualization()
        assert len(renderer.fig.axes) == 2
    finally:
        renderer.close()
