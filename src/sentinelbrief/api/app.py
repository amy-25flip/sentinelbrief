"""FastAPI application for SentinelBrief."""

from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

IST = timezone(timedelta(hours=5, minutes=30))

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
    """Home page with card feed."""
    obligations = _load_obligations()
    instruments = _load_instruments()
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "obligations": obligations,
            "instruments": instruments,
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
    return templates.TemplateResponse(
        request=request,
        name="incident.html",
        context={},
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
