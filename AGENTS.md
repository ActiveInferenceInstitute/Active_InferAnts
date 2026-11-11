# AGENTS.md — Active InferAnts

> Agent guidance for the `.` directory within the Active InferAnts framework.

## Purpose

Multi-language Active Inference framework for advanced AI research and applications.

## Directory Contents

- 📁 `0_CONTEXT/`
- 📁 `1_PREPARE/`
- 📁 `2_OPERATE/`
- 📁 `3_MEASURE/`
- 📁 `4_REPORT/`
- 📁 `5_FOLLOWUP/`
- 📁 `6_API/`
- 📁 `9_OTHER/`
- 📁 `gnn/`
- 📁 `active_infer_ants/`
- 📁 `tests/`
- 📁 `scripts/`
- 📁 `docs/`
- 📁 `.aii/`
- 📄 `LICENSE`
- 📄 `README.md`
- 📄 `SPEC.md`
- 📄 `config.json`
- 📄 `governance.md`
- 📄 `pyproject.toml`
- 📄 `requirements.txt`
- 📄 `requirements-dev.txt`
- 📄 `Dockerfile`
- 📄 `mkdocs.yml`

## Tests

Run the unit suite from the repository root:

```bash
python -m pytest -q
```

The suite in `tests/` covers the `active_infer_ants/` package and both REST APIs; the GNN
conformance test is described below.

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
