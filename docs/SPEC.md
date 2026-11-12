# SPEC.md — Documentation Hub

> Technical specification for the `docs` directory.

## Overview

Modular documentation organized into ten topic sections plus the hub
(`README.md`), the site home (`index.md`), the run guide (`RUN_GUIDE.md`), and
generated pages. Live counts are in [`documentation-index.md`](documentation-index.md),
generated from the tree by `scripts/docgen/doc_index.py`; do not restate them here.

## Structure

| Path | Focus |
|-----------|-------|
| `architecture/` | Pipeline, components, data flow, generative model, integrations |
| `api/` | Knowledge API, MetaInformAnt API, data models |
| `concepts/` | Active Inference theory, agent taxonomy, category theory |
| `guides/` | Getting started, language addition, simulations, research, contributing |
| `operations/` | Simulation ops, API deployment, monitoring, logging, governance |
| `reference/` | Configuration, language matrix, systems, glossary, dependencies |
| `security/` | Architecture, cryptographic primitives |
| `systems/` | P3IF, Cognitive Sovereignty, IC2S2, William Blake, Active Data Sampling, Meta |
| `testing/` | Strategy, cross-language, verification methods |
| `tutorials/` | First agent, pipeline, analysis, systems, grants, benchmarking |
| `documentation-index.md` | Generated flat index of every document |
| `RUN_GUIDE.md` | The `./run.sh` arms, the lint surface, and where CI runs each arm |
| `_generated/` | Generated facts and receipts (gate metrics, frozen baseline) |

## Conventions

- GitHub-flavored Markdown
- Tables for structured data
- Code blocks with language syntax highlighting
- Relative links for cross-referencing within `docs/`; absolute repository URLs
  for targets outside it (the MkDocs build cannot resolve those)
- Generated pages carry a "do not edit by hand" note and a `--write` command
- `./run.sh docs` is the check: `mkdocs build --strict`, relative links, and
  generated-file freshness
