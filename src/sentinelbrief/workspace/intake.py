"""Alerts pushed by a SIEM or other monitoring system (webhook intake).

Rules this module keeps:

- An alert is data from another system. It never becomes a fact about the incident, never
  starts a clock and never opens a case. A named person opens the case and attests the times.
- Nothing here can conclude that an alert is not reportable. Dismissing an alert needs a named
  person and a reason, and is recorded as that person's decision, not a legal finding.
- The sender must prove knowledge of a shared secret (HMAC-SHA256 over the raw body). With no
  secret configured the endpoint is off.
- The raw body is stored byte for byte with its SHA-256, so what was received can be shown
  later. The time recorded is this server's clock at receipt, and says so.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import re
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sentinelbrief.workspace.cases import _require_person

SECRET_ENV = "SENTINELBRIEF_WEBHOOK_SECRET"
SIGNATURE_HEADER = "x-sentinelbrief-signature"
MAX_BODY_BYTES = 64 * 1024
# A shorter secret is guessable; the operator generates it, so there is no reason to allow one.
MIN_SECRET_CHARS = 32
_ID_RE = re.compile(r"^[0-9a-f]{32}$")
_TEXT_FIELDS = ("title", "source", "description", "severity", "external_id")
NOTICE = (
    "Received from another system. Nothing in this alert has been treated as a fact about the "
    "incident. Whether its receipt is the moment the incident was noticed, and whether the "
    "incident is reportable, are for a person to decide."
)


class IntakeError(ValueError):
    """A refused alert. `status` is the HTTP status the API returns."""

    def __init__(self, message: str, status: int):
        super().__init__(message)
        self.status = status


def sign_body(body: bytes, secret: str) -> str:
    """The header value a sender must supply for `body`."""
    return "sha256=" + hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()


def _parse_alert(body: bytes) -> dict[str, Any]:
    try:
        data = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IntakeError("The alert body must be a JSON object in UTF-8", 422) from exc
    if not isinstance(data, dict):
        raise IntakeError("The alert body must be a JSON object in UTF-8", 422)
    alert: dict[str, Any] = {}
    for name in _TEXT_FIELDS:
        value = data.get(name)
        if value is None:
            continue
        if not isinstance(value, str):
            raise IntakeError(f"{name} must be text", 422)
        alert[name] = value.strip()
    if not alert.get("title"):
        raise IntakeError("An alert needs a title", 422)
    detected = data.get("detected_at")
    if detected is not None:
        try:
            parsed = datetime.fromisoformat(str(detected))
        except ValueError as exc:
            raise IntakeError("detected_at must be an ISO 8601 time", 422) from exc
        if parsed.tzinfo is None:
            raise IntakeError("detected_at must carry a UTC offset", 422)
        alert["detected_at"] = parsed.isoformat()
    systems = data.get("systems_affected")
    if systems is not None:
        if not isinstance(systems, list) or not all(isinstance(item, str) for item in systems):
            raise IntakeError("systems_affected must be a list of text values", 422)
        alert["systems_affected"] = [item.strip() for item in systems if item.strip()]
    return alert


class IntakeStore:
    """File-backed alert inbox: one JSON record and one raw body file per alert."""

    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, alert_id: str) -> Path:
        if not _ID_RE.match(alert_id):
            raise KeyError("No such alert")
        path = self.root / f"{alert_id}.json"
        if not path.is_file():
            raise KeyError("No such alert")
        return path

    def _write(self, record: dict[str, Any]) -> None:
        path = self.root / f"{record['id']}.json"
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(
            json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
        )
        tmp.replace(path)

    def receive(
        self,
        body: bytes,
        signature: str | None,
        secret: str | None,
        now: datetime | None = None,
    ) -> tuple[dict[str, Any], bool]:
        """Verify and store an alert. Returns (record, created); a replayed body is not stored twice."""
        if not secret:
            raise IntakeError(f"Webhook intake is off: {SECRET_ENV} is not set", 503)
        if len(secret) < MIN_SECRET_CHARS:
            raise IntakeError(
                f"Webhook intake is off: {SECRET_ENV} must be at least {MIN_SECRET_CHARS} characters",
                503,
            )
        if len(body) > MAX_BODY_BYTES:
            raise IntakeError(f"The alert body is larger than {MAX_BODY_BYTES} bytes", 413)
        if not signature or not hmac.compare_digest(signature.strip(), sign_body(body, secret)):
            raise IntakeError("Missing or wrong signature", 401)
        alert = _parse_alert(body)
        digest = hashlib.sha256(body).hexdigest()
        for existing in self.list():
            if existing["body_sha256"] == digest:
                return existing, False
        record = {
            "id": uuid.uuid4().hex,
            "received_at": (now or datetime.now(UTC)).astimezone(UTC).isoformat(),
            "received_at_clock": "this server's clock; not checked against another source",
            "body_sha256": digest,
            "alert": alert,
            "status": "pending",
            "notice": NOTICE,
        }
        (self.root / f"{record['id']}.body").write_bytes(body)
        self._write(record)
        return record, True

    def get(self, alert_id: str) -> dict[str, Any]:
        value: dict[str, Any] = json.loads(self._path(alert_id).read_text(encoding="utf-8"))
        return value

    def raw_body(self, alert_id: str) -> bytes:
        self._path(alert_id)
        return (self.root / f"{alert_id}.body").read_bytes()

    def list(self, status: str | None = None) -> list[dict[str, Any]]:
        records = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted(self.root.glob("*.json"))
        ]
        records.sort(key=lambda item: (item["received_at"], item["id"]))
        return [item for item in records if status is None or item["status"] == status]

    def _decide(self, alert_id: str, status: str, extra: dict[str, Any]) -> dict[str, Any]:
        record = self.get(alert_id)
        if record["status"] != "pending":
            raise ValueError(f"This alert is already {record['status']}")
        record.update(status=status, **extra)
        self._write(record)
        return record

    def dismiss(
        self, alert_id: str, person: str, reason: str, now: datetime | None = None
    ) -> dict[str, Any]:
        person = _require_person(person, "The person dismissing the alert")
        if not reason.strip():
            raise ValueError("Dismissing an alert needs a reason")
        return self._decide(
            alert_id,
            "dismissed",
            {
                "dismissed_by": person,
                "dismissed_at": (now or datetime.now(UTC)).astimezone(UTC).isoformat(),
                "dismissal_reason": reason.strip(),
                "dismissal_note": (
                    "Recorded as this person's decision. It is not a finding that the event "
                    "was not reportable."
                ),
            },
        )

    def mark_case_opened(self, alert_id: str, case_id: str, person: str) -> dict[str, Any]:
        return self._decide(alert_id, "case_opened", {"case_id": case_id, "opened_by": person})
