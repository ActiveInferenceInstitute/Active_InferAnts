# Logging Conventions

Standardized logging across the Active InferAnts framework.

## Convention

All modules use Python's standard `logging` module:

```python
import logging

class MyModule:
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        self.logger.info("Module initialized")
```

## Log Levels

| Level | Usage |
|-------|-------|
| `DEBUG` | Matrix dumps, per-step agent state, detailed computation |
| `INFO` | Phase transitions, analysis start/complete, export success |
| `WARNING` | Missing optional dependencies, fallback behavior |
| `ERROR` | Missing required data, computation failures |
| `CRITICAL` | Security violations, data corruption |

## Configured Modules

| Module | Logger Name |
|--------|-------------|
| `CognitiveUtilities` | `CognitiveUtilities` |
| `AgentVisualizer` | `root` |
| `SimulationExecutor` | `SimulationExecutor` |
| `FollowUpExecutor` | `FollowUpExecutor` |
| `ReportExecutor` | `ReportExecutor` |
| `SecurityMonitor` | `SecurityMonitor` |

## Configuration

Root-level via `config.json`:
```json
{"logging_level": "INFO"}
```

Programmatic (e.g., in `CognitiveUtilities`):
```python
cu.configure_logger(log_level='DEBUG', log_format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
```
