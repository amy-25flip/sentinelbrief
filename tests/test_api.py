"""Tests for FastAPI endpoints."""

from fastapi.testclient import TestClient

from sentinelbrief.api.app import app

client = TestClient(app)


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
    assert "Report the cyber incident" in response.text


def test_html_obligations_browser():
    response = client.get("/obligations")
    assert response.status_code == 200
    assert "Obligation Browser" in response.text


def test_html_obligation_detail():
    response = client.get("/obligations/cert-in.directions-70b.2022.incident-reporting-6h")
    assert response.status_code == 200
    assert "Direction (ii)" in response.text
    assert "incident@cert-in.org.in" in response.text


def test_html_obligation_detail_not_found():
    response = client.get("/obligations/non-existent-obligation-id")
    assert response.status_code == 404


def test_html_incident_workspace():
    response = client.get("/incident")
    assert response.status_code == 200
    assert "Incident Clock Workspace" in response.text


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
