# GNN conformance

`gnn conformance (pinned)` is the `gnn-conformance` job in
`.github/workflows/ci.yml`; it reads the pin record `gnn/upstream.json`, which
pins `ActiveInferenceInstitute/Generalized_Notation_Notation` at `v5.0.3`
(`8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`).

The job fetches that commit into its own runtime, then runs
`scripts/validate_gnn_spec.py` and
`python -m pytest tests/test_gnn_conformance.py -q`. The script extracts
`gnn/gaussian_agent.gnn.md` with the extractor from the pinned commit and
checks the extracted matrices against the framework agent in
`active_infer_ants`; the tests assert the canonical pin record, the spec's
required `##` sections, the declared state dimensions, and that a mutated
model is rejected. It does not scan the rest of the repository for `*.gnn.md`;
the claim covers that one specification.
