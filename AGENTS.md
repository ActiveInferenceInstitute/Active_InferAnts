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
- 📁 `scripts/` — `validate_gnn_spec.py` and `check_compile.sh`
- 📁 `docs/` — the modular documentation tree (index: `docs/README.md`)
- 📁 `.aii/` — committed InstituteOS sidecar (metadata only)
- 📁 `.github/` — CI workflow and Dependabot configuration
- 📄 `README.md`, `SPEC.md`, `governance.md`, `TODO.md`, `REVIEW_LOG_2026-08-02.md`
- 📄 `pyproject.toml`, `requirements.txt`, `requirements-dev.txt`, `config.json`
- 📄 `Dockerfile`, `mkdocs.yml`, `gnn_conformance.py`, `scorecard.png`, `LICENSE`

## Tests

Run the unit suite from the repository root:

```bash
python -m pytest -q
```

The suite in `tests/` covers the `active_infer_ants/` package and both REST APIs; the GNN
conformance test is described below. Lint and format with the pinned pre-commit hooks:

```bash
pre-commit run --all-files
```

## Documentation

Documentation is modular, one topic per file, under `docs/`. Start at the index
[`docs/README.md`](docs/README.md); `docs/index.md` is the MkDocs home page and `mkdocs.yml`
holds the navigation. Each `docs/<section>/` directory carries its own `README.md`,
`AGENTS.md`, and `SPEC.md`. Keep the index in step when adding or renaming a document.

## Agent Instructions

- This is the repository root. Coordinate across all phase directories.
- Maintain the 6-phase operational pipeline consistency.
- Ensure cross-language implementation parity.
- Keep `gnn/gaussian_agent.gnn.md` in step with `active_infer_ants/agent.py`; validate it
  with `python scripts/validate_gnn_spec.py` (needs the GNN checkout pinned in
  `gnn/upstream.json`) or `python -m pytest tests/test_gnn_conformance.py`. CI runs both in
  the `gnn conformance (pinned)` job, which fetches the pinned revision from the
  public upstream repository and provisions its interpreter, so the pin is re-checked on
  every push and pull request. GNN's
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
