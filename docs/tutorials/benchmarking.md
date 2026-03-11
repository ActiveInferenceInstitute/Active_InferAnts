# Tutorial: Cross-Language Benchmarking

Running and interpreting the benchmark suite across 40 language implementations.

## Running Benchmarks

```bash
cd 0_CONTEXT/Computer_Languages

# Run the full benchmark suite
python3 benchmark_suite.py

# Run all implementations
./run_all.sh

# Check status
./status_dashboard.sh
```

## Benchmark Metrics

| Metric | Description |
|--------|-------------|
| Execution time | Wall-clock time for complete inference loop |
| Memory usage | Peak RSS during execution |
| Numerical accuracy | Agreement with Python reference implementation |
| Convergence speed | Iterations to reach belief equilibrium |

## Interpreting Results

- Results aggregated in `test_results/`
- Visual scorecard in `scorecard.png`
- Detailed reports via `reporting_system.py`

## Configuration

Use `config_manager.py` for cross-language configuration:

```bash
python3 config_manager.py --set max_iterations=500
```
