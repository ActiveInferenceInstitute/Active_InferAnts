"""Environment for the Active InferAnts package."""

from __future__ import annotations

from typing import Any

import numpy as np


class Environment:
    """A simple stochastic observation environment.

    The ``config`` dict controls the number of observation dimensions
    (``complexity``) and the observation noise (``uncertainty``). Observations are
    drawn from a Gaussian centred on a slowly drifting latent state, which gives
    the agent a non-trivial but tractable signal to track.
    """

    def __init__(self, config: dict[str, Any] | None = None,
                 seed: int | None = None) -> None:
        self.config = dict(config or {})
        self.complexity: int = int(self.config.get("complexity", 3))
        self.uncertainty: float = float(self.config.get("uncertainty", 0.2))
        self.rng = np.random.default_rng(seed)
        self.state = np.zeros(self.complexity)
        # A random stable target to drift toward.
        self.target = self.rng.normal(0.0, 1.0, size=self.complexity)
        self.steps = 0

    def observe(self) -> np.ndarray:
        """Return a noisy observation of the current latent state."""
        # Drift the latent state slightly toward the target each step.
        self.state = 0.98 * self.state + 0.02 * self.target
        noise = self.uncertainty * self.rng.normal(size=self.complexity)
        return self.state + noise

    def step(self, action: np.ndarray) -> float:
        """Apply an action and return a reward.

        Reward is the negative squared distance between the action and the latent
        state, so acting close to the current state yields higher reward.
        """
        self.steps += 1
        error = float(np.sum((action - self.state) ** 2))
        return float(np.exp(-error))
