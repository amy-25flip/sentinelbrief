"""Re-download manifest sources and compare their SHA-256 hashes.

This is a reviewer/live-network tool. Normal tests mock the HTTP layer; the live pytest
wrapper is marked `live` and deselected by default.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

from sentinelbrief.ingest.base import BaseFetcher


@dataclass(frozen=True)
class ReverifyFinding:
    filename: str
    ok: bool
    message: str


def load_current_entries(manifest_path: Path) -> list[dict[str, object]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return [
        entry
        for entry in manifest.get("entries", [])
        if entry.get("status", "current") == "current"
    ]


def compare_entry(
    entry: dict[str, object], download_dir: Path, *, respect_robots: bool = True
) -> ReverifyFinding:
    filename = str(entry["filename"])
    expected_sha = str(entry["sha256"])
    try:
        fetcher = BaseFetcher(download_dir, delay_seconds=0, respect_robots=respect_robots)
        result = fetcher.fetch(str(entry["url"]), filename=filename)
    except Exception as exc:
        return ReverifyFinding(filename, False, f"fetch failed: {exc}")

    if result.sha256 != expected_sha:
        return ReverifyFinding(
            filename,
            False,
            f"sha256 mismatch: manifest {expected_sha}, downloaded {result.sha256}",
        )
    return ReverifyFinding(filename, True, "sha256 matches")


def reverify_manifest(raw_dir: Path, *, respect_robots: bool = True) -> list[ReverifyFinding]:
    entries = load_current_entries(raw_dir / "manifest.json")
    with tempfile.TemporaryDirectory(prefix="sentinelbrief-reverify-") as tmp:
        download_dir = Path(tmp)
        return [
            compare_entry(entry, download_dir, respect_robots=respect_robots) for entry in entries
        ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=Path("data/raw"))
    parser.add_argument(
        "--ignore-robots",
        action="store_true",
        help="Disable robots.txt checks for manual reviewer troubleshooting.",
    )
    args = parser.parse_args(argv)

    findings = reverify_manifest(args.raw_dir, respect_robots=not args.ignore_robots)
    ok = True
    for finding in findings:
        status = "PASS" if finding.ok else "FAIL"
        print(f"{status} {finding.filename}: {finding.message}")
        ok = ok and finding.ok
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
