# TODO.md — Active InferAnts

> Project backlog / taskboard. Severity convention: **Major / Medium / Minor**.

**Owner:** Daniel Ari Friedman (Active Inference Institute)
**Status:** Active / Maintained
**Last reviewed:** 2026-11-12 (to-do refresh against `origin/main` at `d713aa17`)

---

## Open — needs an owner

These are open today. None is a defect in the maintained Python surface
(`active_infer_ants/`, `2_OPERATE/`, `3_MEASURE/`, `4_REPORT/`, `5_FOLLOWUP/`,
`6_API/` — the trees `./run.sh lint` covers); they are a version policy
decision, an organisation-level billing lock, and one unpinned corpus
dependency.

- **O-1 — the declared Python floor is never exercised.** `pyproject.toml`
  declares `requires-python = ">=3.9"`, `uv.lock` declares
  `requires-python = ">=3.9"`, and `[tool.ruff] target-version = "py39"`, but
  `.github/workflows/ci.yml` installs only `"3.10"` and `"3.11"`, and both the
  gate and the working `.venv` run 3.12.16 — so no arm ever runs on 3.9, which
  upstream reached end of life in October 2025. **Blocked on a decision, not on
  code:** either raise the floor to the lowest version actually tested and
  refresh `uv.lock` + `target-version`, or put 3.9 back in the matrix.
  **Owner:** repository maintainer (Daniel).
- **O-2 — hosted CI cannot produce evidence while the billing lock holds.**
  `gh run list -R ActiveInferenceInstitute/Active_InferAnts` reports every
  recent `CI` run on `main` as `failure` after ~4 s with no job log (#24, #25),
  and the recent `Dependabot Updates` runs appear as `failure` as well. Local
  arms are therefore the only evidence, and `.github/workflows/ci.yml` says so
  in its header. **Blocked outside this repository:** the organisation's GitHub
  Actions billing must be cleared by an organisation billing administrator.
  **Owner:** Active Inference Institute organisation admins.
- **O-3 — the corpus imports `pymdp`; nothing installs it and the sidecar
  claims it as a dependency.** `0_CONTEXT/Systems/Active_Inference/VCG.py`
  (lines 9–14) and `0_CONTEXT/Systems/IC2S2/utils_active_inference.py` (lines
  7–8) import `pymdp.POMDP`, `pymdp.maths`, `pymdp.algos`, `pymdp.utils` and
  `pymdp.agent`; `1_PREPARE/Things/Thing.py:1` and
  `1_PREPARE/General/SaltFatAcidHeat.py:2` do the same. No manifest provides the
  package — `pyproject.toml`, `requirements.txt`, `requirements-dev.txt` and
  `uv.lock` have no `pymdp`/`inferactively-pymdp` entry — while
  `.aii/config.yaml` declares `ActiveInferenceInstitute/pymdp` as
  `depends-on`. Nothing breaks today because those trees are outside
  `LINT_PATHS` in `run.sh` and the gated trees contain no `pymdp` reference
  (`git grep -i pymdp` over `tests/`, `active_infer_ants/`, `2_OPERATE/`,
  `3_MEASURE/`, `4_REPORT/`, `5_FOLLOWUP/`, `6_API/`, `scripts/` is empty), but
  the corpus cannot be run from `./run.sh setup`'s environment. **Blocked on a
  decision:** pin `inferactively-pymdp` for the corpus and add it to the gate,
  or mark the corpus archival and drop the sidecar `depends-on` relation.
  **Owner:** repository maintainer (Daniel), with the sidecar edited through the
  `aii_platform.aii_sidecar` generator if that relation changes.

---

## Gate and documentation pass — 2026-11-12

### Local evidence — 2026-11-12

Run on `origin/main` at `d713aa17` with the working `.venv` (CPython 3.12.16).
Hosted Actions is billing-locked (O-2), so these local arm runs are the evidence
for the closed items in this file:

- `./run.sh docs` — `mkdocs build --strict` clean; `checked 97 Markdown files,
  0 broken relative links`; `docs/documentation-index.md` and
  `docs/_generated/gate_metrics.md` both current.
- `./run.sh lint` — ruff check and `ruff format --check` clean (`63 files
  already formatted`); the compile sweep over every tracked Python file clean.
- `./run.sh test-fast` — `31 passed, 7 deselected`.
- `./run.sh gnn` — the shared reader's `check` against `v5.1.0`, then
  `7 passed, 31 deselected`.

### GNN-FEP member migration — adopted

- [closed] **G-10 — shared pin reader.** The
  [GNN–FEP contract](https://github.com/ActiveInferenceInstitute/Generalized_Notation_Notation/blob/main/docs/workflows/gnn-fep.md)
  gives pin parsing, pin and pointer validation, and specification validation
  one home in GNN's `src/gnn/importers.py`. This repository could not adopt it
  while its pin named a revision that predates that module: the previous pin was
  `v5.0.3` at `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`, and the migration's
  first pull request recorded that as a blocker. The pin now records `v5.1.0`
  at `75c834bd8519dc7b5adc4d24f16bf393cfd1ecdf`, which ships the reader, and
  the `gnn` arm runs it from the environment the arm already builds:
  `python -m gnn.importers check --repo . --require-pointer
  --workflow .github/workflows/ci.yml --job gnn-conformance`. This repository's
  own reader (`gnn_conformance.py`'s `Pin`, `load_pin`, `verify_pin`) and the
  tests for its pin shape are deleted; the pin declares `spec_files`, so
  validation covers `gnn/gaussian_agent.gnn.md` and not every `*.gnn.md` under
  the tree. The agent-specific checks stay: `scripts/validate_gnn_spec.py` and
  the `gnn`-marked tests still prove the extracted specification matches
  `active_infer_ants/agent.py`, which the reader cannot. No reader is vendored
  and no unpinned source is substituted. Affected: `gnn/upstream.json`,
  `gnn_conformance.py`, `run.sh`, `tests/test_gnn_conformance.py`,
  `.github/GNN.md`, `README.md`, `docs/RUN_GUIDE.md`. Re-run locally
  2026-11-12 on this branch: `./run.sh gnn` ran the shared reader at `v5.1.0`,
  then `7 passed, 31 deselected` (`tests/test_gnn_conformance.py`); the pin's
  shape is now the reader's schema, so this repository keeps no pin validator.
- [closed] **pymdp cohort — not a member.** This repository pins no
  `inferactively-pymdp`: `pyproject.toml`, `requirements.txt`,
  `requirements-dev.txt` and `uv.lock` contain no such entry, so the cohort's
  1.0.5 pin has nothing to apply to here. The `pymdp` imports that remain live
  in `0_CONTEXT/` and `1_PREPARE/` are ungated corpus code — O-3 is a separate
  question about that corpus, not a pin upgrade.

### Locked-environment follow-through

- [closed] **G-7 — shared lock and primary runtime.** `uv.lock` now resolves the
  development and docs extras. `./run.sh setup` uses `uv sync --locked`; the
  Python 3.12 `gnn-conformance` job shares that setup for lint, docs, fast tests
  and conformance instead of installing the primary project twice. The 3.10
  and 3.11 compatibility matrix remains. All jobs use the commit-pinned
  Institute `setup-python-uv` composite described in `docs/RUN_GUIDE.md`.
- [closed] **G-8 — fast default and compile startup.** No-argument `./run.sh`
  runs `test-fast`; `--help` lists arms. The compile sweep checks every tracked
  Python source in one process using the gate interpreter. `test-full`
  prepares the parser before running tests rather than relying on an implicit
  checkout. Before/after observations are generated in
  `docs/_generated/gate_metrics.md`; no hosted timing is claimed.
- [closed] **G-9 — reproducible measurement capture.** The metrics writer can
  import separately captured arm results without rerunning them and returns
  nonzero for failed arms. Baseline refresh measures the current arms rather
  than constructing and forcibly deleting an `origin/main` worktree. The
  generated flat index no longer repeats the run-guide entry.
- **Manuscript:** no `manuscript/` directory exists; no render path was added.

### Earlier gate pass (historical implementation)

- [closed] **G-1 — one gate entry point.** `./run.sh` with separately runnable
  arms (`setup`, `lint`, `test-fast`, `test-full`, `docs`, `gnn`, `metrics`,
  `gate`); `.github/workflows/ci.yml` calls those arms and nothing else. The
  inline compile sweep in CI (a second copy of `scripts/check_compile.sh`) and
  the second Ruff revision in `.pre-commit-config.yaml` are gone; the hook now
  calls `./run.sh lint`. Affected: `run.sh`, `.github/workflows/ci.yml`,
  `.pre-commit-config.yaml`, `pyproject.toml`, `requirements-dev.txt`.
- [closed] **G-2 — one environment spec.** `requirements-dev.txt` is
  `-e .[dev,docs]`; CI and local both install it with `./run.sh setup`, and the
  pip downloads are cached on `pyproject.toml` + `requirements-dev.txt`.
  `pyproject.toml` gained a `docs` extra and an explicit `[tool.ruff]` rule
  selection with Ruff pinned, so a linter release cannot silently widen the gate.
  (Superseded on the install path by G-7: `./run.sh setup` now runs
  `uv sync --locked --extra dev --extra docs`, and `requirements-dev.txt`
  remains only the pip compatibility file.)
- [closed] **G-3 — lint surface made green.** 45 mechanical violations fixed
  (unused imports, unused `except … as e`, unsorted imports), imports formatted,
  and two `lambda` assignments in `3_MEASURE/categorization.py` rewritten as
  `def`. The rule selection is explicit; the excluded trees and their measured
  counts are in `docs/RUN_GUIDE.md` and `docs/_generated/gate_metrics.md`.
- [closed] **G-4 — information now generated.** `docs/documentation-index.md`
  (`scripts/docgen/doc_index.py`) and `docs/_generated/gate_metrics.md`
  (`scripts/docgen/gate_metrics.py`) replace the hand-maintained per-section
  counts and the stale inventory table in `docs/README.md`; `./run.sh docs`
  fails when either is stale. `docs/_generated/gate_baseline.json` freezes the
  pre-change measurements, re-measurable from an `origin/main` worktree.
- [closed] **G-5 — docs hub and links.** `docs/README.md` is the hub,
  `docs/documentation-index.md` the flat index, `mkdocs.yml` excludes the hub
  (it collided with `index.md`), and links to files outside `docs/` are absolute
  repository URLs so `mkdocs build --strict` passes. `scripts/check_doc_links.py`
  checks every relative link in the tracked documentation.
- [closed] **G-6 — GNN gate documented.** The conformance job key
  (`gnn-conformance`, displayed `gnn conformance (pinned)`), the pin file
  `gnn/upstream.json` (schema `gnn-importer-pin/v1`; the revision current at the
  time was `v5.0.3`, `8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1`, since advanced
  to `v5.1.0` by G-10), and the `.github/GNN.md` pointer
  are described in `docs/RUN_GUIDE.md`, `.github/GNN.md`, `README.md`, and
  `AGENTS.md`.

---

## Documentation completion pass 3 — 2026-11-11

Verified, no new defects found:

- [closed] **DOC-1 — `docs/` index completeness.** `docs/README.md` now carries a full
  document index linking every content document in all ten sections; the tracked-file
  counts in the metrics table were refreshed (280 Python / 7,273 Markdown, measured
  2026-11-11). Affected: `docs/README.md`.
- [closed] **DOC-2 — top-level README points at the docs hub.** Added a Documentation
  section and TOC entry linking `docs/README.md`, `docs/index.md`, and the key guides;
  re-verified every command, path, and relative link in `README.md` against the tree.
  Affected: `README.md`.
- [closed] **DOC-3 — root `AGENTS.md` layout and conventions.** Directory list corrected
  to the real top-level layout; added the lint command (`pre-commit run --all-files`)
  and a Documentation pointer. Affected: `AGENTS.md`.
- [closed] **DOC-4 — folder guides for the remaining unguided folders.** Added
  `README.md` + `AGENTS.md` to `active_infer_ants/` (5 files) and `tests/` (8 files).
  `.desloppify/` is a tool artifact directory and was skipped; `gnn/` and `scripts/`
  have fewer than three tracked files. Affected: `active_infer_ants/README.md`,
  `active_infer_ants/AGENTS.md`, `tests/README.md`, `tests/AGENTS.md`.
- [closed] **DOC-5 — sidecar accuracy.** Added the `6_API` entry point to
  `artifacts[]` and hand-synced the rendered `.aii/docs/INTEGRATION.md` (the
  `aii_platform` package is unavailable offline). Affected: `.aii/config.yaml`,
  `.aii/docs/INTEGRATION.md`.

Known environment gap (resolved 2026-11-12): the working-copy `.venv` (untracked;
`.venv/` is gitignored) pointed at a Python 3.14 runtime that no longer exists on
this machine. `./run.sh setup` now (re)creates the environment from the lock —
`uv sync --locked --extra dev --extra docs`; arms use `$PYTHON`, else
`.venv/bin/python`, else `python3`, and the working `.venv` is CPython 3.12.16.
`.github/workflows/ci.yml` runs the same arms on 3.10 and 3.11 (`test` job) and
on 3.12 (`gnn-conformance`). The 3.9 floor those manifests still declare is
never exercised — see O-1.

---

## Red-team pass — measured 2026-08-01 (historical)

State recorded at the end of the red-team review and the follow-on
fix-and-push pass. **M-4 was the one Major still deferred on that date and was
closed on 2026-08-02** (entry at the end of this file), so the `2_OPERATE`
pipeline and its support modules now exist in the tree; do not read the
"remaining" note below as current.

- All **11 red-team Major findings** are resolved: M-1, M-2, M-3, M-5–M-11 in
  the fix-and-push pass, and M-4 on 2026-08-02.
- **Both REST APIs rebuilt and verified**: `Knowledge_API.py` and
  `MetaInformAnt_API.py` now parse, are internally coherent (no async misuse, no
  nonexistent-package imports), CORS-restricted, credentials from env, and pass
  real TestClient round-trips.
- **New real package** `active_infer_ants/` implements the README's public API
  (`InferenceModel`, `ActiveInferenceAgent`, `Environment`, `AntColony`,
  `PheromoneNetwork`); every README quick-start example runs.
- **Packaging / CI**: `pyproject.toml` (`pip install -e .` works),
  `requirements.txt`, `requirements-dev.txt`, `Dockerfile`, `.github/workflows/ci.yml`
  (CI), `.pre-commit-config.yaml`, `mkdocs.yml`.
- **Test suite** `tests/` (24 passing at that date; 38 collected today — 31 in
  `./run.sh test-fast`, 7 `gnn`-marked) covers the package, both APIs, the
  restricted-unpickler security fix, and the 3_MEASURE correctness fixes.
- **Then remaining, since closed:** `2_OPERATE/plan_Simulation.py` +
  `execute_Simulation.py` imported ~8 modules that did not exist anywhere in the
  tree (`MetaInformAnt_Simulation`, `data_logging`, `performance_monitor`,
  `error_handling`, `report_generator`, `computational_resources`,
  `performance_metrics`, `exception_handling`) and referenced a
  `SimulationPlanner` that `plan_Simulation.py` did not define. All nine are
  tracked files under `2_OPERATE/` now (`git ls-files 2_OPERATE`), which is the
  evidence for M-4's closure.

---

## Completed / Closed — 2026-08-01 fix-and-push pass

**Red-team review fixes (Minor/Medium implemented in the review pass), then the
Majors:** you (Daniel) lifted the STOP, so the full batch below is done.

- **[closed] M-1 — Knowledge API rebuilt+secured.** `6_API/Knowledge_API.py`
  parse error fixed, moved to consistently-synchronous SQLAlchemy (no `await` on
  sync calls), CORS restricted to env-allowed origins (no `*`), all credentials
  from `KNOWLEDGE_*` env vars, `.dict()`→`.model_dump()`, Pydantic v2
  `field_validator`. Verified via TestClient (CRUD, 409 dup, 404 missing,
  health, graceful degradation when secondary stores absent).
- **[closed] M-2 — MetaInformAnt API rebuilt.** `6_API/MetaInformAnt_API.py`
  no longer imports the nonexistent `ActiveInferAnts` package; it is now a
  self-contained service (real numpy active-inference + federated engines in
  background tasks, task status, metrics, health, env API key). Verified via
  TestClient.
- **[closed] M-3 — non-compiling Python files.** The 35 syntax-broken tracked
  files (excluding the then-broken Knowledge_API) were repaired with minimal
  syntax-only fixes (round-trip verified with `python3 -m py_compile`); zero new
  failures, and the compile-sweep is now enforced in CI.
- **[closed] M-5 — README/SPEC/packaging claims made real.** Created the
  `active_infer_ants` package, `pyproject.toml`, root `requirements.txt`,
  `requirements-dev.txt`, `Dockerfile`, GitHub Actions `.github/workflows/ci.yml`,
  `.pre-commit-config.yaml`, `mkdocs.yml`, and corrected the stale README/SPEC
  claims (5 = 50 languages; `pytest --watch`→`pytest`; coverage claim made
  honest; docs/testing 40→50).
- **[closed] M-6 — MetaProgramming RCE guard.** `modify_function` /
  `compile_ast` (arbitrary code-execution sinks) now refuse unless explicitly
  enabled (`allow_exec=True` or `META_PROGRAMMING_ALLOW_EXEC`).
- **[closed] M-7 — pymdp_Ant_1 checkpoint load hardened.** Added an explicit
  warning that `allow_pickle=True` unpickles the file, plus strict schema
  validation so a malformed/tampered checkpoint fails closed.
- **[closed] M-8 — memory metrics measure the process tree.** `reporting_system.py`
  and `benchmark_suite.py` now sample peak/average RSS across the process and its
  recursive children (the language binary), not the wrapper/parent process.
- **[closed] M-9 — specify_measure made honest.** `ProjectiveMeasurementStrategy`
  and `POVMMeasurementStrategy` now implement real Born-rule measurements;
  Weak / Continuous / Adaptive raise `NotImplementedError` instead of returning
  fabricated random projections.
- **[closed] M-10 — security_monitor fixed.** `_is_malicious_ip` validates the IP
  (ipaddress) before interpolating it into the threat-intel URL (closes the
  Bearer-key leak injection); `detect_brute_force` returns a bool and no longer
  calls `trigger_incident_response()` with the wrong arity.
- **[closed] M-11 — security-utility cluster.** `encryption.py` no longer reads
  the nonexistent `key_rotation_policy` field, initializes `operation_counter`,
  and surfaces `NotImplementedError` for HSM/FIPS instead of referencing
  undefined state; `repo_security.py` persists its Fernet key (encrypted findings
  are now recoverable); FOIA hardcoded secret moved to an env var; the three
  GitHub clone helpers now sanitize + contain the clone path.

- **[closed] Review-pass Medium/Minor implementations** (from the red-team pass,
  retained): test_suite false-FAIL heuristic removed; benchmark entropy ranking
  direction fixed; `categorization.compute_colimit` now stores+returns;
  `summarize._agents_entropy` normalised; `statistics` NaN alignment;
  `quantum_security` imports; `hashing` HIBP plaintext-leak + complexity + lru_cache;
  `Networking.fetch_website_content` SSRF/size-cap; `config_manager` broken
  installers; `run_all.sh` not-found failure; `Student_Teacher` filename-case +
  seeding; serialization restricted unpickler.

### Red-team review pass: Medium/Minor already done (before the push pass)
See the 2026-08-01 review record — all listed there were implemented and verified
before the fix-and-push pass (the two API files were then reworked as M-1/M-2,
the 35 broken files as M-3).

---

## Documentation deep review — 2026-08-02

Severity definitions: **Minor** = typo, broken link, formatting, or small factual correction; **Medium** = stale section rewrite, documentation restructure, or missing guide; **Major** = large documentation-system or cross-cutting documentation refactor.

### Minor

- [closed] **D-1 — Keep the root README's operational promises source-backed.** Removed unsupported response-time guarantees and coverage/performance/security percentages; dependencies overview corrected against `requirements.txt`; stale internal links repaired. Affected: `README.md`. ✓ (docs: align README with repository reality)
- [closed] **D-2 — Align configuration and dependency prose with the manifests and root `config.json`.** `docs/reference/dependencies.md` rewritten against `pyproject.toml`/`requirements.txt`; `config.json` `initial_values` nesting documented in `docs/api/data_models.md`, `docs/architecture/pipeline_overview.md`, and `docs/reference/configuration.md`. Affected: `docs/reference/configuration.md`, `docs/reference/dependencies.md`, `docs/architecture/pipeline_overview.md`. ✓ (docs: align config/dependency references with manifests)
- [closed] **D-3 — Correct stale CLI examples.** `test_suite.py --report` and `config_manager.py --check/--update/--set` replaced with the actual flags; `run_all.sh --setup` replaced with `master_controller.py setup`. Affected: `README.md`, `docs/tutorials/benchmarking.md`. ✓ (docs: correct CLI examples)

### Medium

- [closed] **D-4 — Replace stale 40-language and repository-count claims with registry/source-backed values.** `languages.json` (50) is now the cited source everywhere; tracked counts updated to 266 Python files / 7,262 Markdown files; the language matrix now lists all 50 registered languages with verified main files. Affected: `docs/README.md`, `docs/SPEC.md`, `docs/reference/language_matrix.md`, `docs/concepts/multi_language_design.md`, `docs/architecture/` and `docs/testing/` pages. ✓ (docs: 50-language and count claims match registry)
- [closed] **D-5 — Repair broken API source links and deployment examples.** Source links now resolve to root `6_API/`; Swagger paths corrected to `/api/docs` + `/api/redoc`; curl example fixed; auth semantics documented as env-enabled. Affected: `docs/api/knowledge_api.md`, `docs/api/metainformant_api.md`, `docs/operations/api_deployment.md`. ✓ (docs: fix API documentation)
- [closed] **D-6 — Replace stale root tooling claims and missing contribution/legal links.** Ruff/MkDocs/GitHub Actions replace Black/Flake8/MyPy/Bandit/Sphinx; links to absent `docs/CONTRIBUTING.md`, `docs/CODE_OF_CONDUCT.md`, `docs/THIRD_PARTY_LICENSES.md` repointed to the existing contribution guide. Affected: `README.md`. ✓ (docs: align README with repository reality)

### Major

- [closed] **D-7 — Repair the MkDocs documentation navigation.** `mkdocs.yml` and `docs/index.md` now reference the existing section `README.md` indexes; validated that every nav target resolves. Affected: `mkdocs.yml`, `docs/index.md`. ✓ (docs: fix MkDocs navigation)
- [closed] **D-8 — Make the simulation quickstart honest about the deferred 2_OPERATE pipeline and provide a verified package/API path.** The getting-started guide now leads with the working `active_infer_ants` package and CLI; the deferred M-4 status is flagged in the guide and pipeline pages. Affected: `docs/guides/getting_started.md`, `docs/guides/running_simulations.md`, `docs/tutorials/running_pipeline.md`, `docs/architecture/pipeline_overview.md`. ✓ (docs: honest simulation quickstart)

## Major — closed

- [closed] **M-4 — `2_OPERATE` plan→execute→render pipeline (closed
  2026-08-02).** The pipeline was rebuilt and wired to the
  now-realisable `active_infer_ants` simulation API:
  - Built the missing support modules in `2_OPERATE/`: `environment.py`
    (grid world with pheromone field), `MetaInformAnt_Simulation.py`
    (`MetaInformAntSimulation` driving `active_infer_ants` agents),
    `data_logging.py`, `performance_monitor.py`, `performance_metrics.py`,
    `error_handling.py`, `exception_handling.py`, `report_generator.py`,
    `computational_resources.py`, `visualization.py`.
  - `plan_Simulation.py` now defines the `SimulationPlanner` class the
    executor imports (with `SimulationSetup` retained as an alias), reads the
    real `1_PREPARE/configs` dictionaries, and seeds randomness explicitly
    (no unseeded `np.random`).
  - `execute_Simulation.py` imports only existing modules, runs the
    plan → execute → render lifecycle, and guards the optional per-agent
    visualizer (which expects matrix attributes the `active_infer_ants`
    agents do not carry).
  - `render_Simulation.py` gained the executor-facing methods
    (`initialize_environment`, `refresh_visualization`,
    `visualize_post_simulation`).
  - Integration suite `tests/test_simulation_pipeline.py` (7 tests) covers
    environment contract, seeded reproducibility, planner/executor end-to-end
    runs, and the support modules. Full suite at that date: 31 passed
    (38 collected today: 31 in `./run.sh test-fast`, 7 `gnn`-marked);
    compile-sweep and ruff (new files) clean. ✓ (fix: rebuild 2_OPERATE
    pipeline on active_infer_ants)
