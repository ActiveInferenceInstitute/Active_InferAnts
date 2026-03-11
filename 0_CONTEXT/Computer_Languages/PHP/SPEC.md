# SPEC.md — Active Inference in PHP

> Technical specification for `0_CONTEXT/Computer_Languages/PHP` within the Active InferAnts framework.

## Overview

PHP — server-side scripting implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `ActiveInferenceAgent.php`
- 📄 `README.md`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test php`

## Dependencies

- PHP compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for PHP
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
