# Cross-Language Tests

Testing the registered language implementations for correctness and consistency.

## Test Infrastructure

| Script | Purpose |
|--------|---------|
| `test_suite.py` | Correctness tests across all languages |
| `benchmark_suite.py` | Performance benchmarks |
| `run_all.sh` | Sequential execution of all implementations |
| `status_dashboard.sh` | Visual test status dashboard |

## Test Criteria

Each language implementation is verified for:

1. **Matrix initialization** — A/B/C/D have correct shapes and values
2. **Belief updating** — Posterior matches reference Python output within tolerance
3. **Action selection** — Selected action agrees with reference for identical inputs
4. **Convergence** — Beliefs converge to equilibrium within max iterations
5. **Exit code** — Process exits cleanly with code 0

## Results

Results stored in `0_CONTEXT/Computer_Languages/test_results/`.
