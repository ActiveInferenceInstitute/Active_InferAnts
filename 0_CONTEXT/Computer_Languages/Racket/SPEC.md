# SPEC.md — Active Inference in Racket

> Technical specification for `0_CONTEXT/Computer_Languages/Racket` within the Active InferAnts framework.

## Overview

Racket — Lisp-family language implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `active_inference.rkt`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test racket`

## Dependencies

- Racket compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Racket
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
