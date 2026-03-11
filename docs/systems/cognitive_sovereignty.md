# Cognitive Sovereignty

3-stage autonomous cognition simulation pipeline.

## Location

`0_CONTEXT/Systems/Cognitive_Sovereignty/`

## Pipeline

```
1_generate_entity_library.py → 2_cognitive_sovereignty_simulation.py → 3_simulation_analysis.py
```

| Stage | Script | Purpose |
|-------|--------|---------|
| 1 | `1_generate_entity_library.py` | Generate entity library from sys.argv inputs |
| 2 | `2_cognitive_sovereignty_simulation.py` | Run cognitive sovereignty simulation |
| 3 | `3_simulation_analysis.py` | JSON-based analysis of simulation results |
| — | `main.py` | Subprocess orchestrator for all 3 stages |
| — | `utils_cognitive_sovereignty.py` | NumPy-based utility functions |

## Concept

Cognitive sovereignty is the principle that agents should maintain autonomous control over their own belief-updating processes. The simulation tests resilience to external belief manipulation.
