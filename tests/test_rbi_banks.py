"""RBI Directions for UCBs, AIFIs and Payments Banks (docs/LABELS_RBI_BANKS.md).

Each test names the bug it catches in its docstring.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2026, 10, 1, 10, 0, tzinfo=IST)
UCB, AIFI, PB = "rbi.ucb-cyber.2026.", "rbi.aifi-cyber.2026.", "rbi.payments-banks-cyber.2026."
REP, NOTIFY, VA, PT = "incident-reporting-6h", "cert-in-notification", "va-half-yearly", "pt-annual"
RANSOMWARE = "Malicious code attacks such as Ransomware"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _run(engine, classes, **kwargs):
    kwargs.setdefault("incident_types", [RANSOMWARE])
    kwargs.setdefault("when_detected", T10)
    kwargs.setdefault("when_noticed", T10)
    return engine.evaluate(IncidentProfile(entity_classes=classes, **kwargs))


def _deadlines(result):
    return {d.obligation_id: d for d in result.deadlines}


def _not_applicable(result):
    return {n["obligation_id"] for n in result.not_applicable}


def test_refinement_question_wording_comes_from_the_data(engine):
    """Catches: every coarse class being asked 'What is the NBFC category?'."""
    questions = {
        cls: next(u.question for u in _run(engine, [cls]).unknowns if "Choose one of" in u.question)
        for cls in ("nbfc", "ucb", "bank")
    }
    assert questions["nbfc"].startswith("What is the NBFC category?")
    assert questions["ucb"].startswith("What is the UCB level?")
    assert questions["bank"].startswith("What kind of bank is it?")
    assert "NBFC" not in questions["ucb"] + questions["bank"]


def test_every_ucb_reports_whatever_its_level(engine):
    """Catches: the Chapter III reporting duty withheld from a UCB whose level is unknown."""
    for cls in ("ucb", "ucb.level_i", "ucb.level_ii", "ucb.level_iii", "ucb.level_iv"):
        result = _run(engine, [cls])
        assert _deadlines(result)[UCB + REP].deadline_ist == T10 + timedelta(hours=6), cls
        assert UCB + NOTIFY in result.applicable_obligations, cls
        assert not any(UCB + REP in u.affects for u in result.unknowns), cls


def test_ucb_va_and_pt_follow_the_level(engine):
    """Catches: the Chapter IV cadence applied to Level I, or dropped for an unknown level."""
    level_i = _run(engine, ["ucb.level_i"])
    assert {UCB + VA, UCB + PT} <= _not_applicable(level_i)
    for cls in ("ucb.level_ii", "ucb.level_iii", "ucb.level_iv"):
        assert {UCB + VA, UCB + PT} <= set(_run(engine, [cls]).applicable_obligations), cls
    bare = _run(engine, ["ucb"])
    assert {UCB + VA, UCB + PT} <= set(bare.undetermined)
    asked = next(u for u in bare.unknowns if "UCB level" in u.question)
    assert sorted(asked.affects) == sorted([UCB + VA, UCB + PT])


def test_generic_bank_is_asked_and_told_the_coverage_gap(engine):
    """Catches: a bank of unstated kind told that no RBI duty applies."""
    result = _run(engine, ["bank"])
    four = {PB + x for x in (REP, NOTIFY, VA, PT)}
    assert four <= set(result.undetermined) and not four & _not_applicable(result)
    asked = next(u for u in result.unknowns if "kind of bank" in u.question)
    assert set(asked.affects) == four
    assert "not covered" in asked.impact and "Payments Banks" in asked.impact
    assert PB + REP in _deadlines(_run(engine, ["bank.payments_bank"]))
    assert not _run(engine, ["bank.payments_bank"]).unknowns


def test_aifi_duties(engine):
    """Catches: an AIFI duty missing, or the untimed CERT-In notification given a clock."""
    result = _run(engine, ["aifi"])
    assert _deadlines(result)[AIFI + REP].anchor_type == "detection"
    assert {AIFI + NOTIFY, AIFI + VA, AIFI + PT} <= set(result.applicable_obligations)
    assert AIFI + NOTIFY not in _deadlines(result)
    assert AIFI + NOTIFY not in {t.obligation_id for t in result.time_critical}


def test_directions_do_not_cross_entity_types(engine):
    """Catches: one entity type shown another type's Direction."""
    owners = {
        "ucb.level_iv": UCB,
        "aifi": AIFI,
        "bank.payments_bank": PB,
        "nbfc.middle_layer": "rbi.nbfc-cyber.2026.",
    }
    for cls, own in owners.items():
        result = _run(engine, [cls])
        shown = (
            set(result.applicable_obligations) | set(result.undetermined) | set(_deadlines(result))
        )
        foreign = {o for o in shown if o.startswith("rbi.") and not o.startswith(own)}
        assert foreign == set(), (cls, foreign)


def test_commencement_boundary(engine):
    """Catches: the three Directions applied to incidents before 31 July 2026."""
    before = datetime(2026, 7, 30, 23, 30, tzinfo=IST)
    on = datetime(2026, 7, 31, 0, 30, tzinfo=IST)
    for cls, prefix in (("ucb.level_ii", UCB), ("aifi", AIFI), ("bank.payments_bank", PB)):
        early = _run(engine, [cls], when_detected=before, when_noticed=before)
        assert {prefix + x for x in (REP, NOTIFY, VA, PT)} <= _not_applicable(early), cls
        late = _run(engine, [cls], when_detected=on, when_noticed=on)
        assert prefix + REP in _deadlines(late), cls


def test_a_class_that_needs_refinement_must_carry_a_question(tmp_path):
    """Catches: a coarse class added to the taxonomy with no question, failing silently."""
    import json
    import shutil

    data = tmp_path / "data"
    shutil.copytree(REPO / "data", data, ignore=shutil.ignore_patterns("raw"))
    path = data / "entities" / "rbi.json"
    entities = json.loads(path.read_text(encoding="utf-8"))
    for item in entities:
        if item["id"] == "ucb":
            del item["refinement_question"]
    path.write_text(json.dumps(entities), encoding="utf-8")
    with pytest.raises(ValueError, match="no refinement_question"):
        _run(IncidentClockEngine(data), ["ucb"])
