from .base import BaseFetcher


class EPSSFetcher(BaseFetcher):
    """Fetcher for FIRST Exploit Prediction Scoring System (EPSS) data."""

    API_URL = "https://api.first.org/data/v1/epss"

    def fetch_by_cve(self, cve_id: str) -> None:
        """Fetch EPSS data for a specific CVE ID."""
        url = f"{self.API_URL}?cve={cve_id}"
        self.fetch(url, f"epss_{cve_id}.json")

    def fetch_bulk_csv(self, date: str | None = None) -> None:
        """Fetch bulk EPSS data in CSV format.

        Args:
            date: Optional YYYY-MM-DD string to fetch for a specific date.
        """
        url = "https://epss.cyentia.com/epss_scores-current.csv.gz"
        if date:
            url = f"https://epss.cyentia.com/epss_scores-{date}.csv.gz"
            self.fetch(url, f"epss_{date}.csv.gz")
        else:
            self.fetch(url, "epss_current.csv.gz")
