# SPEC.md — Active Inference in Java

> Technical specification for `0_CONTEXT/Computer_Languages/Java` within the Active InferAnts framework.

## Overview

Java — enterprise-grade JVM implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `AntColony.java`
- 📄 `README.md`
- 📄 `run.sh`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test java`

## Dependencies

- Java compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for Java
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
