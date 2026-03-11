# AGENTS.md — General Preparation

> Agent guidance for the `1_PREPARE/General` directory.

## Purpose

Core Active Inference algorithms and general-purpose preparation components. Foundation modules for cognitive security, digital twins, pheromone signaling, and cross-domain abstractions.

## Directory Contents

- 📄 `CogSec.py` — Cognitive security module using `ActiveNestmate`/`ActiveColony` from InferAnts with config/metaconfig integration
- 📄 `Cryptography.py` — Cryptographic primitives: hashing (`hashlib`), HMAC authentication, and base64 encoding
- 📄 `DigitalTwin.py` — Async digital twin implementation with typed state management and event-driven updates
- 📄 `DigitalTwin_DesignProcess.py` — `DigitalTwinDesignProcess` class: design methodology for model-reality gap analysis
- 📄 `Metaphysics.py` — Combinatorial metaphysical reasoning with typed predicate logic and JSON serialization
- 📄 `Nesting.py` — Nested data structure management with dataclass serialization
- 📄 `Networking.py` — Network communication: socket programming, HTTP requests, and URL parsing
- 📄 `Pheromones.py` — Pheromone signaling model: enum-based chemical types, diffusion, and decay functions
- 📄 `SaltFatAcidHeat.py` — Cooking-inspired Active Inference agent using PyMDP (`inference`, `control`) with multi-dimensional flavor matrices

## Agent Instructions

- Maintain shared utility functions used across phases.
- Ensure `CogSec.py` imports resolve against `InferAnts` in `1_PREPARE/Things`.
- Preserve `DigitalTwin.py` async patterns for concurrent state updates.
- Track PyMDP version compatibility for `SaltFatAcidHeat.py`.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Import dependencies across 1_PREPARE verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
