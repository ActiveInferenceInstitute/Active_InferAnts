"""Selected JSON ownership and independent, seeded run environments."""

import json

import numpy as np
import pytest
from plan_Simulation import SimulationPlanner


def write_config(path, width=7, height=8, agents=2, steps=3):
    selected = {
        "SIMULATION_SETTINGS": {
            "AGENT_COUNT": agents, "MAX_STEPS": steps, "NEST_COUNT": 2,
            "PARALLEL_EXECUTION": {"ENABLED": True, "WORKER_COUNT": 99},
        },
        "ENVIRONMENT_CONFIG": {
            "GRID": {"WIDTH": width, "HEIGHT": height},
            "RESOURCE_ZONES": [{"TYPE": "food"}, {"TYPE": "water"}],
            "PHEROMONE_CONFIG": {"DECAY_RATE": 0.2},
        },
        "ANT_AND_COLONY_CONFIG": {
            "NESTMATE": {"ACTIVE_INFERENCE": {"sensory_precision": 3.0, "prior_precision": 4.0, "learning_rate": 0.05}}
        },
        "META_CONFIG": {"ANT_AND_COLONY": {"NICHE_PARAMS": {"fixture": str(path.name)}}},
    }
    path.write_text(json.dumps(selected))
    return selected


def test_two_selected_configs_control_all_helper_reads(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for index, (width, height, agents, steps) in enumerate([(7, 8, 2, 3), (11, 12, 4, 5)]):
        path = tmp_path / f"selected-{index}.json"
        selected = write_config(path, width, height, agents, steps)
        planner = SimulationPlanner(str(path), seed=9)
        simulation = planner.create_simulation()
        assert (simulation.environment.width, simulation.environment.height) == (width, height)
        assert simulation.num_agents == agents
        assert simulation.environment.max_steps == steps
        assert len(simulation.environment.nests) == 2
        assert len(simulation.environment.food_sources) == 2
        assert simulation.environment.pheromone_decay == 0.2
        assert planner.get_parallel_execution_settings() == {"ENABLED": True, "WORKER_COUNT": agents}
        assert planner.estimate_computational_load()["estimated_agent_steps"] == agents * steps
        assert simulation.agent_params == selected["ANT_AND_COLONY_CONFIG"]["NESTMATE"]["ACTIVE_INFERENCE"]
        assert simulation.niche_params == {"fixture": path.name}


def test_new_simulation_has_fresh_environment_budget_and_seeded_initial_state(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "selected.json"
    write_config(path)
    planner = SimulationPlanner(str(path), seed=11)
    first = planner.create_simulation(max_steps=1)
    original_positions = list(first.positions)
    first.environment.step()
    first.environment.deposit_pheromone(0, 0, 7)
    first.positions[0] = (0, 0)
    second = planner.create_simulation()
    assert first.environment is not second.environment
    assert first.agents[0] is not second.agents[0]
    assert second.environment.steps == 0 and second.step_count == 0
    assert second.environment.max_steps == 3
    assert np.count_nonzero(second.environment.pheromone) == 0
    assert second.positions == original_positions
    assert second.environment.food_sources == first.environment.food_sources
    assert first.environment.steps == 1 and first.environment.pheromone[0, 0] == 7


@pytest.mark.parametrize("selected", [[], {}, {"SIMULATION_SETTINGS": {}, "ENVIRONMENT_CONFIG": []}, {"SIMULATION_SETTINGS": {}, "ENVIRONMENT_CONFIG": {}, "META_CONFIG": []}])
def test_invalid_selected_configuration_does_not_fall_back(tmp_path, monkeypatch, selected):
    monkeypatch.chdir(tmp_path)
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(selected))
    with pytest.raises(ValueError):
        SimulationPlanner(str(path))
    assert not (tmp_path / "simulation_output").exists()
