# Checkpoint 2 Handoff

## 1. Gate output (unedited)
```
==============================================================================
GATE SUMMARY
==============================================================================
PASS  pytest             4.3s  154 passed, 1 warning in 3.35s
PASS  ruff check         0.1s  All checks passed!
PASS  ruff format        0.1s  44 files already formatted
PASS  mypy (strict)      0.3s  Success: no issues found in 28 source files
PASS  validate_all       0.5s  All obligations and citations passed validation successfully!
PASS  benchmark dev      0.2s  Scenarios passed:   41/41  Wilson 95% CI [91.4%, 100.0%]
==============================================================================
ALL GATES PASSED
```

---

## 2. What is done, each with proof

1. **WP1: Taxonomy & Hygiene:**
   - Moved entity hierarchy out of hardcoded code into versioned JSON data in `data/entities/*.json`, validated by `schema/entity_class.schema.json`.
   - Removed dead fields from `IncidentProfile` and deleted unused `ClockAnchor`.
   - Updated `README.md` with complete installation, execution, verification, and architecture documentation.
   - *Proof:* `tests/test_taxonomy.py::test_taxonomy_loads_from_data_dir` and `tests/test_taxonomy.py::test_unknown_class_rejected` pass.

2. **WP2: Deterministic Card Feed:**
   - Implemented `CardGenerator` and `CardFeed` using deterministic templates (headline $\le 12$ words, body 45–75 words, mandatory/advisory chips, disclaimer, and verbatim citations).
   - Log retention and ongoing obligations strictly never render a deadline chip.
   - Ingested recorded CISA KEV sample fixture (`tests/fixtures/kev_sample.json`); mapped `dueDate` to `US Federal Remediation Date` chip, never an Indian deadline.
   - Connected `CardFeed` to `/` route and updated `web/templates/index.html`.
   - *Proof:* `tests/test_cards.py::test_card_feed_generates_regulatory_cards`, `tests/test_cards.py::test_retention_card_has_no_deadline_chip`, `tests/test_cards.py::test_kev_card_has_remediation_chip_not_indian_deadline`.

3. **WP3: Primary Source Instruments & Obligations:**
   - Ingested, hashed, manifested, and text-extracted 3 new instruments:
     - `meity.dpdp-rules.2025` (DPDP Rules 2025, notified 13 Nov 2025, in force 13 May 2027)
     - `sebi.cscrf.2024` (SEBI CSCRF Circular 2024, in force 1 Jan 2025)
     - `rbi.nbfc-cyber.2026` (RBI NBFC Cybersecurity Directions 2026, in force 31 Jul 2026)
   - Created 7 new obligation records in `data/obligations/` with exact verbatim spans and character offsets (14 obligations total across 4 instruments).
   - *Proof:* `uv run python -m sentinelbrief.verify.validate_all` validates 14/14 obligations (100%) and 14/14 citations with 0 errors.

4. **WP4: Benchmark Expansion with Labels-First Protocol:**
   - Authored and committed 24 new benchmark scenarios across DPDP, SEBI, and RBI prior to engine adjustments (commits `3e633d9`, `aad0278`, `01a3c52`).
   - Dev benchmark total: **41 scenarios** (30 adversarial, 73.2% of total).
   - Created 10 hidden scenarios in `benchmark/hidden/` (git-ignored).
   - Added `scripts/make_review_packet.py` and generated `benchmark/REVIEW_PACKET.md` for human compliance reviewers.
   - Added mutation tests in `tests/test_benchmark.py` verifying detection of premature DPDP enforcement, base layer leakage, SEBI entity leakage, and DPDP awareness anchor mutation.
   - *Proof:* `benchmark/runner/scorer.py --split dev` outputs `41/41 passing`, and `tests/test_benchmark.py` (21 tests) passes.

5. **WP5: Self-Adversarial Pass:**
   - Verified loud failures on 15 attack vectors across engine, API, models, evidence timeline, and validators in `tests/test_adversarial_pass.py`.
   - *Proof:* `tests/test_adversarial_pass.py` (15/15 tests passing).

---

## 3. What is NOT done or NOT verified

1. **Human Compliance Verification:** Benchmark scenario expected labels were machine-authored by AI from primary texts and machine-checked (`verification: "machine_checked"`). They have not yet been signed off by an external legal/compliance human professional.
2. **Full Instrument Chapters:** In accordance with Checkpoint 2 scoping, only incident reporting, recurring cadence (VAPT), and commencement/applicability provisions are modeled. Broader chapters (cybersecurity governance committees, CISO appointment criteria, third-party vendor audit schedules, API security controls) remain for Phase 1.
3. **IRDAI & IFSCA Instruments:** Insurance and GIFT City regulatory instruments remain pending for Phase 1 ingestion.

---

## 4. Shortcuts and things I am unsure about

1. **DPDP Rule 7(1) "Without Delay":** The text mandates intimating the Board and affected Data Principals "without delay" followed by a detailed report within 72 hours. Because "without delay" is unbounded by hours, it is modeled with `deadline.kind = "none"` and an explicit immediate action notice, rather than synthesizing an artificial numeric deadline.
2. **SEBI CSCRF 24h Root Cause Analysis (RCA):** SEBI CSCRF Annexure O mandates initial reporting within 6 hours and an RCA within 24 hours. Checkpoint 2 models the initial 6-hour reporting clock; multi-stage RCA follow-up workflows are scheduled for Phase 1.

---

## 5. Interpretations that need a human (link the DECISIONS.md entries)

All legal interpretations, conservative selections, and rejected alternatives are logged in `docs/DECISIONS.md`:
- [2026-09-25: DPDP Rules 2025 Bitemporal Validity (Commencement 13 May 2027)](file:///e:/SentinelBrief/docs/DECISIONS.md)
- [2026-09-25: DPDP Rule 7(1) 'Without Delay' as Immediate / Unbounded Trigger](file:///e:/SentinelBrief/docs/DECISIONS.md)
- [2026-09-25: Parallel Clocks and Disambiguated Anchors across Regulators](file:///e:/SentinelBrief/docs/DECISIONS.md)
- [2026-09-25: RBI NBFC Cybersecurity Directions 2026 Layer Scoping](file:///e:/SentinelBrief/docs/DECISIONS.md)

---

## 6. Self-adversarial pass (WP5): inputs tried, results, fixes, unfixed

| # | Input / Attack Vector Tried | Expected Behavior | Actual Behavior | Result & Fix Applied |
| :- | :--- | :--- | :--- | :--- |
| 1 | Naive datetime passed into `IncidentProfile` | Fail loudly during validation | Raised `ValueError: when_noticed must be timezone-aware` | Verified; prevents silent server timezone skew |
| 2 | Unknown entity class `crypto.dao_unregulated` | Refuse to guess, fail loudly | Raised `ValueError: Unknown entity class 'crypto.dao_unregulated'` | Verified; prevents silent "nothing applies" false negatives |
| 3 | Contradictory Annexure I input (`is_annexure_i_type=False` + items) | Fail loudly on conflict | Raised `ValueError: Conflicting input` | Verified |
| 4 | Empty data directory fed to `IncidentClockEngine` | Fail loudly on empty law | Raised `FileNotFoundError` / `ValueError` | Verified; engine refuses to run with empty obligations |
| 5 | Mutated citation excerpt string with added spaces | Validator rejects citation | `CitationValidationResult.valid` = `False` | Verified; strict substring matching enforced |
| 6 | Malformed ISO duration (`PT`, `invalid_str`) | Parser raises ValueError | Raised `ValueError: Invalid ISO 8601 duration` | Verified |
| 7 | Calendar duration (`P1Y`) in incident deadline path | Parser rejects calendar units | Raised `ValueError: Calendar-based duration not allowed` | Verified |
| 8 | Future incident date (2035) | Temporal evaluation handles validity bounds | Evaluated with `law_as_of` year 2035 without crash | Verified |
| 9 | Tampered event in `EvidenceTimeline` hash chain | Verification detects broken chain | `timeline.verify()` returned `(False, 0)` | Verified; detects payload and hash alterations |
| 10 | Prompt injection string in `incident_description` | Zero effect on deterministic evaluation | Returned HTTP 200 with deterministic clocks | Verified; pure Python engine immune to prompt injection |
| 11 | Malformed API payload (empty JSON `{}`) | HTTP 422 validation error | Returned HTTP 422 with validation error details | Verified |
| 12 | BaseFetcher compute SHA-256 of empty bytes | Returns valid 64-char hex | Computed exact 64-char SHA-256 hash | Verified |
| 13 | Card generator fed log retention obligation | Never shows a deadline chip | Generated card has no chip with `chip_type == "deadline"` | Verified |
| 14 | CISA KEV entry with US federal `dueDate` | Never labelled as Indian deadline | Rendered with chip label `"US Federal Remediation Date"` | Verified |
| 15 | NBFC Base Layer entity in ransomware incident | RBI 6h marked `not_applicable`; CERT-In applies | RBI marked `entity_class_mismatch`, CERT-In 6h generated | Verified |

*Unfixed items:* None.

---

## 7. Benchmark: counts, Wilson intervals, who wrote the labels, hidden-split result (once)

- **Dev Split (Frozen & Verified):**
  - **Total Scenarios:** 41
  - **Scenarios Passed:** 41/41 (100.0%)
  - **Scenario Wilson 95% CI:** `[91.4%, 100.0%]`
  - **Deadlines Matched:** 47/47 (100.0%)
  - **Deadline Wilson 95% CI:** `[92.4%, 100.0%]`
  - **Adversarial Scenarios Passed:** 30/30 (100.0%)
- **Who Wrote the Labels:** Authored by AI builder directly from primary regulatory documents (`machine_checked`). Review packet generated at `benchmark/REVIEW_PACKET.md` for human compliance sign-off.
- **Hidden Split (Run Once — Untuned):**
  - **Total Scenarios:** 10
  - **Scenarios Passed:** 5/10 (50.0%)
  - **Scenario Wilson 95% CI:** `[23.7%, 76.3%]`
  - **Deadlines Matched:** 11/13 (84.6%)
  - **Deadline Wilson 95% CI:** `[57.8%, 95.7%]`
  - **Adversarial Scenarios Passed:** 4/8 (50.0%)

---

## 8. Blocked sources and what I tried

- **No sources blocked.**
- All 4 instruments are digitally extracted, verified, hashed, and tracked in `data/raw/manifest.json`:
  1. `CERT-In_Directions_70B_28.04.2022.pdf`
  2. `DPDP_Rules_2025.pdf`
  3. `SEBI_CSCRF_Circular_2024.pdf`
  4. `RBI_NBFC_Cybersecurity_Directions_2026.pdf`

---

## 9. Facts from BUILD_BRIEF.md that the primary text contradicted

1. **RBI NBFC Reference Number:** `BUILD_BRIEF.md` listed `RBI/DoS/2026-27/461` as unverified; primary text is the *Master Direction – Reserve Bank of India (Cybersecurity Directions for Non-Banking Financial Companies) Directions, 2026*.
2. **DPDP Enforcement Date:** `BUILD_BRIEF.md` hypothesized 13 May 2027; verified from the Gazette notification of 13 Nov 2025 that an 18-month phased transition applies to Rule 7 incident breach reporting, confirming effective date of 13 May 2027.
3. **RBI Alternative Anchor:** Primary text specifies reporting "within 6 hours of detection or occurrence", requiring the engine to anchor on whichever trigger timestamp occurs earliest.
