# SPEC.md — FieldSHIFT-2

> Technical specification for `1_PREPARE/Methods/Research/FieldSHIFT-2` within the Active InferAnts framework.

## Overview

Domain-shifting dissertation framework that translates research across disciplinary boundaries using Active Inference.

## Structure

- 📁 `FieldSHIFT-1/`
- 📁 `FieldSHIFT_Meta/`
- 📁 `IN_PROGRESS/`
- 📁 `Inputs_and_Outputs/`
- 📄 `AGENTS.md`
- 📄 `FieldSHIFT-2.md`
- 📄 `FieldSHIFT-2_Visualization.txt`
- 📄 `Meta_Analysis_Shifted_Dissertation.py`
- 📄 `Meta_Analysis_Shifted_Dissertation_Outline.py`
- 📄 `README.md`
- 📄 `config.py`
- 📄 `dissertation_entity_evaluation.py`
- 📄 `dissertation_explainer.py`
- 📄 `dissertation_generator.py`
- 📄 `dissertation_grant_evaluator.py`
- 📄 `dissertation_improver.py`
- 📄 `dissertation_outline_generator.py`
- 📄 `dissertation_translation.py`
- 📄 `generate_pro_shift_domains.py`
- 📄 `shift_domains.py`
- 📄 `utils.py`

## Writer contract

The shared text writer is `save_file(content, full_path)`: two arguments,
caller-owned serialization and verbatim UTF-8 text, with no implicit
directory/filename overload. Structured linguistic results are explicitly
JSON-serialized before saving. Existing outputs, including empty files, are
preserved rather than resumed, repaired or silently overwritten.

Multi-artifact methods guard complete groups and individual companions.
Existing PCA/projection/JSON companions do not suppress eligible missing
outputs. Scientific parameters, feature definitions, input filters, filename
conventions and historical tuple serialization are unchanged.

## Version

- **Framework**: Active InferAnts
- **License**: CC BY-NC-ND 4.0
