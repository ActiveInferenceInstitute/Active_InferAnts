# AGENTS.md — `tests`

> Agent guidance for the `tests` directory within the Active InferAnts framework.

## Purpose

The pytest suite covering the `active_infer_ants` package, both REST APIs, the
3_MEASURE correctness fixes, the serializer security fix, the 2_OPERATE
simulation pipeline, and the GNN specification conformance.

## Directory Contents

- 📄 `conftest.py` — path setup and matplotlib `Agg` backend
- 📄 `test_active_infer_ants.py` — package public API
- 📄 `test_knowledge_api.py` — Knowledge API CRUD/status codes
- 📄 `test_meta_api.py` — MetaInformAnt API engines/endpoints
- 📄 `test_measure_fixes.py` — 3_MEASURE correctness fixes
- 📄 `test_serializer.py` — restricted-unpickler security fix
- 📄 `test_simulation_pipeline.py` — 2_OPERATE pipeline integration
- 📄 `test_gnn_conformance.py` — GNN specification conformance

## Agent Instructions

- Run the suite with `python -m pytest -q` from the repository root.
- Never weaken or rewrite a test to make it pass; fix the code or the specification.
- Keep `test_gnn_conformance.py`'s structural checks runnable without the GNN checkout.
- Add a focused test with every behavior change; prefer deterministic, seeded inputs.
- Follow the repository's CC BY-NC-ND 4.0 license.

## Quality Checklist

- [ ] `python -m pytest -q` passes
- [ ] New behavior has a focused test
- [ ] README.md synchronized with this AGENTS.md
