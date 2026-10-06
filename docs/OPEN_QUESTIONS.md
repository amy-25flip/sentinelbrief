# Open Questions

Things needing a human or a primary-source check.

---

## Regulatory Sources

- [x] **CERT-In Directions PDF:** Read from the stored primary text in Review 2; the seven current obligation records are traceable to verbatim spans, subject to the open interpretation questions below.
- [x] **CERT-In MSME extension (27 Jun 2022):** Read from the primary PDF in Review 1. Effective 25 Sep 2022 for MSMEs, and for Direction (v)(a),(f). Ingested; only a pre-Sep-2022 caveat is modelled.
- [ ] **Does "MSME" apply to the target users (small NBFCs, co-op banks)?** Only matters for incidents before 25 Sep 2022. Low priority.
- [ ] **"Earliest of noticing / brought to notice":** conservative reading of Direction (ii); the text does not say "earlier". Ask a compliance professional whether CERT-In reads it that way in practice.
- [ ] **Independent label review:** all 51 benchmark labels, including the 14 RBI labels written by the reviewer before implementation, were authored by AI agents against primary text. An external compliance professional should review them before any accuracy figure is quoted.
- [ ] **Which CERT-In Annexure I terms count as unambiguous?** `data/reference/annexure_i.json` strong/weak terms were chosen conservatively; have a practitioner review them.
- [ ] **FAQ Q10 and non-Annexure incidents:** The FAQ says intermediaries should also report incident types not listed in the CERT-In Rules/Directions annexures considering nature, severity and impact. The current clock only models the explicit mandatory Direction (ii) Annexure I 6-hour obligation. Ask counsel whether and how to encode this as a separate advisory/mandatory duty.
- [ ] **FAQ Q35 and log location:** Direction (iv) says 180-day logs shall be maintained within Indian jurisdiction, while FAQ Q35 says logs may be stored outside India if production to CERT-In is adhered to in reasonable time. Ask counsel whether the normalized action should be caveated or amended, given the FAQ says it does not replace or amend the Directions. FAQ Q36 adds: a service provider offering services to users in India must enable and maintain logs and financial-transaction records in Indian jurisdiction (verified in the stored FAQ text).
- [ ] **RBI six vs seven cyber Directions:** Sources disagree on whether there are six or seven entity-specific cyber instruments in the 31 Jul 2026 consolidation. Must resolve from RBI primary text.
- [x] **RBI NBFC Direction read and modelled:** all 47 stored pages were read. Six obligations from paragraphs 28, 121 and 141 are modelled with paragraph 3 chapter scope, paragraph 4(7)'s definition, and a 31 July 2026 validity start. Paragraphs 7-9 contain no Chapter III incident-reporting duty.
- [ ] **Does the HFC note also govern paragraph 28?** The note, "In respect of Housing Finance Companies, cyber incidents shall continue to be reported to NHB and not RBI" (page 44), sits under paragraph 141 in Chapter V. The model does not extend it to Chapter IV paragraph 28.
- [ ] **What NHB time limit and channel apply?** The HFC note names NHB but gives neither a duration nor a channel. The model conservatively inherits six hours from detection from paragraph 141 and marks confidence 0.5; confirm with RBI/NHB or counsel.
- [ ] **Can RBI “detection” be later than CERT-In “noticing”?** Paragraphs 28 and 141 use “detection”; CERT-In Direction (ii) uses “noticing ... or being brought to notice”. The engine keeps these anchors distinct, even when that produces different clocks.
- [ ] **Which directions were repealed?** Paragraph 155 (page 46) cites circular `DoS.CO.PPG.66/11.01.005/2026-27` dated 31 July 2026, but that circular is not in `data/raw`; no old-to-new mapping can be verified from the stored evidence.
- [ ] **Many RBI paragraphs remain unmodelled:** paragraphs 6, 28, 32, 59(4), 98, 121, 129 and 141 are now modelled. Other governance, controls, response, audit, continuity, outsourcing, repeal/savings, and remaining duties need separate labels-first modelling passes.
- [ ] **SEBI CSCRF:** Real PDF ingested as `sebi.cscrf.2024`, but no obligations are authored. Need to read the whole document before modelling effective date, entity-category thresholds, incident-reporting scope, Annexure-O details, and any Aug 2026 FSB FIRE alignment claim.
- [x] **DPDP Rule 7 obligations and pre-commencement simulation:** the three Rule 7 duties are modelled. A caller can explicitly simulate them before 13 May 2027; every simulated result is marked “not in force”, excluded from real applicability and regulators, and barred from cases and filing drafts.
- [ ] **DPDP Rule 1 commencement:** Gazette text needs whole-document modelling before `in_force_from` is filled. Review 5 records this structure from the Gazette: rules 1, 2 and 17 to 21 are in force on publication; rule 4 comes into force one year after publication; rules 3, 5 to 16, 22 and 23 come into force eighteen months after publication.
- [ ] **DPDP and SEBI `in_force_from`:** Left `null` in instrument records because this fix did not complete a whole-document commencement read. Do not fill from secondary summaries.
- [ ] **DPDP entity taxonomy provisional:** `data/entities/dpdp.json` remains useful scaffolding with descriptions/dates requiring primary-text review. RBI NBFC classes used by this build were revised from paragraph 3.
- [ ] **Current `evidence_required` values are builder-authored suggestions:** all 19 current values need to be removed, authored from exact source text, or reviewed by a compliance professional before being used as requirements. The UI labels them as suggested evidence in the meantime.
- [ ] **IRDAI guidelines:** Depth must be real or clearly labelled partial. Currently secondary-source only.

## Benchmark

- [ ] **Expert label validation:** 2-3 external compliance reviewers should validate benchmark labels (noted in brief section 11). This is a human task.
- [ ] **Hidden split design:** Need adversarial cases for ambiguous anchors, wrong entity class, repealed instruments, DPDP not-yet-in-force.

## Technical

- [ ] **CERT-In has no confirmed RSS/API:** Absence is hard to prove. Assume scraping with polite rate limits.
- [ ] **RBI RSS feed:** Verify `rbi.org.in/Scripts/rss.aspx` is real and useful.
- [ ] **SEBI RSS feed:** Verify `sebi.gov.in/rss.html` is real and useful.
- [ ] **Mandatory/advisory card chip:** Regulatory cards still show `Mandatory` from the current obligation set because obligations do not yet carry a mandatory/advisory field. Add a schema field before modelling advisory duties.

## Review 7 legal questions for counsel / next modelling round

- [ ] **SEBI glide path:** Does the page 9 "glide-path for adoption" make CSCRF duties binding only by 1 January 2025 for the six categories with an existing circular and by 1 April 2025 for other REs, or can duties bind from the 20 August 2024 issue date? The engine uses the earlier date conservatively.
- [x] **SEBI category scope:** closed 2026-10-04; see Build 10 below.
- [ ] **DPDP date arithmetic:** Rule 1(4), PDF page 24, says "eighteen months after the date of publication". Confirm whether publication on 13 November 2025 produces 13 May 2027 or, because of "after", 14 May 2027. The model uses 13 May conservatively.
- [x] **SEBI portal duty not yet modelled:** Page 123 says, "However, necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours." Page 200 likewise says "SEBI Incident Reporting Portal within 24 hours." Modelled in Build 10.
- [x] **SEBI stock-broker/depository-participant duty not yet modelled:** Page 123 says, "Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours" of the stated triggers; page 200 repeats the duty. Modelled in Build 10.
- [x] **SEBI other-incident duty not yet modelled:** Page 123 says, "All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours." Page 200 says "Any/ all other cybersecurity incident(s)" with the same recipients and period. Modelled in Build 10.

## Build 10 (SEBI remaining reporting duties), 2026-10-04

- [x] **SEBI category scope:** closed. Page 123 marks RS.CO.S1 to S3 "All REs (Mandatory)"; the earlier "tension" was a misreading of the extracted table text (see DECISIONS).
- [x] **SEBI portal, broker/DP and other-incident duties:** modelled in Build 10.
- [ ] **Annexure-O A.1 criteria (page 198):** does the six-hour duty apply only to Annexure I incidents that also meet one of the four criteria, with the rest on 24 hours? The tool keeps six hours for all of them.
- [ ] **Starting event for "within 24 hours" (page 123):** the "all other cybersecurity incident(s)" sentence names none. The tool uses noticing, detection or being brought to notice.
- [ ] **Table 36 "Days" (page 201):** from the timestamp (used) or from the calendar date?
- [ ] **Forensic audit report (page 203):** 75 days for High or Critical incidents. Needs the severity classification of Table 35. Not modelled.
- [ ] **Quarterly reports (page 124):** within 15 days of each quarter end. Not modelled.
- [ ] **"Cybersecurity incident" in the CSCRF:** the tool reuses one cyber-incident attestation for the RBI definition (paragraph 4(7)) and the SEBI term. Is one question enough for both regimes?
- [ ] **NCIIPC "as applicable" (page 123):** the 24-hour sentence lists NCIIPC as a recipient "as applicable"; the tool shows the separate NCIIPC duty only for protected systems.

## Sources awaiting a human download (2026-10-04)

- [ ] **IRDAI Information and Cyber Security Guidelines, 2023:** the regulator's robots.txt disallows all automated access. A person must download the PDF from https://irdai.gov.in/document-detail?documentId=3314780 and record `acquired_by` in the manifest. Not ingested; no IRDAI obligation exists.
- [ ] **RBI cybersecurity Directions for other entity types** (AIFIs, UCBs, Payments Banks found; Commercial Banks and Small Finance Banks not yet located): PDFs need a person to download them. Not ingested.
- [ ] **RBI list of repealed circulars and the old circular texts** (for the migrator): not located or ingested.
- [x] **RBI list of repealed circulars and the 2017 NBFC IT Direction:** ingested as HTML in Build 17 with raw-byte and extracted-content hashes.
- [ ] **2017 Annex I template:** the stored Direction page links to a separate PDF instead of embedding the template. The migrator can identify the Annex label but cannot quote or segment the template until that linked PDF is acquired and pinned.
- [ ] **Withdrawal circular display:** the stored withdrawn-list page contains row 47 for the 2017 Direction but does not display `RBI/DoS/2026-27/221`. The stored 2026 Direction paragraph 155 does state `DoS.CO.PPG.66/11.01.005/2026-27`; acquire the separate withdrawal circular if its first reference number is needed as primary evidence.

## Build 11 (RBI Directions for UCBs, AIFIs and Payments Banks), 2026-10-04

- [ ] **Payments Banks amended text:** the stored PDF is "Updated as on October 01, 2026". Did paragraphs 150 and 181 read the same from 31 July 2026? The version as issued is not in the dataset.
- [ ] **Bank Directions not ingested:** commercial banks, small finance banks, and any others (regional rural banks, local area banks). A generic `bank` is asked its kind and can only choose Payments Bank.
- [ ] **UCB level criteria (paragraph 4)** are not evaluated; the user states the level.
- [ ] **Unread paragraphs:** only the scoping, definition, reporting, CERT-In notification, VA/PT and repeal-opening paragraphs of these three Directions were read. The other control paragraphs are not modelled.
- [ ] **AIFI and HFC interplay:** NHB is itself an AIFI and receives HFC incident reports under the NBFC Direction's paragraph 141 note. No text ingested says how.
- [x] **Other RBI cybersecurity Directions (UCBs, AIFIs, Payments Banks):** ingested (human-acquired) and modelled in Build 11.

## Build 12 (IRDAI), 2026-10-04

- [x] **IRDAI Information and Cyber Security Guidelines, 2023:** ingested (human-acquired) and the incident-reporting duty modelled.
- [ ] **IRDAI source not independently verified:** nobody has compared the stored bytes with the regulator's copy. A person should re-download from https://irdai.gov.in/document-detail?documentId=3314780 and compare sha256 `2c8d2fda...618c98`.
- [ ] **IRDAI commencement:** does the duty bind from 24 April 2023 for every entity, or from the next financial year for those that had completed the FY 2022-23 audit?
- [ ] **IRDAI scope of "cyber incidents":** Annexure I types only, or any cyber incident?
- [ ] **IRDAI: what "a copy to IRDAI" requires** (channel, format) is not stated in Policy 2.10.
- [x] **IRDAI: other policies with stated hours (superseded by Build 13 below).** Notably third-party breach notice "within 4 hours from the time of breach discovery" (PDF page 283), lost-device reporting "within 4 hours" (pages 176 and 212), and the IT Rules 2021 section (pages 296 to 299) with 72-hour and 24-hour duties. None is modelled.
- [ ] **IRDAI covering circular not ingested:** it is a 2-page scan whose OCR text is unreliable ("24st Apr, 2023"). The reference number and date in the instrument record come from it.
- [ ] **Later IRDAI amendments or clarifications** to the 2023 guidelines, if any, are not in the dataset.

## Build 13 (IRDAI Part 2), 2026-10-05

- [x] **IRDAI time-bound duties in Policies 2.8, 2.19 and 2.24:** modelled with clocks that do not start from the incident.
- [ ] **IT Rules 2021 not ingested:** Policy 2.24 restates them. Are insurers and insurance intermediaries "intermediaries" under those Rules for these duties? The tool shows the duties to every IRDAI entity with that condition unevaluated.
- [ ] **IRDAI 2.24 item 8** (report cyber security incidents to CERT-In under the 2013 Rules, no time limit) is not modelled; it overlaps Policy 2.10.
- [ ] **IRDAI Policy 2.2 section 3.3** (lost device reported "immediately"; treated as an incident if reported after more than 4 hours or if the remote wipe fails) is not modelled.
- [ ] **A workflow for external clocks:** the tool lists these duties but offers no way to enter the date of an order or complaint and get a deadline.
- [ ] **IRDAI: about 20 policies remain unread** for duties without the word "hours" (audit cadence, VA/PT frequency, annual reviews).

## Builds 14 and 15, 2026-10-05

- [x] **SEBI forensic audit report and quarterly reports:** modelled in Build 15.
- [x] **A workflow for external clocks:** the case page and API accept the time an order or complaint was received.
- [ ] **SEBI severity:** the tool takes the RE's classification as given. Annexure-O A.4 says an incident that disrupts normal operations "must be classified as High or Critical"; the tool does not check a stated Low or Medium against that.
- [ ] **SEBI forensic report for Low or Medium incidents** (RCA inconclusive, or SEBI / HPSC-CS directs): not evaluated; stated in the not-applicable reason.
- [ ] **SEBI quarterly report date:** is "within 15 days from the quarter ended" the 15th of the next month, as modelled?
- [ ] **Workspace has no authentication.** Same-origin checking stops cross-site posts only.

## Migrator limits (Review 15)

- The named-recipient rule uses a fixed list of names taken from this one pair of instruments. Another pair needs its own list or a general method.
- The modal rule compares "may" and "shall" only. "Should" becoming "shall" is not reported as a change, and where it is the only difference the rule can misfire (clause 5.4).
- The gold mappings have seven known status errors (Amendment 1 in `docs/LABELS_MIGRATOR.md`) and have not been reviewed by a qualified person.
- Only one pair of instruments is mapped. The other 2026 RBI Directions have predecessors on the same repeal list that are not ingested.

## Build 18, 2026-10-06

- [x] **IRDAI duties with stated periods:** modelled (26 records after Review 16 found four the first search missed). The search is by wording, so others may remain.
- [ ] **IRDAI duties stated as "periodically" or "at regular intervals":** not modelled; no period in the text.
- [ ] **IRDAI financial year:** assumed 1 April to 31 March for the audit report and the FRB certificate; the guidelines do not define it.
- [ ] **IRDAI Foreign Reinsurance Branches** have no entity class; the Annexure VI duty is shown to every insurer with a prose condition.
- [ ] **Is the 2023 IT Governance Master Direction succeeded by the Payments Banks and AIFI Directions?** It is on the withdrawn list (row 16) and those Directions repeal "IT Governance as applicable"; that they are its successors for these entities is this project's reading.
- [ ] **The 2023 Master Direction also applied to commercial banks, small finance banks, NBFCs and credit information companies.** Those successor Directions are not all ingested.
- [ ] **UCB 2019 Annex I and the 2018 basic framework** are not mapped.
- [ ] **Webhook intake:** no rate limit; replay detection is by body hash only; no per-sender keys.
- [ ] **Signing:** no external timestamp (RFC 3161) and no key rotation.
- [x] **Signing the timeline head, SIEM input, tabletop generator:** built.
