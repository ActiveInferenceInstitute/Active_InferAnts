# TODO.md — Active InferAnts

> Project backlog / taskboard. Severity convention: **Major / Medium / Minor**.

**Owner:** Daniel Ari Friedman (Active Inference Institute)
**Status:** Active / Maintained
**Last reviewed:** 2026-08-02 (documentation deep review; D-1 … D-8 scoped and closed, see below)

---

## Current status — measured 2026-08-01

Working copy on branch `main` (up to date with `origin/main`). State after the
red-team review and follow-on fix-and-push pass:

- All **11 red-team Major findings** are resolved except **M-4** (2_OPERATE
  pipeline — see below), which is deferred with a concrete reason.
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
- **Test suite** `tests/` (24 passing) covers the package, both APIs, the
  restricted-unpickler security fix, and the 3_MEASURE correctness fixes.
- **Remaining** `2_OPERATE/plan_Simulation.py` + `execute_Simulation.py` import
  ~8 modules that do not exist anywhere in the tree
  (`MetaInformAnt_Simulation`, `data_logging`, `performance_monitor`,
  `error_handling`, `report_generator`, `computational_resources`,
  `performance_metrics`, `exception_handling`) and reference a
  `SimulationPlanner` that `plan_Simulation.py` does not define — see M-4.

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

## Major — open / deferred

- **M-4 — `2_OPERATE` plan→execute→render pipeline references non-existent
  modules; **CLOSED 2026-08-02**.** The pipeline was rebuilt and wired to the
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
    runs, and the support modules. Full suite: 31 passed; compile-sweep and
    ruff (new files) clean. ✓ (fix: rebuild 2_OPERATE pipeline on active_infer_ants)
