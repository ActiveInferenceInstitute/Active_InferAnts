# AGENTS.md — `active_infer_ants`

> Agent guidance for the `active_infer_ants` directory within the Active InferAnts framework.

## Purpose

The installable core Python package: the public API (`InferenceModel`,
`ActiveInferenceAgent`, `Environment`, `AntColony`, `PheromoneNetwork`) advertised
by the repository README.

## Directory Contents

- 📄 `__init__.py` — public re-exports and `__version__`
- 📄 `agent.py` — `ActiveInferenceAgent`
- 📄 `environment.py` — `Environment`
- 📄 `colony.py` — `AntColony`, `PheromoneNetwork`
- 📄 `model.py` — `InferenceModel`

## Agent Instructions

- Keep the public API in sync with the README examples and `__init__.__all__`.
- Keep `agent.py` consistent with `../gnn/gaussian_agent.gnn.md`; validate with
  `python scripts/validate_gnn_spec.py` or `python -m pytest tests/test_gnn_conformance.py`.
- Keep implementations dependency-light (NumPy) and deterministic where tests rely on seeding.
- Update `README.md` here and the parent `docs/` pages when the API changes.
- Follow the repository's CC BY-NC-ND 4.0 license.

## Quality Checklist

- [ ] Public API matches the README and `__all__`
- [ ] GNN specification still matches `agent.py`
- [ ] README.md synchronized with this AGENTS.md
