# Decisions Log

Every notable decision and deviation from the build brief, dated.

---

## 2026-09-24: Python 3.13 over 3.14

**Decision:** Pin Python 3.13 (currently 3.13.15) instead of using the system Python 3.14.0.

**Reason:** Python 3.14 is very new (released mid-2026). Key dependencies like PyMuPDF may lack stable wheels. The brief (section 6) explicitly recommends pinning to 3.12 or 3.13 if needed.

**Alternative rejected:** Python 3.14 (too new, risk of incompatible C extensions); Python 3.12 (older than necessary, 3.13 is stable and well-supported).

## 2026-09-24: Frontend — FastAPI + Jinja2 + htmx

**Decision:** Server-rendered templates with FastAPI + Jinja2 + htmx/vanilla JS. No Node build step.

**Reason:** Owner preference. Fewer moving parts. Card feed can be exported as static HTML. React/Svelte only if a specific interactive feature demands it.

**Alternative rejected:** React SPA (unnecessary complexity for this surface), Svelte (same), Next.js (Node dependency).

## 2026-09-24: uv for dependency management

**Decision:** Use uv for Python version pinning, virtual environment, and reproducible installs.

**Reason:** Owner approved. Fast, reproducible, handles Python version management.

## 2026-09-24: hatchling as build backend

**Decision:** Use hatchling instead of uv_build as the PEP 517 build backend.

**Reason:** hatchling is mature, widely used, and supports src-layout cleanly. uv_build is newer and less battle-tested.

## 2026-09-24: Vertical slice approach — CERT-In first

**Decision:** Build the complete pipeline (fetch → extract → obligations → validate → clock → benchmark) for CERT-In Directions only before broadening to RBI, SEBI, DPDP.

**Reason:** Owner directive. Tests the schema against real regulatory text before locking it in. Catches design issues early.
