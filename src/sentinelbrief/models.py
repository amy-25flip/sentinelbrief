"""Core Pydantic v2 models for SentinelBrief."""

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class Bbox(BaseModel):
    """Bounding box for a citation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    x0: float
    y0: float
    x1: float
    y1: float


class Citation(BaseModel):
    """Links a claim to a verbatim span of source text."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    instrument_id: str
    paragraph_ref: str | None = None
    page: int | None = Field(default=None, ge=1)
    char_start: int | None = Field(default=None, ge=0)
    char_end: int | None = Field(default=None, ge=0)
    bbox: Bbox | None = None
    excerpt_verbatim: str = Field(min_length=10)
    source_sha256: str = Field(pattern=r"^[a-f0-9]{64}$")


class Trigger(BaseModel):
    """Trigger condition for an obligation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    type: Literal["event", "periodic", "condition", "always"]
    description: str


class Deadline(BaseModel):
    """Deadline specification for an obligation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    kind: Literal["relative", "absolute", "recurring", "retention", "immediate", "none"]
    duration_iso8601: str | None = None
    alternative_anchors: (
        list[
            Literal[
                "detection",
                "noticing",
                "brought_to_notice",
                "awareness",
                "occurrence",
                "reported",
            ]
        ]
        | None
    ) = None
    anchor: (
        Literal[
            "detection",
            "noticing",
            "brought_to_notice",
            "awareness",
            "occurrence",
            "publication",
            "fixed_date",
            "not_applicable",
            "reported",
        ]
        | None
    ) = None
    calendar: Literal["continuous", "business_days"] = "continuous"
    fixed_date: date | None = None


class Normalized(BaseModel):
    """Normalized details of an obligation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    actor: list[str]
    trigger: Trigger
    action: str
    deadline: Deadline
    recipient: str | None = None
    # Source-stated only: every item must be quoted from text_verbatim (validator-enforced).
    evidence_required: list[str] | None = None
    # Author suggestions, not in the source text and not a legal requirement.
    suggested_evidence: list[str] | None = None


class Applicability(BaseModel):
    """Applicability rules for an obligation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    entity_classes: list[str] | None = None
    all_of_entity_classes: list[str] | None = None
    excluded_entity_classes: list[str] | None = None
    conditions: list[str] | None = None
    requires: (
        list[
            Literal[
                "cert_in_annexure_i",
                "personal_data_involved",
                "rbi_cyber_incident",
                "sebi_other_cybersecurity_incident",
                "sebi_cybersecurity_incident",
                "sebi_incident_reporting_applies",
                "nciipc_protected_system",
            ]
        ]
        | None
    ) = None


class Validity(BaseModel):
    """Validity period for a record."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    valid_from: date
    valid_to: date | None = None
    recorded_at: datetime


class Extraction(BaseModel):
    """Details about how the data was extracted."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    method: Literal["manual", "rule", "llm"]
    model: str | None = None
    prompt_version: str | None = None
    extractor_version: str


class VerificationDetails(BaseModel):
    """Verification details for an obligation."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    reviewer: str | None = None
    verified_date: date | None = Field(default=None, alias="date")


class Obligation(BaseModel):
    """One atomic regulatory requirement."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    id: str
    instrument_id: str
    paragraph_ref: str | None = None
    text_verbatim: str
    normalized: Normalized
    applicability: Applicability | None = None
    validity: Validity
    status: Literal["in_force", "repealed", "not_yet_in_force", "superseded"]
    citations: list[Citation] = Field(min_length=1)
    extraction: Extraction
    verification: Literal["unverified", "machine_checked", "human_verified"]
    verification_details: VerificationDetails | None = None
    confidence: float | None = Field(default=None, ge=0, le=1)
    confidence_reason: str | None = None


class Provenance(BaseModel):
    """Provenance for an instrument."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    parser_version: str | None = None
    extraction_date: datetime | None = None


class Instrument(BaseModel):
    """A legal document."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    id: str
    issuer: Literal["CERT-In", "RBI", "SEBI", "IRDAI", "MeitY", "NCIIPC", "IFSCA"]
    title: str
    reference_no: str | None = None
    issued_on: date | None = None
    in_force_from: date | None = None
    in_force_until: date | None = None
    url: str | None = None
    source_sha256: str | None = Field(default=None, pattern=r"^[a-f0-9]{64}$")
    retrieved_at: datetime | None = None
    language: str = "en"
    status: Literal["in_force", "repealed", "not_yet_in_force", "superseded", "draft"]
    supersedes: list[str] | None = None
    superseded_by: list[str] | None = None
    document_type: (
        Literal[
            "act", "rules", "direction", "circular", "guideline", "notification", "faq", "amendment"
        ]
        | None
    ) = None
    provenance: Provenance | None = None


class EntityClass(BaseModel):
    """Taxonomy for applicability."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    id: str
    regulator: str
    label: str
    parent: str | None = None
    description: str | None = None
    needs_refinement: bool = False
    is_role: bool = False
    version: str
    valid_from: date | None = None
    valid_to: date | None = None


class ClockTemplate(BaseModel):
    """When a filing is due."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    regulator: str
    obligation_id: str
    anchor: str
    duration: str
    calendar: Literal["continuous", "business_days"]
    recipient: str
    channel: str | None = None


class ChangeRecord(BaseModel):
    """Tracks changes between instrument versions."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    id: str
    old_version: str
    new_version: str
    kind: Literal["added", "removed", "modified", "moved", "renumbered"]
    diff: str | None = None
    impact_note: str | None = None
    citations: list[Citation] | None = None
    recorded_at: datetime | None = None


class EntityProfile(BaseModel):
    """Entity profile for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    entity_class: str | None = None
    entity_classes: list[str] | None = None
    is_listed: bool
    holds_personal_data: bool
    uses_protected_systems: bool | None = None
    is_regulated_cloud_vps: bool
    additional_properties: dict[str, Any] | None = None

    @model_validator(mode="after")
    def exactly_one_entity_class_shape(self) -> "EntityProfile":
        if (self.entity_class is None) == (self.entity_classes is None):
            raise ValueError("Supply exactly one of entity_class or entity_classes")
        if self.entity_classes is not None and not self.entity_classes:
            raise ValueError("entity_classes must contain at least one class")
        return self


class IncidentFacts(BaseModel):
    """Incident facts for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    description: str
    incident_types: list[str]
    when_detected: datetime | None = None
    when_noticed: datetime | None = None
    when_occurred: datetime | None = None
    when_brought_to_notice: datetime | None = None
    when_reported_to_sebi: datetime | None = None
    is_annexure_i_type: bool | None = None
    is_cyber_incident: bool | None = None
    annexure_i_items: list[str] | None = None
    personal_data_involved: bool | None = None
    systems_affected: list[str]
    additional_facts: dict[str, Any] | None = None


class ExpectedDeadline(BaseModel):
    """Expected deadline for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    regulator: str
    obligation_id: str
    anchor: str
    deadline_iso8601: str
    deadline_timestamp: datetime


class ExpectedCitation(BaseModel):
    """Expected citation for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    obligation_id: str
    instrument_id: str
    paragraph_ref: str


class NotApplicable(BaseModel):
    """Not applicable expected result for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    regulator: str
    obligation_id: str
    reason: str


class Unknown(BaseModel):
    """Unknown expected result for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    question: str
    affects: str


class Expected(BaseModel):
    """Expected results for a benchmark scenario."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    law_as_of: date | None = None
    regulators: list[str]
    deadlines: list[ExpectedDeadline]
    citations: list[ExpectedCitation]
    required_evidence: list[str]
    not_applicable: list[NotApplicable]
    unknowns: list[Unknown]
    time_critical: list[str] | None = None


class SourceQuote(BaseModel):
    """A benchmark label justified by exact text on a stored PDF page."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    document: str
    page: int = Field(ge=1)
    quote: str = Field(min_length=1)


class BenchmarkScenario(BaseModel):
    """With nested EntityProfile, IncidentFacts, ExpectedDeadline, etc."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    id: str
    description: str
    entity_profile: EntityProfile
    incident_facts: IncidentFacts
    law_snapshot_date: date
    expected: Expected
    adversarial_flags: list[str] | None = None
    split: Literal["dev", "hidden"]
    labels_source: str | None = None
    source_quotes: list[SourceQuote] | None = None


class ManifestEntry(BaseModel):
    """Raw file manifest entry."""

    model_config = ConfigDict(extra="ignore")

    url: str
    filename: str
    sha256: str = Field(pattern=r"^[a-f0-9]{64}$")
    retrieved_at: datetime
    acquired_at: datetime | None = None
    etag: str | None = None
    last_modified: str | None = None
    content_type: str | None = None
    size_bytes: int | None = None
    parser_version: str | None = None
    status: Literal["current", "superseded", "failed"] | None = None
    acquired_by: str | None = None
    fetched_by: str | None = None
    acquisition_note: str | None = None
    authenticity_exemption: str | None = None
    reverify_exemption: str | None = Field(default=None, min_length=1)

    @field_validator("reverify_exemption")
    @classmethod
    def reverify_exemption_must_have_text(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("reverify_exemption must be a non-empty reason")
        return value


class Manifest(BaseModel):
    """Container for manifest entries."""

    model_config = ConfigDict(extra="ignore")

    version: int | None = None
    entries: list[ManifestEntry] | None = None


class EvidenceEvent(BaseModel):
    """Tamper-evident timeline event."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    seq: int = Field(ge=0)
    ts_utc: datetime
    actor: str
    type: Literal[
        "incident_created",
        "fact_recorded",
        "clock_started",
        "draft_created",
        "draft_approved",
        "filing_recorded",
        "note_added",
        "attachment_added",
        "clock_expired",
        "unknown_resolved",
    ]
    payload: dict[str, Any]
    prev_hash: str
    hash: str
    clock_source: str | None = None
    ntp_synced: bool | None = None
