# GNN conformance

`gnn conformance (pinned)` is the job key `gnn-conformance` in
`.github/workflows/ci.yml`; it runs the single gate arm `./run.sh gnn`
(documented in [`../docs/RUN_GUIDE.md`](../docs/RUN_GUIDE.md#the-gnn-arm)).
It reads the pin record `gnn/upstream.json` (schema `gnn-importer-pin/v1`),
which pins `ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.0.3`
(`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`).

The arm fetches that commit into its own cache, then runs
`scripts/validate_gnn_spec.py` and `python -m pytest -q -m gnn` (the
`gnn`-marked module `tests/test_gnn_conformance.py`). A `GNN_ROOT` supplied by
the caller is read-only: the arm verifies that checkout and refuses (exit 2)
instead of fetching, installing or deleting inside it. The script extracts
`gnn/gaussian_agent.gnn.md` with the extractor from the pinned commit and
checks the extracted matrices against the framework agent in
`active_infer_ants`; the tests assert the canonical pin record, the spec's
required `##` sections, the declared state dimensions, and that a mutated
model is rejected. It does not scan the rest of the repository for `*.gnn.md`;
the claim covers that one specification.
