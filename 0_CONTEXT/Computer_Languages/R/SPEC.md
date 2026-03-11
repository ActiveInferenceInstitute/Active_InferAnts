# SPEC.md — Active Inference in R

> Technical specification for `0_CONTEXT/Computer_Languages/R` within the Active InferAnts framework.

## Overview

R — statistical computing implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `active_inference.R`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test r`

## Dependencies

- R compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for R
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
