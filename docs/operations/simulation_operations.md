# Simulation Operations

Running and managing Active Inference simulations at scale.

## Single Simulation

```bash
cd 2_OPERATE
python3 plan_Simulation.py && python3 execute_Simulation.py && python3 render_Simulation.py
```

## Configuration Hierarchy

```
config.json (root)
├── 1_PREPARE/configs/config.py
├── 1_PREPARE/configs/metaconfig.py
├── 1_PREPARE/configs/meta_metaconfig.py
└── 1_PREPARE/configs/security_policy.py
```

| Config | Purpose |
|--------|---------|
| `config.json` | Root simulation parameters (iterations, visualization, logging) |
| `config.py` | Python-accessible configuration wrapper |
| `metaconfig.py` | Meta-level configuration (parameter ranges, defaults) |
| `meta_metaconfig.py` | Meta-meta configuration (configuration of the configuration) |
| `security_policy.py` | Security-related configuration |

## SimulationExecutor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `visualization_frequency` | int | Steps between visual updates |
| `sleep_duration` | float | Pause between steps (seconds) |
| `max_iterations` | int | Maximum simulation steps |
