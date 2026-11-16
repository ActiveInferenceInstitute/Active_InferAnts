"""Typed follow-up and local dispatch contracts, without external services."""

import json
import logging
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest
from source_contract_helpers import load_definitions, load_phase


@pytest.fixture
def followup(monkeypatch):
    return load_phase(monkeypatch, "5_FOLLOWUP", "specify_followup")


def minimal(module):
    specification = module.FollowUpSpecification("fixture")
    specification.set_metrics({"done": True}, {"count": 1}, "once")
    return specification


@pytest.mark.parametrize("purpose", list(range(5)))
@pytest.mark.parametrize("modality", list(range(2)))
@pytest.mark.parametrize("follow_type", list(range(4)))
def test_followup_export_import_export_is_typed_and_stable(
    followup, tmp_path, purpose, modality, follow_type
):
    moment = datetime(
        2026,
        11,
        13,
        12,
        34,
        56,
        789000,
        tzinfo=timezone(timedelta(hours=5, minutes=30)),
    )
    duration = timedelta(days=1, seconds=61, microseconds=250000)
    original = minimal(followup)
    original.follow_up_type = list(followup.FollowUpType)[follow_type]
    original.add_update_area("Documentation", 1, "owner", notes="actual payload")
    original.add_session(
        list(followup.SessionType)[purpose],
        moment,
        duration,
        "owner",
        list(followup.SessionModality)[modality],
        attendees=["participant"],
    )
    original.set_debrief_details(moment, ["participant"], ["review"], ["decision"])
    original.set_timeline(
        moment, None, {"kickoff": moment, "unplanned": None}, {"kickoff": []}
    )
    original.add_resource("undated", "human", 50)
    original.add_resource("dated", "technical", 50, moment, moment + duration)
    first, second = tmp_path / "first.json", tmp_path / "second.json"
    original.export_to_json(str(first))
    loaded = minimal(followup)
    loaded.import_from_json(str(first))
    loaded.export_to_json(str(second))
    assert json.loads(first.read_text()) == json.loads(second.read_text())
    assert loaded.follow_up_type is original.follow_up_type
    assert loaded.sessions[0].type is original.sessions[0].type
    assert loaded.sessions[0].modality is original.sessions[0].modality
    assert loaded.sessions[0].date == moment
    assert loaded.sessions[0].duration == duration
    assert loaded.debrief_details["date"] == moment
    assert loaded.timeline["milestones"] == {"kickoff": moment, "unplanned": None}
    assert loaded.timeline["end_date"] is None
    assert (
        loaded.resources[0].start_date is None and loaded.resources[0].end_date is None
    )
    assert loaded.resources[1].end_date == moment + duration
    assert json.loads(first.read_text())["sessions"][0]["duration"] == 86461.25


def test_empty_optional_debrief_and_timeline_roundtrip(followup, tmp_path):
    original = minimal(followup)
    path = tmp_path / "empty.json"
    original.export_to_json(str(path))
    loaded = minimal(followup)
    loaded.import_from_json(str(path))
    assert (
        loaded.generate_followup_specification()
        == original.generate_followup_specification()
    )
    assert loaded.debrief_details == {} and loaded.timeline == {}


def executor_for(module, specification):
    definitions = load_definitions(
        Path("5_FOLLOWUP/execute_followup.py"),
        SessionModality=module.SessionModality,
        datetime=datetime,
        timezone=timezone,
    )
    executor = object.__new__(definitions["FollowUpExecutor"])
    executor.specification = specification
    executor.logger = logging.getLogger("followup_contract")
    executor._failed = False
    executor.completed_at = None
    executor.result = None
    return executor


@pytest.mark.parametrize("area", ["Database", "Documentation", "Infrastructure"])
def test_updates_use_the_declared_notes_payload(followup, area):
    calls = []
    executor = executor_for(followup, minimal(followup))
    executor.database_service = SimpleNamespace(
        perform_database_update=lambda payload: calls.append(payload)
    )
    executor.project_manager = SimpleNamespace(
        update_documentation=lambda payload: calls.append(payload)
    )
    executor.resource_allocator = SimpleNamespace(
        update_infrastructure=lambda payload: calls.append(payload)
    )
    update = followup.UpdateArea(area, 1, "owner", notes="declared update")
    executor._update_area(update)
    assert calls == ["declared update"]


@pytest.mark.parametrize("purpose", list(range(5)))
@pytest.mark.parametrize("modality", list(range(2)))
def test_session_purpose_is_independent_of_delivery_modality(
    followup, purpose, modality
):
    calls = []
    executor = executor_for(followup, minimal(followup))
    executor.project_manager = SimpleNamespace(
        start_virtual_session=lambda session: calls.append(("virtual", session.type)),
        start_in_person_session=lambda session: calls.append(
            ("in_person", session.type)
        ),
    )
    session_type = list(followup.SessionType)[purpose]
    channel = list(followup.SessionModality)[modality]
    session = followup.Session(
        session_type, datetime.now(timezone.utc), timedelta(minutes=1), "owner", channel
    )
    executor._run_session(session)
    assert calls == [("virtual" if modality == 0 else "in_person", session_type)]


def test_finalization_is_local_and_refuses_failed_operations(followup):
    specification = minimal(followup)
    executor = executor_for(followup, specification)
    executor._failed = True
    with pytest.raises(RuntimeError):
        executor._finalize_followup()
    assert executor.completed_at is None and executor.result is None
    executor._failed = False
    assert (
        executor._finalize_followup() == specification.generate_followup_specification()
    )
    assert executor.completed_at.tzinfo is timezone.utc


def test_cleanup_attempts_both_owned_operations_and_propagates_failure(followup):
    calls = []
    executor = executor_for(followup, minimal(followup))
    failure = OSError("database close failed")

    def close():
        calls.append("close")
        raise failure

    executor.database_service = SimpleNamespace(close_connections=close)
    executor.resource_allocator = SimpleNamespace(
        release_allocation=lambda: calls.append("release")
    )
    executor.error_handler = SimpleNamespace(
        handle_cleanup_error=lambda error: calls.append(error)
    )
    executor.notification_service = SimpleNamespace(
        send_alert=lambda *args: calls.append("alert")
    )
    with pytest.raises(OSError) as caught:
        executor._cleanup()
    assert caught.value is failure
    assert calls == ["close", "release", failure, "alert"]
    assert executor._failed is True and executor.completed_at is None


@pytest.mark.parametrize(
    "method,error_type",
    [
        ("_execute_update_areas", RuntimeError),
        ("_conduct_sessions", RuntimeError),
        ("_conduct_debrief", RuntimeError),
        ("_implement_plan", RuntimeError),
        ("_engage_stakeholders", RuntimeError),
        ("_track_metrics", RuntimeError),
        ("_manage_timeline", RuntimeError),
        ("_allocate_resources", ValueError),
        ("_allocate_resources", RuntimeError),
        ("_generate_and_distribute_reports", RuntimeError),
        ("_distribute_reports", RuntimeError),
        ("_send_email", RuntimeError),
    ],
)
def test_handled_component_failure_cannot_be_finalized_as_success(
    followup, method, error_type
):
    specification = minimal(followup)
    moment = datetime.now(timezone.utc)
    specification.add_update_area("Documentation", 1, "owner", notes="payload")
    specification.add_session(
        followup.SessionType.LESSONS_LEARNED,
        moment,
        timedelta(minutes=1),
        "owner",
        followup.SessionModality.VIRTUAL,
    )
    specification.set_debrief_details(moment, [], [], [])
    specification.set_plan_details("Maintenance", "once", "owner", [], [])
    specification.add_stakeholder(
        "owner", "reviewer", "fixture@example.invalid", engagement_strategy="Email"
    )
    specification.add_resource("resource", "human", 1)
    executor = executor_for(followup, specification)
    failure = error_type("controlled component failure")
    handled = []

    def fail(*args, **kwargs):
        raise failure

    class FailedService:
        def __getattr__(self, name):
            return fail

    class ErrorRecords:
        def __getattr__(self, name):
            return lambda *args, **kwargs: handled.append(name)

    for name in (
        "database_service",
        "project_manager",
        "metrics_analyzer",
        "resource_allocator",
        "email_service",
    ):
        setattr(executor, name, FailedService())
    executor.error_handler = ErrorRecords()
    executor.notification_service = SimpleNamespace(
        send_alert=lambda *args: handled.append("alert")
    )
    overrides = {
        "_execute_update_areas": "_update_area",
        "_conduct_sessions": "_prepare_session",
        "_conduct_debrief": "_prepare_debrief",
        "_engage_stakeholders": "_engage_stakeholder",
        "_generate_and_distribute_reports": "_generate_text_report",
        "_distribute_reports": "_send_email",
    }
    if method in overrides:
        setattr(executor, overrides[method], fail)
    arguments = (
        ("fixture@example.invalid", "subject", "text", "html")
        if method == "_send_email"
        else ("text", "html")
        if method == "_distribute_reports"
        else ()
    )
    getattr(executor, method)(*arguments)
    with pytest.raises(RuntimeError):
        executor._finalize_followup()
    assert executor.result is None and executor.completed_at is None
    assert handled


def test_critical_execution_failure_propagates_after_both_cleanup_operations(followup):
    executor = executor_for(followup, minimal(followup))
    calls = []
    failure = RuntimeError("initialization failed")

    def initialize():
        raise failure

    executor._initialize_followup = initialize
    executor.error_handler = SimpleNamespace(
        handle_critical_error=lambda *args: calls.append("critical")
    )
    executor.notification_service = SimpleNamespace(
        send_alert=lambda *args: calls.append("alert")
    )
    executor.database_service = SimpleNamespace(
        close_connections=lambda: calls.append("close")
    )
    executor.resource_allocator = SimpleNamespace(
        release_allocation=lambda: calls.append("release")
    )
    with pytest.raises(RuntimeError) as caught:
        executor.execute_followup()
    assert caught.value is failure
    assert calls == ["critical", "alert", "close", "release"]
    assert executor.completed_at is None and executor.result is None


def test_session_attendees_are_owned_per_session_and_not_aliased_to_caller(followup):
    first, second = minimal(followup), minimal(followup)
    moment = datetime.now(timezone.utc)
    purpose, modality = (
        followup.SessionType.LESSONS_LEARNED,
        followup.SessionModality.VIRTUAL,
    )
    first.add_session(purpose, moment, timedelta(minutes=1), "owner", modality)
    second.add_session(purpose, moment, timedelta(minutes=1), "owner", modality)
    first.sessions[0].attendees.append("first only")
    assert second.sessions[0].attendees == []
    attendees = ["original"]
    first.add_session(
        followup.SessionType.STAKEHOLDER_REVIEW,
        moment,
        timedelta(minutes=1),
        "owner",
        modality,
        attendees=attendees,
    )
    attendees.append("later caller mutation")
    assert first.sessions[1].attendees == ["original"]
