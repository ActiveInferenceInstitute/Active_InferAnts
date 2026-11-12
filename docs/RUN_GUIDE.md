# Run guide — the gate

One entry point, `./run.sh`, with separately runnable arms. Every arm is the
exact command CI runs: `.github/workflows/ci.yml` calls `./run.sh <arm>`, so a
command exists in one place and a local run exercises the same code path as the
hosted job.

GitHub Actions is billing-locked for this organisation. The arms in this guide
run locally are the only gate; a green local run is not proof that a hosted job
has run.

## Environment

One spec: `requirements-dev.txt`, which installs this project editable plus the
`dev` and `docs` extras declared in `pyproject.toml`. CI and local use the same
file and the same command.

```bash
python3 -m venv .venv            # once; or: uv venv --python 3.12 .venv
./run.sh setup                   # python -m pip install -r requirements-dev.txt
```

The interpreter is `$PYTHON` if set, else `.venv/bin/python`, else `python3`.
CI pins 3.10–3.12 (the `test` matrix); `pyproject.toml` declares `>=3.9`.

## Arms

| Arm | Command | What it checks |
|---|---|---|
| `setup` | `python -m pip install -r requirements-dev.txt` | the one environment |
| `lint` | ruff check + `ruff format --check` on the maintained surface, then `scripts/check_compile.sh` | style, imports, unused code, every tracked source compiles |
| `test-fast` | `pytest -q -m "not gnn"` | everything that needs no GNN checkout |
| `test-full` | `pytest -q` | `test-fast` plus the `gnn`-marked module |
| `docs` | `mkdocs build --strict --quiet`, `scripts/check_doc_links.py`, generated-file `--check` | site build, relative links, generated docs current |
| `gnn` | provisions the pinned parser, then `scripts/validate_gnn_spec.py` and `pytest -q -m gnn` | the Gaussian agent specification against the pinned GNN revision |
| `metrics` | `scripts/docgen/gate_metrics.py --write` | re-measures every arm, rewrites the metrics page |
| `gate` | `lint`, `test-fast`, `docs`, `gnn` | the default: everything, nothing twice |

`pytest -m "not gnn"` and `pytest -m gnn` partition the suite (the marker is
declared in `pyproject.toml`), so `gate` covers `test-full` without running any
test twice.

```bash
./run.sh                    # list the arms
./run.sh lint test-fast     # run some
./run.sh gate               # run the default gate
```

### No type-checking arm

The repository does not use a static type checker: nothing in `pyproject.toml`,
`requirements-dev.txt`, or CI configures `mypy`/`pyright`, and there is no
`[tool.mypy]` section. Annotations in the package are documentation, not a
gate. Adding one is a separate change with its own baseline.

## Where CI runs each arm

| Workflow job (key) | Display name | Arms |
|---|---|---|
| `test` | matrix over Python 3.10, 3.11, 3.12 | `setup`, `test-fast` in every cell; `lint` and `docs` once, in the 3.12 cell |
| `gnn-conformance` | `gnn conformance (pinned)` | `setup`, `gnn` |

Lint and documentation checks are interpreter-independent, so they run once
instead of repeating in each matrix cell. Every job installs from the same spec
with the same `./run.sh setup`, and `actions/setup-python` caches the pip
downloads keyed on `pyproject.toml` and `requirements-dev.txt`.

## The GNN arm

The specification `gnn/gaussian_agent.gnn.md` is validated against the upstream
revision recorded in [`../gnn/upstream.json`](../gnn/upstream.json), whose schema
is `gnn-importer-pin/v1`: `ActiveInferenceInstitute/Generalized_Notation_Notation`
at tag `v5.0.3` (commit `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`).

`./run.sh gnn` has two modes, and neither one modifies a checkout it did not
create:

- **`GNN_ROOT` unset** — provisions into a directory it just created:
  `.cache/gnn/<pin commit>`, or a fresh `.cache/gnn/<pin commit>.XXXXXX`
  beside it when that path already exists but is not a usable cache. The pinned
  parser's virtual environment lives inside it, and a complete cache for the pin
  is reused. Nothing is replaced recursively: a stale or broken cache directory
  is left in place and a new one is made.
- **`GNN_ROOT` set** — treated as read-only. The arm verifies that the checkout
  contains the pinned commit and that a runtime exists (`GNN_PYTHON`, the
  checkout's own `.venv`, or `$PY` with `numpy`/`defusedxml`), then uses it. It
  never fetches into it, never installs into it, and never removes it; an
  unusable checkout is refused with exit code 2 and a message, because that path
  may be another repository's working copy with local work in it.

Either way it then runs the two commands the conformance job has always run: the
strict script and the `gnn`-marked tests. `.github/GNN.md` records what the job
parses and what its claim covers.

## Lint surface

The `lint` arm covers the maintained Python: `active_infer_ants/`, `tests/`,
`scripts/`, `gnn_conformance.py`, and the pipeline phases `2_OPERATE/` through
`6_API/`. The rule selection is explicit in `[tool.ruff.lint]` so a linter
release cannot silently widen the gate, and Ruff is pinned in the `dev` extra.

Excluded are the multi-language implementation corpus (`0_CONTEXT/`), the
research corpora (`1_PREPARE/`), and the third-party integrations (`9_OTHER/`).
They are not lint-clean, and the measured counts under the gate's own rules are
in [`_generated/gate_metrics.md`](_generated/gate_metrics.md) rather than in
this sentence.

The pre-commit hook calls `./run.sh lint`, so a commit is checked by the gate's
own command; there is no second Ruff revision in `.pre-commit-config.yaml`.

## Measured numbers

[`_generated/gate_metrics.md`](_generated/gate_metrics.md) is generated by
`scripts/docgen/gate_metrics.py` and holds every measured number this
documentation quotes: per-arm wall time, test-selection counts, the repository
inventory, the out-of-scope lint counts, and the frozen pre-change baseline.
Do not hand-copy a number from it into prose — link it.

`./run.sh docs` fails when the recorded counts go stale (`--check`), and
`./run.sh metrics` refreshes the page (`--write`). `--write-baseline` re-freezes
the pre-change command list if the comparison ever needs to be redone.
