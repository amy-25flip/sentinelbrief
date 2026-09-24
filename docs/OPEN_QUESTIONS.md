# Open Questions

Things needing a human or a primary-source check.

---

## Regulatory Sources

- [x] **CERT-In Directions PDF:** Read from the stored primary text in Review 2; the seven current obligation records are traceable to verbatim spans, subject to the open interpretation questions below.
- [x] **CERT-In MSME extension (27 Jun 2022):** Read from the primary PDF in Review 1. Effective 25 Sep 2022 for MSMEs, and for Direction (v)(a),(f). Ingested; only a pre-Sep-2022 caveat is modelled.
- [ ] **Does "MSME" apply to the target users (small NBFCs, co-op banks)?** Only matters for incidents before 25 Sep 2022. Low priority.
- [ ] **"Earliest of noticing / brought to notice":** conservative reading of Direction (ii); the text does not say "earlier". Ask a compliance professional whether CERT-In reads it that way in practice.
- [ ] **Independent label review:** all 17 benchmark labels (including the new expected.law_as_of) were written by AI agents against the primary text. An external compliance professional should review them before any accuracy figure is quoted.
- [ ] **Which CERT-In Annexure I terms count as unambiguous?** `data/reference/annexure_i.json` strong/weak terms were chosen conservatively; have a practitioner review them.
- [ ] **FAQ Q10 and non-Annexure incidents:** The FAQ says intermediaries should also report incident types not listed in the CERT-In Rules/Directions annexures considering nature, severity and impact. The current clock only models the explicit mandatory Direction (ii) Annexure I 6-hour obligation. Ask counsel whether and how to encode this as a separate advisory/mandatory duty.
- [ ] **FAQ Q35 and log location:** Direction (iv) says 180-day logs shall be maintained within Indian jurisdiction, while FAQ Q35 says logs may be stored outside India if production to CERT-In is adhered to in reasonable time. Ask counsel whether the normalized action should be caveated or amended, given the FAQ says it does not replace or amend the Directions. FAQ Q36 adds: a service provider offering services to users in India must enable and maintain logs and financial-transaction records in Indian jurisdiction (verified in the stored FAQ text).
- [ ] **RBI six vs seven cyber Directions:** Sources disagree on whether there are six or seven entity-specific cyber instruments in the 31 Jul 2026 consolidation. Must resolve from RBI primary text.
- [ ] **RBI NBFC Direction reference:** `RBI/DoS/2026-27/461` — unverified. Need to find and read the actual Direction.
- [ ] **SEBI CSCRF:** Need to verify entity categories, Annexure-O incident reporting specifics, and the Aug 2026 FSB FIRE alignment claim.
- [ ] **DPDP Rules numbering:** Verify Rule 7 content and numbering against the Gazette PDF.
- [ ] **IRDAI guidelines:** Depth must be real or clearly labelled partial. Currently secondary-source only.

## Benchmark

- [ ] **Expert label validation:** 2-3 external compliance reviewers should validate benchmark labels (noted in brief section 11). This is a human task.
- [ ] **Hidden split design:** Need adversarial cases for ambiguous anchors, wrong entity class, repealed instruments, DPDP not-yet-in-force.

## Technical

- [ ] **CERT-In has no confirmed RSS/API:** Absence is hard to prove. Assume scraping with polite rate limits.
- [ ] **RBI RSS feed:** Verify `rbi.org.in/Scripts/rss.aspx` is real and useful.
- [ ] **SEBI RSS feed:** Verify `sebi.gov.in/rss.html` is real and useful.
