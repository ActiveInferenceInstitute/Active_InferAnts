# SPEC.md — Reporting & Communication

> Technical specification for `4_REPORT` within the Active InferAnts framework.

## Overview

Report generation, specification, and communication of results. This phase transforms measured outcomes into structured reports.

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `execute_report.py`
- 📄 `specify_report.py`

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
