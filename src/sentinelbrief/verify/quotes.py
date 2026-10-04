"""Check that a quote occurs on a stated PDF page of a stored source document."""

import json
import re
from pathlib import Path
from typing import Any


def _collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


class SourcePages:
    """Page text of every ingested instrument, looked up by instrument id."""

    def __init__(self, data_dir: str | Path):
        root = Path(data_dir)
        self._raw = root / "raw"
        manifest = json.loads((self._raw / "manifest.json").read_text(encoding="utf-8"))
        by_hash = {entry["sha256"]: entry for entry in manifest["entries"]}
        self._stems: dict[str, str] = {}
        for path in sorted((root / "instruments").glob("*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            for item in value if isinstance(value, list) else [value]:
                entry = by_hash.get(item.get("source_sha256"))
                if entry is not None:
                    self._stems[item["id"]] = Path(entry["filename"]).stem
        self._cache: dict[str, tuple[str, list[dict[str, Any]]]] = {}

    def page_text(self, instrument_id: str, page: int) -> str:
        stem = self._stems.get(instrument_id)
        if stem is None:
            raise ValueError(f"No stored raw source for instrument: {instrument_id}")
        if stem not in self._cache:
            meta = json.loads((self._raw / f"{stem}.meta.json").read_text(encoding="utf-8"))
            text = (self._raw / f"{stem}.txt").read_text(encoding="utf-8")
            self._cache[stem] = (text, meta["page_offsets"])
        text, offsets = self._cache[stem]
        entry = next((item for item in offsets if item["page"] == page), None)
        if entry is None:
            raise ValueError(f"Page {page} does not exist in {instrument_id}")
        return text[entry["char_start"] : entry["char_end"]]

    def require_quote(self, instrument_id: str, page: int, quote: str) -> None:
        """Raise ValueError unless `quote` (whitespace-collapsed) is on that page."""
        if not quote.strip():
            raise ValueError(f"Empty source quote for {instrument_id} page {page}")
        if _collapse(quote) not in _collapse(self.page_text(instrument_id, page)):
            raise ValueError(f"Source quote for {instrument_id} is not on PDF page {page}")
