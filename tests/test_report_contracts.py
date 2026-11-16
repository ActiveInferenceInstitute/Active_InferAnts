"""Local report specification/validation mechanics; no provider qualification."""

import asyncio
import logging
import uuid
from pathlib import Path

import pytest
from source_contract_helpers import load_definitions, load_phase


def specification(module):
    source = module.DataSource(
        name="fixture",
        type=module.DataSourceType.INTERNAL,
        description="local",
        limitations="fixture only",
        reliability=1.0,
        update_frequency="once",
        access_method="local",
    )
    method = module.AnalysisMethod(
        name="count",
        type=module.AnalysisMethodType.DESCRIPTIVE,
        description="local",
        expected_outcomes="count",
        limitations="fixture",
        required_tools=[],
    )
    audience = module.TargetAudience(
        name="owner",
        expertise_level="technical",
        key_interests=["counts"],
        preferred_formats=[module.DeliveryFormatType.RAW_DATA],
        decision_making_context="unit contract",
    )
    delivery = module.DeliveryFormat(
        type=module.DeliveryFormatType.RAW_DATA,
        reasoning="local fixture",
        alternatives=[],
        accessibility_considerations="text",
    )
    result = module.ReportSpecification(
        "fixture", [source], [method], audience, delivery
    )
    result.add_section("Result", "Controlled local observation")
    return result, [source, method, audience, delivery]


def test_every_report_dataclass_constructs_and_retains_required_fields(monkeypatch):
    module = load_phase(monkeypatch, "4_REPORT", "specify_report")
    report, components = specification(module)
    for component in components:
        assert str(uuid.UUID(component.id)) == component.id
        assert component.validate() is True
    assert components[0].name == "fixture"
    assert components[1].required_tools == []
    assert components[2].preferred_formats == [module.DeliveryFormatType.RAW_DATA]
    assert components[3].type is module.DeliveryFormatType.RAW_DATA
    assert report.validate() is True


@pytest.mark.parametrize("valid", [False, True])
def test_executor_consumes_synchronous_validation_before_provider_work(
    monkeypatch, valid
):
    module = load_phase(monkeypatch, "4_REPORT", "specify_report")
    report, _ = specification(module)
    if not valid:
        report.sections.clear()

    class ReportFailure(RuntimeError):
        pass

    definitions = load_definitions(
        Path("4_REPORT/execute_report.py"), ReportExecutionError=ReportFailure
    )
    executor = object.__new__(definitions["ReportExecutor"])
    executor.report_specification = report
    executor.logger = logging.getLogger("report_contract")
    unavailable = RuntimeError("Owner-selected collection provider not supplied")

    async def collection_boundary():
        raise unavailable

    executor._collect_data = collection_boundary
    with pytest.raises(ReportFailure) as failure:
        asyncio.run(executor.execute_report())
    if valid:
        assert failure.value.__cause__ is unavailable
    else:
        assert isinstance(failure.value.__cause__, ValueError)
        assert str(failure.value.__cause__) == "Invalid report specification"
