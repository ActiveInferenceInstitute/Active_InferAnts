# Tutorial: Grant Generation

Using the automated grant proposal pipeline.

## Overview

The grant generation pipeline at `1_PREPARE/Methods/Grant_Methods_1/` produces entity-specific grant proposals using catechism-based structured interviews.

## Pipeline Flow

```
1. Select Entity (researcher profile)
2. Select Funding Agency (DARPA, NSF, NIH, etc.)
3. Load Catechism (structured questions for agency)
4. Generate Proposal (entity answers × catechism structure)
5. Evaluate (scoring and feedback)
```

## Entities Available (17)

AIME, Active Inference Institute, Albarracin, Clippinger, Fields, Friston, Fuller, Gordon, Hipolito, Levin, Mobus, Ramstead, Synthetic Art/Entomology/Math/Philosophy, Systems 2024

## Funding Agencies (8)

DARPA, FLI, IARPA, NIH, NIST, NSF, SAM.gov, Templeton

## Using FieldSHIFT-2

For domain-shifting dissertations, use the pipeline at `1_PREPARE/Methods/Research/FieldSHIFT-2/`:

```bash
cd 1_PREPARE/Methods/Research/FieldSHIFT-2

# Configure domains
python3 config.py

# Generate shift mappings
python3 shift_domains.py

# Generate dissertation
python3 dissertation_generator.py

# Translate to 24 languages
python3 dissertation_translation.py

# Evaluate
python3 dissertation_entity_evaluation.py
python3 dissertation_grant_evaluator.py
```
