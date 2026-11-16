"""One observable stay/east/west/south/north grid contract."""

import numpy as np
import pytest
from environment import Environment
from MetaInformAnt_Simulation import MetaInformAntSimulation

MOVES = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]


@pytest.mark.parametrize("position", [(2, 2), (0, 0), (4, 0), (0, 4), (4, 4), (0, 2), (4, 2), (2, 0), (2, 4)])
def test_observation_order_and_boundary_clipping(position):
    environment = Environment(5, 5, num_food_sources=0, num_nests=0, seed=0)
    environment.pheromone[:] = np.arange(25).reshape(5, 5)
    x, y = position
    expected = [environment.pheromone[min(max(y + dy, 0), 4), min(max(x + dx, 0), 4)] for dx, dy in MOVES]
    np.testing.assert_array_equal(environment.sense_pheromone(x, y), expected)


@pytest.mark.parametrize("position", [(2, 2), (0, 0), (4, 0), (0, 4), (4, 4)])
@pytest.mark.parametrize("action,delta", list(enumerate(MOVES)))
def test_stay_cardinals_and_deposition_share_coordinates(position, action, delta):
    environment = Environment(5, 5, num_food_sources=0, num_nests=0, seed=0)
    simulation = MetaInformAntSimulation(1, environment, 0, 0, seed=0)
    simulation.positions[0] = position
    x, y = position
    dx, dy = delta
    destination = (min(max(x + dx, 0), 4), min(max(y + dy, 0), 4))
    simulation._act(simulation.agents[0], np.eye(5)[action], x, y, 0)
    assert simulation.positions[0] == destination
    assert environment.agent_positions[0] == destination
    assert environment.pheromone[destination[1], destination[0]] == 0.5
    assert environment.pheromone.sum() == 0.5


@pytest.mark.parametrize("action,delta", list(enumerate(MOVES)))
def test_strongest_sensed_direction_selects_matching_destination(action, delta):
    environment = Environment(5, 5, num_food_sources=0, num_nests=0, seed=0)
    simulation = MetaInformAntSimulation(1, environment, 0, 0, seed=0)
    simulation.positions[0] = (2, 2)
    destination = (2 + delta[0], 2 + delta[1])
    environment.pheromone[destination[1], destination[0]] = 4.0
    signal = environment.sense_pheromone(2, 2)
    assert int(np.argmax(signal)) == action
    simulation._act(simulation.agents[0], signal, 2, 2, 0)
    assert simulation.positions[0] == destination
    assert environment.pheromone[destination[1], destination[0]] == 4.5
