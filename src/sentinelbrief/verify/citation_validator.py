import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from sentinelbrief.models import Citation


@dataclass
class CitationValidationResult:
    valid: bool
    errors: list[str]
    warnings: list[str]


class SourceTextStore:
    """Store for retrieving raw extracted text corresponding to an instrument."""

    def __init__(self, raw_dir: str | Path):
        self.raw_dir = Path(raw_dir)
        self._cache: dict[str, str] = {}
        self._id_to_file: dict[str, str] = {
            "cert-in.directions-70b.2022": "CERT-In_Directions_70B_28.04.2022.txt",
            "cert-in.faqs-70b.2022": "FAQs_on_CyberSecurityDirections_May2022.txt",
        }

    def get_text(self, instrument_id: str) -> str | None:
        if instrument_id in self._cache:
            return self._cache[instrument_id]

        # 1. Direct match: {instrument_id}.txt
        direct_path = self.raw_dir / f"{instrument_id}.txt"
        if direct_path.exists():
            text = direct_path.read_text(encoding="utf-8")
            self._cache[instrument_id] = text
            return text

        # 2. Known mapping
        if instrument_id in self._id_to_file:
            mapped_path = self.raw_dir / self._id_to_file[instrument_id]
            if mapped_path.exists():
                text = mapped_path.read_text(encoding="utf-8")
                self._cache[instrument_id] = text
                return text

        # 3. Scan metadata files
        for meta_file in self.raw_dir.glob("*.meta.json"):
            try:
                meta = json.loads(meta_file.read_text(encoding="utf-8"))
                if meta.get("instrument_id") == instrument_id:
                    txt_file = meta_file.with_suffix(".txt")
                    if txt_file.exists():
                        text = txt_file.read_text(encoding="utf-8")
                        self._cache[instrument_id] = text
                        return text
            except Exception:
                continue

        return None


def validate_citation(
    citation: Citation, source_text: str, expected_sha256: str | None = None
) -> CitationValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    # 1. verify excerpt_verbatim is an exact substring
    if citation.excerpt_verbatim not in source_text:
        errors.append("excerpt_verbatim is not an exact substring of the source text")

    # 2. if char_start and char_end are provided
    if citation.char_start is not None and citation.char_end is not None:
        expected_text = source_text[citation.char_start : citation.char_end]
        if expected_text != citation.excerpt_verbatim:
            errors.append(
                f"excerpt_verbatim does not match text at positions {citation.char_start}:{citation.char_end}"
            )

    # 3. verify source_sha256
    text_sha256 = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    if expected_sha256:
        # Check against the provided instrument/source hash (or text hash as fallback)
        if citation.source_sha256 != expected_sha256 and citation.source_sha256 != text_sha256:
            errors.append(
                f"source_sha256 mismatch: expected {expected_sha256}, got {citation.source_sha256}"
            )
    else:
        # Check against text hash
        if citation.source_sha256 != text_sha256:
            errors.append(
                f"source_sha256 mismatch: expected {text_sha256}, got {citation.source_sha256}"
            )

    return CitationValidationResult(valid=len(errors) == 0, errors=errors, warnings=warnings)
