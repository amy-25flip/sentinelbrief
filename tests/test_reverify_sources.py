import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest
import respx

REPO = Path(__file__).resolve().parents[1]


def _load_reverify():
    spec = importlib.util.spec_from_file_location(
        "reverify_sources", REPO / "scripts" / "reverify_sources.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["reverify_sources"] = module
    spec.loader.exec_module(module)
    return module


reverify_sources = _load_reverify()


def _manifest(tmp_path: Path, url: str, sha: str) -> Path:
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()
    (raw_dir / "manifest.json").write_text(
        json.dumps(
            {
                "version": 1,
                "entries": [{"url": url, "filename": "doc.pdf", "sha256": sha}],
            }
        ),
        encoding="utf-8",
    )
    return raw_dir


@respx.mock
def test_compare_entry_passes_on_matching_sha(tmp_path):
    content = b"official bytes"
    sha = hashlib.sha256(content).hexdigest()
    respx.get("https://example.test/doc.pdf").respond(200, content=content)

    finding = reverify_sources.compare_entry(
        {
            "url": "https://example.test/doc.pdf",
            "filename": "doc.pdf",
            "sha256": sha,
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is True
    assert finding.message == "sha256 matches"


@respx.mock
def test_compare_entry_fails_on_mismatch(tmp_path):
    respx.get("https://example.test/doc.pdf").respond(200, content=b"changed bytes")

    finding = reverify_sources.compare_entry(
        {
            "url": "https://example.test/doc.pdf",
            "filename": "doc.pdf",
            "sha256": "0" * 64,
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is False
    assert "sha256 mismatch" in finding.message


@respx.mock
def test_compare_entry_fails_on_http_error(tmp_path):
    respx.get("https://example.test/missing.pdf").respond(404)

    finding = reverify_sources.compare_entry(
        {
            "url": "https://example.test/missing.pdf",
            "filename": "missing.pdf",
            "sha256": "0" * 64,
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is False
    assert "fetch failed" in finding.message


def test_compare_entry_skips_rbi_entry_with_documented_exemption(tmp_path):
    finding = reverify_sources.compare_entry(
        {
            "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/doc.pdf",
            "filename": "rbi.pdf",
            "sha256": "0" * 64,
            "reverify_exemption": "RBI serves a CAPTCHA to automated clients",
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is True
    assert finding.skipped is True
    assert "CAPTCHA" in finding.message


@respx.mock
def test_non_exempt_entry_still_fails_on_fetch_error(tmp_path):
    respx.get("https://rbidocs.rbi.org.in/rdocs/notification/PDFs/doc.pdf").respond(403)

    finding = reverify_sources.compare_entry(
        {
            "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/doc.pdf",
            "filename": "rbi.pdf",
            "sha256": "0" * 64,
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is False
    assert finding.skipped is False
    assert "fetch failed" in finding.message


def test_reverify_exemption_requires_non_empty_reason(tmp_path):
    finding = reverify_sources.compare_entry(
        {
            "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/doc.pdf",
            "filename": "rbi.pdf",
            "sha256": "0" * 64,
            "reverify_exemption": " ",
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is False
    assert "non-empty reason" in finding.message


def test_reverify_exemption_is_limited_to_rbi_hosts(tmp_path):
    finding = reverify_sources.compare_entry(
        {
            "url": "https://example.test/doc.pdf",
            "filename": "doc.pdf",
            "sha256": "0" * 64,
            "reverify_exemption": "site blocks automated clients",
        },
        tmp_path,
        respect_robots=False,
    )

    assert finding.ok is False
    assert "only allowed for RBI hosts" in finding.message


@respx.mock
def test_main_returns_zero_when_all_entries_match(tmp_path, capsys):
    content = b"official bytes"
    sha = hashlib.sha256(content).hexdigest()
    raw_dir = _manifest(tmp_path, "https://example.test/doc.pdf", sha)
    respx.get("https://example.test/doc.pdf").respond(200, content=content)

    assert reverify_sources.main(["--raw-dir", str(raw_dir), "--ignore-robots"]) == 0
    output = capsys.readouterr().out
    assert "PASS doc.pdf" in output
    assert "Summary: 1 passed, 0 failed, 0 skipped" in output


@respx.mock
def test_main_returns_one_when_any_entry_fails(tmp_path, capsys):
    raw_dir = _manifest(tmp_path, "https://example.test/doc.pdf", "0" * 64)
    respx.get("https://example.test/doc.pdf").respond(200, content=b"changed bytes")

    assert reverify_sources.main(["--raw-dir", str(raw_dir), "--ignore-robots"]) == 1
    output = capsys.readouterr().out
    assert "FAIL doc.pdf" in output
    assert "Summary: 0 passed, 1 failed, 0 skipped" in output


def test_main_reports_skipped_entries(tmp_path, capsys):
    raw_dir = _manifest(
        tmp_path,
        "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/doc.pdf",
        "0" * 64,
    )
    manifest = json.loads((raw_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest["entries"][0]["reverify_exemption"] = "RBI serves a CAPTCHA to automated clients"
    (raw_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

    assert reverify_sources.main(["--raw-dir", str(raw_dir), "--ignore-robots"]) == 0
    output = capsys.readouterr().out
    assert "SKIP doc.pdf: RBI serves a CAPTCHA to automated clients" in output
    assert "Summary: 0 passed, 0 failed, 1 skipped" in output


@respx.mock
def test_main_respects_robots_by_default(tmp_path):
    content = b"official bytes"
    sha = hashlib.sha256(content).hexdigest()
    raw_dir = _manifest(tmp_path, "https://example.test/doc.pdf", sha)
    respx.get("https://example.test/robots.txt").respond(
        200, content=b"User-agent: *\nDisallow: /doc.pdf\n", headers={"content-type": "text/plain"}
    )

    assert reverify_sources.main(["--raw-dir", str(raw_dir)]) == 1


@respx.mock
def test_html_wrapper_change_with_same_instrument_content_passes(tmp_path):
    source = REPO / "data/raw/RBI_NBFC_IT_Framework_Master_Direction_2017.html"
    changed = source.read_bytes() + b"\n<!-- volatile wrapper marker -->\n"
    entry = next(
        item
        for item in json.loads((REPO / "data/raw/manifest.json").read_text(encoding="utf-8"))[
            "entries"
        ]
        if item["filename"] == source.name
    )
    respx.get(entry["url"]).respond(200, content=changed)
    finding = reverify_sources.compare_entry(entry, tmp_path, respect_robots=False)
    assert finding.ok
    assert "content_sha256" in finding.message
    assert "raw page bytes may differ" in finding.message


@pytest.mark.live
def test_live_reverify_sources_wrapper():
    assert reverify_sources.main(["--raw-dir", str(REPO / "data" / "raw"), "--ignore-robots"]) == 0
