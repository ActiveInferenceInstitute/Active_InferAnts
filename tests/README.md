# Tests

The pytest suite for Active InferAnts. Run it from the repository root:

```bash
python -m pytest -q
```

[`conftest.py`](conftest.py) puts the flat, non-package phase directories
(`2_OPERATE/`, `3_MEASURE/`, `6_API/`, `0_CONTEXT/Computer_Languages/`, …) on
`sys.path` and forces the non-interactive matplotlib `Agg` backend.

## Test modules

| Module | Covers |
|--------|--------|
| [`test_active_infer_ants.py`](test_active_infer_ants.py) | The `active_infer_ants` package public API |
| [`test_knowledge_api.py`](test_knowledge_api.py) | Knowledge API CRUD and status codes |
| [`test_meta_api.py`](test_meta_api.py) | MetaInformAnt API engines and endpoints |
| [`test_measure_fixes.py`](test_measure_fixes.py) | The 3_MEASURE correctness fixes |
| [`test_serializer.py`](test_serializer.py) | The restricted-unpickler security fix |
| [`test_simulation_pipeline.py`](test_simulation_pipeline.py) | The 2_OPERATE plan → execute → render pipeline |
| [`test_gnn_conformance.py`](test_gnn_conformance.py) | The Gaussian agent GNN specification against the pinned revision |

`test_gnn_conformance.py` always runs its structural half; the pinned-parser half
needs the GNN checkout selected by `GNN_ROOT` and is exercised in CI by the
`gnn conformance (pinned)` job. When `GNN_ROOT` is set explicitly an unusable
checkout fails rather than skips.

## Related

- Parent: [Active InferAnts](../README.md)
- Testing documentation: [docs/testing/](../docs/testing/README.md)
- CI workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
