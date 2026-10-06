"""Tabletop exercise generator. Each test names the bug it catches."""

import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.workspace import tabletop
from sentinelbrief.workspace.tabletop import SCENARIOS, build_tabletop, render_markdown

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
START = datetime(2026, 10, 1, 9, 0, tzinfo=IST)
CERT_IN = "cert-in.directions-70b.2022.incident-reporting-6h"
RBI = "rbi.nbfc-cyber.2026.ch5-incident-reporting-6h"
IRDAI = "irdai.ics-guidelines.2023.incident-reporting-6h"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _due(stage: dict) -> dict[str, str]:
    return {d["obligation_id"]: d["due_ist"] for d in stage["answer_key"]["deadlines"]}


def test_detection_alone_starts_no_clock_and_lists_what_to_ask(engine):
    """Catches: an automated alert treated as noticing, or a stage with no questions."""
    stages = build_tabletop(engine, ["nbfc.middle_layer"], "ransomware-with-personal-data", START)[
        "stages"
    ]
    first = stages[0]
    assert first["answer_key"]["deadlines"] == []
    questions = [q["question"] for q in first["answer_key"]["open_questions"]]
    assert any("Annexure I" in q for q in questions)
    assert len(questions) == len(set(questions))  # one question is asked once


def test_two_regulators_get_two_clocks_from_two_starting_events(engine):
    """Catches: RBI and CERT-In collapsed onto one starting event."""
    stages = build_tabletop(engine, ["nbfc.middle_layer"], "ransomware-with-personal-data", START)[
        "stages"
    ]
    second = stages[1]
    assert _due(second) == {
        RBI: "2026-10-01T15:00:00+05:30",  # six hours from detection at 09:00
        CERT_IN: "2026-10-01T15:25:00+05:30",  # six hours from noticing at 09:25
    }
    starts = {d["obligation_id"]: d["starts_from"] for d in second["answer_key"]["deadlines"]}
    assert starts == {RBI: "detection", CERT_IN: "noticing"}
    assert sorted(second["clocks_started_at_this_stage"]) == sorted([RBI, CERT_IN])
    assert stages[2]["clocks_started_at_this_stage"] == []


def test_answer_key_is_exactly_what_the_engine_says_for_the_facts_so_far(engine):
    """Catches: any deadline, clause or question in the key that the engine did not produce."""
    for scenario in SCENARIOS:
        for classes in (["nbfc.middle_layer"], ["irdai.insurer"], ["sebi.stock_broker"]):
            exercise = build_tabletop(engine, classes, scenario.id, START)
            facts: dict = {}
            for stage, built in zip(scenario.stages, exercise["stages"], strict=True):
                for name, value in stage.reveals.items():
                    facts[name] = (
                        START + timedelta(minutes=int(value[1:]))
                        if isinstance(value, str) and value.startswith("+")
                        else value
                    )
                at = START + timedelta(minutes=stage.minutes)
                result = engine.evaluate(IncidentProfile(entity_classes=classes, **facts), now=at)
                assert _due(built) == {
                    d.obligation_id: d.deadline_ist.isoformat() for d in result.deadlines
                }
                assert {q["question"] for q in built["answer_key"]["open_questions"]} == {
                    u.question for u in result.unknowns
                }
                clauses = {
                    d.obligation_id: f"{d.citation_instrument} {d.citation_paragraph}"
                    for d in result.deadlines
                }
                for item in built["answer_key"]["deadlines"]:
                    obligation = engine.get_obligation(item["obligation_id"])
                    assert item["clause"] == clauses[item["obligation_id"]]
                    assert item["clause"].startswith(obligation["instrument_id"] + " ")


def test_hardware_failure_storyline_never_produces_a_deadline(engine):
    """Catches: an outage reported as a cyber incident before anyone has attested it."""
    for classes in (["nbfc.middle_layer"], ["irdai.insurer"]):
        stages = build_tabletop(engine, classes, "unclear-outage", START)["stages"]
        assert all(stage["answer_key"]["deadlines"] == [] for stage in stages)
        assert (
            stages[0]["answer_key"]["open_questions"] and stages[1]["answer_key"]["open_questions"]
        )
        assert stages[-1]["answer_key"]["open_questions"] == []


def test_dpdp_is_shown_as_not_in_force_unless_simulated(engine):
    """Catches: DPDP Rule 7 taught as a live duty in 2026, or a simulation not labelled."""
    classes = ["nbfc.middle_layer", "dpdp.data_fiduciary"]
    plain = build_tabletop(engine, classes, "ransomware-with-personal-data", START)
    last = plain["stages"][-1]
    assert all("dpdp" not in key for key in _due(last))
    assert any("dpdp" in item for item in last["answer_key"]["not_in_force_at_this_date"])
    assert "Not in force at this date" in render_markdown(plain)

    simulated = build_tabletop(
        engine, classes, "ransomware-with-personal-data", START, ["meity.dpdp-rules.2025"]
    )
    rows = [
        d
        for d in simulated["stages"][-1]["answer_key"]["deadlines"]
        if "dpdp" in d["obligation_id"]
    ]
    assert rows and all(row["simulated"] for row in rows)
    assert simulated["simulated_instruments"] == ["meity.dpdp-rules.2025"]
    assert any(
        c.startswith("SIMULATION:") for c in simulated["stages"][-1]["answer_key"]["caveats"]
    )
    assert "(simulated, not in force)" in render_markdown(simulated)


def test_build_is_deterministic_and_says_what_it_is(engine):
    """Catches: output that changes between runs, or a hand-out without the disclaimer."""
    one = build_tabletop(engine, ["irdai.insurer"], "website-defacement-no-personal-data", START)
    two = build_tabletop(engine, ["irdai.insurer"], "website-defacement-no-personal-data", START)
    assert json.dumps(one, sort_keys=True) == json.dumps(two, sort_keys=True)
    text = render_markdown(one)
    assert text == render_markdown(two)
    assert "The storyline is invented" in text and "not legal advice" in text
    assert text.count("**Read out (fiction):**") == len(one["stages"])


def test_bad_inputs_are_refused(engine):
    """Catches: a naive start time read silently, or an unknown storyline or class accepted."""
    with pytest.raises(ValueError, match="UTC offset"):
        build_tabletop(engine, ["irdai.insurer"], "unclear-outage", datetime(2026, 10, 1, 9, 0))
    with pytest.raises(KeyError):
        build_tabletop(engine, ["irdai.insurer"], "no-such-storyline", START)
    with pytest.raises(ValueError):
        build_tabletop(engine, [], "unclear-outage", START)
    with pytest.raises(ValueError):
        build_tabletop(engine, ["no.such.class"], "unclear-outage", START)


def test_mutation_storyline_that_states_law_would_not_reach_the_key(engine, monkeypatch):
    """Mutation: changing only the fiction changes no deadline; changing a fact does."""
    original = SCENARIOS[0]
    reworded = replace(
        original,
        stages=tuple(
            replace(s, inject="CERT-In must be told within 1 hour.") for s in original.stages
        ),
    )
    monkeypatch.setattr(tabletop, "SCENARIOS", (reworded, *SCENARIOS[1:]))
    changed_story = build_tabletop(engine, ["nbfc.middle_layer"], original.id, START)
    assert _due(changed_story["stages"][1])[CERT_IN] == "2026-10-01T15:25:00+05:30"

    later = replace(
        original,
        stages=(
            original.stages[0],
            replace(
                original.stages[1], reveals={**original.stages[1].reveals, "when_noticed": "+60"}
            ),
            *original.stages[2:],
        ),
    )
    monkeypatch.setattr(tabletop, "SCENARIOS", (later, *SCENARIOS[1:]))
    changed_fact = build_tabletop(engine, ["nbfc.middle_layer"], original.id, START)
    assert _due(changed_fact["stages"][1])[CERT_IN] == "2026-10-01T16:00:00+05:30"


def test_api_json_markdown_and_page():
    """Catches: endpoints that disagree with the builder, or sender-controlled text unescaped."""
    client = TestClient(app)
    query = {
        "classes": "irdai.insurer",
        "scenario": "ransomware-with-personal-data",
        "start": "2026-10-01T09:00:00+05:30",
    }
    body = client.get("/api/tabletop", params=query)
    assert body.status_code == 200
    second = body.json()["stages"][1]
    assert _due(second) == {
        CERT_IN: "2026-10-01T15:25:00+05:30",
        IRDAI: "2026-10-01T15:25:00+05:30",
    }
    hand_out = client.get("/api/tabletop.md", params=query)
    assert hand_out.status_code == 200 and hand_out.text.startswith("# Tabletop exercise:")
    assert "attachment" in hand_out.headers["content-disposition"]
    page = client.get("/tabletop", params={**query, "start": "2026-10-01T09:00"})  # typed as IST
    assert page.status_code == 200 and "2026-10-01T15:25:00+05:30" in page.text
    assert "Read out (fiction)" in page.text and "The storyline is invented" in page.text
    assert client.get("/tabletop").status_code == 200
    for bad in (
        {**query, "scenario": "nope"},
        {**query, "classes": ""},
        {**query, "start": ""},
        {**query, "classes": "<script>alert(1)</script>"},
    ):
        assert client.get("/api/tabletop", params=bad).status_code == 422
    hostile = client.get("/tabletop", params={**query, "classes": "<script>alert(1)</script>"})
    assert hostile.status_code == 422 and "<script>alert(1)</script>" not in hostile.text
