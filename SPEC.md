# SPEC.md — Active InferAnts

> Technical specification for the Active InferAnts framework repository root.

## Overview

Multi-language Active Inference framework for advanced AI research and applications. Implements Active Inference algorithms across 50 programming languages with a 6-phase operational pipeline.

## Structure

- 📁 `0_CONTEXT/` — Research context, specs, and multi-language implementations
- 📁 `1_PREPARE/` — Data preparation, configs, methods, agents, and utilities
- 📁 `2_OPERATE/` — Runtime execution and simulation management
- 📁 `3_MEASURE/` — Analysis, statistics, and measurement
- 📁 `4_REPORT/` — Report generation and communication
- 📁 `5_FOLLOWUP/` — Continuous improvement and follow-up
- 📁 `6_API/` — REST APIs and external interfaces
- 📁 `9_OTHER/` — Third-party integrations and experimental modules
- 📄 `config.json` — Global configuration parameters
- 📄 `governance.md` — Project governance documentation
- 📄 `LICENSE` — CC BY-NC-ND 4.0

## Interfaces

### Pipeline Flow

```
0_CONTEXT → 1_PREPARE → 2_OPERATE → 3_MEASURE → 4_REPORT → 5_FOLLOWUP → 6_API
```

Each phase receives structured output from the preceding phase and produces artifacts consumed by the subsequent phase.

### Entry Points

| Entry Point | Command | Description |
|---|---|---|
| Master Controller | `python3 0_CONTEXT/Computer_Languages/master_controller.py` | Cross-language orchestration |
| Knowledge API | `python3 6_API/Knowledge_API.py` | REST API on port 8000 |
| MetaInformAnt API | `python3 6_API/MetaInformAnt_API.py` | Meta-information API |

### Configuration

Global parameters in `config.json`:
- Simulation parameters (iterations, learning rate, precision)
- Output directories
- Visualization settings
- API configuration

## Dependencies

- **Python 3.8+** (core orchestration)
- **NumPy, SciPy** (mathematical operations)
- **FastAPI, uvicorn** (API services)
- **50 language runtimes** (optional, for multi-language implementations)
- See per-language subdirectories for language-specific dependencies

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
