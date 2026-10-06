"""DPDP Rule 7 simulation remains visibly separate from enforceable duties."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.workspace import CaseStore, build_drafts, load_filing_content

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
IST = timezone(timedelta(hours=5, minutes=30))
INSTRUMENT = "meity.dpdp-rules.2025"
DETAILED = f"{INSTRUMENT}.rule7-2-b-board-detailed"
SIMULATED_IDS = {
    f"{INSTRUMENT}.rule7-1-principal-intimation",
    f"{INSTRUMENT}.rule7-2-a-board-initial",
    DETAILED,
}


def _profile(day: int = 1) -> IncidentProfile:
    noticed = datetime(2026, 10, day, 10, 0, tzinfo=IST)
    return IncidentProfile(
        entity_classes=["dpdp.data_fiduciary"],
        incident_types=["Data breach"],
        when_noticed=noticed,
        when_aware=noticed + timedelta(hours=1),
        personal_data_involved=True,
    )


def test_simulated_outputs_are_not_real_or_pending():
    """Catches a simulated deadline reported with status pending or counted as applicable."""
    result = IncidentClockEngine(DATA).evaluate(_profile(), simulate_instruments=[INSTRUMENT])
    assert set(result.simulated_obligations) == SIMULATED_IDS
    assert not SIMULATED_IDS & set(result.applicable_obligations)
    detailed = next(d for d in result.deadlines if d.obligation_id == DETAILED)
    assert detailed.simulated is True and detailed.status == "simulated"
    assert all(t.simulated for t in result.time_critical if t.obligation_id in SIMULATED_IDS)


def test_simulation_after_commencement_is_refused():
    """Catches simulation being applied to obligations already in force."""
    noticed = datetime(2027, 6, 1, 10, 0, tzinfo=IST)
    profile = replace(_profile(), when_noticed=noticed, when_aware=noticed)
    with pytest.raises(ValueError, match="Nothing to simulate"):
        IncidentClockEngine(DATA).evaluate(profile, simulate_instruments=[INSTRUMENT])


def test_mutation_already_in_force_obligation_becoming_simulated_is_caught():
    """`test_simulation_after_commencement_is_refused` catches a later fake validity date."""
    engine = IncidentClockEngine(DATA)
    for obligation in engine.obligations:
        if obligation["id"].startswith(INSTRUMENT + ".rule7"):
            obligation["validity"]["valid_from"] = "2028-05-13"
    noticed = datetime(2027, 6, 1, 10, 0, tzinfo=IST)
    profile = replace(_profile(), when_noticed=noticed, when_aware=noticed)
    mutated = engine.evaluate(profile, simulate_instruments=[INSTRUMENT])
    assert mutated.simulated_obligations


def test_non_fiduciary_gets_no_simulated_dpdp_duty():
    """The fourth label row keeps the entity gate even under simulation."""
    result = IncidentClockEngine(DATA).evaluate(
        IncidentProfile(
            entity_classes=["nbfc.middle_layer"],
            incident_types=["Data breach"],
            when_detected=datetime(2026, 10, 1, 10, 0, tzinfo=IST),
            when_noticed=datetime(2026, 10, 1, 10, 0, tzinfo=IST),
            personal_data_involved=True,
        ),
        simulate_instruments=[INSTRUMENT],
    )
    assert result.simulated_obligations == []
    assert not any(d.obligation_id.startswith(INSTRUMENT) for d in result.deadlines)


def test_workspace_refuses_simulation_and_builds_no_simulated_draft(tmp_path):
    """Catches a case opening with simulation or a simulated duty becoming a draft."""
    engine = IncidentClockEngine(DATA)
    result = engine.evaluate(_profile(), simulate_instruments=[INSTRUMENT])
    drafts = build_drafts(engine, result, load_filing_content(DATA))
    assert not SIMULATED_IDS & {draft.obligation_id for draft in drafts}
    with pytest.raises(ValueError, match="cannot be opened with a simulation"):
        CaseStore(tmp_path / "cases", DATA).create(
            _profile(), "Asha Rao", simulate_instruments=[INSTRUMENT]
        )


def test_api_and_page_keep_simulation_visibly_separate():
    client = TestClient(app)
    payload = {
        "entity_classes": ["dpdp.data_fiduciary"],
        "incident_types": ["Data breach"],
        "when_noticed": "2026-10-01T10:00:00+05:30",
        "when_aware": "2026-10-01T11:00:00+05:30",
        "personal_data_involved": True,
        "simulate_instruments": [INSTRUMENT],
    }
    response = client.post("/api/incident/clock", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert set(body["simulated_obligations"]) == SIMULATED_IDS
    assert "not in force" in next(c for c in body["caveats"] if c.startswith("SIMULATION:"))
    form = client.post(
        "/api/incident/clock",
        data={
            "entity_class": "dpdp.data_fiduciary",
            "incident_types": "Data breach",
            "when_noticed": "2026-10-01T10:00",
            "when_aware": "2026-10-01T11:00",
            "personal_data_involved": "true",
            "simulate_instruments": INSTRUMENT,
        },
        headers={"hx-request": "true"},
    )
    assert "Simulation — not in force" in form.text
    assert "Simulate DPDP Rule 7 as if in force" in client.get("/incident").text
