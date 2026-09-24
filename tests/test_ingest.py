import time
from datetime import UTC, datetime

import httpx
import pytest
import respx

from sentinelbrief.ingest.base import BaseFetcher, FetchResult


class DummyFetcher(BaseFetcher):
    pass


@pytest.fixture
def data_dir(tmp_path):
    return tmp_path / "raw"


@pytest.fixture
def fetcher(data_dir):
    return DummyFetcher(data_dir=data_dir, delay_seconds=0.1)


def test_compute_sha256(fetcher):
    data = b"hello world"
    # echo -n "hello world" | sha256sum
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert fetcher._compute_sha256(data) == expected


def test_manifest_loading_updating(fetcher, data_dir):
    assert fetcher._load_manifest() == {}

    result = FetchResult(
        url="http://example.com/file.txt",
        filename="file.txt",
        sha256="fakehash",
        content_type="text/plain",
        size_bytes=10,
        etag='W/"12345"',
        last_modified=None,
        retrieved_at=datetime.now(UTC).isoformat(),
        changed=True,
        filepath=data_dir / "file.txt",
    )

    fetcher._update_manifest(result)

    manifest = fetcher._load_manifest()
    assert "file.txt" in manifest
    assert manifest["file.txt"]["sha256"] == "fakehash"
    assert manifest["file.txt"]["url"] == "http://example.com/file.txt"
    assert manifest["file.txt"]["etag"] == 'W/"12345"'

    # Check physical file
    manifest_path = data_dir / "manifest.json"
    assert manifest_path.exists()


@respx.mock
def test_idempotent_download(fetcher, data_dir):
    url = "https://example.com/test.txt"
    filename = "test.txt"

    # Mock route returning 200 on first call, 304 on second
    route = respx.get(url)
    route.side_effect = [
        httpx.Response(
            200,
            content=b"content v1",
            headers={"ETag": "etag1", "Last-Modified": "Wed, 21 Oct 2015 07:28:00 GMT"},
        ),
        httpx.Response(304),
    ]

    result1 = fetcher.fetch(url, filename)
    assert route.call_count == 1
    assert result1.changed is True
    assert result1.sha256 == fetcher._compute_sha256(b"content v1")
    assert result1.etag == "etag1"

    # Reset delay for test speed
    fetcher._last_request_time = 0

    result2 = fetcher.fetch(url, filename)
    assert route.call_count == 2
    assert result2.changed is False
    assert result2.sha256 == result1.sha256
    assert result2.etag == result1.etag


@respx.mock
def test_change_detection(fetcher, data_dir):
    url = "https://example.com/test2.txt"
    filename = "test2.txt"

    # V1
    respx.get(url).respond(status_code=200, content=b"content v1")
    result1 = fetcher.fetch(url, filename)
    assert result1.changed is True

    fetcher._last_request_time = 0

    # V2 - changed content
    respx.get(url).respond(status_code=200, content=b"content v2")
    result2 = fetcher.fetch(url, filename)

    assert result2.changed is True
    assert result2.sha256 != result1.sha256
    assert result2.size_bytes == len(b"content v2")


def test_rate_limiting(fetcher):
    fetcher.delay_seconds = 0.5

    start = time.time()
    fetcher._wait_for_rate_limit()
    fetcher._wait_for_rate_limit()
    end = time.time()

    # Should take at least 0.5 seconds for the second wait
    assert end - start >= 0.5
