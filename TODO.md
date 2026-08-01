# TODO.md — Active InferAnts

> Project backlog / taskboard. Severity convention: **Major / Medium / Minor**.

**Owner:** Daniel Ari Friedman (Active Inference Institute)
**Status:** Active / Maintained
**Last reviewed:** 2026-08-01 (fix-and-push pass; red-team review completed, fixes implemented)

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

## Major — open / deferred

- **M-4 — `2_OPERATE` plan→execute→render pipeline references non-existent
  modules; deferred.**
  Affected: `2_OPERATE/plan_Simulation.py`, `2_OPERATE/execute_Simulation.py`,
  `2_OPERATE/render_Simulation.py`.
  Why it matters: `execute_Simulation.py` imports
  `from plan_Simulation import SimulationPlanner` (the file defines
  `SimulationSetup`), and both files import ~8 modules
  (`MetaInformAnt_Simulation`, `data_logging`, `performance_monitor`,
  `error_handling`, `report_generator`, `computational_resources`,
  `performance_metrics`, `exception_handling`, `config`, `metaconfig`) that do
  not exist anywhere in the tree; `plan_Simulation.py` also draws an unseeded
  seed. Suggested fix: build those modules and reconcile the class/renderer
  contracts (or wire the pipeline to the now-realisable `active_infer_ants`
  simulation API), add a seed, then add an integration test. Deferred because
  this is a large, untestable-here scaffolding build and fabricating
  non-existent modules without a test gate was judged worse than deferring.
