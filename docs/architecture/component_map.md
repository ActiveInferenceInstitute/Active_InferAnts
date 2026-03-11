# Component Map

Directory-to-module mapping for the Active InferAnts framework.

## Core Pipeline

```
activeinferants/
├── 0_CONTEXT/                    # Foundation Layer
│   ├── Computer_Languages/       # 40 language implementations
│   │   ├── Python/              # Reference implementation
│   │   ├── Rust/                # Systems-level implementation
│   │   ├── Julia/               # Scientific computing (RxInfer)
│   │   └── ... (37 more)
│   ├── Systems/                 # Specialized systems
│   │   ├── Active_Inference/    # Core PyMDP utilities
│   │   ├── P3IF/               # Privacy/Policy/Procedure framework
│   │   ├── Cognitive_Sovereignty/  # 3-stage simulation pipeline
│   │   ├── William_Blake/       # NLP entity extraction
│   │   ├── BOLTS/              # 5-dimensional org analysis
│   │   └── IC2S2/              # Computational social science
│   └── specs_and_prompts/       # System specs v1-v3
├── 1_PREPARE/                    # Preparation Layer
│   ├── Things/                  # Agent classes (ActiveNestmate, Thing)
│   ├── General/                 # Shared modules (CogSec, Crypto, etc.)
│   ├── Utils/                   # Security infrastructure
│   ├── Methods/                 # Research & grant methods
│   └── configs/                 # Configuration files
├── 2_OPERATE/                    # Execution Layer
├── 3_MEASURE/                    # Analysis Layer
├── 4_REPORT/                     # Reporting Layer
├── 5_FOLLOWUP/                   # Continuous Improvement
├── 6_API/                        # External Interfaces
└── 9_OTHER/                      # Third-Party Integrations
    ├── Kafka/                   # Event streaming
    ├── Nostr/                   # Decentralized protocol
    ├── HoloChain/              # Distributed ledger
    ├── FOIA/                   # Government transparency
    └── TheBrain/               # Knowledge graphs
```

## Module Count by Phase

| Phase | Python Modules | Subdirectories |
|-------|---------------|----------------|
| 0_CONTEXT | ~80 | 52 |
| 1_PREPARE | ~30 | 15 |
| 2_OPERATE | 5 | 0 |
| 3_MEASURE | 5 | 0 |
| 4_REPORT | 2 | 0 |
| 5_FOLLOWUP | 2 | 0 |
| 6_API | 2 | 0 |
| 9_OTHER | ~20 | 30+ |
