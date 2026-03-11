# SPEC.md — Active Inference in Python

> Technical specification for `0_CONTEXT/Computer_Languages/Python` within the Active InferAnts framework.

## Overview

Python — primary scientific computing implementation

## Structure

- 📁 `output/`
- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `Student_Teacher.py`
- 📄 `config_manager.py`
- 📄 `run.sh`
- 📄 `serializer.py`
- 📄 `teacher_wrapper.py`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test python`

## Dependencies

- Python compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Python
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
