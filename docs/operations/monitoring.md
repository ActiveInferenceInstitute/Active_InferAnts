# Monitoring

System monitoring and observability infrastructure.

## Security Monitoring

`1_PREPARE/Utils/security_monitor.py` provides:
- Real-time security event detection
- Alert generation for anomalous behavior
- Integration with the security orchestrator

## Monitoring Stack

```
security_orchestrator.py
        │
        ▼
security_monitor.py ──alerts──▶ NotificationService
        │
        ▼
security_mesh.py ──events──▶ Logging
```

## Logging

All modules use Python's `logging` module with configurable levels:

```python
import logging
logger = logging.getLogger(__name__)
logger.info("Operation completed")
```

Configuration via `config.json`:
```json
{"logging_level": "INFO"}
```

## eBPF Integration

For kernel-level observability, see the eBPF integration at `9_OTHER/eBPF/`.
