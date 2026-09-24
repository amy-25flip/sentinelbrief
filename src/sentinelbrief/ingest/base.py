import hashlib
import json
import logging
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx

logger = logging.getLogger(__name__)


@dataclass
class FetchResult:
    """Result of a fetch operation."""

    url: str
    filename: str
    sha256: str
    content_type: str | None
    size_bytes: int
    etag: str | None
    last_modified: str | None
    retrieved_at: str  # ISO 8601
    changed: bool  # True if content changed vs previous fetch
    filepath: Path


class BaseFetcher:
    """Base class for all source fetchers.

    Implements polite fetching with:
    - Descriptive User-Agent
    - Rate limiting
    - Conditional requests (ETag/Last-Modified)
    - Retries with exponential backoff
    - SHA-256 hashing and manifest tracking
    - Idempotent: re-running doesn't duplicate
    - Change detection: if hash changes, records new version
    """

    USER_AGENT = "SentinelBrief/0.1 (Indian cyber-regulatory compliance research; contact: github.com/sentinelbrief)"
    DEFAULT_DELAY_SECONDS = 2.0
    MAX_RETRIES = 3

    def __init__(
        self, data_dir: str | Path = "data/raw", delay_seconds: float = DEFAULT_DELAY_SECONDS
    ):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.data_dir / "manifest.json"
        self.delay_seconds = delay_seconds
        self._last_request_time = 0.0

    def _wait_for_rate_limit(self) -> None:
        """Enforce rate limit between requests."""
        now = time.time()
        elapsed = now - self._last_request_time
        if elapsed < self.delay_seconds:
            time.sleep(self.delay_seconds - elapsed)
        self._last_request_time = time.time()

    def _compute_sha256(self, data: bytes) -> str:
        """Compute SHA-256 hash of data."""
        return hashlib.sha256(data).hexdigest()

    def _load_manifest(self) -> dict[str, Any]:
        """Load manifest from disk."""
        if self.manifest_path.exists():
            try:
                with open(self.manifest_path, encoding="utf-8") as f:
                    data: dict[str, Any] = json.load(f)
                    return data
            except json.JSONDecodeError:
                logger.warning("Manifest file is corrupt, creating a new one.")
                return {}
        return {}

    def _save_manifest(self, manifest: dict[str, Any]) -> None:
        """Save manifest to disk."""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)

    def _update_manifest(self, result: FetchResult) -> None:
        """Update manifest with a new fetch result."""
        manifest = self._load_manifest()

        # Convert Path object to string for JSON serialization
        manifest_entry = {
            "url": result.url,
            "filename": result.filename,
            "sha256": result.sha256,
            "content_type": result.content_type,
            "size_bytes": result.size_bytes,
            "etag": result.etag,
            "last_modified": result.last_modified,
            "retrieved_at": result.retrieved_at,
            "filepath": str(result.filepath),
        }

        manifest[result.filename] = manifest_entry
        self._save_manifest(manifest)

    def fetch(self, url: str, filename: str) -> FetchResult:
        """Fetch URL content with retry and backoff, updating manifest."""
        manifest = self._load_manifest()
        manifest_entry = manifest.get(filename)

        headers = {"User-Agent": self.USER_AGENT}
        if manifest_entry:
            if manifest_entry.get("etag"):
                headers["If-None-Match"] = manifest_entry["etag"]
            if manifest_entry.get("last_modified"):
                headers["If-Modified-Since"] = manifest_entry["last_modified"]

        logger.info(f"Fetching {url}")

        for attempt in range(self.MAX_RETRIES):
            self._wait_for_rate_limit()
            try:
                with httpx.Client(follow_redirects=True) as client:
                    response = client.get(url, headers=headers)

                if response.status_code == 304 and manifest_entry:
                    logger.info("Content not modified (304).")
                    filepath = self.data_dir / filename

                    # Ensure file exists even if 304, in case it was deleted
                    if not filepath.exists():
                        logger.warning(
                            "Got 304 but file missing, fetching without conditional headers."
                        )
                        headers.pop("If-None-Match", None)
                        headers.pop("If-Modified-Since", None)
                        continue

                    return FetchResult(
                        url=url,
                        filename=filename,
                        sha256=manifest_entry["sha256"],
                        content_type=manifest_entry.get("content_type"),
                        size_bytes=manifest_entry["size_bytes"],
                        etag=manifest_entry.get("etag"),
                        last_modified=manifest_entry.get("last_modified"),
                        retrieved_at=datetime.now(UTC).isoformat(),
                        changed=False,
                        filepath=filepath,
                    )

                response.raise_for_status()

                data = response.content
                sha256_hash = self._compute_sha256(data)

                filepath = self.data_dir / filename
                filepath.write_bytes(data)

                changed = True
                if manifest_entry and manifest_entry.get("sha256") == sha256_hash:
                    changed = False

                result = FetchResult(
                    url=url,
                    filename=filename,
                    sha256=sha256_hash,
                    content_type=response.headers.get("content-type"),
                    size_bytes=len(data),
                    etag=response.headers.get("etag"),
                    last_modified=response.headers.get("last-modified"),
                    retrieved_at=datetime.now(UTC).isoformat(),
                    changed=changed,
                    filepath=filepath,
                )

                self._update_manifest(result)
                return result

            except httpx.HTTPError as e:
                logger.error(f"Attempt {attempt + 1}/{self.MAX_RETRIES} failed: {e}")
                if attempt == self.MAX_RETRIES - 1:
                    raise
                # Exponential backoff
                time.sleep(2**attempt)

        raise RuntimeError(f"Failed to fetch {url} after {self.MAX_RETRIES} attempts.")

    def fetch_if_changed(self, url: str, filename: str) -> FetchResult | None:
        """Fetch URL content only if it has changed, returning None if unchanged."""
        result = self.fetch(url, filename)
        return result if result.changed else None
