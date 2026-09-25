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

---

Decisions below were made during Review 1 (the reviewer agent, 2026-09-24). See REVIEW_LOG.md for the evidence behind each.

## 2026-09-24: Free text can never conclude an incident is not reportable

**Decision:** Whether an incident is a CERT-In Annexure I type is decided only by (a) structured selection of the 20 listed types, (b) an unambiguous named-type match on word boundaries, or (c) an explicit user attestation that it is NOT Annexure I. Everything else is an Unknown the user must answer, with suggestions.

**Reason:** A false "not reportable" costs a missed 6-hour filing; a false "reportable" costs a question. Keyword lists cannot be complete (real types x and vi contain no attack vocabulary).

**Alternative rejected:** Broader keyword lists (still wrong in both directions); an LLM classifier (non-deterministic, and incident text should not leave the machine by default).

## 2026-09-24: New deadline kind `retention`; `alternative_anchors` for joined triggers

**Decision:** Storage duties (Directions (iv), (v), (vi)) use `deadline.kind = "retention"` and never produce an incident deadline. Where a clause joins triggers with "or" (Direction (ii): "noticing ... or being brought to notice"), the obligation carries `anchor` plus `alternative_anchors`; the engine starts the clock at the earliest known trigger.

**Reason:** `relative` + `occurrence` produced a fake 2031 deadline. "Earliest trigger" is a conservative reading, not stated in the text, so it is recorded in `confidence_reason` and can be revisited.

## 2026-09-24: Law is evaluated as of the incident date

**Decision:** `evaluate()` takes `as_of` (default: earliest known incident timestamp, in IST) and filters obligations by `valid_from`/`valid_to`. The result reports `law_as_of`.

**Reason:** Brief principle 5. Obligations, penalties and deadlines change; "what applied then" is what an auditor asks.

## 2026-09-24: Unknown entity class and missing data raise

**Decision:** The engine refuses to run with an unknown entity class or an empty/missing obligation set.

**Reason:** The failure mode of a compliance tool must be a loud error, never a quiet "nothing applies".

## 2026-09-24: Only a person may set `human_verified`

**Decision:** AI-authored records are `machine_checked`. The validator rejects `human_verified` without a named reviewer or with an AI-looking reviewer name.

**Reason:** Trust labels must mean what they say. Expert label validation is still an open human task (OPEN_QUESTIONS.md).

## 2026-09-24: Evidence is never overwritten

**Decision:** When a fetched regulatory document changes, the previous bytes are kept as `<stem>.<sha8><ext>` and its manifest entry becomes `superseded`. Daily data feeds (KEV, EPSS) are exempt (`keep_history = False`). A corrupt manifest raises instead of being reset.

**Reason:** Brief section 7 and principle 6. A citation is only as good as the ability to reproduce what the source said on the day.

## 2026-09-24: Extraction is code, verified on every run

**Decision:** `extract/pdf_text.py` generates the stored text (LF line endings) and metadata; `verify/raw_provenance.py` re-extracts and compares on every `validate_all`. PyMuPDF version drift is a warning, any other mismatch is an error.

**Reason:** The stored text is what citations point into; it must be reproducible from the PDF.

## 2026-09-24: htmx is vendored

**Decision:** `web/static/htmx.min.js` (htmx 2.0.4, sha256 `e209dda5c8235479f3166defc7750e1dbcd5a5c1808b7792fc2e6733768fb447`) is served locally.

**Reason:** An incident workspace should not load third-party scripts, and the previous tag was unpinned and had no integrity check.

## 2026-09-24: MSME extension notice ingested

**Decision:** CERT-In's notice of 27 Jun 2022 (`cert-in.directions-70b.msme-extension.2022`, sha256 `f0a2805f2a3bd0745560d417ffb6d41bf2cfe9920a5fd8a45b806ff10d61979f`) is stored as a primary source. It moves effectiveness to 25 Sep 2022 for MSMEs and for Direction (v)(a),(f). It is not modelled beyond a caveat for incidents before that date.

**Reason:** Read from the primary PDF. It does not change any current (post Sep 2022) result.

## 2026-09-24: Benchmark labels assert as-of, citation and not-applicable states

**Decision:** The benchmark verifies expected citation `instrument_id`/`paragraph_ref` against the obligation record, requires expected `not_applicable` obligations to appear in the engine's `not_applicable` list (not merely be absent from `applicable_obligations`, which an unresolved unknown also satisfies), and asserts the labelled `expected.law_as_of`. The scorer does NOT force `as_of` from `law_snapshot_date`.

**Reason:** A scenario label is a contract. `law_snapshot_date` pins the dataset version and the evaluation time; the law that applies is the law as of the *incident* date (principle 5). Forcing the snapshot date as `as_of` (proposed in Review 2) applies today's law to old incidents: a 2021 incident evaluated with a 2026 snapshot gets the 2022 Directions. The pre-effective-date scenario now uses today's snapshot with a 2021 incident, and a mutation test proves that ignoring the incident date is caught.

**Alternative rejected:** Passing `law_snapshot_date` as `as_of` (Review 2): it hides exactly the as-of regression it was meant to catch.

---

## 2026-09-25: Withdrawn Checkpoint 2 DPDP/SEBI/RBI modelling decisions

**Decision:** The previous Checkpoint 2 entries for DPDP commencement, DPDP "without delay" modelling as `relative` without a duration, and multi-regulator DPDP/RBI/SEBI clocks are withdrawn.

**Reason:** Review 4 found the source PDFs and derived obligations/scenarios were fabricated. The real DPDP and SEBI PDFs are now ingested as raw evidence only. No DPDP, SEBI, or RBI obligations, scenarios, labels, or legal clocks are modelled in this fix round.

**Alternative rejected:** Keeping the decisions as historical interpretations. That would leave false legal claims in the project record.

## 2026-09-25: Immediate deadline kind

**Decision:** `deadline.kind = "immediate"` represents "without delay" duties. The engine never computes a fixed clock for `immediate`; applicable duties are returned in `ClockResult.time_critical` and rendered under "Do without delay". A `relative` deadline with no `duration_iso8601` is a data error and becomes an Unknown.

**Reason:** "Without delay" is a real legal timing concept but has no numeric duration. A missing duration on a relative deadline is different: it is malformed data and must fail loudly.

**Alternative rejected:** Reusing `relative` with a null duration, which silently hid data errors.

## 2026-09-25: Raw source authenticity gate

**Decision:** Raw provenance validation rejects PDFs whose producer and creator metadata are both empty unless the manifest carries a documented `authenticity_exemption`. Synthetic test fixtures can switch the check off explicitly.

**Reason:** The fabricated Checkpoint 2 PDFs had blank metadata and were generated in-repo. This check is not proof of authenticity, but it catches that failure mode.

**Alternative rejected:** Trusting the manifest hash alone. A hash only proves stable bytes, not that the bytes came from the regulator.

## 2026-09-25: Generated-source tripwire and live reverify tool

**Decision:** Tests now fail if `scripts/` or `src/` contain PyMuPDF page/text-generation calls used to build primary-source PDFs. `scripts/reverify_sources.py` re-downloads manifest URLs into a temp directory with `BaseFetcher` and compares SHA-256; its live pytest wrapper is marked `live`.

**Reason:** Primary evidence must come from regulator bytes, not generated local PDFs. Reviewers also need a repeatable way to re-check source URLs outside offline test runs.

## 2026-09-25: Provisional RBI and DPDP entity taxonomy

**Decision:** `data/entities/rbi.json` and `data/entities/dpdp.json` remain usable taxonomy scaffolding but are documented as provisional. SEBI categories were replaced with the five CSCRF category names read from the real circular; thresholds and scoped entity lists are not modelled.

**Reason:** The entity hierarchy is useful for UI/testing, but several dates and descriptions have not been re-verified against primary text after Review 4.

## 2026-09-25: Curated but grounded card summaries

**Decision:** Regulatory card summaries remain hand-curated deterministic text, but a grounding verifier rejects card bodies that introduce numbers, durations, email addresses, phone numbers, or named bodies absent from the cited source text or normalized record.

**Reason:** The brief preferred structured templates, but concise cards need readable wording. The verifier prevents hard factual drift while keeping the current deterministic feed.

**Alternative rejected:** Free prose with only length tests; that already allowed unsupported sentences.

## 2026-09-25: Complete PDF and acquisition-marker gates

**Decision:** Raw provenance validation now rejects PDFs that do not end with `%%EOF` or that PyMuPDF opens only after repair, unless the manifest carries a documented exemption. Every current manifest entry must also carry either `fetched_by` or `acquired_by`; `BaseFetcher` writes `fetched_by: "BaseFetcher"` for new pipeline downloads.

**Reason:** Review 5 found the stored SEBI PDF was a truncated reviewer-acquired copy. Hash and text checks passed because the extracted text happened to match, so completeness and acquisition-path checks need to be first-class gates.

## 2026-09-25: Evidence suggestions are not source-stated requirements

**Decision:** `normalized.evidence_required` is retained for now but rendered as "Suggested evidence (not stated in the source text)" with a note that these are builder-authored operational suggestions, not quoted legal requirements.

**Reason:** Review 5 found all current values are not stated in the CERT-In Directions text. Deleting or reauthoring them needs a separate source/professional review; the immediate fix is to stop presenting them as legal requirements.

## 2026-09-25: Card grounding source boundary tightened

**Decision:** Regulatory card hard facts may be grounded only in source-derived text (`text_verbatim`, citation excerpt, paragraph reference) plus rendered numeric deadline durations from `duration_iso8601`. Builder-authored normalized fields such as action, actor, trigger text and evidence suggestions no longer ground card facts.

**Reason:** A previous invented card sentence came from `evidence_required`; trusting builder-authored fields would let that failure repeat.
