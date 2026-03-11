# William Blake Analysis

NLP entity extraction from William Blake's literary works.

## Location

`0_CONTEXT/Systems/William_Blake/`

## Modules

| Module | Description |
|--------|-------------|
| `Blake_Analysis.py` | OS-based file analysis of Blake's texts |
| `Blake_Entity_Extraction_Simple.py` | Rule-based entity extraction (no dependencies) |
| `Blake_Entity_Extraction_Spacy.py` | SpaCy-powered NLP entity extraction |
| `Blake_Mentions.py` | Regex-based mention detection |
| `Blake_Zed.py` | Supplementary analysis module |

## Two Extraction Approaches

| Approach | Module | Dependencies | Speed | Accuracy |
|----------|--------|-------------|-------|----------|
| Simple | `*_Simple.py` | None (OS, re) | Fast | Lower |
| SpaCy | `*_Spacy.py` | SpaCy model | Slower | Higher |

## Data

Blake's literary texts stored alongside modules for analysis.
