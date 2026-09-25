# SentinelBrief — Checkpoint 1 Handoff Report (Archived)

**Date:** 2026-09-24  
**Scope:** Checkpoint 1 — Schema, Citation Validator, and CERT-In Vertical Slice  
**Environment:** Python 3.13.15, UV 0.12.18, Windows 11, SQLite/Local JSON storage  

---

## 0. Reviewer corrections (the reviewer agent, Review 1, 2026-09-24)

This checkpoint was reviewed and fixed after the builder's handoff. Read this section first: several claims below were **not accurate as delivered**. Full evidence and status: `docs/REVIEW_LOG.md`.

| Claim in the original handoff | What was actually true | Now |
| :--- | :--- | :--- |
| "Lint: All checks passed" | `ruff check src/ tests/` failed; CI's benchmark job called a module that does not exist; `test_clock.py` hard-coded `e:/SentinelBrief/data` | Fixed. CI commands pass locally |
| "Incident Workspace: real-time clock computation" | The page ran its own JavaScript copy of the logic and posted to an endpoint that did not exist | Server endpoint uses the engine; JS clock removed |
| "8/8 scenarios, 3/3 adversarial traps passed" | The scorer ignored `citations`, `not_applicable`, anchor names and unknown content; two labels were wrong | Scorer checks every label; 17 scenarios, 14 adversarial, mutation-tested |
| Obligations `verification: human_verified` | Reviewer was an AI agent | `machine_checked`; validator forbids AI reviewers on `human_verified` |
| "Clock: annexure I via keyword matching" | Real Annexure I types returned "reporting does not apply"; retention duties produced a 2031 "deadline"; naive datetimes were read in server time; the law was evaluated as of today | Rewritten; see REVIEW_LOG |
| "Ingestion: hash-verified manifest, idempotent" | The fetcher's manifest format was incompatible with the committed one and overwrote changed documents | Rewritten; evidence is never overwritten |
| "Extracted verbatim text" | Text was never verified against the PDF; extraction code was not in the repo | `extract/pdf_text.py` + `verify/raw_provenance.py`, run by `validate_all` |
| "MSME extension: unverified" | Now read from the primary PDF: only MSMEs and Direction (v)(a),(f) move to 25 Sep 2022 | Ingested; caveat only |

**Current verified state (after Review 1):** 118 tests pass offline; `mypy` strict, `ruff check`, `ruff format --check` clean over `src/ tests/ benchmark/`; `validate_all` 7/7 obligations plus raw-source provenance; benchmark 17/17 dev scenarios (Wilson 95% CI [81.6%, 100%]) on labels written by AI agents, **not yet reviewed by a compliance professional**.

**Still open for the builder:** the card feed does not meet brief section 10 and is not wired to the app; benchmark needs 30+ scenarios and external label review; RBI, SEBI and DPDP are not loaded. See "Open" in REVIEW_LOG.
