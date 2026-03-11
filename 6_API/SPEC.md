# SPEC.md — External Interfaces & APIs

> Technical specification for `6_API` within the Active InferAnts framework.

## Overview

REST APIs, knowledge management services, and external interfaces. This phase exposes Active Inference capabilities to external consumers.

## Structure

- 📄 `AGENTS.md`
- 📄 `Knowledge_API.py`
- 📄 `MetaInformAnt_API.py`
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
