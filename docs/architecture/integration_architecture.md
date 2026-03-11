# Integration Architecture

Third-party integration patterns in the `9_OTHER/` directory.

## Integration Directory

| Integration | Protocol | Purpose |
|-------------|----------|---------|
| **Kafka** | Apache Kafka | Real-time streaming of Active Inference events |
| **Nostr** | Nostr (NIP) | Decentralized censorship-resistant communication |
| **HoloChain** | Holochain | Distributed agent coordination |
| **ActivityPub** | ActivityPub/W3C | Federated social networking |
| **Matterbridge** | Multi-protocol | Cross-platform chat bridging |
| **eBPF** | Extended BPF | Kernel-level observability |
| **BPMN** | ISO 19510 | Business process modeling |
| **Coda** | Coda API | Collaborative document platform |
| **GitHub** | GitHub REST/GraphQL | Repository management |
| **TheBrain** | TheBrain export | Knowledge graph mind-mapping |
| **FOIA** | HTTP/JSON | Government transparency data (18 agencies) |
| **Languages** | Various | Supplementary language resources |

## FOIA Coverage

18 federal agencies: DHS, DOC, DOD, DOE, DOI, DOJ, DOL, DOS, DOT, ED, EPA, HHS, HUD, OIP, SSA, TREASURY, USDA, VA

## Integration Pattern

Each integration follows a consistent structure:
```
9_OTHER/<integration>/
├── AGENTS.md       # Agent coding guidance
├── README.md       # User documentation
├── SPEC.md         # Technical specification
└── <source files>  # Integration code
```
