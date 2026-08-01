"""High-level InferenceModel wrapper for the Active InferAnts package."""

from __future__ import annotations

from typing import Any

import numpy as np

from .agent import ActiveInferenceAgent
from .environment import Environment


class InferenceModel:
    """Convenience wrapper that runs an agent in an environment.

    ``run`` returns a results dictionary with per-iteration rewards and belief
    means; ``visualize`` prints a compact summary (kept matplotlib-free so the
    core package has no hard plotting dependency).
    """

    def __init__(self, config: dict[str, Any] | None = None,
                 seed: int | None = None) -> None:
        self.config = dict(config or {})
        self.seed = seed
        n_dims = int(self.config.get("complexity", 3))
        self.agent = ActiveInferenceAgent(
            sensory_precision=self.config.get("sensory_precision", 5.0),
            prior_precision=self.config.get("prior_precision", 2.0),
            learning_rate=self.config.get("learning_rate", 0.1),
            n_dims=n_dims,
            seed=seed,
        )
        self.env = Environment(config=self.config, seed=seed)
        self.results: dict[str, Any] = {}

    def run(self, max_iterations: int = 1000) -> dict[str, Any]:
        rewards: list[float] = []
        actions: list[np.ndarray] = []
        for _ in range(int(max_iterations)):
            observation = self.env.observe()
            action = self.agent.infer(observation)
            reward = self.env.step(action)
            self.agent.learn(reward)
            rewards.append(reward)
            actions.append(action)
        self.results = {
            "max_iterations": int(max_iterations),
            "mean_reward": float(np.mean(rewards)),
            "final_reward": float(rewards[-1]) if rewards else 0.0,
            "belief_mean": self.agent.mu.tolist(),
            "belief_precision": self.agent.pi.tolist(),
            "preferred": self.agent.preferred.tolist(),
            "rewards": rewards,
        }
        return self.results

    def visualize(self, results: dict[str, Any] | None = None) -> None:
        results = results or self.results
        if not results:
            print("No results yet — call run() first.")
            return
        print("=== Active Inference Results ===")
        print(f"  mean reward   : {results.get('mean_reward', 0.0):.4f}")
        print(f"  final reward  : {results.get('final_reward', 0.0):.4f}")
        print(f"  belief mean   : {np.round(results.get('belief_mean', []), 4)}")
        print(f"  preferred     : {np.round(results.get('preferred', []), 4)}")


def main() -> None:
    """CLI entry point: run a short inference and print the summary."""
    import argparse

    parser = argparse.ArgumentParser(description="Active InferAnts demo")
    parser.add_argument("--iterations", type=int, default=100)
    parser.add_argument("--seed", type=int, default=None)
    args = parser.parse_args()
    model = InferenceModel(seed=args.seed)
    results = model.run(max_iterations=args.iterations)
    model.visualize(results)


if __name__ == "__main__":
    main()
