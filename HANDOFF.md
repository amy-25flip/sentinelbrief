# SentinelBrief handoff (2026-10-06)

Written by the reviewer agent. Antigravity is no longer on the project; from Build 9 on, the reviewer agent writes the labels and reviews, and Codex builds. Earlier history is in `docs/REVIEW_LOG.md`.

## 1. Gate output (`python scripts/check.py`, run by the reviewer agent on 2026-10-06)

```
PASS  pytest             442 passed, 1 deselected, 1 warning
PASS  ruff check         All checks passed!
PASS  ruff format        81 files already formatted
PASS  mypy (strict)      Success: no issues found in 42 source files
PASS  validate_all       All obligations and citations passed validation successfully!
PASS  benchmark dev      Scenarios passed:   107/107  Wilson 95% CI [96.5%, 100.0%]
ALL GATES PASSED
```

Hidden split (git-ignored, 30 scenarios): 29/30. Set A (14, written by the reviewer agent for Codex-built regimes) 14/14; set B (16, written by Codex for the reviewer agent-built work) 15/16. The one failure is the contested SEBI start date (Review 12, Q5).

Live source re-verification, 2026-10-06: 9 passed, 0 failed, 5 skipped (RBI's document server and IRDAI refuse automated clients; those PDFs are pinned by sha256). The four RBI HTML pages are compared by the hash of their extracted text, because the raw page bytes differ between fetches.

Migrator (`python -m sentinelbrief.migrator score`): hit@1 46/47, status 38/47 against the gold as committed. Seven of the nine status disagreements are errors in the gold (Review 15, R15-4). Three further pairs, hit@1 only: UCB 59/61, Payments Banks 27/27, AIFI 27/27 (Build 18).

## 2. What exists

| Area | Built by | Reviewed by |
|---|---|---|
| CERT-In (7), DPDP Rule 7 (3), SEBI six-hour duty | Antigravity, repaired by Codex | The reviewer agent (Reviews 1 to 8) |
| RBI NBFC Direction (6) | Codex, against the reviewer agent's labels | The reviewer agent (Review 9) |
| SEBI remaining duties, forensic and quarterly (10 more) | Codex and the reviewer agent | Codex (Review 12), fixes checked by the reviewer agent (Review 13) |
| RBI UCB, AIFI, Payments Banks Directions (12) | The reviewer agent | Codex (Review 12: found sound) |
| IRDAI guidelines (8; partial) | The reviewer agent | Codex (Review 12), fixes checked by the reviewer agent |
| Incident workspace, external clocks, evidence fields, cards | The reviewer agent | The reviewer agent self-review (Review 11), then Codex (Review 12) |
| Recurring RBI NBFC duties, DPDP simulation, RSS feed | Codex | The reviewer agent (Review 14) |
| HTML evidence path, 2017 NBFC IT Framework, circular migrator and its reviewer pages | Codex, against the reviewer agent's gold mappings | The reviewer agent (Review 15) |
| IRDAI periodic duties (22), migrator on three more pairs, signed evidence head, webhook alert intake, tabletop generator, screenshots | The reviewer agent | Codex (Review 16) |
| Provenance attack tests and source pinning | The reviewer agent | Codex (Review 12: found sound) |

## 3. Claims about the law

Every obligation's `text_verbatim` and citation page is machine-checked against the stored text on every run. The readings behind each model are in `docs/DECISIONS.md` with quotes and pages; label specs with the same quotes are in `docs/LABELS_RBI.md` and `docs/LABELS_SEBI.md`.

## 4. Behaviour claims

Each rule has a unit test and a mutation test that names the scenarios that catch its removal: `tests/test_benchmark.py` (27 mutation tests), `tests/test_clock.py`, `tests/test_sebi_reporting.py`, `tests/test_workspace.py`, `tests/test_evidence_fields.py`.

## 5. Not done

- **RBI Directions for commercial banks and small finance banks.** These need source documents a person must download.
- **Migrator for the remaining pairs.** Four pairs are mapped. The 2018 UCB basic framework, the 2016 cyber security framework for banks and the 2021 digital payment security controls are on the repeal list and not mapped.
- **IRDAI duties without a stated period** ("periodically", "at regular intervals"). Not modelled; the text gives no period.
- **LLM baselines** for the benchmark. Need API access.
- **Jev (TypeSafe AI, early beta) as a supporting model.** Proposed, not started; needs an API key the owner must create. It returns typed probabilities rather than text, so it may only suggest or rank, never decide a deadline, applicability or anything shown as law. In order of value:
  1. Benchmark baseline: ask it "does this duty apply: yes, no or unknown" on the dev scenarios and report accuracy and calibration next to the deterministic engine. Store its responses so the result is reproducible.
  2. Incident intake triage: estimate the facts the clock needs from a free-text description, used only to order the questions; a person still attests each fact. Off by default, because it sends incident text to a third party.
  3. Second opinion in the migrator: where it disagrees with the lexical method, the mapping becomes `needs_human`. Score it on the same 47 gold mappings.
  4. Card grounding: a probability that each card sentence is supported by the quoted clause, alongside the existing check.
  5. New-circular routing: which entity classes a new publication likely affects, to prioritise human reading.
  Unverified before any build: pricing and limits, run-to-run repeatability, data handling terms.
- **External timestamping of the signed head (RFC 3161), rate limiting on the webhook, more tabletop storylines.** Not started.

## 6. Needs a human

- A compliance professional to review the benchmark labels (`benchmark/REVIEW_PACKET.md` predates RBI and the new SEBI scenarios and needs regenerating first).
- Counsel on the contested readings listed in the README and in `docs/OPEN_QUESTIONS.md`.

## 7. What I am unsure about

- One cyber-incident attestation serves both the RBI definition and SEBI's "cybersecurity incident". They may not be the same test.
- SEBI Table 36 "Days" are counted from the timestamp, the earlier reading.
- The workspace is single-user and file-backed. It has no authentication; it must not be exposed on a network as it stands.
- Codex's sandbox on this machine cannot run the full test suite or write files in the repository root, so its own gate reports are partial; the gate output above is the reviewer agent's.
