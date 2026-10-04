# SentinelBrief handoff (2026-10-04)

Written by the reviewer agent. Antigravity is no longer on the project; from Build 9 on, the reviewer agent writes the labels and reviews, and Codex builds. Earlier history is in `docs/REVIEW_LOG.md`.

## 1. Gate output (`python scripts/check.py`, run by the reviewer agent)

```
PASS  pytest             298 passed, 1 deselected, 1 warning
PASS  ruff check         All checks passed!
PASS  ruff format        59 files already formatted
PASS  mypy (strict)      Success: no issues found in 33 source files
PASS  validate_all       All obligations and citations passed validation successfully!
PASS  benchmark dev      Scenarios passed:   92/92  Wilson 95% CI [96.0%, 100.0%]
ALL GATES PASSED
```

Hidden set A (14 scenarios written by the reviewer agent for Codex-built regimes): 14/14 on its only scored run before Build 11, and unchanged after Builds 11 and 12.

Live source re-verification was last run on 2026-09-25 for the CERT-In, DPDP and SEBI sources. The five RBI and IRDAI sources are exempt and pinned by sha256.

## 2. What exists

| Area | State | Built by | Independently reviewed |
|---|---|---|---|
| CERT-In (7 obligations) | modelled | Antigravity, repaired by Codex | yes |
| DPDP Rule 7 (3) | modelled | Antigravity, repaired by Codex | yes |
| SEBI six-hour duty (1) | modelled | Antigravity, repaired by Codex | yes |
| RBI NBFC Direction (6) | modelled | Codex, against the reviewer agent's labels | yes (Review 9) |
| SEBI remaining duties (8) | modelled | Codex started, the reviewer agent finished | **no** |
| Evidence-field cleanup | done | The reviewer agent | **no** |
| Incident workspace | done | The reviewer agent | **no** |
| Provenance attack tests and source pinning | done | The reviewer agent | **no** |
| RBI UCB, AIFI, Payments Banks Directions (12) | modelled | The reviewer agent | **no** |
| IRDAI guidelines (8; partial) | modelled | The reviewer agent | **no** |

## 3. Claims about the law

Every obligation's `text_verbatim` and citation page is machine-checked against the stored text on every run. The readings behind each model are in `docs/DECISIONS.md` with quotes and pages; label specs with the same quotes are in `docs/LABELS_RBI.md` and `docs/LABELS_SEBI.md`.

## 4. Behaviour claims

Each rule has a unit test and a mutation test that names the scenarios that catch its removal: `tests/test_benchmark.py` (27 mutation tests), `tests/test_clock.py`, `tests/test_sebi_reporting.py`, `tests/test_workspace.py`, `tests/test_evidence_fields.py`.

## 5. Not done

- **Independent review of the reviewer agent's builds** (SEBI remaining duties, evidence fields, workspace). Codex hit its usage limit on 2026-10-04; it should review them and its findings go in `docs/REVIEW_LOG.md`.
- **Hidden set B.** Set A (14 scenarios, by the reviewer agent, for Codex-built regimes) exists. Set B, for everything the reviewer agent built, must be written by Codex.
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
