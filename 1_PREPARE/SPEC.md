# SPEC.md — Preparation & Configuration

> Technical specification for `1_PREPARE` within the Active InferAnts framework.

## Overview

Data preparation, configuration management, research methods, agent implementations, and utility modules. This phase transforms raw research into actionable components.

## Structure

- 📁 `General/`
- 📁 `Methods/`
- 📁 `Things/`
- 📁 `Utils/`
- 📁 `configs/`
- 📄 `AGENTS.md`
- 📄 `README.md`

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
