# Run guide — the gate

`./run.sh` is the single entry point. CI invokes the same arms; commands are
not duplicated in workflow YAML. With no arguments it runs `test-fast`.
`./run.sh --help` lists the arms; `./run.sh gate` runs the complete local gate.

GitHub Actions is billing-locked for this organisation. Local runs are the
only gate; a green local run is not proof that a hosted job has run.

## Environment

Use uv 0.13.7, the version installed by the pinned Institute composite action.
Dependencies are declared in `pyproject.toml`; the universal `uv.lock` is shared
by local setup and every CI interpreter. Refresh it with `uv lock` after an
intentional dependency change, then run:

```bash
./run.sh setup                   # uv sync --locked --extra dev --extra docs
./run.sh                         # fast tests; no setup or downloads
./run.sh lint docs               # selected arms
./run.sh gate                    # complete local gate, no overlapping tests
```

Setup selects `$UV_PYTHON`, else the gate interpreter (`$PYTHON`, then the
existing `.venv/bin/python`, then `python3`). For a new environment matching the
primary CI job, use `UV_PYTHON=3.12 ./run.sh setup`. Other arms never sync the
environment; they use `$PYTHON`, `.venv/bin/python`, or `python3`, in that order.
The compile sweep uses that same interpreter in one process, rather than
starting a different host `python3` for each source file.

`requirements-dev.txt` remains a compatibility pip install of the declared
extras, not a second CI environment. It does not enforce the lock.
`pyproject.toml` declares Python `>=3.9`; CI retains its existing 3.10–3.12
coverage. Local verification on this host covers the interpreter recorded in
the [generated metrics](_generated/gate_metrics.md), not the whole CI matrix.

## Arms

| Arm | Checks |
|---|---|
| `setup` | Synchronise the locked development and documentation extras |
| `lint` | Ruff check and format check on maintained Python; compile every tracked Python source |
| `test-fast` | `pytest -q -m "not gnn"`; no parser checkout needed |
| `test-full` | Prepare the pinned parser, then `pytest -q`; includes conformance tests |
| `docs` | Strict MkDocs build, relative links, generated index and metrics freshness |
| `gnn` | Prepare the pinned parser, strict specification validator, then `pytest -q -m gnn` |
| `metrics` | Measure the arms and refresh the generated metrics document |
| `gate` | `lint`, `test-fast`, `docs`, `gnn`; full coverage without repeated tests |

`test-fast` and `gnn` partition the suite using the declared `gnn` marker.
`test-full` is a standalone alternative, not an additional step in `gate` or CI.
It prepares the parser first so a missing checkout cannot silently turn the
full run into a skipped-parser run.

### No type-checking arm

No static type checker is configured in `pyproject.toml`, the dependency spec,
or CI. Annotations are documentation, not a mypy/pyright gate.

## Where CI runs each arm

| Job key | Display name | Python | Arms |
|---|---|---|---|
| `test` | `test` matrix | 3.10, 3.11 | `setup`, `test-fast` |
| `gnn-conformance` | `gnn conformance (pinned)` | 3.12 | `setup`, `lint`, `docs`, `test-fast`, `gnn` |

The primary interpreter now installs once for lint, docs, ordinary tests and
conformance, instead of provisioning the same project environment in two jobs.
Older-interpreter compatibility jobs necessarily have independent environments;
all resolve from the same lock. Lint and docs run only once, and no CI job runs
`test-full` on top of its two constituent selections.

Both job definitions use the exact composite action
`ActiveInferenceInstitute/.github/.github/actions/setup-python-uv@7159e67315330aac8e414aebae0ad1e999a41448`.
It installs uv and the requested Python and caches uv dependencies keyed by
`uv.lock`; it does not install this project. `./run.sh setup` owns that step.

## The GNN arm

The canonical pin is [`gnn/upstream.json`](https://github.com/ActiveInferenceInstitute/Active_InferAnts/blob/main/gnn/upstream.json), schema
`gnn-importer-pin/v1`: `ActiveInferenceInstitute/Generalized_Notation_Notation`
at `v5.0.3`, revision `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`.
[`.github/GNN.md`](https://github.com/ActiveInferenceInstitute/Active_InferAnts/blob/main/.github/GNN.md) records exactly what the
`gnn-conformance` job, displayed `gnn conformance (pinned)`, parses:
`gnn/gaussian_agent.gnn.md`, not a repository-wide scan. Its extracted matrices
and Gaussian posterior update are checked against `active_infer_ants/agent.py`.

Both `gnn` and `test-full` prepare the parser in the same way:

- **`GNN_ROOT` unset:** reuse the verified owned cache at
  `.cache/gnn/<pin commit>`, or provision a fresh owned directory. An occupied,
  unusable cache is preserved; a new sibling is created instead. Initial
  acquisition needs network access; provision it before an offline gate.
- **`GNN_ROOT` set:** treat it as read-only. Verify the pinned commit and runtime
  (`GNN_PYTHON`, the checkout's `.venv`, or the project interpreter with
  `numpy`/`defusedxml`). Refuse an unusable checkout with exit 2; never fetch,
  install, or delete inside it.

The validator reads parser sources from the pinned commit with `git archive`,
not from the checkout's potentially edited working tree.

## Lint surface

Maintained Python is `active_infer_ants/`, `tests/`, `scripts/`,
`gnn_conformance.py`, and pipeline phases `2_OPERATE/` through `6_API/`.
Ruff and its rule selection are explicit in `pyproject.toml` and the lock.
The multi-language corpus (`0_CONTEXT/`), research corpus (`1_PREPARE/`) and
third-party integrations (`9_OTHER/`) remain outside lint; the generated
metrics record their findings. Every tracked Python file still compiles in
`lint`. The pre-commit hook invokes `./run.sh lint`, not another Ruff version.

## Measured numbers

[`_generated/gate_metrics.md`](_generated/gate_metrics.md) is the single
generated document for arm wall times, selection counts, inventory and the
before/after comparison. The pre-change snapshot is stored in
`docs/_generated/gate_baseline.json`. Do not copy these numbers into prose.

```bash
# Before changing the gate:
python scripts/docgen/gate_metrics.py --write-baseline
# After changing it:
python scripts/docgen/doc_index.py --write
./run.sh metrics
```

The metrics writer returns nonzero if any measured arm fails. The docs arm
checks count freshness. For source-bound offline runs that must not rewrite
tracked files during execution, capture an arm-keyed JSON object first
(`seconds`, `exit`, and `detail` or raw `output` per arm), then publish it without
re-running the arms:

```bash
python scripts/docgen/gate_metrics.py --write --measurements /path/to/results.json
```

The same import option works with `--write-baseline`; capture that before
editing and import before changing HEAD. Measurements include arm subprocesses
but exclude environment setup and initial parser acquisition. One sample per
arm is an observation, not a statistical performance claim.
