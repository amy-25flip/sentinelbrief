import hashlib
import json
import os
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, get_args

from sentinelbrief.models import EvidenceEvent as EvidenceEventModel

IST = timezone(timedelta(hours=5, minutes=30))
ZERO_HASH = "0" * 64  # Genesis hash
EVENT_TYPES: frozenset[str] = frozenset(
    get_args(EvidenceEventModel.model_fields["type"].annotation)
)


def canonical_json(obj: dict[str, Any]) -> str:
    """Canonical JSON: sorted keys, no extra whitespace, ensure_ascii=False."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


@dataclass
class EvidenceEvent:
    seq: int
    ts_utc: datetime
    actor: str
    type: str  # incident_created, fact_recorded, clock_started, etc.
    payload: dict[str, Any]
    prev_hash: str
    hash: str
    clock_source: str = "system"
    ntp_synced: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "seq": self.seq,
            "ts_utc": self.ts_utc.isoformat(),
            "actor": self.actor,
            "type": self.type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "hash": self.hash,
            "clock_source": self.clock_source,
            "ntp_synced": self.ntp_synced,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceEvent":
        ts_utc = datetime.fromisoformat(data["ts_utc"])
        return cls(
            seq=data["seq"],
            ts_utc=ts_utc,
            actor=data["actor"],
            type=data["type"],
            payload=data["payload"],
            prev_hash=data["prev_hash"],
            hash=data["hash"],
            clock_source=data.get("clock_source", "system"),
            ntp_synced=data.get("ntp_synced", False),
        )


class EvidenceTimeline:
    """Append-only, hash-chained evidence timeline.

    Each event: {seq, ts_utc, actor, type, payload, prev_hash, hash}
    hash = SHA-256(canonical_json(event without hash) || prev_hash)

    Limits, stated plainly (shown in every export):
    - The chain proves ordering and integrity AFTER THE FACT, not that recorded times are true.
    - clock_source and ntp_synced are DECLARED by the caller. This module does not measure them.
    - Removing the most recent events cannot be detected from the file alone. Keep the head hash
      (or event count) somewhere the file owner cannot edit and pass it to verify().
    - Single writer only. append() refuses to run if the file changed under it, but that check
      is not a lock.
    """

    DISCLAIMER = (
        "LIMITS OF THIS EVIDENCE:\n"
        "- A hash chain proves ordering and integrity AFTER THE FACT. It does NOT prove that "
        "the recorded times were truthful.\n"
        "- clock_source and ntp_synced are declared by whoever recorded each event; they were "
        "not measured by this tool.\n"
        "- Removing the most recent events cannot be detected from this file alone. Compare the "
        "head hash below with a copy held elsewhere (email it, print it, or anchor it with an "
        "external timestamp authority)."
    )

    def __init__(self, storage_path: Path):
        self.storage_path = storage_path
        self.events: list[EvidenceEvent] = []
        self._load()

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        with open(self.storage_path, encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    self.events.append(EvidenceEvent.from_dict(data))

    def _compute_hash(self, event_dict: dict[str, Any], prev_hash: str) -> str:
        raw = canonical_json(event_dict)
        return hashlib.sha256((raw + prev_hash).encode("utf-8")).hexdigest()

    def append(
        self,
        actor: str,
        event_type: str,
        payload: dict[str, Any],
        clock_source: str = "system",
        ntp_synced: bool = False,
    ) -> EvidenceEvent:
        if event_type not in EVENT_TYPES:
            raise ValueError(f"Unknown event type '{event_type}'. Allowed: {sorted(EVENT_TYPES)}")
        self._assert_in_sync()
        seq = len(self.events)
        ts_utc = datetime.now(UTC)
        prev_hash = self.events[-1].hash if self.events else ZERO_HASH

        event_dict_no_hash: dict[str, Any] = {
            "seq": seq,
            "ts_utc": ts_utc.isoformat(),
            "actor": actor,
            "type": event_type,
            "payload": payload,
            "prev_hash": prev_hash,
            "clock_source": clock_source,
            "ntp_synced": ntp_synced,
        }

        h = self._compute_hash(event_dict_no_hash, prev_hash)

        event = EvidenceEvent(
            seq=seq,
            ts_utc=ts_utc,
            actor=actor,
            type=event_type,
            payload=payload,
            prev_hash=prev_hash,
            hash=h,
            clock_source=clock_source,
            ntp_synced=ntp_synced,
        )
        self.events.append(event)

        with open(self.storage_path, "a", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(event.to_dict()) + "\n")
            f.flush()
            os.fsync(f.fileno())

        return event

    def _assert_in_sync(self) -> None:
        """Refuse to append if another writer changed the file since it was loaded."""
        on_disk = 0
        last = ""
        if self.storage_path.exists():
            with open(self.storage_path, encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        on_disk += 1
                        last = line
        if on_disk != len(self.events):
            raise RuntimeError(
                f"Timeline file has {on_disk} events but {len(self.events)} are loaded: "
                "another writer changed it. Reload before appending."
            )
        if last and json.loads(last)["hash"] != self.events[-1].hash:
            raise RuntimeError("Timeline file head differs from the loaded head: reload first.")

    def verify(
        self, expected_head_hash: str | None = None, expected_count: int | None = None
    ) -> tuple[bool, int | None]:
        """Re-walk the chain. Returns (valid, first_bad_seq).

        Pass expected_head_hash / expected_count from an independently held record to also
        detect deletion of the most recent events.
        """
        prev_hash = ZERO_HASH
        prev_ts: datetime | None = None
        for i, event in enumerate(self.events):
            if event.seq != i:
                return False, i
            if event.prev_hash != prev_hash:
                return False, i
            if prev_ts is not None and event.ts_utc < prev_ts:
                return False, i  # time went backwards
            prev_ts = event.ts_utc

            event_dict = event.to_dict()
            del event_dict["hash"]
            expected_hash = self._compute_hash(event_dict, prev_hash)

            if event.hash != expected_hash:
                return False, i

            prev_hash = event.hash

        if expected_count is not None and len(self.events) != expected_count:
            return False, min(len(self.events), expected_count)
        if expected_head_hash is not None and self.head_hash() != expected_head_hash:
            return False, max(len(self.events) - 1, 0)
        return True, None

    def export_bundle(self, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)

        timeline_path = output_dir / "timeline.jsonl"
        manifest_path = output_dir / "manifest.json"
        summary_path = output_dir / "summary.md"
        verification_path = output_dir / "verification_result.json"

        # 1. Timeline
        with open(timeline_path, "w", encoding="utf-8", newline="\n") as f:
            for event in self.events:
                f.write(json.dumps(event.to_dict()) + "\n")

        # 2. Verification
        is_valid, broken_seq = self.verify()
        with open(verification_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "valid": is_valid,
                    "first_break_seq": broken_seq,
                    "verified_at": datetime.now(UTC).isoformat(),
                },
                f,
                indent=2,
            )

        # 3. Manifest
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "head_hash": self.head_hash(),
                    "event_count": len(self.events),
                    "generated_at": datetime.now(UTC).isoformat(),
                    "declared_clock_sources": sorted({e.clock_source for e in self.events}),
                    "events_declared_ntp_synced": sum(e.ntp_synced for e in self.events),
                    "disclaimer": self.DISCLAIMER,
                },
                f,
                indent=2,
            )

        # 4. Summary
        with open(summary_path, "w", encoding="utf-8", newline="\n") as f:
            f.write("# Evidence Timeline Audit Bundle\n\n")
            f.write(self.DISCLAIMER + "\n\n")
            f.write(f"**Event Count:** {len(self.events)}\n")
            f.write(f"**Head Hash:** `{self.head_hash()}`\n")
            sources = ", ".join(sorted({e.clock_source for e in self.events})) or "none"
            synced = sum(e.ntp_synced for e in self.events)
            f.write(
                f"**Declared clock sources:** {sources} "
                f"({synced} of {len(self.events)} events declared NTP-synced)\n"
            )
            f.write(
                f"**Integrity Valid:** {'Yes' if is_valid else f'No (breaks at seq {broken_seq})'}\n"
            )

        return output_dir

    def __len__(self) -> int:
        return len(self.events)

    def __iter__(self) -> Iterator[EvidenceEvent]:
        return iter(self.events)

    def head_hash(self) -> str:
        if not self.events:
            return ZERO_HASH
        return self.events[-1].hash
