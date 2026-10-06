# Circular migrator: specification and gold mappings, written before implementation

Author: the label author. Written from a full read of both texts, before any migrator code exists.

## What it is for

On 31 July 2026 RBI repealed 628 circulars and issued 64 consolidated Directions. RBI published the list of repealed circulars but no clause-level concordance. An NBFC whose internal policy cites "paragraph 3.9 of the 2017 IT Framework Master Direction" needs to know which paragraph of the 2026 Direction now carries that requirement.

The migrator proposes that mapping. **It is inference, not an RBI concordance, and every output says so.**

## Sources (both public RBI pages; neither is ingested yet)

| | Old | New |
|---|---|---|
| Instrument | Master Direction - Information Technology Framework for the NBFC Sector | RBI (NBFCs - Cybersecurity, Technology: Risk, Resilience and Assurance Framework) Directions, 2026 |
| Reference | RBI/DNBS/2016-17/53, DNBS.PPD.No.04/66.15.001/2016-17, 8 June 2017 | RBI/DoS/2026-27/461, 31 July 2026 |
| Where | `https://www.rbi.org.in/Scripts/NotificationUser.aspx?Id=10999&Mode=0` (HTML) | already in `data/raw` (PDF) |
| Repeal | Listed as item 47 under "Circulars Withdrawn by the Department of Supervision" at `https://www.rbi.org.in/Scripts/NotificationUserWithdrawnCircular.aspx`, repealed by circular RBI/DoS/2026-27/221 (DoS.CO.PPG.66/11.01.005/2026-27, 31 July 2026) | Paragraph 155 of the new Direction |

The old text is an HTML page. Its raw bytes differ between two fetches seconds apart (a trailing dynamic block), so the raw sha256 cannot be re-verified. Provenance rule for HTML sources: store the raw bytes as fetched with their sha256 (evidence of what was received), extract the instrument text deterministically, and record `content_sha256` of the extracted text; re-verification compares `content_sha256`. The extracted text starts at the reference line "RBI/DNBS/2016-17/53" and ends before the site's archive navigation ("2026 / All Months / January ...").

## Structure the texts give

The old direction has Section A (NBFCs with asset size above Rs 500 crore) with clauses 1 to 7.3, and Section B (below Rs 500 crore) with clauses 8 and 8.1. The new Direction's Chapter IV (Base Layer, Rs 500 crore and above) is paragraphs 10 to 64 and Chapter III (Base Layer below Rs 500 crore, and CICs) is paragraphs 7 to 9. Chapter V (Middle Layer and above, paragraphs 65 to 154) has no counterpart in the 2017 direction.

## Output, per old clause

`status` is one of:

- `matched`: one or more new paragraphs carry the same requirement in substantially the same words.
- `changed`: a successor exists but the requirement differs in substance (a new time limit, "may" became "shall", a different recipient). The difference is described from the two texts.
- `obsolete_no_successor`: nothing in the new Direction carries it (transition dates, the old reporting template).
- `needs_human`: the method cannot choose between candidates.

Each entry carries the old excerpt, the candidate new paragraphs with a similarity score and excerpt, the method and its version, and `reviewer: null` until a named person confirms or corrects it. A confirmed entry records the person and date and is never overwritten by a re-run.

The method must be deterministic and must not use an LLM: paragraph segmentation of both texts, lexical similarity (for example TF-IDF cosine over word n-grams) for candidates, and explicit rules for `changed` (modal verbs may/should/shall, numbers and durations, named recipients present on one side only).

## Gold mappings (old clause to new paragraph numbers)

The measure is: for each old clause, is the method's top candidate one of the gold paragraphs (hit@1), and is the status right.

| Old clause | Subject | New paragraph(s) | Gold status |
|---|---|---|---|
| Introduction 2, 4, 5 | gap analysis, Board placement by 30 Sep 2017, compliance by 30 Jun and 30 Sep 2018 | none | obsolete_no_successor |
| 1 | IT Governance principles and stakeholders | 10, 11, 12, 13, 14 | matched |
| 1.1 | IT Strategy Committee | 15 | matched |
| 1.2 | ITSC roles and responsibilities | 16 | matched |
| 2 | IT Policy | 18 | changed (IPv6: "should migrate ... as per National Telecom Policy" became "shall enable its public facing IT infrastructure to handle IPv6 traffic"; "may formulate" became "shall formulate") |
| 3 | Information Security tenets | 19, 20 | matched |
| 3.1 | IS Policy framework (nine items) | 21 | matched |
| 3.2 | Cyber security policy | 22 | matched |
| 3.3 | Vulnerability management | 23 | changed ("may devise a strategy" became "shall establish a vulnerability management process") |
| 3.4 | Preparedness indicators | 24 | matched |
| 3.5 | Cyber Crisis Management Plan | 25, 26, 27 | matched |
| 3.6 | Reporting incidents to RBI | 28 | changed (old: report "all types of unusual security incidents ... to the DNBS Central Office, Mumbai" in the Annex I template, no time limit; new: "on DAKSH platform ... within six hours of detection") |
| 3.7 | Awareness of Board and stakeholders | 29, 30 | matched |
| 3.8 | Digital signatures | 31 | changed ("may consider use" became "shall use") |
| 3.9 | IT risk assessment | 32 | matched |
| 3.10 | Mobile financial services | 33 | matched |
| 3.11 | Social media risks | 34 | matched |
| 3.12 | Training | 35, 36 | matched |
| 4 | IT Operations | 37, 38 | matched |
| 4.1 | Acquisition and development | 39, 40 | matched |
| 4.2 | Change management | 41, 42 | matched |
| 4.3 | IT-enabled MIS | 43 | matched |
| 4.4 | MIS contents | 44 | matched |
| 4.5 | MIS for supervisory requirements | 45, 46 | changed (old names "reporting under COSMOS"; new does not) |
| 5 | IS Audit objective | 47 | matched |
| 5.1 | IS Audit framework | 48, 49, 50 | matched |
| 5.2 | Coverage | 52, 53, 54 | matched |
| 5.3 | Personnel | 55 | matched |
| 5.4 | Periodicity | 56 | matched |
| 5.5 | Reporting | 51 | matched |
| 5.6 | Compliance | 57 | matched |
| 5.7 | CAATs | 58 | matched |
| 6, 6.1, 6.2, 6.3, 6.4 | BCP and its four features | 59 | matched (59(5), on vendors' cyber resilience testing, is new and has no old clause) |
| 7 | Outsourcing policy | 60, 61 | matched |
| 7.1 | Contract provisions | 62 | matched |
| 7.2 | Board responsibility | 63 | matched |
| 7.3 | ITSC role in outsourcing | 17 | matched (moved from the outsourcing section to IT Governance) |
| 7, closing paragraph | Business continuity not compromised by outsourcing | 64 | matched |
| 8 | Section B: basic standards for smaller NBFCs | 7, 8 | changed (compliance date 30 Sep 2018 dropped; "COSMOS Returns" dropped; CICs added to scope by paragraph 3(2)) |
| 8.1 | Scale up IT systems | 9 | matched |
| Annex I | Template for reporting cyber incidents | none | obsolete_no_successor (reporting is on DAKSH) |

That is 47 old units (counting 6 to 6.4 as five and the three introduction paragraphs as three).

## What will be reported

Hit@1 and status accuracy on these 47, as counts with a Wilson interval, plus the list of misses. The gold mappings are AI-authored from the two texts and not reviewed by a qualified person; aligning near-identical wording is a much smaller judgement than reading a legal duty, but the caveat stands.

## Reviewer workflow

A page listing every proposed mapping with both excerpts side by side, filterable by status; a named person can confirm or correct each one; confirmed mappings are stored with reviewer and date, shown as "confirmed by <name>", and survive re-runs. Unconfirmed mappings are always labelled "proposed, not confirmed".

## New facts about the law found while reading (to record in DECISIONS)

- The six-hour DAKSH reporting duty in paragraph 28 has no time limit in its 2017 predecessor (clause 3.6). The consolidation is not "as is" on this point.
- Digital signatures and vulnerability management moved from "may" to "shall".
- The old direction applied Section A to NBFCs "with asset size above Rs 500 crore"; the new Chapter IV applies to Base Layer NBFCs "with asset size Rs 500 crore and above", and Middle Layer and above now have a separate, longer Chapter V.

## Amendment 1 (after implementation; the table above is unchanged)

Written by the label author after Review 15. The method disagreed with the gold status on nine clauses. On re-reading both texts, seven of those are errors in the table above: clauses 3.4, 3.12, 4.4, 5.3, 5.6, 6.4 and 7.1 each have a "may" in 2017 that is "shall" in the successor paragraph, which this document's own definition calls `changed`. The quotes are in `docs/REVIEW_LOG.md`, Review 15, R15-4.

The table and `benchmark/migrator_gold.json` are left as committed, because they were written before the code and a gold set corrected after seeing the system's output is no longer independent of it. Results are reported against the gold as committed (status 38/47), with the corrected count (45/47) stated separately and marked as post hoc.
