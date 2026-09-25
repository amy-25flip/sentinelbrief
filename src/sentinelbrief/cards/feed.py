"""Feed management and ranking for SentinelBrief cards."""

import json
from pathlib import Path
from typing import Any

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
