"""Field-level filing drafts.

A draft holds three kinds of field, each labelled with where it came from:
- `computed`: recipient, deadline and clock start, from the deterministic engine;
- `your_input`: facts the user entered;
- `source_text`: content the cited clause says the filing must carry, quoted verbatim, with an
  empty value for a person to complete.

No field value is generated text. The tool does not know what a regulator's form asks beyond
what the ingested clause says, and does not pretend to.
"""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

from sentinelbrief.clock.engine import IST, ClockResult, IncidentClockEngine, IncidentProfile
from sentinelbrief.verify.quotes import SourcePages

Origin = Literal["computed", "your_input", "source_text"]
Urgency = Literal["deadline", "without_delay", "no_time_limit"]
DRAFT_NOTICE = (
    "DRAFT for human review. Not legal advice. This tool does not file anything: a person "
    "approves this draft and submits it on the regulator's own channel."
)
_FACT_LABELS = {
    "when_occurred": "Incident occurred at",
    "when_detected": "Incident detected at",
    "when_noticed": "Incident noticed at",
    "when_brought_to_notice": "Incident brought to notice at",
    "when_aware": "Entity became aware at",
    "when_reported_to_sebi": "Reported to SEBI at",
}


@dataclass(frozen=True)
class DraftField:
    label: str
    value: str | None
    origin: Origin
    citation: str | None = None


@dataclass(frozen=True)
class FilingDraft:
    obligation_id: str
    regulator: str
    recipient: str
    clause: str
    instrument_id: str
    urgency: Urgency
    due_ist: str | None
    action: str
    fields: list[DraftField] = field(default_factory=list)
    notice: str = DRAFT_NOTICE

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def open_fields(self) -> list[DraftField]:
        """Fields a person still has to complete."""
        return [f for f in self.fields if f.value is None]


def load_filing_content(data_dir: str | Path) -> dict[str, list[dict[str, Any]]]:
    """Load the per-obligation content lists and re-verify every quote against its page.

    Fails loudly: a content item that is not in the source would present invented text as the
    law's own words.
    """
    root = Path(data_dir)
    raw = json.loads((root / "reference" / "filing_content.json").read_text(encoding="utf-8"))
    pages = SourcePages(root)
    content: dict[str, list[dict[str, Any]]] = raw["content"]
    for obligation_id, items in content.items():
        if not items:
            raise ValueError(f"filing content for {obligation_id} is empty")
        for item in items:
            pages.require_quote(item["document"], item["page"], item["quote"])
    return content


def _fact_fields(profile: IncidentProfile) -> list[DraftField]:
    fields = [
        DraftField("Entity classes", ", ".join(profile.entity_classes or []), "your_input"),
        DraftField(
            "Incident type(s) as stated", "; ".join(profile.incident_types) or None, "your_input"
        ),
    ]
    for name, label in _FACT_LABELS.items():
        value = getattr(profile, name)
        if value is not None:
            fields.append(
                DraftField(
                    label, value.astimezone(IST).strftime("%d %b %Y, %H:%M IST"), "your_input"
                )
            )
    if profile.systems_affected:
        fields.append(
            DraftField("Systems affected", "; ".join(profile.systems_affected), "your_input")
        )
    if profile.personal_data_involved is not None:
        fields.append(
            DraftField(
                "Personal data involved",
                "yes" if profile.personal_data_involved else "no",
                "your_input",
            )
        )
    return fields


def build_drafts(
    engine: IncidentClockEngine,
    result: ClockResult,
    content: dict[str, list[dict[str, Any]]],
) -> list[FilingDraft]:
    """One draft per applicable reporting duty: timed, without-delay, or event duty with no limit."""
    facts = _fact_fields(result.incident_profile)
    drafts: list[FilingDraft] = []
    seen: set[str] = set()

    def add(obligation_id: str, urgency: Urgency, due: str | None, anchor: str | None) -> None:
        obligation = engine.get_obligation(obligation_id)
        if obligation is None:
            raise ValueError(
                f"Engine returned an obligation that is not in the dataset: {obligation_id}"
            )
        normalized = obligation.get("normalized") or {}
        instrument_id = obligation.get("instrument_id", "")
        clause = obligation.get("paragraph_ref", "")
        citation = f"{instrument_id} {clause}".strip()
        computed = [
            DraftField("Report to", normalized.get("recipient") or None, "computed", citation)
        ]
        if due is not None:
            computed.append(DraftField("Deadline", due, "computed", citation))
        if anchor is not None:
            computed.append(
                DraftField("Clock started by", anchor.replace("_", " "), "computed", citation)
            )
        required = [
            DraftField(
                " ".join(item["quote"].split()),
                None,
                "source_text",
                f"{item['document']} PDF page {item['page']}",
            )
            for item in content.get(obligation_id, [])
        ]
        drafts.append(
            FilingDraft(
                obligation_id=obligation_id,
                regulator=engine._issuer.get(instrument_id, instrument_id.split(".")[0].upper()),
                recipient=normalized.get("recipient") or "",
                clause=clause,
                instrument_id=instrument_id,
                urgency=urgency,
                due_ist=due,
                action=normalized.get("action", ""),
                fields=[*computed, *facts, *required],
            )
        )
        seen.add(obligation_id)

    for deadline in sorted(result.deadlines, key=lambda d: d.deadline_utc):
        if deadline.simulated:
            continue
        add(
            deadline.obligation_id,
            "deadline",
            deadline.deadline_ist.strftime("%d %b %Y, %H:%M IST"),
            deadline.anchor_type,
        )
    for urgent in result.time_critical:
        if urgent.simulated:
            continue
        if urgent.obligation_id not in seen:
            add(urgent.obligation_id, "without_delay", None, urgent.anchor_type)
    for obligation_id in result.applicable_obligations:
        if obligation_id in seen:
            continue
        obligation = engine.get_obligation(obligation_id) or {}
        normalized = obligation.get("normalized") or {}
        # Only duties tied to this incident by a structured gate. An event duty with no gate
        # (for example "comply when CERT-In issues an order") waits on something else.
        gated = bool((obligation.get("applicability") or {}).get("requires"))
        is_event = (normalized.get("trigger") or {}).get("type") == "event"
        if gated and is_event and (normalized.get("deadline") or {}).get("kind") == "none":
            add(obligation_id, "no_time_limit", None, None)
    return drafts
