# SPEC.md — Active Inference in Cpp

> Technical specification for `0_CONTEXT/Computer_Languages/Cpp` within the Active InferAnts framework.

## Overview

C++ — high-performance systems implementation

## Structure

- 📁 `include/`
- 📁 `src/`
- 📄 `AGENTS.md`
- 📄 `CMakeLists.txt`
- 📄 `README.md`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test cpp`

## Dependencies

- Cpp compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Cpp
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
