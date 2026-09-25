"""Generate benchmark/REVIEW_PACKET.md for human compliance reviewers."""

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SCENARIOS_DIR = REPO / "benchmark" / "scenarios"
DATA_DIR = REPO / "data"
OUTPUT_FILE = REPO / "benchmark" / "REVIEW_PACKET.md"


def load_obligations() -> dict[str, dict[str, Any]]:
    obligations: dict[str, dict[str, Any]] = {}
    obl_dir = DATA_DIR / "obligations"
    for p in obl_dir.glob("*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        for item in data if isinstance(data, list) else [data]:
            obligations[item["id"]] = item
    return obligations


def main() -> None:
    obligations = load_obligations()
    scenarios: list[dict[str, Any]] = []
    for p in sorted(SCENARIOS_DIR.glob("*.json")):
        scenarios.append(json.loads(p.read_text(encoding="utf-8")))

    lines: list[str] = [
        "# SentinelBrief — Benchmark Compliance Review Packet",
        "",
        "> **Notice:** This document is generated for external legal/compliance experts to validate",
        "> the benchmark scenario ground truth labels. Benchmark labels were originally drafted by AI",
        "> (`machine_checked`) from official regulatory texts and require independent human verification.",
        "",
        f"**Total Dev Scenarios:** {len(scenarios)}  ",
        "**Generated from:** `benchmark/scenarios/`  ",
        "",
        "---",
        "",
    ]

    for i, s in enumerate(scenarios, start=1):
        s_id = s.get("id", "unknown")
        desc = s.get("description", "")
        ep = s.get("entity_profile", {})
        facts = s.get("incident_facts", {})
        exp = s.get("expected", {})
        adv_flags = s.get("adversarial_flags", [])

        lines.extend(
            [
                f"## Scenario {i}: `{s_id}`",
                "",
                f"**Description:** {desc}",
                "",
                f"**Adversarial Flags:** {', '.join(adv_flags) if adv_flags else 'None'}",
                "",
                "### 1. Situation Facts",
                f"- **Entity Class:** `{ep.get('entity_class')}`",
                f"- **Incident Summary:** {facts.get('description', 'N/A')}",
                f"- **Incident Types:** {', '.join(facts.get('incident_types', []))}",
                f"- **When Detected:** `{facts.get('when_detected') or 'None'}`",
                f"- **When Noticed:** `{facts.get('when_noticed') or 'None'}`",
                f"- **When Brought to Notice:** `{facts.get('when_brought_to_notice') or 'None'}`",
                f"- **When Occurred:** `{facts.get('when_occurred') or 'None'}`",
                f"- **When Aware (DPDP):** `{facts.get('when_aware') or 'None'}`",
                f"- **Personal Data Involved:** `{facts.get('personal_data_involved')}`",
                f"- **Systems Affected:** {', '.join(facts.get('systems_affected', [])) or 'None'}",
                "",
                "### 2. Expected Regulatory Output",
                f"- **Law As-Of Date:** `{exp.get('law_as_of')}`",
                f"- **Applicable Regulators:** {', '.join(exp.get('regulators', []))}",
                "",
                "#### Computed Deadlines",
            ]
        )

        if exp.get("deadlines"):
            for dl in exp["deadlines"]:
                lines.append(
                    f"- **{dl.get('regulator')}** (`{dl.get('obligation_id')}`): "
                    f"Anchor `{dl.get('anchor')}`, Duration `{dl.get('deadline_iso8601')}` "
                    f"-> Deadline `{dl.get('deadline_timestamp')}`"
                )
        else:
            lines.append("- *(No active incident deadlines expected)*")

        lines.extend(["", "#### Required Citations & Legal Basis"])
        if exp.get("citations"):
            for cit in exp["citations"]:
                obl_id = cit.get("obligation_id")
                obl = obligations.get(obl_id, {})
                verbatim = obl.get("text_verbatim", "N/A")
                lines.extend(
                    [
                        f"- **Obligation `{obl_id}`** ({cit.get('instrument_id')}, {cit.get('paragraph_ref')}):",
                        f'  > *"{verbatim}"*',
                    ]
                )
        else:
            lines.append("- *(No specific citations)*")

        if exp.get("not_applicable"):
            lines.extend(["", "#### Explicitly Not Applicable"])
            for na in exp["not_applicable"]:
                lines.append(f"- `{na.get('obligation_id')}`: {na.get('reason')}")

        if exp.get("unknowns"):
            lines.extend(["", "#### Expected Clarifying Unknowns Required"])
            for unk in exp["unknowns"]:
                lines.append(
                    f'- Question: *"{unk.get("question")}"* (affects `{unk.get("affects")}`)'
                )

        lines.extend(
            [
                "",
                "### 3. Human Reviewer Verdict",
                "- [ ] **CORRECT** (Expected outcome, deadlines, and anchors are legally accurate)",
                "- [ ] **INCORRECT** (Discrepancy found)",
                "- **Reviewer Name / Organisation:** _______________________",
                "- **Date:** _______________",
                "- **Reviewer Comments / Corrections:**",
                "",
                "---",
                "",
            ]
        )

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated review packet with {len(scenarios)} scenarios at {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
