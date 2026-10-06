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
        "board-quarterly-inputs": "20260701",
        "classification-review-two-yearly": "20280401",
        "assurance-auditor-rotation-three-yearly": "20290401",
    }
)
INSURER = dict(COMMON)
INTERMEDIARY = COMMON | {"intermediary-annexure-iii-to-insurer-annual": "20270401"}
# Left out of the calendar and listed in its notice (Review 16): duties that hang on a
# condition the engine cannot evaluate, and the audit report whose date needs the audit date.
IT_RULES = {"users-informed-of-termination-right-annual", "users-informed-of-rules-annual"}
INSURER_OMITTED = IT_RULES | {"insurer-audit-report-to-irdai", "frb-annexure-vi-year-end"}
NOT_RECURRING = {
    "log-retention-180d",
    "vapt-high-risk-closure-1m",
    "audit-gap-closure-2m",
    "physical-access-revocation-last-working-day",
}


@pytest.fixture
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _blocks(ics: str) -> list[dict[str, str]]:
    unfolded = ics.replace("\r\n ", "")
    return [
        dict(line.split(":", 1) for line in block.split("\r\n") if ":" in line)
        for block in unfolded.split("BEGIN:VEVENT")[1:]
    ]


def _events(ics: str) -> dict[str, str]:
    """Obligation id (without the instrument prefix) -> first due date, IRDAI events only."""
    found: dict[str, str] = {}
    for fields in _blocks(ics):
        obligation_id = fields.get("X-SENTINELBRIEF-OBLIGATION", "")
        if obligation_id.startswith(P):
            assert obligation_id[len(P) :] not in found
            found[obligation_id[len(P) :]] = fields["DTSTART;VALUE=DATE"]
    return found


def _omitted(ics: str) -> set[str]:
    listed: set[str] = set()
    for fields in _blocks(ics):
        for obligation_id in filter(None, fields.get("X-SENTINELBRIEF-OMITTED", "").split(",")):
            listed.add(obligation_id[len(P) :])
    return listed


def _calendar(engine: IncidentClockEngine, cls: str) -> tuple[dict[str, str], list[str]]:
    ics, undetermined = recurring_duties_ics(engine, [cls], LAST_DONE)
    return _events(ics), undetermined


def test_insurer_calendar_is_exactly_the_label(engine):
    """Catches: a missing or extra recurring duty, or a wrong first due date, for an insurer."""
    ics, undetermined = recurring_duties_ics(engine, ["irdai.insurer"], LAST_DONE)
    assert _events(ics) == INSURER and len(INSURER) == 17
    assert _omitted(ics) == INSURER_OMITTED
    assert undetermined == []


def test_intermediary_calendar_is_exactly_the_label(engine):
    """Catches: insurer-only filings shown to an intermediary, or its own submission missing."""
    ics, undetermined = recurring_duties_ics(engine, ["irdai.intermediary"], LAST_DONE)
    assert _events(ics) == INTERMEDIARY and len(INTERMEDIARY) == 18
    assert _omitted(ics) == IT_RULES
    assert undetermined == []


def test_no_irdai_event_for_an_nbfc(engine):
    """Catches: IRDAI periodic duties leaking to an entity IRDAI does not regulate."""
    ics, _ = recurring_duties_ics(engine, ["nbfc.middle_layer"], LAST_DONE)
    assert _events(ics) == {} and _omitted(ics) == set()
    assert "NOT in this calendar" not in ics


def test_conditional_duties_get_no_date_and_the_calendar_says_so(engine):
    """Catches: a Foreign Reinsurance Branch or IT Rules duty dated for every insurer."""
    ics, _ = recurring_duties_ics(engine, ["irdai.insurer"], LAST_DONE)
    notice = next(f for f in _blocks(ics) if "X-SENTINELBRIEF-OMITTED" in f)
    assert "4 duties are NOT in this calendar" in notice["SUMMARY"]
    assert "RRULE" not in notice and notice["DTSTART;VALUE=DATE"] == "20260402"
    text = notice["DESCRIPTION"]
    assert "Foreign Reinsurance Branch" in text and "IT Rules 2021" in text
    assert "give the audit completion date" in text


def test_audit_report_is_dated_only_from_the_audit_date_and_takes_the_earlier_limit(engine):
    """Catches: 29 June shown as the due date when 30 days after the audit comes first."""
    early, _ = recurring_duties_ics(
        engine, ["irdai.insurer"], LAST_DONE, audit_completed=date(2026, 4, 20)
    )
    assert _events(early)["insurer-audit-report-to-irdai"] == "20260520"
    assert "insurer-audit-report-to-irdai" not in _omitted(early)
    block = next(
        f for f in _blocks(early) if f.get("X-SENTINELBRIEF-OBLIGATION", "").endswith("to-irdai")
    )
    assert "RRULE" not in block and "does not repeat" in block["DESCRIPTION"]
    late, _ = recurring_duties_ics(
        engine, ["irdai.insurer"], LAST_DONE, audit_completed=date(2026, 6, 20)
    )
    assert _events(late)["insurer-audit-report-to-irdai"] == "20260629"
    same_day, _ = recurring_duties_ics(
        engine, ["irdai.insurer"], LAST_DONE, audit_completed=date(2026, 5, 30)
    )
    assert _events(same_day)["insurer-audit-report-to-irdai"] == "20260629"


def test_recommended_duties_are_labelled_in_the_calendar_and_on_the_page(engine):
    """Catches: a clause that says 'should' displayed as mandatory."""
    from fastapi.testclient import TestClient

    from sentinelbrief.api.app import app

    ics, _ = recurring_duties_ics(engine, ["irdai.insurer"], LAST_DONE)
    block = next(
        f
        for f in _blocks(ics)
        if f.get("X-SENTINELBRIEF-OBLIGATION", "").endswith("pt-half-yearly")
    )
    assert block["SUMMARY"].startswith("Recommended\\, not mandatory:")
    client = TestClient(app)
    for name in ("external-pt-half-yearly", "vapt-high-risk-closure-1m"):
        page = client.get(f"/obligations/{P}{name}").text
        assert "Recommended: the clause says" in page and ">Mandatory<" not in page
    assert ">Mandatory<" in client.get(f"/obligations/{P}assurance-audit-annual").text
    assert "Recommended (" in client.get("/").text


def test_every_should_only_clause_is_marked_recommended(engine):
    """Catches: a new record whose clause says only 'should' but is shown as mandatory."""
    import re

    exempt = {
        P + "audit-gap-closure-2m"
    }  # "should be based on risk; however, the outer time limit ... is"
    for record in engine.obligations:
        text = " ".join(record["text_verbatim"].split()).lower()
        only_should = re.search(r"\bshould\b", text) and not re.search(
            r"\bshall\b|\bmust\b|\brequired\b|mandat", text
        )
        if only_should and record["id"] not in exempt:
            assert record["normalized"].get("modality") == "recommended", record["id"]
        if record["normalized"].get("modality") == "recommended":
            assert "should" in text, record["id"]


def test_closure_limits_do_not_invent_a_starting_event(engine):
    """Catches: a period said to run from a report when the clause names no starting event."""
    for name in ("vapt-high-risk-closure-1m", "audit-gap-closure-2m"):
        action = engine.get_obligation(P + name)["normalized"]["action"]
        assert "does not say what" in action and "runs from the" not in action


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
    assert record["normalized"]["deadline"]["earlier_of_days_after_event"] == 30
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
    assert {P + name for name in INSURER | dict.fromkeys(INSURER_OMITTED)} <= set(
        result.applicable_obligations
    )


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
    """Mutation: the audit report's fixed date moved off 29 June changes the computed date."""
    _mutated(engine, "insurer-audit-report-to-irdai")["normalized"]["deadline"][
        "fixed_schedule"
    ] = ["07-15"]
    ics, _ = recurring_duties_ics(
        engine, ["irdai.insurer"], LAST_DONE, audit_completed=date(2026, 6, 20)
    )
    assert _events(ics)["insurer-audit-report-to-irdai"] == "20260715"


def test_mutation_dropping_the_earlier_limit_is_caught(engine):
    """Mutation: without the 30-day limit the report becomes a yearly 29 June event again."""
    del _mutated(engine, "insurer-audit-report-to-irdai")["normalized"]["deadline"][
        "earlier_of_days_after_event"
    ]
    ics, _ = recurring_duties_ics(engine, ["irdai.insurer"], LAST_DONE)
    assert _events(ics).get("insurer-audit-report-to-irdai") == "20260629"
    assert _events(ics) != INSURER


def test_mutation_insurer_report_leaking_to_intermediaries_is_caught(engine):
    """Mutation: the insurer-only audit report given to intermediaries changes the label."""
    _mutated(engine, "insurer-audit-report-to-irdai")["applicability"]["entity_classes"].append(
        "irdai.intermediary"
    )
    ics, _ = recurring_duties_ics(engine, ["irdai.intermediary"], LAST_DONE)
    assert _omitted(ics) != IT_RULES and "insurer-audit-report-to-irdai" in _omitted(ics)
