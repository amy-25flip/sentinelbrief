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
