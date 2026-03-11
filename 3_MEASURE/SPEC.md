# SPEC.md — Analysis & Measurement

> Technical specification for `3_MEASURE` within the Active InferAnts framework.

## Overview

Analysis, statistics, categorization, and performance measurement. This phase quantifies and evaluates the outputs of Active Inference operations.

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `categorization.py`
- 📄 `poly_functor.py`
- 📄 `specify_measure.py`
- 📄 `statistics.py`
- 📄 `summarize.py`

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
