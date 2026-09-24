from .base import BaseFetcher


class CertinFetcher(BaseFetcher):
    """Fetcher for CERT-In documents. Filenames match the committed data/raw files."""

    DIRECTIONS_URL = "https://www.cert-in.org.in/PDF/CERT-In_Directions_70B_28.04.2022.pdf"
    FAQS_URL = "https://www.cert-in.org.in/PDF/FAQs_on_CyberSecurityDirections_May2022.pdf"
    MSME_EXTENSION_URL = "https://www.cert-in.org.in/PDF/CERT-In_directions_extension_MSMEs_and_validation_27.06.2022.pdf"

    def fetch_directions(self) -> None:
        self.fetch(self.DIRECTIONS_URL)

    def fetch_faqs(self) -> None:
        self.fetch(self.FAQS_URL)

    def fetch_msme_extension(self) -> None:
        self.fetch(self.MSME_EXTENSION_URL)
