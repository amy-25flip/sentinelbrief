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
    ]


class Card(BaseModel):
    """A single card in the feed.

    headline: <= 12 words
    body: ~60 words
    Every regulatory card must show the disclaimer.
    """

    model_config = ConfigDict(frozen=True)

    id: str
    stream: Literal["regulatory", "vulnerability"]
    headline: str = Field(max_length=120)  # approx 12 words
    body: str = Field(max_length=500)  # approx 60 words
    chips: list[CardChip]
    source_url: str | None = None
    source_title: str | None = None
    citation_text: str | None = None  # verbatim citation
    what_changed: str | None = None
    published_at: datetime
    relevance_reason: str | None = None  # "shown because you are a NBFC middle-layer entity"
    disclaimer: str = "AI-assisted summary, not legal advice. See the source."
    priority: float = 0.0  # higher = more important
    obligation_id: str | None = None  # link to obligation
    cve_id: str | None = None
