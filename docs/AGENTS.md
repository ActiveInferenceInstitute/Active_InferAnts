# AGENTS.md — Documentation Hub

> Agent guidance for the `docs` directory within the Active InferAnts framework.

## Purpose

Modular documentation for the Active InferAnts framework: ten topic sections,
the hub [`README.md`](README.md), the MkDocs home [`index.md`](index.md), the
gate guide [`RUN_GUIDE.md`](RUN_GUIDE.md), the generated
[`documentation-index.md`](documentation-index.md), and generated facts under
[`_generated/`](_generated/).

## Directory Contents

- 📁 `architecture/` — System design, pipeline flow, data flow, generative model
- 📁 `api/` — REST API reference, data models
- 📁 `concepts/` — Active Inference primer, agent types, category theory, BOLTS
- 📁 `guides/` — Getting started, adding a language, contributing
- 📁 `operations/` — Deployment, monitoring, logging, governance
- 📁 `reference/` — Configuration, language matrix, glossary, dependencies
- 📁 `security/` — Security architecture, cryptographic primitives
- 📁 `systems/` — P3IF, Cognitive Sovereignty, IC2S2, William Blake deep-dives
- 📁 `testing/` — Testing strategy, cross-language tests, verification
- 📁 `tutorials/` — First agent, pipeline, analysis, grant generation
- 📁 `_generated/` — generated gate metrics and the frozen pre-change baseline
- 📄 `README.md` — the hub (excluded from the MkDocs build, which uses `index.md`)
- 📄 `RUN_GUIDE.md` — the `./run.sh` arms and where CI runs each one
- 📄 `documentation-index.md` — generated flat index of every document
- 📄 `AGENTS.md`, `SPEC.md`, `index.md`

Each section keeps its own `README.md`, `AGENTS.md`, and `SPEC.md`.

## Agent Instructions

- Maintain documentation accuracy with the codebase; verify a command before documenting it.
- Never hand-write a number a script produces: link
  [`documentation-index.md`](documentation-index.md) or
  [`_generated/gate_metrics.md`](_generated/gate_metrics.md).
- Regenerate with `python scripts/docgen/doc_index.py --write` and
  `./run.sh metrics`; `./run.sh docs` fails when a generated page is stale.
- Keep links inside `docs/` relative; link files outside it with absolute
  repository URLs.
- Follow the repository's CC BY-NC-ND 4.0 license.

## Quality Checklist

- [ ] `./run.sh docs` passes (strict build, relative links, generated pages current)
- [ ] Generated pages regenerated, not edited
- [ ] Section `README.md` lists match the directory
