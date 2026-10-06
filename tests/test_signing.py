"""Ed25519 signature over the evidence timeline head. Each test names the bug it catches."""

import json
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from sentinelbrief.clock.engine import IncidentProfile
from sentinelbrief.evidence.__main__ import main as evidence_cli
from sentinelbrief.evidence.signing import (
    KEY_ENV,
    KEY_FILE_ENV,
    SIGNATURE_FILE,
    generate_keypair,
    sign_head,
    verify_bundle,
    verify_head_signature,
)
from sentinelbrief.evidence.timeline import EvidenceTimeline
from sentinelbrief.workspace import CaseStore

REPO = Path(__file__).resolve().parents[1]
IST = timezone(timedelta(hours=5, minutes=30))


def _timeline(tmp_path: Path, events: int = 3) -> EvidenceTimeline:
    timeline = EvidenceTimeline(tmp_path / "timeline.jsonl")
    for index in range(events):
        timeline.append("Asha Rao", "note_added", {"n": index})
    return timeline


def test_signature_verifies_against_the_expected_key(tmp_path):
    """Catches: a correct signature rejected, or accepted without saying the key was pinned."""
    seed, public = generate_keypair()
    timeline = _timeline(tmp_path)
    record = sign_head(timeline, seed, "Asha Rao", datetime(2026, 10, 6, tzinfo=UTC))
    assert record["head_hash"] == timeline.head_hash() and record["event_count"] == 3
    assert record["public_key"] == public and "seed" not in json.dumps(record)
    assert seed not in json.dumps(record)
    result = verify_head_signature(record, timeline, public)
    assert result == {
        "trusted": True,
        "signature_consistent": True,
        "key_pinned": True,
        "reason": "signature verifies against the expected key",
    }


def test_unpinned_verification_says_so(tmp_path):
    """Catches: a bundle that carries its own key being reported as proof of who signed."""
    seed, _ = generate_keypair()
    timeline = _timeline(tmp_path)
    result = verify_head_signature(sign_head(timeline, seed, "Asha Rao"), timeline)
    assert result["trusted"] is False and result["key_pinned"] is False
    assert result["signature_consistent"] is True
    assert result["reason"].startswith("NOT TRUSTED")
    assert "valid" not in result  # no field a reader could take for acceptance


def test_attacker_resigning_with_their_own_key_fails_a_pinned_check(tmp_path):
    """Catches: a rewritten timeline re-signed with a new key passing verification."""
    seed, public = generate_keypair()
    attacker_seed, _ = generate_keypair()
    timeline = _timeline(tmp_path)
    forged = sign_head(timeline, attacker_seed, "Asha Rao")
    unpinned = verify_head_signature(forged, timeline)
    assert unpinned["signature_consistent"] is True and unpinned["trusted"] is False
    pinned = verify_head_signature(forged, timeline, public)
    assert pinned["trusted"] is False and "different key" in pinned["reason"]
    assert verify_head_signature(sign_head(timeline, seed, "Asha Rao"), timeline, public)["trusted"]


def test_truncating_the_timeline_after_signing_is_detected(tmp_path):
    """Catches: the most recent events removed without the signature noticing."""
    seed, public = generate_keypair()
    timeline = _timeline(tmp_path, events=4)
    record = sign_head(timeline, seed, "Asha Rao")
    path = tmp_path / "timeline.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(lines[:3]) + "\n", encoding="utf-8")
    shorter = EvidenceTimeline(path)
    assert shorter.verify()[0] is True  # the chain alone cannot see the truncation
    result = verify_head_signature(record, shorter, public)
    assert result["trusted"] is False and result["signature_consistent"] is False
    assert "does not match the signed head" in result["reason"]


def test_editing_an_event_after_signing_is_detected(tmp_path):
    """Catches: an altered event accepted because the signature was checked alone."""
    seed, public = generate_keypair()
    timeline = _timeline(tmp_path)
    record = sign_head(timeline, seed, "Asha Rao")
    path = tmp_path / "timeline.jsonl"
    path.write_text(path.read_text(encoding="utf-8").replace('"n": 1', '"n": 9'), encoding="utf-8")
    result = verify_head_signature(record, EvidenceTimeline(path), public)
    assert result["trusted"] is False and "broken" in result["reason"]


@pytest.mark.parametrize("field", ["head_hash", "event_count", "signed_at", "signer"])
def test_every_signed_field_is_covered_by_the_signature(tmp_path, field):
    """Catches: a field shown as signed that can be changed without breaking the signature."""
    seed, public = generate_keypair()
    record = sign_head(_timeline(tmp_path), seed, "Asha Rao")
    record[field] = 99 if field == "event_count" else str(record[field]) + "x"
    assert verify_head_signature(record, None, public)["trusted"] is False


def test_bad_keys_and_broken_timelines_are_refused(tmp_path):
    """Catches: signing with a malformed key, with no signer, or over a broken chain."""
    seed, _ = generate_keypair()
    timeline = _timeline(tmp_path)
    for bad in ("", "abc", "zz" * 32, seed[:-2]):
        with pytest.raises(ValueError, match="64 hexadecimal"):
            sign_head(timeline, bad, "Asha Rao")
    with pytest.raises(ValueError, match="name of the person"):
        sign_head(timeline, seed, "  ")
    path = tmp_path / "timeline.jsonl"
    path.write_text(path.read_text(encoding="utf-8").replace('"n": 0', '"n": 7'), encoding="utf-8")
    with pytest.raises(ValueError, match="broken timeline"):
        sign_head(EvidenceTimeline(path), seed, "Asha Rao")


def _case(tmp_path: Path) -> tuple[CaseStore, str]:
    store = CaseStore(tmp_path / "cases", REPO / "data")
    case_id = store.create(
        IncidentProfile(
            entity_classes=["irdai.insurer"],
            incident_types=["Malicious code attacks such as Ransomware"],
            when_noticed=datetime(2026, 10, 1, 10, 0, tzinfo=IST),
        ),
        "Asha Rao",
    )
    return store, case_id


def test_export_is_signed_only_when_a_key_is_configured(tmp_path, monkeypatch):
    """Catches: an unsigned bundle that does not say so, or a private key leaking into it."""
    store, case_id = _case(tmp_path)
    monkeypatch.delenv(KEY_ENV, raising=False)
    plain = store.export(case_id, tmp_path / "plain")
    assert not (plain / SIGNATURE_FILE).exists()
    assert "NOT signed" in (plain / "CASE_SUMMARY.md").read_text(encoding="utf-8")
    assert verify_bundle(plain)["reason"] == "the bundle is not signed"
    assert verify_bundle(plain)["trusted"] is False

    seed, public = generate_keypair()
    monkeypatch.setenv(KEY_ENV, seed)
    signed = store.export(case_id, tmp_path / "signed", signer="Asha Rao")
    assert "is signed (Ed25519)" in (signed / "CASE_SUMMARY.md").read_text(encoding="utf-8")
    manifest = json.loads((signed / "bundle_manifest.json").read_text(encoding="utf-8"))
    assert SIGNATURE_FILE in manifest["files"]
    for path in signed.iterdir():
        assert seed not in path.read_text(encoding="utf-8")
    assert verify_bundle(signed, public) == {
        "trusted": True,
        "signature_consistent": True,
        "key_pinned": True,
        "reason": "signature verifies against the expected key",
    }


def test_cli_exits_nonzero_unless_the_key_is_pinned_and_valid(tmp_path, monkeypatch, capsys):
    """Catches: `verify` reporting success for a bundle checked only against its own key."""
    store, case_id = _case(tmp_path)
    seed, public = generate_keypair()
    monkeypatch.setenv(KEY_ENV, seed)
    bundle = store.export(case_id, tmp_path / "bundle")
    assert evidence_cli(["verify", str(bundle), "--public-key", public]) == 0
    assert evidence_cli(["verify", str(bundle)]) == 1
    assert evidence_cli(["verify", str(bundle), "--public-key", generate_keypair()[1]]) == 1
    printed = capsys.readouterr().out
    assert printed.count("NOT TRUSTED") >= 2 and "TRUSTED\n" in printed
    assert '"valid"' not in printed


def test_keygen_writes_the_seed_to_a_new_file_and_never_prints_it(tmp_path, monkeypatch, capsys):
    """Catches: the private seed in terminal or CI output, or an existing key overwritten."""
    out = tmp_path / "signing.key"
    assert evidence_cli(["keygen", "--out", str(out)]) == 0
    seed = out.read_text(encoding="utf-8").strip()
    printed = capsys.readouterr()
    assert len(seed) == 64 and seed not in printed.out and seed not in printed.err
    assert "Public key" in printed.out
    assert evidence_cli(["keygen", "--out", str(out)]) == 2
    assert out.read_text(encoding="utf-8").strip() == seed

    store, case_id = _case(tmp_path)
    monkeypatch.delenv(KEY_ENV, raising=False)
    monkeypatch.setenv(KEY_FILE_ENV, str(out))
    bundle = store.export(case_id, tmp_path / "from-file")
    assert (bundle / SIGNATURE_FILE).is_file()


def test_export_fails_closed_on_a_malformed_key(tmp_path, monkeypatch):
    """Catches: a bad key producing an unsigned bundle that looks like a normal export."""
    store, case_id = _case(tmp_path)
    monkeypatch.setenv(KEY_ENV, "not-a-key")
    with pytest.raises(ValueError, match="64 hexadecimal"):
        store.export(case_id, tmp_path / "bad")
