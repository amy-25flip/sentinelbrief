"""FastAPI application for SentinelBrief."""

import io
import os
import re
import tempfile
import zipfile
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sentinelbrief.cards import CardFeed
from sentinelbrief.cards.feed import regulatory_rss
from sentinelbrief.clock import IncidentClockEngine, IncidentProfile
from sentinelbrief.clock.engine import IST
from sentinelbrief.migrator.review import ConfirmationStore
from sentinelbrief.workspace import CaseStore, recurring_duties_ics

app = FastAPI(
    title="SentinelBrief",
    description="Indian cyber-regulatory compliance: obligation dataset, incident clock, and card feed",
    version="0.1.0",
)

# Paths
BASE_DIR = Path(__file__).resolve().parents[3]
WEB_DIR = BASE_DIR / "web"
TEMPLATES_DIR = WEB_DIR / "templates"
STATIC_DIR = WEB_DIR / "static"
DATA_DIR = BASE_DIR / "data"
# The home page and the RSS feed list every card; the feed's default page size would hide
# obligations once the dataset outgrows it.
FEED_LIMIT = 10_000

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["ist"] = lambda dt: dt.astimezone(IST).strftime("%d %b %Y, %H:%M IST")

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.middleware("http")
async def same_origin_for_state_changes(request: Request, call_next: Any) -> Any:
    """Refuse state-changing requests sent by another website.

    The app has no login and usually runs on localhost, so a page on another site could
    otherwise post to it from the user's browser (approve a draft, change facts). Browsers
    send Origin on such requests; a mismatch with Host is refused. Non-browser clients,
    which send no Origin, are unaffected.
    """
    if request.method not in {"GET", "HEAD", "OPTIONS"}:
        origin = request.headers.get("origin")
        if origin is not None and urlparse(origin).netloc != request.headers.get("host", ""):
            return JSONResponse({"error": "cross-origin request refused"}, status_code=403)
    return await call_next(request)


def _load_json(path: Path) -> Any:
    """Load a JSON file."""
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def _load_instruments() -> list[dict[str, Any]]:
    """Load all instrument records."""
    instruments_dir = DATA_DIR / "instruments"
    results = []
    if instruments_dir.exists():
        for f in sorted(instruments_dir.glob("*.json")):
            results.append(_load_json(f))
    return results


def _load_obligations() -> list[dict[str, Any]]:
    """Load all obligation records."""
    obligations_dir = DATA_DIR / "obligations"
    results = []
    if obligations_dir.exists():
        for f in sorted(obligations_dir.glob("*.json")):
            data = _load_json(f)
            if isinstance(data, list):
                results.extend(data)
            else:
                results.append(data)
    return results


def _migration_store() -> ConfirmationStore:
    return ConfirmationStore(DATA_DIR)


@app.get("/migrations", response_class=HTMLResponse)
async def migration_list(request: Request) -> HTMLResponse:
    migrations = []
    for path in sorted((DATA_DIR / "migrations").glob("*.json")):
        migrations.append(_load_json(path))
    return templates.TemplateResponse(
        request=request, name="migrations.html", context={"migrations": migrations}
    )


@app.get("/migrations/{migration_id}", response_class=HTMLResponse)
async def migration_detail(
    request: Request, migration_id: str, status: str | None = None
) -> Response:
    try:
        migration = _migration_store().load(migration_id)
    except KeyError:
        return HTMLResponse("<h1>Migration not found</h1>", status_code=404)
    mappings = migration["mappings"]
    if status:
        mappings = [item for item in mappings if item["status"] == status]
    return templates.TemplateResponse(
        request=request,
        name="migration_detail.html",
        context={"migration": migration, "mappings": mappings, "status_filter": status},
    )


@app.post("/api/migrations/{migration_id}/{old_clause}/confirm", response_model=None)
async def confirm_migration(request: Request, migration_id: str, old_clause: str) -> Response:
    try:
        payload, is_json = await _payload(request)
        record = _migration_store().confirm(
            migration_id, old_clause, str(payload.get("reviewer", ""))
        )
        if is_json:
            return JSONResponse(record)
        return RedirectResponse(f"/migrations/{migration_id}#clause-{old_clause}", status_code=303)
    except (ValueError, KeyError, TypeError) as exc:
        return _case_error(exc)


@app.post("/api/migrations/{migration_id}/{old_clause}/correct", response_model=None)
async def correct_migration(request: Request, migration_id: str, old_clause: str) -> Response:
    try:
        payload, is_json = await _payload(request)
        paragraphs = payload.get("paragraphs") or []
        if isinstance(paragraphs, str):
            paragraphs = [part.strip() for part in paragraphs.split(",") if part.strip()]
        if not isinstance(paragraphs, list):
            raise ValueError("paragraphs must be a list or comma-separated string")
        record = _migration_store().correct(
            migration_id,
            old_clause,
            str(payload.get("reviewer", "")),
            [str(item) for item in paragraphs],
            str(payload.get("reason", "")),
        )
        if is_json:
            return JSONResponse(record)
        return RedirectResponse(f"/migrations/{migration_id}#clause-{old_clause}", status_code=303)
    except (ValueError, KeyError, TypeError) as exc:
        return _case_error(exc)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Home page with deterministic card feed."""
    feed = CardFeed(DATA_DIR)
    fixtures_dir = BASE_DIR / "tests" / "fixtures"
    feed.load_from_data_dir(fixtures_dir=fixtures_dir)
    cards = feed.get_feed(limit=FEED_LIMIT)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "cards": cards,
            "now_ist": datetime.now(IST).strftime("%Y-%m-%d %H:%M IST"),
        },
    )


@app.get("/feed.xml", response_model=None)
async def rss_feed(request: Request) -> Response:
    """RSS 2.0 generated from the same regulatory-card data as the home page."""
    feed = CardFeed(DATA_DIR)
    feed.load_from_data_dir(fixtures_dir=BASE_DIR / "tests" / "fixtures")
    payload = regulatory_rss(feed.get_feed(limit=FEED_LIMIT), str(request.base_url))
    return Response(payload, media_type="application/rss+xml; charset=utf-8")


@app.get("/obligations", response_class=HTMLResponse)
async def obligation_browser(request: Request) -> HTMLResponse:
    """Browse all obligations."""
    obligations = _load_obligations()
    instruments = _load_instruments()
    instrument_map = {i["id"]: i for i in instruments}
    return templates.TemplateResponse(
        request=request,
        name="obligations.html",
        context={
            "obligations": obligations,
            "instrument_map": instrument_map,
        },
    )


@app.get("/obligations/{obligation_id}", response_class=HTMLResponse)
async def obligation_detail(request: Request, obligation_id: str) -> HTMLResponse:
    """View a single obligation with its full citation."""
    obligations = _load_obligations()
    instruments = _load_instruments()
    instrument_map = {i["id"]: i for i in instruments}

    obligation = next((o for o in obligations if o["id"] == obligation_id), None)
    if not obligation:
        return HTMLResponse("<h1>Obligation not found</h1>", status_code=404)

    instrument = instrument_map.get(obligation["instrument_id"])
    return templates.TemplateResponse(
        request=request,
        name="obligation_detail.html",
        context={
            "obligation": obligation,
            "instrument": instrument,
        },
    )


@app.get("/instruments/{instrument_id}", response_class=HTMLResponse)
async def instrument_detail(request: Request, instrument_id: str) -> Response:
    instrument = next((item for item in _load_instruments() if item["id"] == instrument_id), None)
    if instrument is None:
        return HTMLResponse("<h1>Instrument not found</h1>", status_code=404)
    return templates.TemplateResponse(
        request=request, name="instrument_detail.html", context={"instrument": instrument}
    )


@app.get("/incident", response_class=HTMLResponse)
async def incident_workspace(request: Request) -> HTMLResponse:
    """Incident clock workspace."""
    engine = IncidentClockEngine(DATA_DIR)
    return templates.TemplateResponse(
        request=request,
        name="incident.html",
        context={
            "entity_classes": sorted(engine.taxonomy.classes.keys()),
            "annexure_items": engine.annexure_items(),
        },
    )


_TIME_FIELDS = (
    "when_noticed",
    "when_brought_to_notice",
    "when_detected",
    "when_occurred",
    "when_aware",
    "when_reported_to_sebi",
)


def _parse_time(value: str, *, form_input: bool) -> datetime:
    """Form times (datetime-local) are entered in IST. API times must carry an explicit offset."""
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        if not form_input:
            raise ValueError("timestamps must include a UTC offset, e.g. 2026-09-24T09:00:00+05:30")
        parsed = parsed.replace(tzinfo=IST)
    return parsed


def _profile_from_payload(payload: dict[str, Any], *, form_input: bool) -> IncidentProfile:
    kwargs: dict[str, Any] = {}
    for name in _TIME_FIELDS:
        value = payload.get(name)
        if value:
            kwargs[name] = _parse_time(str(value), form_input=form_input)

    incident_types = payload.get("incident_types") or []
    if isinstance(incident_types, str):
        incident_types = [t.strip() for t in re.split(r"[,\n;]", incident_types) if t.strip()]

    attestation = payload.get("annexure_attestation", "unknown")
    also_classes = payload.get("also_classes") or []
    if isinstance(also_classes, str):
        also_classes = [also_classes]
    primary_class = payload.get("entity_class")
    entity_classes = payload.get("entity_classes")
    if entity_classes is not None and primary_class is not None:
        raise ValueError("Supply either entity_class or entity_classes, not both")
    if entity_classes is None and also_classes:
        entity_classes = [primary_class, *also_classes]
    personal_data = payload.get("personal_data_involved")
    if isinstance(personal_data, str):
        if personal_data.lower() not in {"true", "false"}:
            raise ValueError("personal_data_involved must be true or false")
        personal_data = personal_data.lower() == "true"

    def optional_bool(name: str, attestation_name: str | None = None) -> bool | None:
        value = payload.get(name)
        if value is None and attestation_name is not None:
            attestation = payload.get(attestation_name, "unknown")
            if attestation not in {"unknown", "yes", "no"}:
                raise ValueError(f"{attestation_name} must be unknown, yes or no")
            return True if attestation == "yes" else False if attestation == "no" else None
        if value is None:
            return None
        if isinstance(value, str):
            if value.lower() not in {"true", "false"}:
                raise ValueError(f"{name} must be true, false or null")
            return value.lower() == "true"
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be true, false or null")
        return value

    cyber_incident = optional_bool("is_cyber_incident", "cyber_incident_attestation")
    irdai_cyber_incident = optional_bool("is_irdai_cyber_incident")
    sebi_cybersecurity_incident = optional_bool("is_sebi_cybersecurity_incident")
    sebi_forensic = optional_bool("sebi_forensic_directed_or_rca_inconclusive")
    protected_systems = payload.get("uses_protected_systems")
    if protected_systems is None:
        protected_attestation = payload.get("protected_system_attestation", "unknown")
        if protected_attestation not in {"unknown", "yes", "no"}:
            raise ValueError("protected_system_attestation must be unknown, yes or no")
        protected_systems = (
            True
            if protected_attestation == "yes"
            else False
            if protected_attestation == "no"
            else None
        )
    elif isinstance(protected_systems, str):
        if protected_systems.lower() not in {"true", "false"}:
            raise ValueError("uses_protected_systems must be true, false or null")
        protected_systems = protected_systems.lower() == "true"
    elif not isinstance(protected_systems, bool):
        raise ValueError("uses_protected_systems must be true, false or null")
    external_raw = payload.get("external_events") or {}
    if not isinstance(external_raw, dict):
        raise ValueError("external_events must be an object of obligation id to timestamp")
    external_events = {
        str(key): _parse_time(str(value), form_input=form_input)
        for key, value in external_raw.items()
        if value
    }
    return IncidentProfile(
        entity_class=str(primary_class) if entity_classes is None else None,
        entity_classes=list(entity_classes) if entity_classes is not None else None,
        incident_types=list(incident_types),
        annexure_i_items=list(payload.get("annexure_i_items") or []),
        is_annexure_i_type=False if attestation == "no" else None,
        is_cyber_incident=cyber_incident,
        is_irdai_cyber_incident=irdai_cyber_incident,
        is_sebi_cybersecurity_incident=sebi_cybersecurity_incident,
        sebi_severity=(str(payload["sebi_severity"]).lower() or None)
        if payload.get("sebi_severity")
        else None,
        sebi_forensic_directed_or_rca_inconclusive=sebi_forensic,
        personal_data_involved=personal_data,
        uses_protected_systems=protected_systems,
        external_events=external_events,
        **kwargs,
    )


@app.post("/api/incident/clock", response_model=None)
async def incident_clock(request: Request) -> Response:
    """Compute regulatory clocks with the deterministic engine.

    HTMX form posts get an HTML fragment (times read as IST); JSON posts get JSON
    (timestamps need an explicit offset).
    """
    is_json = "application/json" in request.headers.get("content-type", "")
    is_htmx = request.headers.get("hx-request") == "true"
    try:
        if is_json:
            payload = await request.json()
        else:
            raw = parse_qs((await request.body()).decode("utf-8"), keep_blank_values=False)
            repeated = {"annexure_i_items", "also_classes", "simulate_instruments"}
            payload = {k: (v if k in repeated else v[-1]) for k, v in raw.items()}
        simulation_value = payload.pop("simulate_instruments", []) or []
        if not isinstance(simulation_value, list):
            raise ValueError("simulate_instruments must be a list of instrument ids")
        simulate_instruments = [str(value) for value in simulation_value]
        profile = _profile_from_payload(payload, form_input=not is_json)
        engine = IncidentClockEngine(DATA_DIR)
        result = engine.evaluate(profile, simulate_instruments=simulate_instruments)
    except (ValueError, KeyError, TypeError) as exc:
        if is_htmx:
            return templates.TemplateResponse(
                request=request,
                name="partials/clock_error.html",
                context={"message": str(exc)},
                status_code=422,
            )
        return JSONResponse({"error": str(exc)}, status_code=422)

    if not is_htmx:
        return JSONResponse(result.to_dict())

    applicable = set(result.applicable_obligations)
    with_deadline = {d.obligation_id for d in result.deadlines}
    time_critical_ids = {t.obligation_id for t in result.time_critical}
    ongoing = []
    for obl_id in result.applicable_obligations:
        if obl_id in with_deadline or obl_id in time_critical_ids:
            continue
        obl = engine.get_obligation(obl_id) or {}
        deadline = (obl.get("normalized") or {}).get("deadline") or {}
        ongoing.append(
            {
                "id": obl_id,
                "paragraph": obl.get("paragraph_ref", ""),
                "action": (obl.get("normalized") or {}).get("action", ""),
                "retain": deadline.get("duration_iso8601")
                if deadline.get("kind") == "retention"
                else None,
                "within": deadline.get("duration_iso8601")
                if deadline.get("anchor") == "external_event"
                else None,
                "starts_from": ((obl.get("normalized") or {}).get("trigger") or {}).get(
                    "description", ""
                ),
                "conditions": result.conditions_unevaluated.get(obl_id, []),
            }
        )
    matched = [{"id": m, "title": engine.annexure_title(m)} for m in result.annexure_i.matched]
    return templates.TemplateResponse(
        request=request,
        name="partials/clock_result.html",
        context={
            "result": result,
            "ongoing": ongoing,
            "matched": matched,
            "n_applicable": len(applicable),
            "simulated_deadlines": [d for d in result.deadlines if d.simulated],
            "real_deadlines": [d for d in result.deadlines if not d.simulated],
            "simulated_time_critical": [t for t in result.time_critical if t.simulated],
            "real_time_critical": [t for t in result.time_critical if not t.simulated],
        },
    )


# --- Incident cases: drafts, human approval, audit bundle, calendar ---


def _case_store() -> CaseStore:
    """Cases live on local disk only. SENTINELBRIEF_CASES_DIR overrides the default location."""
    root = Path(os.environ.get("SENTINELBRIEF_CASES_DIR") or BASE_DIR / "var" / "cases")
    root.mkdir(parents=True, exist_ok=True)
    return CaseStore(root, DATA_DIR)


async def _payload(request: Request) -> tuple[dict[str, Any], bool]:
    """Return (payload, is_json). Form posts keep repeated fields as lists."""
    if "application/json" in request.headers.get("content-type", ""):
        value = await request.json()
        if not isinstance(value, dict):
            raise ValueError("JSON body must be an object")
        return value, True
    raw = parse_qs((await request.body()).decode("utf-8"), keep_blank_values=False)
    repeated = {"annexure_i_items", "also_classes", "simulate_instruments"}
    return {k: (v if k in repeated else v[-1]) for k, v in raw.items()}, False


def _case_error(exc: Exception) -> JSONResponse:
    status = 404 if isinstance(exc, KeyError) else 422
    return JSONResponse({"error": str(exc).strip("'\"")}, status_code=status)


@app.post("/api/cases", response_model=None)
async def create_case(request: Request) -> Response:
    """Open a case from incident facts. `opened_by` must name a person."""
    try:
        payload, is_json = await _payload(request)
        actor = str(payload.pop("opened_by", ""))
        simulation_value = payload.pop("simulate_instruments", []) or []
        if not isinstance(simulation_value, list):
            raise ValueError("simulate_instruments must be a list of instrument ids")
        simulate_instruments = [str(value) for value in simulation_value]
        profile = _profile_from_payload(payload, form_input=not is_json)
        case_id = _case_store().create(profile, actor, simulate_instruments)
    except (ValueError, KeyError, TypeError) as exc:
        return JSONResponse({"error": str(exc)}, status_code=422)
    if is_json:
        return JSONResponse({"case_id": case_id}, status_code=201)
    return RedirectResponse(f"/cases/{case_id}", status_code=303)


@app.get("/api/cases/{case_id}", response_model=None)
async def get_case(case_id: str) -> Response:
    try:
        return JSONResponse(_case_store().view(case_id))
    except (ValueError, KeyError) as exc:
        return _case_error(exc)


@app.get("/cases/{case_id}", response_model=None)
async def case_page(request: Request, case_id: str) -> Response:
    try:
        view = _case_store().view(case_id)
    except (ValueError, KeyError):
        return HTMLResponse("<h1>Case not found</h1>", status_code=404)
    return templates.TemplateResponse(request=request, name="case.html", context={"view": view})


@app.post("/api/cases/{case_id}/facts", response_model=None)
async def update_case_facts(request: Request, case_id: str) -> Response:
    """Record new or corrected facts. Timestamps need a UTC offset. Withdraws unfiled approvals."""
    try:
        payload, is_json = await _payload(request)
        actor = str(payload.pop("recorded_by", ""))
        changes = {k: v for k, v in payload.items() if v not in ("", None) or is_json}
        if not is_json:
            duty, started = (
                changes.pop("external_duty", None),
                changes.pop("external_started", None),
            )
            if duty or started:
                if not (duty and started):
                    raise ValueError("Choose the duty and give the time its clock started")
                current = dict(
                    _case_store().view(case_id)["case"]["facts"].get("external_events") or {}
                )
                current[str(duty)] = _parse_time(str(started), form_input=True).isoformat()
                changes["external_events"] = current
            for name in _TIME_FIELDS:
                if name in changes:
                    changes[name] = _parse_time(str(changes[name]), form_input=True).isoformat()
            for name in (
                "personal_data_involved",
                "uses_protected_systems",
                "is_annexure_i_type",
                "is_cyber_incident",
                "is_irdai_cyber_incident",
                "is_sebi_cybersecurity_incident",
                "sebi_forensic_directed_or_rca_inconclusive",
            ):
                if name in changes:
                    if changes[name] not in {"true", "false"}:
                        raise ValueError(f"{name} must be true or false")
                    changes[name] = changes[name] == "true"
        _case_store().update_facts(case_id, changes, actor)
    except (ValueError, KeyError, TypeError) as exc:
        return _case_error(exc)
    if is_json:
        return JSONResponse({"ok": True})
    return RedirectResponse(f"/cases/{case_id}", status_code=303)


@app.post("/api/cases/{case_id}/drafts/{obligation_id}/approve", response_model=None)
async def approve_draft(request: Request, case_id: str, obligation_id: str) -> Response:
    """A named person approves the current content of one draft. Nothing is submitted."""
    try:
        payload, is_json = await _payload(request)
        accept = payload.get("accept_open_fields") in (True, "true", "on", "yes")
        digest = _case_store().approve(
            case_id, obligation_id, str(payload.get("approver", "")), accept_open_fields=accept
        )
    except (ValueError, KeyError, TypeError) as exc:
        return _case_error(exc)
    if is_json:
        return JSONResponse({"status": "approved", "draft_sha256": digest})
    return RedirectResponse(f"/cases/{case_id}", status_code=303)


@app.post("/api/cases/{case_id}/drafts/{obligation_id}/fields", response_model=None)
async def complete_draft_field(request: Request, case_id: str, obligation_id: str) -> Response:
    """A person completes one field the cited clause requires. Stored on this machine only."""
    try:
        payload, is_json = await _payload(request)
        _case_store().set_entry(
            case_id,
            obligation_id,
            str(payload.get("label", "")),
            str(payload.get("value", "")),
            str(payload.get("recorded_by", "")),
        )
    except (ValueError, KeyError, TypeError) as exc:
        return _case_error(exc)
    if is_json:
        return JSONResponse({"ok": True})
    return RedirectResponse(f"/cases/{case_id}#draft-{obligation_id}", status_code=303)


@app.post("/api/cases/{case_id}/drafts/{obligation_id}/filed", response_model=None)
async def record_filing(request: Request, case_id: str, obligation_id: str) -> Response:
    """Record that a person filed on the regulator's own channel. This tool files nothing."""
    try:
        payload, is_json = await _payload(request)
        filed_at = _parse_time(str(payload.get("filed_at", "")), form_input=not is_json)
        _case_store().record_filing(
            case_id,
            obligation_id,
            str(payload.get("filed_by", "")),
            str(payload.get("reference", "")),
            filed_at,
        )
    except (ValueError, KeyError, TypeError) as exc:
        return _case_error(exc)
    if is_json:
        return JSONResponse({"status": "filed"})
    return RedirectResponse(f"/cases/{case_id}", status_code=303)


@app.get("/api/cases/{case_id}/export.zip", response_model=None)
async def export_case(case_id: str) -> Response:
    """Auditor bundle: timeline, clocks, drafts, the law as applied, hashes."""
    try:
        store = _case_store()
        with tempfile.TemporaryDirectory() as tmp:
            bundle = store.export(case_id, Path(tmp) / "bundle")
            buffer = io.BytesIO()
            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
                for path in sorted(bundle.iterdir()):
                    archive.write(path, path.name)
    except (ValueError, KeyError) as exc:
        return _case_error(exc)
    return Response(
        buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="sentinelbrief-case-{case_id[:8]}.zip"'
        },
    )


@app.get("/api/calendar.ics", response_model=None)
async def calendar_export(classes: str = "", last_done: str = "") -> Response:
    """Recurring duties for the given entity classes as an iCalendar file.

    `classes` is comma-separated; `last_done` (YYYY-MM-DD) is when the duties were last performed.
    """
    try:
        entity_classes = [c.strip() for c in classes.split(",") if c.strip()]
        if not entity_classes:
            raise ValueError("classes is required, e.g. classes=nbfc.middle_layer")
        if not last_done:
            raise ValueError("last_done is required, e.g. last_done=2026-10-01")
        ics, undetermined = recurring_duties_ics(
            IncidentClockEngine(DATA_DIR), entity_classes, date.fromisoformat(last_done)
        )
    except (ValueError, TypeError) as exc:
        return JSONResponse({"error": str(exc)}, status_code=422)
    if undetermined:
        return JSONResponse(
            {
                "error": "Applicability of some recurring duties cannot be decided from these classes; choose a more specific class.",
                "undetermined": undetermined,
            },
            status_code=422,
        )
    return Response(
        ics,
        media_type="text/calendar; charset=utf-8",
        headers={
            "Content-Disposition": 'attachment; filename="sentinelbrief-recurring-duties.ics"'
        },
    )


# --- API endpoints (JSON) ---


@app.get("/api/obligations")
async def api_obligations() -> list[dict[str, Any]]:
    """Return all obligations as JSON."""
    return _load_obligations()


@app.get("/api/instruments")
async def api_instruments() -> list[dict[str, Any]]:
    """Return all instruments as JSON."""
    return _load_instruments()


@app.get("/api/health")
async def health() -> dict[str, str]:
    """Health check."""
    return {"status": "ok", "version": "0.1.0", "timestamp": datetime.now(UTC).isoformat()}
