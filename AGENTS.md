# AGENTS.md — Active InferAnts

> Agent guidance for the `.` directory within the Active InferAnts framework.

## Purpose

Multi-language Active Inference framework for advanced AI research and applications.

## Directory Contents

- 📁 `0_CONTEXT/` — research context, specifications, and the multi-language implementations
- 📁 `1_PREPARE/` — data preparation, configuration, and foundational components
- 📁 `2_OPERATE/` — simulation planning, execution, and rendering
- 📁 `3_MEASURE/` — analysis, statistics, and performance measurement
- 📁 `4_REPORT/` — report generation
- 📁 `5_FOLLOWUP/` — follow-up actions and continuous improvement
- 📁 `6_API/` — the Knowledge and MetaInformAnt REST APIs
- 📁 `9_OTHER/` — third-party integrations and specialized modules
- 📁 `gnn/` — GNN specification of the Gaussian agent and the pinned upstream revision
- 📁 `active_infer_ants/` — the installable core Python package
- 📁 `tests/` — the pytest suite
- 📁 `scripts/` — `validate_gnn_spec.py`, `check_compile.sh`, `check_doc_links.py`, and the
  `docgen/` generators behind `docs/documentation-index.md` and the gate metrics
- 📁 `docs/` — the modular documentation tree (index: `docs/README.md`)
- 📁 `.aii/` — committed InstituteOS sidecar (metadata only)
- 📁 `.github/` — CI workflow and Dependabot configuration
- 📄 `README.md`, `SPEC.md`, `governance.md`, `TODO.md`, `REVIEW_LOG_2026-08-02.md`
- 📄 `pyproject.toml`, `uv.lock`, `requirements.txt`, `requirements-dev.txt`, `config.json`
- 📄 `Dockerfile`, `mkdocs.yml`, `gnn_conformance.py`, `run.sh`, `scorecard.png`, `LICENSE`

## Tests and the gate

`./run.sh` is the single entry point; no arguments runs fast tests, and CI calls its arms.
The suite in `tests/` covers the `active_infer_ants/` package and both REST
APIs; the GNN conformance module is described below.

```bash
./run.sh setup        # uv sync --locked --extra dev --extra docs
./run.sh lint         # ruff (maintained surface) + compile sweep of every tracked source
./run.sh test-fast    # pytest -m "not gnn"
./run.sh test-full    # pytest (adds the gnn-marked module)
./run.sh docs         # mkdocs --strict, relative links, generated docs current
./run.sh gnn          # pinned GNN parser + specification conformance
```

The pre-commit hook calls `./run.sh lint`, so a commit is checked by the same
command. Arms, the lint surface, and where CI runs each one:
[`docs/RUN_GUIDE.md`](docs/RUN_GUIDE.md). Measured wall times and test counts:
[`docs/_generated/gate_metrics.md`](docs/_generated/gate_metrics.md) — link it,
never restate the numbers.

## Documentation

Documentation is modular, one topic per file, under `docs/`. Start at the hub
[`docs/README.md`](docs/README.md); [`docs/index.md`](docs/index.md) is the
MkDocs home page (`mkdocs.yml` excludes the hub so the two do not collide) and
`mkdocs.yml` holds the navigation. [`docs/documentation-index.md`](docs/documentation-index.md)
is the generated flat index, and `docs/_generated/` holds generated facts. Each
`docs/<section>/` directory carries its own `README.md`, `AGENTS.md`, and
`SPEC.md`. Regenerate the generated pages with
`python scripts/docgen/doc_index.py --write` and `./run.sh metrics`; `./run.sh docs`
fails when they are stale.

## Agent Instructions

- This is the repository root. Coordinate across all phase directories.
- Maintain the 6-phase operational pipeline consistency.
- Ensure cross-language implementation parity.
- Keep `gnn/gaussian_agent.gnn.md` in step with `active_infer_ants/agent.py`; validate it
  with `./run.sh gnn`, which fetches the revision pinned in `gnn/upstream.json` (schema
  `gnn-importer-pin/v1`) into its own cache and runs both the strict script and the
  `gnn`-marked tests. A `GNN_ROOT` you set is read-only: the arm verifies it and refuses
  instead of fetching, installing or deleting inside it. CI runs the same arm in the
  `gnn-conformance` job, displayed as `gnn conformance (pinned)` (see
  [`.github/GNN.md`](.github/GNN.md)), so the pin is re-checked on every push and pull
  request. GNN's
  [downstream adoption
  guide](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/blob/main/docs/gnn/integration/downstream_adoption.md)
  documents the adoption patterns, pin discipline, and drift-guard checks used here.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Maintain consistency with parent and sibling directory conventions.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Directory structure reflects current organization
- [ ] Cross-references to related directories verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
