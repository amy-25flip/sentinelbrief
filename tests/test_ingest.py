import json
import time
from pathlib import Path

import httpx
import jsonschema
import pytest
import respx

from sentinelbrief.ingest.base import BaseFetcher
from sentinelbrief.ingest.kev import KEVFetcher

REPO = Path(__file__).resolve().parents[1]
MANIFEST_SCHEMA = json.loads((REPO / "schema" / "manifest.schema.json").read_text(encoding="utf-8"))


class DummyFetcher(BaseFetcher):
    pass


@pytest.fixture
def data_dir(tmp_path):
    return tmp_path / "raw"


@pytest.fixture
def fetcher(data_dir):
    return DummyFetcher(data_dir=data_dir, delay_seconds=0.0, respect_robots=False)


def _manifest(data_dir):
    return json.loads((data_dir / "manifest.json").read_text(encoding="utf-8"))


def test_compute_sha256(fetcher):
    assert (
        fetcher._compute_sha256(b"hello world")
        == "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    )


def test_empty_manifest_has_the_schema_shape(fetcher):
    assert fetcher._load_manifest() == {"version": 1, "entries": []}


@respx.mock
def test_manifest_written_in_schema_format(fetcher, data_dir):
    respx.get("https://example.com/a.txt").respond(200, content=b"v1", headers={"ETag": "e1"})
    fetcher.fetch("https://example.com/a.txt")
    manifest = _manifest(data_dir)
    jsonschema.validate(manifest, MANIFEST_SCHEMA)
    (entry,) = manifest["entries"]
    assert entry["filename"] == "a.txt" and entry["status"] == "current"
    assert entry["sha256"] == fetcher._compute_sha256(b"v1") and entry["etag"] == "e1"


@respx.mock
def test_conditional_request_and_304_adds_nothing(fetcher, data_dir):
    url = "https://example.com/test.txt"
    route = respx.get(url)
    route.side_effect = [
        httpx.Response(200, content=b"content v1", headers={"ETag": "etag1"}),
        httpx.Response(304),
    ]
    first = fetcher.fetch(url, "test.txt")
    second = fetcher.fetch(url, "test.txt")
    assert route.calls[1].request.headers["if-none-match"] == "etag1"
    assert first.changed is True and second.changed is False
    assert second.sha256 == first.sha256
    assert len(_manifest(data_dir)["entries"]) == 1


@respx.mock
def test_same_bytes_again_is_not_a_change(fetcher, data_dir):
    url = "https://example.com/same.txt"
    respx.get(url).respond(200, content=b"same")
    fetcher.fetch(url, "same.txt")
    again = fetcher.fetch(url, "same.txt")
    assert again.changed is False
    assert len(_manifest(data_dir)["entries"]) == 1
    assert sorted(p.name for p in data_dir.iterdir()) == ["manifest.json", "same.txt"]


@respx.mock
def test_changed_document_keeps_the_old_bytes(fetcher, data_dir):
    url = "https://example.com/circular.pdf"
    respx.get(url).respond(200, content=b"version one")
    first = fetcher.fetch(url)
    respx.get(url).respond(200, content=b"version two")
    second = fetcher.fetch(url)

    assert second.changed is True and second.sha256 != first.sha256
    assert (data_dir / "circular.pdf").read_bytes() == b"version two"

    manifest = _manifest(data_dir)
    jsonschema.validate(manifest, MANIFEST_SCHEMA)
    by_status = {e["status"]: e for e in manifest["entries"]}
    old = by_status["superseded"]
    assert (data_dir / old["filename"]).read_bytes() == b"version one"
    assert old["sha256"] == first.sha256
    assert by_status["current"]["sha256"] == second.sha256


@respx.mock
def test_feed_fetchers_do_not_hoard_history(data_dir):
    feed = KEVFetcher(data_dir=data_dir, delay_seconds=0.0, respect_robots=False)
    respx.get(feed.KEV_URL).respond(200, content=b'{"vulnerabilities": []}')
    feed.fetch_catalog()
    respx.get(feed.KEV_URL).respond(200, content=b'{"vulnerabilities": [{"cveID": "CVE-1"}]}')
    feed.fetch_catalog()
    assert len(_manifest(data_dir)["entries"]) == 1
    assert sorted(p.name for p in data_dir.iterdir()) == ["kev.json", "manifest.json"]
    assert feed.load_records() == [{"cveID": "CVE-1"}]


def test_corrupt_manifest_raises_and_is_left_alone(fetcher, data_dir):
    data_dir.mkdir(exist_ok=True)
    (data_dir / "manifest.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="corrupt"):
        fetcher._load_manifest()
    assert (data_dir / "manifest.json").read_text(encoding="utf-8") == "{not json"


def test_unrecognised_manifest_format_raises(fetcher, data_dir):
    data_dir.mkdir(exist_ok=True)
    (data_dir / "manifest.json").write_text('{"a.pdf": {"sha256": "x"}}', encoding="utf-8")
    with pytest.raises(ValueError, match="unrecognised"):
        fetcher._load_manifest()


def test_real_manifest_is_loadable_and_schema_valid():
    real = DummyFetcher(data_dir=REPO / "data" / "raw", respect_robots=False)
    manifest = real._load_manifest()
    jsonschema.validate(manifest, MANIFEST_SCHEMA)
    assert real._current_entry(manifest, "CERT-In_Directions_70B_28.04.2022.pdf") is not None


@respx.mock
def test_client_errors_are_not_retried(fetcher):
    route = respx.get("https://example.com/missing.txt").respond(404)
    with pytest.raises(httpx.HTTPStatusError):
        fetcher.fetch("https://example.com/missing.txt")
    assert route.call_count == 1


@respx.mock
def test_server_errors_are_retried(fetcher, monkeypatch):
    monkeypatch.setattr(time, "sleep", lambda _s: None)
    route = respx.get("https://example.com/flaky.txt")
    route.side_effect = [httpx.Response(503), httpx.Response(200, content=b"ok")]
    assert fetcher.fetch("https://example.com/flaky.txt").changed is True
    assert route.call_count == 2


@respx.mock
def test_robots_txt_disallow_is_honoured(data_dir):
    polite = DummyFetcher(data_dir=data_dir, delay_seconds=0.0, contact="me@example.test")
    respx.get("https://example.com/robots.txt").respond(
        200, text="User-agent: *\nDisallow: /private/\n", headers={"content-type": "text/plain"}
    )
    ok = respx.get("https://example.com/public/a.txt").respond(200, content=b"a")
    blocked = respx.get("https://example.com/private/b.txt").respond(200, content=b"b")
    polite.fetch("https://example.com/public/a.txt")
    with pytest.raises(PermissionError):
        polite.fetch("https://example.com/private/b.txt")
    assert ok.called and not blocked.called


@respx.mock
def test_html_instead_of_robots_is_treated_as_no_rules(data_dir):
    polite = DummyFetcher(data_dir=data_dir, delay_seconds=0.0)
    respx.get("https://example.com/robots.txt").respond(
        200, text="<html>Disallow: /</html>", headers={"content-type": "text/html"}
    )
    respx.get("https://example.com/a.txt").respond(200, content=b"a")
    assert polite.fetch("https://example.com/a.txt").changed is True


def test_user_agent_uses_configured_contact(data_dir):
    f = DummyFetcher(data_dir=data_dir, contact="security@example.test")
    assert "security@example.test" in f.user_agent
    assert "github.com/sentinelbrief" not in f.user_agent


def test_rate_limiting(data_dir):
    f = DummyFetcher(data_dir=data_dir, delay_seconds=0.5, respect_robots=False)
    start = time.time()
    f._wait_for_rate_limit()
    f._wait_for_rate_limit()
    assert time.time() - start >= 0.5
