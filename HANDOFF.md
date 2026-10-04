# Review 6 Fix Handoff

## 1. Gate output

Commands were run with `UV_CACHE_DIR=E:\SentinelBrief\.uv-cache-work` because uv's default cache path under `C:\Users\Admin` is locked in this sandbox. `pytest` was run with `PYTEST_ADDOPTS='--basetemp=.pytest_tmp_review6_final -o cache_dir=.pytest_cache_review6_final'` because the default `.pytest_tmp` / `.pytest_cache` directories are stale and locked. `pyproject.toml` was not changed. The temporary pytest directory was removed after the run. Live source reverify was not run because this task explicitly said not to use the network.

`uv run --no-sync pytest -q`

```
........................................................................ [ 40%]
........................................................................ [ 80%]
..................................                                       [100%]
============================== warnings summary ===============================
.venv\Lib\site-packages\fastapi\testclient.py:1
  E:\SentinelBrief\.venv\Lib\site-packages\fastapi\testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
178 passed, 1 deselected, 1 warning in 5.20s
```

`uv run --no-sync ruff check src/ tests/ benchmark/ scripts/`

```
All checks passed!
```

`uv run --no-sync ruff format --check src/ tests/ benchmark/ scripts/`

```
46 files already formatted
```

`uv run --no-sync mypy src/sentinelbrief/`

```
pyproject.toml: note: unused section(s): module = ['fitz.*']
Success: no issues found in 28 source files
```

`uv run --no-sync python -m sentinelbrief.verify.validate_all`

```
Running raw-source provenance checks...
Raw-source provenance passed.
Running schema validation...
Schema validation passed.
Running obligation and citation validation...

Validation Summary:
Total Obligations: 7
Valid: 7
Invalid: 0
Warnings: 0

All obligations and citations passed validation successfully!
```

`uv run --no-sync python benchmark/runner/scorer.py --split dev`

```
================================================================
BENCHMARK RESULTS (split: dev)
================================================================
Scenarios passed:   17/17  Wilson 95% CI [81.6%, 100.0%]
Deadlines matched:  11/11  Wilson 95% CI [74.1%, 100.0%]
Adversarial passed: 14/14
----------------------------------------------------------------
  [PASS] cert-in-ambiguous-anchor [ADVERSARIAL]
  [PASS] cert-in-attack-on-application [ADVERSARIAL]
  [PASS] cert-in-attack-on-servers [ADVERSARIAL]
  [PASS] cert-in-before-directions-effective [ADVERSARIAL]
  [PASS] cert-in-brought-to-notice [ADVERSARIAL]
  [PASS] cert-in-cloud-outage-not-assumed [ADVERSARIAL]
  [PASS] cert-in-data-breach-unknown-time
  [PASS] cert-in-detection-time-only [ADVERSARIAL]
  [PASS] cert-in-government-org [ADVERSARIAL]
  [PASS] cert-in-nbfc-ransomware
  [PASS] cert-in-non-annexure-i-type [ADVERSARIAL]
  [PASS] cert-in-noticed-before-brought [ADVERSARIAL]
  [PASS] cert-in-retention-is-not-a-deadline [ADVERSARIAL]
  [PASS] cert-in-unattested-hardware-failure [ADVERSARIAL]
  [PASS] cert-in-utc-input [ADVERSARIAL]
  [PASS] cert-in-vps-provider
  [PASS] cert-in-wrong-entity-trap [ADVERSARIAL]
================================================================
Note: one instrument (CERT-In) is loaded, so regulator identification is trivial.
```

## 2. H1 and H2 status

- H1: FIXED. The human-acquired RBI PDF is copied to `data/raw/RBI_NBFC_Cybersecurity_Directions_2026.pdf`; extracted text and metadata exist; manifest records URL, sha256 `5b2432e53e1b1d1b500fb21ebe6176d28bcf3386543097b6c53aeb43ad860073`, size `552900`, `acquired_at`/`retrieved_at`, `acquired_by`, acquisition note, and `reverify_exemption`. `validate_all` proves provenance/authenticity/completeness gates pass.
- H2: FIXED. `scripts/reverify_sources.py` now prints `SKIP` for documented RBI-host exemptions, counts skipped entries in the summary, rejects empty exemption reasons, rejects non-RBI exemption hosts, and still fails non-exempt fetch/hash failures.

## 3. RBI facts recorded, not modelled

- Instrument only: `data/instruments/rbi.nbfc-cyber.2026.json`.
- No RBI obligation, scenario, benchmark label, or clock output was authored.
- Text-confirmed facts recorded in docs: paragraph 2 immediate effect; paragraph 3 applicability; paragraphs 28 and 141 six hours from detection; paragraph 141 CERT-In proactive notification; Chapter VI "Repeal and Other Provisions" / "A. Repeal and Saving"; no incident-reporting "or occurrence" wording in paragraphs 28 or 141.

## 4. Still open

- DPDP, SEBI, and RBI remain raw evidence only and unmodelled.
- RBI chapter/entity scoping must be read carefully before modelling; `data/entities/rbi.json` is still provisional.
- Benchmark labels remain CERT-In only and AI-authored, pending external compliance review.

# Review 7 and Review 8 fixes (2026-10-04)

The fixer (Codex) made the code and data changes in commits `831b353` and the Review 8 follow-up. Codex could not write `HANDOFF.md` or `README.md` in its sandbox on two attempts, so the reviewer (the reviewer agent) wrote this section and the README status lines. Sections above this line describe the earlier Review 6 state and are out of date.

## Gate output (`python scripts/check.py`, run by the reviewer)

```
PASS  pytest             190 passed, 1 deselected, 1 warning
PASS  ruff check         All checks passed!
PASS  ruff format        46 files already formatted
PASS  mypy (strict)      Success: no issues found in 28 source files
PASS  validate_all       All obligations and citations passed validation successfully!
PASS  benchmark dev      Scenarios passed:   37/37  Wilson 95% CI [90.6%, 100.0%]
ALL GATES PASSED
```

## Findings

- J1 FIXED: the engine gates on `applicability.requires`; prose conditions are never evaluated. Scenarios `sebi-mii-hardware-failure-unattested` and `sebi-mii-attested-not-annexure-i`.
- J2 FIXED: SEBI `valid_from` is the issue date 2024-08-20; paragraphs 17.1 and 17.2 (PDF page 9) quoted; reading recorded as contested.
- J3 FIXED: SEBI scope tension and three unmodelled duties recorded in DECISIONS and OPEN_QUESTIONS.
- J4 FIXED: unit and mutation tests added (178 to 190 tests).
- J5 FIXED: `source_quotes` on all 37 dev scenarios, verified against page text.
- J6 FIXED: `IncidentProfile.entity_classes` in the engine, scorer, API and form. Scenario `sebi-mii-also-data-fiduciary-2027`.
- J7 FIXED: `docs/RBI_NBFC_PREPARATION.md` neutralised, pages verified.
- J8, J9 FIXED: DECISIONS entries carry quotes, pages and alternatives.
- K1 FIXED: ten scenarios now also quote the clause their outcome turns on.
- K2 FIXED by the reviewer (this section and README).
- J10 OPEN: the builder's Checkpoint 2B handoff. See `BUILD_BRIEF_CHECKPOINT3.md`, WP-0.

## Still open

- RBI NBFC Direction and three SEBI duties are not modelled.
- Benchmark labels are not reviewed by a compliance professional.
- Two contested readings await counsel (SEBI binding date; DPDP 13 or 14 May 2027).
- Live source reverify was last run on 2026-09-25, not in this round.
