"""Simulation environment for the 2_OPERATE pipeline.

A 2D grid world with pheromone fields, food sources, and nests. The renderer
contract requires ``width``, ``height`` and ``get_pheromone_levels()``; the
executor additionally reads ``max_steps`` and ``get_state()``.

This module intentionally keeps a small, self-contained surface: it is the
environment counterpart to the ``active_infer_ants`` package (which provides
the agent-side API), and it is what the pipeline's renderer actually plots.
"""

from __future__ import annotations

import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class Environment:
    """A 2D grid world for ant-colony active-inference simulations.

    Parameters
    ----------
    width, height:
        Grid dimensions.
    max_steps:
        Maximum number of time steps a simulation may run.
    num_food_sources:
        Number of food zones to place on the grid.
    num_nests:
        Number of nest positions to place on the grid.
    pheromone_decay:
        Per-step pheromone decay factor (0..1).
    seed:
        Random seed for reproducible food/nest placement.
    """

    def __init__(
        self,
        width: int = 100,
        height: int = 100,
        max_steps: int = 500,
        num_food_sources: int = 3,
        num_nests: int = 1,
        pheromone_decay: float = 0.01,
        seed: int | None = None,
    ) -> None:
        self.width = int(width)
        self.height = int(height)
        self.max_steps = int(max_steps)
        self.pheromone_decay = float(pheromone_decay)
        self.rng = np.random.default_rng(seed)

        self.pheromone: np.ndarray = np.zeros((self.height, self.width))
        self.food_sources: list[tuple[int, int]] = self._place_food(num_food_sources)
        self.nests: list[tuple[int, int]] = self._place_nests(num_nests)
        self.steps = 0
        self.agent_positions: list[tuple[int, int]] = []
        logger.debug(
            "Environment initialized: %dx%d, %d food sources, %d nests, %d steps max",
            self.width,
            self.height,
            len(self.food_sources),
            len(self.nests),
            self.max_steps,
        )

    def _place_food(self, count: int) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for _ in range(max(0, count)):
            x = int(self.rng.integers(0, self.width))
            y = int(self.rng.integers(0, self.height))
            positions.append((x, y))
        return positions

    def _place_nests(self, count: int) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []
        for _ in range(max(0, count)):
            x = int(self.rng.integers(0, self.width))
            y = int(self.rng.integers(0, self.height))
            positions.append((x, y))
        return positions

    def deposit_pheromone(self, x: int, y: int, amount: float) -> None:
        """Add pheromone at a grid cell (clamped to the grid)."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        self.pheromone[y, x] += float(amount)

    def get_pheromone_levels(self) -> np.ndarray:
        """Return the current pheromone field (used by the renderer)."""
        return self.pheromone

    def sense_pheromone(self, x: int, y: int) -> np.ndarray:
        """Return the local pheromone signal around a cell as a vector.

        The signal is the 5-cell cross centred on the agent's position
        (centre, north, south, east, west), which matches the 5-move action
        space used by :class:`MetaInformAntSimulation`.
        """
        cx = int(np.clip(x, 0, self.width - 1))
        cy = int(np.clip(y, 0, self.height - 1))
        cross = [
            (cy, cx),
            (max(0, cy - 1), cx),
            (min(self.height - 1, cy + 1), cx),
            (cy, min(self.width - 1, cx + 1)),
            (cy, max(0, cx - 1)),
        ]
        return np.asarray([self.pheromone[yy, xx] for yy, xx in cross], dtype=float)

    def nearest_food_distance(self, x: int, y: int) -> float:
        """Euclidean distance to the nearest food source."""
        if not self.food_sources:
            return float("inf")
        distances = [np.hypot(fx - x, fy - y) for fx, fy in self.food_sources]
        return float(min(distances))

    def step(self) -> None:
        """Advance time: decay pheromones and increment the step counter."""
        self.pheromone *= 1.0 - self.pheromone_decay
        self.steps += 1

    def get_state(self) -> dict[str, Any]:
        """Return a serializable snapshot of the environment."""
        return {
            "width": self.width,
            "height": self.height,
            "steps": self.steps,
            "max_steps": self.max_steps,
            "food_sources": self.food_sources,
            "nests": self.nests,
            "pheromone_total": float(self.pheromone.sum()),
            "agent_count": len(self.agent_positions),
        }


def build_environment_from_config(
    settings: dict[str, Any],
    environment_config: dict[str, Any],
    seed: int | None = None,
) -> Environment:
    """Build an :class:`Environment` from the 1_PREPARE/configs dictionaries.

    The full config dictionaries are large and ant-centred; this helper
    extracts only the fields the grid environment consumes, so the pipeline
    stays honest about what it actually uses.
    """
    grid = environment_config.get("GRID", {}) if environment_config else {}
    width = int(grid.get("WIDTH", settings.get("GRID_WIDTH", 100)))
    height = int(grid.get("HEIGHT", settings.get("GRID_HEIGHT", 100)))
    max_steps = int(settings.get("MAX_STEPS", 500))
    num_food = len(environment_config.get("RESOURCE_ZONES", [])) if environment_config else 3
    pheromone_cfg = environment_config.get("PHEROMONE_CONFIG", {}) if environment_config else {}
    decay = float(pheromone_cfg.get("DECAY_RATE", 0.01))
    return Environment(
        width=width,
        height=height,
        max_steps=max_steps,
        num_food_sources=max(1, num_food),
        num_nests=max(1, int(settings.get("NEST_COUNT", 1))),
        pheromone_decay=decay,
        seed=seed,
    )
