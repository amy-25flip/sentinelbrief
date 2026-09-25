"""Deterministic incident clock. No LLM is involved anywhere in this module.

Design rules (see BUILD_BRIEF sections 2 and 9):
- Free text can never establish that an incident is NOT reportable. Only an explicit
  user attestation can. Anything unresolved becomes an Unknown the user must answer.
- Every timestamp must be timezone-aware. Naive datetimes are rejected, never guessed.
- The law is evaluated as of the incident date, not as of today.
- Retention and other ongoing duties never produce an incident deadline.
"""

import json
import re
from dataclasses import dataclass, field
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from sentinelbrief.clock.taxonomy import EntityTaxonomy
from sentinelbrief.models import Obligation

# IST is UTC+5:30, always. India does not observe DST.
IST = timezone(timedelta(hours=5, minutes=30))

# Which IncidentProfile field supplies each anchor.
_ANCHOR_FIELDS: dict[str, str] = {
    "noticing": "when_noticed",
    "brought_to_notice": "when_brought_to_notice",
    "detection": "when_detected",
    "occurrence": "when_occurred",
    "awareness": "when_aware",
}
_ANCHOR_LABELS: dict[str, str] = {
    "noticing": "first noticed",
    "brought_to_notice": "brought to notice",
    "detection": "detected",
    "occurrence": "occurring",
    "awareness": "became known to the entity",
}
_DATETIME_FIELDS = tuple(_ANCHOR_FIELDS.values())

# CERT-In's MSME notice of 27 Jun 2022 delays effectiveness to 25 Sep 2022 for MSMEs and for
# Direction (v)(a) and (f). The engine does not model MSME status or sub-clause dates.
_MSME_EFFECTIVE = date(2022, 9, 25)


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


@dataclass(frozen=True)
class DeadlineResult:
    """A computed deadline for one obligation."""

    obligation_id: str
    regulator: str
    obligation_action: str
    anchor_type: str
    anchor_timestamp: datetime
    deadline_utc: datetime
    deadline_ist: datetime
    duration_iso8601: str
    status: str  # 'pending' | 'overdue'
    citation_paragraph: str
    citation_instrument: str
    recipient: str
    channel: str | None


@dataclass(frozen=True)
class TimeCriticalResult:
    """An applicable duty that must be done without delay but has no fixed clock."""

    obligation_id: str
    regulator: str
    obligation_action: str
    anchor_type: str | None
    citation_paragraph: str
    citation_instrument: str
    recipient: str | None


@dataclass(frozen=True)
class Unknown:
    """A fact the system needs but does not have."""

    question: str
    affects: list[str]
    impact: str


@dataclass(frozen=True)
class AnnexureResolution:
    """How (or whether) the incident was matched to a CERT-In Annexure I type."""

    decision: bool | None  # True / False (only via attestation) / None = unresolved
    basis: str  # 'user_attested' | 'structured' | 'term_match' | 'unresolved'
    matched: list[str]
    suggestions: list[str]


@dataclass
class IncidentProfile:
    """User-provided entity and incident facts. All datetimes must be timezone-aware."""

    entity_class: str

    incident_description: str = ""
    incident_types: list[str] = field(default_factory=list)
    annexure_i_items: list[str] = field(default_factory=list)  # e.g. ["annexure_i.v"]
    when_detected: datetime | None = None
    when_noticed: datetime | None = None
    when_brought_to_notice: datetime | None = None
    when_occurred: datetime | None = None
    when_aware: datetime | None = None
    personal_data_involved: bool | None = None
    systems_affected: list[str] = field(default_factory=list)
    # Explicit user attestation. Only this can make Annexure I "not applicable".
    is_annexure_i_type: bool | None = None

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        for name in _DATETIME_FIELDS:
            value = getattr(self, name)
            if value is not None and (value.tzinfo is None or value.utcoffset() is None):
                raise ValueError(
                    f"{name} must be timezone-aware; a naive datetime would be silently read "
                    "in the server's local timezone, which can shift a legal deadline by hours"
                )
        if self.is_annexure_i_type is False and self.annexure_i_items:
            raise ValueError(
                "Conflicting input: incident attested as NOT Annexure I but Annexure I types selected"
            )

    def earliest_known_time(self) -> datetime | None:
        known = [getattr(self, n) for n in _DATETIME_FIELDS if getattr(self, n) is not None]
        return min(known) if known else None


@dataclass
class ClockResult:
    """Full result of running the clock engine."""

    incident_profile: IncidentProfile
    deadlines: list[DeadlineResult]
    time_critical: list[TimeCriticalResult]
    unknowns: list[Unknown]
    applicable_obligations: list[str]
    not_applicable: list[dict[str, Any]]
    undetermined: list[str]
    conditions_unevaluated: dict[str, list[str]]
    caveats: list[str]
    annexure_i: AnnexureResolution
    computed_at: datetime
    law_as_of: date

    def to_dict(self) -> dict[str, Any]:
        return {
            "law_as_of": self.law_as_of.isoformat(),
            "computed_at": self.computed_at.isoformat(),
            "deadlines": [
                {
                    "obligation_id": d.obligation_id,
                    "regulator": d.regulator,
                    "action": d.obligation_action,
                    "anchor": d.anchor_type,
                    "anchor_timestamp": d.anchor_timestamp.isoformat(),
                    "deadline_utc": d.deadline_utc.isoformat(),
                    "deadline_ist": d.deadline_ist.isoformat(),
                    "duration": d.duration_iso8601,
                    "status": d.status,
                    "citation": {
                        "instrument_id": d.citation_instrument,
                        "paragraph_ref": d.citation_paragraph,
                    },
                    "recipient": d.recipient,
                }
                for d in self.deadlines
            ],
            "time_critical": [
                {
                    "obligation_id": t.obligation_id,
                    "regulator": t.regulator,
                    "action": t.obligation_action,
                    "anchor": t.anchor_type,
                    "citation": {
                        "instrument_id": t.citation_instrument,
                        "paragraph_ref": t.citation_paragraph,
                    },
                    "recipient": t.recipient,
                }
                for t in self.time_critical
            ],
            "unknowns": [
                {"question": u.question, "affects": u.affects, "impact": u.impact}
                for u in self.unknowns
            ],
            "applicable_obligations": self.applicable_obligations,
            "not_applicable": self.not_applicable,
            "undetermined": self.undetermined,
            "conditions_unevaluated": self.conditions_unevaluated,
            "caveats": self.caveats,
            "annexure_i": {
                "decision": self.annexure_i.decision,
                "basis": self.annexure_i.basis,
                "matched": self.annexure_i.matched,
                "suggestions": self.annexure_i.suggestions,
            },
        }


_DURATION_RE = re.compile(
    r"^P(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?(?:(?P<days>\d+)D)?"
    r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$"
)


def parse_iso8601_duration(duration_str: str, allow_calendar: bool = True) -> timedelta:
    """Parse an ISO 8601 duration. Years and months are approximated (365 / 30 days) and are
    refused when allow_calendar is False, which the deadline path uses."""
    if not duration_str:
        return timedelta()
    match = _DURATION_RE.match(duration_str)
    if not match or duration_str in ("P", "PT"):
        raise ValueError(f"Invalid ISO 8601 duration: {duration_str}")

    parts = {k: int(v) for k, v in match.groupdict().items() if v}
    if not allow_calendar and ("years" in parts or "months" in parts):
        raise ValueError(f"Calendar-based duration not allowed for a deadline: {duration_str}")

    days = parts.get("days", 0) + parts.get("years", 0) * 365 + parts.get("months", 0) * 30
    return timedelta(
        days=days,
        hours=parts.get("hours", 0),
        minutes=parts.get("minutes", 0),
        seconds=parts.get("seconds", 0),
    )


class IncidentClockEngine:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.taxonomy = EntityTaxonomy(self.data_dir / "entities")
        self.obligations: list[dict[str, Any]] = []
        self._issuer: dict[str, str] = {}
        self._annexure_items: list[dict[str, Any]] = []
        self._strong: list[tuple[str, re.Pattern[str]]] = []
        self._weak: list[tuple[str, re.Pattern[str]]] = []
        self._load_obligations()
        self._load_instruments()
        self._load_annexure_i()

    def _load_obligations(self) -> None:
        obligations_dir = self.data_dir / "obligations"
        if not obligations_dir.is_dir():
            raise FileNotFoundError(
                f"Obligations directory not found: {obligations_dir}. Refusing to run with an "
                "empty law: that would silently report that nothing applies."
            )
        for filepath in sorted(obligations_dir.glob("*.json")):
            data = json.loads(filepath.read_text(encoding="utf-8"))
            for item in data if isinstance(data, list) else [data]:
                Obligation.model_validate(item)  # fail loudly on malformed records
                self.obligations.append(item)
        if not self.obligations:
            raise ValueError(f"No obligations found in {obligations_dir}")

    def _load_instruments(self) -> None:
        instruments_dir = self.data_dir / "instruments"
        if not instruments_dir.is_dir():
            return
        for filepath in sorted(instruments_dir.glob("*.json")):
            data = json.loads(filepath.read_text(encoding="utf-8"))
            for item in data if isinstance(data, list) else [data]:
                if "id" in item and "issuer" in item:
                    self._issuer[item["id"]] = item["issuer"]

    def _load_annexure_i(self) -> None:
        path = self.data_dir / "reference" / "annexure_i.json"
        if not path.exists():
            return
        data = json.loads(path.read_text(encoding="utf-8"))
        self._annexure_items = data["items"]
        for item in self._annexure_items:
            for term in item.get("strong_terms", []):
                self._strong.append((item["id"], re.compile(term, re.IGNORECASE)))
            for term in item.get("weak_terms", []):
                self._weak.append((item["id"], re.compile(term, re.IGNORECASE)))

    def get_obligation(self, obligation_id: str) -> dict[str, Any] | None:
        return next((o for o in self.obligations if o.get("id") == obligation_id), None)

    def annexure_items(self) -> list[dict[str, Any]]:
        return list(self._annexure_items)

    def _matches_entity_class(self, profile_class: str, target_classes: list[str]) -> bool:
        if not target_classes:
            return True
        return self.taxonomy.matches(profile_class, target_classes)

    def resolve_annexure_i(self, profile: IncidentProfile) -> AnnexureResolution:
        """Decide whether the incident is an Annexure I type. Never returns False from text."""
        valid_ids = {i["id"] for i in self._annexure_items}
        titles = {_norm(i["title"]): i["id"] for i in self._annexure_items}

        matched: list[str] = []
        for sel in profile.annexure_i_items:
            if sel not in valid_ids:
                raise ValueError(f"Unknown Annexure I item: {sel}")
            if sel not in matched:
                matched.append(sel)

        if profile.is_annexure_i_type is not None:
            return AnnexureResolution(
                profile.is_annexure_i_type,
                "user_attested",
                matched,
                [],
            )

        basis = "structured" if matched else "unresolved"

        suggestions: list[str] = []
        for text in profile.incident_types:
            text_n = _norm(text)
            if text_n in titles and titles[text_n] not in matched:
                matched.append(titles[text_n])
                basis = "structured"
                continue
            for item_id, pattern in self._strong:
                if pattern.search(text_n) and item_id not in matched:
                    matched.append(item_id)
                    if basis == "unresolved":
                        basis = "term_match"
            for item_id, pattern in self._weak:
                if pattern.search(text_n) and item_id not in suggestions:
                    suggestions.append(item_id)

        suggestions = [s for s in suggestions if s not in matched]
        if matched:
            return AnnexureResolution(True, basis, matched, suggestions)
        return AnnexureResolution(None, "unresolved", [], suggestions)

    def annexure_title(self, item_id: str) -> str:
        for item in self._annexure_items:
            if item["id"] == item_id:
                return f"{item_id.split('.')[-1]}. {item['title']}"
        return item_id

    def evaluate(
        self,
        profile: IncidentProfile,
        now: datetime | None = None,
        as_of: date | None = None,
    ) -> ClockResult:
        profile.validate()
        if now is None:
            now = datetime.now(UTC)
        if now.tzinfo is None:
            raise ValueError("now must be timezone-aware")

        if as_of is None:
            earliest = profile.earliest_known_time()
            as_of = (earliest or now).astimezone(IST).date()

        if profile.entity_class not in self.taxonomy:
            raise ValueError(
                f"Unknown entity class '{profile.entity_class}'. Refusing to guess: an "
                f"unrecognised class would silently report that nothing applies. "
                f"Known classes: {', '.join(sorted(self.taxonomy.classes.keys()))}"
            )

        caveats: list[str] = []
        if as_of < _MSME_EFFECTIVE:
            caveats.append(
                "Before 25 Sep 2022 CERT-In's notice of 27 Jun 2022 delayed the Directions for "
                "MSMEs and Direction (v)(a),(f). MSME status and sub-clause dates are not modelled."
            )

        annexure = self.resolve_annexure_i(profile)

        deadlines: list[DeadlineResult] = []
        time_critical: list[TimeCriticalResult] = []
        unknowns: list[Unknown] = []
        applicable: list[str] = []
        not_applicable: list[dict[str, Any]] = []
        undetermined: list[str] = []
        conditions_unevaluated: dict[str, list[str]] = {}

        for obs in self.obligations:
            obs_id = obs["id"]

            reason = self._not_in_force_reason(obs, as_of)
            if reason:
                not_applicable.append({"obligation_id": obs_id, "reason": reason})
                continue

            applicability = obs.get("applicability") or {}
            if not self._matches_entity_class(
                profile.entity_class, applicability.get("entity_classes") or []
            ):
                not_applicable.append({"obligation_id": obs_id, "reason": "entity_class_mismatch"})
                continue

            needs_annexure = False
            needs_personal_data = False
            other_conditions: list[str] = []
            for cond in applicability.get("conditions") or []:
                if re.search(r"\bannexure i\b", cond, re.IGNORECASE):
                    needs_annexure = True
                elif re.search(r"\bpersonal data\b", cond, re.IGNORECASE):
                    needs_personal_data = True
                else:
                    other_conditions.append(cond)

            if needs_annexure:
                if annexure.decision is False:
                    not_applicable.append(
                        {
                            "obligation_id": obs_id,
                            "reason": "condition_not_met: user attested not an Annexure I type",
                        }
                    )
                    continue
                if annexure.decision is None:
                    hint = ""
                    if annexure.suggestions:
                        listed = "; ".join(self.annexure_title(s) for s in annexure.suggestions)
                        hint = f" Possible matches to confirm: {listed}."
                    unknowns.append(
                        Unknown(
                            question="Is this incident of a type listed in CERT-In Annexure I?",
                            affects=[obs_id],
                            impact="This decides whether the 6-hour reporting obligation applies."
                            + hint,
                        )
                    )
                    undetermined.append(obs_id)
                    continue

            if needs_personal_data:
                if profile.personal_data_involved is False:
                    not_applicable.append(
                        {
                            "obligation_id": obs_id,
                            "reason": "condition_not_met: no personal data involved",
                        }
                    )
                    continue
                if profile.personal_data_involved is None:
                    unknowns.append(
                        Unknown(
                            question="Is personal data involved in this incident?",
                            affects=[obs_id],
                            impact="DPDP personal data breach notification obligations apply only if personal data is involved.",
                        )
                    )
                    undetermined.append(obs_id)
                    continue

            applicable.append(obs_id)
            if other_conditions:
                conditions_unevaluated[obs_id] = other_conditions

            self._compute_deadline(obs, profile, now, deadlines, time_critical, unknowns)

        return ClockResult(
            incident_profile=profile,
            deadlines=deadlines,
            time_critical=time_critical,
            unknowns=unknowns,
            applicable_obligations=applicable,
            not_applicable=not_applicable,
            undetermined=undetermined,
            conditions_unevaluated=conditions_unevaluated,
            caveats=caveats,
            annexure_i=annexure,
            computed_at=now,
            law_as_of=as_of,
        )

    @staticmethod
    def _not_in_force_reason(obs: dict[str, Any], as_of: date) -> str | None:
        validity = obs.get("validity") or {}
        valid_from = validity.get("valid_from")
        valid_to = validity.get("valid_to")
        status = obs.get("status")

        if valid_from and as_of < date.fromisoformat(valid_from):
            return f"not_yet_valid_at_incident_date ({valid_from})"
        if valid_to and as_of > date.fromisoformat(valid_to):
            return f"no_longer_valid_at_incident_date ({valid_to})"
        if status == "not_yet_in_force" and not valid_from:
            return "not_yet_in_force"
        if status in ("repealed", "superseded") and not valid_to:
            return f"status_{status}_without_valid_to"
        return None

    def _compute_deadline(
        self,
        obs: dict[str, Any],
        profile: IncidentProfile,
        now: datetime,
        deadlines: list[DeadlineResult],
        time_critical: list[TimeCriticalResult],
        unknowns: list[Unknown],
    ) -> None:
        obs_id = obs["id"]
        norm = obs.get("normalized") or {}
        spec = norm.get("deadline") or {}
        kind = spec.get("kind")

        if kind in (None, "none", "recurring", "retention"):
            return  # ongoing duties never produce an incident deadline
        if kind == "immediate":
            citation = (obs.get("citations") or [{}])[0]
            instrument_id = obs.get("instrument_id", "")
            time_critical.append(
                TimeCriticalResult(
                    obligation_id=obs_id,
                    regulator=self._issuer.get(instrument_id, instrument_id.split(".")[0].upper()),
                    obligation_action=norm.get("action", ""),
                    anchor_type=spec.get("anchor"),
                    citation_paragraph=citation.get("paragraph_ref", ""),
                    citation_instrument=citation.get("instrument_id", ""),
                    recipient=norm.get("recipient"),
                )
            )
            return
        if kind != "relative":
            unknowns.append(
                Unknown(
                    question=f"The engine cannot yet compute '{kind}' deadlines.",
                    affects=[obs_id],
                    impact="Read the cited clause directly; no deadline was computed.",
                )
            )
            return

        duration_str = spec.get("duration_iso8601")
        if not duration_str:
            unknowns.append(
                Unknown(
                    question="This relative deadline is missing duration_iso8601 in the dataset.",
                    affects=[obs_id],
                    impact="Data error: no deadline was computed; fix the obligation record.",
                )
            )
            return

        anchors = [spec.get("anchor"), *(spec.get("alternative_anchors") or [])]
        known: list[tuple[datetime, str]] = []
        for anchor in anchors:
            if anchor not in _ANCHOR_FIELDS:
                unknowns.append(
                    Unknown(
                        question=f"The engine cannot compute clocks from anchor '{anchor}'.",
                        affects=[obs_id],
                        impact="No deadline was computed; read the cited clause directly.",
                    )
                )
                return
            value = getattr(profile, _ANCHOR_FIELDS[anchor])
            if value is not None:
                known.append((value, anchor))

        if not known:
            if anchors == ["awareness"]:
                q = "When did the entity become aware of the personal data breach?"
            elif len(anchors) == 1:
                lbl = _ANCHOR_LABELS.get(anchors[0], anchors[0])
                q = f"When was the incident {lbl}?"
            elif len(anchors) == 2:
                lbls = [_ANCHOR_LABELS.get(a, a) for a in anchors]
                q = f"When was the incident {lbls[0]} or {lbls[1]}?"
            else:
                lbls = [_ANCHOR_LABELS.get(a, a) for a in anchors]
                q = f"When was the incident {', '.join(lbls[:-1])}, or {lbls[-1]}?"
            unknowns.append(
                Unknown(
                    question=q,
                    affects=[obs_id],
                    impact="The clock cannot start until this is known.",
                )
            )
            return

        anchor_ts, anchor_type = min(known, key=lambda k: k[0])
        duration = parse_iso8601_duration(duration_str, allow_calendar=False)
        deadline_utc = anchor_ts.astimezone(UTC) + duration
        citation = (obs.get("citations") or [{}])[0]
        instrument_id = obs.get("instrument_id", "")

        deadlines.append(
            DeadlineResult(
                obligation_id=obs["id"],
                regulator=self._issuer.get(instrument_id, instrument_id.split(".")[0].upper()),
                obligation_action=norm.get("action", ""),
                anchor_type=anchor_type,
                anchor_timestamp=anchor_ts,
                deadline_utc=deadline_utc,
                deadline_ist=deadline_utc.astimezone(IST),
                duration_iso8601=duration_str,
                status="pending" if deadline_utc > now else "overdue",
                citation_paragraph=citation.get("paragraph_ref", ""),
                citation_instrument=citation.get("instrument_id", ""),
                recipient=norm.get("recipient", ""),
                channel=None,
            )
        )
