"""Evidence lists: only source-quoted items may be called required (WP-D)."""

import json
from pathlib import Path

from fastapi.testclient import TestClient

from sentinelbrief.api.app import app
from sentinelbrief.models import Instrument, Obligation
from sentinelbrief.verify.obligation_validator import validate_obligation

REPO = Path(__file__).resolve().parents[1]


def _all_obligations() -> list[dict]:
    items: list[dict] = []
    for path in sorted((REPO / "data" / "obligations").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        items.extend(data if isinstance(data, list) else [data])
    return items


def _ntp() -> tuple[dict, Instrument, str]:
    raw = next(o for o in _all_obligations() if o["id"].endswith("ntp-sync"))
    instrument = Instrument.model_validate(
        json.loads(
            (REPO / "data" / "instruments" / f"{raw['instrument_id']}.json").read_text(
                encoding="utf-8"
            )
        )
    )
    manifest = json.loads((REPO / "data" / "raw" / "manifest.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    entry = next(e for e in entries if e["sha256"] == instrument.source_sha256)
    text = (
        (REPO / "data" / "raw" / entry["filename"]).with_suffix(".txt").read_text(encoding="utf-8")
    )
    return raw, instrument, text


def test_no_dataset_record_claims_unquoted_evidence_as_required():
    """Catches: an invented evidence item presented as a legal requirement."""
    for raw in _all_obligations():
        source = " ".join(raw["text_verbatim"].split())
        for item in raw["normalized"].get("evidence_required") or []:
            assert " ".join(item.split()) in source, (raw["id"], item)


def test_validator_rejects_invented_required_evidence():
    """Catches: the validator letting an author-written item into evidence_required."""
    raw, instrument, text = _ntp()
    poisoned = {
        **raw,
        "normalized": {
            **raw["normalized"],
            "evidence_required": ["Screenshot of the NTP dashboard"],
        },
    }
    result = validate_obligation(Obligation.model_validate(poisoned), instrument, text)
    assert not result.valid
    assert any("not quoted from text_verbatim" in e for e in result.errors)


def test_validator_accepts_quoted_required_evidence_and_any_suggestion():
    """Catches: the rule also blocking honest suggestions or genuine quotes."""
    raw, instrument, text = _ntp()
    quoted = " ".join(raw["text_verbatim"].split()[:6])
    record = {
        **raw,
        "normalized": {
            **raw["normalized"],
            "evidence_required": [quoted],
            "suggested_evidence": ["Screenshot of the NTP dashboard"],
        },
    }
    result = validate_obligation(Obligation.model_validate(record), instrument, text)
    assert result.valid, result.errors


def test_obligation_page_labels_suggestions_as_suggestions():
    """Catches: suggestions rendered under a heading that implies the law requires them."""
    raw = next(o for o in _all_obligations() if o["normalized"].get("suggested_evidence"))
    page = TestClient(app).get(f"/obligations/{raw['id']}")
    assert page.status_code == 200
    assert "Suggested evidence (not stated in the source text)" in page.text
    assert "Evidence the source requires" not in page.text
