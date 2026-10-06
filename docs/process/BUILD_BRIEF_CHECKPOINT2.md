# SentinelBrief — Build Brief, Checkpoint 2

**Audience:** Antigravity ("Anti"), lead builder. Read `BUILD_BRIEF.md` first; it still governs. This brief adds to it and, where the two differ, this one wins for Checkpoint 2.
**Reviewers after you:** the reviewer agent (review and fixes), then Codex (review and fixes). They will re-run everything you claim.
**Starting point:** commit `b7d1bad` plus `scripts/check.py`. State: 125 tests, 17 benchmark scenarios, CERT-In Directions only.

---

## 0. Read this first: how your last checkpoint went

You are fast, well organised and good at structure, volume and following a plan. Checkpoint 1 was a solid skeleton. It also had serious problems, and the pattern matters more than any single bug. Reviewers found:

| What you did | What was true | Why it matters |
| :--- | :--- | :--- |
| Wrote "All checks passed" | `ruff` failed, CI would have been red, tests hard-coded `E:\SentinelBrief` | You reported success without running the gates |
| Described the incident page as server-computed | It ran a private JavaScript copy of the logic and posted to an endpoint that did not exist | You described intent, not the code |
| Marked obligations `human_verified` with reviewer "antigravity-agent" | An AI is not a human reviewer | A trust label that lies is worse than no label |
| Decided "is this an Annexure I incident?" by substring keywords, where no match meant "no" | Two real Annexure I types returned "6-hour report does not apply" | A false "not reportable" is a missed legal filing |
| Modelled a 5-year retention duty as a deadline from `occurrence` | Produced a "deadline" in 2031 | Wrong semantics passed because nothing tested them |
| Evaluated the law "as of now" | A 2021 incident received the 2022 Directions | Brief principle 5 |
| Scorer checked only part of each label | "3/3 adversarial traps passed" verified nothing about the traps | A weak benchmark gives false confidence |
| Never read the MSME extension notice | It was linked from the same page | Incomplete reading of the primary source |

The root causes are three habits. **You report before you verify. You fill gaps with plausible defaults instead of failing loudly. You write tests that confirm your implementation instead of tests that could catch it being wrong.** This brief is built to remove those three habits. It is not a criticism of your ability to build. Your best work is well-specified, structured, mechanical work at volume, so this brief gives you a lot of that, and it puts the hard guardrails exactly where you slipped.

---

## 1. The evidence protocol (non-negotiable)

1. **One command decides "done".** `uv run python scripts/check.py` runs pytest, ruff check, ruff format, mypy strict, `validate_all` and the benchmark, and prints a summary. You may not write "done", "passing" or "green" about anything unless the latest run of this command shows `ALL GATES PASSED`. Paste its summary block, unedited, into HANDOFF.md.
2. **Every claim in HANDOFF.md carries proof.** A claim about behaviour cites the test that proves it (`tests/test_x.py::test_name`) or the command and its output. A claim about the source law cites the document, page and quoted text. If you cannot attach proof, move the claim to "Not verified".
3. **Test first for anything that decides a legal outcome.** For each rule (deadline, applicability, anchor, entity scope, validity date): write the failing test, run it, see it fail for the right reason, then implement. Record the failing run in the commit message body (one line is enough).
4. **Fail loudly.** A missing file, unknown id, unrecognised enum, empty result set, unparseable date or unsupported case must raise or produce an explicit `Unknown`. It must never fall back to a default, an empty list, or "not applicable".
5. **Trust labels mean what they say.** Only a person sets `human_verified`. Your records are `machine_checked` at most. The validator enforces this; do not try to route around it.
6. **Small commits, one concern each,** conventional commit messages. Never commit `.env`, keys or scratch files. Do not commit or leave behind pytest scratch directories.

## 2. Forbidden patterns (each one caused a real bug)

- Substring or keyword matching to decide a legal outcome. Use structured data, exact ids or word-boundary matches, and let "no match" mean "unknown".
- `except Exception: continue`, `.get(x, default)` on a legal field, or returning an empty list on failure.
- Deriving a fact by sniffing an id or a string (`"cert-in" in obs_id`). Put it in data.
- Hard-coded absolute paths, or a data directory that silently loads nothing.
- Two implementations of the same logic (for example JavaScript and Python). Server code is the only place legal logic lives.
- Tests that only re-do the implementation's arithmetic, or assert only that a function returns something.
- Copying legal text or numbers from a blog, a mirror or this brief instead of the official document.
- Using the phrases "should work", "appears to", or "all passing" without a command output next to them.

## 3. The primary-source protocol (for every new instrument)

Do this in order and record each step in the instrument's commit:
1. **Locate the official document.** The regulator's own site or the Gazette only. Mirrors (TrackRBI, blogs, law-firm PDFs) may help you *find* the official URL but are never the source.
2. **Fetch with the existing fetcher** (`ingest/base.py`), so the PDF is hashed and listed in `data/raw/manifest.json`. Then run `sentinelbrief.extract.pdf_text` to produce the `.txt` and `.meta.json` with the correct `instrument_id`. `validate_all` must then pass its provenance checks.
3. **If you cannot reach or read the official document, stop for that instrument.** Mark it BLOCKED in `docs/OPEN_QUESTIONS.md` with what you tried. Do not substitute a secondary source. Missing is acceptable; guessed is not.
4. **Read the whole document, not just the clause you expect.** Find repeals, savings clauses, effective dates, phased commencement, definitions, entity scoping, and annexures. Read any linked amendment or extension notices (the MSME notice was linked on the CERT-In page and you missed it).
5. **Author obligations from verbatim text.** `text_verbatim` and every citation excerpt must be exact substrings. Prefer one obligation per atomic requirement.
6. **Every judgement call becomes a DECISIONS.md entry** with: the exact clause quoted, the interpretation you chose, at least one alternative reading, and why yours is the conservative one (the one that never tells a user they owe less). Then continue with the conservative choice and flag it as needing a human. Do not silently pick one.
7. **Facts in `BUILD_BRIEF.md` section 4 are hypotheses.** If the primary text disagrees, the primary text wins; log the correction.

---

## 4. Work packages

Do them in this order. **Stop and write the checkpoint HANDOFF after WP4 even if later packages are incomplete.** A smaller, verified checkpoint beats a larger, unverified one.

### WP1 — Setup and hygiene (small; do first)
- Write real setup instructions in `README.md`: prerequisites, `uv sync`, `uv run python scripts/check.py`, how to run the app, how to run each source fetch, and where data lives.
- Remove dead code that reviewers flagged: the unused `ClockAnchor`, and the `IncidentProfile` fields the engine never reads (`is_listed`, `holds_personal_data`, `uses_protected_systems`, `is_regulated_cloud_vps`, `is_virtual_asset_provider`, `personal_data_involved`) unless a package below starts using them. Keep the API and tests consistent.
- Move `ENTITY_HIERARCHY` out of `engine.py` into versioned data (`data/entities/*.json`, validated by `schema/entity_class.schema.json`). You need this for WP3.
- **Acceptance:** `scripts/check.py` passes; a new test proves the engine loads the taxonomy from data and rejects an entity class that is not in it.

### WP2 — Make the card feed real (matches brief section 10)
The current feed does not use `cards/generator.py` or `cards/feed.py`, and it does not meet the card spec.
- Cards are built from **structured fields only**, by deterministic templates. No LLM in this checkpoint.
- Regulatory card: headline at most 12 words; body about 60 words (between 45 and 75); chips for issuer, jurisdiction, mandatory or advisory, effective date, and deadline **only when the obligation has an incident deadline** (never for retention or ongoing duties); a working citation to the primary document; the disclaimer "AI-assisted summary, not legal advice. See the source."
- Vulnerability stream: thin. Read a **recorded fixture** of the KEV JSON (do not hit the network in tests). Show CVE id, KEV flag, `knownRansomwareCampaignUse`, and a link. Never present KEV `dueDate` as an Indian deadline; label it "US federal remediation date" if shown at all. Keep `cvss`, `kev`, `epss` and derived `priority` as separate fields; KEV raises priority and never rewrites CVSS. Do not depend on NVD for CVSS or CPE (NIST stopped enriching most CVEs on 15 Apr 2026).
- Wire the feed into `/`. Delete the template logic that bypasses it.
- **Acceptance (each is a test):** every card validates against its record; headline and body length rules hold for all current obligations; no retention duty shows a deadline chip; every regulatory card has a citation that passes the citation validator; no field on a card is absent from its source record; the disclaimer is present; the vulnerability card never shows `dueDate` as an Indian deadline.

### WP3 — New instruments (the core of the checkpoint)
Scope each instrument to what the incident clock needs. Do **not** try to model whole instruments yet. Model only: (a) incident-reporting duties (recipient, deadline, anchor, who it applies to), (b) recurring cadence duties such as vulnerability assessment and penetration testing, (c) effective dates and repeals. Everything else is Phase 1.

Do them in this order, because the first two are most likely to be reachable:
1. **DPDP Rules 2025** (Gazette, notified 13 Nov 2025). The brief cites a MeitY Gazette PDF; find and verify the official URL. Model Rule 7 (breach notification: initial intimation "without delay", detailed report within 72 hours, notification to data principals) and the commencement schedule. The breach duty is **not yet in force** (expected 13 May 2027; verify from the Gazette text, do not trust that date). Use `validity.valid_from`, and add a planning switch to the incident page: "show obligations that take effect later". Never present a not-yet-in-force duty as currently enforceable.
2. **SEBI CSCRF** circular of 20 Aug 2024 (and the April 2025 clarifications). Model the incident-reporting timelines (the brief says 6 hours to CERT-In-type reporting and a 24-hour portal filing; **verify each against the text**, plus the entity categories that scope them).
3. **RBI NBFC cybersecurity Direction** (31 Jul 2026). Find the official RBI document (the reference `RBI/DoS/2026-27/461` is unverified). Model the incident-reporting clause (the brief says six hours to RBI's DAKSH platform), vulnerability assessment and penetration testing cadence, and the repeal. Also fetch RBI's "Circulars Withdrawn" list. If RBI's site blocks you, mark BLOCKED (section 3, step 3) and continue.

Engine work this requires. Decide the design in `docs/DECISIONS.md` first, then test-first:
- "Without delay" has no number. Model it explicitly (for example a `deadline.kind` for "immediate") so the tool tells the user a duty exists and is unbounded, instead of computing nothing or inventing a time.
- Two duties from one incident (CERT-In 6 hours plus RBI 6 hours plus DPDP 72 hours) must each get a clock, a recipient, and a citation, grouped by regulator.
- Where anchors differ between instruments ("detection" versus "noticing" versus "awareness"), keep each as written and ask the user for the timestamp that applies. Do not merge them.
- Entity scoping (NBFC layers, SEBI categories) comes from data (WP1), not code.
- **Acceptance per instrument:** raw files hashed in the manifest and passing provenance; obligations validate with verbatim citations; at least 8 new benchmark scenarios per instrument (WP4); a written list in DECISIONS.md of every interpretation you made and its alternative.

### WP4 — Benchmark to 30+ with the labels-first protocol
You are marking your own homework, so the process has to make that hard to do.
1. **Write labels before code.** For each new instrument, write the scenario files (situation, entity, times, expected regulators, deadlines with anchor, applicable and not-applicable obligations, expected unknowns, `expected.law_as_of`) **from the primary text and commit them on their own, before you touch the engine.** Commit message: `labels: <instrument> scenarios (before implementation)`.
2. Then implement. If a label turns out to be wrong, change it in a separate commit whose message says which label, what was wrong, and quote the clause that shows it. Reviewers will read that history.
3. Reach at least **30 dev scenarios in total**, at least half adversarial, covering for each regulator: the anchor trap, the wrong-entity trap, the not-yet-in-force trap, a repealed-instrument trap, a missing-fact (unknown) case, and a multi-regulator overlap case.
4. Create **at least 10 hidden scenarios** in `benchmark/hidden/` (git-ignored) only after the dev set is frozen. Run the hidden split at most once per checkpoint, report the result, and do not tune against it.
5. Write `scripts/make_review_packet.py` that generates `benchmark/REVIEW_PACKET.md` for an external compliance professional: for each scenario, a plain-English situation, the expected outcome, the quoted clause with page number, and a "correct / incorrect / comment" line. Generating this is your job; reviewing it is a human's.
- **Acceptance:** `scripts/check.py` shows 30+ dev scenarios passing; the mutation tests in `tests/test_benchmark.py` still pass and you have added at least one mutation test per new rule; the review packet is generated and committed. Report counts and Wilson intervals, and state plainly that labels were written by an AI.

### WP5 — Break your own work (before handoff)
Write 15 inputs you believe will break the clock engine, the API, the fetcher and the validators (for example malformed times, DST-like offsets, duplicate ids, empty data, wrong entity for the instrument, contradictory facts, hostile form input). Run them. For each: what happened, whether it failed loudly, and what you changed. List any you did not fix. Put this in HANDOFF.md under "Self-adversarial pass". This is the step that would have caught most of Checkpoint 1's bugs.

### WP6 — Handoff
Use the template below. Do not skip sections. Reviewers will diff it against reality.

---

## 5. Handoff template (HANDOFF.md, replace the old content; keep the old file's Section 0 history in `docs/`)

```
# Checkpoint 2 Handoff
## 1. Gate output (unedited)
<paste the GATE SUMMARY block from scripts/check.py>
## 2. What is done, each with proof
- <claim> — proof: tests/...::test_name  |  command + output  |  clause quote (doc, page)
## 3. What is NOT done or NOT verified
## 4. Shortcuts and things I am unsure about
## 5. Interpretations that need a human (link the DECISIONS.md entries)
## 6. Self-adversarial pass (WP5): inputs tried, results, fixes, unfixed
## 7. Benchmark: counts, Wilson intervals, who wrote the labels, hidden-split result (once)
## 8. Blocked sources and what I tried
## 9. Facts from BUILD_BRIEF.md that the primary text contradicted
```

## 6. What the reviewers will do (so you can do it first)

They will re-run `scripts/check.py`, then try to break it: reintroduce the earlier bug classes (free text deciding reportability, retention as a deadline, law as of today, dropped anchors, naive datetimes), feed adversarial incidents, check every new obligation against the PDF, re-derive your benchmark labels independently, look for claims in HANDOFF.md without proof, and check that nothing decides a legal outcome from a keyword, a default or a mirror. Anything they find that you had not already listed under "Not verified" or "Self-adversarial pass" will be recorded against the handoff's honesty, not just the code.

## 7. Freedom to improve

You may add things that raise correctness, verifiability or clarity, and you should tell us about them. Log each addition in `docs/DECISIONS.md` with the alternative you rejected. Nothing may violate `BUILD_BRIEF.md` section 2 or section 1 of this brief. Do not add new surfaces (mobile, accounts, LLM extraction, RSS pipelines) in this checkpoint. Depth on the four instruments beats breadth. Good places to spend spare effort: extra adversarial scenarios, clearer `Unknown` questions for the user, and sharper error messages.
