"""Durable human confirmations and corrections for migration proposals."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, cast

if TYPE_CHECKING:
    from pathlib import Path

from sentinelbrief.workspace.cases import _require_person


def _safe(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", value)


class ConfirmationStore:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.root = data_dir / "migrations" / "confirmations"
        self.root.mkdir(parents=True, exist_ok=True)

    def proposal_path(self, migration_id: str) -> Path:
        return self.data_dir / "migrations" / f"{migration_id}.json"

    def load(self, migration_id: str) -> dict[str, Any]:
        path = self.proposal_path(migration_id)
        if not path.exists():
            raise KeyError("migration not found")
        proposal: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        for mapping in proposal["mappings"]:
            confirmation = self._read(migration_id, mapping["old_clause"])
            if confirmation:
                mapping["confirmation"] = confirmation
        return proposal

    def _path(self, migration_id: str, old_clause: str) -> Path:
        return self.root / f"{_safe(migration_id)}__{_safe(old_clause)}.json"

    def _read(self, migration_id: str, old_clause: str) -> dict[str, Any] | None:
        path = self._path(migration_id, old_clause)
        if not path.exists():
            return None
        value: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        return value

    def _mapping(self, migration_id: str, old_clause: str) -> dict[str, Any]:
        proposal = json.loads(self.proposal_path(migration_id).read_text(encoding="utf-8"))
        mapping = next(
            (item for item in proposal["mappings"] if item["old_clause"] == old_clause), None
        )
        if mapping is None:
            raise KeyError("old clause not found")
        return cast("dict[str, Any]", mapping)

    def confirm(self, migration_id: str, old_clause: str, reviewer: str) -> dict[str, Any]:
        reviewer = _require_person(reviewer, "The reviewer")
        mapping = self._mapping(migration_id, old_clause)
        paragraphs = [candidate["paragraph"] for candidate in mapping["candidates"][:1]]
        record = {
            "migration_id": migration_id,
            "old_clause": old_clause,
            "decision": "confirmed",
            "paragraphs": paragraphs,
            "reviewer": reviewer,
            "date": datetime.now(UTC).date().isoformat(),
        }
        self._write(record)
        return record

    def correct(
        self,
        migration_id: str,
        old_clause: str,
        reviewer: str,
        paragraphs: list[str],
        reason: str,
    ) -> dict[str, Any]:
        reviewer = _require_person(reviewer, "The reviewer")
        self._mapping(migration_id, old_clause)
        if not paragraphs or any(not p.isdigit() or not 1 <= int(p) <= 158 for p in paragraphs):
            raise ValueError("corrections require one or more paragraph numbers from 1 to 158")
        if not reason.strip():
            raise ValueError("corrections require a reason")
        record = {
            "migration_id": migration_id,
            "old_clause": old_clause,
            "decision": "corrected",
            "paragraphs": paragraphs,
            "reason": reason.strip(),
            "reviewer": reviewer,
            "date": datetime.now(UTC).date().isoformat(),
        }
        self._write(record)
        return record

    def _write(self, record: dict[str, Any]) -> None:
        path = self._path(record["migration_id"], record["old_clause"])
        path.write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
        )
