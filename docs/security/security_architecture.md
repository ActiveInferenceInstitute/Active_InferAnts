# Security Architecture

Layered security infrastructure in `1_PREPARE/Utils/`.

## Security Stack

```
┌─────────────────────────────┐
│   security_orchestrator.py   │  Policy orchestration
├─────────────────────────────┤
│   security_monitor.py        │  Real-time monitoring & alerting
├─────────────────────────────┤
│   security_mesh.py           │  Distributed security mesh
├─────────────────────────────┤
│   security_base.py           │  Abstract interfaces
├─────────────────────────────┤
│   quantum_security.py        │  Post-quantum cryptographic primitives
├─────────────────────────────┤
│   vault_adapter.py           │  Secrets management integration
├─────────────────────────────┤
│   encryption.py / hashing.py │  Core cryptographic operations
│   compression.py             │  Data compression
└─────────────────────────────┘
```

## Cognitive Security

`1_PREPARE/General/CogSec.py` provides cognitive security using `ActiveNestmate`/`ActiveColony` agent types for adversarial simulation.

## API Security

`6_API/Knowledge_API.py` enforces:
- API Key authentication (`X-API-Key` header)
- CORS middleware
- Input validation via Pydantic models
