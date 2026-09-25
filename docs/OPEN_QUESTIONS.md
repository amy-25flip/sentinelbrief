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
- [ ] **RBI NBFC Direction BLOCKED:** Official page believed to be `https://www.rbi.org.in/Scripts/BS_ViewMasDirections.aspx?id=13592`; PDF believed to be `https://rbidocs.rbi.org.in/rdocs/notification/PDFs/461MD9FAF2CD7550844EE9A70C884DBE4A8A6.PDF`. Automated GET returned a CAPTCHA page. A human must download the official document and place it in `data/raw` with an `acquired_by` note. TrackRBI or other mirrors may only help locate the official document, never serve as source text.
- [ ] **SEBI CSCRF:** Real PDF ingested as `sebi.cscrf.2024`, but no obligations are authored. Need to read the whole document before modelling effective date, entity-category thresholds, incident-reporting scope, Annexure-O details, and any Aug 2026 FSB FIRE alignment claim.
- [ ] **DPDP Rules:** Real Gazette PDF ingested as `meity.dpdp-rules.2025`, but no obligations are authored. Review 4 notes real Rule 7 includes affected Data Principal intimation without delay, Board intimation without delay, and a detailed Board update within seventy-two hours of awareness or a longer period allowed by the Board. Need full primary-text modelling before any clock/scenario is added.
- [ ] **DPDP Rule 1 commencement:** Gazette text needs whole-document modelling before `in_force_from` is filled. Review 5 records this structure from the Gazette: rules 1, 2 and 17 to 21 are in force on publication; rule 4 comes into force one year after publication; rules 3, 5 to 16, 22 and 23 come into force eighteen months after publication.
- [ ] **DPDP and SEBI `in_force_from`:** Left `null` in instrument records because this fix did not complete a whole-document commencement read. Do not fill from secondary summaries.
- [ ] **RBI and DPDP entity taxonomy provisional:** `data/entities/rbi.json` and `data/entities/dpdp.json` contain useful scaffolding but include dates/descriptions not re-verified in this fix. Confirm or revise from primary text before using them for legal outcomes.
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
