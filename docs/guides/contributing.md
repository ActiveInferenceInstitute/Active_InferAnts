# Contributing

Contribution guidelines for the Active InferAnts framework.

## Set up a GitHub contribution in Cursor

Install Git, Cursor, the Python extension for Cursor, and [uv](https://docs.astral.sh/uv/getting-started/installation/). Use a Bash terminal on macOS, Linux, or WSL for the repository's shell commands.

1. Fork [ActiveInferenceInstitute/Active_InferAnts](https://github.com/ActiveInferenceInstitute/Active_InferAnts) on GitHub. Replace `YOUR-GITHUB-USERNAME` with the owner of your fork, then clone it and create a branch.

   ```bash
   git clone https://github.com/YOUR-GITHUB-USERNAME/Active_InferAnts.git
   cd Active_InferAnts
   git remote add upstream https://github.com/ActiveInferenceInstitute/Active_InferAnts.git
   git switch -c docs/my-first-change
   UV_PYTHON=3.12 ./run.sh setup
   ```

2. Open the repository folder in Cursor. From the Command Palette, run `Python: Select Interpreter` and choose `.venv/bin/python` from that folder. The locked setup installs the project's development dependencies in that environment. [Cursor Python setup](https://cursor.com/for/python)

3. Run a small simulation and the fast tests from the repository root. The simulation prints `5` when it completes.

   ```bash
   .venv/bin/python -c 'from active_infer_ants import InferenceModel; print(InferenceModel(seed=1).run(max_iterations=5)["max_iterations"])'
   ./run.sh test-fast
   ```

4. Make the change, review it with `git diff`, and follow the checklist below. Push your branch to `origin`, then open a GitHub pull request from your fork against `ActiveInferenceInstitute/Active_InferAnts:main`. The [run guide](../RUN_GUIDE.md) explains the full gate and its pinned GNN parser.

## Code Standards

- All Python modules must include docstrings and type hints
- Use `logging` module (not `print`) for output
- Follow the existing module patterns in each phase directory
- Maintain A/B/C/D matrix conventions across all implementations

## Documentation Requirements

Every directory must have three documentation files:

| File | Purpose |
|------|---------|
| `AGENTS.md` | Agent coding guidance — directory path, purpose, contents listing, instructions |
| `README.md` | User-facing documentation — overview, modules table, usage |
| `SPEC.md` | Technical specification — interfaces, dependencies, constraints |

## File Listing Format

Use emoji icons in AGENTS.md directory listings:
- `📁` for directories (with trailing `/`)
- `📄` for files
- Include brief descriptions after em-dash (`—`)

## Pull Request Checklist

- [ ] `./run.sh gate` passes locally (lint, test-fast, docs, gnn — the same arms CI runs)
- [ ] New behavior has a focused test; never weaken a test to make it pass
- [ ] All 3 documentation files present for any new directories
- [ ] AGENTS.md listings match actual directory contents
- [ ] Python modules have docstrings and type hints
- [ ] `run.sh` scripts are executable and tested
- [ ] No phase-specific dependencies in shared modules
- [ ] Generated pages refreshed (`python scripts/docgen/doc_index.py --write`, `./run.sh metrics`), never hand-edited

## License

All contributions are under CC BY-NC-ND 4.0.
