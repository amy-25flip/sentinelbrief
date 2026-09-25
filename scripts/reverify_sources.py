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
from urllib.parse import urlparse

from sentinelbrief.ingest.base import BaseFetcher

RBI_REVERIFY_EXEMPTION_HOSTS = {"rbidocs.rbi.org.in", "rbi.org.in"}


@dataclass(frozen=True)
class ReverifyFinding:
    filename: str
    ok: bool
    message: str
    skipped: bool = False


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
    if "reverify_exemption" in entry:
        reason = str(entry.get("reverify_exemption") or "").strip()
        if not reason:
            return ReverifyFinding(
                filename,
                False,
                "reverify_exemption requires a non-empty reason",
            )
        host = (urlparse(str(entry["url"])).hostname or "").lower()
        if host not in RBI_REVERIFY_EXEMPTION_HOSTS:
            allowed = ", ".join(sorted(RBI_REVERIFY_EXEMPTION_HOSTS))
            return ReverifyFinding(
                filename,
                False,
                f"reverify_exemption is only allowed for RBI hosts ({allowed}); got {host}",
            )
        return ReverifyFinding(filename, True, reason, skipped=True)

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
    passed = failed = skipped = 0
    for finding in findings:
        if finding.skipped:
            status = "SKIP"
            skipped += 1
        elif finding.ok:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1
        print(f"{status} {finding.filename}: {finding.message}")
        ok = ok and finding.ok
    print(f"Summary: {passed} passed, {failed} failed, {skipped} skipped")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
