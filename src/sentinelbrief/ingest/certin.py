from .base import BaseFetcher


class CertinFetcher(BaseFetcher):
    """Fetcher for CERT-In documents."""

    DIRECTIONS_URL = "https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf"
    FAQS_URL = "https://www.cert-in.org.in/PDF/FAQs_on_CyberSecurityDirections_May2022.pdf"

    def fetch_directions(self) -> None:
        """Fetch the CERT-In Directions PDF."""
        self.fetch(self.DIRECTIONS_URL, "certin_directions.pdf")

    def fetch_faqs(self) -> None:
        """Fetch the CERT-In FAQs PDF."""
        self.fetch(self.FAQS_URL, "certin_faqs.pdf")
