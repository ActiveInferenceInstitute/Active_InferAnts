# SPEC.md — Runtime Execution

> Technical specification for `2_OPERATE` within the Active InferAnts framework.

## Overview

Runtime execution, simulation management, and cognitive utilities. This phase orchestrates the execution of Active Inference simulations and agent behaviors.

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `cognitive_utilities.py`
- 📄 `computational_resources.py`
- 📄 `data_logging.py`
- 📄 `environment.py`
- 📄 `error_handling.py`
- 📄 `exception_handling.py`
- 📄 `execute_Simulation.py`
- 📄 `MetaInformAnt_Simulation.py`
- 📄 `performance_metrics.py`
- 📄 `performance_monitor.py`
- 📄 `plan_Simulation.py`
- 📄 `render_Simulation.py`
- 📄 `report_generator.py`
- 📄 `situational_Antwareness.py`
- 📄 `visualization.py`

## Interfaces

- **Input**: Receives output from the preceding pipeline phase
- **Output**: Produces structured data/artifacts for the subsequent phase
- **Configuration**: Managed via `config.json` at the repository root and the `1_PREPARE/configs` dictionaries
- **Agent API**: Wired to the `active_infer_ants` package (agents, colony, environment)

## Dependencies

- Python 3.9+
- NumPy, SciPy (core mathematical operations), matplotlib (rendering)
- `active_infer_ants` package (agent-side API)
- See `requirements.txt` at repository root for full dependency list

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
