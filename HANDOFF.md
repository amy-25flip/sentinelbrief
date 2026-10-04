# SentinelBrief handoff (2026-10-04)

Written by the reviewer agent. Antigravity is no longer on the project; from Build 9 on, the reviewer agent writes the labels and reviews, and Codex builds. Earlier history is in `docs/REVIEW_LOG.md`.

## 1. Gate output (`python scripts/check.py`, run by the reviewer agent)

```
PASS  pytest             259 passed, 1 deselected, 1 warning
PASS  ruff check         All checks passed!
PASS  ruff format        55 files already formatted
PASS  mypy (strict)      Success: no issues found in 33 source files
PASS  validate_all       All obligations and citations passed validation successfully!
PASS  benchmark dev      Scenarios passed:   68/68  Wilson 95% CI [94.7%, 100.0%]
ALL GATES PASSED
```

Live source re-verification was last run on 2026-09-25 (5 passed, 0 failed, 1 skipped). No source file has changed since.

## 2. What exists

| Area | State | Built by | Independently reviewed |
|---|---|---|---|
| CERT-In (7 obligations) | modelled | Antigravity, repaired by Codex | yes |
| DPDP Rule 7 (3) | modelled | Antigravity, repaired by Codex | yes |
| SEBI six-hour duty (1) | modelled | Antigravity, repaired by Codex | yes |
| RBI NBFC Direction (6) | modelled | Codex, against the reviewer agent's labels | yes (Reviews 9) |
| SEBI remaining duties (8) | modelled | Codex started, the reviewer agent finished | **no** |
| Evidence-field cleanup | done | The reviewer agent | **no** |
| Incident workspace | done | The reviewer agent | **no** |

## 3. Claims about the law

Every obligation's `text_verbatim` and citation page is machine-checked against the stored text on every run. The readings behind each model are in `docs/DECISIONS.md` with quotes and pages; label specs with the same quotes are in `docs/LABELS_RBI.md` and `docs/LABELS_SEBI.md`.

## 4. Behaviour claims

Each rule has a unit test and a mutation test that names the scenarios that catch its removal: `tests/test_benchmark.py` (27 mutation tests), `tests/test_clock.py`, `tests/test_sebi_reporting.py`, `tests/test_workspace.py`, `tests/test_evidence_fields.py`.

## 5. Not done

- **Independent review of the reviewer agent's builds** (SEBI remaining duties, evidence fields, workspace). Codex hit its usage limit on 2026-10-04; it should review them and its findings go in `docs/REVIEW_LOG.md`.
- **Hidden benchmark split.** None exists. The party that did not build a regime should write its hidden scenarios.
- **Adversarial pass (WP-E)** against the provenance controls for the new work.
- **IRDAI, the other RBI Directions, the repeal list and the migrator.** These need source documents from regulator sites, which the owner must authorise or supply.
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
