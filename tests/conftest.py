"""Shared pytest fixtures/configuration for Active InferAnts tests.

Adds the phase directories to ``sys.path`` so the flat, non-package modules
(e.g. ``3_MEASURE/*.py``, ``6_API/*.py``) can be imported, and forces the
non-interactive matplotlib backend for plotting modules.
"""

import os

# Pre-import the STANDARD LIBRARY `statistics` module BEFORE putting the phase
# dirs on sys.path. 3_MEASURE/statistics.py shadows the stdlib name, and if it
# is found first seaborn's `from statistics import NormalDist` breaks. Caching
# the stdlib module here keeps bare imports resolving to the stdlib across the
# session.
import statistics as _stdlib_statistics  # noqa: F401
import sys

import matplotlib

matplotlib.use("Agg")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_PATHS = [
    ROOT,
    os.path.join(ROOT, "3_MEASURE"),
    os.path.join(ROOT, "6_API"),
    os.path.join(ROOT, "0_CONTEXT", "Computer_Languages"),
    os.path.join(ROOT, "0_CONTEXT", "Computer_Languages", "Python"),
    os.path.join(ROOT, "1_PREPARE", "General"),
]

for _p in _PATHS:
    if _p not in sys.path:
        sys.path.insert(0, _p)
