"""Attempts to get a bad source document past the provenance controls (adversarial pass, WP-E).

Findings recorded in docs/REVIEW_LOG.md "Review 10". Two attacks got through the offline gates:
a generated PDF with forged producer metadata, and a fabricated document carrying an exemption.
No offline check can tell forged bytes from real ones, so the control added here is a pinned
list: the committed source set cannot change without this file changing, which a reviewer sees
and answers by running scripts/reverify_sources.py against the regulators.
"""

import hashlib
import json
import shutil
from pathlib import Path

import pymupdf
import pytest

from sentinelbrief.extract.pdf_text import write_extraction
from sentinelbrief.verify.raw_provenance import verify_raw_dir

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"

# Every source document that is legal evidence, with its sha256 and whether it is exempt from
# live re-verification. Changing this list is a statement that you re-downloaded the document
# from the regulator (or, for an exempt one, that a named person did) and compared the hash.
PINNED_SOURCES: dict[str, tuple[str, bool] | tuple[str, bool, str]] = {
    "CERT-In_Directions_70B_28.04.2022.pdf": (
        "202c2f3953d792dcfb3ecb3634fc82ab75437ee596de89b8d59a211e8e42431f",
        False,
    ),
    "FAQs_on_CyberSecurityDirections_May2022.pdf": (
        "7c4ae9eab453db32a5feece63987f7606373d689755b5b2869bb367b5682d6af",
        False,
    ),
    "CERT-In_directions_extension_MSMEs_and_validation_27.06.2022.pdf": (
        "f0a2805f2a3bd0745560d417ffb6d41bf2cfe9920a5fd8a45b806ff10d61979f",
        False,
    ),
    "DPDP_Rules_2025_Gazette_GSR846E.pdf": (
        "eabc7d05e013144615d78ddc0e8b9c9aac1920e814f4fad38ce6560951f5aa08",
        False,
    ),
    "SEBI_CSCRF_Circular_2024-08-20.pdf": (
        "bd9ddb68bb49b9a92771ff01ed3138e01f0962b383e9ff643008b729290fc85d",
        False,
    ),
    "RBI_UCB_Cybersecurity_Directions_2026.pdf": (
        "c0225a9b1eed70d2900dd81eaeab7ec5be5e9574e64e84edbb7a33f434b593f9",
        True,
    ),
    "RBI_AIFI_Cybersecurity_Directions_2026.pdf": (
        "9658157f623bc8e8d60cec88948c4f2ce3146570c54f1094cf04bdd44c0e468a",
        True,
    ),
    "RBI_PaymentsBanks_Cybersecurity_Directions_2026.pdf": (
        "1d66101517708f620176f214abd869af24a1190ef1d796f943ca53c6fb17e4c5",
        True,
    ),
    "IRDAI_Information_and_Cyber_Security_Guidelines_2023.pdf": (
        "2c8d2fdac0008ee348a3c8fc12dcd27c2c14e61a3e1c9479344baae2ea618c98",
        True,
    ),
    "RBI_NBFC_Cybersecurity_Directions_2026.pdf": (
        "5b2432e53e1b1d1b500fb21ebe6176d28bcf3386543097b6c53aeb43ad860073",
        True,
    ),
    "RBI_NBFC_IT_Framework_Master_Direction_2017.html": (
        "040e28071c8e225737d82e966830d772a06e25ad55890f0428276f1e3d8c317c",
        False,
        "f00966dfa118b8c4530b632e598d4eb253ed8c043f57980451b1163e23a9c20c",
    ),
    "RBI_Circulars_Withdrawn_List.html": (
        "976c51313ff1240a17d1b49bf77915d6435df1977f0ed7514eddf7e232a05e2d",
        False,
        "31584176c8b4f771c7086d558b3ade6d82156f7b2d4d5f4577a725f85e257124",
    ),
}


def _manifest() -> list[dict]:
    return json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))["entries"]


def test_committed_sources_match_the_pinned_list():
    """Catches: a source added, replaced or newly exempted without a reviewer-visible change."""
    current = {
        e["filename"]: (
            (e["sha256"], bool(e.get("reverify_exemption")), e["content_sha256"])
            if e.get("content_sha256")
            else (e["sha256"], bool(e.get("reverify_exemption")))
        )
        for e in _manifest()
        if e.get("status", "current") == "current"
        and e["filename"].lower().endswith((".pdf", ".html"))
    }
    assert current == PINNED_SOURCES
    for filename, pin in PINNED_SOURCES.items():
        assert hashlib.sha256((RAW / filename).read_bytes()).hexdigest() == pin[0]
        if len(pin) == 3:
            meta = json.loads(
                (RAW / filename).with_suffix(".meta.json").read_text(encoding="utf-8")
            )
            assert meta["content_sha256"] == pin[2]


def test_no_committed_source_waives_the_authenticity_or_integrity_gate():
    """Catches: `authenticity_exemption` used to wave a generated or truncated file through."""
    assert [e["filename"] for e in _manifest() if e.get("authenticity_exemption")] == []


def test_pdf_generation_stays_out_of_the_codebase():
    """Catches: source-building code hidden outside scripts/ and src/, or using other libraries."""
    markers = (
        ".new_page(",
        "insert_text(",
        "insert_textbox(",
        "set_metadata(",
        "reportlab",
        "fpdf",
        "%PDF-",
    )
    # Test files that build synthetic PDFs as fixtures or as attacks. Nothing else may.
    allowed = {
        "tests/test_provenance.py",
        "tests/test_provenance_attacks.py",
        "tests/test_no_generated_sources.py",
    }
    offenders = []
    for root in ("scripts", "src", "benchmark", "tests"):
        for path in (REPO / root).rglob("*.py"):
            rel = path.relative_to(REPO).as_posix()
            if rel in allowed or ".pytest" in rel or "pytest-" in rel:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (PermissionError, OSError):
                continue  # stale sandbox scratch directories are unreadable and untracked
            offenders += [f"{rel} contains {m}" for m in markers if m in text]
    assert offenders == []


# --- the attacks themselves, run against a copy of the real data ---


@pytest.fixture
def raw_copy(tmp_path) -> Path:
    target = tmp_path / "raw"
    target.mkdir()
    for path in RAW.iterdir():
        if (
            path.is_file() and "CERT-In_Directions_70B" in path.name
        ) or path.name == "manifest.json":
            shutil.copy2(path, target / path.name)
    manifest = json.loads((target / "manifest.json").read_text(encoding="utf-8"))
    manifest["entries"] = [e for e in manifest["entries"] if (target / e["filename"]).exists()]
    (target / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    assert verify_raw_dir(target) == ([], [])
    return target


def _add_entry(raw: Path, filename: str, **extra) -> None:
    manifest = json.loads((raw / "manifest.json").read_text(encoding="utf-8"))
    data = (raw / filename).read_bytes()
    manifest["entries"].append(
        {
            "url": "https://rbidocs.rbi.org.in/rdocs/notification/PDFs/FAKE.PDF",
            "filename": filename,
            "sha256": hashlib.sha256(data).hexdigest(),
            "retrieved_at": "2026-10-04T00:00:00Z",
            "content_type": "application/pdf",
            "size_bytes": len(data),
            "status": "current",
            **extra,
        }
    )
    (raw / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")


def _forge(raw: Path, filename: str, *, producer: str) -> None:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), "The NBFC shall report cyber incidents within ninety days.")
    doc.set_metadata({"producer": producer, "creator": producer})
    doc.save(raw / filename)
    doc.close()
    write_extraction(
        raw / filename,
        instrument_id="fake.rbi",
        source_url="https://example.invalid",
        retrieved_at="2026-10-04T00:00:00Z",
    )


def test_attack_plain_generated_pdf_is_stopped(raw_copy):
    """Attack 1: a typed-up PDF with blank metadata. Stopped by the authenticity gate."""
    _forge(raw_copy, "Fake.pdf", producer="")
    _add_entry(raw_copy, "Fake.pdf", acquired_by="someone")
    errors, _ = verify_raw_dir(raw_copy)
    assert any("producer and creator metadata are both empty" in e for e in errors)


def test_attack_truncated_pdf_is_stopped(raw_copy):
    """Attack 2: a partial download. Stopped by the completeness gate and the hash."""
    real = next(raw_copy.glob("CERT-In_Directions_70B*.pdf"))
    real.write_bytes(real.read_bytes()[:-4096])
    errors, _ = verify_raw_dir(raw_copy)
    assert any("%%EOF" in e for e in errors) and any("do not match the sha256" in e for e in errors)


def test_attack_undocumented_entry_is_stopped(raw_copy):
    """Attack 3: a file dropped in with no acquisition marker, or with no manifest entry."""
    _forge(raw_copy, "Fake.pdf", producer="Adobe PDF Library 15.0")
    errors, _ = verify_raw_dir(raw_copy)
    assert any("not listed in the manifest" in e for e in errors)
    _add_entry(raw_copy, "Fake.pdf")
    errors, _ = verify_raw_dir(raw_copy)
    assert any("lacks fetched_by or acquired_by" in e for e in errors)


def test_attack_forged_metadata_passes_offline_gates_and_is_caught_by_the_pin(raw_copy):
    """Attack 4 (got through): forged producer metadata, an acquisition marker and an exempt
    RBI-host URL satisfy every offline gate, and live reverify would skip the entry. The pinned
    list is what stops it: the forged file is not on it."""
    _forge(raw_copy, "Fake.pdf", producer="Adobe PDF Library 15.0")
    _add_entry(
        raw_copy,
        "Fake.pdf",
        acquired_by="a person",
        reverify_exemption="the official server serves a CAPTCHA to automated clients",
    )
    assert verify_raw_dir(raw_copy) == ([], [])  # the documented limit of the offline gates
    entries = json.loads((raw_copy / "manifest.json").read_text(encoding="utf-8"))["entries"]
    current = {e["filename"] for e in entries if e["filename"].endswith(".pdf")}
    assert not current <= set(PINNED_SOURCES)  # the pin rejects it
