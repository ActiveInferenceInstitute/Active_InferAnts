# AGENTS.md — External Interfaces & APIs

> Agent guidance for the `6_API` directory within the Active InferAnts framework.

## Purpose

REST APIs, knowledge management services, and external interfaces. This phase exposes Active Inference capabilities to external consumers.

## Directory Contents

- 📄 `Knowledge_API.py` — FastAPI knowledge service with multi-database backend (PostgreSQL, MongoDB, Redis, Neo4j, Elasticsearch)
- 📄 `MetaInformAnt_API.py` — FastAPI meta-information service with process tracking and agent management

## Agent Instructions

- Maintain FastAPI endpoint contracts and pydantic model schemas.
- Ensure API key authentication is enforced on all mutating endpoints.
- Preserve multi-database synchronization logic in `Knowledge_API.py`.
- Keep OpenAPI/Swagger documentation auto-generation working.
- Track breaking API changes and version accordingly.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Maintain consistency with parent and sibling directory conventions.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Directory structure reflects current organization
- [ ] Cross-references to related directories verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
