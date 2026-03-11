# AGENTS.md — William Blake Analysis

> Agent guidance for the `0_CONTEXT/Systems/William_Blake` directory.

## Purpose

Literary and philosophical analysis of William Blake's works through Active Inference epistemology. Combines NLP entity extraction with Active Inference modeling of Blake's visionary system.

## Directory Contents

- 📁 `Analysis/` — Analysis output directory
- 📄 `Blake_Analysis.py` — Main analysis pipeline
- 📄 `Blake_Entity.json` — Entity extraction data
- 📄 `Blake_Entity_Extraction_Simple.py` — Simple entity extraction
- 📄 `Blake_Entity_Extraction_Spacy.py` — SpaCy-based NLP entity extraction
- 📄 `Blake_Mentions.py` — Mention tracking and analysis
- 📄 `Blake_Zed.py` — Zed-model integration
- 📁 `Outputs/` — Generated outputs
- 📁 `William_Blake_Resources/` — Source texts and reference materials

## Agent Instructions

- Maintain NLP pipeline compatibility (Simple and SpaCy extractors).
- Ensure `Blake_Entity.json` is generated from, not manually created for, the extraction scripts.
- Track source text provenance in `William_Blake_Resources/`.
- Follow the repository's CC BY-NC-ND 4.0 license.
- Keep all documentation synchronized with actual contents.

## Quality Checklist

- [ ] All files documented and up-to-date
- [ ] Entity extraction pipeline (Simple + SpaCy) verified
- [ ] README.md and SPEC.md synchronized with this AGENTS.md
