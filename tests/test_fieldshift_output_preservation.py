"""Actual FieldSHIFT entrypoint preservation with temporary text/JSON only.

Definitions are loaded without credential/config imports. Local producer
fixtures never contact a provider; they do not qualify research generation.
"""

import json
import time
from pathlib import Path
from types import SimpleNamespace

import pytest
from source_contract_helpers import FIELD, ForbiddenWork, load_definitions, seed_output


def utilities(**values):
    return load_definitions(FIELD / "utils.py", **values)


@pytest.mark.parametrize("content", [b"", b"archived\x00\xff\r\n"])
def test_shared_two_argument_writer_preserves_existing_bytes_before_work(
    tmp_path, content
):
    existing = seed_output(tmp_path, "output.md", content)
    work = ForbiddenWork()
    source = utilities(open=work)
    before = existing.stat().st_mtime_ns
    assert source["save_file"](object(), str(existing)) is None
    assert existing.read_bytes() == content
    assert existing.stat().st_mtime_ns == before
    assert work.calls == []


def test_shared_writer_writes_verbatim_utf8_and_propagates_io_errors(tmp_path):
    source = utilities()
    target = tmp_path / "new.md"
    text = "  café Ω\r\n\n"
    assert source["save_file"](text, str(target)) is None
    assert target.read_bytes() == text.encode("utf-8")
    blocked = tmp_path / "not-a-directory"
    blocked.write_text("blocked")
    with pytest.raises(OSError):
        source["save_file"]("new", str(blocked / "child.md"))
    assert blocked.read_text() == "blocked"


def test_entity_serializer_preserves_existing_and_supports_new_bare_filename(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    source = utilities()
    existing = seed_output(tmp_path, "entity.json")
    source["save_entity_library"]({"unsupported": object()}, str(existing))
    assert existing.read_bytes() == b"historical\x00\xff\r\n"
    library = {"entities": [{"name": "café", "allocation": 0.5}]}
    source["save_entity_library"](library, "new.json")
    assert (tmp_path / "new.json").read_text() == json.dumps(library, indent=2)


@pytest.mark.parametrize(
    "script",
    ["generate_pro_shift_domains.py", "IN_PROGRESS/generate_pre_pro_shifted_grants.py"],
)
def test_concatenation_preserves_ordered_pairs_and_exact_text(tmp_path, script):
    utility = utilities()
    source = load_definitions(
        FIELD / script, load_file=utility["load_file"], save_file=utility["save_file"]
    )
    first, second = tmp_path / "a.md", tmp_path / "b.md"
    first.write_text("alpha")
    second.write_text("beta")
    output = tmp_path / "output"
    preserved = seed_output(output, "concatenated_a_to_b.md")
    source["generate_concatenated_domains"](
        [str(first), str(second)], "PROMPT", str(output)
    )
    assert preserved.read_bytes() == b"historical\x00\xff\r\n"
    for left, right, a, b in [
        ("a", "a", "alpha", "alpha"),
        ("b", "a", "beta", "alpha"),
        ("b", "b", "beta", "beta"),
    ]:
        expected = f"\nPROMPT\n\nDOMAIN A:\n{a}\n\nDOMAIN B:\n{b}\n\nNow apply the Field Shift from Domain A to Domain B\n"
        assert (output / f"concatenated_{left}_to_{right}.md").read_text() == expected
    forbidden = ForbiddenWork()
    source["load_file"] = forbidden
    source["generate_pro_shift_domains"] = forbidden
    source["generate_concatenated_domains"](
        [str(first), str(second)], "unused", str(output)
    )
    assert forbidden.calls == []
    assert preserved.read_bytes() == b"historical\x00\xff\r\n"


@pytest.mark.parametrize(
    "script",
    ["generate_pro_shift_domains.py", "IN_PROGRESS/generate_pre_pro_shifted_grants.py"],
)
def test_complete_concatenation_caller_does_not_read_sources_or_prompt(
    tmp_path, script
):
    inputs = tmp_path / "Inputs_and_Outputs" / "Domain"
    inputs.mkdir(parents=True)
    (inputs / "a.md").touch()
    output = tmp_path / "Inputs_and_Outputs" / "Pro-Shifted_Domain"
    existing = seed_output(output, "concatenated_a_to_a.md")
    forbidden = ForbiddenWork()
    source = load_definitions(
        FIELD / script,
        SCRIPT_DIR=str(tmp_path),
        load_file=forbidden,
        save_file=forbidden,
    )
    source["process_domains"]({})
    assert forbidden.calls == []
    assert existing.read_bytes() == b"historical\x00\xff\r\n"


def test_direct_and_batch_domain_shift_skip_before_credentials_or_provider(tmp_path):
    inputs, outputs = tmp_path / "inputs", tmp_path / "outputs"
    inputs.mkdir()
    (inputs / "concatenated_a.md").touch()
    existing = seed_output(outputs, "shifted_a.md")
    forbidden = ForbiddenWork()
    api = SimpleNamespace(api_key="unchanged")
    source = load_definitions(
        FIELD / "shift_domains.py",
        load_file=forbidden,
        save_file=forbidden,
        generate_llm_response=forbidden,
        openai=api,
        time=time,
    )
    source["get_api_key"] = forbidden
    source["perform_domain_shift"](str(inputs / "concatenated_a.md"), str(outputs), {})
    source["process_domain_shift"](str(inputs), str(outputs), {})
    assert forbidden.calls == []
    assert api.api_key == "unchanged"
    assert existing.read_bytes() == b"historical\x00\xff\r\n"


def test_domain_shift_new_output_keeps_unpacked_response_bytes(tmp_path):
    utility = utilities()
    input_file = tmp_path / "concatenated_a.md"
    input_file.write_text("local input")
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    source = load_definitions(
        FIELD / "shift_domains.py",
        load_file=utility["load_file"],
        save_file=utility["save_file"],
        generate_llm_response=lambda *args: (" shifted café \n", 1.0),
        openai=SimpleNamespace(api_key=None),
    )
    source["perform_domain_shift"](str(input_file), str(outputs), {"api_key": None})
    assert (outputs / "shifted_a.md").read_bytes() == " shifted café \n".encode()


def test_utils_batch_skips_existing_inputs_and_only_generates_missing_outputs(tmp_path):
    inputs, outputs = tmp_path / "inputs", tmp_path / "outputs"
    inputs.mkdir()
    (inputs / "a.md").write_text("a")
    (inputs / "b.md").write_text("b")
    existing = seed_output(outputs, "shifted_a.md")
    calls = []
    source = utilities(
        generate_llm_response=lambda prompt, params: (
            calls.append(prompt) or "new β\n",
            0.1,
        )
    )
    source["process_pro_shifted_domains"](str(inputs), str(outputs), {})
    assert calls == ["Please shift the following pro-shifted domain:\n\nb"]
    assert existing.read_bytes() == b"historical\x00\xff\r\n"
    assert (outputs / "shifted_b.md").read_text() == "new β\n"
    forbidden = ForbiddenWork()
    source["open"] = forbidden
    source["generate_llm_response"] = forbidden
    source["process_pro_shifted_domains"](str(inputs), str(outputs), {})
    assert forbidden.calls == []


GUARDED = [
    (
        "dissertation_generator.py",
        "process_dissertation_writing",
        "Dissertation_Outline_fixture.md",
        "Written_Dissertation_Outline_fixture.md",
    ),
    (
        "dissertation_outline_generator.py",
        "process_dissertation_generation",
        "fixture.md",
        "Dissertation_Outline_fixture.md",
    ),
    (
        "dissertation_improver.py",
        "process_dissertation_improvement",
        "Written_Dissertation_Outline_fixture.md",
        "Improved_Written_Dissertation_Outline_fixture.md",
    ),
    (
        "dissertation_translation.py",
        "process_dissertation_translation",
        "fixture.md",
        None,
    ),
    (
        "dissertation_explainer.py",
        "process_dissertation_explanation",
        "fixture.md",
        None,
    ),
    (
        "dissertation_entity_evaluation.py",
        "process_dissertation_evaluation",
        "fixture.md",
        "Evaluated_by_owner/fixture_evaluated_by_owner.md",
    ),
    (
        "dissertation_grant_evaluator.py",
        "process_dissertation_evaluation",
        "fixture.md",
        "Evaluated_for_call/fixture_evaluated_for_call.md",
    ),
]


@pytest.mark.parametrize("script,function,input_name,target", GUARDED)
def test_every_already_guarded_dissertation_writer_preserves_all_variants(
    tmp_path, script, function, input_name, target
):
    inputs, outputs = tmp_path / "inputs", tmp_path / "outputs"
    inputs.mkdir()
    (inputs / input_name).touch()
    forbidden = ForbiddenWork()
    source = load_definitions(
        FIELD / script, load_file=forbidden, save_file=forbidden, time=time
    )
    if "translation" in script:
        targets = [
            f"{language}_Dissertations/Translated_fixture_{language}.md"
            for language in source["TARGET_LANGUAGES"]
        ]
    elif "explainer" in script:
        targets = [
            f"Explained_for_{audience}/Explained_fixture_{audience}.md"
            for audience in source["TARGET_AUDIENCES"]
        ]
    else:
        targets = [target]
    if "entity_evaluation" in script or "grant_evaluator" in script:
        script_root = tmp_path / "FieldSHIFT-2"
        script_root.mkdir()
        source["__file__"] = str(script_root / script)
        folder = (
            tmp_path
            / "Fonds"
            / ("Entity" if "entity_evaluation" in script else "Summarized_Grants")
        )
        folder.mkdir(parents=True)
        (
            folder / ("owner.py" if "entity_evaluation" in script else "call.md")
        ).write_text("Harmless descriptor fixture")
    seeded = [seed_output(outputs, path) for path in targets]
    source["open"] = forbidden
    source[function](str(inputs), str(outputs), {})
    assert forbidden.calls == []
    assert all(path.read_bytes() == b"historical\x00\xff\r\n" for path in seeded)


def language_source(**values):
    utility = utilities()
    values.setdefault("save_file", utility["save_file"])
    values.setdefault("load_file", utility["load_file"])
    return load_definitions(FIELD / "IN_PROGRESS/language_analysis.py", **values)


def test_existing_linguistic_companions_skip_before_input_or_pca(tmp_path):
    output = tmp_path / "output"
    json_path = seed_output(output, "analysis.json")
    pca_path = seed_output(output, "missing-input_pca.png")
    forbidden = ForbiddenWork()
    source = language_source(load_file=forbidden, PCA=forbidden, plt=forbidden)
    source["perform_linguistic_analysis"](str(tmp_path / "missing-input"), str(output))
    source["perform_pca_analysis"](forbidden, str(output), "missing-input")
    assert forbidden.calls == []
    assert json_path.read_bytes() == pca_path.read_bytes() == b"historical\x00\xff\r\n"


def test_linguistic_json_is_structured_and_preserves_existing_pca(tmp_path):
    inputs, outputs = tmp_path / "inputs", tmp_path / "outputs"
    inputs.mkdir()
    (inputs / "one.md").write_text("local text")
    existing = seed_output(outputs, "inputs_pca.png")
    forbidden = ForbiddenWork()
    source = language_source(
        DEFAULT_CONFIG={"analysis_params": {"linguistic_features": ["sentiment"]}},
        process_text=str.lower,
        calculate_sentiment=lambda text: {"compound": 0.25, "detail": "café"},
        PCA=forbidden,
        plt=forbidden,
    )
    source["perform_linguistic_analysis"](str(inputs), str(outputs))
    assert json.loads((outputs / "analysis.json").read_text()) == {
        "one.md": {"sentiment": {"compound": 0.25, "detail": "café"}}
    }
    assert existing.read_bytes() == b"historical\x00\xff\r\n"
    assert forbidden.calls == []


def test_existing_linguistic_json_does_not_suppress_missing_eligible_pca(tmp_path):
    inputs, outputs = tmp_path / "inputs", tmp_path / "outputs"
    inputs.mkdir()
    (inputs / "one.md").write_text("word word")
    existing = seed_output(outputs, "analysis.json")
    source = language_source(
        DEFAULT_CONFIG={
            "analysis_params": {"linguistic_features": ["lexical_diversity"]}
        },
        process_text=str.lower,
        word_tokenize=str.split,
    )
    produced = []

    def pca(features, output_dir, filename):
        produced.append(features)
        Path(output_dir, f"{filename}_pca.png").write_bytes(b"controlled PCA fixture")

    source["perform_pca_analysis"] = pca
    source["perform_linguistic_analysis"](str(inputs), str(outputs))
    assert produced == [[[0.5]]]
    assert existing.read_bytes() == b"historical\x00\xff\r\n"
    assert (outputs / "inputs_pca.png").read_bytes() == b"controlled PCA fixture"


@pytest.mark.parametrize("kind", ["entity", "grant"])
def test_missing_evaluation_keeps_description_payload_and_legacy_tuple_bytes(
    tmp_path, kind
):
    script = (
        "dissertation_entity_evaluation.py"
        if kind == "entity"
        else "dissertation_grant_evaluator.py"
    )
    folder_name = "Entity" if kind == "entity" else "Summarized_Grants"
    descriptor_name = "owner.py" if kind == "entity" else "call.md"
    inputs, outputs = tmp_path / "inputs", tmp_path / "outputs"
    inputs.mkdir()
    (inputs / "first.md").write_text("preserved input")
    (inputs / "second.md").write_text("new dissertation")
    script_root = tmp_path / "FieldSHIFT-2"
    script_root.mkdir()
    descriptors = tmp_path / "Fonds" / folder_name
    descriptors.mkdir(parents=True)
    (descriptors / descriptor_name).write_text("original description")
    calls = []

    def evaluate(*args):
        calls.append(args)
        return "evaluated text", 1.5

    utility = utilities()
    source = load_definitions(
        FIELD / script,
        load_file=utility["load_file"],
        evaluate_dissertation=evaluate,
        time=time,
        __file__=str(script_root / script),
    )
    prefix = "Evaluated_by_owner" if kind == "entity" else "Evaluated_for_call"
    suffix = "evaluated_by_owner" if kind == "entity" else "evaluated_for_call"
    existing = seed_output(outputs, f"{prefix}/first_{suffix}.md")
    source["process_dissertation_evaluation"](str(inputs), str(outputs), {})
    assert existing.read_bytes() == b"historical\x00\xff\r\n"
    assert (
        outputs / prefix / f"second_{suffix}.md"
    ).read_text() == "evaluated text 1.5"
    expected = (
        ("new dissertation", "owner", "original description", {})
        if kind == "entity"
        else ("new dissertation", "original description", {})
    )
    assert calls == [expected]
