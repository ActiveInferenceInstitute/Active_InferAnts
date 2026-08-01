"""Tests for the active_infer_ants package (public README API)."""

import numpy as np
from active_infer_ants import (
    ActiveInferenceAgent,
    AntColony,
    Environment,
    InferenceModel,
    PheromoneNetwork,
)


def test_inference_model_runs_and_bounds_reward():
    model = InferenceModel(seed=0)
    res = model.run(max_iterations=200)
    assert 0.0 <= res["mean_reward"] <= 1.0
    assert len(res["rewards"]) == 200
    assert len(res["belief_mean"]) == 3


def test_agent_learns_preferred_state():
    env = Environment(config={"complexity": 2, "uncertainty": 0.1}, seed=1)
    agent = ActiveInferenceAgent(n_dims=2, seed=1)
    for _ in range(100):
        obs = env.observe()
        action = agent.infer(obs)
        reward = env.step(action)
        agent.learn(reward)
    # Belief precision should grow past the initial tiny value.
    assert np.all(agent.pi > 1.0)


def test_agent_from_config():
    agent = ActiveInferenceAgent.from_config(
        {"complexity": 4, "sensory_precision": 9.0, "learning_rate": 0.05}
    )
    assert agent.n_dims == 4
    assert agent.sensory_precision == 9.0


def test_colony_and_pheromone_network():
    colony = AntColony(n_agents=20, seed=2)
    phero = PheromoneNetwork(colony.agents)
    for _ in range(10):
        actions = colony.parallel_inference()
        phero.update_trails(actions)
        colony.learn_from_colony(phero.get_pheromone_map())
    stats = colony.analyze_emergent_behavior()
    assert stats["n_agents"] == 20.0
    assert len(phero.get_pheromone_map()) == 20


def test_pheromone_map_never_empty_with_input():
    colony = AntColony(n_agents=5, seed=3)
    phero = PheromoneNetwork(colony.agents)
    phero.update_trails(colony.parallel_inference())
    assert phero.get_pheromone_map()
