"""SEBI forensic report and quarterly reports (docs/LABELS_SEBI.md Part 2).

Each test names the bug it catches in its docstring.
"""

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.workspace import recurring_duties_ics

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2026, 10, 1, 10, 0, tzinfo=IST)
REPORTED = T10 + timedelta(hours=5)
FORENSIC = "sebi.cscrf.2024.post-incident-forensic-report-75d"
INTERIM = "sebi.cscrf.2024.post-incident-interim-report-3d"
QUARTERLY = "sebi.cscrf.2024.quarterly-report-15d"
RANSOMWARE = "Malicious code attacks such as Ransomware"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _run(engine, **kwargs):
    kwargs.setdefault("entity_classes", ["sebi.qualified_re"])
    kwargs.setdefault("incident_types", [RANSOMWARE])
    kwargs.setdefault("when_noticed", T10)
    kwargs.setdefault("uses_protected_systems", False)
    return engine.evaluate(IncidentProfile(**kwargs))


def _deadlines(result):
    return {d.obligation_id: d for d in result.deadlines}


def _asked(result, obligation_id):
    return [u.question for u in result.unknowns if obligation_id in u.affects]


def test_forensic_report_follows_the_severity_the_entity_states(engine):
    """Catches: a forensic deadline for Low or Medium incidents, or none for High or Critical."""
    for severity in ("high", "critical"):
        due = _deadlines(_run(engine, when_reported_to_sebi=REPORTED, sebi_severity=severity))[
            FORENSIC
        ]
        assert due.anchor_type == "reported" and due.deadline_ist == REPORTED + timedelta(days=75)
    for severity in ("low", "medium"):
        result = _run(engine, when_reported_to_sebi=REPORTED, sebi_severity=severity)
        reason = next(n["reason"] for n in result.not_applicable if n["obligation_id"] == FORENSIC)
        assert "may still be required" in reason and not _asked(result, FORENSIC)


def test_severity_is_asked_never_assumed(engine):
    """Catches: severity defaulted (either way) when the entity has not classified the incident."""
    result = _run(engine, when_reported_to_sebi=REPORTED)
    assert FORENSIC not in _deadlines(result) and FORENSIC in result.undetermined
    assert any("severity" in q for q in _asked(result, FORENSIC))
    with pytest.raises(ValueError, match="low, medium, high or critical"):
        IncidentProfile(entity_classes=["sebi.mii"], sebi_severity="severe")


def test_forensic_clock_starts_only_from_the_report(engine):
    """Catches: 'brought to notice' starting the forensic clock as it starts the Table 36 clocks."""
    brought = T10 - timedelta(hours=1)
    result = _run(engine, when_noticed=None, when_brought_to_notice=brought, sebi_severity="high")
    assert _deadlines(result)[INTERIM].anchor_type == "brought_to_notice"
    assert FORENSIC not in _deadlines(result)
    assert any("reported to SEBI" in q for q in _asked(result, FORENSIC))


def test_severity_question_waits_for_the_incident_question(engine):
    """Catches: asking for severity before knowing whether any SEBI reporting duty applies."""
    unresolved = _run(engine, incident_types=["hardware failure"])
    assert any("Annexure I" in q for q in _asked(unresolved, FORENSIC))
    assert not any("severity" in q for q in _asked(unresolved, FORENSIC))
    none = _run(
        engine,
        incident_types=["hardware failure"],
        is_annexure_i_type=False,
        is_cyber_incident=False,
    )
    assert FORENSIC in {n["obligation_id"] for n in none.not_applicable} and not none.unknowns


def test_forensic_duty_does_not_reach_other_sectors(engine):
    """Catches: the SEBI forensic duty or its severity question shown to an NBFC."""
    result = _run(
        engine, entity_classes=["nbfc.middle_layer"], when_detected=T10, sebi_severity="high"
    )
    assert FORENSIC in {n["obligation_id"] for n in result.not_applicable}
    assert not _asked(result, FORENSIC)


def test_quarterly_report_is_ongoing_and_lands_on_the_fixed_dates(engine):
    """Catches: the quarterly report computed as an incident deadline, or placed on wrong dates."""
    result = _run(engine)
    assert QUARTERLY in result.applicable_obligations and QUARTERLY not in _deadlines(result)
    ics, undetermined = recurring_duties_ics(engine, ["sebi.small_re"], date(2026, 10, 1))
    starts = sorted(line.split(":")[1] for line in ics.split("\r\n") if line.startswith("DTSTART"))
    assert starts == ["20261015", "20270115", "20270415", "20270715"]
    assert ics.count("RRULE:FREQ=YEARLY;INTERVAL=1") == 4 and undetermined == []
    assert "Due on a date fixed by the clause." in ics.replace("\r\n ", "")
    on_the_day, _ = recurring_duties_ics(engine, ["sebi.small_re"], date(2026, 10, 15))
    assert "DTSTART;VALUE=DATE:20271015" in on_the_day
    nothing, _ = recurring_duties_ics(engine, ["nbfc.bl_below_500cr"], date(2026, 10, 1))
    assert "BEGIN:VEVENT" not in nothing


def test_api_and_case_accept_severity(tmp_path, monkeypatch):
    """Catches: the severity not reaching the engine through the API or a stored case."""
    monkeypatch.setenv("SENTINELBRIEF_CASES_DIR", str(tmp_path / "cases"))
    client = TestClient(app, follow_redirects=False)
    base = {
        "entity_classes": ["sebi.qualified_re"],
        "incident_types": [RANSOMWARE],
        "when_noticed": "2026-10-01T10:00:00+05:30",
        "when_reported_to_sebi": "2026-10-01T15:00:00+05:30",
        "uses_protected_systems": False,
    }
    high = client.post("/api/incident/clock", json={**base, "sebi_severity": "high"})
    assert FORENSIC in {d["obligation_id"] for d in high.json()["deadlines"]}
    assert (
        client.post("/api/incident/clock", json={**base, "sebi_severity": "awful"}).status_code
        == 422
    )
    case_id = client.post("/api/cases", json={**base, "opened_by": "Asha Rao"}).json()["case_id"]
    assert FORENSIC in client.get(f"/api/cases/{case_id}").json()["clock"]["undetermined"]
    saved = client.post(
        f"/api/cases/{case_id}/facts",
        content="sebi_severity=critical&recorded_by=Asha+Rao",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert saved.status_code == 303, saved.text
    due = {
        d["obligation_id"]: d["deadline_ist"]
        for d in client.get(f"/api/cases/{case_id}").json()["clock"]["deadlines"]
    }
    assert due[FORENSIC] == "2026-12-15T15:00:00+05:30"
