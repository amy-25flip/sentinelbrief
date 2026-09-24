# Open Questions

Things needing a human or a primary-source check.

---

## Regulatory Sources

- [ ] **CERT-In Directions PDF:** Need to read the full text at `cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf` and author obligations from verbatim text. The brief's summary is secondary/unconfirmed.
- [x] **CERT-In MSME extension (27 Jun 2022):** Read from the primary PDF in Review 1. Effective 25 Sep 2022 for MSMEs, and for Direction (v)(a),(f). Ingested; only a pre-Sep-2022 caveat is modelled.
- [ ] **Does "MSME" apply to the target users (small NBFCs, co-op banks)?** Only matters for incidents before 25 Sep 2022. Low priority.
- [ ] **"Earliest of noticing / brought to notice":** conservative reading of Direction (ii); the text does not say "earlier". Ask a compliance professional whether CERT-In reads it that way in practice.
- [ ] **Independent label review:** all 17 benchmark labels were written by AI agents against the primary text. An external compliance professional should review them before any accuracy figure is quoted.
- [ ] **Which CERT-In Annexure I terms count as unambiguous?** `data/reference/annexure_i.json` strong/weak terms were chosen conservatively; have a practitioner review them.
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
