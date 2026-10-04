# SentinelBrief

Indian cyber-regulatory compliance - obligation dataset, incident clock, filing copilot, and card feed

## Overview

SentinelBrief provides three main surfaces:
1. **Dataset**: Citation-first structured obligations parsed from primary regulatory texts.
2. **Card Feed**: Deterministic cards grounded in obligation records and cited source text.
3. **Incident Clock**: A deterministic tool to determine filing deadlines from incident facts and one or more entity classes (`entity_classes`). Legal gating uses the structured `applicability.requires` keys on each obligation; prose conditions are shown to the user and never evaluated.

Current data status:
- Modelled obligations (11): CERT-In Directions 70B (2022), 7; DPDP Rules 2025 Rule 7, 3; SEBI CSCRF 2024 incident reporting, 1.
- Ingested but not modelled: RBI NBFC Cybersecurity Directions 2026. Three further SEBI reporting duties are recorded in `docs/OPEN_QUESTIONS.md` and not modelled.
- Benchmark: 37 dev scenarios, each with a clause quote verified against the page text. Labels are AI-authored and not yet reviewed by a compliance professional, so no accuracy figure should be quoted.
- Two readings are contested and recorded for counsel in `docs/DECISIONS.md`: the date from which SEBI CSCRF duties bind, and the DPDP Rule 7 commencement date.
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

## Data Directory Layout

- `data/raw/`: Verbatim primary source files (`.pdf`, `.txt`, `.meta.json`) tracked by `manifest.json`.
- `data/instruments/`: Regulatory instrument metadata definitions.
- `data/obligations/`: Atomic obligations extracted with exact verbatim citations.
- `data/entities/`: Versioned regulatory entity class taxonomy (`general.json`, `cert-in.json`, `rbi.json`, `sebi.json`, `dpdp.json`).
- `data/reference/`: Reference catalogs, such as `annexure_i.json` for CERT-In incident types.

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
