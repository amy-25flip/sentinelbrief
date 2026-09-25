# SentinelBrief

Indian cyber-regulatory compliance — obligation dataset, incident clock, filing copilot, and card feed

## Overview

SentinelBrief provides three main surfaces:
1. **Dataset**: Structured obligations parsed from regulatory texts.
2. **Card Feed**: A unified view of updates, filing deadlines, and changes across regulators.
3. **Incident Clock**: A tool to determine filing deadlines based on incident type and entity categorization.

Disclaimer: This tool is not legal advice and is not affiliated with any regulator.

## Prerequisites

- Python 3.13 (e.g. Python 3.13.15)
- [`uv`](https://docs.astral.sh/uv/) for Python environment and dependency management

## Setup & Installation

1. Clone or navigate to the repository:
   ```bash
   cd e:\SentinelBrief
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

- `data/raw/`: Verbatim primary source files (.pdf, .txt, .meta.json) tracked by `manifest.json`.
- `data/instruments/`: Regulatory instrument metadata definitions.
- `data/obligations/`: Atomic obligations extracted with exact verbatim citations.
- `data/entities/`: Versioned regulatory entity class taxonomy (`general.json`, `cert-in.json`, `rbi.json`, `sebi.json`, `dpdp.json`).
- `data/reference/`: Reference catalogs (e.g. `annexure_i.json` for CERT-In incident types).

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

## License

MIT
