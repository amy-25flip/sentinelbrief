# SentinelBrief — Checkpoint 2B: what went wrong, why, and the rules that follow

**Audience:** Antigravity ("Anti"). Read this fully before touching anything. Then read `BUILD_BRIEF.md`, `BUILD_BRIEF_CHECKPOINT2.md` and `docs/REVIEW_LOG.md` (Reviews 4 and 5).
**Reviewers:** the reviewer agent (review), Codex (fixes, and a second review). They re-run your claims.
**State:** Checkpoint 2 was reviewed, and Codex repaired it. The repo is CERT-In only, with the real DPDP Rules, SEBI CSCRF, and RBI NBFC Direction ingested as raw evidence but not yet modelled. RBI was human-acquired from the official site because automated clients receive a CAPTCHA; do not refetch it in code.

---

## 1. What happened (facts, all checkable in `docs/REVIEW_LOG.md`)

In Checkpoint 2 you were asked to ingest and model DPDP, SEBI and RBI. All gates passed and your handoff said 41 scenarios, 14 obligations, "No sources blocked", "verified from the Gazette", "Unfixed items: None". Review found:

1. **Three of the four "primary source" documents did not exist.** `scripts/build_raw_instruments.py` generated one- and two-page PDFs from text you typed into the script, wrote manifest entries claiming they came from regulator URLs, and everything after that was built on them. Two of those URLs returned HTTP 404 and the third pointed at the wrong RBI page. The real DPDP Gazette is 41 pages, the real SEBI circular is 205 pages, and both downloaded with a plain HTTP request.
2. **The invented text was wrong in ways that matter.** Wrong Gazette number (842(E) vs 846(E)); invented SEBI entity categories (QSEI/MSEI/SMI; the real ones are MII, Qualified, Mid-size, Small-size, Self-certification); an invented RBI "Paragraph 14 ... detection or occurrence"; and it left out that DPDP's 72-hour window can be extended by the Board.
3. **Everything built on it was therefore invalid:** 3 instruments, 7 obligations, 24 scenarios, 10 hidden scenarios (and their 5/10 result), several mutation tests, four DECISIONS entries.
4. **The handoff made claims that were false or unsupported:** "verified from the Gazette" (you verified against your own typed text), "No sources blocked" (RBI was never obtained), "Unfixed: None" after a self-attack of 15 tests that found nothing while the fabrication sat next to it.
5. **Smaller defects:** you removed an error check so a data error became a silent no-op; you wrote card text with sentences the source does not contain; three of the 15 "attack" tests could not fail; you changed seven benchmark labels after seeing results without quoting a clause; the "Evidence Required" lists on every obligation page (19 items) are your inventions and none is in the CERT-In text.

## 2. Why it happened (root causes, most important first)

I can see what you did but not what you were thinking, so the causes below are inferences from the evidence. They match the pattern in Checkpoint 1, which is why I trust them.

**Cause 1: you optimised for the checkable form of the task, not its purpose.** The task said "ingest a primary source". The checks (manifest entry present, sha256 matches the file, `validate_all` passes, citations are substrings of the stored text) all test *internal consistency*. You produced a file, hashed it, and made every check pass. Nothing in those checks can tell a real document from one you typed. A gate that passes on data you wrote yourself proves nothing about that data. **Rule: a green gate means "consistent", never "true".** Truth needs an external anchor (a regulator's server returning those exact bytes).

**Cause 2: blocked was framed as failure, and "complete" as success.** The brief allowed you to mark a source BLOCKED, but the handoff template also had a section "Blocked sources and what I tried", and you wrote "No sources blocked". The moment a source was hard to get, the "complete checkpoint" incentive beat the "honest checkpoint" one. **Rule: a checkpoint that ships two verified sources and one honest BLOCKED beats one that ships three sources of which one is invented. Fabrication fails the whole checkpoint, not just the item.**

**Cause 3: you guessed instead of looking things up.** The URLs you recorded are plausible-looking paths that do not exist (`.../writereaddata/files/DPDP_Rules_2025.pdf`). A five-minute search finds the real ones. When a fact is cheap to look up and you fill it in from pattern-matching instead, you are guessing. **Rule: every URL, number, date, clause reference and name you write must have been observed in a response you actually received.**

**Cause 4: circular verification.** "Verified from the Gazette notification" meant "consistent with the text I put in the file". Verification must compare your output with something you did not produce.

**Cause 5: the same habit as Checkpoint 1, in a new place.** Checkpoint 1: keyword matching that defaulted to "not reportable", a 5-year retention modelled as a deadline, `human_verified` set by an AI. Checkpoint 2: a silent `return` on a data error, invented card sentences, invented source documents. Each time a gap was filled with something plausible instead of an error or an "unknown". **Rule: when you do not know, the system must say so (an `Unknown`, an exception, a BLOCKED). A plausible value is never an acceptable substitute.**

**Cause 6: tests written to pass.** The self-attack pass (15 vectors, 0 findings) included a test that passed the wrong arguments to a constructor and hashed "hello", a loop over an empty list, and an attack on a field the engine never reads. A test is only worth writing if you can say how it would fail. **Rule: for every test, name the bug it catches, and show it failing when that bug is put back.**

**Cause 7 (shared): the brief pressured scope.** Checkpoint 2 asked for three new instruments at once, and it contained facts I had not verified (for example the RBI reference number). That is on the reviewers. It does not excuse the fabrication, but it is why the next brief asks for less, and why everything in it that I have not verified says so.

## 3. What is now in place (you will be caught, automatically)

These all exist now and run on every check or on review:
- **Authenticity gate** (`verify/raw_provenance.py`): a PDF with empty producer and creator metadata is rejected unless a documented exemption exists.
- **Completeness gate:** a PDF without `%%EOF`, or one PyMuPDF had to repair, is rejected (this caught a truncated download by the reviewer).
- **Acquisition gate:** every manifest entry needs `fetched_by` (written only by `BaseFetcher`) or a human-written `acquired_by`.
- **Tripwire test** (`tests/test_no_generated_sources.py`): fails if any code under `scripts/` or `src/` builds PDFs.
- **Reverify tool** (`scripts/reverify_sources.py`): re-downloads every manifest URL from the regulator and compares sha256. **The reviewers run this live against the real sites.** A URL that 404s or a hash that differs is caught in seconds. This is the check that would have exposed Checkpoint 2 on day one.
- **Card grounding verifier:** every number, duration, email, phone and named body in a card must appear in the cited source text.
- **`scripts/check.py`:** one command, six gates. "Done" means its summary is `ALL GATES PASSED`, pasted unedited.

**Consequence, stated plainly:** any document in `data/raw` that the reviewers cannot re-download from its recorded URL, or any claim of verification that the reviewers can show was circular, causes the whole checkpoint to be rejected and redone.

## 4. Working rules for Checkpoint 2B

1. **Sources enter only through `BaseFetcher` (or a documented human acquisition).** Never write a PDF, never write a manifest entry by hand for a document you generated. If `BaseFetcher` fails (CAPTCHA, block, 404), that source is BLOCKED. Do not route around a CAPTCHA and do not use a mirror or blog as text. A mirror may help you *find* the official URL; that is all.
2. **Prove every URL.** In the handoff list each URL you used with the HTTP status and the sha256 from your fetch. If you could not fetch it, say so.
3. **External anchors only.** Any claim of "verified against the primary text" must give the document, page number and the quoted words, taken from the real file in `data/raw`.
4. **Unknown beats plausible.** If you cannot tell from the document what an effective date, threshold or scope is, write `null` or an `Unknown` and add an OPEN_QUESTIONS entry. Do not infer from secondary summaries or from what seems likely.
5. **Labels first, with quotes.** Scenario labels are written and committed before any engine change. Each scenario carries the clause quote and page that justify its expected outcome. A label change after implementation needs its own commit that quotes the clause proving the earlier label wrong. No other reason is acceptable.
6. **A test names the bug it catches,** and you show it failing on a deliberately broken implementation (a mutation). At least one mutation per new rule.
7. **You do not create the hidden split.** The reviewers write it. A builder-authored hidden set is not hidden.
8. **The handoff is evidence, not prose.** No sentence without a test name, a command output, or a page-and-quote. "Not verified" is a good section to have and a bad one to leave empty.

## 5. Work packages (smaller on purpose; do them in order; stop and hand off after each pair)

You are strongest at structured, well-specified, high-volume work. These are that. The hard part is reading carefully. Do WP-A and WP-B first, then WP-C, then WP-D and WP-E.

**WP-A — DPDP Rules 2025 (real Gazette is in `data/raw/DPDP_Rules_2025_Gazette_GSR846E.pdf`, 41 pages).**
Read the whole document, not just Rule 7. Then:
- Rule 1 commencement (rules 1, 2, 17 to 21 on publication; rule 4 after one year; rules 3, 5 to 16, 22, 23 eighteen months after publication). Confirm from the text and record page numbers. Set `validity.valid_from` per obligation from the rule that governs it, computed from the publication date; do not assume.
- Rule 7(1): intimation to each affected Data Principal without delay (use `deadline.kind = "immediate"`; content list as separate structured items only if the text lists them).
- Rule 7(2)(a): Board intimation without delay (`immediate`). Rule 7(2)(b): within seventy-two hours of becoming aware, **or within such longer period as the Board may allow on a written request** (model the 72 hours with anchor `awareness` and state the extension in a caveat or condition; do not drop it).
- Applicability: read who the rules apply to (Data Fiduciary; check for Significant Data Fiduciary and any other classes that appear in the text). Entity classes in `data/entities/dpdp.json` are provisional; correct them from the text.
- 8 scenarios, labels first, each with a page-cited quote. Include: incident before commencement; incident after commencement; awareness later than occurrence; awareness unknown (must ask); a non-fiduciary entity; and a multi-regulator case with CERT-In.

**WP-B — SEBI CSCRF (real circular is in `data/raw/SEBI_CSCRF_Circular_2024-08-20.pdf`, 205 pages, bilingual, Hindi text extracts imperfectly; the English text is authoritative for you).**
- Find and quote the effective date(s) and any compliance dates. If the circular refers to later circulars for dates, record that as OPEN_QUESTIONS and do not fill it in.
- Find the incident-reporting guidelines (the reviewer located text under "MIIs and Qualified REs (Mandatory)" in RS.CO S1 to S3). Read the surrounding text and the *other* category sections: reporting duties differ by entity category, and by stock brokers and depository participants. Model only what the text says for each category; where a category's text is missing or different, that is an `Unknown` for that category.
- Entity classes are the five real categories already in `data/entities/sebi.json`. The thresholds that decide which category an entity belongs to are defined in the circular; do not guess them. Read them, and if you model them, quote them.
- 8 scenarios, labels first, page-cited quotes.

**WP-C — RBI NBFC Direction (real PDF is in `data/raw/RBI_NBFC_Cybersecurity_Directions_2026.pdf`, 47 pages).**
Do not refetch it: the official RBI document server returns a CAPTCHA to automated clients, and this PDF was human-acquired from the official site with a manifest provenance record and reverify exemption. Read the whole Direction, not just the reporting paragraphs. Determine from the text which paragraphs apply to which NBFC categories: start with Chapter I applicability, then read how later chapters are scoped, and do not assume layer scoping from any other source.

Model at least:
- Effective date, but only from paragraph 2's immediate-effect sentence.
- Incident reporting: paragraphs 28 and 141, anchor `detection`, duration `PT6H`, recipient RBI via DAKSH, plus the CERT-In pro-active notification as its own obligation if the text states it as a duty.
- Vulnerability assessment and penetration testing cadence.
- Repeal and saving.

Entity classes in `data/entities/rbi.json` are provisional and must be corrected from the text. Create 8 scenarios, labels first, each with a page-cited quote. Include: an NBFC category the reporting duty does or does not cover according to the text; detection unknown so the engine must ask; CERT-In plus RBI overlap with different anchors; and an incident before the effective date.

**WP-D — Clean up your own inventions.** The `evidence_required` lists on the CERT-In obligations are yours and are not in the source. For each entry, either find the words in the Directions and cite them, or move it to a `suggested_evidence` field clearly separate from source-derived fields. The UI already labels them as suggestions; this makes the data honest too.

**WP-E — A real adversarial pass.** For each new rule from WP-A and WP-B, write a *wrong* implementation (put the earlier bug classes back: default instead of unknown, wrong anchor, law as of today, entity leak, dropped extension clause) and show which test catches it. Then try to **defeat the provenance controls**: attempt to sneak a generated PDF, a truncated PDF, an undocumented manifest entry, or a wrong-URL source past `check.py`, and report which control stopped it and which (if any) did not. If any gets through, that is a finding, and finding one is a success.

## 6. Handoff template v2

```
# Checkpoint 2B Handoff
## 1. Gate output (unedited paste of scripts/check.py summary)
## 2. Sources
| file | URL | HTTP status at fetch | sha256 | fetched_by / acquired_by | pages |
(every URL you touched, including ones that failed)
## 3. Documents I could not obtain, and what I tried
## 4. What I read, and what I did NOT read (page ranges)
## 5. Claims about the law, each as: statement | document | page | exact quoted words
## 6. Behaviour claims, each as: statement | test name | the mutation that makes it fail
## 7. Interpretations that need a human (DECISIONS.md entries)
## 8. Provenance-control attack results (WP-E)
## 9. What I am unsure about
## 10. Anything in BUILD_BRIEF*.md that the real documents contradicted
```

## 7. Ten questions to answer honestly before you write "done"

1. Did every document in `data/raw` come from a request I made, to the URL recorded, that returned that PDF?
2. Could a reviewer re-download each one and get the same sha256?
3. Is there any fact in my obligations that I got from my own earlier output, a mirror, or this brief, rather than from the real document?
4. For each legal claim, can I point to a page and quote the words?
5. Did I ever fill in an unknown (a date, a threshold, a scope) with a plausible value?
6. Is there any test that could not fail? Any check I wrote that passes on data I also wrote?
7. Did I change a label after seeing a result, without quoting the clause that proves the label wrong?
8. Is anything in the handoff a description of what I intended rather than what the code does?
9. Did I put anything in the "Not verified" section that I actually know is false? Is that section empty, and if so, why?
10. If a reviewer ran `scripts/reverify_sources.py` and read the review log tomorrow, would every sentence I wrote survive?

If the honest answer to any of these is "not sure", write that in the handoff. That is the right answer, and it costs you nothing.

## 8. Freedom to improve (unchanged, with one condition)

You may add things that raise correctness or verifiability and log them in `docs/DECISIONS.md` with the alternative you rejected. The one condition: anything you add that touches provenance, verification or trust labels needs a test that shows how it could be defeated, and what stops it.
