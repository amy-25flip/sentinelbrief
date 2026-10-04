# SentinelBrief

Indian cyber-regulatory compliance - obligation dataset, incident clock, filing copilot, and card feed

## Overview

SentinelBrief turns "we have an incident" into what Indian law requires, by when, to whom, with the clause cited.

1. **Dataset**: clause-level obligations, each with a verbatim citation checked against the stored source text.
2. **Card feed**: deterministic cards grounded in the obligation records.
3. **Incident clock**: a deterministic engine (no LLM) that computes every applicable regulator's deadline from the incident facts and one or more entity classes, and asks when a fact it needs is missing. Legal gating uses structured `applicability.requires` keys; prose conditions are shown and never evaluated.
4. **Incident workspace**: a case with field-level filing drafts, approval by a named person, a hash-chained evidence timeline, an audit bundle and a calendar export for recurring duties. It files nothing: a person submits on the regulator's own channel and records the reference.

Current data status:
- Modelled obligations (25): CERT-In Directions 70B (2022), 7; DPDP Rules 2025 Rule 7, 3; SEBI CSCRF 2024 incident reporting and post-incident reports, 9; RBI NBFC Cybersecurity Directions 2026 (paragraphs 28, 121, 141), 6.
- Not modelled: IRDAI; the other RBI Directions; the rest of the RBI NBFC Direction; SEBI forensic and quarterly reports. See `docs/OPEN_QUESTIONS.md`.
- Benchmark: 68 dev scenarios, each with clause quotes verified against the page text; labels for RBI and SEBI were written and committed before implementation (`docs/LABELS_RBI.md`, `docs/LABELS_SEBI.md`). Labels are AI-authored and not yet reviewed by a compliance professional, and there is no hidden split yet, so no accuracy figure should be quoted.
- Contested readings recorded for counsel in `docs/DECISIONS.md`: the date from which SEBI CSCRF duties bind; the DPDP Rule 7 commencement date; the starting event for SEBI's 24-hour "other incident" duty; the time limit for HFCs reporting to NHB.
- RBI live reverify is exempted because the official RBI document server returns a CAPTCHA to automated clients; a human must re-check by downloading the official URL and comparing sha256.

Disclaimer: This tool is not legal advice and is not affiliated with any regulator.

## Prerequisites

- Python 3.13 (for example, Python 3.13.15)
- [`uv`](https://docs.astral.sh/uv/) for Python environment and dependency management

## Setup & Installation

1. Clone or navigate to the repository:
   ```bash
   cd E:\SentinelBrief
   ```

2. Install dependencies with `uv`:
   ```bash
   uv sync
   ```

3. Verify environment and quality gates:
   ```bash
   uv run python scripts/check.py
   ```

## Running the Application

Start the local FastAPI development server:
```bash
uv run uvicorn sentinelbrief.api.app:app --reload --port 8000
```
Open [http://localhost:8000](http://localhost:8000) to access the web application and incident clock.

On the incident page, "Open case" (with your name) creates a case at `/cases/<id>` with filing drafts and an evidence timeline. Cases are plain files under `var/cases/` on this machine (git-ignored; set `SENTINELBRIEF_CASES_DIR` to move them). Nothing is sent to any regulator or third party.

Useful endpoints:
- `POST /api/incident/clock` compute clocks without storing anything.
- `POST /api/cases`, `GET /api/cases/<id>`, `POST /api/cases/<id>/facts`, `.../drafts/<obligation>/approve`, `.../drafts/<obligation>/filed`, `GET /api/cases/<id>/export.zip`.
- `GET /api/calendar.ics?classes=nbfc.middle_layer&last_done=2026-10-01` recurring duties as an iCalendar file.

Check a profile from the command line:
```bash
uv run --no-sync python scripts/probe.py nbfc.middle_layer,dpdp.data_fiduciary detected=09:00 noticed=10:00 aware=11:00 personal=true date=2027-06-01
```

## Data Directory Layout

- `data/raw/`: Verbatim primary source files (`.pdf`, `.txt`, `.meta.json`) tracked by `manifest.json`.
- `data/instruments/`: Regulatory instrument metadata definitions.
- `data/obligations/`: Atomic obligations extracted with exact verbatim citations.
- `data/entities/`: Versioned regulatory entity class taxonomy (`general.json`, `cert-in.json`, `rbi.json`, `sebi.json`, `dpdp.json`).
- `data/reference/`: `annexure_i.json` (CERT-In incident types) and `filing_content.json` (content each filing must carry, quoted from the source).

## Ingestion & Verification Commands

- Run all gates (tests, ruff, mypy, validation, benchmark):
  ```bash
  uv run python scripts/check.py
  ```
- Run dataset schema and citation verification:
  ```bash
  uv run python -m sentinelbrief.verify.validate_all
  ```
- Run benchmark scorer:
  ```bash
  uv run python benchmark/runner/scorer.py --split dev
  ```
- Re-extract a staged PDF after adding it to `data/raw/`:
  ```bash
  uv run --no-sync python -m sentinelbrief.extract.pdf_text data/raw/<file>.pdf --instrument-id <id> --source-url <official-url> --retrieved-at <timestamp>
  ```
- Live source re-verification (network required; not part of offline tests):
  ```bash
  uv run --no-sync python scripts/reverify_sources.py
  ```

## License

MIT
