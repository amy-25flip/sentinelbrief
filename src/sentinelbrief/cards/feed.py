from typing import Any

from sentinelbrief.cards.models import Card


class CardFeed:
    """Manages the feed of cards."""

    def __init__(self) -> None:
        self._cards: list[Card] = []

    def add_card(self, card: Card) -> None:
        self._cards.append(card)

    def add_cards(self, cards: list[Card]) -> None:
        self._cards.extend(cards)

    def get_feed(
        self, entity_classes: list[str] | None = None, limit: int = 10, offset: int = 0
    ) -> list[Card]:
        """Get ranked cards for an entity profile."""
        # For now, simplistic filtering if we added applicability info to cards.
        # Right now just sort by priority then recency
        sorted_cards = sorted(
            self._cards, key=lambda c: (c.priority, c.published_at.timestamp()), reverse=True
        )
        return sorted_cards[offset : offset + limit]

    def to_json(self) -> list[dict[str, Any]]:
        return [c.model_dump(mode="json") for c in self._cards]
