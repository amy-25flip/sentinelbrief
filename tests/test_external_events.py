"""Entering the event that starts an external clock (docs/LABELS_IRDAI.md Part 3).

Each test names the bug it catches in its docstring.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.workspace import CaseStore
from sentinelbrief.workspace.cases import facts_to_profile, profile_to_facts

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2026, 10, 1, 10, 0, tzinfo=IST)
ORDER = "irdai.ics-guidelines.2023.gov-order-information-72h"
DISPOSE = "irdai.ics-guidelines.2023.grievance-dispose-15d"
IRDAI_6H = "irdai.ics-guidelines.2023.incident-reporting-6h"
RANSOMWARE = "Malicious code attacks such as Ransomware"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _profile(**kwargs) -> IncidentProfile:
    kwargs.setdefault("entity_classes", ["irdai.insurer"])
    return IncidentProfile(incident_types=[RANSOMWARE], when_noticed=T10, **kwargs)


def test_external_clock_runs_from_its_own_event(engine):
    """Catches: the order clock computed from the incident, or the fifteen days miscounted."""
    order_at = T10 + timedelta(days=30)
    result = engine.evaluate(_profile(external_events={ORDER: order_at, DISPOSE: order_at}))
    deadlines = {d.obligation_id: d for d in result.deadlines}
    assert deadlines[ORDER].anchor_type == "external_event"
    assert deadlines[ORDER].deadline_ist == order_at + timedelta(hours=72)
    assert deadlines[DISPOSE].deadline_ist == order_at + timedelta(days=15)
    assert deadlines[IRDAI_6H].deadline_ist == T10 + timedelta(hours=6)


def test_external_event_time_never_moves_the_governing_law_date(engine):
    """Catches: an order received before the incident, or long after, changing 'law as of'."""
    for delta in (timedelta(days=-400), timedelta(days=400)):
        result = engine.evaluate(_profile(external_events={ORDER: T10 + delta}))
        assert result.law_as_of == T10.date()


def test_invalid_external_events_are_rejected(engine):
    """Catches: a start time attached to an incident-driven duty, a naive time, or a typo'd id."""
    with pytest.raises(ValueError, match="not an obligation whose clock starts"):
        engine.evaluate(_profile(external_events={IRDAI_6H: T10}))
    with pytest.raises(ValueError, match="not an obligation whose clock starts"):
        engine.evaluate(_profile(external_events={"no.such.duty": T10}))
    with pytest.raises(ValueError, match="timezone-aware"):
        _profile(external_events={ORDER: datetime(2026, 10, 2, 9, 0)})


def test_external_time_for_a_duty_that_does_not_apply_gives_no_deadline(engine):
    """Catches: an IRDAI clock shown to an NBFC because a start time was supplied."""
    result = engine.evaluate(
        _profile(
            entity_classes=["nbfc.middle_layer"], when_detected=T10, external_events={ORDER: T10}
        )
    )
    assert ORDER not in {d.obligation_id for d in result.deadlines}
    assert ORDER in {n["obligation_id"] for n in result.not_applicable}


def test_external_events_survive_case_storage():
    """Catches: the start time lost or altered when a case is saved and reloaded."""
    profile = _profile(external_events={ORDER: T10 + timedelta(hours=23)})
    assert profile_to_facts(facts_to_profile(profile_to_facts(profile))) == profile_to_facts(
        profile
    )


def test_case_page_starts_an_external_clock(tmp_path, monkeypatch):
    """Catches: the case page offering no way to record the order, or losing an earlier one."""
    monkeypatch.setenv("SENTINELBRIEF_CASES_DIR", str(tmp_path / "cases"))
    client = TestClient(app, follow_redirects=False)
    case_id = CaseStore(tmp_path / "cases", REPO / "data").create(_profile(), "Asha Rao")
    page = client.get(f"/cases/{case_id}")
    assert "Clocks that start from another event" in page.text and ORDER in page.text
    headers = {"content-type": "application/x-www-form-urlencoded"}
    first = client.post(
        f"/api/cases/{case_id}/facts",
        content=f"external_duty={ORDER}&external_started=2026-10-02T09%3A00&recorded_by=Asha+Rao",
        headers=headers,
    )
    assert first.status_code == 303, first.text
    second = client.post(
        f"/api/cases/{case_id}/facts",
        content=f"external_duty={DISPOSE}&external_started=2026-10-01T12%3A00&recorded_by=Asha+Rao",
        headers=headers,
    )
    assert second.status_code == 303, second.text
    view = client.get(f"/api/cases/{case_id}").json()
    due = {d["obligation_id"]: d["deadline_ist"] for d in view["clock"]["deadlines"]}
    assert due[ORDER] == "2026-10-05T09:00:00+05:30"
    assert due[DISPOSE] == "2026-10-16T12:00:00+05:30"
    assert ORDER in {r["draft"]["obligation_id"] for r in view["drafts"]}
    half = client.post(
        f"/api/cases/{case_id}/facts",
        content=f"external_duty={ORDER}&recorded_by=Asha+Rao",
        headers=headers,
    )
    assert half.status_code == 422


def test_json_api_accepts_external_events():
    """Catches: the JSON API silently dropping the start time, or accepting one without an offset."""
    client = TestClient(app)
    base = {
        "entity_classes": ["irdai.insurer"],
        "incident_types": [RANSOMWARE],
        "when_noticed": "2026-10-01T10:00:00+05:30",
    }
    ok = client.post(
        "/api/incident/clock",
        json={**base, "external_events": {ORDER: "2026-10-02T09:00:00+05:30"}},
    )
    assert ok.status_code == 200, ok.text
    assert ORDER in {d["obligation_id"] for d in ok.json()["deadlines"]}
    naive = client.post(
        "/api/incident/clock", json={**base, "external_events": {ORDER: "2026-10-02T09:00:00"}}
    )
    assert naive.status_code == 422
    wrong = client.post(
        "/api/incident/clock",
        json={**base, "external_events": {IRDAI_6H: "2026-10-02T09:00:00+05:30"}},
    )
    assert wrong.status_code == 422


def test_external_duty_is_governed_by_the_law_on_the_day_of_its_event(engine):
    """Catches: an order received after the guidelines began being ignored because the incident
    predates them, or one received before they began being given a clock."""
    old_incident = datetime(2023, 4, 1, 10, 0, tzinfo=IST)
    after = datetime(2023, 5, 2, 9, 0, tzinfo=IST)
    result = engine.evaluate(
        IncidentProfile(
            entity_classes=["irdai.insurer"],
            incident_types=[RANSOMWARE],
            when_noticed=old_incident,
            external_events={ORDER: after},
        )
    )
    deadlines = {d.obligation_id: d for d in result.deadlines}
    assert deadlines[ORDER].deadline_ist == after + timedelta(hours=72)
    assert IRDAI_6H in {n["obligation_id"] for n in result.not_applicable}
    assert result.law_as_of == old_incident.date()
    before = engine.evaluate(
        _profile(external_events={ORDER: datetime(2023, 4, 2, 9, 0, tzinfo=IST)})
    )
    assert ORDER in {n["obligation_id"] for n in before.not_applicable}


def test_report_time_before_the_incident_is_flagged(engine):
    """Catches: an impossible order of events accepted with no warning."""
    odd = engine.evaluate(
        IncidentProfile(
            entity_classes=["sebi.mii"],
            incident_types=[RANSOMWARE],
            when_noticed=T10,
            when_reported_to_sebi=T10 - timedelta(hours=2),
            uses_protected_systems=False,
        )
    )
    assert any("earlier than every incident time" in c for c in odd.caveats)
    fine = engine.evaluate(
        IncidentProfile(
            entity_classes=["sebi.mii"],
            incident_types=[RANSOMWARE],
            when_noticed=T10,
            when_reported_to_sebi=T10 + timedelta(hours=2),
            uses_protected_systems=False,
        )
    )
    assert not any("earlier than every incident time" in c for c in fine.caveats)
