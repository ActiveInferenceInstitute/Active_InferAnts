# SPEC.md — Active Inference in Julia

> Technical specification for `0_CONTEXT/Computer_Languages/Julia` within the Active InferAnts framework.

## Overview

Julia — high-performance scientific computing implementation

## Structure

- 📁 `Category_Theory_Julia/`
- 📁 `SideCar/`
- 📁 `Visualization/`
- 📄 `AGENTS.md`
- 📄 `Clone_Julia_Repo.jl`
- 📄 `Julia_InferAnts.jl`
- 📄 `README.md`
- 📄 `RxInfer.jl`
- 📄 `RxInfer_Agent_Model.jl`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test julia`

## Dependencies

- Julia compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Julia
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
