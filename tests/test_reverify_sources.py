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


@respx.mock
def test_main_returns_zero_when_all_entries_match(tmp_path, capsys):
    content = b"official bytes"
    sha = hashlib.sha256(content).hexdigest()
    raw_dir = _manifest(tmp_path, "https://example.test/doc.pdf", sha)
    respx.get("https://example.test/doc.pdf").respond(200, content=content)

    assert reverify_sources.main(["--raw-dir", str(raw_dir), "--ignore-robots"]) == 0
    assert "PASS doc.pdf" in capsys.readouterr().out


@respx.mock
def test_main_returns_one_when_any_entry_fails(tmp_path, capsys):
    raw_dir = _manifest(tmp_path, "https://example.test/doc.pdf", "0" * 64)
    respx.get("https://example.test/doc.pdf").respond(200, content=b"changed bytes")

    assert reverify_sources.main(["--raw-dir", str(raw_dir), "--ignore-robots"]) == 1
    assert "FAIL doc.pdf" in capsys.readouterr().out


@respx.mock
def test_main_respects_robots_by_default(tmp_path):
    content = b"official bytes"
    sha = hashlib.sha256(content).hexdigest()
    raw_dir = _manifest(tmp_path, "https://example.test/doc.pdf", sha)
    respx.get("https://example.test/robots.txt").respond(
        200, content=b"User-agent: *\nDisallow: /doc.pdf\n", headers={"content-type": "text/plain"}
    )

    assert reverify_sources.main(["--raw-dir", str(raw_dir)]) == 1


@pytest.mark.live
def test_live_reverify_sources_wrapper():
    assert reverify_sources.main(["--raw-dir", str(REPO / "data" / "raw"), "--ignore-robots"]) == 0
