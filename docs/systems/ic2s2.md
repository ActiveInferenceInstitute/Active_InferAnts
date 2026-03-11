# IC2S2 — Computational Social Science

## Location

`0_CONTEXT/Systems/IC2S2/`

## Architecture

| Module | Prefix | Description |
|--------|--------|-------------|
| `main.py` | — | Entry point with datetime tracking |
| `setup.py` | — | OS-level environment setup |
| `utils_active_inference.py` | utils_ | Active Inference computation utilities |
| `utils_agents.py` | utils_ | Logging-based agent management |
| `utils_analysis.py` | utils_ | Logging-based analysis tools |
| `utils_data.py` | utils_ | Random-seeded data generation |
| `utils_math.py` | utils_ | NumPy mathematical functions |
| `utils_visualizing.py` | utils_ | NumPy-based visualization utilities |

## Pattern

IC2S2 follows the `main + utils_*` pattern: one orchestrator with 7 utility modules organized by concern.
