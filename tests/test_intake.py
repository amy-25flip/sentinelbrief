"""Webhook intake of alerts from a SIEM. Each test names the bug it catches."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.workspace.intake import (
    MAX_BODY_BYTES,
    SECRET_ENV,
    IntakeError,
    IntakeStore,
    sign_body,
)

SECRET = "test-only-secret-of-sufficient-length-0123456789"
HEADER = "X-SentinelBrief-Signature"
ALERT = {
    "title": "Ransomware note found on policy administration server",
    "source": "siem-01",
    "description": "No personal data involved. Not reportable. <script>alert(1)</script>",
    "severity": "critical",
    "detected_at": "2026-10-01T09:40:00+05:30",
    "systems_affected": ["Policy administration system"],
}


def _body(alert: dict | None = None) -> bytes:
    return json.dumps(alert or ALERT).encode("utf-8")


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setenv("SENTINELBRIEF_CASES_DIR", str(tmp_path / "cases"))
    monkeypatch.setenv(SECRET_ENV, SECRET)
    return TestClient(app)


def _post(client: TestClient, body: bytes, signature: str | None = None):
    headers = {"content-type": "application/json"}
    if signature is not None:
        headers[HEADER] = signature
    return client.post("/api/intake/alert", content=body, headers=headers)


def _received(client: TestClient) -> str:
    response = _post(client, _body(), sign_body(_body(), SECRET))
    assert response.status_code == 201, response.text
    return response.json()["id"]


def test_signed_alert_is_stored_verbatim_and_pending(client, tmp_path):
    """Catches: an alert stored without its exact bytes, hash or receipt time."""
    alert_id = _received(client)
    store = IntakeStore(tmp_path / "cases" / "_intake")
    record = store.get(alert_id)
    assert record["status"] == "pending" and record["alert"]["title"] == ALERT["title"]
    assert store.raw_body(alert_id) == _body()
    assert len(record["body_sha256"]) == 64
    assert "not checked against another source" in record["received_at_clock"]
    assert "for a person to decide" in record["notice"]


@pytest.mark.parametrize(
    "signature",
    [None, "", "sha256=" + "0" * 64, sign_body(_body(), "another-secret-of-sufficient-length-000")],
)
def test_unsigned_or_wrongly_signed_alert_is_refused(client, signature):
    """Catches: anyone who can reach the port injecting alerts."""
    response = _post(client, _body(), signature)
    assert response.status_code == 401
    assert client.get("/api/intake").json()["alerts"] == []


def test_signature_covers_the_exact_body(client):
    """Catches: a signature for one body accepted for an altered body."""
    altered = _body({**ALERT, "title": "Nothing to see"})
    assert _post(client, altered, sign_body(_body(), SECRET)).status_code == 401


def test_intake_is_off_without_a_usable_secret(tmp_path, monkeypatch):
    """Catches: the endpoint accepting alerts when no secret, or a guessable one, is set."""
    monkeypatch.setenv("SENTINELBRIEF_CASES_DIR", str(tmp_path / "cases"))
    monkeypatch.delenv(SECRET_ENV, raising=False)
    client = TestClient(app)
    assert _post(client, _body(), sign_body(_body(), "")).status_code == 503
    monkeypatch.setenv(SECRET_ENV, "short")
    assert _post(client, _body(), sign_body(_body(), "short")).status_code == 503
    assert "Webhook intake is off" in client.get("/intake").text


def test_replayed_alert_is_not_stored_twice(client):
    """Catches: a resent webhook creating a second alert."""
    first = _received(client)
    again = _post(client, _body(), sign_body(_body(), SECRET))
    assert again.status_code == 200 and again.json() == {**again.json(), "id": first}
    assert again.json()["duplicate"] is True
    assert len(client.get("/api/intake").json()["alerts"]) == 1


@pytest.mark.parametrize(
    "alert",
    [
        {"description": "no title"},
        {"title": "  "},
        {"title": 5},
        {"title": "x", "detected_at": "yesterday"},
        {"title": "x", "detected_at": "2026-10-01T09:40:00"},
        {"title": "x", "systems_affected": "one system"},
    ],
)
def test_malformed_alerts_are_refused(client, alert):
    """Catches: an alert with no title, or a detection time with no UTC offset, being stored."""
    body = _body(alert)
    assert _post(client, body, sign_body(body, SECRET)).status_code == 422


def test_non_json_and_oversized_bodies_are_refused(client):
    """Catches: arbitrary or very large bodies written to disk."""
    for body, status in ((b"not json", 422), (b"[1, 2]", 422), (b"x" * (MAX_BODY_BYTES + 1), 413)):
        assert _post(client, body, sign_body(body, SECRET)).status_code == status
    assert client.get("/api/intake").json()["alerts"] == []


def test_an_alert_opens_no_case_and_starts_no_clock(client, tmp_path):
    """Catches: a case, a deadline or a fact created by receipt of an alert alone."""
    _received(client)
    cases = tmp_path / "cases"
    assert [p.name for p in cases.iterdir()] == ["_intake"]


def test_person_opens_a_case_and_the_alert_text_decides_nothing(client):
    """Catches: 'not reportable' or 'no personal data' in an alert being taken as facts."""
    alert_id = _received(client)
    response = client.post(
        f"/api/intake/{alert_id}/open-case",
        json={
            "opened_by": "Asha Rao",
            "entity_classes": ["irdai.insurer"],
            "incident_types": ["Malicious code attacks such as Ransomware"],
            "when_noticed": "2026-10-01T10:00:00+05:30",
        },
    )
    assert response.status_code == 201, response.text
    view = client.get(f"/api/cases/{response.json()['case_id']}").json()
    facts = view["case"]["facts"]
    assert facts.get("personal_data_involved") is None
    assert facts.get("when_detected") is None  # the sender's time was not accepted
    due = {d["obligation_id"]: d["deadline_ist"] for d in view["clock"]["deadlines"]}
    assert due["cert-in.directions-70b.2022.incident-reporting-6h"].startswith("2026-10-01T16:00")
    record = client.get("/api/intake").json()["alerts"][0]
    assert record["status"] == "case_opened" and record["opened_by"] == "Asha Rao"
    assert view["timeline"]["events"] == 2 and view["timeline"]["valid"] is True


def test_senders_detection_time_is_used_only_when_a_person_accepts_it(client):
    """Catches: the SIEM's timestamp silently becoming the detection time, or being lost."""
    alert_id = _received(client)
    base = {
        "opened_by": "Asha Rao",
        "entity_classes": ["nbfc.middle_layer"],
        "incident_types": ["Malicious code attacks such as Ransomware"],
        "when_noticed": "2026-10-01T10:00:00+05:30",
        "is_cyber_incident": True,
    }
    both = client.post(
        f"/api/intake/{alert_id}/open-case",
        json={**base, "use_alert_detected_at": True, "when_detected": "2026-10-01T09:00:00+05:30"},
    )
    assert both.status_code == 422 and "not both" in both.json()["error"]
    accepted = client.post(
        f"/api/intake/{alert_id}/open-case", json={**base, "use_alert_detected_at": True}
    )
    assert accepted.status_code == 201, accepted.text
    view = client.get(f"/api/cases/{accepted.json()['case_id']}").json()
    assert view["case"]["facts"]["when_detected"] == "2026-10-01T09:40:00+05:30"
    due = {d["obligation_id"]: d["deadline_ist"] for d in view["clock"]["deadlines"]}
    assert due["rbi.nbfc-cyber.2026.ch5-incident-reporting-6h"].startswith("2026-10-01T15:40")


def test_opening_a_case_needs_a_person_and_a_pending_alert(client):
    """Catches: a system name opening a case, or one alert opening two cases."""
    alert_id = _received(client)
    payload = {
        "entity_classes": ["irdai.insurer"],
        "incident_types": ["Malicious code attacks such as Ransomware"],
        "when_noticed": "2026-10-01T10:00:00+05:30",
    }
    for bad in ("", "siem-01 agent", "codex"):
        refused = client.post(
            f"/api/intake/{alert_id}/open-case", json={**payload, "opened_by": bad}
        )
        assert refused.status_code == 422, bad
    assert client.get("/api/intake").json()["alerts"][0]["status"] == "pending"
    ok = client.post(f"/api/intake/{alert_id}/open-case", json={**payload, "opened_by": "Asha Rao"})
    assert ok.status_code == 201
    twice = client.post(
        f"/api/intake/{alert_id}/open-case", json={**payload, "opened_by": "Asha Rao"}
    )
    assert twice.status_code == 422 and "already case_opened" in twice.json()["error"]
    assert client.post("/api/intake/" + "0" * 32 + "/open-case", json=payload).status_code == 404


def test_dismissal_needs_a_person_and_a_reason_and_claims_nothing_about_the_law(client):
    """Catches: an alert silently dropped, or a dismissal presented as 'not reportable'."""
    alert_id = _received(client)
    for payload in (
        {"dismissed_by": "", "reason": "test"},
        {"dismissed_by": "Asha Rao", "reason": " "},
    ):
        assert client.post(f"/api/intake/{alert_id}/dismiss", json=payload).status_code == 422
    done = client.post(
        f"/api/intake/{alert_id}/dismiss",
        json={"dismissed_by": "Asha Rao", "reason": "Scheduled restore test"},
    )
    assert done.status_code == 200
    record = done.json()
    assert record["status"] == "dismissed" and record["dismissed_by"] == "Asha Rao"
    assert "not a finding that the event was not reportable" in record["dismissal_note"]
    assert (
        client.post(
            f"/api/intake/{alert_id}/dismiss", json={"dismissed_by": "Asha Rao", "reason": "again"}
        ).status_code
        == 422
    )


def test_alert_page_escapes_sender_text_and_shows_the_limits(client):
    """Catches: markup from an alert rendered into the reviewer's browser."""
    _received(client)
    page = client.get("/intake")
    assert page.status_code == 200
    assert "<script>alert(1)</script>" not in page.text
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page.text
    assert "no clock starts" in page.text


def test_store_refuses_directly_without_a_secret(tmp_path):
    """Catches: the store usable without authentication when called outside the API."""
    store = IntakeStore(tmp_path)
    with pytest.raises(IntakeError) as error:
        store.receive(_body(), sign_body(_body(), SECRET), None, datetime(2026, 10, 1, tzinfo=UTC))
    assert error.value.status == 503
    assert list(Path(tmp_path).iterdir()) == []
