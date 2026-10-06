"""Verify data/raw: manifest, PDFs, extracted text and metadata must all agree."""

import json
from pathlib import Path

import pymupdf

from sentinelbrief.extract.html_text import verify_extraction as verify_html_extraction
from sentinelbrief.extract.pdf_text import sha256_bytes
from sentinelbrief.extract.pdf_text import verify_extraction as verify_pdf_extraction


def _pdf_metadata(path: Path) -> dict[str, str]:
    with pymupdf.open(path) as doc:  # type: ignore[no-untyped-call]
        metadata: dict[str, str] = doc.metadata or {}
        return metadata


def verify_pdf_authenticity(
    pdf_path: Path,
    manifest_entry: dict[str, object],
    *,
    allow_synthetic: bool = False,
) -> list[str]:
    """Reject blank-producer/creator PDFs unless explicitly exempted."""
    if allow_synthetic:
        return []
    if manifest_entry.get("authenticity_exemption"):
        return []

    metadata = _pdf_metadata(pdf_path)
    producer = str(metadata.get("producer") or "").strip()
    creator = str(metadata.get("creator") or "").strip()
    if not producer and not creator:
        return [
            f"{pdf_path.name}: PDF producer and creator metadata are both empty; "
            "generated-looking documents need authenticity_exemption with a reason"
        ]
    return []


def verify_pdf_integrity(
    pdf_path: Path,
    manifest_entry: dict[str, object],
    *,
    allow_synthetic: bool = False,
) -> list[str]:
    """Reject incomplete PDFs and PDFs PyMuPDF had to repair unless explicitly exempted."""
    if allow_synthetic:
        return []
    if manifest_entry.get("authenticity_exemption"):
        return []

    errors: list[str] = []
    if not pdf_path.read_bytes().rstrip().endswith(b"%%EOF"):
        errors.append(f"{pdf_path.name}: PDF does not end with %%EOF")
    try:
        with pymupdf.open(pdf_path) as doc:  # type: ignore[no-untyped-call]
            if doc.is_repaired:
                errors.append(f"{pdf_path.name}: PyMuPDF repaired the PDF on open")
    except pymupdf.FileDataError as exc:
        errors.append(f"{pdf_path.name}: PyMuPDF could not open the PDF without error: {exc}")
    return errors


def validate_acquisition_marker(entry: dict[str, object]) -> list[str]:
    """Every current source must say whether it was fetched by code or acquired by hand."""
    if str(entry.get("fetched_by") or "").strip() or str(entry.get("acquired_by") or "").strip():
        return []
    return [f"{entry.get('filename', '<unknown>')}: manifest entry lacks fetched_by or acquired_by"]


def validate_hand_acquisition(entry: dict[str, object], *, hand_acquired: bool) -> list[str]:
    """Hand-acquired source records must say who acquired them and how."""
    if hand_acquired and not str(entry.get("acquired_by") or "").strip():
        return [f"{entry.get('filename', '<unknown>')}: hand-acquired document lacks acquired_by"]
    return []


def verify_raw_dir(
    raw_dir: str | Path, *, allow_synthetic_fixtures: bool = False
) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors mean evidence cannot be trusted."""
    raw = Path(raw_dir)
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = raw / "manifest.json"
    manifest_hashes: dict[str, str] = {}
    manifest_entries: dict[str, dict[str, object]] = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for entry in manifest.get("entries", []):
            path = raw / entry["filename"]
            if not path.exists():
                errors.append(f"manifest lists {entry['filename']} but the file is missing")
                continue
            actual = sha256_bytes(path.read_bytes())
            if actual != entry["sha256"]:
                errors.append(f"{entry['filename']}: bytes do not match the sha256 in the manifest")
            if entry.get("status", "current") == "current":
                errors.extend(validate_acquisition_marker(entry))
            manifest_hashes[entry["filename"]] = entry["sha256"]
            manifest_entries[entry["filename"]] = entry
    else:
        errors.append("data/raw/manifest.json is missing")

    pdfs = sorted(raw.glob("*.pdf"))
    for pdf in pdfs:
        if pdf.name not in manifest_hashes:
            errors.append(f"{pdf.name}: PDF present but not listed in the manifest")
        entry = manifest_entries.get(pdf.name, {})
        errors.extend(verify_pdf_authenticity(pdf, entry, allow_synthetic=allow_synthetic_fixtures))
        errors.extend(verify_pdf_integrity(pdf, entry, allow_synthetic=allow_synthetic_fixtures))
        errs, warns = verify_pdf_extraction(pdf)
        errors.extend(errs)
        warnings.extend(warns)

    htmls = sorted(raw.glob("*.html"))
    for html in htmls:
        if html.name not in manifest_hashes:
            errors.append(f"{html.name}: HTML present but not listed in the manifest")
        errs, warns = verify_html_extraction(html)
        errors.extend(errs)
        warnings.extend(warns)

    source_stems = {p.with_suffix("").name for p in [*pdfs, *htmls]}
    for txt in raw.glob("*.txt"):
        if txt.with_suffix("").name not in source_stems:
            errors.append(f"{txt.name}: extracted text has no matching PDF or HTML source")
    return errors, warnings
