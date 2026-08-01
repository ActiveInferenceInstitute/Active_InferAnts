"""Ant colony + pheromone network for the Active InferAnts package."""

from __future__ import annotations

import numpy as np


class AntColony:
    """A collection of simple active-inference agents forming a colony.

    Each agent tracks a local belief mean and outputs an action; ``learn_from_colony``
    nudges agents toward the colony's average pheromone-weighted direction, giving a
    minimal collective optimisation behaviour.
    """

    def __init__(self, n_agents: int = 50, n_dims: int = 3,
                 seed: int | None = None) -> None:
        self.n_agents = n_agents
        self.n_dims = n_dims
        self.rng = np.random.default_rng(seed)
        self.agents = [self.rng.normal(size=n_dims) for _ in range(n_agents)]
        self.actions: list[np.ndarray] = []

    def parallel_inference(self) -> list[np.ndarray]:
        """Compute an action for every agent (vectorised)."""
        self.actions = [a + self.rng.normal(0.0, 0.1, size=self.n_dims) for a in self.agents]
        return self.actions

    def learn_from_colony(self, pheromone_map: dict[int, float]) -> None:
        """Move agents toward the pheromone-richest agent's position."""
        if not pheromone_map:
            return
        best_idx = max(pheromone_map, key=lambda k: pheromone_map[k])
        strength = pheromone_map.get(best_idx, 0.0)
        for i in range(self.n_agents):
            self.agents[i] = self.agents[i] + 0.05 * strength * (self.agents[best_idx] - self.agents[i])

    def analyze_emergent_behavior(self) -> dict[str, float]:
        """Return simple aggregate statistics over the colony."""
        arr = np.array(self.agents)
        return {
            "n_agents": float(self.n_agents),
            "mean_position": float(np.mean(arr)),
            "std_position": float(np.std(arr)),
        }


class PheromoneNetwork:
    """Tracks a pheromone strength per agent over time (with decay).

    ``update_trails`` adds pheromone proportionally to each agent's action
    magnitude; ``get_pheromone_map`` returns current per-agent strengths.
    """

    def __init__(self, agents: list[np.ndarray], decay: float = 0.9) -> None:
        self.n = len(agents)
        self.strengths = {i: 1.0 for i in range(self.n)}
        self.decay = float(decay)
        self.actions: list[np.ndarray] = []

    def update_trails(self, actions: list[np.ndarray]) -> None:
        self.actions = actions
        for i, act in enumerate(actions):
            deposit = float(np.linalg.norm(act)) * 0.1
            self.strengths[i] = self.decay * self.strengths.get(i, 1.0) + deposit

    def get_pheromone_map(self) -> dict[int, float]:
        return dict(self.strengths)
