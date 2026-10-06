"""Incident cases on local disk: facts, draft approval by a named person, and an audit bundle.

Incident data is sensitive. Cases are plain files under a directory the operator chooses; nothing
is sent anywhere. Every state change is appended to the case's hash-chained evidence timeline.
"""

import hashlib
import json
import re
import uuid
from dataclasses import replace
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from sentinelbrief.clock.engine import ClockResult, IncidentClockEngine, IncidentProfile
from sentinelbrief.evidence.timeline import EvidenceTimeline, canonical_json
from sentinelbrief.workspace.drafts import FilingDraft, build_drafts, load_filing_content

_CASE_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_TIME_FIELDS = (
    "when_noticed",
    "when_brought_to_notice",
    "when_detected",
    "when_occurred",
    "when_aware",
    "when_reported_to_sebi",
)
_FACT_FIELDS = (
    *_TIME_FIELDS,
    "entity_classes",
    "incident_description",
    "incident_types",
    "annexure_i_items",
    "personal_data_involved",
    "uses_protected_systems",
    "systems_affected",
    "is_annexure_i_type",
    "is_cyber_incident",
    "is_irdai_cyber_incident",
    "is_sebi_cybersecurity_incident",
    "sebi_severity",
    "sebi_forensic_directed_or_rca_inconclusive",
    "external_events",
)
# A person approves and files. Names that indicate an AI agent or a placeholder are refused.
_NON_HUMAN = (
    "agent",
    "antigravity",
    "claude",
    "codex",
    "gpt",
    "gemini",
    "llm",
    "bot",
    "system",
    "auto",
)


def profile_to_facts(profile: IncidentProfile) -> dict[str, Any]:
    """JSON-safe copy of the profile (timestamps as ISO strings with offset)."""
    facts: dict[str, Any] = {}
    for name in _FACT_FIELDS:
        value = getattr(profile, name)
        if name == "external_events":
            value = {key: when.isoformat() for key, when in value.items()}
        facts[name] = value.isoformat() if isinstance(value, datetime) else value
    return facts


def facts_to_profile(facts: dict[str, Any]) -> IncidentProfile:
    unknown = set(facts) - set(_FACT_FIELDS)
    if unknown:
        raise ValueError(f"Unknown fact field(s): {', '.join(sorted(unknown))}")
    kwargs = dict(facts)
    for name in _TIME_FIELDS:
        if kwargs.get(name) is not None:
            kwargs[name] = datetime.fromisoformat(str(kwargs[name]))
    kwargs["external_events"] = {
        str(key): datetime.fromisoformat(str(when))
        for key, when in (kwargs.get("external_events") or {}).items()
    }
    return IncidentProfile(**kwargs)


def _require_person(name: str, role: str) -> str:
    cleaned = (name or "").strip()
    if len(cleaned) < 2:
        raise ValueError(f"{role} must be a named person")
    if any(tag in cleaned.lower().split() or cleaned.lower() == tag for tag in _NON_HUMAN):
        raise ValueError(f"{role} must be a person, not '{cleaned}'")
    return cleaned


def draft_digest(draft: FilingDraft) -> str:
    """SHA-256 of the draft's content, recorded when a person approves it."""
    return hashlib.sha256(canonical_json(draft.to_dict()).encode("utf-8")).hexdigest()


def draft_dict_digest(draft: dict[str, Any]) -> str:
    """SHA-256 of a serialized draft snapshot."""
    return hashlib.sha256(canonical_json(draft).encode("utf-8")).hexdigest()


class CaseStore:
    """File-backed incident cases. Single writer; not a multi-user system."""

    def __init__(self, root: str | Path, data_dir: str | Path):
        self.root = Path(root)
        self.data_dir = Path(data_dir)
        self.engine = IncidentClockEngine(self.data_dir)
        self.content = load_filing_content(self.data_dir)

    # --- storage ---

    def _dir(self, case_id: str) -> Path:
        if not _CASE_ID_RE.match(case_id):
            raise ValueError("Invalid case id")
        path = self.root / case_id
        if not (path / "case.json").is_file():
            raise KeyError(f"No such case: {case_id}")
        return path

    def _read(self, case_id: str) -> dict[str, Any]:
        value: dict[str, Any] = json.loads(
            (self._dir(case_id) / "case.json").read_text(encoding="utf-8")
        )
        return value

    def _write(self, case: dict[str, Any]) -> None:
        path = self.root / case["id"] / "case.json"
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(case, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
        )
        tmp.replace(path)

    def timeline(self, case_id: str) -> EvidenceTimeline:
        return EvidenceTimeline(self._dir(case_id) / "timeline.jsonl")

    # --- operations ---

    def create(self, profile: IncidentProfile, actor: str) -> str:
        actor = _require_person(actor, "The person opening the case")
        self.engine.evaluate(profile)  # reject invalid facts before anything is stored
        case_id = uuid.uuid4().hex
        (self.root / case_id).mkdir(parents=True, exist_ok=False)
        case = {
            "id": case_id,
            "created_at": datetime.now(UTC).isoformat(),
            "created_by": actor,
            "facts": profile_to_facts(profile),
            "drafts": {},
        }
        self._write(case)
        self.timeline(case_id).append(actor, "incident_created", {"facts": case["facts"]})
        return case_id

    def evaluate(
        self, case_id: str, now: datetime | None = None
    ) -> tuple[ClockResult, list[FilingDraft]]:
        case = self._read(case_id)
        result = self.engine.evaluate(facts_to_profile(case["facts"]), now=now)
        drafts = []
        for draft in build_drafts(self.engine, result, self.content):
            entries = (case.get("entries") or {}).get(draft.obligation_id) or {}
            fields = [
                replace(f, value=entries[f.label])
                if f.origin == "source_text" and f.label in entries
                else f
                for f in draft.fields
            ]
            drafts.append(replace(draft, fields=fields))
        return result, drafts

    def view(self, case_id: str, now: datetime | None = None) -> dict[str, Any]:
        """Everything a page or API client needs for one case."""
        case = self._read(case_id)
        result, drafts = self.evaluate(case_id, now=now)
        rows = []
        for draft in drafts:
            state = dict(case["drafts"].get(draft.obligation_id) or {"status": "draft"})
            rendered = draft.to_dict()
            if state["status"] == "filed":
                snapshot = state.get("filed_snapshot")
                if not isinstance(snapshot, dict):
                    state = {"status": "draft", "note": "filed draft snapshot missing"}
                elif state.get("filed_snapshot_digest") != draft_dict_digest(snapshot):
                    state = {"status": "draft", "note": "filed draft snapshot digest mismatch"}
                else:
                    rendered = snapshot
                    live_digest = draft_digest(draft)
                    if live_digest != state.get("filed_snapshot_digest"):
                        state["note"] = (
                            "filed snapshot shown; live draft would now differ from the filed content"
                        )
            if state["status"] == "approved" and state.get("approved_digest") != draft_digest(
                draft
            ):
                # Defence in depth: an approval never covers content it did not see.
                state = {"status": "draft", "note": "content changed after approval; approve again"}
            rows.append(
                {
                    "draft": rendered,
                    "open_fields": len(
                        [f for f in rendered.get("fields", []) if f.get("value") is None]
                    ),
                    **state,
                }
            )
        ok, first_bad = self.timeline(case_id).verify()
        external = []
        for obligation_id in result.applicable_obligations:
            obligation = self.engine.get_obligation(obligation_id) or {}
            normalized = obligation.get("normalized") or {}
            deadline = normalized.get("deadline") or {}
            if deadline.get("anchor") == "external_event":
                external.append(
                    {
                        "id": obligation_id,
                        "action": normalized.get("action", ""),
                        "within": deadline.get("duration_iso8601"),
                        "starts_from": (normalized.get("trigger") or {}).get("description", ""),
                        "started": (case["facts"].get("external_events") or {}).get(obligation_id),
                    }
                )
        return {
            "external_clocks": external,
            "case": {k: case[k] for k in ("id", "created_at", "created_by", "facts")},
            "clock": result.to_dict(),
            "drafts": rows,
            "timeline": {
                "events": len(self.timeline(case_id)),
                "head_hash": self.timeline(case_id).head_hash(),
                "valid": ok,
                "first_break_seq": first_bad,
            },
        }

    def update_facts(self, case_id: str, changes: dict[str, Any], actor: str) -> None:
        """Record new or corrected facts. Approvals not yet filed are withdrawn."""
        actor = _require_person(actor, "The person recording facts")
        if not changes:
            raise ValueError("No facts given")
        case = self._read(case_id)
        merged = {**case["facts"], **changes}
        profile = facts_to_profile(merged)
        self.engine.evaluate(profile)
        before = {k: case["facts"].get(k) for k in changes}
        case["facts"] = profile_to_facts(profile)
        withdrawn = []
        for obligation_id, state in case["drafts"].items():
            if state["status"] == "approved":
                case["drafts"][obligation_id] = {
                    "status": "draft",
                    "note": "facts changed; approve again",
                }
                withdrawn.append(obligation_id)
        timeline = self.timeline(case_id)
        timeline.append(
            actor,
            "fact_recorded",
            {
                "changed": {k: case["facts"][k] for k in changes},
                "previous": before,
                "approvals_withdrawn": withdrawn,
            },
        )
        self._write(case)

    def _draft(self, case_id: str, obligation_id: str) -> FilingDraft:
        _, drafts = self.evaluate(case_id)
        draft = next((d for d in drafts if d.obligation_id == obligation_id), None)
        if draft is None:
            raise KeyError(f"No draft for {obligation_id} in this case")
        return draft

    def set_entry(
        self, case_id: str, obligation_id: str, label: str, value: str, actor: str
    ) -> None:
        """A person completes one field the clause requires. Withdraws an unfiled approval."""
        actor = _require_person(actor, "The person completing the field")
        case = self._read(case_id)
        state = case["drafts"].get(obligation_id) or {}
        if state.get("status") == "filed":
            raise ValueError("This filing is already recorded as filed")
        draft = self._draft(case_id, obligation_id)
        if label not in {f.label for f in draft.fields if f.origin == "source_text"}:
            raise ValueError("That is not a field the cited clause requires for this filing")
        text = value.strip()
        entries = case.setdefault("entries", {}).setdefault(obligation_id, {})
        if text:
            entries[label] = text
        else:
            entries.pop(label, None)
        withdrawn = state.get("status") == "approved"
        if withdrawn:
            case["drafts"][obligation_id] = {
                "status": "draft",
                "note": "field changed; approve again",
            }
        self.timeline(case_id).append(
            actor,
            "note_added",
            {
                "obligation_id": obligation_id,
                "field": label,
                "value": text,
                "approval_withdrawn": withdrawn,
            },
        )
        self._write(case)

    def approve(
        self, case_id: str, obligation_id: str, approver: str, accept_open_fields: bool = False
    ) -> str:
        """A named person approves the current draft content. Returns the content digest.

        A draft with fields still empty is approved only if the approver says so explicitly.
        """
        approver = _require_person(approver, "The approver")
        case = self._read(case_id)
        if (case["drafts"].get(obligation_id) or {}).get("status") == "filed":
            raise ValueError("This filing is already recorded as filed")
        draft = self._draft(case_id, obligation_id)
        empty = len(draft.open_fields())
        if empty and not accept_open_fields:
            raise ValueError(
                f"{empty} field(s) the clause requires are still empty. Complete them, or approve "
                "with accept_open_fields to record that they will be completed on the regulator's channel."
            )
        digest = draft_digest(draft)
        now = datetime.now(UTC).isoformat()
        self.timeline(case_id).append(
            approver,
            "draft_approved",
            {"obligation_id": obligation_id, "draft_sha256": digest, "fields_left_empty": empty},
        )
        case["drafts"][obligation_id] = {
            "status": "approved",
            "approved_by": approver,
            "approved_at": now,
            "approved_digest": digest,
            "fields_left_empty": empty,
        }
        self._write(case)
        return digest

    def record_filing(
        self, case_id: str, obligation_id: str, filed_by: str, reference: str, filed_at: datetime
    ) -> None:
        """Record that a person filed on the regulator's own channel. The tool files nothing."""
        filed_by = _require_person(filed_by, "The person who filed")
        if filed_at.tzinfo is None or filed_at.utcoffset() is None:
            raise ValueError("filed_at must be timezone-aware")
        if filed_at > datetime.now(UTC) + timedelta(minutes=5):
            raise ValueError(
                "filed_at is in the future; record a filing only after it has been made"
            )
        if not reference.strip():
            raise ValueError(
                "A filing reference (acknowledgement number or message id) is required"
            )
        case = self._read(case_id)
        created_at = datetime.fromisoformat(case["created_at"])
        if filed_at.astimezone(UTC) < created_at.astimezone(UTC):
            raise ValueError("filed_at cannot be before the case was opened")
        state = case["drafts"].get(obligation_id) or {}
        if state.get("status") != "approved":
            raise ValueError("A draft must be approved by a person before a filing is recorded")
        approved_at = datetime.fromisoformat(state.get("approved_at", ""))
        if filed_at.astimezone(UTC) < approved_at.astimezone(UTC):
            raise ValueError("filed_at cannot be before the draft was approved")
        draft = self._draft(case_id, obligation_id)
        if state.get("approved_digest") != draft_digest(draft):
            raise ValueError(
                "The draft changed after approval; approve it again before recording a filing"
            )
        snapshot = draft.to_dict()
        snapshot_digest = draft_dict_digest(snapshot)
        self.timeline(case_id).append(
            filed_by,
            "filing_recorded",
            {
                "obligation_id": obligation_id,
                "reference": reference.strip(),
                "filed_at": filed_at.isoformat(),
                "draft_sha256": state["approved_digest"],
                "filed_snapshot_sha256": snapshot_digest,
            },
        )
        case["drafts"][obligation_id] = {
            **state,
            "status": "filed",
            "filed_by": filed_by,
            "filed_at": filed_at.isoformat(),
            "reference": reference.strip(),
            "filed_snapshot": snapshot,
            "filed_snapshot_digest": snapshot_digest,
        }
        self._write(case)

    def export(self, case_id: str, output_dir: str | Path) -> Path:
        """Write the auditor bundle: timeline, clocks, drafts, the law as applied, and a manifest."""
        out = Path(output_dir)
        self.timeline(case_id).export_bundle(out)
        case = self._read(case_id)
        result, drafts = self.evaluate(case_id)
        cited = [d.obligation_id for d in drafts] + result.applicable_obligations
        law = []
        for obligation_id in dict.fromkeys(cited):
            obligation = self.engine.get_obligation(obligation_id) or {}
            law.append(
                {
                    "obligation_id": obligation_id,
                    "instrument_id": obligation.get("instrument_id"),
                    "paragraph_ref": obligation.get("paragraph_ref"),
                    "text_verbatim": obligation.get("text_verbatim"),
                    "citations": obligation.get("citations"),
                    "validity": obligation.get("validity"),
                    "verification": obligation.get("verification"),
                    "confidence": obligation.get("confidence"),
                    "confidence_reason": obligation.get("confidence_reason"),
                }
            )
        files: dict[str, Any] = {
            "case.json": case,
            "clock_result.json": result.to_dict(),
            "drafts.json": [
                {
                    **(
                        (case["drafts"].get(d.obligation_id) or {}).get("filed_snapshot")
                        or d.to_dict()
                    ),
                    "state": case["drafts"].get(d.obligation_id) or {"status": "draft"},
                }
                for d in drafts
            ],
            "law_snapshot.json": {"law_as_of": result.law_as_of.isoformat(), "obligations": law},
        }
        for name, value in files.items():
            (out / name).write_text(
                json.dumps(value, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
                newline="\n",
            )
        lines = [
            "# Incident case bundle",
            "",
            EvidenceTimeline.DISCLAIMER,
            "",
            "Deadlines and applicability were computed by a deterministic engine from the facts in",
            "`case.json` and the law in `law_snapshot.json` (evaluated as of the incident date).",
            "Drafts are not filings. A filing appears here only because a person recorded that they",
            "filed it; this tool submitted nothing. Not legal advice.",
            "",
            f"- Case: `{case['id']}` opened {case['created_at']} by {case['created_by']}",
            f"- Law as of: {result.law_as_of.isoformat()}",
            f"- Open questions: {len(result.unknowns)}",
            "",
            "| Duty | Recipient | Due | State |",
            "|---|---|---|---|",
        ]
        for draft in drafts:
            state = case["drafts"].get(draft.obligation_id) or {"status": "draft"}
            lines.append(
                f"| {draft.obligation_id} | {draft.recipient} | {draft.due_ist or draft.urgency} | {state['status']} |"
            )
        (out / "CASE_SUMMARY.md").write_text(
            "\n".join(lines) + "\n", encoding="utf-8", newline="\n"
        )
        manifest = {
            "generated_at": datetime.now(UTC).isoformat(),
            "files": {
                path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                for path in sorted(out.iterdir())
                if path.is_file() and path.name != "bundle_manifest.json"
            },
        }
        (out / "bundle_manifest.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n"
        )
        return out
