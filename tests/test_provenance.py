"""Provenance: PDF, stored text, metadata and manifest must agree, and tampering must be caught."""

import json
from pathlib import Path

import pymupdf
import pytest

from sentinelbrief.extract.pdf_text import (
    meta_path_for,
    txt_path_for,
    verify_extraction,
    write_extraction,
)
from sentinelbrief.models import Instrument, ManifestEntry, Obligation
from sentinelbrief.verify.citation_validator import SourceTextStore, validate_citation
from sentinelbrief.verify.obligation_validator import validate_obligation
from sentinelbrief.verify.raw_provenance import (
    validate_acquisition_marker,
    validate_hand_acquisition,
    verify_pdf_authenticity,
    verify_pdf_integrity,
    verify_raw_dir,
)

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"


def _make_pdf(path: Path, text: str = "Direction one: report within 6 hours.") -> Path:
    doc = pymupdf.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    doc.save(path)
    doc.close()
    return path


@pytest.fixture
def raw_dir(tmp_path):
    pdf = _make_pdf(tmp_path / "doc.pdf")
    meta = write_extraction(
        pdf,
        instrument_id="test.doc",
        source_url="https://example.test/doc.pdf",
        retrieved_at="2026-01-01T00:00:00Z",
    )
    manifest = {
        "version": 1,
        "entries": [
            {
                "url": "https://example.test/doc.pdf",
                "filename": "doc.pdf",
                "sha256": meta["source_sha256"],
                "retrieved_at": "2026-01-01T00:00:00Z",
                "fetched_by": "BaseFetcher",
            }
        ],
    }
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return tmp_path


def test_clean_directory_passes(raw_dir):
    assert verify_raw_dir(raw_dir, allow_synthetic_fixtures=True) == ([], [])


def test_generated_pdf_is_rejected_without_authenticity_exemption(raw_dir):
    errors, _ = verify_raw_dir(raw_dir)
    assert any("producer and creator metadata are both empty" in e for e in errors)


def test_authenticity_exemption_is_documented(raw_dir):
    manifest = json.loads((raw_dir / "manifest.json").read_text(encoding="utf-8"))
    manifest["entries"][0]["authenticity_exemption"] = "unit-test synthetic PDF fixture"
    (raw_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    assert verify_raw_dir(raw_dir) == ([], [])


def test_manifest_entry_reverify_exemption_requires_text():
    with pytest.raises(ValueError, match="reverify_exemption"):
        ManifestEntry(
            url="https://rbidocs.rbi.org.in/rdocs/notification/PDFs/doc.pdf",
            filename="doc.pdf",
            sha256="0" * 64,
            retrieved_at="2026-01-01T00:00:00Z",
            reverify_exemption=" ",
        )


def test_committed_raw_data_is_consistent():
    errors, _ = verify_raw_dir(RAW)
    assert errors == []


def test_real_committed_pdfs_pass_authenticity_check():
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    entries = {e["filename"]: e for e in manifest["entries"]}
    assert (
        verify_pdf_authenticity(
            RAW / "CERT-In_Directions_70B_28.04.2022.pdf",
            entries["CERT-In_Directions_70B_28.04.2022.pdf"],
        )
        == []
    )


def test_truncated_pdf_is_rejected(tmp_path):
    source = RAW / "CERT-In_Directions_70B_28.04.2022.pdf"
    truncated = tmp_path / "truncated.pdf"
    truncated.write_bytes(source.read_bytes()[:-128])
    errors = verify_pdf_integrity(truncated, {"filename": "truncated.pdf"})
    assert any("does not end with %%EOF" in e for e in errors)


def test_real_committed_pdfs_pass_integrity_check():
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    entries = {e["filename"]: e for e in manifest["entries"]}
    for filename in (
        "CERT-In_Directions_70B_28.04.2022.pdf",
        "FAQs_on_CyberSecurityDirections_May2022.pdf",
        "CERT-In_directions_extension_MSMEs_and_validation_27.06.2022.pdf",
        "DPDP_Rules_2025_Gazette_GSR846E.pdf",
        "SEBI_CSCRF_Circular_2024-08-20.pdf",
        "RBI_NBFC_Cybersecurity_Directions_2026.pdf",
    ):
        assert verify_pdf_integrity(RAW / filename, entries[filename]) == []


def test_manifest_entry_requires_fetch_or_acquisition_marker():
    assert validate_acquisition_marker({"filename": "missing.pdf"})
    assert (
        validate_acquisition_marker({"filename": "fetched.pdf", "fetched_by": "BaseFetcher"}) == []
    )
    assert validate_acquisition_marker({"filename": "hand.pdf", "acquired_by": "reviewer"}) == []


def test_hand_acquired_manifest_entry_requires_acquired_by_note():
    entry = {"filename": "hand.pdf"}
    assert validate_hand_acquisition(entry, hand_acquired=False) == []
    assert validate_hand_acquisition(entry, hand_acquired=True)
    assert (
        validate_hand_acquisition(
            {"filename": "hand.pdf", "acquired_by": "reviewer via curl"}, hand_acquired=True
        )
        == []
    )


def test_real_hand_acquired_sources_have_acquired_by_notes():
    manifest = json.loads((RAW / "manifest.json").read_text(encoding="utf-8"))
    by_name = {e["filename"]: e for e in manifest["entries"]}
    assert by_name["CERT-In_Directions_70B_28.04.2022.pdf"]["acquired_by"]
    assert by_name["FAQs_on_CyberSecurityDirections_May2022.pdf"]["acquired_by"]
    assert by_name["CERT-In_directions_extension_MSMEs_and_validation_27.06.2022.pdf"][
        "acquired_by"
    ]
    assert by_name["DPDP_Rules_2025_Gazette_GSR846E.pdf"]["acquired_by"]
    assert by_name["SEBI_CSCRF_Circular_2024-08-20.pdf"]["acquired_by"]
    assert by_name["RBI_NBFC_Cybersecurity_Directions_2026.pdf"]["acquired_by"]
    assert by_name["RBI_NBFC_Cybersecurity_Directions_2026.pdf"]["acquired_at"]


def test_stored_text_is_written_with_lf(raw_dir):
    assert b"\r" not in txt_path_for(raw_dir / "doc.pdf").read_bytes()


def test_edited_text_is_detected(raw_dir):
    txt = txt_path_for(raw_dir / "doc.pdf")
    txt.write_text(txt.read_text(encoding="utf-8").replace("6 hours", "72 hours"), encoding="utf-8")
    errors, _ = verify_raw_dir(raw_dir)
    assert any("text_sha256" in e for e in errors)
    assert any("differs from a fresh extraction" in e for e in errors)


def test_edited_pdf_is_detected(raw_dir):
    _make_pdf(raw_dir / "doc.pdf", "Direction one: report within 72 hours.")
    errors, _ = verify_raw_dir(raw_dir)
    assert any("source_sha256" in e for e in errors)
    assert any("manifest" in e for e in errors)


def test_missing_metadata_is_detected(raw_dir):
    meta_path_for(raw_dir / "doc.pdf").unlink()
    errors, _ = verify_raw_dir(raw_dir)
    assert any("metadata file missing" in e for e in errors)


def test_pdf_not_in_manifest_is_detected(raw_dir):
    (raw_dir / "manifest.json").write_text('{"version": 1, "entries": []}', encoding="utf-8")
    errors, _ = verify_raw_dir(raw_dir)
    assert any("not listed in the manifest" in e for e in errors)


def test_crlf_checkout_still_verifies(raw_dir):
    txt = txt_path_for(raw_dir / "doc.pdf")
    txt.write_bytes(txt.read_bytes().replace(b"\n", b"\r\n"))
    assert verify_extraction(raw_dir / "doc.pdf") == ([], [])


def test_extraction_is_deterministic(tmp_path):
    a = write_extraction(
        _make_pdf(tmp_path / "a.pdf"), instrument_id="x", source_url="u", retrieved_at="t"
    )
    b = write_extraction(
        _make_pdf(tmp_path / "b.pdf"), instrument_id="x", source_url="u", retrieved_at="t"
    )
    assert a["text_sha256"] == b["text_sha256"]


def test_source_store_finds_text_by_instrument_id(raw_dir):
    store = SourceTextStore(raw_dir)
    assert "report within 6 hours" in (store.get_text("test.doc") or "")
    assert store.get_text("nope") is None


def test_source_store_rejects_duplicate_instrument_ids(raw_dir):
    pdf2 = _make_pdf(raw_dir / "other.pdf", "another document body text")
    write_extraction(pdf2, instrument_id="test.doc", source_url="u", retrieved_at="t")
    with pytest.raises(ValueError, match="Two source documents"):
        SourceTextStore(raw_dir)


def _real_obligation(**overrides):
    obligations = json.loads(
        (REPO / "data/obligations/cert-in.directions-70b.2022.json").read_text(encoding="utf-8")
    )
    data = {**obligations[1], **overrides}
    return Obligation.model_validate(data)


def _real_instrument():
    return Instrument.model_validate(
        json.loads(
            (REPO / "data/instruments/cert-in.directions-70b.2022.json").read_text(encoding="utf-8")
        )
    )


def _real_text():
    return SourceTextStore(RAW).get_text("cert-in.directions-70b.2022")


def test_real_obligation_passes():
    res = validate_obligation(_real_obligation(), _real_instrument(), _real_text())
    assert res.valid, res.errors


def test_ai_reviewer_cannot_mark_human_verified():
    obl = _real_obligation(
        verification="human_verified",
        verification_details={"reviewer": "antigravity-agent", "date": "2026-09-24"},
    )
    res = validate_obligation(obl, _real_instrument(), _real_text())
    assert not res.valid
    assert any("non-human" in e for e in res.errors)


def test_human_verified_needs_a_named_reviewer():
    obl = _real_obligation(verification="human_verified", verification_details=None)
    res = validate_obligation(obl, _real_instrument(), _real_text())
    assert any("named human reviewer" in e for e in res.errors)


def test_altered_verbatim_text_is_an_error_not_a_warning():
    obl = _real_obligation(text_verbatim="(ii) within 72 hours of noticing such incidents")
    res = validate_obligation(obl, _real_instrument(), _real_text())
    assert any("text_verbatim" in e for e in res.errors)


def test_citation_must_carry_the_pdf_hash_exactly():
    text = _real_text()
    obl = _real_obligation()
    cit = obl.citations[0]
    wrong = validate_citation(cit, text, expected_sha256="0" * 64)
    assert not wrong.valid
    # A citation carrying the *text* hash no longer passes when the PDF hash is expected.
    from sentinelbrief.extract.pdf_text import sha256_text

    text_hash_cit = cit.model_copy(update={"source_sha256": sha256_text(text)})
    assert not validate_citation(text_hash_cit, text, expected_sha256=cit.source_sha256).valid


def test_ambiguous_excerpt_without_range_is_rejected():
    from sentinelbrief.extract.pdf_text import sha256_text
    from sentinelbrief.models import Citation

    text = "the same sentence appears here. the same sentence appears here."
    cit = Citation(
        instrument_id="t",
        excerpt_verbatim="the same sentence appears here.",
        source_sha256=sha256_text(text),
    )
    res = validate_citation(cit, text)
    assert not res.valid
    assert "more than once" in res.errors[0]


def test_msme_extension_notice_is_ingested_and_says_25_sep_2022():
    text = SourceTextStore(RAW).get_text("cert-in.directions-70b.msme-extension.2022") or ""
    normalised = " ".join(text.split())
    assert "effective on 25th September, 2022" in normalised
    assert "Micro, Small & Medium Enterprises" in normalised
