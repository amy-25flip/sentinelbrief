"""IRDAI duties with a stated period or time limit (docs/LABELS_IRDAI.md Part 4).

Each test names the bug it catches in its docstring.
"""

import copy
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.workspace import recurring_duties_ics

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
P = "irdai.ics-guidelines.2023."
LAST_DONE = date(2026, 4, 1)

ANNUAL = {
    "policy-review-annual",
    "risk-assessment-annual",
    "assurance-audit-annual",
    "bcp-risk-analysis-annual",
    "dr-plan-review-annual",
    "bcp-dr-test-annual",
    "evacuation-drill-annual",
    "vapt-internet-facing-annual",
    "is-practices-review-annual",
    "users-informed-of-termination-right-annual",
    "users-informed-of-rules-annual",
}
HALF_YEARLY = {
    "restoration-test-half-yearly",
    "physical-access-review-half-yearly",
    "external-pt-half-yearly",
}
COMMON = (
    {name: "20270401" for name in ANNUAL}
    | {name: "20261001" for name in HALF_YEARLY}
    | {
        "remote-access-accounts-monthly": "20260501",
        "risk-mitigation-plan-review-quarterly": "20260701",
    }
)
INSURER = COMMON | {
    "insurer-audit-report-to-irdai": "20260629",
    "frb-annexure-vi-year-end": "20270331",
}
INTERMEDIARY = COMMON | {"intermediary-annexure-iii-to-insurer-annual": "20270401"}
NOT_RECURRING = {"log-retention-180d", "vapt-high-risk-closure-1m", "audit-gap-closure-2m"}


@pytest.fixture
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _events(ics: str) -> dict[str, str]:
    """Obligation id (without the instrument prefix) -> first due date, IRDAI events only."""
    unfolded = ics.replace("\r\n ", "")
    found: dict[str, str] = {}
    for block in unfolded.split("BEGIN:VEVENT")[1:]:
        fields = dict(line.split(":", 1) for line in block.split("\r\n") if ":" in line)
        obligation_id = fields["X-SENTINELBRIEF-OBLIGATION"]
        if obligation_id.startswith(P):
            assert obligation_id[len(P) :] not in found
            found[obligation_id[len(P) :]] = fields["DTSTART;VALUE=DATE"]
    return found


def _calendar(engine: IncidentClockEngine, cls: str) -> tuple[dict[str, str], list[str]]:
    ics, undetermined = recurring_duties_ics(engine, [cls], LAST_DONE)
    return _events(ics), undetermined


def test_insurer_calendar_is_exactly_the_label(engine):
    """Catches: a missing or extra recurring duty, or a wrong first due date, for an insurer."""
    events, undetermined = _calendar(engine, "irdai.insurer")
    assert events == INSURER and len(events) == 18
    assert undetermined == []


def test_intermediary_calendar_is_exactly_the_label(engine):
    """Catches: insurer-only filings shown to an intermediary, or its own submission missing."""
    events, undetermined = _calendar(engine, "irdai.intermediary")
    assert events == INTERMEDIARY and len(events) == 17
    assert undetermined == []


def test_no_irdai_event_for_an_nbfc(engine):
    """Catches: IRDAI periodic duties leaking to an entity IRDAI does not regulate."""
    events, _ = _calendar(engine, "nbfc.middle_layer")
    assert events == {}


def test_retention_and_closure_limits_are_not_calendar_events(engine):
    """Catches: a retention period or a limit that runs from a report exported as a due date."""
    events, _ = _calendar(engine, "irdai.insurer")
    assert NOT_RECURRING.isdisjoint(events)
    for name in NOT_RECURRING:
        deadline = engine.get_obligation(P + name)["normalized"]["deadline"]
        assert deadline["kind"] in ("retention", "none")


def test_audit_report_says_the_date_is_the_latest_possible(engine):
    """Catches: 29 June presented as the due date although the clause takes the earlier limit."""
    record = engine.get_obligation(P + "insurer-audit-report-to-irdai")
    action = record["normalized"]["action"]
    assert "29 June" in action and "latest" in action and "30 days" in action
    assert record["normalized"]["recipient"] == "IRDAI"
    assert record["normalized"]["deadline"]["fixed_schedule"] == ["06-29"]
    assert "whichever is earlier" in " ".join(record["text_verbatim"].split())


def test_should_duties_do_not_claim_to_be_mandatory(engine):
    """Catches: a clause that says 'should' rewritten as a must."""
    for name in ("external-pt-half-yearly", "vapt-high-risk-closure-1m"):
        record = engine.get_obligation(P + name)
        assert "should" in record["text_verbatim"]
        action = record["normalized"]["action"].lower()
        assert "should" in action and "must" not in action and "shall" not in action


def test_periodic_duties_add_no_deadline_and_no_question(engine):
    """Catches: a periodic duty producing an incident deadline or a question."""
    result = engine.evaluate(
        IncidentProfile(
            entity_classes=["irdai.insurer"],
            incident_types=["Malicious code attacks such as Ransomware"],
            when_noticed=datetime(2026, 10, 1, 10, 0, tzinfo=IST),
        )
    )
    assert {d.obligation_id for d in result.deadlines} == {
        "cert-in.directions-70b.2022.incident-reporting-6h",
        P + "incident-reporting-6h",
    }
    assert result.unknowns == []
    assert {P + name for name in INSURER} <= set(result.applicable_obligations)


def _mutated(engine: IncidentClockEngine, name: str) -> dict:
    engine.obligations = copy.deepcopy(engine.obligations)
    return next(item for item in engine.obligations if item["id"] == P + name)


def test_mutation_restoration_test_made_yearly_is_caught(engine):
    """Mutation: the six-month restoration test recorded as twelve months changes the label."""
    _mutated(engine, "restoration-test-half-yearly")["normalized"]["deadline"][
        "duration_iso8601"
    ] = "P12M"
    events, _ = _calendar(engine, "irdai.insurer")
    assert events != INSURER and events["restoration-test-half-yearly"] == "20270401"


def test_mutation_audit_report_date_moved_is_caught(engine):
    """Mutation: the audit report date moved off 29 June changes the label."""
    _mutated(engine, "insurer-audit-report-to-irdai")["normalized"]["deadline"][
        "fixed_schedule"
    ] = ["06-30"]
    events, _ = _calendar(engine, "irdai.insurer")
    assert events != INSURER


def test_mutation_insurer_report_leaking_to_intermediaries_is_caught(engine):
    """Mutation: the insurer-only audit report given to intermediaries changes the label."""
    _mutated(engine, "insurer-audit-report-to-irdai")["applicability"]["entity_classes"].append(
        "irdai.intermediary"
    )
    events, _ = _calendar(engine, "irdai.intermediary")
    assert events != INTERMEDIARY
