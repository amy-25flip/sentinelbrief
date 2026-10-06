"""Deterministic extraction of the two stored RBI HTML evidence pages.

The 2017 Direction is emitted as one normalised visible-text block per line.  Its
segments use the document's printed clause identifiers, with ``intro-N`` for
numbered introduction paragraphs, ``7-closing`` for the unnumbered closing
outsourcing paragraph, and ``annex-i`` for Annex I.  The withdrawn-circular page
is emitted as tab-separated rows: serial, reference, subject, date.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

EXTRACTOR = "sentinelbrief-rbi-html"
EXTRACTOR_VERSION = "1.0"
OLD_FILENAME = "RBI_NBFC_IT_Framework_Master_Direction_2017.html"
WITHDRAWN_FILENAME = "RBI_Circulars_Withdrawn_List.html"
WITHDRAWN_HEADING = "Circulars Withdrawn by the Department of Supervision"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def _clean(value: str) -> str:
    return " ".join(value.replace("\xa0", " ").split())


class _VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self.skip += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self.skip:
            self.skip -= 1

    def handle_data(self, data: str) -> None:
        cleaned = _clean(data)
        if not self.skip and cleaned:
            self.parts.append(cleaned)


class _SupervisionRows(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_h3 = False
        self.heading: list[str] = []
        self.target = False
        self.in_table = False
        self.in_cell = False
        self.cell: list[str] = []
        self.row: list[str] = []
        self.rows: list[list[str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "h3":
            self.in_h3 = True
            self.heading = []
        elif tag == "table" and self.target and not self.in_table:
            self.in_table = True
        elif tag in {"td", "th"} and self.in_table:
            self.in_cell = True
            self.cell = []
        elif tag == "tr" and self.in_table:
            self.row = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h3" and self.in_h3:
            self.in_h3 = False
            self.target = _clean(" ".join(self.heading)) == WITHDRAWN_HEADING
        elif tag in {"td", "th"} and self.in_cell:
            self.in_cell = False
            self.row.append(_clean(" ".join(self.cell)))
        elif tag == "tr" and self.in_table and len(self.row) == 4:
            self.rows.append(self.row)
        elif tag == "table" and self.in_table:
            self.in_table = False
            self.target = False

    def handle_data(self, data: str) -> None:
        if self.in_h3:
            self.heading.append(data)
        if self.in_cell:
            self.cell.append(data)


def _old_segments(text: str) -> list[dict[str, int | str]]:
    """Locate the document's 47 migration units in the extracted text."""
    starts: list[tuple[str, int]] = []
    intro_start = text.index("Introduction:")
    section_a = text.index("Section-A\nIT GOVERNANCE", intro_start)
    section_b = text.index("Section-B", section_a)
    # Annex I is linked, rather than embedded, by the stored RBI page.  The index's
    # verbatim label is therefore the only self-contained Annex segment in this HTML.
    annex = text.index("Annex- I")

    for number in (2, 4, 5):
        match = re.search(rf"(?m)^{number}\. ", text[intro_start:section_a])
        if not match:
            raise ValueError(f"2017 Direction introduction paragraph {number} was not found")
        starts.append((f"intro-{number}", intro_start + match.start()))

    clause_ids = [
        "1",
        "1.1",
        "1.2",
        "2",
        "3",
        "3.1",
        "3.2",
        "3.3",
        "3.4",
        "3.5",
        "3.6",
        "3.7",
        "3.8",
        "3.9",
        "3.10",
        "3.11",
        "3.12",
        "4",
        "4.1",
        "4.2",
        "4.3",
        "4.4",
        "4.5",
        "5",
        "5.1",
        "5.2",
        "5.3",
        "5.4",
        "5.5",
        "5.6",
        "5.7",
        "6",
        "6.1",
        "6.2",
        "6.3",
        "6.4",
        "7",
        "7.1",
        "7.2",
        "7.3",
        "8",
        "8.1",
    ]
    cursor = section_a
    for clause_id in clause_ids:
        limit = section_b if not clause_id.startswith("8") else len(text)
        match = re.search(rf"(?m)^{re.escape(clause_id)}(?:\.|\s)", text[cursor:limit])
        if not match:
            raise ValueError(f"2017 Direction clause {clause_id} was not found")
        absolute = cursor + match.start()
        starts.append((clause_id, absolute))
        cursor = absolute + len(match.group(0))

    closing_match = re.search(
        r"(?im)^NBFC should ensure that their business continuity preparedness",
        text[section_a:section_b],
    )
    if not closing_match:
        raise ValueError("2017 Direction closing outsourcing paragraph was not found")
    starts.append(("7-closing", section_a + closing_match.start()))
    starts.append(("annex-i", annex))
    starts.sort(key=lambda item: item[1])
    if len(starts) != 47:
        raise ValueError(f"expected 47 old units, extracted {len(starts)}")
    result: list[dict[str, int | str]] = []
    for index, (segment_id, start) in enumerate(starts):
        end = starts[index + 1][1] if index + 1 < len(starts) else len(text)
        result.append({"id": segment_id, "char_start": start, "char_end": end})
    return result


def extract_html_text(html_path: Path) -> tuple[str, list[dict[str, int | str]]]:
    """Extract a supported RBI page into stable citation text and segments."""
    source = html_path.read_text(encoding="utf-8")
    if html_path.name == OLD_FILENAME:
        visible_parser = _VisibleText()
        visible_parser.feed(source)
        try:
            start = visible_parser.parts.index("RBI/DNBS/2016-17/53")
            end = visible_parser.parts.index("2026", start)
        except ValueError as exc:
            raise ValueError("RBI Direction content boundaries changed") from exc
        text = "\n".join(visible_parser.parts[start:end]).strip() + "\n"
        return text, _old_segments(text)
    if html_path.name == WITHDRAWN_FILENAME:
        rows_parser = _SupervisionRows()
        rows_parser.feed(source)
        rows = rows_parser.rows
        if not rows or rows[0] != ["Sr. No.", "Circular Number", "Subject", "Date"]:
            raise ValueError("RBI withdrawn-circular table structure changed")
        text = "\n".join("\t".join(row) for row in rows) + "\n"
        segments: list[dict[str, int | str]] = []
        position = 0
        for row in rows[1:]:
            line = "\t".join(row) + "\n"
            segments.append(
                {
                    "id": f"row-{row[0].rstrip('.')}",
                    "char_start": position,
                    "char_end": position + len(line),
                }
            )
            position += len(line)
        # Account for the header in all row offsets.
        header_length = len("\t".join(rows[0]) + "\n")
        for segment in segments:
            segment["char_start"] = int(segment["char_start"]) + header_length
            segment["char_end"] = int(segment["char_end"]) + header_length
        return text, segments
    raise ValueError(f"unsupported RBI HTML source: {html_path.name}")


def txt_path_for(html_path: Path) -> Path:
    return html_path.with_suffix(".txt")


def meta_path_for(html_path: Path) -> Path:
    return html_path.with_suffix(".meta.json")


def write_extraction(
    html_path: Path, *, instrument_id: str, source_url: str, retrieved_at: str
) -> dict[str, Any]:
    text, segments = extract_html_text(html_path)
    raw = html_path.read_bytes()
    txt_path_for(html_path).write_text(text, encoding="utf-8", newline="\n")
    meta: dict[str, Any] = {
        "instrument_id": instrument_id,
        "source_url": source_url,
        "source_sha256": sha256_bytes(raw),
        "content_sha256": sha256_text(text),
        "retrieved_at": retrieved_at,
        "extractor": EXTRACTOR,
        "extractor_version": EXTRACTOR_VERSION,
        "segments": segments,
    }
    meta_path_for(html_path).write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    return meta


def verify_extraction(html_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    meta_path = meta_path_for(html_path)
    txt_path = txt_path_for(html_path)
    if not meta_path.exists():
        return [f"{html_path.name}: metadata file missing ({meta_path.name})"], []
    if not txt_path.exists():
        return [f"{html_path.name}: extracted text missing ({txt_path.name})"], []
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    stored = txt_path.read_text(encoding="utf-8")
    if sha256_bytes(html_path.read_bytes()) != meta.get("source_sha256"):
        errors.append(f"{html_path.name}: HTML bytes do not match source_sha256 in metadata")
    if sha256_text(stored) != meta.get("content_sha256"):
        errors.append(
            f"{html_path.name}: stored text does not match content_sha256 in metadata (edited?)"
        )
    fresh, segments = extract_html_text(html_path)
    if fresh != stored:
        errors.append(f"{html_path.name}: stored text differs from a fresh extraction of the HTML")
    if segments != meta.get("segments"):
        errors.append(f"{html_path.name}: segment offsets in metadata do not match the text")
    return errors, []


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path)
    parser.add_argument("--instrument-id", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--retrieved-at", required=True)
    args = parser.parse_args(argv)
    meta = write_extraction(
        args.html,
        instrument_id=args.instrument_id,
        source_url=args.source_url,
        retrieved_at=args.retrieved_at,
    )
    print(f"{args.html.name}: content_sha256={meta['content_sha256']}")


if __name__ == "__main__":
    main()
