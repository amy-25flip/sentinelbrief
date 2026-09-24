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
