import importlib.util
import json
import shutil
import sys
from pathlib import Path

from fastapi.testclient import TestClient

import sentinelbrief.api.app as api_module
from sentinelbrief.api.app import app
from sentinelbrief.migrator.core import (
    build_migration,
    detect_differences,
    segment_new_direction,
    write_migration,
)

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "data" / "raw"
MIGRATION_ID = "rbi.nbfc-it-framework.2017__rbi.nbfc-cyber.2026"

_spec = importlib.util.spec_from_file_location(
    "migrator_scorer", REPO / "benchmark/runner/migrator_scorer.py"
)
assert _spec and _spec.loader
_scorer = importlib.util.module_from_spec(_spec)
sys.modules["migrator_scorer"] = _scorer
_spec.loader.exec_module(_scorer)
score = _scorer.score
wilson = _scorer.wilson


def _new_segments():
    text = (RAW / "RBI_NBFC_Cybersecurity_Directions_2026.txt").read_text(encoding="utf-8")
    meta = json.loads(
        (RAW / "RBI_NBFC_Cybersecurity_Directions_2026.meta.json").read_text(encoding="utf-8")
    )
    return segment_new_direction(text, meta["page_offsets"])


def test_new_direction_has_158_numbered_paragraphs_and_known_page():
    segments = _new_segments()
    assert [segment.id for segment in segments] == [str(number) for number in range(1, 159)]
    paragraph = segments[27]
    assert paragraph.page == 18
    assert " ".join(paragraph.text.split()).startswith(
        "28. The NBFC shall report cyber incidents on DAKSH"
    )


def test_running_headers_are_stripped_from_search_text():
    assert all(
        "RBI (NBFCs \N{EN DASH} Cybersecurity" not in (segment.search_text or "")
        for segment in _new_segments()
    )


def test_changed_rule_modal_shift():
    differences = detect_differences(
        "The NBFC may use signatures.", "The NBFC shall use signatures."
    )
    assert any("modal verb" in item for item in differences)


def test_changed_rule_number_or_duration_shift():
    differences = detect_differences("Report within twelve hours.", "Report within six hours.")
    assert any(
        "duration" in item and "twelve hours" in item and "six hours" in item
        for item in differences
    )


def test_changed_rule_named_recipient_or_system():
    differences = detect_differences("Report to DNBS Central Office.", "Report on DAKSH.")
    assert any("dnbs central office" in item and "daksh" in item for item in differences)


def test_build_is_byte_deterministic():
    path = write_migration(REPO)
    first = path.read_bytes()
    path = write_migration(REPO)
    assert path.read_bytes() == first
    assert build_migration(REPO)["mappings"]


def test_scorer_numbers_equal_independent_recomputation():
    gold = json.loads((REPO / "benchmark/migrator_gold.json").read_text(encoding="utf-8"))
    proposal = json.loads(
        (REPO / f"data/migrations/{MIGRATION_ID}.json").read_text(encoding="utf-8")
    )
    result = score(gold, proposal)
    by_clause = {item["old_clause"]: item for item in proposal["mappings"]}
    hits = sum(
        (
            bool(by_clause[item["old_clause"]]["candidates"])
            and by_clause[item["old_clause"]]["candidates"][0]["paragraph"] in item["paragraphs"]
            if item["paragraphs"]
            else by_clause[item["old_clause"]]["status"] == "obsolete_no_successor"
        )
        for item in gold
    )
    statuses = sum(by_clause[item["old_clause"]]["status"] == item["status"] for item in gold)
    assert (result["hit_at_1"], result["status_correct"]) == (hits, statuses)
    assert result["hit_at_1_wilson_95"] == list(wilson(hits, 47))


def _api_data(tmp_path: Path, monkeypatch) -> Path:
    data = tmp_path / "data"
    migrations = data / "migrations"
    migrations.mkdir(parents=True)
    shutil.copy2(REPO / f"data/migrations/{MIGRATION_ID}.json", migrations / f"{MIGRATION_ID}.json")
    monkeypatch.setattr(api_module, "DATA_DIR", data)
    return data


def test_api_requires_named_person_and_confirmation_survives_rebuild(tmp_path, monkeypatch):
    data = _api_data(tmp_path, monkeypatch)
    client = TestClient(app)
    bad = client.post(f"/api/migrations/{MIGRATION_ID}/1/confirm", json={"reviewer": "agent"})
    assert bad.status_code == 422
    good = client.post(f"/api/migrations/{MIGRATION_ID}/1/confirm", json={"reviewer": "Asha Rao"})
    assert good.status_code == 200
    proposal_path = data / "migrations" / f"{MIGRATION_ID}.json"
    proposal_path.write_text(proposal_path.read_text(encoding="utf-8"), encoding="utf-8")
    page = client.get(f"/migrations/{MIGRATION_ID}")
    assert "confirmed by Asha Rao on" in page.text


def test_migration_page_escapes_excerpts(tmp_path, monkeypatch):
    data = _api_data(tmp_path, monkeypatch)
    path = data / "migrations" / f"{MIGRATION_ID}.json"
    proposal = json.loads(path.read_text(encoding="utf-8"))
    proposal["mappings"][0]["old_excerpt"] = "<script>alert(1)</script>"
    path.write_text(json.dumps(proposal), encoding="utf-8")
    page = TestClient(app).get(f"/migrations/{MIGRATION_ID}")
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in page.text
    assert "<script>alert(1)</script>" not in page.text
