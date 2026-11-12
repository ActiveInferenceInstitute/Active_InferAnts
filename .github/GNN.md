# GNN conformance

`gnn conformance (pinned)` is the job key `gnn-conformance` in
`.github/workflows/ci.yml`; it runs the single gate arm `./run.sh gnn`
(documented in [`../docs/RUN_GUIDE.md`](../docs/RUN_GUIDE.md#the-gnn-arm)).
It reads the pin record `gnn/upstream.json` (schema `gnn-importer-pin/v1`),
which pins `ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.1.0`
(`75c834bd8519dc7b5adc4d24f16bf393cfd1ecdf`) and declares the one
specification this repository validates, `gnn/gaussian_agent.gnn.md`.

The arm fetches that commit into its own cache, then runs the shared GNN-FEP
reader from that cache as `python -m gnn.importers check --repo .`, so the pin,
its shape and the specification's syntax are validated by the reader the pinned
revision ships, not by a copy kept here. It then runs
`scripts/validate_gnn_spec.py` and `python -m pytest -q -m gnn` (the
`gnn`-marked module `tests/test_gnn_conformance.py`). A `GNN_ROOT` supplied by
the caller is read-only: the arm verifies that checkout and refuses (exit 2)
instead of fetching, installing or deleting inside it. The script extracts
`gnn/gaussian_agent.gnn.md` with the extractor from the pinned commit and
checks the extracted matrices against the framework agent in
`active_infer_ants`; the tests assert the pin record through the shared reader,
the spec's required `##` sections, the declared state dimensions, and that a
mutated model is rejected. The pin's `spec_files` entry is authoritative, so the
claim covers that one specification and not the rest of the tree.

The primary Python 3.12 job shares one `./run.sh setup` environment from
`uv.lock` across lint, docs, fast tests and conformance. It uses
`ActiveInferenceInstitute/.github/.github/actions/setup-python-uv@7159e67315330aac8e414aebae0ad1e999a41448`
to install Python and uv; project dependency installation stays in `run.sh`.
