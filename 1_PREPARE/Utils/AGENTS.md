# AGENTS.md — Utilities

> Agent guidance for the `1_PREPARE/Utils` directory within the Active InferAnts framework.

## Purpose

Security, compression, hashing, and general-purpose utility modules. Provides the cryptographic and data-handling infrastructure for the framework.

## Directory Contents

- 📄 `compression.py` — Data compression utilities
- 📄 `encryption.py` — Encryption/decryption operations
- 📄 `hashing.py` — Cryptographic hash functions
- 📄 `quantum_security.py` — Post-quantum cryptographic primitives
- 📄 `security_base.py` — Base security classes and interfaces
- 📄 `security_mesh.py` — Distributed security mesh networking
- 📄 `security_monitor.py` — Real-time security monitoring and alerting
- 📄 `security_orchestrator.py` — Security policy orchestration
- 📄 `vault_adapter.py` — Secrets management vault integration

## Agent Instructions

- Maintain cryptographic algorithm correctness and security best practices.
- Ensure `security_base.py` abstract interfaces are implemented by all concrete security modules.
- Preserve the security orchestrator → monitor → mesh layered architecture.
- Track upstream cryptographic library versions for vulnerability patches.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Maintain consistency with parent and sibling directory conventions.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Directory structure reflects current organization
- [ ] Cross-references to related directories verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
