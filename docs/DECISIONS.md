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

## 2026-09-25: RBI reverify exemption for CAPTCHA-blocked official PDFs

**Decision:** Manifest entries may carry `reverify_exemption` only with a non-empty reason, and `scripts/reverify_sources.py` accepts it only for official RBI hosts (`rbidocs.rbi.org.in` or `rbi.org.in`). Exempt entries print `SKIP <filename>: <reason>` and are counted as skipped, not failed.

**Reason:** RBI's official document server serves a CAPTCHA to automated clients, but the project owner downloaded `RBI_NBFC_Cybersecurity_Directions_2026.pdf` from the official site in a browser and the reviewer verified its hash, 47 pages, Adobe producer, EOF marker, no repair, and key text. Automated re-download cannot be the gate for this one source; human re-check is comparing the official download to sha256 `5b2432e53e1b1d1b500fb21ebe6176d28bcf3386543097b6c53aeb43ad860073`.

**Alternative rejected:** Marking all CAPTCHA-blocked sources as failed forever. That would force the project back toward mirrors or invented substitutes; the exemption is narrower and louder.

## 2026-09-25: DPDP Rules 2025 Commencement and Rule 7 Breach Intimation Modelling

**Decision:** Model DPDP Rules 2025 (`meity.dpdp-rules.2025`) using Notification No. G.S.R. 846(E) dated 2025-11-13.
- Gazette PDF page 24, Rule 1(4), says exactly: "Rules 3, 5 to 16, 22 and 23 shall come into force eighteen months after the date of publication of this Gazette." Counting eighteen calendar months from 13 November 2025 gives the conservative `valid_from: "2027-05-13"` for Rule 7.
- Rule 7(1) (intimation to affected Data Principals) and Rule 7(2)(a) (initial intimation to Data Protection Board) are modelled as `deadline.kind: "immediate"` ("without delay") with anchor `awareness`.
- Rule 7(2)(b) (detailed report to Board) is modelled as `deadline.kind: "relative"`, `PT72H`, anchor `awareness`, with an explicit note regarding the Board's power to allow a longer period upon written request.
- Applicability condition enforces that personal data must be involved (`personal_data_involved: true`); if `personal_data_involved` is missing/null, an Unknown question is generated.

**Alternative and reason:** Counsel could treat "after" as excluding the anniversary day and select 14 May 2027. The earlier date is retained pending counsel review because it never tells a user that the duty starts later than the conservative reading. Rule 7 wording is quoted in each obligation from Gazette PDF page 26.

## 2026-09-25: SEBI CSCRF Incident Reporting (RS.CO.S1) Multi-Anchor Modelling

**Decision:** Model SEBI CSCRF (`sebi.cscrf.2024`) incident reporting from Circular SEBI/HO/ITD-1/ITD_CSC_EXT/P/CIR/2024/113 dated 2024-08-20.
- PDF page 9 calls the dates a "glide-path for adoption of CSCRF provisions". Paragraph 17.1 says exactly: "For six categories of REs where cybersecurity and cyber resilience circular already exists – by January 01, 2025." Paragraph 17.2 says exactly: "For other REs where CSCRF is being issued for the first time – by April 01, 2025."
- Because those words describe a compliance glide path, not one universal in-force date, the conservative model uses the circular's issue date, 20 August 2024, as `valid_from` pending legal review.
- Standard RS.CO.S1 (page 123) / Annexure-O Section B.1 (page 200) requires notification within 6 hours of `noticing/detecting` or `being brought to notice` to SEBI (`mkt_incidents@sebi.gov.in`) and CERT-In.
- Modelled as `deadline.kind: "relative"`, `PT6H`, anchor `noticing`, with `alternative_anchors: ["detection", "brought_to_notice"]`.
- The engine uses the earliest available timestamp among noticing, detection, and brought-to-notice.

**Alternative and reason:** Duties may bind only from 1 January 2025 for the six categories with earlier circulars, and from 1 April 2025 for other REs. Category mapping is not yet encoded. Applying from issue avoids telling a user they owe less during the contested interval; confidence is therefore 0.7, not a claim that the interpretation is settled.

## 2026-09-25: SEBI incident-reporting scope is all REs (corrected 2026-10-04)

**Decision:** The SEBI incident-reporting duties bind all five CSCRF categories and the stock broker and depository participant roles.

**Text:** On PDF page 123 the applicability cell of row "RS.CO.S1, RS.CO.S2, RS.CO.S3" reads "All REs (Mandatory)". Annexure-O B.1 (page 200) says "experienced by REs".

**Correction:** An earlier version of this entry, and Review 7 finding J3, recorded a tension between a heading "MIIs and Qualified REs (Mandatory)" and Annexure-O. That was the reviewer's misreading of the extracted text, which prints each table cell after its row: "MIIs and Qualified REs (Mandatory)" is the cell of the row above (RS.MA.S5). The rendered PDF page shows this. There is no tension and no alternative reading to record.

## 2026-10-04: RBI Decision 1 — commencement on 31 July 2026

**Decision:** RBI obligations use `valid_from: 2026-07-31`.

**Text:** The Direction is dated "July 31, 2026" (PDF page 1), and paragraph 2 says, "These Directions shall come into force with immediate effect" (page 3).

**Alternative and safety:** A later operational date could be inferred from publication or implementation practice, but the text names none. Using the printed issue date is the earliest text-supported date and therefore never tells a user the duties began later.

## 2026-10-04: RBI Decision 2 — chapter-specific entity classes and refinement

**Decision:** Model `nbfc.bl_below_500cr`, `nbfc.bl_500cr_and_above`, `nbfc.middle_layer`, `nbfc.upper_layer`, `nbfc.top_layer`, plus additive role classes `nbfc.cic` and `nbfc.hfc`. Mark `nbfc` and `nbfc.base_layer` as needing refinement. A role class does not resolve its refinement family: only a held descendant that is neither a refinement class nor a role selects the category. An unresolved family produces one Unknown covering every affected duty, regardless of trigger type; exclusions and required additive roles are applied first.

**Text:** Paragraph 3 says Chapter III applies to "NBFCs-Base Layer (NBFCs-BL) with asset size below ₹500 crore, and Core Investment Companies (CICs)" (page 3); Chapter IV applies to "NBFCs-BL with asset size ₹500 crore and above" (page 3); Chapter V applies to "NBFCs-Top Layer (NBFCs-TL), NBFCs-Upper Layer (NBFCs-UL), and NBFCs-Middle Layer (NBFCs-ML) ... excluding CICs" (pages 3-4).

**Alternative and safety:** Treat generic `nbfc` as outside every specific chapter. Rejected because it silently says no duty where the category is merely unknown; asking for refinement never tells the user they owe less.

## 2026-10-04: RBI Decision 3 — CIC exclusion overrides layer

**Decision:** A profile holding `nbfc.cic` is excluded from all Chapter V obligations even if it also holds a Chapter V layer.

**Text:** Paragraph 3(2) assigns "Core Investment Companies (CICs)" to Chapter III (page 3), while paragraph 3(4) ends Chapter V scope with "excluding CICs" (page 4).

**Alternative and safety:** Let a positive Middle/Upper/Top match override CIC status. Rejected because it ignores the express exclusion and would misstate Chapter V; checking exclusions first respects the narrower text without suppressing Chapter III duties that may later be modelled.

## 2026-10-04: RBI Decision 4 — RBI cyber-incident gate is wider than Annexure I

**Decision:** Add a separate `rbi_cyber_incident` gate. An explicit attestation decides; otherwise an Annexure-I match establishes the RBI condition, while a non-match remains Unknown.

**Text:** Paragraph 4(7) defines a Cyber Incident as "A cyber event that adversely affects the cybersecurity of an information asset whether resulting from malicious activity or not" (page 4). The source note says it "includes cybersecurity incidents as well as IT incidents" (page 5).

**Alternative and safety:** Reuse the narrower CERT-In Annexure-I gate or infer false from unmatched text. Rejected because either could suppress an RBI duty; the independent Unknown never tells a user they owe less.

## 2026-10-04: RBI Decision 5 — paragraph 141 CERT-In notification has no deadline

**Decision:** Model the paragraph 141 CERT-In notification as `deadline.kind = none`: applicable, but neither a computed deadline nor time-critical.

**Text:** Paragraph 141 says, "The NBFC shall also pro-actively notify Indian Computer Emergency Response Team (CERT-In) regarding cyber incidents" (page 44). It states no duration or channel for this sentence.

**Alternative and safety:** Treat "pro-actively" as `immediate` or import CERT-In's own six-hour limit. Rejected because either invents timing in this RBI duty. The separate CERT-In Direction (ii) clock remains modelled where Annexure I applies, so no existing six-hour duty is removed.

## 2026-10-04: RBI Decision 6 — conservative Chapter V HFC redirection

**Decision:** For a Chapter V HFC, replace the RBI-recipient duty with a contested NHB duty at six hours from detection, confidence 0.5. Require both an HFC role and a Chapter V layer; do not extend the note to paragraph 28.

**Text:** The paragraph 141 note says, "In respect of Housing Finance Companies, cyber incidents shall continue to be reported to NHB and not RBI" (page 44). The preceding sentence says "within six hours of detection" (page 43) but the note itself gives no time limit or channel.

**Alternative and safety:** Give the NHB duty no deadline, or apply the note to Chapter IV too. Inheriting the surrounding six-hour clock is the conservative choice that does not tell a Chapter V HFC it has longer; Chapter IV extension remains an explicit open question rather than unsupported scope.

## 2026-10-04: RBI Decision 7 — detection is the sole RBI clock anchor

**Decision:** Paragraphs 28 and 141 use only `detection`; a missing detection timestamp produces an Unknown even when noticing is known.

**Text:** Paragraph 28 requires reporting "within six hours of detection" (page 18), and paragraph 141 repeats "within six hours of detection" (page 43).

**Alternative and safety:** Substitute CERT-In's "noticing ... or being brought to notice" anchor. Rejected because the RBI text does not offer it. Asking for detection preserves the written trigger and cannot silently postpone or erase the clock.

## 2026-10-04: SEBI Decision 1 - the portal filing shares the six-hour starting event

**Decision:** `incident-portal-24h` is `PT24H` from noticing, detection or being brought to notice, earliest known.

**Text:** "However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours." (page 123). Annexure-O B.1: "This information shall be shared to SEBI through the email ID mkt_incidents@sebi.gov.in within 6 hours and SEBI Incident Reporting Portal within 24 hours." (page 200).

**Alternative and safety:** 24 hours from the six-hour email. Rejected: the text does not say so, and that reading gives a later deadline. The chosen reading is the earlier one.

## 2026-10-04: SEBI Decision 2 - "all other" incidents: 24 hours from the same events (contested)

**Decision:** `other-incidents-24h` is `PT24H` from the same three events. Confidence 0.5.

**Text:** "All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours." (page 123). The sentence names no starting event.

**Alternative and safety:** 24 hours from classification, or from the end of the day. Neither is in the text and both are later. The earliest text-supported start is used, so the tool never shows a later deadline than a stricter reading would.

## 2026-10-04: SEBI Decision 3 - what "other" means, and when to ask

**Decision:** Structured key `sebi_other_cybersecurity_incident`. Annexure I matched: not applicable, the six-hour duties apply. Annexure I unresolved: the Annexure I question. Attested not Annexure I: the cyber-incident attestation decides, and when it is missing the engine asks "Is this a cybersecurity incident?".

**Text:** the six-hour sentence covers incidents "falling under CERT-In Cybersecurity directions"; the next sentence covers "All other cybersecurity incident(s)" (page 123).

**Alternative and safety:** treat every non-Annexure-I event as an "other" incident. Rejected: a hardware fault is not necessarily a cybersecurity incident, and the circular gives no definition to decide it from free text. Asking never tells a user they owe less.

## 2026-10-04: SEBI Decision 4 - Annexure-O A.1 criteria are not evaluated

**Decision:** Every Annexure I incident keeps the six-hour duty.

**Text:** Annexure-O A.1: "Any incident stated under CERT-In Cybersecurity directions and meeting below criteria shall be mandatorily reported within 6 hours" with four criteria (page 198).

**Alternative and safety:** apply six hours only when a criterion is met, 24 hours otherwise. Not modelled: the criteria ("severe nature", "large-scale") need judgement. Keeping six hours can only tell a user they owe more. Open question.

## 2026-10-04: SEBI Decision 5 - stock broker and depository participant are roles

**Decision:** Classes `sebi.stock_broker` and `sebi.depository_participant` are roles held in addition to a size category. Every duty that binds REs lists both roles, so a profile holding only a role still owes them.

**Text:** "Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours" (page 123).

**Alternative and safety:** require a size category before any SEBI duty applies. Rejected: a broker who has not picked a category would be told it owes nothing.

## 2026-10-04: SEBI Decision 6 - NCIIPC report has no computed deadline

**Decision:** `nciipc-protected-system-report` needs `uses_protected_systems` (true, false, or unknown, which asks) and a cybersecurity incident. Deadline kind `none`.

**Text:** "Additionally, the REs, whose systems have been identified as "Protected system" by NCIIPC shall also report the incident to NCIIPC." (page 124). Annexure-O 3.1: "shall report and inform the incident to NCIIPC in a timely manner" (page 200).

**Alternative and safety:** model "timely" as six or 24 hours. Rejected: the text gives no number. The duty is shown as applicable with no clock.

## 2026-10-04: SEBI Decision 7 - Table 36 clocks run from the report or being brought to notice

**Decision:** Four duties (`P3D`, `P7D`, `P30D`, `P45D`) with anchor `reported` (new fact `when_reported_to_sebi`) and alternative anchor brought to notice, earliest known, counted from the timestamp. If neither is known the engine asks. They apply whenever a SEBI incident-reporting duty applies. The report time is not used for "law as of" unless it is the only time given.

**Text:** Table 36 heading: "Timeline for Submission (from the date of reporting the incident or being brought to notice about the incident)"; rows "Interim Report* 3 Days", "Mitigation measure 7 Days", "Root Cause Analysis (RCA) report** 30 Days#", VAPT "45 days" (page 201). Footnote: "Additional time may be provided by SEBI for the submission of RCA on a case-by-case basis on request of the RE" (page 202).

**Alternative and safety:** count whole calendar days from the date, which ends later in the day. The timestamp reading is the earlier one. Open question.

## 2026-10-04: SEBI Decision 8 - forensic and quarterly reports are not modelled

**Decision:** Not modelled.

**Text:** "the maximum period for the submission of forensic audit report shall be 75 days from date of reporting of incident" for incidents classified High or Critical (page 203); quarterly reports "within 15 days from the quarter ended June, September, December and March" (page 124).

**Reason:** the forensic duty depends on a severity classification the tool does not hold; the quarterly report is periodic, not incident-driven. Both are open questions.

## 2026-10-04: Author-written evidence lists move to `suggested_evidence`

**Decision:** Every existing `normalized.evidence_required` list is renamed to `normalized.suggested_evidence`. `evidence_required` stays in the schema for evidence the cited text itself demands, and the obligation validator rejects any item that is not quoted from `text_verbatim`.

**Reason:** Review 5 found that none of the listed items is in the source text. The page already labelled them as suggestions; the data now says the same thing, and a future author cannot put an invented item back into the source-stated field without the gate failing.

**Alternative rejected:** deleting the lists. They are useful operational prompts once clearly separated from what the law says.
