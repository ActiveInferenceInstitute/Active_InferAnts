"""
Active InferAnts — core Active Inference package.

Provides the public API referenced by the project README:
``InferenceModel``, ``ActiveInferenceAgent``, ``Environment``,
``AntColony`` and ``PheromoneNetwork``. Implementations are intentionally small,
clear, and numPy-based so they run anywhere and are easy to reason about.
"""

from .agent import ActiveInferenceAgent
from .colony import AntColony, PheromoneNetwork
from .environment import Environment
from .model import InferenceModel

__all__ = [
    "InferenceModel",
    "ActiveInferenceAgent",
    "Environment",
    "AntColony",
    "PheromoneNetwork",
]

__version__ = "1.0.0"
