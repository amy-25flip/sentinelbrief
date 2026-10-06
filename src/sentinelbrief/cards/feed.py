"""Feed management and ranking for SentinelBrief cards."""

import json
from email.utils import format_datetime
from pathlib import Path
from typing import Any, cast
from xml.etree import ElementTree

from sentinelbrief.cards.generator import CardGenerator
from sentinelbrief.cards.models import Card


class CardFeed:
    """Manages ranking, filtering, and export of compliance and vulnerability cards."""

    def __init__(self, data_dir: str | Path | None = None):
        self.data_dir = Path(data_dir) if data_dir else None
        self._cards: list[Card] = []
        self.generator = CardGenerator()

    def add_card(self, card: Card) -> None:
        self._cards.append(card)

    def add_cards(self, cards: list[Card]) -> None:
        self._cards.extend(cards)

    def load_from_data_dir(self, fixtures_dir: Path | None = None) -> None:
        """Load regulatory cards from data directory and vulnerability cards from fixture."""
        if not self.data_dir or not self.data_dir.exists():
            return

        instruments_dir = self.data_dir / "instruments"
        obligations_dir = self.data_dir / "obligations"

        instruments_map: dict[str, dict[str, Any]] = {}
        if instruments_dir.exists():
            for p in sorted(instruments_dir.glob("*.json")):
                inst = json.loads(p.read_text(encoding="utf-8"))
                if isinstance(inst, list):
                    for i in inst:
                        instruments_map[i["id"]] = i
                else:
                    instruments_map[inst["id"]] = inst

        if obligations_dir.exists():
            for p in sorted(obligations_dir.glob("*.json")):
                obls = json.loads(p.read_text(encoding="utf-8"))
                items = obls if isinstance(obls, list) else [obls]
                for obl in items:
                    inst = instruments_map.get(obl.get("instrument_id", ""))
                    card = self.generator.generate_regulatory_card(obl, instrument=inst)
                    self.add_card(card)

        # Load KEV recorded fixture if available
        if fixtures_dir and (fixtures_dir / "kev_sample.json").exists():
            kev_data = json.loads((fixtures_dir / "kev_sample.json").read_text(encoding="utf-8"))
            for v in kev_data.get("vulnerabilities", []):
                vuln_card = self.generator.generate_vulnerability_card(v)
                self.add_card(vuln_card)

    def get_feed(
        self,
        stream: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[Card]:
        """Get ranked cards, sorted by priority (descending) and published_at (descending)."""
        filtered = self._cards
        if stream:
            filtered = [c for c in filtered if c.stream == stream]

        sorted_cards = sorted(
            filtered,
            key=lambda c: (c.priority, c.published_at.timestamp()),
            reverse=True,
        )
        return sorted_cards[offset : offset + limit]

    def to_json(self) -> list[dict[str, Any]]:
        return [c.model_dump(mode="json") for c in self.get_feed()]


def regulatory_rss(cards: list[Card], base_url: str) -> bytes:
    """Return deterministic RSS 2.0 bytes for regulatory cards."""
    regulatory = [card for card in cards if card.stream == "regulatory"]
    root = ElementTree.Element("rss", {"version": "2.0"})
    channel = ElementTree.SubElement(root, "channel")
    ElementTree.SubElement(channel, "title").text = "SentinelBrief regulatory cards"
    ElementTree.SubElement(channel, "link").text = base_url.rstrip("/") + "/"
    ElementTree.SubElement(
        channel, "description"
    ).text = "Citation-first Indian cyber-regulatory obligation cards."
    if regulatory:
        newest = max(card.published_at for card in regulatory)
        ElementTree.SubElement(channel, "lastBuildDate").text = format_datetime(newest)

    for card in regulatory:
        if not card.obligation_id:
            raise ValueError(f"Regulatory card {card.id} has no obligation id")
        item = ElementTree.SubElement(channel, "item")
        ElementTree.SubElement(item, "title").text = card.headline
        ElementTree.SubElement(item, "description").text = f"{card.body}\n\n{card.disclaimer}"
        link = f"{base_url.rstrip('/')}/obligations/{card.obligation_id}"
        ElementTree.SubElement(item, "link").text = link
        guid = ElementTree.SubElement(item, "guid", {"isPermaLink": "false"})
        guid.text = card.obligation_id
        ElementTree.SubElement(item, "pubDate").text = format_datetime(card.published_at)
        issuer = next((chip.value for chip in card.chips if chip.chip_type == "issuer"), "")
        ElementTree.SubElement(item, "category").text = issuer

    ElementTree.indent(root, space="  ")
    return cast("bytes", ElementTree.tostring(root, encoding="utf-8", xml_declaration=True))
