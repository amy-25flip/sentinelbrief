"""Verify data/raw: manifest, PDFs, extracted text and metadata must all agree."""

import json
from pathlib import Path

from sentinelbrief.extract.pdf_text import sha256_bytes, verify_extraction


def verify_raw_dir(raw_dir: str | Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings). Errors mean evidence cannot be trusted."""
    raw = Path(raw_dir)
    errors: list[str] = []
    warnings: list[str] = []

    manifest_path = raw / "manifest.json"
    manifest_hashes: dict[str, str] = {}
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
            manifest_hashes[entry["filename"]] = entry["sha256"]
    else:
        errors.append("data/raw/manifest.json is missing")

    pdfs = sorted(raw.glob("*.pdf"))
    for pdf in pdfs:
        if pdf.name not in manifest_hashes:
            errors.append(f"{pdf.name}: PDF present but not listed in the manifest")
        errs, warns = verify_extraction(pdf)
        errors.extend(errs)
        warnings.extend(warns)

    pdf_stems = {p.with_suffix("").name for p in pdfs}
    for txt in raw.glob("*.txt"):
        if txt.with_suffix("").name not in pdf_stems:
            errors.append(f"{txt.name}: extracted text has no matching PDF")
    return errors, warnings
