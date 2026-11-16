# FieldSHIFT-2

Domain-shifting dissertation framework for cross-disciplinary Active Inference analysis.

## Pipeline

| Stage | Script | Description |
|-------|--------|-------------|
| 1. Config | `config.py` | Domain definitions and parameters |
| 2. Shift | `shift_domains.py`, `generate_pro_shift_domains.py` | Domain shift mappings |
| 3. Generate | `dissertation_generator.py`, `dissertation_outline_generator.py` | Dissertation text/outline generation |
| 4. Explain | `dissertation_explainer.py` | Dissertation explanation module |
| 5. Improve | `dissertation_improver.py` | Iterative quality improvement |
| 6. Translate | `dissertation_translation.py` | 24-language translation |
| 7. Evaluate | `dissertation_entity_evaluation.py`, `dissertation_grant_evaluator.py` | Entity and grant evaluation |
| 8. Meta-analyze | `Meta_Analysis_Shifted_Dissertation.py`, `Meta_Analysis_Shifted_Dissertation_Outline.py` | Dissertation and outline meta-analysis |

## Data Structure

| Directory | Description |
|---|---|
| `Inputs_and_Outputs/` | Translated dissertations (24 langs), grant evaluations, shifted outputs |
| `FieldSHIFT-1/` | First-generation predecessor framework |
| `FieldSHIFT_Meta/` | Meta-analysis data |

## Languages (24)

Arabic, Bengali, Chinese-Mandarin, English, French, German, Hebrew, Hindi, Japanese, Javanese, Korean, Navajo, Portuguese, Punjabi, Russian, Sami, Sanskrit, Spanish, Telugu, Vietnamese, and more.

## Existing-output preservation

Artifact-writing callables preserve an existing destination before
artifact-specific input/provider/computation work, including empty existing
files. Complete batches skip generation; partial batches retain existing
artifacts and produce eligible missing companions. Both dissertation and
outline meta-analysis modules are covered.

This is not credential-free/import-free script execution or scientific-runtime
qualification. Normal imports/entrypoints retain existing optional-library,
configuration/key-file and NLTK initialization requirements. Use only an
explicitly authorized research runtime for generation.

## References

See `FieldSHIFT-2.md` for the complete framework documentation.

## Related

- Parent: [Research](../README.md)
