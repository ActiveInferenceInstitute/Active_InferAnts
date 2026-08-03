# Documentation Deep Review — 2026-08-02

## Scope

DOCS-DEEP review of the repository root documentation, `docs/`, MkDocs configuration, CI/development metadata, and documentation claims checked against tracked files and Python source.

## Preflight

- Branch: `main`
- Default remote branch: `origin/main`
- Initial HEAD: `307bab1`
- `git fetch origin` and `git pull --ff-only origin main`: already up to date
- Initial working tree: clean
- Documentation surface: `docs/` contains 48 topic documents plus hub metadata; the repository contains 7,262 tracked Markdown files, including the large phase archive.

## Findings

### Major

1. MkDocs navigation and the documentation hub linked ten missing `docs/<section>/index.md` files. The existing section `README.md` files are the actual indexes.
2. The documentation architecture described a runnable 2_OPERATE simulation pipeline even though the repository TODO records unresolved imports and class-contract mismatches in that pipeline. The user-facing getting-started/tutorial pages needed an explicit limitation and a verified package quickstart.

### Medium

1. Several hub/reference documents claimed 40 language implementations while the canonical `languages.json` registry contains 50 entries and the root documentation uses 50.
2. `docs/README.md` reported stale repository counts (254 Python modules, 40 languages, 7,100+ docs); current tracked counts are 266 Python files, 50 registry languages, and 7,262 Markdown files.
3. Root README linked missing `docs/CONTRIBUTING.md`, `docs/CODE_OF_CONDUCT.md`, and `docs/THIRD_PARTY_LICENSES.md`; the contribution guide exists at `docs/guides/contributing.md`, while the other two files do not exist.
4. API source links in `docs/api/` resolved to `docs/6_API/...` instead of the repository-root `6_API/...` directory.
5. API deployment documentation used the wrong Swagger paths and contained a malformed `curl` example; current FastAPI configuration exposes `/api/docs` and `/api/redoc`.
6. Root development/tooling prose named Black, Flake8, MyPy, Bandit, and Sphinx although the repository's configured Python quality tooling is Ruff plus compile checks and pytest.
7. Several documentation pages listed commands or examples that were not supported by the current CLI (notably `test_suite.py --report` and `config_manager.py --help` semantics).

### Minor

1. The root README contained stale or unsupported internal documentation links and unverified operational promises (response-time guarantees, coverage/performance percentages, and community/funding claims).
2. The configuration/dependency documentation diverged from `pyproject.toml`, `requirements.txt`, and the actual root `config.json` shape.
3. A few pages repeated the old 40-language wording and needed cross-linking to the canonical language registry and section indexes.

## M-4 implementation — 2026-08-02 (second pass, "do all improvements comprehensively")

Closed the last open Major item: the `2_OPERATE` plan→execute→render pipeline
was rebuilt on the real `active_infer_ants` API instead of the ~10 modules it
referenced that did not exist anywhere in the tree.

- New support modules in `2_OPERATE/`: `environment.py` (2D grid world with
  pheromone field matching the renderer contract), `MetaInformAnt_Simulation.py`
  (`MetaInformAntSimulation` — `active_infer_ants` agents acting in the grid),
  `data_logging.py`, `performance_monitor.py`, `performance_metrics.py`,
  `error_handling.py`, `exception_handling.py`, `report_generator.py`,
  `computational_resources.py`, `visualization.py`.
- `plan_Simulation.py`: defines `SimulationPlanner` (executor's import) with
  `SimulationSetup` retained as an alias; reads the real `1_PREPARE/configs`
  dictionaries via a path bootstrap; explicit seed (default 0), no unseeded
  RNG; parallel-execution setting validated and reported (runs sequential).
- `execute_Simulation.py`: imports only existing modules; `max_steps`,
  `output_dir`, and interval parameters exposed; optional per-agent
  visualizer guarded (the `ConcreteAgentVisualizer` requires matrix
  attributes the `active_infer_ants` agents do not carry — logged, non-fatal).
- `render_Simulation.py`: added the executor-facing methods
  (`initialize_environment`, `refresh_visualization`,
  `visualize_post_simulation`).
- `tests/conftest.py`: added `2_OPERATE` and `1_PREPARE/configs` to the
  flat-module `sys.path` bootstrap.
- New `tests/test_simulation_pipeline.py` (7 tests): environment contract,
  seeded reproducibility, planner/executor end-to-end, support modules.
- Verification: full pytest suite 31 passed; compile-sweep over all tracked
  `.py` clean; ruff check+format clean on all new/changed files (pre-existing
  2_OPERATE files still have baseline ruff findings, untouched).
- Docs updated: `docs/guides/getting_started.md`,
  `docs/guides/running_simulations.md`, `docs/tutorials/running_pipeline.md`
  now describe the pipeline as runnable (the "under repair" flags from the
  first pass are removed); `docs/architecture/pipeline_overview.md` lists the
  real classes; `TODO.md` M-4 marked CLOSED.

Heavy suites not run: full cross-language execution and mkdocs build (mkdocs
not installed in the repo venv); the pipeline integration is covered by pytest
with the Agg matplotlib backend instead.
