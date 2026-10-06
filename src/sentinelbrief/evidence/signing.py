"""Ed25519 signature over the head of an evidence timeline.

What a signature adds, and what it does not:

- It binds a head hash and an event count to a key. Anyone holding the public key can check
  that the holder of the private key signed exactly this head. A copy of the timeline with
  events removed, added or altered no longer matches the signed head.
- It does NOT prove when the signature was made. `signed_at` is the signer's own clock. For
  time, send the signed head to an external timestamp authority or simply to someone else.
- It is only as good as the way the verifier obtained the public key. A bundle that carries
  both a signature and "its" public key proves nothing by itself: whoever rewrote the
  timeline could re-sign it with a new key. `verify_head_signature` therefore reports
  `key_pinned: False` unless the caller supplies the key it expects.
- The private key is supplied by the operator: a file named by SENTINELBRIEF_SIGNING_KEY_FILE
  (preferred) or the SENTINELBRIEF_SIGNING_KEY variable. Key generation writes the seed to a
  file the operator names and never prints it.
"""

from __future__ import annotations

import json
import os
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

from sentinelbrief.evidence.timeline import EvidenceTimeline, canonical_json

if TYPE_CHECKING:
    from collections.abc import Mapping

ALGORITHM = "Ed25519"
KEY_ENV = "SENTINELBRIEF_SIGNING_KEY"
KEY_FILE_ENV = "SENTINELBRIEF_SIGNING_KEY_FILE"
SIGNATURE_FILE = "head_signature.json"
_SIGNED_FIELDS = ("algorithm", "head_hash", "event_count", "signed_at", "signer")


def generate_keypair() -> tuple[str, str]:
    """Return (private seed, public key), both hex. The caller stores the seed."""
    key = SigningKey.generate()
    return key.encode().hex(), key.verify_key.encode().hex()


def _signing_key(seed_hex: str) -> SigningKey:
    try:
        seed = bytes.fromhex(seed_hex.strip())
    except ValueError as exc:
        raise ValueError("The signing key must be 64 hexadecimal characters") from exc
    if len(seed) != 32:
        raise ValueError("The signing key must be 64 hexadecimal characters")
    return SigningKey(seed)


def _message(record: Mapping[str, Any]) -> bytes:
    return canonical_json({name: record[name] for name in _SIGNED_FIELDS}).encode("utf-8")


def sign_head(
    timeline: EvidenceTimeline, seed_hex: str, signer: str, signed_at: datetime | None = None
) -> dict[str, Any]:
    """Sign the timeline's current head hash and event count."""
    if not signer.strip():
        raise ValueError("A signature needs the name of the person or system that signs")
    ok, first_break = timeline.verify()
    if not ok:
        raise ValueError(f"Refusing to sign a broken timeline (first break at seq {first_break})")
    key = _signing_key(seed_hex)
    record: dict[str, Any] = {
        "algorithm": ALGORITHM,
        "head_hash": timeline.head_hash(),
        "event_count": len(timeline),
        "signed_at": (signed_at or datetime.now(UTC)).astimezone(UTC).isoformat(),
        "signer": signer.strip(),
    }
    record["public_key"] = key.verify_key.encode().hex()
    record["signature"] = key.sign(_message(record)).signature.hex()
    return record


def _verdict(consistent: bool, pinned: bool, reason: str) -> dict[str, Any]:
    """`trusted` is the only field that means "accept this". It needs a pinned key."""
    return {
        "trusted": consistent and pinned,
        "signature_consistent": consistent,
        "key_pinned": pinned,
        "reason": reason,
    }


def verify_head_signature(
    record: Mapping[str, Any],
    timeline: EvidenceTimeline | None = None,
    expected_public_key: str | None = None,
) -> dict[str, Any]:
    """Check a signature record. Returns {trusted, signature_consistent, key_pinned, reason}.

    `signature_consistent` means the signature verifies against the key carried in the record
    and (when a timeline is given) the timeline is intact and has exactly the signed head hash
    and event count. That alone proves nothing about who signed: whoever rewrote a timeline
    could re-sign it. `trusted` is True only when, in addition, the key equals
    `expected_public_key`, which the caller must have obtained outside the bundle.
    """
    pinned = expected_public_key is not None
    missing = [name for name in (*_SIGNED_FIELDS, "public_key", "signature") if name not in record]
    if missing:
        return _verdict(False, pinned, f"missing fields: {missing}")
    if record["algorithm"] != ALGORITHM:
        return _verdict(False, pinned, "unsupported algorithm")
    public_key = str(record["public_key"]).lower()
    if pinned and public_key != str(expected_public_key).strip().lower():
        return _verdict(False, True, "signed with a different key than the one expected")
    try:
        VerifyKey(bytes.fromhex(public_key)).verify(
            _message(record), bytes.fromhex(str(record["signature"]))
        )
    except (BadSignatureError, ValueError):
        return _verdict(False, pinned, "signature does not verify")
    if timeline is not None:
        ok, first_break = timeline.verify()
        if not ok:
            return _verdict(False, pinned, f"timeline hash chain is broken at seq {first_break}")
        if timeline.head_hash() != record["head_hash"] or len(timeline) != record["event_count"]:
            return _verdict(
                False, pinned, "timeline does not match the signed head hash and event count"
            )
    if pinned:
        return _verdict(True, True, "signature verifies against the expected key")
    return _verdict(
        True,
        False,
        "NOT TRUSTED: the signature is only consistent with the key carried in the record. "
        "Obtain the public key independently and pass it to establish who signed",
    )


def load_seed() -> str | None:
    """The operator's signing seed: a file named by KEY_FILE_ENV, else the KEY_ENV variable."""
    key_file = os.environ.get(KEY_FILE_ENV)
    if key_file:
        return Path(key_file).read_text(encoding="utf-8").strip()
    return os.environ.get(KEY_ENV) or None


def write_signature(
    bundle_dir: Path, timeline: EvidenceTimeline, signer: str, seed_hex: str | None = None
) -> Path | None:
    """Write `head_signature.json` into an export bundle if a signing key is configured."""
    seed = seed_hex if seed_hex is not None else load_seed()
    if not seed:
        return None
    path = bundle_dir / SIGNATURE_FILE
    path.write_text(
        json.dumps(sign_head(timeline, seed, signer), indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def verify_bundle(bundle_dir: Path, expected_public_key: str | None = None) -> dict[str, Any]:
    """Verify the signature in an exported bundle against the bundle's own timeline."""
    signature_path = bundle_dir / SIGNATURE_FILE
    if not signature_path.is_file():
        return _verdict(False, expected_public_key is not None, "the bundle is not signed")
    record = json.loads(signature_path.read_text(encoding="utf-8"))
    timeline = EvidenceTimeline(bundle_dir / "timeline.jsonl")
    return verify_head_signature(record, timeline, expected_public_key)
