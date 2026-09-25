"""Card data models for SentinelBrief feed."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CardChip(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    value: str
    chip_type: Literal[
        "issuer",
        "jurisdiction",
        "severity",
        "deadline",
        "effective_date",
        "cve_id",
        "kev",
        "epss",
        "product",
        "mandatory",
        "advisory",
        "ransomware",
        "us_federal_deadline",
    ]


class Card(BaseModel):
    """A single card in the feed.

    Requirements:
    - headline: at most 12 words
    - body: between 45 and 75 words
    - disclaimer: 'AI-assisted summary, not legal advice. See the source.'
    """

    model_config = ConfigDict(frozen=True)

    id: str
    stream: Literal["regulatory", "vulnerability"]
    headline: str = Field(max_length=150)
    body: str = Field(max_length=600)
    chips: list[CardChip]
    source_url: str | None = None
    source_title: str | None = None
    citation_text: str | None = None
    instrument_id: str | None = None
    paragraph_ref: str | None = None
    what_changed: str | None = None
    published_at: datetime
    relevance_reason: str | None = None
    disclaimer: str = "AI-assisted summary, not legal advice. See the source."
    priority: float = 0.0
    obligation_id: str | None = None
    cve_id: str | None = None
    cvss: float | None = None
    epss: float | None = None
    kev: bool | None = None
    known_ransomware_campaign_use: str | None = None
    us_federal_due_date: str | None = None
