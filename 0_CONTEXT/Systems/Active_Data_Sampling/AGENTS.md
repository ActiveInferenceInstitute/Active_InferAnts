# AGENTS.md — Active Data Sampling

> Agent guidance for the `0_CONTEXT/Systems/Active_Data_Sampling` directory.

## Purpose

Active data sampling strategies using Active Inference for optimal experimental design and data collection. Implements methods for intelligently selecting data points to minimize uncertainty.

## Directory Contents

- 📄 `Analysis_ActiveDataSampling.py` — Analysis utilities for sampling experiments
- 📄 `Methods_ActiveDataSampling.py` — Core sampling methods and strategies
- 📁 `Outputs/` — Generated output data
- 📄 `Run_ActiveDataSampling.py` — Execution script for sampling experiments
- 📄 `Visualization_ActiveDataSampling.py` — Visualization of sampling results
- 📄 `log.txt` — Execution log

## Agent Instructions

- Maintain the Methods → Run → Analysis → Visualization pipeline flow.
- Ensure sampling methods correctly implement Active Inference exploration-exploitation trade-offs.
- Track output data provenance in the `Outputs/` directory.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Pipeline flow (Methods → Run → Analysis → Visualization) verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
