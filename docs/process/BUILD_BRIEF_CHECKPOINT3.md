# SentinelBrief — Checkpoint 3: how Checkpoint 2B went, why, and what to build next

**Audience:** Antigravity ("Anti"). Read this fully first. Then read `docs/REVIEW_LOG.md` Reviews 7 and 8, and skim the diff of commit `831b353` (the fixer's repairs to your work), because it shows the patterns you are now expected to use.
**Reviewers:** the reviewer agent (review), Codex (fixes). They re-run your claims and read the real PDFs.
**State:** CERT-In (7 obligations), DPDP Rule 7 (3) and SEBI incident reporting (1) are modelled. The RBI NBFC Direction is in `data/raw` and not modelled. 37 dev scenarios pass, 190 tests.

---

## 1. What happened in Checkpoint 2B

### What you did well (keep doing exactly this)

1. **No fabricated sources.** You added no documents, and every source re-verifies against the regulator. This was the main thing asked of you and you did it.
2. **Labels before implementation.** Commit `4a376de` (labels) precedes `393e83d` (implementation) and you did not edit a label afterwards.
3. **DPDP was modelled correctly.** Verbatim spans on the right page, `immediate` for the "without delay" duties, the 72 hours anchored on `awareness` with the Board's extension kept, and an Unknown when the awareness time is missing.
4. **You used SEBI's five real categories** and kept `noticing`, `detection` and `brought_to_notice` as written.

### What went wrong (all in Review 7, J1 to J10)

| # | Defect | Effect |
|---|---|---|
| J1 | The SEBI 6-hour duty's condition ("falls under CERT-In Cybersecurity directions") was written as prose. The engine only recognised conditions by matching words such as "Annexure I". | A SEBI entity with a hardware failure got a firm 6-hour SEBI deadline, even after attesting the incident was not reportable. |
| J2 | You recorded `valid_from` 2025-01-01 for SEBI. That date is in paragraph 17.1, a compliance glide path for six categories; paragraph 17.2 gives 1 April 2025 for the others. You cited page 10; it is page 9. | A scenario asserted that SEBI reporting was not owed in October 2024. That tells a user they owe less, on a reading you did not justify. |
| J3 | Page 123 puts the clause under "MIIs and Qualified REs (Mandatory)"; Annexure-O (page 200) says "REs". You modelled all five categories and recorded neither the tension nor three other duties in the same paragraph. | A reader could not tell a choice had been made. |
| J4 | The implementation commit added no tests. The count stayed at 178. | Every new rule was covered only by scenarios you wrote yourself. |
| J5 | No scenario carried a clause quote, which rule 5 of the last brief required. | Labels could not be checked against the law. |
| J6 | A profile could hold one entity class. | An NBFC that is also a Data Fiduciary could not be evaluated. You worked within the limit and did not report it. |
| J7 | `docs/RBI_NBFC_PREPARATION.md` pre-decided a "base layer exemption", named "Cloudflare", and cited pages you had not checked. | The same guessing habit as before, in a planning document. |
| J10 | You wrote no handoff. | The reviewers had to reconstruct what you did from the diff. |

## 2. Why it happened

These are inferences from the evidence. I can see what you did, not what you were thinking.

**Cause 1: you stopped at the scenarios you had written.** All 16 of your scenarios used reportable incidents on in-scope entities. None asked "what should NOT trigger this duty?". The gates were green, so J1 was invisible to you. **Rule: for every obligation, write at least one scenario where it must not apply, and one where the engine must ask.** A rule tested only on cases where it fires is untested.

**Cause 2: a new condition was put where the engine could not read it.** The engine's condition handling was a short list of recognised phrases. Your condition used different words, so it was silently listed as "unevaluated" and the duty applied anyway. You did not check what the engine did with the sentence you wrote. **Rule: after adding any condition, run the engine on a case where the condition is false and look at the output.** The mechanism is now structured (section 3), so the silent path is gone, but the habit of checking the false case is what matters.

**Cause 3: you took the first date you found.** "by January 01, 2025" looked like an effective date, so it became one. You did not read 17.2, the sentence after it, or ask what kind of date it was. This is the same habit as the guessed URLs in Checkpoint 2, at a smaller scale. **Rule: a date goes into `validity` only with the sentence that says what the date does, quoted, and with the sentences before and after it read.** If the text does not say "comes into force", you have a compliance date, and the question is open.

**Cause 4: when the text was ambiguous you chose silently.** The SEBI scope choice was reasonable. Making it without a record was the defect. **Rule: every choice between two readings gets a DECISIONS entry with both quotes, both pages, the reading you rejected, and why your reading never tells a user they owe less.**

**Cause 5: the mechanical checks became the definition of done again.** Tests, quotes and the handoff were all in the brief. None is enforced by `scripts/check.py`, and all three were skipped. Labels-first is visible in the commit order, and you did that. **Rule: the brief is the definition of done. The gates are the minimum.** Quotes are now enforced mechanically. Tests and the handoff are checked by the reviewers on every checkpoint.

**Cause 6: you did not report a limit you hit.** The single entity class was a design gap in the repo, not your mistake. Not mentioning it was. **Rule: if the existing code cannot express something the law needs, stop and write it in the handoff under "what the code cannot express".** Finding such a gap counts in your favour.

## 3. What the repo now gives you (use these; do not rebuild them)

- **`applicability.requires`** on each obligation: an array of keys from a closed list (`cert_in_annexure_i`, `personal_data_involved`). The engine gates only on these. Prose in `conditions` is for humans and is never evaluated. **If a duty needs a condition that has no key, you add a key**: to the schema enum, the model, the engine, with a unit test for true, false and unknown, and a mutation test. Never gate on wording.
- **`IncidentProfile.entity_classes`** (a list). An entity can be a SEBI entity, a Data Fiduciary and an NBFC at once. Scenarios accept `entity_profile.entity_classes`.
- **`source_quotes`** on every scenario: `{document, page, quote}`. A test verifies each quote is on that PDF page of the stored text. A scenario without a quote fails the suite. Quote the clause the expected outcome turns on, not merely a clause from the same document (Review 8, K1).
- **`expected.time_critical`**: list the `immediate` duties a scenario expects.
- **Mutation tests** in `tests/test_benchmark.py`: each breaks one engine rule and asserts which named scenarios then fail. Copy that pattern.

## 4. Rules for this checkpoint (additions to the Checkpoint 2B rules, which all still apply)

1. **Negative cases are mandatory.** Per obligation: one scenario where it applies, one where it must not, one where the engine must ask.
2. **No date without its sentence.** See Cause 3.
3. **No silent choice.** See Cause 4.
4. **Tests ship in the same commit as the rule.** A rule without a unit test and a mutation test is not done.
5. **The handoff is part of the work.** No handoff means the checkpoint is not reviewed.
6. **Page numbers are computed, not remembered.** Take them from `page_offsets` in the `.meta.json`. The page printed on the document often differs from the PDF page.
7. **Stop after each work package pair** and hand off. Do not run ahead.

## 5. Work packages, in order

### WP-0 — The missing Checkpoint 2B handoff (do this first; one hour)

Write `HANDOFF_CHECKPOINT2B.md` using template v2 from the last brief, for the work in commits `4a376de` and `393e83d` as you actually did it. Fill section 4 ("what I read and did NOT read") with real page ranges for the DPDP Gazette and the SEBI circular. Under section 9, list what Review 7 found. Do not describe the fixer's work as yours. Leave the existing `HANDOFF.md` alone.

### WP-C — RBI NBFC Direction (`data/raw/RBI_NBFC_Cybersecurity_Directions_2026.pdf`, 47 pages; do not refetch)

Facts the reviewers have verified in the stored text, with PDF pages:
- Paragraph 2, page 3: "These Directions shall come into force with immediate effect."
- Paragraph 3, page 3: scoping by chapter. Chapter III for Base Layer NBFCs below Rs 500 crore and CICs; Chapter IV for Base Layer NBFCs at Rs 500 crore and above; Chapter V for Top, Upper and Middle Layer NBFCs excluding CICs. Read the exact words yourself and quote them.
- Paragraph 28, page 18: report cyber incidents on DAKSH "within six hours of detection".
- Paragraph 141, pages 43 to 44: report to RBI within six hours of detection on DAKSH, and "shall also pro-actively notify" CERT-In.

Not verified by anyone, and yours to establish from the text:
- Which chapter paragraph 28 sits in and which chapter paragraph 141 sits in, and therefore which NBFC classes each covers.
- Whether Base Layer NBFCs below Rs 500 crore and CICs (Chapter III) have an incident-reporting duty at all. Find the paragraph or record that there is none. Do not assume either way.
- Whether paragraph 28 also carries a CERT-In notification duty, as 141 does.
- What "immediate effect" means for the date: the Direction's date is 2026-07-31 in the instrument record. Confirm the date printed on the document.
- What the repeal chapter repeals, and whether anything is saved.

Tasks:
1. Read all 47 pages. Record page ranges read.
2. Correct `data/entities/rbi.json` from paragraph 3. The asset-size threshold splits Base Layer into two classes; model both, quoting the words.
3. Model: incident reporting to RBI per chapter (anchor `detection`, `PT6H`); the CERT-In notification as its own obligation where the text states it (the text gives it no time limit; do not invent one, and decide between `immediate` and `none` in DECISIONS with the quote); VAPT cadence per chapter; repeal.
4. Decide which `requires` key, if any, the RBI duty needs. "Cyber incidents" in this Direction is not the CERT-In Annexure I list. Find the Direction's own definition, quote it, and if it needs a new key, add one properly (section 3).
5. Scenarios, labels first, at least 10: each NBFC class against the reporting duty (apply, not apply, per the text); detection time unknown (must ask); an NBFC that is also a Data Fiduciary with personal data, after 13 May 2027 (three regimes at once, three anchors); an NBFC where noticing and detection differ, so CERT-In and RBI deadlines differ; incident before 2026-07-31; a bank (not an NBFC) that must not get the RBI NBFC duty; a non-incident that must not trigger it.
6. Unit and mutation tests for every rule.

### WP-F — The three SEBI duties that are real and unmodelled (page 123 and Annexure-O page 200)

The same paragraph you already modelled also says:
1. "necessary details of the incidents shall be reported on SEBI Incident Reporting Portal within 24 hours."
2. "Stock Brokers/ Depository Participants shall also report the incidents to Stock Exchanges/ Depositories along with SEBI and CERT-In within 6 hours of noticing/ detecting such incidents or being brought to notice about such incidents."
3. "All other cybersecurity incident(s) shall be reported to SEBI, CERT-In and NCIIPC (as applicable) within 24 hours."

Points to resolve from the text, not from assumption:
- Sentences 1 and 3 say "within 24 hours" without naming the starting event. Read the surrounding text and Annexure-O for one. If the text gives none, that is a DECISIONS entry with the conservative reading (the same anchors as the 6-hour duty) and an OPEN_QUESTIONS item.
- Stock broker and depository participant are roles, not size categories. They are not in `data/entities/sebi.json`. Add them as classes an entity holds in addition to its category (this is what `entity_classes` is for), quoting where the circular defines them.
- Sentence 3 covers incidents that are not under the CERT-In directions. That is the complement of `cert_in_annexure_i`, and when the Annexure I question is unresolved the engine must ask, not pick one. "NCIIPC (as applicable)" is a condition you cannot evaluate; keep it as an Unknown.
- Scenarios, labels first, at least 8, with negative and ask cases. Unit and mutation tests.

### WP-D and WP-E (unchanged from the Checkpoint 2B brief)

WP-D: move the invented `evidence_required` entries to `suggested_evidence` or cite them. WP-E: the adversarial pass, now including RBI and the new SEBI duties, and the attempt to defeat the provenance controls.

**Order:** WP-0, then WP-C, hand off. Then WP-F and WP-D, hand off. Then WP-E, hand off.

## 6. Handoff template v3

Template v2, plus:

```
## 11. For each new obligation: the scenario where it applies | where it must not | where the engine asks
## 12. Every date I put in validity: date | the sentence that says what it does | page
## 13. Every choice between two readings: DECISIONS entry title | reading rejected
## 14. What the existing code could not express
## 15. Tests added: count before, count after, and the mutation each new rule is caught by
```

## 7. Five more questions before you write "done"

1. For each new duty, did I run a case where it must not apply and look at the output?
2. Is any legal condition expressed only in prose?
3. For each date, did I read the sentence before and after it?
4. Did the test count go up, and can I name the bug each new test catches?
5. Is there a choice I made between two readings that appears nowhere in DECISIONS?

"Not sure" is an acceptable answer in the handoff. A missing handoff is not.
