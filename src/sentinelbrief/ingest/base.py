import hashlib
import json
import logging
import os
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

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
    changed: bool  # True if content changed vs the previous fetch
    filepath: Path


def _now() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


class BaseFetcher:
    """Polite, evidence-preserving fetcher.

    - Descriptive User-Agent with a configurable contact; robots.txt honoured.
    - Rate limiting, conditional requests (ETag / Last-Modified), retry with backoff.
    - Writes data/raw/manifest.json in the format defined by schema/manifest.schema.json.
    - Idempotent: unchanged content adds nothing.
    - Evidence is never overwritten: when a document changes, the previous bytes are kept under
      `<stem>.<sha8><suffix>` and its manifest entry becomes `superseded`. Volatile data feeds
      (KEV, EPSS) set keep_history = False because they are not legal evidence.
    """

    DEFAULT_DELAY_SECONDS = 2.0
    MAX_RETRIES = 3
    keep_history = True

    def __init__(
        self,
        data_dir: str | Path = "data/raw",
        delay_seconds: float = DEFAULT_DELAY_SECONDS,
        respect_robots: bool = True,
        contact: str | None = None,
    ):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.data_dir / "manifest.json"
        self.delay_seconds = delay_seconds
        self.respect_robots = respect_robots
        contact = contact or os.environ.get("SENTINELBRIEF_CONTACT", "not set")
        self.user_agent = (
            f"SentinelBrief/0.1 (Indian cyber-regulatory research; contact: {contact})"
        )
        self._last_request_time = 0.0
        self._robots: dict[str, RobotFileParser | None] = {}

    # --- politeness -------------------------------------------------------------------------

    def _wait_for_rate_limit(self) -> None:
        elapsed = time.time() - self._last_request_time
        if elapsed < self.delay_seconds:
            time.sleep(self.delay_seconds - elapsed)
        self._last_request_time = time.time()

    def _check_robots(self, url: str) -> None:
        if not self.respect_robots:
            return
        parts = urlparse(url)
        origin = f"{parts.scheme}://{parts.netloc}"
        if origin not in self._robots:
            parser: RobotFileParser | None = None
            try:
                self._wait_for_rate_limit()
                resp = httpx.get(
                    f"{origin}/robots.txt",
                    headers={"User-Agent": self.user_agent},
                    follow_redirects=True,
                    timeout=20,
                )
                # Some sites answer with an HTML page instead of a robots file: treat as none.
                if resp.status_code == 200 and "text/plain" in resp.headers.get("content-type", ""):
                    parser = RobotFileParser()
                    parser.parse(resp.text.splitlines())
            except httpx.HTTPError:
                logger.warning("Could not read robots.txt for %s; proceeding", origin)
            self._robots[origin] = parser
        parser = self._robots[origin]
        if parser is not None and not parser.can_fetch(self.user_agent, url):
            raise PermissionError(f"robots.txt at {origin} disallows fetching {url}")

    # --- hashing and manifest ---------------------------------------------------------------

    def _compute_sha256(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

    def _load_manifest(self) -> dict[str, Any]:
        """Load the manifest. A corrupt or unrecognised file raises: it is never silently reset,
        because that would drop the record of what evidence we hold."""
        if not self.manifest_path.exists():
            return {"version": 1, "entries": []}
        try:
            data = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Manifest {self.manifest_path} is corrupt: {exc}") from exc
        if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
            raise ValueError(f"Manifest {self.manifest_path} has an unrecognised format")
        return data

    def _save_manifest(self, manifest: dict[str, Any]) -> None:
        tmp = self.manifest_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, self.manifest_path)

    @staticmethod
    def _current_entry(manifest: dict[str, Any], filename: str) -> dict[str, Any] | None:
        for entry in manifest["entries"]:
            if entry["filename"] == filename and entry.get("status", "current") == "current":
                result: dict[str, Any] = entry
                return result
        return None

    def _write_file(self, path: Path, data: bytes) -> None:
        tmp = path.with_name(path.name + ".tmp")
        tmp.write_bytes(data)
        os.replace(tmp, path)

    # --- fetching ---------------------------------------------------------------------------

    def fetch(self, url: str, filename: str | None = None) -> FetchResult:
        filename = filename or Path(urlparse(url).path).name
        if not filename:
            raise ValueError(f"Cannot derive a filename from {url}")
        self._check_robots(url)

        manifest = self._load_manifest()
        current = self._current_entry(manifest, filename)
        filepath = self.data_dir / filename

        headers = {"User-Agent": self.user_agent}
        if current and filepath.exists():
            if current.get("etag"):
                headers["If-None-Match"] = current["etag"]
            if current.get("last_modified"):
                headers["If-Modified-Since"] = current["last_modified"]

        logger.info("Fetching %s", url)
        for attempt in range(self.MAX_RETRIES):
            self._wait_for_rate_limit()
            try:
                with httpx.Client(follow_redirects=True, timeout=60) as client:
                    response = client.get(url, headers=headers)

                if response.status_code == 304 and current and filepath.exists():
                    current["last_checked_at"] = _now()
                    self._save_manifest(manifest)
                    return FetchResult(
                        url=url,
                        filename=filename,
                        sha256=current["sha256"],
                        content_type=current.get("content_type"),
                        size_bytes=current["size_bytes"],
                        etag=current.get("etag"),
                        last_modified=current.get("last_modified"),
                        retrieved_at=current["retrieved_at"],
                        changed=False,
                        filepath=filepath,
                    )
                if response.status_code == 304:
                    headers.pop("If-None-Match", None)
                    headers.pop("If-Modified-Since", None)
                    continue

                response.raise_for_status()
                return self._store(manifest, current, url, filename, filepath, response)

            except httpx.HTTPStatusError as exc:
                status = exc.response.status_code
                if 400 <= status < 500 and status != 429:
                    raise  # retrying a 404 or 403 will not help
                self._backoff(attempt, exc)
            except httpx.HTTPError as exc:
                self._backoff(attempt, exc)

        raise RuntimeError(f"Failed to fetch {url} after {self.MAX_RETRIES} attempts.")

    def _backoff(self, attempt: int, exc: Exception) -> None:
        logger.error("Attempt %d/%d failed: %s", attempt + 1, self.MAX_RETRIES, exc)
        if attempt == self.MAX_RETRIES - 1:
            raise exc
        time.sleep(2**attempt)

    def _store(
        self,
        manifest: dict[str, Any],
        current: dict[str, Any] | None,
        url: str,
        filename: str,
        filepath: Path,
        response: httpx.Response,
    ) -> FetchResult:
        data = response.content
        sha256 = self._compute_sha256(data)
        changed = current is None or current["sha256"] != sha256
        retrieved_at = _now()

        if not changed and current is not None:
            current["last_checked_at"] = retrieved_at
            if not filepath.exists():
                self._write_file(filepath, data)
            self._save_manifest(manifest)
            return FetchResult(
                url=url,
                filename=filename,
                sha256=sha256,
                content_type=current.get("content_type"),
                size_bytes=len(data),
                etag=response.headers.get("etag"),
                last_modified=response.headers.get("last-modified"),
                retrieved_at=current["retrieved_at"],
                changed=False,
                filepath=filepath,
            )

        if current is not None:
            if self.keep_history and filepath.exists():
                path = Path(filename)
                archive_name = f"{path.stem}.{current['sha256'][:8]}{path.suffix}"
                os.replace(filepath, self.data_dir / archive_name)
                current["filename"] = archive_name
                current["status"] = "superseded"
            else:
                manifest["entries"].remove(current)

        self._write_file(filepath, data)
        entry: dict[str, Any] = {
            "url": url,
            "filename": filename,
            "sha256": sha256,
            "retrieved_at": retrieved_at,
            "etag": response.headers.get("etag"),
            "last_modified": response.headers.get("last-modified"),
            "content_type": response.headers.get("content-type", ""),
            "size_bytes": len(data),
            "status": "current",
        }
        manifest["entries"].append(entry)
        self._save_manifest(manifest)
        return FetchResult(
            url=url,
            filename=filename,
            sha256=sha256,
            content_type=entry["content_type"],
            size_bytes=len(data),
            etag=entry["etag"],
            last_modified=entry["last_modified"],
            retrieved_at=retrieved_at,
            changed=True,
            filepath=filepath,
        )

    def fetch_if_changed(self, url: str, filename: str | None = None) -> FetchResult | None:
        result = self.fetch(url, filename)
        return result if result.changed else None
