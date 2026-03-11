# SPEC.md — Active Inference in Clojure

> Technical specification for `0_CONTEXT/Computer_Languages/Clojure` within the Active InferAnts framework.

## Overview

Clojure — functional Lisp dialect on the JVM

## Structure

- 📁 `src/`
- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `project.clj`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test clojure`

## Dependencies

- Clojure compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Clojure
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
