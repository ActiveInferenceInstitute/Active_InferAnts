"""Active inference agent for the Active InferAnts package."""

from __future__ import annotations

from typing import Any

import numpy as np


class ActiveInferenceAgent:
    """A minimal active-inference agent.

    Maintains a (Gaussian) belief over the latent state, fuses observations
    weighted by ``sensory_precision``, and selects actions that minimise expected
    free energy — here approximated as the precision-weighted mismatch between the
    current belief and a desired (prior) state.

    Parameters
    ----------
    sensory_precision:
        Precision (inverse variance) of incoming observations.
    prior_precision:
        Precision of the agent's preferred/prior state.
    learning_rate:
        Rate at which the agent updates its preferred state toward experience.
    """

    def __init__(self, sensory_precision: float = 5.0,
                 prior_precision: float = 2.0,
                 learning_rate: float = 0.1,
                 n_dims: int = 3,
                 seed: int | None = None) -> None:
        self.sensory_precision = float(sensory_precision)
        self.prior_precision = float(prior_precision)
        self.learning_rate = float(learning_rate)
        self.n_dims = n_dims
        self.rng = np.random.default_rng(seed)
        # Belief: mean (mu) and precision (pi).
        self.mu = np.zeros(n_dims)
        self.pi = np.ones(n_dims) * 1e-3
        # Preferred state (learned toward rewarded states).
        self.preferred = np.zeros(n_dims)
        self.history: list[float] = []

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> ActiveInferenceAgent:
        """Build an agent from the JSON-style config used elsewhere in the repo."""
        return cls(
            sensory_precision=config.get("sensory_precision", 5.0),
            prior_precision=config.get("prior_precision", 2.0),
            learning_rate=config.get("learning_rate", 0.1),
            n_dims=config.get("complexity", 3),
        )

    def infer(self, observation: np.ndarray) -> np.ndarray:
        """Update beliefs from an observation and return the chosen action.

        The observation is a vector; precision-weighted fusion of the prior and
        the observation yields the posterior mean.
        """
        obs = np.asarray(observation, dtype=float)
        # Precision-weighted belief update (Gaussian prior <-> likelihood).
        self.pi = self.prior_precision + self.sensory_precision * np.ones_like(obs)
        self.mu = (
            (self.prior_precision * self.preferred + self.sensory_precision * obs)
            / self.pi
        )
        # Action that minimises expected free energy: move toward the preferred
        # state (the belief already encodes the mismatch).
        action = self.preferred + (self.mu - self.preferred)
        return action

    def learn(self, reward: float) -> None:
        """Update the preferred state toward recently rewarded actions."""
        self.preferred = self.preferred + self.learning_rate * (self.mu - self.preferred)
        self.history.append(float(reward))

    def visualize_beliefs(self) -> None:
        """Print a plain-text summary of the current belief (no matplotlib needed)."""
        print("Belief mean:", np.round(self.mu, 4))
        print("Belief precision:", np.round(self.pi, 4))
        print("Preferred state:", np.round(self.preferred, 4))
