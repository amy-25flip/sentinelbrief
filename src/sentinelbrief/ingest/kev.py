import json
from typing import Any

from .base import BaseFetcher


class KEVFetcher(BaseFetcher):
    """Fetcher for CISA Known Exploited Vulnerabilities (KEV) catalog."""

    KEV_URL = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    def fetch_catalog(self) -> None:
        """Fetch the CISA KEV JSON catalog."""
        self.fetch(self.KEV_URL, "kev.json")

    def load_records(self) -> list[dict[str, Any]]:
        """Parse the KEV JSON into structured records.

        Note: The 'dueDate' field in these records is a US federal deadline,
        NOT an Indian regulatory deadline.
        """
        filepath = self.data_dir / "kev.json"
        if not filepath.exists():
            return []

        with open(filepath, encoding="utf-8") as f:
            data = json.load(f)
            vulnerabilities: list[dict[str, Any]] = data.get("vulnerabilities", [])
            return vulnerabilities
