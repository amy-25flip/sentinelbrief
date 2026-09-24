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
    """Finds the extracted text for an instrument via the instrument_id in each .meta.json."""

    def __init__(self, raw_dir: str | Path):
        self.raw_dir = Path(raw_dir)
        self._cache: dict[str, str] = {}
        self._index: dict[str, Path] = {}
        for meta_file in sorted(self.raw_dir.glob("*.meta.json")):
            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            instrument_id = meta.get("instrument_id")
            if not instrument_id:
                raise ValueError(f"{meta_file.name} has no instrument_id")
            if instrument_id in self._index:
                raise ValueError(f"Two source documents claim instrument_id {instrument_id}")
            self._index[instrument_id] = meta_file.with_suffix("").with_suffix(".txt")

    def get_text(self, instrument_id: str) -> str | None:
        if instrument_id in self._cache:
            return self._cache[instrument_id]
        path = self._index.get(instrument_id)
        if path is None or not path.exists():
            return None
        text = path.read_text(encoding="utf-8")  # universal newlines: CRLF checkouts hash as LF
        self._cache[instrument_id] = text
        return text


def validate_citation(
    citation: Citation, source_text: str, expected_sha256: str | None = None
) -> CitationValidationResult:
    """Check a citation against its source.

    expected_sha256 is the hash of the original source document (the PDF). When given, the
    citation must carry exactly that hash. Without it the citation is checked against the hash
    of the extracted text, which is only meaningful for self-contained unit tests.
    """
    errors: list[str] = []

    if citation.excerpt_verbatim not in source_text:
        errors.append("excerpt_verbatim is not an exact substring of the source text")

    if citation.char_start is not None and citation.char_end is not None:
        if source_text[citation.char_start : citation.char_end] != citation.excerpt_verbatim:
            errors.append(
                "excerpt_verbatim does not match text at positions "
                f"{citation.char_start}:{citation.char_end}"
            )
    elif (
        citation.excerpt_verbatim in source_text
        and source_text.count(citation.excerpt_verbatim) > 1
    ):
        errors.append("excerpt_verbatim occurs more than once and no char range disambiguates it")

    expected = expected_sha256 or hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    if citation.source_sha256 != expected:
        errors.append(f"source_sha256 mismatch: expected {expected}, got {citation.source_sha256}")

    return CitationValidationResult(valid=not errors, errors=errors, warnings=[])
