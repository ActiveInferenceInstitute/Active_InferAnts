# SPEC.md — Runtime Execution

> Technical specification for `2_OPERATE` within the Active InferAnts framework.

## Overview

Runtime execution, simulation management, and cognitive utilities. This phase orchestrates the execution of Active Inference simulations and agent behaviors.

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `cognitive_utilities.py`
- 📄 `execute_Simulation.py`
- 📄 `plan_Simulation.py`
- 📄 `render_Simulation.py`
- 📄 `situational_Antwareness.py`

## Interfaces

- **Input**: Receives output from the preceding pipeline phase
- **Output**: Produces structured data/artifacts for the subsequent phase
- **Configuration**: Managed via `config.json` at the repository root

## Dependencies

- Python 3.8+
- NumPy, SciPy (core mathematical operations)
- See `requirements.txt` at repository root for full dependency list

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
