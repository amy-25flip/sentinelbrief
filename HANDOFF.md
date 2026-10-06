# SentinelBrief handoff (2026-10-06)

Written by the reviewer agent. Antigravity is no longer on the project; from Build 9 on, the reviewer agent writes the labels and reviews, and Codex builds. Earlier history is in `docs/REVIEW_LOG.md`.

## 1. Gate output (`python scripts/check.py`, run by the reviewer agent on 2026-10-06)

```
PASS  pytest             368 passed, 1 deselected, 1 warning
PASS  ruff check         All checks passed!
PASS  ruff format        65 files already formatted
PASS  mypy (strict)      Success: no issues found in 33 source files
PASS  validate_all       All obligations and citations passed validation successfully!
PASS  benchmark dev      Scenarios passed:   104/104  Wilson 95% CI [96.4%, 100.0%]
ALL GATES PASSED
```

Hidden split (git-ignored, 30 scenarios): 29/30. Set A (14, written by the reviewer agent for Codex-built regimes) 14/14; set B (16, written by Codex for the reviewer agent-built work) 15/16. The one failure is the contested SEBI start date (Review 12, Q5).

Live source re-verification, 2026-10-05: 5 passed, 0 failed, 5 skipped (RBI and IRDAI hosts refuse automated clients; those sources are pinned by sha256).

## 2. What exists

| Area | Built by | Reviewed by |
|---|---|---|
| CERT-In (7), DPDP Rule 7 (3), SEBI six-hour duty | Antigravity, repaired by Codex | The reviewer agent (Reviews 1 to 8) |
| RBI NBFC Direction (6) | Codex, against the reviewer agent's labels | The reviewer agent (Review 9) |
| SEBI remaining duties, forensic and quarterly (10 more) | Codex and the reviewer agent | Codex (Review 12), fixes checked by the reviewer agent (Review 13) |
| RBI UCB, AIFI, Payments Banks Directions (12) | The reviewer agent | Codex (Review 12: found sound) |
| IRDAI guidelines (8; partial) | The reviewer agent | Codex (Review 12), fixes checked by the reviewer agent |
| Incident workspace, external clocks, evidence fields, cards | The reviewer agent | The reviewer agent self-review (Review 11), then Codex (Review 12) |
| Provenance attack tests and source pinning | The reviewer agent | Codex (Review 12: found sound) |

## 3. Claims about the law

Every obligation's `text_verbatim` and citation page is machine-checked against the stored text on every run. The readings behind each model are in `docs/DECISIONS.md` with quotes and pages; label specs with the same quotes are in `docs/LABELS_RBI.md` and `docs/LABELS_SEBI.md`.

## 4. Behaviour claims

Each rule has a unit test and a mutation test that names the scenarios that catch its removal: `tests/test_benchmark.py` (27 mutation tests), `tests/test_clock.py`, `tests/test_sebi_reporting.py`, `tests/test_workspace.py`, `tests/test_evidence_fields.py`.

## 5. Not done

- **RBI Directions for commercial banks and small finance banks, the repeal list and old circular texts, and the migrator.** These need source documents a person must download.
- **The rest of the IRDAI guidelines** (about 20 policies unread).
- **LLM baselines** for the benchmark. Need API access.
- **Signing the timeline head hash; SIEM input; tabletop generator.** Optional items in the brief, not started.

## 6. Needs a human

- A compliance professional to review the benchmark labels (`benchmark/REVIEW_PACKET.md` predates RBI and the new SEBI scenarios and needs regenerating first).
- Counsel on the contested readings listed in the README and in `docs/OPEN_QUESTIONS.md`.

## 7. What I am unsure about

- One cyber-incident attestation serves both the RBI definition and SEBI's "cybersecurity incident". They may not be the same test.
- SEBI Table 36 "Days" are counted from the timestamp, the earlier reading.
- The workspace is single-user and file-backed. It has no authentication; it must not be exposed on a network as it stands.
- Codex's sandbox on this machine cannot run the full test suite or write files in the repository root, so its own gate reports are partial; the gate output above is the reviewer agent's.
