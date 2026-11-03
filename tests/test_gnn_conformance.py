"""Conformance tests for the Active InferAnts Gaussian agent GNN specification.

The specification is validated with the pinned GNN revision when the GNN
checkout and a suitable interpreter are available; the structural and
specification-vs-agent checks always run so CI still guards the specification.
When ``GNN_ROOT`` selects a checkout explicitly (as CI does after provisioning
the pinned revision), an unusable checkout is a failure, never a skip.
"""

from __future__ import annotations

import copy
import os
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gnn_conformance import (
    SPEC_PATH,
    ConformanceError,
    GnnUnavailable,
    canonical_model,
    check_conformance,
    extract_spec,
    load_pin,
)

REQUIRED_SECTIONS = (
    "GNNSection",
    "GNNVersionAndFlags",
    "ModelName",
    "StateSpaceBlock",
    "Connections",
    "InitialParameterization",
    "Equations",
    "Time",
    "ActInfOntologyAnnotation",
    "ModelParameters",
    "Footer",
    "Signature",
)

CANONICAL_PIN = {
    "repository": "ActiveInferenceInstitute/Generalized_Notation_Notation",
    "tag": "v5.0.3",
    "commit": "8f293d9ba810e6eda5c09842d9c7ed9ffa5f92c1",
}


@pytest.fixture(scope="module")
def extracted_model() -> dict:
    try:
        return extract_spec()
    except GnnUnavailable as exc:
        if os.environ.get("GNN_ROOT"):
            pytest.fail(f"GNN_ROOT selects a checkout, but the pinned parser is unavailable: {exc}")
        pytest.skip(f"pinned GNN checkout unavailable: {exc}")


def test_pin_record_is_canonical() -> None:
    pin = load_pin()
    assert pin.repository == CANONICAL_PIN["repository"]
    assert pin.tag == CANONICAL_PIN["tag"]
    assert pin.commit == CANONICAL_PIN["commit"]


def test_spec_declares_every_section() -> None:
    text = SPEC_PATH.read_text(encoding="utf-8")
    for section in REQUIRED_SECTIONS:
        assert f"## {section}" in text, f"missing section {section}"


def declared_dimensions() -> dict[str, tuple[int, ...]]:
    text = SPEC_PATH.read_text(encoding="utf-8")
    dimensions: dict[str, tuple[int, ...]] = {}
    for line in text.splitlines():
        match = re.match(
            r"^([A-Za-z_][A-Za-z0-9_]*)\[([0-9]+(?:\s*,\s*[0-9]+)*)\s*,type=",
            line.strip(),
        )
        if match:
            dimensions[match.group(1)] = tuple(
                int(part) for part in match.group(2).split(",")
            )
    return dimensions


def test_declared_dimensions_match_the_agent() -> None:
    dimensions = declared_dimensions()
    model = canonical_model()
    dimension = model["num_states"]
    for name in ("F", "H", "Q", "R", "prior_cov"):
        assert dimensions[name] == (dimension, dimension)
    for name in ("x", "y"):
        assert dimensions[name] == (dimension, 1)
    assert dimensions["prior_mean"] == (dimension,)


def test_agent_canonical_model_conforms() -> None:
    assert len(check_conformance(canonical_model())) == 4


def test_mutated_model_is_rejected() -> None:
    model = copy.deepcopy(canonical_model())
    model["initial_parameterization"]["Q"] = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
    with pytest.raises(ConformanceError, match="Q must be"):
        check_conformance(model)


def test_extraction_uses_schema_major_one(extracted_model: dict) -> None:
    assert extracted_model["extraction_schema_version"].startswith("1.")


def test_extracted_spec_conforms_to_the_agent(extracted_model: dict) -> None:
    assert len(check_conformance(extracted_model)) == 4


def test_missing_pin_file_is_rejected(tmp_path) -> None:
    with pytest.raises(ConformanceError, match="is missing"):
        load_pin(tmp_path / "upstream.json")


def test_incomplete_pin_record_is_rejected(tmp_path) -> None:
    pin = tmp_path / "upstream.json"
    pin.write_text('{"repository": "x", "tag": "v1"}', encoding="utf-8")
    with pytest.raises(ConformanceError, match="missing the 'commit' field"):
        load_pin(pin)


def test_malformed_pin_file_is_rejected(tmp_path) -> None:
    pin = tmp_path / "upstream.json"
    pin.write_text("not json", encoding="utf-8")
    with pytest.raises(ConformanceError, match="is unreadable"):
        load_pin(pin)
