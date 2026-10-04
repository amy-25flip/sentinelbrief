"""IRDAI Information and Cyber Security Guidelines, 2023 (docs/LABELS_IRDAI.md).

Each test names the bug it catches in its docstring.
"""

import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.verify.quotes import SourcePages

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2026, 10, 1, 10, 0, tzinfo=IST)
IRDAI = "irdai.ics-guidelines.2023.incident-reporting-6h"
CERT_IN = "cert-in.directions-70b.2022.incident-reporting-6h"
RANSOMWARE = "Malicious code attacks such as Ransomware"


@pytest.fixture(scope="module")
def engine() -> IncidentClockEngine:
    return IncidentClockEngine(REPO / "data")


def _run(engine, classes, **kwargs):
    kwargs.setdefault("incident_types", [RANSOMWARE])
    return engine.evaluate(IncidentProfile(entity_classes=classes, **kwargs))


def _deadlines(result):
    return {d.obligation_id: d for d in result.deadlines}


def test_clause_is_on_the_cited_page_of_the_english_text():
    """Catches: the obligation citing the wrong page of a 305-page bilingual file."""
    pages = SourcePages(REPO / "data")
    pages.require_quote(
        "irdai.ics-guidelines.2023",
        224,
        "report cyber incidents to Cert-In within 6 hours of noticing",
    )
    assert "Page 94 of 175" in pages.page_text("irdai.ics-guidelines.2023", 224)


def test_insurers_and_intermediaries_owe_the_duty_and_others_do_not(engine):
    """Catches: the IRDAI duty missing for an intermediary, or leaking to another sector."""
    for cls in ("irdai.insurer", "irdai.intermediary"):
        deadline = _deadlines(_run(engine, [cls], when_noticed=T10))[IRDAI]
        assert deadline.deadline_ist == T10 + timedelta(hours=6) and deadline.regulator == "IRDAI"
        assert "copy to IRDAI" in deadline.recipient
    for cls in ("bank.payments_bank", "nbfc.middle_layer", "sebi.mii", "aifi"):
        result = _run(engine, [cls], when_noticed=T10, when_detected=T10)
        assert IRDAI in {n["obligation_id"] for n in result.not_applicable}, cls
        assert not any(IRDAI in u.affects for u in result.unknowns), cls


def test_clock_runs_from_noticing_or_brought_to_notice_not_detection(engine):
    """Catches: a detection time starting a clock the text ties to noticing."""
    detected_only = _run(engine, ["irdai.insurer"], when_detected=T10)
    assert IRDAI not in _deadlines(detected_only)
    assert any(IRDAI in u.affects and "noticed" in u.question for u in detected_only.unknowns)
    brought = _run(
        engine, ["irdai.insurer"], when_brought_to_notice=T10 - timedelta(hours=1), when_noticed=T10
    )
    assert _deadlines(brought)[IRDAI].anchor_type == "brought_to_notice"


def test_cyber_incident_gate_states(engine):
    """Catches: the wider IRDAI wording collapsed into the Annexure I gate, or guessed from text."""
    hardware = {"incident_types": ["hardware failure"], "when_noticed": T10}
    unknown = _run(engine, ["irdai.insurer"], **hardware)
    asked = next(u for u in unknown.unknowns if IRDAI in u.affects)
    assert "cyber incident" in asked.question and "Policy 2.10" in asked.question
    wider = _run(
        engine, ["irdai.insurer"], is_annexure_i_type=False, is_cyber_incident=True, **hardware
    )
    assert set(_deadlines(wider)) == {IRDAI}
    neither = _run(
        engine, ["irdai.insurer"], is_annexure_i_type=False, is_cyber_incident=False, **hardware
    )
    assert not neither.deadlines and not neither.unknowns


def test_not_in_force_before_24_april_2023(engine):
    """Catches: the guidelines applied to an incident that predates them."""
    for day, expected in ((23, False), (24, True)):
        when = datetime(2023, 4, day, 10, 0, tzinfo=IST)
        assert (IRDAI in _deadlines(_run(engine, ["irdai.insurer"], when_noticed=when))) is expected
        assert CERT_IN in _deadlines(_run(engine, ["irdai.insurer"], when_noticed=when))


def test_reverify_exemption_covers_irdai_and_still_rejects_other_hosts(tmp_path):
    """Catches: the robots-blocked host failing reverify, or the exemption opened to any host."""
    spec = importlib.util.spec_from_file_location(
        "reverify_sources", REPO / "scripts" / "reverify_sources.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["reverify_sources"] = module
    spec.loader.exec_module(module)
    base = {
        "filename": "x.pdf",
        "sha256": "0" * 64,
        "reverify_exemption": "robots.txt disallows automated access",
    }
    ok = module.compare_entry(
        {**base, "url": "https://irdai.gov.in/document-detail?documentId=1"}, tmp_path
    )
    assert ok.ok and ok.skipped
    bad = module.compare_entry({**base, "url": "https://example.org/x.pdf"}, tmp_path)
    assert not bad.ok and "only allowed" in bad.message
    lookalike = module.compare_entry(
        {**base, "url": "https://irdai.gov.in.example.org/x.pdf"}, tmp_path
    )
    assert not lookalike.ok
