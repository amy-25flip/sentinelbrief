"""Generate benchmark/REVIEW_PACKET.md for human compliance reviewers.

The packet puts the contested legal readings first (one decision there settles many scenarios),
then every dev scenario with its facts, expected outcome and the clause quotes behind it.

Usage: python scripts/make_review_packet.py [--check]
--check exits 1 if the committed packet is out of date.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SCENARIOS_DIR = REPO / "benchmark" / "scenarios"
DATA_DIR = REPO / "data"
OUTPUT_FILE = REPO / "benchmark" / "REVIEW_PACKET.md"
REGIMES = [
    ("cert-in", "CERT-In Directions (2022)"),
    ("dpdp", "DPDP Rules 2025, Rule 7"),
    ("sebi", "SEBI CSCRF (2024)"),
    ("rbi", "RBI cybersecurity Directions (2026)"),
    ("irdai", "IRDAI Information and Cyber Security Guidelines (2023)"),
]
CONTESTED_BELOW = 0.9
FACT_LABELS = [
    ("when_occurred", "Occurred"),
    ("when_detected", "Detected"),
    ("when_noticed", "Noticed"),
    ("when_brought_to_notice", "Brought to notice"),
    ("when_aware", "Became aware (DPDP)"),
    ("when_reported_to_sebi", "Reported to SEBI"),
    ("personal_data_involved", "Personal data involved"),
    ("annexure_i_items", "Selected Annexure I items"),
    ("is_annexure_i_type", "Attested Annexure I type"),
    ("is_cyber_incident", "RBI paragraph 4(7) cyber incident"),
    ("is_irdai_cyber_incident", "IRDAI cyber incident"),
    ("is_sebi_cybersecurity_incident", "SEBI cybersecurity incident"),
    ("sebi_severity", "SEBI severity"),
    (
        "sebi_forensic_directed_or_rca_inconclusive",
        "SEBI forensic directed or RCA inconclusive",
    ),
    ("external_events", "External clock events"),
]


def load_obligations() -> dict[str, dict[str, Any]]:
    obligations: dict[str, dict[str, Any]] = {}
    for path in sorted((DATA_DIR / "obligations").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data if isinstance(data, list) else [data]:
            obligations[item["id"]] = item
    return obligations


def _one_line(text: str) -> str:
    return " ".join(text.split())


def _contested(obligations: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "## Part A. Readings to confirm first",
        "",
        f"Each obligation below is modelled on a reading the authors are not sure of (confidence below {CONTESTED_BELOW}).",
        "Confirming or correcting one of these settles every scenario that depends on it.",
        "",
    ]
    for obligation in obligations.values():
        confidence = obligation.get("confidence")
        if confidence is None or confidence >= CONTESTED_BELOW:
            continue
        citation = (obligation.get("citations") or [{}])[0]
        lines += [
            f"### `{obligation['id']}` (confidence {confidence})",
            "",
            f"- **Clause** ({obligation.get('paragraph_ref')}, PDF page {citation.get('page')}): "
            f'"{_one_line(obligation.get("text_verbatim", ""))}"',
            f"- **Modelled as:** {(obligation.get('normalized') or {}).get('action', '')}",
            f"- **Why it is uncertain:** {_one_line(obligation.get('confidence_reason') or '')}",
            "- [ ] Reading is right   - [ ] Reading is wrong (say why): ____________________",
            "",
        ]
    return lines


def _scenario(index: int, s: dict[str, Any], obligations: dict[str, dict[str, Any]]) -> list[str]:
    ep, facts, exp = s.get("entity_profile", {}), s.get("incident_facts", {}), s.get("expected", {})
    classes = ep.get("entity_classes") or [ep.get("entity_class")]
    lines = [
        f"### {index}. `{s.get('id')}`",
        "",
        f"{s.get('description', '')}",
        "",
        f"- **Entity classes:** {', '.join(f'`{c}`' for c in classes)}",
        f"- **Incident type(s) as stated:** {'; '.join(facts.get('incident_types', [])) or 'none'}",
    ]
    for key, label in FACT_LABELS:
        if facts.get(key) is not None:
            value = facts[key]
            if isinstance(value, dict):
                rendered = ", ".join(f"{k}={v}" for k, v in sorted(value.items()))
            elif isinstance(value, list):
                rendered = ", ".join(str(v) for v in value) or "none"
            else:
                rendered = str(value)
            lines.append(f"- **{label}:** `{rendered}`")
    if ep.get("uses_protected_systems") is not None:
        lines.append(f"- **Protected system (NCIIPC):** `{ep['uses_protected_systems']}`")
    lines += [
        "",
        f"**Expected** (law as of `{exp.get('law_as_of')}`; regulators: {', '.join(exp.get('regulators', [])) or 'none'})",
        "",
    ]
    for d in exp.get("deadlines", []):
        lines.append(
            f"- Deadline `{d['deadline_timestamp']}` for `{d['obligation_id']}` "
            f"({d['deadline_iso8601']} from {d['anchor'].replace('_', ' ')})"
        )
    if not exp.get("deadlines"):
        lines.append("- No deadline is computed.")
    deadline_ids = {d["obligation_id"] for d in exp.get("deadlines", [])}
    for c in exp.get("citations", []):
        if c["obligation_id"] not in deadline_ids:
            lines.append(f"- Applies, with no computed deadline: `{c['obligation_id']}`")
    for oid in exp.get("time_critical", []) or []:
        lines.append(f"- Must be done without delay: `{oid}`")
    for na in exp.get("not_applicable", []):
        lines.append(f"- Does not apply: `{na['obligation_id']}`")
    for u in exp.get("unknowns", []):
        lines.append(
            f'- The tool must ask (question contains "{u["question"]}") before deciding `{u["affects"]}`'
        )
    for substring in exp.get("caveats_contain", []) or []:
        lines.append(f'- The result must carry a warning containing "{substring}"')
    quotes = s.get("source_quotes") or []
    if quotes:
        lines += ["", "**Clauses relied on**", ""]
        for q in quotes:
            lines.append(f'- `{q["document"]}`, PDF page {q["page"]}: "{_one_line(q["quote"])}"')
    missing = [
        c["obligation_id"]
        for c in exp.get("citations", [])
        if c["obligation_id"] not in obligations
    ]
    if missing:
        raise SystemExit(f"{s.get('id')}: cites obligations that are not in the dataset: {missing}")
    lines += ["", "- [ ] Correct   - [ ] Incorrect: ____________________", ""]
    return lines


def build() -> str:
    obligations = load_obligations()
    scenarios = [
        json.loads(p.read_text(encoding="utf-8")) for p in sorted(SCENARIOS_DIR.glob("*.json"))
    ]
    lines = [
        "# SentinelBrief: benchmark review packet",
        "",
        "For a compliance professional. Every expected outcome below was written by an AI from the",
        "primary texts and has not been checked by a qualified person. Until it has, no accuracy",
        "figure for this tool should be quoted.",
        "",
        f"{len(scenarios)} dev scenarios over {len(obligations)} modelled obligations.",
        "",
        "How to review: do Part A first. In Part B, tick each scenario or say what is wrong.",
        "PDF page numbers refer to the files in `data/raw/`.",
        "",
        "Reviewer name and organisation: ______________________   Date: ____________",
        "",
    ]
    lines += _contested(obligations)
    lines += ["## Part B. Scenarios", ""]
    index = 0
    grouped: set[str] = set()
    for prefix, title in REGIMES:
        group = [s for s in scenarios if s["id"].startswith(prefix + "-")]
        if not group:
            continue
        lines += [f"## {title} ({len(group)} scenarios)", ""]
        for s in group:
            index += 1
            grouped.add(s["id"])
            lines += _scenario(index, s, obligations)
    rest = [s for s in scenarios if s["id"] not in grouped]
    if rest:
        raise SystemExit(f"Scenarios with no regime group: {[s['id'] for s in rest]}")
    return "\n".join(lines).rstrip("\n") + "\n"


def main(argv: list[str]) -> int:
    packet = build()
    if "--check" in argv:
        current = (
            OUTPUT_FILE.read_text(encoding="utf-8").replace("\r\n", "\n")
            if OUTPUT_FILE.exists()
            else ""
        )
        if current != packet:
            print("benchmark/REVIEW_PACKET.md is out of date; run scripts/make_review_packet.py")
            return 1
        print("review packet is up to date")
        return 0
    OUTPUT_FILE.write_text(packet, encoding="utf-8", newline="\n")
    print(f"Generated review packet at {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
