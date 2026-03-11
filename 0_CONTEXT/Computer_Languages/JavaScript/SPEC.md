# SPEC.md — Active Inference in JavaScript

> Technical specification for `0_CONTEXT/Computer_Languages/JavaScript` within the Active InferAnts framework.

## Overview

JavaScript — browser and Node.js implementation

## Structure

- 📄 `AGENTS.md`
- 📄 `README.md`
- 📄 `SKILL.md`
- 📄 `active_inference.js`
- 📄 `ant_colony_demo.js`
- 📄 `config.js`
- 📄 `enhanced_demo.html`
- 📄 `logger.js`
- 📄 `package-lock.json`
- 📄 `package.json`
- 📄 `run.sh`
- 📄 `serializer.js`
- 📄 `visualizer.js`

## Interfaces

- **Input**: Active Inference parameters (state space, observation model, transition model)
- **Output**: Inference results (beliefs, policies, free energy values)
- **API**: Language-specific API consistent with the cross-language Active Inference interface
- **Testing**: Validated via `master_controller.py test javascript`

## Dependencies

- JavaScript compiler/interpreter (see language-specific README)
- Active Inference mathematical libraries for JavaScript
- Visualization libraries (where applicable)

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
