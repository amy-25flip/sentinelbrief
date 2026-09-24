from datetime import datetime
from typing import Any

from sentinelbrief.cards.models import Card, CardChip


class CardGenerator:
    """Generates cards for the feed from various data sources."""

    def generate_regulatory_card(self, obligation: dict[str, Any], published_at: datetime) -> Card:
        """Generate a card for a regulatory obligation."""
        # Simple extraction for now
        action = obligation.get("normalized", {}).get("action", "")
        headline = action[:117] + "..." if len(action) > 120 else action
        body = (
            obligation.get("text_verbatim", "")[:497] + "..."
            if len(obligation.get("text_verbatim", "")) > 500
            else obligation.get("text_verbatim", "")
        )

        chips: list[CardChip] = []
        # Add basic chips
        chips.append(CardChip(label="Type", value="Mandatory", chip_type="mandatory"))

        deadline = obligation.get("normalized", {}).get("deadline", {})
        if deadline and deadline.get("kind") != "none":
            duration = deadline.get("duration_iso8601") or "specified"
            chips.append(CardChip(label="Deadline", value=duration, chip_type="deadline"))

        return Card(
            id=f"card-reg-{obligation.get('id')}",
            stream="regulatory",
            headline=headline,
            body=body,
            chips=chips,
            citation_text=obligation.get("text_verbatim"),
            published_at=published_at,
            priority=1.0,
            obligation_id=obligation.get("id"),
        )

    def generate_vulnerability_card(self, cve: dict[str, Any], published_at: datetime) -> Card:
        """Generate a thin card for a vulnerability."""
        cve_id = cve.get("cve_id", "Unknown")
        chips = [CardChip(label="CVE", value=cve_id, chip_type="cve_id")]

        priority = 0.5
        if cve.get("kev"):
            chips.append(CardChip(label="KEV", value="True", chip_type="kev"))
            priority = 2.0

        epss = cve.get("epss_score")
        if epss:
            chips.append(CardChip(label="EPSS", value=f"{epss}", chip_type="epss"))
            if float(epss) > 0.1:
                priority = max(priority, 1.5)

        return Card(
            id=f"card-vuln-{cve_id}",
            stream="vulnerability",
            headline=f"Vulnerability: {cve_id}",
            body=cve.get("description", "Vulnerability details")[:500],
            chips=chips,
            published_at=published_at,
            priority=priority,
            cve_id=cve_id,
        )
