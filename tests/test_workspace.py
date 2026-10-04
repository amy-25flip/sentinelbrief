"""Incident workspace: drafts, human approval, audit bundle, calendar export.

Each test names the bug it catches in its docstring.
"""

import hashlib
import io
import json
import zipfile
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile
from sentinelbrief.verify.quotes import SourcePages
from sentinelbrief.workspace import (
    CaseStore,
    build_drafts,
    load_filing_content,
    recurring_duties_ics,
)
from sentinelbrief.workspace.cases import facts_to_profile, profile_to_facts

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
IST = timezone(timedelta(hours=5, minutes=30))
T10 = datetime(2027, 6, 1, 10, 0, tzinfo=IST)
RANSOMWARE = "Malicious code attacks such as Ransomware"
CERT_6H = "cert-in.directions-70b.2022.incident-reporting-6h"
RBI_6H = "rbi.nbfc-cyber.2026.ch5-incident-reporting-6h"
DPDP_72H = "meity.dpdp-rules.2025.rule7-2-b-board-detailed"
DPDP_PRINCIPAL = "meity.dpdp-rules.2025.rule7-1-principal-intimation"
RBI_CERT_IN = "rbi.nbfc-cyber.2026.ch5-cert-in-notification"


def _profile(**overrides) -> IncidentProfile:
    kwargs = {
        "entity_classes": ["nbfc.middle_layer", "dpdp.data_fiduciary"],
        "incident_types": [RANSOMWARE, "Data breach"],
        "when_detected": T10 - timedelta(hours=1),
        "when_noticed": T10,
        "when_aware": T10 + timedelta(hours=1),
        "personal_data_involved": True,
        "systems_affected": ["Loan management system"],
    }
    kwargs.update(overrides)
    return IncidentProfile(**kwargs)


@pytest.fixture
def store(tmp_path) -> CaseStore:
    return CaseStore(tmp_path / "cases", DATA)


@pytest.fixture
def client(tmp_path, monkeypatch) -> TestClient:
    monkeypatch.setenv("SENTINELBRIEF_CASES_DIR", str(tmp_path / "cases"))
    return TestClient(app, follow_redirects=False)


# --- drafts ---


def test_filing_content_is_quoted_from_the_stated_pages():
    """Catches: a 'required content' item that is not in the source text."""
    content = load_filing_content(DATA)
    assert DPDP_72H in content and len(content[DPDP_72H]) == 6
    obligations = {o["id"] for o in IncidentClockEngine(DATA).obligations}
    assert set(content) <= obligations


def test_filing_content_loader_rejects_an_invented_item(tmp_path):
    """Catches: the loader accepting text that is not on the cited page."""
    pages = SourcePages(DATA)
    with pytest.raises(ValueError, match="not on PDF page"):
        pages.require_quote("meity.dpdp-rules.2025", 26, "a screenshot of the firewall dashboard")
    with pytest.raises(ValueError, match="not on PDF page"):
        pages.require_quote("meity.dpdp-rules.2025", 2, "(vi) a report regarding the intimations")
    with pytest.raises(ValueError, match="Empty"):
        pages.require_quote("meity.dpdp-rules.2025", 26, "  ")


def test_drafts_cover_timed_urgent_and_untimed_duties():
    """Catches: a reporting duty with no draft, or an ongoing duty drafted as a filing."""
    engine = IncidentClockEngine(DATA)
    result = engine.evaluate(_profile())
    drafts = {d.obligation_id: d for d in build_drafts(engine, result, load_filing_content(DATA))}
    assert (
        drafts[CERT_6H].urgency == drafts[RBI_6H].urgency == drafts[DPDP_72H].urgency == "deadline"
    )
    assert (
        drafts[DPDP_PRINCIPAL].urgency == "without_delay" and drafts[DPDP_PRINCIPAL].due_ist is None
    )
    assert drafts[RBI_CERT_IN].urgency == "no_time_limit"
    assert not any(oid.endswith("comply-with-orders") for oid in drafts)
    ordered = [
        d
        for d in build_drafts(engine, result, load_filing_content(DATA))
        if d.urgency == "deadline"
    ]
    assert [d.obligation_id for d in ordered] == [RBI_6H, CERT_6H, DPDP_72H]
    assert not any(
        "va-half-yearly" in oid or "ntp-sync" in oid or "log-retention" in oid for oid in drafts
    )
    assert drafts[RBI_6H].due_ist == "01 Jun 2027, 15:00 IST"


def test_draft_fields_state_their_origin_and_invent_nothing():
    """Catches: generated text in a draft, or clause content pre-filled by the tool."""
    engine = IncidentClockEngine(DATA)
    result = engine.evaluate(_profile())
    draft = next(
        d
        for d in build_drafts(engine, result, load_filing_content(DATA))
        if d.obligation_id == DPDP_72H
    )
    assert draft.notice.startswith("DRAFT")
    source_fields = [f for f in draft.fields if f.origin == "source_text"]
    assert len(source_fields) == 6
    assert all(f.value is None and "PDF page 26" in (f.citation or "") for f in source_fields)
    pages = SourcePages(DATA)
    for f in source_fields:
        pages.require_quote("meity.dpdp-rules.2025", 26, f.label)
    assert draft.open_fields() == source_fields
    inputs = {f.label: f.value for f in draft.fields if f.origin == "your_input"}
    assert inputs["Systems affected"] == "Loan management system"
    assert inputs["Entity became aware at"] == "01 Jun 2027, 11:00 IST"
    assert {f.origin for f in draft.fields} == {"computed", "your_input", "source_text"}


# --- cases ---


def test_facts_round_trip_through_storage():
    """Catches: a stored case re-evaluating to different law because a fact was lost."""
    profile = _profile(uses_protected_systems=None, is_cyber_incident=True)
    again = facts_to_profile(json.loads(json.dumps(profile_to_facts(profile))))
    assert profile_to_facts(again) == profile_to_facts(profile)
    with pytest.raises(ValueError, match="Unknown fact"):
        facts_to_profile({"entity_classes": ["bank"], "favourite_colour": "blue"})


def test_case_lifecycle_requires_a_person_at_each_step(store):
    """Catches: filing recorded without approval, or approval by an AI agent or nobody."""
    case_id = store.create(_profile(), "Asha Rao")
    with pytest.raises(ValueError, match="approved by a person"):
        store.record_filing(case_id, CERT_6H, "Asha Rao", "CERTIN-1", T10)
    for bad in ("", " ", "Claude", "codex", "auto"):
        with pytest.raises(ValueError, match="person"):
            store.approve(case_id, CERT_6H, bad)
    digest = store.approve(case_id, CERT_6H, "Asha Rao")
    with pytest.raises(ValueError, match="reference"):
        store.record_filing(case_id, CERT_6H, "Asha Rao", " ", T10)
    with pytest.raises(ValueError, match="timezone-aware"):
        store.record_filing(case_id, CERT_6H, "Asha Rao", "CERTIN-1", datetime(2027, 6, 1, 12, 0))
    store.record_filing(case_id, CERT_6H, "Asha Rao", "CERTIN-1", T10 + timedelta(hours=2))
    row = next(r for r in store.view(case_id)["drafts"] if r["draft"]["obligation_id"] == CERT_6H)
    assert (
        row["status"] == "filed"
        and row["reference"] == "CERTIN-1"
        and row["approved_digest"] == digest
    )
    with pytest.raises(ValueError, match="already recorded as filed"):
        store.approve(case_id, CERT_6H, "Asha Rao")
    with pytest.raises(KeyError):
        store.approve(case_id, "cert-in.directions-70b.2022.ntp-sync", "Asha Rao")


def test_changing_a_fact_withdraws_unfiled_approvals(store):
    """Catches: an approval surviving a change to the content it approved."""
    case_id = store.create(_profile(), "Asha Rao")
    store.approve(case_id, RBI_6H, "Asha Rao")
    store.approve(case_id, CERT_6H, "Asha Rao")
    store.record_filing(case_id, CERT_6H, "Asha Rao", "CERTIN-1", T10 + timedelta(hours=2))
    store.update_facts(
        case_id, {"when_detected": (T10 - timedelta(hours=3)).isoformat()}, "Asha Rao"
    )
    rows = {r["draft"]["obligation_id"]: r for r in store.view(case_id)["drafts"]}
    assert rows[RBI_6H]["status"] == "draft"
    assert rows[RBI_6H]["draft"]["due_ist"] == "01 Jun 2027, 13:00 IST"
    assert rows[CERT_6H]["status"] == "filed"
    with pytest.raises(ValueError, match="approved by a person"):
        store.record_filing(case_id, RBI_6H, "Asha Rao", "DAKSH-9", T10)


def test_answering_an_unknown_through_facts_produces_the_deadline(store):
    """Catches: the case not re-evaluating when a missing fact is supplied."""
    case_id = store.create(_profile(when_aware=None), "Asha Rao")
    view = store.view(case_id)
    assert any("aware" in u["question"] for u in view["clock"]["unknowns"])
    assert DPDP_72H not in {r["draft"]["obligation_id"] for r in view["drafts"]}
    store.update_facts(case_id, {"when_aware": (T10 + timedelta(hours=1)).isoformat()}, "Asha Rao")
    assert DPDP_72H in {r["draft"]["obligation_id"] for r in store.view(case_id)["drafts"]}


def test_invalid_facts_are_rejected_and_nothing_is_stored(store):
    """Catches: a naive timestamp or unknown class stored and silently misread later."""
    with pytest.raises(ValueError):
        store.create(_profile(entity_classes=["not.a.class"]), "Asha Rao")
    assert not list(store.root.glob("*")) if store.root.exists() else True
    case_id = store.create(_profile(), "Asha Rao")
    before = store.view(case_id)["timeline"]["events"]
    with pytest.raises(ValueError):
        store.update_facts(case_id, {"when_detected": "2027-06-01T09:00:00"}, "Asha Rao")
    assert store.view(case_id)["timeline"]["events"] == before
    with pytest.raises(ValueError, match="Invalid case id"):
        store.view("../../etc")


def test_every_state_change_is_on_the_evidence_chain(store):
    """Catches: an approval or filing that leaves no tamper-evident record."""
    case_id = store.create(_profile(), "Asha Rao")
    store.approve(case_id, CERT_6H, "Asha Rao")
    store.record_filing(case_id, CERT_6H, "Vikram Shah", "CERTIN-1", T10 + timedelta(hours=2))
    timeline = store.timeline(case_id)
    assert [e.type for e in timeline] == ["incident_created", "draft_approved", "filing_recorded"]
    assert [e.actor for e in timeline] == ["Asha Rao", "Asha Rao", "Vikram Shah"]
    assert timeline.verify() == (True, None)
    path = store.root / case_id / "timeline.jsonl"
    path.write_text(
        path.read_text(encoding="utf-8").replace("CERTIN-1", "CERTIN-2"), encoding="utf-8"
    )
    view = store.view(case_id)
    assert view["timeline"]["valid"] is False and view["timeline"]["first_break_seq"] == 2


def test_export_bundle_is_complete_and_hashes_match(store, tmp_path):
    """Catches: a bundle missing the law as applied, or a manifest that does not match its files."""
    case_id = store.create(_profile(), "Asha Rao")
    store.approve(case_id, CERT_6H, "Asha Rao")
    bundle = store.export(case_id, tmp_path / "bundle")
    names = {p.name for p in bundle.iterdir()}
    assert {
        "timeline.jsonl",
        "case.json",
        "clock_result.json",
        "drafts.json",
        "law_snapshot.json",
        "CASE_SUMMARY.md",
        "bundle_manifest.json",
    } <= names
    manifest = json.loads((bundle / "bundle_manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((bundle / name).read_bytes()).hexdigest() == digest
    assert set(manifest["files"]) == names - {"bundle_manifest.json"}
    law = json.loads((bundle / "law_snapshot.json").read_text(encoding="utf-8"))
    assert law["law_as_of"] == "2027-06-01"
    cert = next(o for o in law["obligations"] if o["obligation_id"] == CERT_6H)
    assert "within 6 hours" in cert["text_verbatim"] and cert["citations"]
    summary = (bundle / "CASE_SUMMARY.md").read_text(encoding="utf-8")
    assert "does NOT prove" in summary and "submitted nothing" in summary and "approved" in summary


# --- calendar ---


def test_calendar_lists_recurring_duties_with_correct_rules():
    """Catches: wrong first due date or repeat rule for VA (six months) and PT (12 months)."""
    engine = IncidentClockEngine(DATA)
    stamp = datetime(2026, 10, 4, tzinfo=IST)
    ics, undetermined = recurring_duties_ics(
        engine, ["nbfc.middle_layer"], date(2026, 8, 31), stamp
    )
    assert undetermined == []
    assert ics.startswith("BEGIN:VCALENDAR\r\n") and ics.endswith("END:VCALENDAR\r\n")
    assert ics.count("BEGIN:VEVENT") == 2
    assert "DTSTART;VALUE=DATE:20270228" in ics and "RRULE:FREQ=MONTHLY;INTERVAL=6" in ics
    assert "DTSTART;VALUE=DATE:20270831" in ics and "RRULE:FREQ=YEARLY;INTERVAL=1" in ics
    assert all(len(line.encode("utf-8")) <= 75 for line in ics.split("\r\n"))
    assert recurring_duties_ics(engine, ["nbfc.middle_layer"], date(2026, 8, 31), stamp)[0] == ics


def test_calendar_never_silently_drops_an_undetermined_duty():
    """Catches: a generic NBFC getting an empty calendar instead of being asked its category."""
    engine = IncidentClockEngine(DATA)
    ics, undetermined = recurring_duties_ics(engine, ["nbfc"], date(2026, 10, 1))
    assert "BEGIN:VEVENT" not in ics
    assert {u.split(".")[-1] for u in undetermined} == {"ch5-va-half-yearly", "ch5-pt-annual"}
    ics_bank, none = recurring_duties_ics(engine, ["bank"], date(2026, 10, 1))
    assert "BEGIN:VEVENT" not in ics_bank and none == []
    before, _ = recurring_duties_ics(engine, ["nbfc.middle_layer"], date(2026, 7, 1))
    assert "BEGIN:VEVENT" not in before  # the Direction was not yet in force


# --- HTTP ---

_JSON_FACTS = {
    "entity_classes": ["nbfc.middle_layer"],
    "incident_types": [RANSOMWARE],
    "when_detected": "2026-10-01T10:00:00+05:30",
    "when_noticed": "2026-10-01T10:00:00+05:30",
}


def test_api_case_flow(client):
    """Catches: the HTTP layer bypassing the person and approval checks, or filing by itself."""
    assert client.post("/api/cases", json=_JSON_FACTS).status_code == 422  # nobody named
    created = client.post("/api/cases", json={**_JSON_FACTS, "opened_by": "Asha Rao"})
    assert created.status_code == 201, created.text
    case_id = created.json()["case_id"]
    base = f"/api/cases/{case_id}"

    view = client.get(base).json()
    assert {r["status"] for r in view["drafts"]} == {"draft"}
    assert RBI_6H in {r["draft"]["obligation_id"] for r in view["drafts"]}

    filed_early = client.post(
        f"{base}/drafts/{RBI_6H}/filed",
        json={"filed_by": "Asha Rao", "reference": "D-1", "filed_at": "2026-10-01T12:00:00+05:30"},
    )
    assert filed_early.status_code == 422
    assert (
        client.post(f"{base}/drafts/{RBI_6H}/approve", json={"approver": "gpt"}).status_code == 422
    )
    assert (
        client.post(f"{base}/drafts/{RBI_6H}/approve", json={"approver": "Asha Rao"}).status_code
        == 200
    )
    naive = client.post(
        f"{base}/drafts/{RBI_6H}/filed",
        json={"filed_by": "Asha Rao", "reference": "D-1", "filed_at": "2026-10-01T12:00:00"},
    )
    assert naive.status_code == 422
    filed = client.post(
        f"{base}/drafts/{RBI_6H}/filed",
        json={"filed_by": "Asha Rao", "reference": "D-1", "filed_at": "2026-10-01T12:00:00+05:30"},
    )
    assert filed.status_code == 200, filed.text

    facts = client.post(
        f"{base}/facts", json={"recorded_by": "Asha Rao", "is_cyber_incident": True}
    )
    assert facts.status_code == 200, facts.text
    assert client.get(base).json()["timeline"]["events"] == 4

    page = client.get(f"/cases/{case_id}")
    assert page.status_code == 200
    assert "does not file anything" in page.text and "Recorded as filed by Asha Rao" in page.text

    assert client.get("/api/cases/" + "0" * 32).status_code == 404
    assert client.get("/api/cases/not-an-id").status_code == 422
    assert (
        client.post(
            f"{base}/drafts/unknown.duty/approve", json={"approver": "Asha Rao"}
        ).status_code
        == 404
    )


def test_api_export_zip_and_form_flow(client):
    """Catches: the browser form path not creating a case, or the bundle download being empty."""
    form = (
        "entity_class=nbfc.middle_layer&incident_types=Malicious+code+attacks+such+as+Ransomware"
        "&when_detected=2026-10-01T10%3A00&when_noticed=2026-10-01T10%3A00&opened_by=Asha+Rao"
    )
    created = client.post(
        "/api/cases", content=form, headers={"content-type": "application/x-www-form-urlencoded"}
    )
    assert created.status_code == 303, created.text
    case_id = created.headers["location"].rsplit("/", 1)[-1]
    approve = client.post(
        f"/api/cases/{case_id}/drafts/{RBI_6H}/approve",
        content="approver=Asha+Rao",
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert approve.status_code == 303
    download = client.get(f"/api/cases/{case_id}/export.zip")
    assert download.status_code == 200 and download.headers["content-type"] == "application/zip"
    names = set(zipfile.ZipFile(io.BytesIO(download.content)).namelist())
    assert {
        "timeline.jsonl",
        "law_snapshot.json",
        "bundle_manifest.json",
        "CASE_SUMMARY.md",
    } <= names


def test_api_calendar(client):
    """Catches: the calendar endpoint returning a partial calendar for an ambiguous class."""
    ok = client.get(
        "/api/calendar.ics", params={"classes": "nbfc.middle_layer", "last_done": "2026-10-01"}
    )
    assert ok.status_code == 200 and ok.headers["content-type"].startswith("text/calendar")
    assert ok.text.count("BEGIN:VEVENT") == 2
    vague = client.get("/api/calendar.ics", params={"classes": "nbfc", "last_done": "2026-10-01"})
    assert vague.status_code == 422 and len(vague.json()["undetermined"]) == 2
    assert (
        client.get("/api/calendar.ics", params={"classes": "nbfc.middle_layer"}).status_code == 422
    )
    assert (
        client.get(
            "/api/calendar.ics", params={"classes": "x.y", "last_done": "2026-10-01"}
        ).status_code
        == 422
    )


def test_incident_form_offers_opening_a_case():
    """Catches: no way to open a case from the incident page."""
    page = TestClient(app).get("/incident")
    assert 'name="opened_by"' in page.text and 'formaction="/api/cases"' in page.text
