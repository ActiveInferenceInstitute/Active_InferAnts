"""MetaInformAnt simulation engine for the 2_OPERATE pipeline.

``MetaInformAntSimulation`` is the concrete simulation object the planning
layer constructs and the executor drives. It combines the environment from
``environment.py`` with the agent-side API of the ``active_infer_ants``
package: each ant is an ``ActiveInferenceAgent`` whose action vector is
mapped to a movement direction on the grid, and pheromone deposition is the
action's observable consequence.

The class exposes the contract the executor and renderer expect:
``progress()``, ``should_terminate_early()``, ``aggregate_results()``,
``get_visualization_parameters()``, ``get_parameters()`` and
``update_parameters()``.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np
from active_infer_ants import ActiveInferenceAgent
from environment import Environment

logger = logging.getLogger(__name__)

_MOVEMENT = [
    (0, 0),  # stay
    (1, 0),  # east
    (-1, 0),  # west
    (0, 1),  # south
    (0, -1),  # north
]


class MetaInformAntSimulation:
    """A grid-world ant-colony active-inference simulation.

    Parameters
    ----------
    num_agents:
        Number of ants to instantiate.
    simulation_environment:
        The :class:`~environment.Environment` the agents act in.
    num_food_sources:
        Number of food zones (used for the reward signal).
    num_nests:
        Number of nests (informational; plotted by the renderer).
    agent_params:
        Optional agent-parameter overrides passed to ``ActiveInferenceAgent``.
    niche_params:
        Optional niche parameters (reserved; logged when provided).
    colony:
        Optional pre-built colony object; when provided its agents are used
        instead of creating fresh ones.
    data_logger, visualizer, performance_tracker:
        Optional pipeline components attached for observability.
    seed:
        Random seed for reproducible agent initialization.
    """

    def __init__(
        self,
        num_agents: int,
        simulation_environment: Environment,
        num_food_sources: int,
        num_nests: int,
        agent_params: dict[str, Any] | None = None,
        niche_params: dict[str, Any] | None = None,
        colony: Any = None,
        data_logger: Any = None,
        visualizer: Any = None,
        performance_tracker: Any = None,
        seed: int | None = None,
    ) -> None:
        self.environment = simulation_environment
        self.num_food_sources = int(num_food_sources)
        self.num_nests = int(num_nests)
        self.agent_params = dict(agent_params or {})
        self.niche_params = dict(niche_params or {})
        self.data_logger = data_logger
        self.visualizer = visualizer
        self.performance_tracker = performance_tracker
        self.seed = seed
        self.rng = np.random.default_rng(seed)

        if colony is not None and getattr(colony, "agents", None):
            self.agents: list[Any] = list(colony.agents)
            self.colony = colony
        else:
            self.colony = None
            self.agents = [
                ActiveInferenceAgent(
                    n_dims=len(_MOVEMENT),
                    seed=int(self.rng.integers(0, 2**31 - 1)),
                    **self.agent_params,
                )
                for _ in range(int(num_agents))
            ]

        # Grid positions: one per agent, initialized near a nest (or centre).
        centre = (self.environment.width // 2, self.environment.height // 2)
        self.positions: list[tuple[int, int]] = [
            (
                int(np.clip(centre[0] + self.rng.integers(-5, 6), 0, self.environment.width - 1)),
                int(np.clip(centre[1] + self.rng.integers(-5, 6), 0, self.environment.height - 1)),
            )
            for _ in self.agents
        ]
        self.environment.agent_positions = self.positions

        self.step_count = 0
        self.rewards: list[float] = []
        self.belief_history: list[Any] = []
        self.early_terminated = False
        logger.info(
            "MetaInformAntSimulation created: %d agents, %d food sources, %d nests",
            len(self.agents),
            self.num_food_sources,
            self.num_nests,
        )

    @property
    def num_agents(self) -> int:
        """Number of agents in the simulation."""
        return len(self.agents)

    # ------------------------------------------------------------------ #
    # Core loop
    # ------------------------------------------------------------------ #
    def progress(self) -> None:
        """Advance the simulation by a single time step."""
        for i, agent in enumerate(self.agents):
            x, y = self.positions[i]
            observation = self.environment.sense_pheromone(x, y)
            action = agent.infer(observation)
            reward = self._act(agent, action, x, y, i)
            agent.learn(reward)
            self.rewards.append(reward)
        self.environment.step()
        self.step_count += 1

    def _act(self, agent: ActiveInferenceAgent, action: np.ndarray, x: int, y: int, index: int) -> float:
        """Move an agent according to its action vector and deposit pheromone."""
        move_index = int(np.argmax(np.asarray(action)))
        move_index = min(max(move_index, 0), len(_MOVEMENT) - 1)
        dx, dy = _MOVEMENT[move_index]
        nx = int(np.clip(x + dx, 0, self.environment.width - 1))
        ny = int(np.clip(y + dy, 0, self.environment.height - 1))
        self.positions[index] = (nx, ny)
        self.environment.deposit_pheromone(nx, ny, amount=0.5)
        distance = self.environment.nearest_food_distance(nx, ny)
        return float(np.exp(-distance / max(1.0, self.environment.width)))

    def run(self, max_steps: int | None = None) -> dict[str, Any]:
        """Run the simulation for ``max_steps`` steps and return results."""
        max_steps = int(max_steps or self.environment.max_steps)
        for _ in range(max_steps):
            if self.should_terminate_early():
                break
            self.progress()
        return self.aggregate_results()

    def should_terminate_early(self) -> bool:
        """Return True when the step budget is exhausted."""
        if self.step_count >= self.environment.max_steps:
            self.early_terminated = True
            return True
        return False

    # ------------------------------------------------------------------ #
    # Results / observability
    # ------------------------------------------------------------------ #
    def aggregate_results(self) -> dict[str, Any]:
        """Return a serializable results dictionary."""
        rewards = np.asarray(self.rewards, dtype=float) if self.rewards else np.zeros(1)
        return {
            "step_count": self.step_count,
            "num_agents": len(self.agents),
            "mean_reward": float(np.mean(rewards)),
            "final_reward": float(rewards[-1]) if len(rewards) else 0.0,
            "total_pheromone": float(self.environment.pheromone.sum()),
            "environment": self.environment.get_state(),
            "early_terminated": bool(self.early_terminated),
        }

    def get_parameters(self) -> dict[str, Any]:
        """Return the parameters currently in effect."""
        return {
            "num_agents": len(self.agents),
            "num_food_sources": self.num_food_sources,
            "num_nests": self.num_nests,
            "max_steps": self.environment.max_steps,
            "agent_params": self.agent_params,
            "niche_params": self.niche_params,
            "seed": self.seed,
        }

    def update_parameters(self, new_params: dict[str, Any]) -> None:
        """Apply a parameter update (e.g. from the performance monitor)."""
        if not new_params:
            return
        if "max_steps" in new_params:
            self.environment.max_steps = int(new_params["max_steps"])
        for key in ("agent_params", "niche_params"):
            if key in new_params and isinstance(new_params[key], dict):
                getattr(self, key).update(new_params[key])
        logger.info("Simulation parameters updated: %s", new_params)

    def get_visualization_parameters(self) -> tuple[Environment, list[Any], list[Any]]:
        """Return ``(environment, nests, agents)`` for the renderer.

        The renderer expects ``Entity``-like objects with ``x`` and ``y``;
        small adapters are returned so the pipeline does not depend on the
        renderer's private dataclass.
        """
        return self.environment, self._entity_list(self.environment.nests), self._entity_list(self.positions)

    @staticmethod
    def _entity_list(points: list[tuple[int, int]]) -> list[Any]:
        class _Point:
            def __init__(self, x: int, y: int) -> None:
                self.x = x
                self.y = y

        return [_Point(int(x), int(y)) for x, y in points]
