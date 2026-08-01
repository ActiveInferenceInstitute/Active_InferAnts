# Testing Strategy

Testing approach for the Active InferAnts framework.

## Test Levels

| Level | Scope | Tools |
|-------|-------|-------|
| **Unit** | Individual functions, matrix operations | pytest |
| **Integration** | Module interactions, pipeline phases | pytest + fixtures |
| **Cross-language** | 50 language implementations | `test_suite.py`, `benchmark_suite.py` |
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
