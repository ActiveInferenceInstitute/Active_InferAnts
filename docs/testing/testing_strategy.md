# Testing Strategy

Testing approach for the Active InferAnts framework.

## The gate

Every check runs through `./run.sh`, the single entry point documented in
[`../RUN_GUIDE.md`](../RUN_GUIDE.md). Each arm is the exact command CI runs:

```bash
./run.sh lint        # ruff on the maintained surface + compile sweep
./run.sh test-fast   # pytest -m "not gnn"
./run.sh test-full   # pytest (adds the gnn-marked conformance module)
./run.sh docs        # mkdocs --strict, relative links, generated pages
./run.sh gnn         # pinned GNN parser + specification conformance
./run.sh gate        # lint, test-fast, docs, gnn
```

`test-fast` and `gnn` partition the suite by the `gnn` marker, so `gate` covers
`test-full` without repeating a test. Measured wall times and per-selection
counts: [`../_generated/gate_metrics.md`](../_generated/gate_metrics.md).

## Test Levels

| Level | Scope | Tools |
|-------|-------|-------|
| **Unit** | Individual functions, matrix operations | pytest |
| **Integration** | Module interactions, pipeline phases | pytest + fixtures |
| **Cross-language** | Registered language implementations | `test_suite.py`, `benchmark_suite.py` |
| **System** | Full pipeline end-to-end | Shell scripts |
| **Security** | Vault, encryption, hashing | `1_PREPARE/Utils/` test modules |

## Cross-Language Testing

```bash
cd 0_CONTEXT/Computer_Languages
python3 test_suite.py          # Run all language tests
python3 benchmark_suite.py     # Performance benchmarks
```

## Augmented Active Inference Tests

```
0_CONTEXT/Systems/Augmented_Active_Inference/tests/
```

## Mathematical Verification

- Functor law compliance for `PolyFunctor` implementations
- Matrix normalization checks for A/B/C/D
- Entropy bounds for belief distributions
- Expected free energy sign conventions
