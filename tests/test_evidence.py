import json
from pathlib import Path

from sentinelbrief.evidence.timeline import EvidenceTimeline, canonical_json


def test_canonical_json():
    # Test canonical JSON is deterministic (same input -> same output)
    dict1 = {"b": 2, "a": 1, "c": {"e": 5, "d": 4}}
    dict2 = {"c": {"d": 4, "e": 5}, "a": 1, "b": 2}
    assert canonical_json(dict1) == canonical_json(dict2)
    assert canonical_json(dict1) == '{"a":1,"b":2,"c":{"d":4,"e":5}}'


def test_timeline_basic(tmp_path: Path):
    # 1. Create a new timeline, append 3 events, verify the chain
    storage = tmp_path / "timeline.jsonl"
    timeline = EvidenceTimeline(storage)

    e1 = timeline.append("admin", "incident_created", {"id": "123"})
    assert e1.seq == 0
    assert e1.prev_hash == "0" * 64

    e2 = timeline.append("admin", "fact_recorded", {"fact": "x"})
    assert e2.seq == 1
    assert e2.prev_hash == e1.hash

    e3 = timeline.append("system", "clock_started", {})
    assert e3.seq == 2
    assert e3.prev_hash == e2.hash

    valid, broken_seq = timeline.verify()
    assert valid is True
    assert broken_seq is None
    assert len(timeline) == 3


def test_timeline_tamper_payload(tmp_path: Path):
    # 2. Tamper with an event (change payload), verify detection
    storage = tmp_path / "timeline.jsonl"
    timeline = EvidenceTimeline(storage)
    timeline.append("admin", "incident_created", {"id": "123"})
    timeline.append("admin", "fact_recorded", {"fact": "x"})

    valid, broken_seq = timeline.verify()
    assert valid is True

    # Tamper payload in memory
    timeline.events[1].payload = {"fact": "y"}
    valid, broken_seq = timeline.verify()
    assert valid is False
    assert broken_seq == 1


def test_timeline_tamper_hash(tmp_path: Path):
    # 3. Tamper with the hash, verify detection
    storage = tmp_path / "timeline.jsonl"
    timeline = EvidenceTimeline(storage)
    timeline.append("admin", "incident_created", {"id": "123"})
    timeline.append("admin", "fact_recorded", {"fact": "x"})

    # Tamper hash
    timeline.events[1].hash = "1" * 64
    valid, broken_seq = timeline.verify()
    assert valid is False
    assert broken_seq == 1


def test_timeline_delete_event(tmp_path: Path):
    # 4. Delete an event from the middle, verify detection
    storage = tmp_path / "timeline.jsonl"
    timeline = EvidenceTimeline(storage)
    timeline.append("admin", "incident_created", {"id": "1"})
    timeline.append("admin", "fact_recorded", {"fact": "a"})
    timeline.append("admin", "fact_recorded", {"fact": "b"})

    # Delete middle event
    del timeline.events[1]

    # This will cause seq numbers to be out of sync or prev_hash mismatch
    valid, broken_seq = timeline.verify()
    assert valid is False
    # Depending on how verify checks seq vs i, it might fail on seq or prev_hash
    # In our implementation, event.seq != i fails first at i=1
    assert broken_seq == 1


def test_timeline_export_bundle(tmp_path: Path):
    # 5. Export bundle and verify it contains all expected files
    storage = tmp_path / "timeline.jsonl"
    timeline = EvidenceTimeline(storage)
    timeline.append("admin", "incident_created", {"id": "1"})

    bundle_dir = tmp_path / "bundle"
    timeline.export_bundle(bundle_dir)

    assert (bundle_dir / "timeline.jsonl").exists()
    assert (bundle_dir / "manifest.json").exists()
    assert (bundle_dir / "summary.md").exists()
    assert (bundle_dir / "verification_result.json").exists()

    # Check manifest contents
    with open(bundle_dir / "manifest.json") as f:
        manifest = json.load(f)
        assert manifest["event_count"] == 1
        assert manifest["head_hash"] == timeline.head_hash()

    # Check disclaimer in summary
    with open(bundle_dir / "summary.md") as f:
        summary = f.read()
        assert "LIMITS OF THIS EVIDENCE" in summary
        assert "declared" in summary


def test_genesis_hash_zero(tmp_path: Path):
    # 7. Test genesis event has prev_hash = '0' * 64
    storage = tmp_path / "timeline.jsonl"
    timeline = EvidenceTimeline(storage)
    e = timeline.append("test", "note_added", {})
    assert e.prev_hash == "0" * 64
