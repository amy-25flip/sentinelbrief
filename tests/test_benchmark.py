"""The benchmark must pass on the real engine AND fail when the engine regresses."""

import importlib.util
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


def test_hidden_split_with_no_scenarios_is_an_error():
    assert scorer.main(["--split", "hidden"]) == 1


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

    def buggy(self, obs, profile, now, deadlines, unknowns):
        if obs["id"].endswith("incident-reporting-6h"):
            spec = obs["normalized"]["deadline"]
            obs = {**obs, "normalized": {**obs["normalized"], "deadline": {**spec, **change}}}
        return original(self, obs, profile, now, deadlines, unknowns)

    monkeypatch.setattr(engine_module.IncidentClockEngine, "_compute_deadline", buggy)
    assert expected_failure in _failed(_run())


def test_catches_retention_treated_as_a_deadline(monkeypatch):
    original = engine_module.IncidentClockEngine._compute_deadline

    def buggy(self, obs, profile, now, deadlines, unknowns):
        if obs["id"].endswith("log-retention-180d"):
            spec = obs["normalized"]["deadline"]
            deadline = {**spec, "kind": "relative", "anchor": "noticing"}
            obs = {**obs, "normalized": {**obs["normalized"], "deadline": deadline}}
        return original(self, obs, profile, now, deadlines, unknowns)

    monkeypatch.setattr(engine_module.IncidentClockEngine, "_compute_deadline", buggy)
    assert "cert-in-retention-is-not-a-deadline" in _failed(_run())
