# AGENTS.md — Analysis & Measurement

> Agent guidance for the `3_MEASURE` directory within the Active InferAnts framework.

## Purpose

Analysis, statistics, categorization, and performance measurement. This phase quantifies and evaluates the outputs of Active Inference operations.

## Directory Contents

- 📄 `categorization.py` — `CategoryTheoryAnalyzer`: graph-based result categorization using NetworkX with morphism tracking and functor composition
- 📄 `poly_functor.py` — `PolyFunctor` generic class: polynomial functor abstractions (Tuple2, Tuple3, List, Maybe, Either, Tree functors with `hmap` operations)
- 📄 `specify_measure.py` — `MeasurementMethod` enum + `QRFParameters` dataclass: Quantum Reference Frame measurement specification with JSON serialization
- 📄 `statistics.py` — `SimulationSummary` class: pandas/seaborn-based statistical analysis, hypothesis testing, and visualization
- 📄 `summarize.py` — `SimulationEntity` class: entropy-based automated summarization with matplotlib/seaborn output

## Agent Instructions

- Maintain mathematical correctness in `CategoryTheoryAnalyzer` morphisms and composition.
- Ensure `specify_measure.py` enum types are consistent with measurement consumers in `4_REPORT`.
- Preserve the functor law compliance (identity + composition) in `poly_functor.py` implementations.
- Track schema consistency between `SimulationSummary` outputs and `ReportExecutor` inputs.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Functor law compliance verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
