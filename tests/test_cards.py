"""Tests for the deterministic card feed generator and feed manager (WP2)."""

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from sentinelbrief.cards.feed import CardFeed
from sentinelbrief.cards.generator import CardGenerator, verify_grounded_body
from sentinelbrief.cards.models import Card
from sentinelbrief.models import Citation
from sentinelbrief.verify.citation_validator import SourceTextStore, validate_citation

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


@pytest.fixture
def obligations_and_instruments() -> tuple[list[dict], dict[str, dict]]:
    obligations_dir = DATA_DIR / "obligations"
    instruments_dir = DATA_DIR / "instruments"

    instruments = {}
    for p in instruments_dir.glob("*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        for item in items:
            instruments[item["id"]] = item

    obligations = []
    for p in obligations_dir.glob("*.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        obligations.extend(items)

    return obligations, instruments


def test_every_obligation_generates_valid_card(obligations_and_instruments):
    obligations, instruments = obligations_and_instruments
    generator = CardGenerator()

    for obl in obligations:
        inst = instruments.get(obl.get("instrument_id", ""))
        card = generator.generate_regulatory_card(obl, instrument=inst)
        assert isinstance(card, Card)
        assert card.stream == "regulatory"
        assert card.obligation_id == obl["id"]
        assert card.disclaimer == "AI-assisted summary, not legal advice. See the source."


def test_card_headline_and_body_length_bounds(obligations_and_instruments):
    """Headline <= 12 words; body 45 to 75 words, shorter only when a short clause is quoted whole."""
    obligations, instruments = obligations_and_instruments
    generator = CardGenerator()

    for obl in obligations:
        inst = instruments.get(obl.get("instrument_id", ""))
        card = generator.generate_regulatory_card(obl, instrument=inst)

        headline_words = card.headline.split()
        body_words = card.body.split()

        assert len(headline_words) <= 12, (
            f"Headline exceeds 12 words for {obl['id']}: {len(headline_words)} words ('{card.headline}')"
        )
        assert len(body_words) <= 75, f"Body exceeds 75 words for {obl['id']}: {len(body_words)}"
        clause = " ".join(obl["text_verbatim"].split())
        if len(body_words) < 45:
            # A body may be shorter than 45 words only when the clause itself is short and is
            # quoted whole: padding it with text the source does not contain is not allowed.
            assert len(clause.split()) < 50 and clause in card.body, (
                f"Short body for {obl['id']} does not quote its short clause in full"
            )
        assert "must be maintained as prescribed" not in card.body


def test_no_retention_or_ongoing_duty_shows_deadline_chip(obligations_and_instruments):
    """Deadline chip must only appear when obligation has an incident deadline, never for retention/ongoing."""
    obligations, instruments = obligations_and_instruments
    generator = CardGenerator()

    for obl in obligations:
        inst = instruments.get(obl.get("instrument_id", ""))
        card = generator.generate_regulatory_card(obl, instrument=inst)

        norm = obl.get("normalized", {})
        deadline = norm.get("deadline", {})
        kind = deadline.get("kind")

        deadline_chips = [c for c in card.chips if c.chip_type == "deadline"]

        if kind == "relative" and deadline.get("duration_iso8601"):
            assert len(deadline_chips) == 1, (
                f"Expected deadline chip for relative deadline in {obl['id']}"
            )
            assert deadline_chips[0].value == deadline["duration_iso8601"]
        else:
            assert len(deadline_chips) == 0, (
                f"Retention or ongoing duty {obl['id']} must NOT have a deadline chip, but had {deadline_chips}"
            )


def test_card_citations_pass_citation_validator(obligations_and_instruments):
    """Every regulatory card citation must pass the CitationValidator."""
    obligations, instruments = obligations_and_instruments
    generator = CardGenerator()
    source_store = SourceTextStore(DATA_DIR / "raw")

    for obl in obligations:
        inst = instruments.get(obl.get("instrument_id", ""))
        card = generator.generate_regulatory_card(obl, instrument=inst)

        assert card.citation_text is not None
        citations = obl.get("citations", [])
        assert len(citations) > 0

        first_cit = citations[0]
        cit_obj = Citation(**first_cit)
        source_text = source_store.get_text(obl["instrument_id"])
        assert source_text is not None
        res = validate_citation(
            cit_obj, source_text, expected_sha256=inst.get("source_sha256") if inst else None
        )
        assert res.valid, f"Citation for card {card.id} failed validation: {res.errors}"


def test_vulnerability_card_never_presents_due_date_as_indian_deadline():
    """CISA KEV dueDate is a US federal remediation deadline, never an Indian deadline."""
    kev_path = FIXTURES_DIR / "kev_sample.json"
    assert kev_path.exists(), "Recorded KEV sample fixture must exist"

    kev_data = json.loads(kev_path.read_text(encoding="utf-8"))
    generator = CardGenerator()

    for item in kev_data.get("vulnerabilities", []):
        card = generator.generate_vulnerability_card(
            item, epss_score=0.75, cvss_score=9.8, published_at=datetime.now(UTC)
        )

        assert card.stream == "vulnerability"
        assert card.cve_id == item["cveID"]
        assert card.kev is True
        assert card.cvss == 9.8
        assert card.epss == 0.75
        assert card.priority >= 2.0  # KEV raises priority

        # Check chips
        for chip in card.chips:
            # Chip type 'deadline' is reserved for Indian regulatory deadlines
            assert chip.chip_type != "deadline", (
                f"KEV dueDate must not be a 'deadline' chip type: {chip}"
            )
            if chip.label == "US Federal Remediation Date":
                assert chip.chip_type == "us_federal_deadline"
                assert chip.value == item["dueDate"]


def test_regulatory_card_grounding_rejects_invented_hard_fact(obligations_and_instruments):
    obligations, _ = obligations_and_instruments
    obligation = next(o for o in obligations if o["id"].endswith("incident-reporting-6h"))
    with pytest.raises(ValueError, match="ungrounded fact"):
        verify_grounded_body(
            "Report to CERT-In within 72 hours by emailing made-up@example.test.",
            obligation,
        )


def test_regulatory_card_grounding_rejects_fact_only_in_evidence_required(
    obligations_and_instruments,
):
    obligations, _ = obligations_and_instruments
    obligation = next(o for o in obligations if o["id"].endswith("ntp-sync"))
    poisoned = {
        **obligation,
        "normalized": {
            **obligation["normalized"],
            "evidence_required": ["Retain NTP configuration records for 72 hours"],
        },
    }
    with pytest.raises(ValueError, match="72"):
        verify_grounded_body(
            "Retain NTP configuration records for 72 hours.",
            poisoned,
        )


def test_every_regulatory_card_body_passes_grounding(obligations_and_instruments):
    obligations, instruments = obligations_and_instruments
    generator = CardGenerator()
    for obl in obligations:
        inst = instruments.get(obl.get("instrument_id", ""))
        card = generator.generate_regulatory_card(obl, instrument=inst)
        verify_grounded_body(card.body, obl)


def test_vulnerability_source_url_is_single_http_url_and_body_truncates_on_word_boundary():
    generator = CardGenerator()
    card = generator.generate_vulnerability_card(
        {
            "cveID": "CVE-2026-12345",
            "vendorProject": "Vendor",
            "product": "Product",
            "shortDescription": " ".join(["word"] * 200),
            "requiredAction": "Apply fixes",
            "knownRansomwareCampaignUse": "Unknown",
            "notes": "https://first.example/a; https://second.example/b",
        },
        published_at=datetime.now(UTC),
    )
    assert card.source_url == "https://www.cve.org/CVERecord?id=CVE-2026-12345"
    assert len(card.body) <= 500
    assert card.body.endswith("...")
    assert not card.body[:-3].endswith("wo")


def test_card_feed_loading_and_sorting(obligations_and_instruments):
    feed = CardFeed(DATA_DIR)
    feed.load_from_data_dir(fixtures_dir=FIXTURES_DIR)
    cards = feed.get_feed()

    assert len(cards) > 0
    # Feed should contain both regulatory and vulnerability cards
    streams = {c.stream for c in cards}
    assert "regulatory" in streams
    assert "vulnerability" in streams

    # Sorted by priority descending
    for i in range(len(cards) - 1):
        assert cards[i].priority >= cards[i + 1].priority or (
            cards[i].priority == cards[i + 1].priority
            and cards[i].published_at >= cards[i + 1].published_at
        )


def test_disclaimer_present_on_all_cards(obligations_and_instruments):
    feed = CardFeed(DATA_DIR)
    feed.load_from_data_dir(fixtures_dir=FIXTURES_DIR)
    for card in feed.get_feed():
        assert "AI-assisted summary, not legal advice" in card.disclaimer
