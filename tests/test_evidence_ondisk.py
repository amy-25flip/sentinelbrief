"""Tampering with the FILE on disk (the real threat), not just objects held in memory."""

import json
from datetime import timedelta
from pathlib import Path

import pytest

from sentinelbrief.evidence.timeline import EvidenceTimeline


def _build(tmp_path: Path, n: int = 4):
    path = tmp_path / "timeline.jsonl"
    tl = EvidenceTimeline(path)
    for i in range(n):
        tl.append("admin", "fact_recorded", {"n": i})
    return path, tl


def test_edited_file_is_detected_after_reload(tmp_path):
    path, _ = _build(tmp_path)
    lines = path.read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[2])
    event["payload"] = {"n": 999}
    lines[2] = json.dumps(event)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert EvidenceTimeline(path).verify() == (False, 2)


def test_deleted_middle_line_is_detected_after_reload(tmp_path):
    path, _ = _build(tmp_path)
    lines = path.read_text(encoding="utf-8").splitlines()
    del lines[1]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    valid, broken = EvidenceTimeline(path).verify()
    assert valid is False and broken == 1


def test_tail_truncation_is_invisible_without_an_external_head(tmp_path):
    path, tl = _build(tmp_path)
    head, count = tl.head_hash(), len(tl)
    lines = path.read_text(encoding="utf-8").splitlines()[:-2]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    reloaded = EvidenceTimeline(path)
    assert reloaded.verify() == (True, None)  # the file alone cannot show it
    assert reloaded.verify(expected_head_hash=head)[0] is False
    assert reloaded.verify(expected_count=count)[0] is False


def test_matching_external_head_passes(tmp_path):
    _, tl = _build(tmp_path)
    assert tl.verify(expected_head_hash=tl.head_hash(), expected_count=len(tl)) == (True, None)


def test_timestamps_going_backwards_are_flagged(tmp_path):
    _, tl = _build(tmp_path, 3)
    tl.events[2].ts_utc = tl.events[1].ts_utc - timedelta(seconds=5)
    assert tl.verify()[0] is False


def test_unknown_event_type_is_rejected(tmp_path):
    tl = EvidenceTimeline(tmp_path / "t.jsonl")
    with pytest.raises(ValueError, match="Unknown event type"):
        tl.append("a", "made_up_type", {})


def test_second_writer_is_detected(tmp_path):
    path, tl = _build(tmp_path, 2)
    other = EvidenceTimeline(path)
    other.append("b", "note_added", {"x": 1})
    with pytest.raises(RuntimeError, match="another writer"):
        tl.append("a", "note_added", {"y": 2})


def test_file_is_written_with_lf_only(tmp_path):
    path, _ = _build(tmp_path, 2)
    assert b"\r" not in path.read_bytes()


def test_clock_claims_are_labelled_as_declared(tmp_path):
    tl = EvidenceTimeline(tmp_path / "t.jsonl")
    tl.append("a", "note_added", {}, clock_source="ntp:time.nplindia.org", ntp_synced=True)
    tl.append("a", "note_added", {})
    bundle = tl.export_bundle(tmp_path / "b")
    manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["events_declared_ntp_synced"] == 1
    assert "system" in manifest["declared_clock_sources"]
    assert "not measured" in manifest["disclaimer"]
