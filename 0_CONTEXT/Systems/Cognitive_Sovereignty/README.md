# Cognitive Sovereignty

Cognitive sovereignty research exploring autonomous cognition and self-determination through Active Inference.

## Pipeline

| Stage | Script | Description |
|-------|--------|-------------|
| 1 | `1_generate_entity_library.py` | Generate entity profiles for simulation |
| 2 | `2_cognitive_sovereignty_simulation.py` | Run cognitive sovereignty simulations |
| 3 | `3_simulation_analysis.py` | Analyze simulation outcomes |

## Usage

```bash
python3 main.py                               # Run full pipeline
python3 1_generate_entity_library.py          # Stage 1 only
python3 2_cognitive_sovereignty_simulation.py  # Stage 2 only
python3 3_simulation_analysis.py              # Stage 3 only
```

## Configuration

Parameters in `config.json` control simulation behavior:
- Entity generation parameters
- Simulation duration and precision
- Analysis metrics

## Related

- Parent: [Systems](../README.md)
