# FieldSHIFT-2: Domain Shifting Framework

FieldSHIFT-2 contains research scripts for domain transformations,
dissertation/outline generation, evaluation, translation and analysis.
Real provider access and scientific-runtime qualification remain separate
from the existing-output preservation contract.

## Actual source layout

```text
FieldSHIFT-2/
├── config.py
├── utils.py
├── generate_pro_shift_domains.py
├── shift_domains.py
├── dissertation_outline_generator.py
├── dissertation_generator.py
├── dissertation_explainer.py
├── dissertation_improver.py
├── dissertation_translation.py
├── dissertation_entity_evaluation.py
├── dissertation_grant_evaluator.py
├── Meta_Analysis_Shifted_Dissertation.py
├── Meta_Analysis_Shifted_Dissertation_Outline.py
├── IN_PROGRESS/
│   ├── language_analysis.py
│   └── generate_pre_pro_shifted_grants.py
├── Inputs_and_Outputs/
├── FieldSHIFT_Meta/
└── FieldSHIFT-1/
```

There is no `src/core/FieldSHIFT-2.py` master CLI or central `--config`
orchestrator. The scripts are flat modules except for the two named
`IN_PROGRESS` consumers. `config.py` supplies Python configuration; each
caller's actual directory/full-path arguments control its output, rather than
an invented common dissertation or analysis destination.
Preserved artifacts under `Inputs_and_Outputs/`, `FieldSHIFT_Meta/` and the
predecessor tree are not rewritten to match an aspirational layout.

## Writers and execution boundary

`save_file(content, full_path)` writes caller-serialized UTF-8 text; it has no
implicit directory/filename overload. Existing destinations, including empty
files, are preserved before artifact-specific input/provider/computation work.
Complete groups skip; partial groups preserve existing companions while
eligible missing outputs remain independent. Both meta-analysis modules
participate in this contract.

`IN_PROGRESS/language_analysis.py` writes `analysis.json` and a conditional
PCA companion. Existing companions are preserved independently; nested
linguistic features are not silently flattened into a new scientific model.

Normal imports and entrypoints retain their optional-library, key/configuration
and NLTK prerequisites. Preservation controls are not credential-free execution,
provider integration or permission to generate research outputs. Grant-product
generation and all-folder language analysis remain separate owner decisions;
see [the original pending requests](IN_PROGRESS/FieldShift_TODO.md).

## References and maintenance

The [pipeline inventory](README.md) and [writer specification](SPEC.md) describe
the current local interfaces. The predecessor paper and its historical CSVs
remain historical evidence, not newly executed writer entrypoints.

Contribute through the repository's normal review process.
Contact <blanket@activeinference.institute>.
Repository license: CC BY-NC-ND 4.0.

