# AGENTS.md — Computer Languages

> Agent guidance for the `0_CONTEXT/Computer_Languages` directory within the Active InferAnts framework.

## Purpose

Multi-language Active Inference implementations across 50 programming languages. Each subdirectory contains a complete Active Inference implementation in the respective language.

## Directory Contents

### Language Implementations (50 directories)

- 📁 `Ada/` — Safety-critical systems
- 📁 `Assembly/` — Low-level machine code
- 📁 `Brainfuck/` — Esoteric minimalist
- 📁 `C/` — Systems-level performance
- 📁 `COBOL/` — Enterprise legacy
- 📁 `CommonLisp/` — Historical AI language
- 📁 `Cpp/` — High-performance C++
- 📁 `Crystal/` — Ruby-like compiled
- 📁 `CSharp/` — .NET ecosystem
- 📁 `D/` — Systems metaprogramming
- 📁 `Dart/` — Flutter/Google ecosystem
- 📁 `Elixir/` — Concurrent (BEAM VM)
- 📁 `Erlang/` — Distributed (BEAM VM)
- 📁 `FSharp/` — Functional-first .NET
- 📁 `Fortran/` — Scientific computing
- 📁 `Golang/` — Concurrent, statically-typed
- 📁 `Groovy/` — JVM scripting
- 📁 `Haskell/` — Purely functional
- 📁 `Java/` — Enterprise JVM
- 📁 `JavaScript/` — Browser/Node.js
- 📁 `Jock/` — Experimental
- 📁 `Julia/` — Scientific computing
- 📁 `Kotlin/` — Modern JVM
- 📁 `Lua/` — Lightweight embeddable
- 📁 `MATLAB/` — Numerical computing
- 📁 `Nim/` — Efficient compiled
- 📁 `ObjectiveC/` — Apple legacy
- 📁 `OCaml/` — Strongly-typed functional
- 📁 `Odin/` — Systems programming
- 📁 `Pascal/` — Structured programming
- 📁 `Perl/` — Text processing
- 📁 `PHP/` — Server-side scripting
- 📁 `PowerShell/` — Windows/cross-platform automation
- 📁 `Prolog/` — Logic programming
- 📁 `Python/` — Primary reference implementation
- 📁 `R/` — Statistical computing
- 📁 `Racket/` — Lisp-family
- 📁 `Ruby/` — Dynamic, expressive
- 📁 `Rust/` — Memory-safe systems
- 📁 `Scala/` — Functional/OO hybrid (JVM)
- 📁 `Scheme/` — SICP heritage functional
- 📁 `Shell/` — Unix scripting
- 📁 `Solidity/` — Blockchain smart contracts
- 📁 `SQL/` — Declarative database
- 📁 `Swift/` — Apple ecosystem
- 📁 `Tcl/` — Extensible scripting
- 📁 `TypeScript/` — Type-safe JavaScript
- 📁 `V/` — Simple, fast compiled
- 📁 `Zig/` — Low-level systems
- 📁 `Clojure/` — Functional Lisp (JVM)

### Orchestration & Infrastructure

- 📄 `languages.json` — Canonical language registry (single source of truth)
- 📄 `setup_dependencies.sh` — Consolidated dependency installer (--check/--list/--install)
- 📄 `master_controller.py` — Central cross-language orchestration
- 📄 `run_all.sh` — Shell-based multi-language runner
- 📄 `test_suite.py` — Comprehensive testing framework
- 📄 `benchmark_suite.py` — Cross-language performance benchmarking
- 📄 `config_manager.py` — Dependency and configuration management
- 📄 `reporting_system.py` — Test and benchmark report generation
- 📄 `status_dashboard.sh` — Interactive status dashboard
- 📄 `dependency_report.txt` — Current dependency status
- 📁 `test_results/` — Test output directory

### Documentation

- 📄 `README.md` — Multi-language overview and CLI usage
- 📄 `SPEC.md` — Technical specification
- 📄 `AGENTS.md` — This file

## Agent Instructions

- Maintain algorithmic parity across all language implementations.
- Use Python as the reference implementation for correctness validation.
- Ensure `master_controller.py` can orchestrate all language implementations.
- Document language-specific build prerequisites in each language README.
- Track test results and benchmark performance across languages.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Maintain consistency with parent and sibling directory conventions.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Directory structure reflects current organization
- [ ] Cross-references to related directories verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
