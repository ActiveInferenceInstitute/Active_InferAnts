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
| `config.py` | Module-shaped planner defaults, separate from root `config.json` |
| `metaconfig.py` | Meta-level configuration (parameter ranges, defaults) |
| `meta_metaconfig.py` | Meta-meta configuration (configuration of the configuration) |
| `security_policy.py` | Security-related configuration |

## SimulationExecutor Parameters

These are Python constructor arguments, not command-line flags.

- `visualization_interval: int | None = 100` — optional per-agent visualization
  interval; `None` disables that path. The renderer still refreshes each step.
- `pause_duration: float = 0.1` — pause between steps, in seconds.
- `log_level: int = logging.INFO` — executor logging level.
- `output_dir: str = "simulation_output"` — local logging/final-report directory.
- `max_steps: int | None = None` — optional limit forwarded to the planner.

`visualization_frequency`, `sleep_duration`, and `max_iterations` are not
constructor keywords. Required initialization, step, rendering, report-write
and cleanup failures propagate; optional per-agent visualization remains
nonfatal. The executor closes its owned renderer during cleanup.
The configuration table above is an inventory, not an implicit translation
pipeline; see [planner selection](../reference/configuration.md#2_operate-planner-selection).

