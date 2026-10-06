"""Duties whose clock starts from something other than the incident (IRDAI Part 2).

Each test names the bug it catches in its docstring.
"""

import copy
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.workspace import build_drafts, load_filing_content, recurring_duties_ics

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2026, 10, 1, 10, 0, tzinfo=IST)
IRDAI = "irdai.ics-guidelines.2023."
EXTERNAL = {
    IRDAI + "gov-order-information-72h": "PT72H",
    IRDAI + "grievance-acknowledge-24h": "PT24H",
    IRDAI + "grievance-dispose-15d": "P15D",
    IRDAI + "content-takedown-24h": "PT24H",
    IRDAI + "lost-device-internal-report-4h": "PT4H",
}
OTHER = {IRDAI + "registration-data-retention-180d", IRDAI + "cloud-breach-notice-contract-clause"}
RANSOMWARE = "Malicious code attacks such as Ransomware"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _insurer(engine, **kwargs):
    kwargs.setdefault("when_noticed", T10)
    return engine.evaluate(
        IncidentProfile(entity_classes=["irdai.insurer"], incident_types=[RANSOMWARE], **kwargs)
    )


def test_external_clock_duties_are_listed_without_a_deadline_or_a_question(engine):
    """Catches: a 72-hour 'government order' clock computed from the time the incident was noticed."""
    result = _insurer(
        engine, when_detected=T10, when_occurred=T10, when_aware=T10, when_brought_to_notice=T10
    )
    with_deadline = {d.obligation_id for d in result.deadlines}
    assert set(EXTERNAL) | OTHER <= set(result.applicable_obligations)
    assert not (set(EXTERNAL) | OTHER) & with_deadline
    assert not (set(EXTERNAL) | OTHER) & {t.obligation_id for t in result.time_critical}
    assert not result.unknowns


def test_external_clock_duties_keep_their_duration_in_the_data(engine):
    """Catches: the time limit lost because the duty was flattened to 'no deadline'."""
    for obligation_id, duration in EXTERNAL.items():
        deadline = engine.get_obligation(obligation_id)["normalized"]["deadline"]
        assert (deadline["kind"], deadline["anchor"], deadline["duration_iso8601"]) == (
            "relative",
            "external_event",
            duration,
        )


def test_external_clock_cannot_be_mixed_with_incident_anchors(engine, monkeypatch):
    """Catches: a record that says 'external' but would still start from an incident time."""
    broken = copy.deepcopy(engine.get_obligation(IRDAI + "gov-order-information-72h"))
    broken["normalized"]["deadline"]["alternative_anchors"] = ["noticing"]
    monkeypatch.setattr(engine, "obligations", [broken])
    with pytest.raises(ValueError, match="external_event clock cannot have"):
        _insurer(engine)


def test_external_and_contract_duties_are_not_drafted_as_filings(engine):
    """Catches: a 'filing draft' for a duty that is not triggered by this incident."""
    result = _insurer(engine)
    drafted = {
        d.obligation_id for d in build_drafts(engine, result, load_filing_content(REPO / "data"))
    }
    assert not (set(EXTERNAL) | OTHER) & drafted
    assert IRDAI + "incident-reporting-6h" in drafted


def test_calendar_ignores_external_and_retention_duties(engine):
    """Catches: a complaint or retention clock exported as a recurring calendar event."""
    ics, undetermined = recurring_duties_ics(engine, ["irdai.insurer"], T10.date())
    assert undetermined == []
    unfolded = ics.replace("\r\n ", "")
    for obligation_id in [*EXTERNAL, *OTHER]:
        assert f"X-SENTINELBRIEF-OBLIGATION:{obligation_id}" not in unfolded
    assert "X-SENTINELBRIEF-OBLIGATION:" in unfolded


def test_clock_page_says_the_clock_does_not_start_from_the_incident():
    """Catches: the page showing '72 hours' with nothing to say what it runs from."""
    form = (
        "entity_class=irdai.insurer&incident_types=Malicious+code+attacks+such+as+Ransomware"
        "&when_noticed=2026-10-01T10%3A00"
    )
    page = TestClient(app).post(
        "/api/incident/clock",
        content=form,
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )
    assert page.status_code == 200
    assert "Within PT72H of: receipt of an order" in page.text
    assert "does not start from the incident" in page.text
    assert "Retain P180D" in page.text
