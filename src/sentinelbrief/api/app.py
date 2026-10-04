"""FastAPI application for SentinelBrief."""

import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from sentinelbrief.cards import CardFeed
from sentinelbrief.clock import IncidentClockEngine, IncidentProfile
from sentinelbrief.clock.engine import IST

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

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
templates.env.filters["ist"] = lambda dt: dt.astimezone(IST).strftime("%d %b %Y, %H:%M IST")

# Mount static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


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


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    """Home page with deterministic card feed."""
    feed = CardFeed(DATA_DIR)
    fixtures_dir = BASE_DIR / "tests" / "fixtures"
    feed.load_from_data_dir(fixtures_dir=fixtures_dir)
    cards = feed.get_feed()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "cards": cards,
            "now_ist": datetime.now(IST).strftime("%Y-%m-%d %H:%M IST"),
        },
    )


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
    cyber_incident = payload.get("is_cyber_incident")
    if cyber_incident is None:
        cyber_attestation = payload.get("cyber_incident_attestation", "unknown")
        if cyber_attestation not in {"unknown", "yes", "no"}:
            raise ValueError("cyber_incident_attestation must be unknown, yes or no")
        cyber_incident = (
            True if cyber_attestation == "yes" else False if cyber_attestation == "no" else None
        )
    elif isinstance(cyber_incident, str):
        if cyber_incident.lower() not in {"true", "false"}:
            raise ValueError("is_cyber_incident must be true, false or null")
        cyber_incident = cyber_incident.lower() == "true"
    elif not isinstance(cyber_incident, bool):
        raise ValueError("is_cyber_incident must be true, false or null")
    return IncidentProfile(
        entity_class=str(primary_class) if entity_classes is None else None,
        entity_classes=list(entity_classes) if entity_classes is not None else None,
        incident_types=list(incident_types),
        annexure_i_items=list(payload.get("annexure_i_items") or []),
        is_annexure_i_type=False if attestation == "no" else None,
        is_cyber_incident=cyber_incident,
        personal_data_involved=personal_data,
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
            repeated = {"annexure_i_items", "also_classes"}
            payload = {k: (v if k in repeated else v[-1]) for k, v in raw.items()}
        profile = _profile_from_payload(payload, form_input=not is_json)
        engine = IncidentClockEngine(DATA_DIR)
        result = engine.evaluate(profile)
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
