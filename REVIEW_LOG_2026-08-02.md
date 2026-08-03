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

## Implementation plan

- Replace missing MkDocs section indexes with the existing section README files.
- Repair all broken internal documentation links found by the repository-wide scan.
- Correct language/count/configuration/API/tooling claims against source and manifests.
- Clarify deferred simulation-pipeline status and provide a verified package/API quickstart.
- Re-run link, anchor, documentation build, Ruff, compile, and pytest checks; commit logical documentation changes and push `main`.
