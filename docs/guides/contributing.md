# Contributing

Contribution guidelines for the Active InferAnts framework.

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
