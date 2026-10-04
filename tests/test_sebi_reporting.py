"""SEBI CSCRF reporting duties beyond the six-hour notice (docs/LABELS_SEBI.md).

Each test names the bug it catches in its docstring.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2026, 10, 1, 10, 0, tzinfo=IST)
S = "sebi.cscrf.2024."
SIX, PORTAL, BROKER = (
    S + "incident-reporting-6h",
    S + "incident-portal-24h",
    S + "broker-dp-exchange-reporting-6h",
)
OTHER, NCIIPC = S + "other-incidents-24h", S + "nciipc-protected-system-report"
POST = [
    S + "post-incident-interim-report-3d",
    S + "post-incident-mitigation-7d",
    S + "post-incident-rca-30d",
    S + "post-incident-vapt-45d",
]
RANSOMWARE = "Malicious code attacks such as Ransomware"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _run(engine, classes, **kwargs):
    kwargs.setdefault("incident_types", [RANSOMWARE])
    kwargs.setdefault("when_noticed", T10)
    kwargs.setdefault("uses_protected_systems", False)
    return engine.evaluate(IncidentProfile(entity_classes=classes, **kwargs))


def _deadlines(result):
    return {d.obligation_id: d for d in result.deadlines}


def _not_applicable(result):
    return {n["obligation_id"] for n in result.not_applicable}


def _asked(result):
    return {(oid, u.question) for u in result.unknowns for oid in u.affects}


def test_portal_clock_starts_at_the_six_hour_anchor(engine):
    """Catches: the 24-hour portal filing computed from a different event than the six-hour notice."""
    result = _run(engine, ["sebi.mii"], when_noticed=T10, when_detected=T10 - timedelta(hours=2))
    deadlines = _deadlines(result)
    assert deadlines[SIX].anchor_type == deadlines[PORTAL].anchor_type == "detection"
    assert deadlines[PORTAL].deadline_utc - deadlines[SIX].deadline_utc == timedelta(hours=18)


def test_broker_duty_only_for_brokers_and_depository_participants(engine):
    """Catches: the exchange-reporting duty leaking to every regulated entity."""
    assert BROKER in _not_applicable(_run(engine, ["sebi.small_re"]))
    for role in ("sebi.stock_broker", "sebi.depository_participant"):
        assert BROKER in _deadlines(_run(engine, ["sebi.small_re", role]))


def test_role_only_profile_still_owes_the_re_duties(engine):
    """Catches: a broker with no size category selected being told it owes nothing."""
    deadlines = _deadlines(_run(engine, ["sebi.stock_broker"]))
    assert {SIX, PORTAL, BROKER} <= set(deadlines)


def test_other_incident_duty_states(engine):
    """Catches: the 24-hour 'other incident' duty firing for Annexure I incidents, or without
    knowing whether the event is a cybersecurity incident at all."""
    listed = _run(engine, ["sebi.midsize_re"])
    assert OTHER in _not_applicable(listed)

    hardware = {"incident_types": ["hardware failure"]}
    unresolved = _run(engine, ["sebi.midsize_re"], **hardware)
    assert OTHER in unresolved.undetermined and not unresolved.deadlines
    assert any(oid == OTHER and "Annexure I" in q for oid, q in _asked(unresolved))

    not_listed = _run(engine, ["sebi.midsize_re"], is_annexure_i_type=False, **hardware)
    assert any(oid == OTHER and "cybersecurity incident" in q for oid, q in _asked(not_listed))

    other = _run(
        engine, ["sebi.midsize_re"], is_annexure_i_type=False, is_cyber_incident=True, **hardware
    )
    assert set(_deadlines(other)) == {OTHER}
    assert _deadlines(other)[OTHER].deadline_ist == T10 + timedelta(hours=24)

    nothing = _run(
        engine, ["sebi.midsize_re"], is_annexure_i_type=False, is_cyber_incident=False, **hardware
    )
    assert {SIX, PORTAL, OTHER, *POST} <= _not_applicable(nothing)
    assert not nothing.unknowns


def test_nciipc_duty_states(engine):
    """Catches: the NCIIPC duty assumed, or dropped, when protected-system status is unknown."""
    yes = _run(engine, ["sebi.mii"], uses_protected_systems=True)
    assert NCIIPC in yes.applicable_obligations
    assert NCIIPC not in _deadlines(yes)
    assert NCIIPC not in {t.obligation_id for t in yes.time_critical}

    assert NCIIPC in _not_applicable(_run(engine, ["sebi.mii"], uses_protected_systems=False))

    unknown = _run(engine, ["sebi.mii"], uses_protected_systems=None)
    assert NCIIPC in unknown.undetermined
    assert any(oid == NCIIPC and "Protected system" in q for oid, q in _asked(unknown))
    assert SIX in _deadlines(unknown)


def test_post_incident_clocks_run_from_the_report_time(engine):
    """Catches: Table 36 deadlines counted from noticing instead of the report to SEBI."""
    reported = T10 + timedelta(hours=5)
    deadlines = _deadlines(_run(engine, ["sebi.qualified_re"], when_reported_to_sebi=reported))
    for oid, days in zip(POST, (3, 7, 30, 45), strict=True):
        assert deadlines[oid].anchor_type == "reported"
        assert deadlines[oid].deadline_ist == reported + timedelta(days=days)


def test_post_incident_clock_uses_the_earlier_of_report_and_brought_to_notice(engine):
    """Catches: ignoring 'or being brought to notice' in the Table 36 heading."""
    brought = T10 - timedelta(hours=1)
    result = _run(
        engine,
        ["sebi.qualified_re"],
        when_noticed=None,
        when_brought_to_notice=brought,
        when_reported_to_sebi=T10 + timedelta(hours=5),
    )
    interim = _deadlines(result)[POST[0]]
    assert interim.anchor_type == "brought_to_notice"
    assert interim.deadline_ist == brought + timedelta(days=3)


def test_post_incident_clock_asks_when_no_report_time(engine):
    """Catches: a post-incident deadline invented from the noticing time."""
    result = _run(engine, ["sebi.qualified_re"])
    assert not set(POST) & set(_deadlines(result))
    for oid in POST:
        assert any(a == oid and "reported to SEBI" in q for a, q in _asked(result))


def test_report_time_does_not_move_the_governing_law_date(engine):
    """Catches: a late report shifting 'law as of' away from the incident date."""
    result = _run(engine, ["sebi.mii"], when_reported_to_sebi=T10 + timedelta(days=40))
    assert result.law_as_of == T10.date()
    only_report = engine.evaluate(
        IncidentProfile(
            entity_classes=["sebi.mii"], incident_types=[RANSOMWARE], when_reported_to_sebi=T10
        )
    )
    assert only_report.law_as_of == T10.date()


def test_sebi_duties_do_not_reach_an_nbfc(engine):
    """Catches: SEBI duties, or SEBI questions, shown to an entity SEBI does not regulate."""
    result = _run(engine, ["nbfc.middle_layer"], when_detected=T10, uses_protected_systems=None)
    assert {SIX, PORTAL, BROKER, OTHER, NCIIPC, *POST} <= _not_applicable(result)
    assert not any(oid.startswith(S) for oid, _ in _asked(result))


def test_naive_report_time_is_rejected():
    """Catches: a report time silently read in the server's timezone."""
    with pytest.raises(ValueError, match="timezone-aware"):
        IncidentProfile(
            entity_classes=["sebi.mii"], when_reported_to_sebi=datetime(2026, 10, 1, 15, 0)
        )


def test_api_accepts_protected_system_and_report_time():
    """Catches: the new facts not reaching the engine through the JSON API."""
    client = TestClient(app)
    base = {
        "entity_classes": ["sebi.mii"],
        "incident_types": [RANSOMWARE],
        "when_noticed": "2026-10-01T10:00:00+05:30",
    }
    full = client.post(
        "/api/incident/clock",
        json={
            **base,
            "uses_protected_systems": True,
            "when_reported_to_sebi": "2026-10-01T15:00:00+05:30",
        },
    )
    assert full.status_code == 200, full.text
    body = full.json()
    assert NCIIPC in body["applicable_obligations"]
    assert POST[0] in {d["obligation_id"] for d in body["deadlines"]}

    unknown = client.post("/api/incident/clock", json=base)
    assert unknown.status_code == 200, unknown.text
    assert NCIIPC in unknown.json()["undetermined"]

    bad = client.post("/api/incident/clock", json={**base, "uses_protected_systems": "maybe"})
    assert bad.status_code in (400, 422)


def test_incident_form_offers_the_new_fields():
    """Catches: the form having no way to state protected-system status or the report time."""
    page = TestClient(app).get("/incident")
    assert page.status_code == 200
    assert 'name="protected_system_attestation"' in page.text
    assert 'name="when_reported_to_sebi"' in page.text
