# Multi-Language Design Philosophy

Why Active InferAnts implements Active Inference in 40 programming languages.

## Design Goals

1. **Universality verification** — If Active Inference is truly universal, it should be expressible in any computational paradigm
2. **Cross-paradigm insights** — Each language reveals different aspects of the algorithm
3. **Community accessibility** — Researchers can engage using their preferred language
4. **Formal correspondence** — Mapping between language features and mathematical structures

## Language Paradigm Coverage

| Paradigm | Languages | Insight |
|----------|-----------|---------|
| **Functional** | Haskell, OCaml, Elixir, Clojure, Racket, F# | Belief updating as function composition |
| **Systems** | C, C++, Rust, Zig, Nim | Memory layout of generative models |
| **Scientific** | Python, Julia, R, MATLAB, Fortran | Numerical stability of matrix operations |
| **Logic** | Prolog | Inference as logical resolution |
| **Concurrent** | Erlang, Elixir, Go | Multi-agent as concurrent processes |
| **OOP** | Java, C#, Kotlin, Swift | Agent hierarchy as class hierarchy |
| **JVM** | Java, Kotlin, Scala, Clojure | Cross-language interop on single VM |
| **Scripting** | Python, Ruby, Perl, PHP, Lua, Shell | Rapid prototyping |
| **Esoteric** | Brainfuck, Jock | Computational minimalism |

## Shared Contract

All implementations must provide:
- A/B/C/D matrix initialization
- Bayesian belief updating
- Expected free energy computation
- Action selection loop

## Orchestration

| Script | Purpose |
|--------|---------|
| `run_all.sh` | Sequential execution of all 40 implementations |
| `master_controller.py` | Python-based orchestration |
| `benchmark_suite.py` | Cross-language performance benchmarking |
| `test_suite.py` | Cross-language correctness tests |
| `config_manager.py` | Shared configuration |
| `reporting_system.py` | Cross-language result aggregation |
