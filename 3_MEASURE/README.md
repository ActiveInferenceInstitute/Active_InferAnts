# Analysis & Measurement

Analysis, statistics, categorization, and performance measurement. This phase quantifies and evaluates the outputs of Active Inference operations.

## Modules

| Module | Description |
|---|---|
| `categorization.py` | `CategoryTheoryAnalyzer` class — graph-based categorization with NetworkX, morphism tracking, and functor composition |
| `poly_functor.py` | `PolyFunctor` generic class — 6 polynomial functor types (Tuple2, Tuple3, List, Maybe, Either, Tree) with `hmap` operations |
| `specify_measure.py` | `MeasurementMethod` enum + `QRFParameters` dataclass — Quantum Reference Frame measurement specs with JSON serialization |
| `statistics.py` | `SimulationSummary` class — pandas/seaborn-based statistical analysis, hypothesis testing, and visualization |
| `summarize.py` | `SimulationEntity` class — entropy-based automated summarization with pandas DataFrames |

## Pipeline Position

```
2_OPERATE → [3_MEASURE] → 4_REPORT
```

- **Input**: Simulation traces and behavioral data from `2_OPERATE`
- **Output**: Statistical summaries, categorized results, and metrics for `4_REPORT`

## Related

- Parent: [Active InferAnts](../README.md)
- Previous phase: [2_OPERATE](../2_OPERATE/README.md)
- Next phase: [4_REPORT](../4_REPORT/README.md)
