"""Tests for FastAPI endpoints."""

import json
import shutil
from pathlib import Path

from fastapi.testclient import TestClient

from sentinelbrief.api import app as api_app
from sentinelbrief.api.app import app

client = TestClient(app)
REPO = Path(__file__).resolve().parents[1]


def test_api_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_api_obligations():
    response = client.get("/api/obligations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 7


def test_api_instruments():
    response = client.get("/api/instruments")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_html_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "SentinelBrief" in response.text
    assert "Report cybersecurity incidents to CERT-In within 6 hours" in response.text


def test_html_obligations_browser():
    response = client.get("/obligations")
    assert response.status_code == 200
    assert "Obligation Browser" in response.text


def test_html_obligation_detail():
    response = client.get("/obligations/cert-in.directions-70b.2022.incident-reporting-6h")
    assert response.status_code == 200
    assert "Direction (ii)" in response.text
    assert "incident@cert-in.org.in" in response.text


def test_html_obligation_detail_labels_suggested_evidence_as_not_source_text():
    response = client.get("/obligations/cert-in.directions-70b.2022.incident-reporting-6h")
    assert response.status_code == 200
    assert "Suggested evidence (not stated in the source text)" in response.text
    assert "builder-authored suggestions" in response.text
    assert "Evidence Required" not in response.text


def test_html_obligation_detail_not_found():
    response = client.get("/obligations/non-existent-obligation-id")
    assert response.status_code == 404


def test_html_incident_workspace():
    response = client.get("/incident")
    assert response.status_code == 200
    assert "Incident Clock Workspace" in response.text
    assert "Also a (tick all that apply)" in response.text
    assert 'name="also_classes"' in response.text


def _ist(hour):
    return f"2026-09-24T{hour:02d}:00:00+05:30"


def test_incident_clock_json_uses_the_engine():
    r = client.post(
        "/api/incident/clock",
        json={
            "entity_class": "nbfc",
            "incident_types": ["ransomware"],
            "when_noticed": _ist(9),
        },
    )
    assert r.status_code == 200
    data = r.json()
    (dl,) = data["deadlines"]
    assert dl["obligation_id"].endswith("incident-reporting-6h")
    assert dl["deadline_ist"] == "2026-09-24T15:00:00+05:30"
    assert dl["regulator"] == "CERT-In"


def test_incident_clock_json_accepts_multiple_entity_classes():
    r = client.post(
        "/api/incident/clock",
        json={
            "entity_classes": ["sebi.mii", "dpdp.data_fiduciary", "sebi.mii"],
            "incident_types": ["Malicious code attacks such as Ransomware"],
            "personal_data_involved": True,
            "when_noticed": "2027-06-01T10:00:00+05:30",
            "when_aware": "2027-06-01T10:00:00+05:30",
        },
    )
    assert r.status_code == 200
    ids = {item["obligation_id"] for item in r.json()["deadlines"]}
    assert "sebi.cscrf.2024.incident-reporting-6h" in ids
    assert "meity.dpdp-rules.2025.rule7-2-b-board-detailed" in ids


def test_incident_clock_json_accepts_three_state_rbi_cyber_incident():
    base = {
        "entity_class": "nbfc.middle_layer",
        "when_detected": _ist(9),
        "incident_types": ["hardware failure"],
    }
    yes = client.post("/api/incident/clock", json={**base, "is_cyber_incident": True})
    assert yes.status_code == 200
    assert any(
        item["obligation_id"].endswith("ch5-incident-reporting-6h")
        for item in yes.json()["deadlines"]
    )

    no = client.post("/api/incident/clock", json={**base, "is_cyber_incident": False})
    assert no.status_code == 200
    assert any(
        item["reason"] == "condition_not_met: user attested not a cyber incident"
        for item in no.json()["not_applicable"]
    )

    unknown = client.post("/api/incident/clock", json={**base, "is_cyber_incident": None})
    assert unknown.status_code == 200
    assert any("cyber incident" in item["question"].lower() for item in unknown.json()["unknowns"])


def test_incident_clock_form_accepts_rbi_cyber_incident_attestation():
    page = client.get("/incident")
    assert 'name="cyber_incident_attestation"' in page.text
    response = client.post(
        "/api/incident/clock",
        content=(
            "entity_class=nbfc.middle_layer&incident_types=hardware+failure&"
            "when_detected=2026-09-24T09%3A00&cyber_incident_attestation=yes"
        ),
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )
    assert response.status_code == 200
    assert "Report the cyber incident to RBI" in response.text


def test_incident_clock_form_accepts_repeated_also_classes():
    r = client.post(
        "/api/incident/clock",
        content=(
            "entity_class=sebi.mii&also_classes=dpdp.data_fiduciary&"
            "also_classes=sebi.mii&incident_types=ransomware&personal_data_involved=true&"
            "when_noticed=2027-06-01T10%3A00&when_aware=2027-06-01T10%3A00"
        ),
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )
    assert r.status_code == 200
    assert "mkt_incidents@sebi.gov.in" in r.text
    assert "Intimate to the Data Protection Board" in r.text


def test_incident_clock_json_rejects_naive_time():
    r = client.post(
        "/api/incident/clock",
        json={"entity_class": "nbfc", "when_noticed": "2026-09-24T09:00:00"},
    )
    assert r.status_code == 422
    assert "offset" in r.json()["error"]


def test_incident_clock_rejects_unknown_entity_class():
    r = client.post("/api/incident/clock", json={"entity_class": "NBFC"})
    assert r.status_code == 422
    assert "Unknown entity class" in r.json()["error"]


def test_incident_clock_form_reads_times_as_ist_and_renders_fragment():
    r = client.post(
        "/api/incident/clock",
        content="entity_class=nbfc&incident_types=data+breach&when_noticed=2026-09-24T09%3A00",
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )
    assert r.status_code == 200
    assert "24 Sep 2026, 15:00 IST" in r.text
    assert "noticing at 24 Sep 2026, 09:00 IST" in r.text
    assert "Ongoing duties" in r.text


def test_incident_clock_unresolved_type_asks_instead_of_guessing():
    r = client.post(
        "/api/incident/clock",
        content="entity_class=nbfc&incident_types=hardware+failure&when_noticed=2026-09-24T09%3A00",
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )
    assert r.status_code == 200
    assert "Needs your answer" in r.text
    assert "Annexure I" in r.text
    assert "No deadline could be computed" in r.text


def test_incident_clock_fragment_shows_time_critical_duties(monkeypatch, tmp_path):
    data_dir = tmp_path / "data"
    shutil.copytree(REPO / "data", data_dir)
    obligations_path = data_dir / "obligations" / "cert-in.directions-70b.2022.json"
    obligations = json.loads(obligations_path.read_text(encoding="utf-8"))
    immediate = {**obligations[0]}
    immediate["id"] = "mock.immediate-duty"
    immediate["paragraph_ref"] = "Mock immediate"
    immediate["normalized"] = {
        **immediate["normalized"],
        "action": "Notify without delay",
        "recipient": "CERT-In",
        "deadline": {"kind": "immediate", "anchor": "noticing"},
    }
    obligations.append(immediate)
    obligations_path.write_text(json.dumps(obligations, indent=2), encoding="utf-8")
    monkeypatch.setattr(api_app, "DATA_DIR", data_dir)

    r = client.post(
        "/api/incident/clock",
        content="entity_class=nbfc&incident_types=data+breach&when_noticed=2026-09-24T09%3A00",
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )

    assert r.status_code == 200
    assert "Do without delay" in r.text
    assert "Notify without delay" in r.text
    assert "Notify without delay" not in r.text.split("Ongoing duties", 1)[-1]


def test_incident_clock_escapes_user_text():
    r = client.post(
        "/api/incident/clock",
        content="entity_class=<script>alert(1)</script>&when_noticed=2026-09-24T09%3A00",
        headers={"content-type": "application/x-www-form-urlencoded", "hx-request": "true"},
    )
    assert r.status_code == 422
    assert "<script>alert(1)</script>" not in r.text


def test_incident_page_has_no_client_side_clock_logic():
    r = client.get("/incident")
    assert "getTime()" not in r.text and "6 * 60 * 60" not in r.text
    assert 'hx-post="/api/incident/clock"' in r.text


def test_retention_duties_are_not_shown_as_deadlines():
    r = client.get("/obligations/cert-in.directions-70b.2022.log-retention-180d")
    assert r.status_code == 200
    assert "not an incident deadline" in r.text
