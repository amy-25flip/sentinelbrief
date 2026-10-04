"""The benchmark must pass on the real engine AND fail when the engine regresses."""

import copy
import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

from sentinelbrief.clock import engine as engine_module

REPO = Path(__file__).resolve().parents[1]


def _load_scorer():
    spec = importlib.util.spec_from_file_location(
        "scorer", REPO / "benchmark" / "runner" / "scorer.py"
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["scorer"] = module
    spec.loader.exec_module(module)
    return module


scorer = _load_scorer()


def _run():
    return scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios").run_all("dev")


def _failed(report):
    return {r["id"] for r in report["results"] if not r["passed"]}


def test_all_dev_scenarios_pass():
    report = _run()
    assert report["total"] >= 15
    assert _failed(report) == set(), [r for r in report["results"] if not r["passed"]]


def test_adversarial_cases_are_a_large_share():
    report = _run()
    assert report["adversarial_total"] >= report["total"] // 2


def test_every_scenario_label_names_its_source():
    for scenario in scorer.BenchmarkScorer(
        REPO / "data", REPO / "benchmark" / "scenarios"
    ).scenarios:
        assert scenario.get("labels_source")
        for na in scenario["expected"]["not_applicable"]:
            assert na["obligation_id"]


def test_every_dev_scenario_has_verified_source_quotes():
    bench = scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios")
    for scenario in bench.scenarios:
        assert scenario.get("source_quotes"), scenario["id"]
        scorer.verify_source_quotes(scenario, REPO / "data")


def test_source_quote_verifier_rejects_fabrication_and_wrong_page():
    bench = scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios")
    scenario = copy.deepcopy(bench.scenarios[0])
    scenario["source_quotes"][0]["quote"] = "fabricated legal words absent from the source"
    with pytest.raises(ValueError, match="not on PDF page"):
        scorer.verify_source_quotes(scenario, REPO / "data")
    scenario = copy.deepcopy(bench.scenarios[0])
    scenario["source_quotes"][0]["page"] = 9999
    with pytest.raises(ValueError, match="does not exist"):
        scorer.verify_source_quotes(scenario, REPO / "data")


def test_law_as_of_comes_from_the_incident_not_the_snapshot_date():
    """The snapshot date pins the dataset and evaluation time; the incident date picks the law."""
    bench = scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios")
    scenario = next(s for s in bench.scenarios if s["id"] == "cert-in-before-directions-effective")
    assert scenario["law_snapshot_date"] == "2026-09-24"
    assert scenario["expected"]["law_as_of"] == "2021-01-05"
    assert bench.evaluate_scenario(scenario)["failures"] == []


def test_wrong_law_as_of_label_is_flagged():
    bench = scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios")
    scenario = copy.deepcopy(next(s for s in bench.scenarios if s["id"] == "cert-in-utc-input"))
    scenario["expected"]["law_as_of"] = "2026-09-16"
    assert any("law_as_of" in f for f in bench.evaluate_scenario(scenario)["failures"])


def test_every_scenario_states_its_law_as_of():
    for scenario in scorer.BenchmarkScorer(
        REPO / "data", REPO / "benchmark" / "scenarios"
    ).scenarios:
        assert "law_as_of" in scenario["expected"], scenario["id"]


def test_catches_law_evaluated_as_of_today_instead_of_the_incident(monkeypatch):
    monkeypatch.setattr(engine_module.IncidentProfile, "earliest_known_time", lambda self: None)
    failed = _failed(_run())
    assert "cert-in-before-directions-effective" in failed
    assert len(failed) >= 10  # the law_as_of label is wrong for almost every scenario


def test_scorer_checks_citation_labels():
    bench = scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios")
    scenario = copy.deepcopy(
        next(s for s in bench.scenarios if s["id"] == "cert-in-nbfc-ransomware")
    )
    scenario["expected"]["citations"][0]["paragraph_ref"] = "Direction (wrong)"

    failures = bench.evaluate_scenario(scenario)["failures"]

    assert any("citation paragraph" in failure for failure in failures)


def test_scorer_distinguishes_not_applicable_from_unknown():
    bench = scorer.BenchmarkScorer(REPO / "data", REPO / "benchmark" / "scenarios")
    scenario = copy.deepcopy(
        next(s for s in bench.scenarios if s["id"] == "cert-in-non-annexure-i-type")
    )
    scenario["incident_facts"]["is_annexure_i_type"] = None

    failures = bench.evaluate_scenario(scenario)["failures"]

    assert any("expected not_applicable" in failure for failure in failures)


def test_wilson_interval_bounds():
    lo, hi = scorer.wilson_interval(17, 17)
    assert 0.8 < lo < 0.85 and hi == 1.0
    assert scorer.wilson_interval(0, 0) == (0.0, 1.0)
    lo, hi = scorer.wilson_interval(0, 10)
    assert lo == 0.0 and hi < 0.4


def test_cli_exits_nonzero_when_a_scenario_fails(monkeypatch):
    monkeypatch.setattr(
        engine_module.IncidentClockEngine,
        "_not_in_force_reason",
        staticmethod(lambda obs, as_of: None),
    )
    assert scorer.main(["--split", "dev"]) == 1
    assert scorer.main(["--split", "dev", "--no-fail"]) == 0


def test_hidden_split_with_no_scenarios_is_an_error(tmp_path):
    hidden = tmp_path / "hidden"
    hidden.mkdir()
    shutil.copytree(REPO / "data", tmp_path / "data")
    original_base_dir = scorer.BASE_DIR
    scorer.BASE_DIR = tmp_path
    try:
        assert scorer.main(["--split", "hidden"]) == 1
    finally:
        scorer.BASE_DIR = original_base_dir


# Each reintroduced bug must be caught by the scenarios written for it.


def test_catches_free_text_concluding_not_reportable(monkeypatch):
    original = engine_module.IncidentClockEngine.resolve_annexure_i

    def buggy(self, profile):
        result = original(self, profile)
        if result.decision is None:
            return engine_module.AnnexureResolution(False, "term_match", [], [])
        return result

    monkeypatch.setattr(engine_module.IncidentClockEngine, "resolve_annexure_i", buggy)
    assert {"cert-in-unattested-hardware-failure", "cert-in-cloud-outage-not-assumed"} <= _failed(
        _run()
    )


def test_catches_ignoring_validity_dates(monkeypatch):
    monkeypatch.setattr(
        engine_module.IncidentClockEngine,
        "_not_in_force_reason",
        staticmethod(lambda obs, as_of: None),
    )
    assert "cert-in-before-directions-effective" in _failed(_run())


@pytest.mark.parametrize(
    ("change", "expected_failure"),
    [
        ({"alternative_anchors": []}, "cert-in-brought-to-notice"),
        (
            {"alternative_anchors": ["brought_to_notice", "detection"]},
            "cert-in-detection-time-only",
        ),
    ],
)
def test_catches_wrong_anchor_handling(monkeypatch, change, expected_failure):
    original = engine_module.IncidentClockEngine._compute_deadline

    def buggy(self, obs, profile, now, deadlines, time_critical, unknowns):
        if obs["id"].endswith("incident-reporting-6h"):
            spec = obs["normalized"]["deadline"]
            obs = {**obs, "normalized": {**obs["normalized"], "deadline": {**spec, **change}}}
        return original(self, obs, profile, now, deadlines, time_critical, unknowns)

    monkeypatch.setattr(engine_module.IncidentClockEngine, "_compute_deadline", buggy)
    assert expected_failure in _failed(_run())


def test_catches_retention_treated_as_a_deadline(monkeypatch):
    original = engine_module.IncidentClockEngine._compute_deadline

    def buggy(self, obs, profile, now, deadlines, time_critical, unknowns):
        if obs["id"].endswith("log-retention-180d"):
            spec = obs["normalized"]["deadline"]
            deadline = {**spec, "kind": "relative", "anchor": "noticing"}
            obs = {**obs, "normalized": {**obs["normalized"], "deadline": deadline}}
        return original(self, obs, profile, now, deadlines, time_critical, unknowns)

    monkeypatch.setattr(engine_module.IncidentClockEngine, "_compute_deadline", buggy)
    assert "cert-in-retention-is-not-a-deadline" in _failed(_run())


def _mutate_loaded_obligations(monkeypatch, mutation):
    original = engine_module.IncidentClockEngine._load_obligations

    def changed(self):
        original(self)
        mutation(self.obligations)

    monkeypatch.setattr(engine_module.IncidentClockEngine, "_load_obligations", changed)


def test_catches_personal_data_gate_ignored(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].startswith("meity.dpdp-rules.2025.rule7"):
                item["applicability"]["requires"] = []

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "dpdp-no-personal-data" in _failed(_run())


def test_catches_awareness_swapped_for_occurrence(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].endswith("rule7-2-b-board-detailed"):
                item["normalized"]["deadline"]["anchor"] = "occurrence"

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "dpdp-awareness-later-than-occurrence" in _failed(_run())


def test_catches_dpdp_valid_from_ignored(monkeypatch):
    original = engine_module.IncidentClockEngine._not_in_force_reason

    def mutation(item, as_of):
        if item["id"].startswith("meity.dpdp-rules.2025.rule7"):
            return None
        return original(item, as_of)

    monkeypatch.setattr(
        engine_module.IncidentClockEngine, "_not_in_force_reason", staticmethod(mutation)
    )
    assert "dpdp-commencement-before-may-2027" in _failed(_run())


def test_catches_structured_requires_ignored(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].endswith("incident-reporting-6h"):
                item["applicability"]["requires"] = []

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert {"sebi-mii-hardware-failure-unattested", "sebi-mii-attested-not-annexure-i"} <= _failed(
        _run()
    )


def test_catches_sebi_entity_leak(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"] == "sebi.cscrf.2024.incident-reporting-6h":
                item["applicability"]["entity_classes"].append("bank")

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "sebi-non-sebi-entity-bank-trap" in _failed(_run())


def test_catches_rbi_refinement_rule_removed(monkeypatch):
    monkeypatch.setattr(
        engine_module.IncidentClockEngine,
        "_needs_entity_refinement",
        lambda self, profile_classes, target_classes: False,
    )
    assert "rbi-generic-nbfc-must-ask-category" in _failed(_run())


def test_catches_rbi_exclusions_ignored(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].startswith("rbi.nbfc-cyber.2026.ch5"):
                item["applicability"]["excluded_entity_classes"] = []

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "rbi-cic-in-middle-layer-excluded" in _failed(_run())


def test_catches_rbi_all_of_ignored(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].endswith("ch5-hfc-incident-reporting-nhb"):
                item["applicability"]["all_of_entity_classes"] = []

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "rbi-ml-ransomware" in _failed(_run())


def test_catches_rbi_cyber_incident_requirement_ignored(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].startswith("rbi.nbfc-cyber.2026"):
                item["applicability"]["requires"] = []

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "rbi-ml-hardware-failure-unattested" in _failed(_run())


def test_catches_rbi_detection_replaced_by_noticing(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].startswith("rbi.nbfc-cyber.2026"):
                deadline = item["normalized"]["deadline"]
                if deadline["kind"] == "relative":
                    deadline["anchor"] = "noticing"

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "rbi-detected-before-noticed" in _failed(_run())


def test_catches_rbi_valid_from_ignored(monkeypatch):
    original = engine_module.IncidentClockEngine._not_in_force_reason

    def mutation(item, as_of):
        if item["id"].startswith("rbi.nbfc-cyber.2026"):
            return None
        return original(item, as_of)

    monkeypatch.setattr(
        engine_module.IncidentClockEngine, "_not_in_force_reason", staticmethod(mutation)
    )
    assert "rbi-incident-before-commencement" in _failed(_run())


def test_catches_rbi_chapter_iv_leaking_to_chapter_iii(monkeypatch):
    def mutation(items):
        for item in items:
            if item["id"].endswith("ch4-incident-reporting-6h"):
                item["applicability"]["entity_classes"].append("nbfc.bl_below_500cr")

    _mutate_loaded_obligations(monkeypatch, mutation)
    assert "rbi-bl-below-500cr-no-reporting-duty" in _failed(_run())
