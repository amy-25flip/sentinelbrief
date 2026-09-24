"""Deterministic PDF -> text extraction with page offsets and provenance metadata.

The stored .txt is the text that citations point into. It is always written with LF line
endings so its hash and character offsets are identical on every platform, and it can always be
regenerated from the original PDF with `verify_extraction`.
"""

import argparse
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pymupdf

EXTRACTOR = "pymupdf"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def extract_pdf_text(pdf_path: Path) -> tuple[str, list[dict[str, int]]]:
    """Return the concatenated text of every page and each page's character offsets."""
    parts: list[str] = []
    offsets: list[dict[str, int]] = []
    position = 0
    with pymupdf.open(pdf_path) as doc:  # type: ignore[no-untyped-call]
        for number, page in enumerate(doc, start=1):
            text = page.get_text()
            parts.append(text)
            offsets.append(
                {"page": number, "char_start": position, "char_end": position + len(text)}
            )
            position += len(text)
    return "".join(parts), offsets


def txt_path_for(pdf_path: Path) -> Path:
    return pdf_path.with_suffix(".txt")


def meta_path_for(pdf_path: Path) -> Path:
    return pdf_path.with_suffix(".meta.json")


def write_extraction(
    pdf_path: Path,
    *,
    instrument_id: str,
    source_url: str,
    retrieved_at: str,
    content_type: str = "application/pdf",
) -> dict[str, Any]:
    """Extract text next to the PDF and write the metadata that ties them together."""
    text, offsets = extract_pdf_text(pdf_path)
    pdf_bytes = pdf_path.read_bytes()
    txt_path_for(pdf_path).write_text(text, encoding="utf-8", newline="\n")
    meta: dict[str, Any] = {
        "instrument_id": instrument_id,
        "source_url": source_url,
        "source_sha256": sha256_bytes(pdf_bytes),
        "retrieved_at": retrieved_at,
        "content_type": content_type,
        "size_bytes": len(pdf_bytes),
        "pages": len(offsets),
        "page_offsets": offsets,
        "text_sha256": sha256_text(text),
        "text_chars": len(text),
        "extractor": EXTRACTOR,
        "extractor_version": pymupdf.__version__,
    }
    meta_path_for(pdf_path).write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )
    return meta


def read_normalised_text(txt_path: Path) -> str:
    """Read stored text with universal newlines, so CRLF checkouts hash the same as LF."""
    return txt_path.read_text(encoding="utf-8")


def verify_extraction(pdf_path: Path) -> tuple[list[str], list[str]]:
    """Check that PDF, stored text and metadata agree. Returns (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []
    name = pdf_path.name
    meta_path, txt_path = meta_path_for(pdf_path), txt_path_for(pdf_path)

    if not pdf_path.exists():
        return [f"{name}: PDF missing"], warnings
    if not meta_path.exists():
        return [f"{name}: metadata file missing ({meta_path.name})"], warnings
    if not txt_path.exists():
        return [f"{name}: extracted text missing ({txt_path.name})"], warnings

    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    stored = read_normalised_text(txt_path)

    if sha256_bytes(pdf_path.read_bytes()) != meta.get("source_sha256"):
        errors.append(f"{name}: PDF bytes do not match source_sha256 in metadata")
    if sha256_text(stored) != meta.get("text_sha256"):
        errors.append(f"{name}: stored text does not match text_sha256 in metadata (edited?)")

    fresh, offsets = extract_pdf_text(pdf_path)
    if fresh != stored:
        message = f"{name}: stored text differs from a fresh extraction of the PDF"
        if meta.get("extractor_version") == pymupdf.__version__:
            errors.append(message)
        else:
            warnings.append(
                f"{message} (extractor {meta.get('extractor_version')} -> {pymupdf.__version__})"
            )
    elif offsets != meta.get("page_offsets"):
        errors.append(f"{name}: page offsets in metadata do not match the text")
    return errors, warnings


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Extract a PDF's text with provenance metadata")
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--instrument-id", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--retrieved-at", default=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"))
    args = parser.parse_args(argv)
    meta = write_extraction(
        args.pdf,
        instrument_id=args.instrument_id,
        source_url=args.source_url,
        retrieved_at=args.retrieved_at,
    )
    print(
        f"{args.pdf.name}: {meta['pages']} pages, {meta['text_chars']} chars, text_sha256={meta['text_sha256'][:12]}"
    )


if __name__ == "__main__":
    main()
