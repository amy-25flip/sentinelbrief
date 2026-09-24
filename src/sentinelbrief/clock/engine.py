import json
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

# IST is UTC+5:30, always. India does not observe DST.
IST = timezone(timedelta(hours=5, minutes=30))

# Entity taxonomy and implied parent classes
ENTITY_HIERARCHY: dict[str, set[str]] = {
    "virtual_asset_exchange": {
        "virtual_asset_exchange",
        "service_provider",
        "body_corporate",
        "intermediary",
    },
    "virtual_asset_service_provider": {
        "virtual_asset_service_provider",
        "service_provider",
        "body_corporate",
        "intermediary",
    },
    "custodian_wallet_provider": {
        "custodian_wallet_provider",
        "service_provider",
        "body_corporate",
        "intermediary",
    },
    "vps_provider": {"vps_provider", "service_provider", "body_corporate"},
    "cloud_provider": {"cloud_provider", "service_provider", "body_corporate"},
    "vpn_provider": {"vpn_provider", "service_provider", "body_corporate"},
    "data_centre": {"data_centre", "service_provider", "body_corporate"},
    "bank": {"bank", "body_corporate"},
    "nbfc": {"nbfc", "body_corporate"},
    "nbfc.base_layer": {"nbfc.base_layer", "nbfc", "body_corporate"},
    "nbfc.middle_layer": {"nbfc.middle_layer", "nbfc", "body_corporate"},
    "government_org": {"government_org"},
    "service_provider": {"service_provider", "body_corporate"},
    "intermediary": {"intermediary", "body_corporate"},
    "body_corporate": {"body_corporate"},
}

# Annexure I keywords matching CERT-In 20 incident categories
ANNEXURE_I_KEYWORDS = {
    "ransomware",
    "malicious code",
    "malware",
    "virus",
    "worm",
    "trojan",
    "bots",
    "spyware",
    "cryptominer",
    "unauthorised access",
    "unauthorized access",
    "data breach",
    "data leak",
    "ddos",
    "dos",
    "denial of service",
    "phishing",
    "spoofing",
    "identity theft",
    "defacement",
    "scanning",
    "probing",
    "intrusion",
    "critical systems",
    "scada",
    "iot",
    "payment systems",
    "fake mobile apps",
    "cloud",
    "artificial intelligence",
    "virtual asset",
}


@dataclass(frozen=True)
class ClockAnchor:
    """A timestamp for a specific anchor type."""

    anchor_type: str  # 'detection', 'noticing', 'brought_to_notice', 'awareness', 'occurrence'
    timestamp: datetime  # Must be timezone-aware
    set_by: str  # Who set this timestamp
    set_at: datetime  # When it was set


@dataclass(frozen=True)
class DeadlineResult:
    """A computed deadline for one obligation."""

    obligation_id: str
    regulator: str
    obligation_action: str
    anchor_type: str
    anchor_timestamp: datetime  # The anchor used
    deadline_utc: datetime
    deadline_ist: datetime
    duration_iso8601: str
    status: str  # 'pending', 'overdue', 'filed_by_human'
    citation_paragraph: str
    citation_instrument: str
    recipient: str
    channel: str | None


@dataclass(frozen=True)
class Unknown:
    """A fact the system needs but doesn't have."""

    question: str
    affects: list[str]  # Which obligation IDs are affected
    impact: str  # What happens if we don't know this


@dataclass
class IncidentProfile:
    """User-provided entity and incident facts."""

    # Entity facts
    entity_class: str  # e.g. 'nbfc.base_layer', 'service_provider'
    is_listed: bool | None = None
    holds_personal_data: bool | None = None
    uses_protected_systems: bool | None = None
    is_regulated_cloud_vps: bool | None = None
    is_virtual_asset_provider: bool | None = None

    # Incident facts
    incident_description: str = ""
    incident_types: list[str] = field(default_factory=list)  # Annexure I types
    when_detected: datetime | None = None
    when_noticed: datetime | None = None
    when_brought_to_notice: datetime | None = None
    when_occurred: datetime | None = None
    personal_data_involved: bool | None = None
    systems_affected: list[str] = field(default_factory=list)
    is_annexure_i_type: bool | None = None  # Whether it's a CERT-In Annexure I incident type


@dataclass
class ClockResult:
    """Full result of running the clock engine."""

    incident_profile: IncidentProfile
    deadlines: list[DeadlineResult]
    unknowns: list[Unknown]
    applicable_obligations: list[str]  # obligation IDs
    not_applicable: list[dict[str, Any]]  # {obligation_id, reason}
    computed_at: datetime
    law_snapshot_date: str  # date of the law snapshot used


def parse_iso8601_duration(duration_str: str) -> timedelta:
    if not duration_str:
        return timedelta()
    pattern = re.compile(
        r"^P(?:(?P<years>\d+)Y)?(?:(?P<months>\d+)M)?(?:(?P<days>\d+)D)?"
        r"(?:T(?:(?P<hours>\d+)H)?(?:(?P<minutes>\d+)M)?(?:(?P<seconds>\d+)S)?)?$"
    )
    match = pattern.match(duration_str)
    if not match:
        raise ValueError(f"Invalid ISO 8601 duration: {duration_str}")

    parts = {k: int(v) for k, v in match.groupdict().items() if v}

    # Deterministic calculation for days/years/months
    days = parts.get("days", 0)
    days += parts.get("years", 0) * 365
    days += parts.get("months", 0) * 30

    return timedelta(
        days=days,
        hours=parts.get("hours", 0),
        minutes=parts.get("minutes", 0),
        seconds=parts.get("seconds", 0),
    )


class IncidentClockEngine:
    def __init__(self, data_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.obligations: list[dict[str, Any]] = []
        self._load_obligations()

    def _load_obligations(self) -> None:
        obligations_dir = self.data_dir / "obligations"
        if not obligations_dir.exists():
            return

        for filepath in obligations_dir.glob("*.json"):
            with open(filepath, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.obligations.extend(data)
                elif isinstance(data, dict):
                    self.obligations.append(data)

    def _matches_entity_class(self, profile_class: str, target_classes: list[str]) -> bool:
        if not target_classes:
            return True
        implied = ENTITY_HIERARCHY.get(profile_class, {profile_class})
        return bool(implied & set(target_classes))

    def _resolve_annexure_i(self, profile: IncidentProfile) -> bool | None:
        if profile.is_annexure_i_type is not None:
            return profile.is_annexure_i_type
        if not profile.incident_types:
            return None

        # Check against keywords
        for itype in profile.incident_types:
            itype_lower = itype.lower()
            for kw in ANNEXURE_I_KEYWORDS:
                if kw in itype_lower:
                    return True
        # If types were provided but none matched Annexure I keywords (e.g. "hardware failure")
        return False

    def evaluate(self, profile: IncidentProfile, now: datetime | None = None) -> ClockResult:
        if now is None:
            now = datetime.now(UTC)

        deadlines: list[DeadlineResult] = []
        unknowns: list[Unknown] = []
        applicable_obligations: list[str] = []
        not_applicable: list[dict[str, Any]] = []

        is_annexure_i = self._resolve_annexure_i(profile)

        for obs in self.obligations:
            obs_id = obs["id"]

            # Status check
            if obs.get("status") == "not_yet_in_force":
                not_applicable.append({"obligation_id": obs_id, "reason": "not_yet_in_force"})
                continue

            # Check applicability based on entity_class
            applicability = obs.get("applicability", {})
            entity_classes = applicability.get("entity_classes", [])

            if not self._matches_entity_class(profile.entity_class, entity_classes):
                not_applicable.append({"obligation_id": obs_id, "reason": "entity_class_mismatch"})
                continue

            # Check conditions
            conditions = applicability.get("conditions", [])
            condition_met = True
            is_annexure_condition = False
            for cond in conditions:
                if "Annexure I" in cond:
                    is_annexure_condition = True
                    if is_annexure_i is False:
                        condition_met = False
                        not_applicable.append(
                            {"obligation_id": obs_id, "reason": "condition_not_met: not annexure I"}
                        )

            if not condition_met:
                continue

            if is_annexure_condition and is_annexure_i is None:
                unknowns.append(
                    Unknown(
                        question="Is this incident of a type listed in CERT-In Annexure I?",
                        affects=[obs_id],
                        impact="This determines whether the 6-hour reporting obligation applies",
                    )
                )
                continue

            # If we reach here, it's applicable
            applicable_obligations.append(obs_id)

            norm = obs.get("normalized", {})
            deadline_spec = norm.get("deadline", {})

            if deadline_spec.get("kind") == "none" or not deadline_spec.get("duration_iso8601"):
                continue

            anchor_type = deadline_spec.get("anchor")
            anchor_timestamp = None
            resolved_anchor_type = anchor_type

            if anchor_type == "noticing":
                # CERT-In specific rule: noticing or brought_to_notice, whichever is earlier
                if (
                    "cert-in" in obs_id.lower()
                    or "brought to notice" in obs.get("text_verbatim", "").lower()
                ):
                    if profile.when_noticed and profile.when_brought_to_notice:
                        if profile.when_noticed <= profile.when_brought_to_notice:
                            anchor_timestamp = profile.when_noticed
                            resolved_anchor_type = "noticing"
                        else:
                            anchor_timestamp = profile.when_brought_to_notice
                            resolved_anchor_type = "brought_to_notice"
                    elif profile.when_noticed:
                        anchor_timestamp = profile.when_noticed
                        resolved_anchor_type = "noticing"
                    elif profile.when_brought_to_notice:
                        anchor_timestamp = profile.when_brought_to_notice
                        resolved_anchor_type = "brought_to_notice"
                    else:
                        unknowns.append(
                            Unknown(
                                question="When was the incident first noticed or brought to notice?",
                                affects=[obs_id],
                                impact="CERT-In clock starts from noticing or being brought to notice",
                            )
                        )
                else:
                    anchor_timestamp = profile.when_noticed
                    if not anchor_timestamp:
                        unknowns.append(
                            Unknown(
                                question="When was the incident first noticed?",
                                affects=[obs_id],
                                impact="Clock starts from noticing",
                            )
                        )
            elif anchor_type == "occurrence":
                anchor_timestamp = profile.when_occurred
                if not anchor_timestamp:
                    unknowns.append(
                        Unknown(
                            question="When did the incident occur?",
                            affects=[obs_id],
                            impact="Clock starts from occurrence",
                        )
                    )
            elif anchor_type == "detection":
                anchor_timestamp = profile.when_detected
                if not anchor_timestamp:
                    unknowns.append(
                        Unknown(
                            question="When was the incident detected?",
                            affects=[obs_id],
                            impact="Clock starts from detection",
                        )
                    )

            if anchor_timestamp:
                duration_str = deadline_spec.get("duration_iso8601")
                duration = parse_iso8601_duration(duration_str)

                # Compute deadline
                deadline_utc = anchor_timestamp.astimezone(UTC) + duration
                deadline_ist = deadline_utc.astimezone(IST)

                citation = obs.get("citations", [{}])[0]

                deadlines.append(
                    DeadlineResult(
                        obligation_id=obs_id,
                        regulator=obs.get("instrument_id", "").split(".")[0].upper(),
                        obligation_action=norm.get("action", ""),
                        anchor_type=resolved_anchor_type or "noticing",
                        anchor_timestamp=anchor_timestamp,
                        deadline_utc=deadline_utc,
                        deadline_ist=deadline_ist,
                        duration_iso8601=duration_str,
                        status="pending" if deadline_utc > now else "overdue",
                        citation_paragraph=citation.get("paragraph_ref", ""),
                        citation_instrument=citation.get("instrument_id", ""),
                        recipient=norm.get("recipient", ""),
                        channel=None,
                    )
                )

        return ClockResult(
            incident_profile=profile,
            deadlines=deadlines,
            unknowns=unknowns,
            applicable_obligations=applicable_obligations,
            not_applicable=not_applicable,
            computed_at=now,
            law_snapshot_date=now.strftime("%Y-%m-%d"),
        )
