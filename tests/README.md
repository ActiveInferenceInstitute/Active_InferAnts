# Tests

The pytest suite for Active InferAnts. Run it through the gate from the
repository root — the arms are the exact commands CI runs
([`docs/RUN_GUIDE.md`](../docs/RUN_GUIDE.md)):

```bash
./run.sh test-fast    # pytest -m "not gnn" — no GNN checkout needed
./run.sh test-full    # pytest — adds the gnn-marked module
./run.sh gnn          # provisions the pinned parser, runs validate + gnn tests
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

`test_gnn_conformance.py` is marked `gnn` at module level (the marker is
declared in `pyproject.toml`), so `pytest -m "not gnn"` and `pytest -m gnn`
partition the suite. The conformance arm is `./run.sh gnn`; it provisions the
pinned checkout and runs the module, which needs the GNN parser selected by
`GNN_ROOT`. When `GNN_ROOT` is set explicitly an unusable checkout fails rather
than skips.

Measured counts for each selection live in
[`docs/_generated/gate_metrics.md`](../docs/_generated/gate_metrics.md).

## Related

- Parent: [Active InferAnts](../README.md)
- Testing documentation: [docs/testing/](../docs/testing/README.md)
- Run guide: [`docs/RUN_GUIDE.md`](../docs/RUN_GUIDE.md)
- CI workflow: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml)
