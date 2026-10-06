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


def test_every_configured_pair_segments_to_its_declared_size():
    """Catches: a pair whose old units or new paragraphs silently change count."""
    from sentinelbrief.migrator.core import PAIRS, build_migration

    for pair in PAIRS:
        built = build_migration(REPO, pair)
        assert len(built["mappings"]) == pair.old_units
        assert built["id"] == pair.id
        committed = json.loads(
            (REPO / "data" / "migrations" / f"{pair.id}.json").read_text(encoding="utf-8")
        )
        assert committed == built


def test_ucb_controls_carry_their_group_heading_and_exact_text():
    """Catches: a control cut at the wrong place or given another group's heading."""
    raw = REPO / "data" / "raw"
    stem = "RBI_UCB_Comprehensive_Cyber_Security_Framework_2019"
    text = (raw / f"{stem}.txt").read_text(encoding="utf-8")
    segments = {
        item["id"]: item
        for item in json.loads((raw / f"{stem}.meta.json").read_text(encoding="utf-8"))["segments"]
    }
    assert len(segments) == 61
    control = segments["II-8.1"]
    body = text[control["char_start"] : control["char_end"]]
    assert control["heading"] == "8. Anti-Phishing"
    assert body.startswith("8.1. Subscribe to Anti-phishing") and "9. Data Leak" not in body
    assert segments["IV-6.6"]["heading"] == "6. IT and IS Governance Framework"
    assert "Ref:" not in text[segments["IV-6.6"]["char_start"] : segments["IV-6.6"]["char_end"]]


def test_master_direction_clause_stops_before_the_next_chapter_heading():
    """Catches: a chapter heading swallowed into the clause before it."""
    raw = REPO / "data" / "raw"
    stem = "RBI_IT_Governance_Master_Direction_2023"
    text = (raw / f"{stem}.txt").read_text(encoding="utf-8")
    segments = json.loads((raw / f"{stem}.meta.json").read_text(encoding="utf-8"))["segments"]
    assert [item["id"] for item in segments] == [str(n) for n in range(4, 31)]
    for item in segments:
        assert "\nChapter " not in text[item["char_start"] : item["char_end"]]


def test_scorer_handles_gold_without_status():
    """Catches: a pair with paragraph-only gold counted as status failures."""
    result = _scorer.score_pair("rbi.ucb-cyber-framework.2019__rbi.ucb-cyber.2026")
    assert result["total"] == 61 and result["status_total"] == 0
    assert result["status_accuracy"] is None
    assert all(not miss["hit"] for miss in result["misses"])


def test_correction_is_bounded_by_the_new_directions_own_paragraph_count(tmp_path):
    """Catches: the 158-paragraph bound of the NBFC Direction applied to another Direction."""
    import shutil

    from sentinelbrief.migrator.review import ConfirmationStore

    shutil.copytree(REPO / "data" / "migrations", tmp_path / "migrations")
    store = ConfirmationStore(tmp_path)
    pair = "rbi.it-governance.2023__rbi.payments-banks-cyber.2026"
    record = store.correct(pair, "30", "Asha Rao", ["223"], "IS Audit chapter")
    assert record["paragraphs"] == ["223"]
    try:
        store.correct(pair, "30", "Asha Rao", ["233"], "beyond the last paragraph")
    except ValueError as exc:
        assert "1 to 232" in str(exc)
    else:
        raise AssertionError("paragraph 233 does not exist in the Payments Banks Direction")
