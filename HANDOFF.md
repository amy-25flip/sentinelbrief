# Review 5 Fix Handoff

## 1. Gate output

Commands were run with `UV_CACHE_DIR=E:\SentinelBrief\.uv-cache-work` because uv's default cache path under `C:\Users\Admin` is locked in this sandbox. `pytest` was run with `PYTEST_ADDOPTS='--basetemp=.pytest_tmp_review5 -o cache_dir=.pytest_cache_review5'` because the default `.pytest_tmp` / `.pytest_cache` directories are stale and locked. `pyproject.toml` was not changed.

`uv run --no-sync pytest -q`

```
172 passed, 1 deselected, 1 warning in 5.28s
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
Scenarios passed:   17/17  Wilson 95% CI [81.6%, 100.0%]
Deadlines matched:  11/11  Wilson 95% CI [74.1%, 100.0%]
Adversarial passed: 14/14
Note: one instrument (CERT-In) is loaded, so regulator identification is trivial.
```

## 2. Review 5 fixes

- G1: Replaced the truncated SEBI PDF with `.staging/real_sources/SEBI_CSCRF_Circular_2024-08-20.COMPLETE.pdf`. Regenerated metadata. `text_sha256` stayed `a184672544ce08f82adf0cae53b73fbdfb1983ae5f5d0d04766307d8b1c2b548`; source bytes are now `bd9ddb68bb49b9a92771ff01ed3138e01f0962b383e9ff643008b729290fc85d`, size `3177522`.
- G2: Raw provenance now rejects PDFs without a trailing `%%EOF` or PDFs PyMuPDF opens as repaired, with the same documented exemption path as the authenticity gate.
- G3: `BaseFetcher` writes `fetched_by: "BaseFetcher"`; `verify_raw_dir` now errors when a current manifest entry has neither `fetched_by` nor `acquired_by`. Existing CERT-In entries now disclose the Checkpoint 1 manual/script gap.
- G4: `scripts/reverify_sources.py` respects robots.txt by default and has `--ignore-robots` for explicit reviewer use. Unit tests cover `main()` exit codes.
- G5: Regulatory card grounding now trusts only source-derived text and rendered numeric durations. Facts present only in `evidence_required` are rejected.
- G6: Obligation detail pages now label the field as "Suggested evidence (not stated in the source text)" and explain that it is builder-authored, not quoted legal text.
- G7: DPDP and SEBI manifest/instrument records now state that `retrieved_at=2026-09-25T00:00:00Z` is date-precision only, not a verified exact timestamp.
- G8: `docs/OPEN_QUESTIONS.md` records the DPDP Rule 1 commencement structure and keeps `in_force_from` null until whole-document modelling.

## 3. Current repo state, with proof

- Modelled obligations remain CERT-In only: `validate_all` reports `Total Obligations: 7`, `Valid: 7`, `Invalid: 0`.
- Dev benchmark remains 17 CERT-In scenarios: scorer reports `17/17`, Wilson `[81.6%, 100.0%]`.
- DPDP and SEBI real PDFs are ingested but unmodelled; RBI remains blocked, not substituted.
- `benchmark/REVIEW_PACKET.md` was not regenerated in this round because scenarios did not change.
- Live source reverify was not run in this round because the user explicitly said not to use the network.

## 4. Not done or still open

- No DPDP, SEBI, or RBI obligations/scenarios were authored, by design.
- All current `evidence_required` values remain builder-authored suggestions and need removal, source-based authorship, or compliance-professional review before they can be presented as requirements.
- DPDP and SEBI effective dates remain `null` in instrument records pending whole-document review.
- Benchmark labels remain AI-authored and need external compliance review.

## 5. Least sure

1. The EOF/repair PDF gate is a useful completeness check, but it is not proof of regulator authenticity.
2. The card grounding verifier now catches hard factual drift from builder-authored fields, but softer legal completeness still needs human review.
