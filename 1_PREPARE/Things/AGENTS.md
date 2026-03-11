# AGENTS.md — Things

> Agent guidance for the `1_PREPARE/Things` directory within the Active InferAnts framework.

## Purpose

Agent implementations, digital twins, and PyMDP-based Active Inference entities. This is where Active Inference agents are defined and initialized.

## Directory Contents

- 📄 `InferAnts.py` — Core `ActiveNestmate` and `ActiveColony` agent classes with NumPy-based generative models and typed parameters
- 📄 `Thing.py` — Base `Thing` abstraction using PyMDP (`inference`, `control`, `utils`) for generic Active Inference entities
- 📄 `initialize_Nestmate_Colony.py` — Colony initialization: creates `ActiveNestmate` populations with typed configuration
- 📄 `pseudo-pymdp_Ant_1.py` — Pseudo-PyMDP ant agent variant 1 with `tabulate`-based state display
- 📄 `pseudo-pymdp_Ant_2.py` — Pseudo-PyMDP ant agent variant 2 with `tabulate`-based state display
- 📄 `pymdp_Ant_1.py` — Full PyMDP ant agent using `pymdp.inference`, `pymdp.control`, `pymdp.utils`

## Agent Instructions

- Maintain the `Thing` base class hierarchy used by domain-specific agents.
- Ensure PyMDP agent implementations use consistent A/B/C/D matrix conventions.
- Preserve `ActiveNestmate`/`ActiveColony` class interfaces consumed by `CogSec.py` in `1_PREPARE/General`.
- Track PyMDP version compatibility across all `pymdp_*` files.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] PyMDP compatibility verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
