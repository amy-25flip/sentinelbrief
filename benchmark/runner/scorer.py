"""Benchmark scorer for SentinelBrief.

Runs each scenario through the deterministic IncidentClockEngine and checks *everything* a
label asserts. A scenario passes only if all of these hold:
- the set of regulators matches;
- every expected deadline is produced at the same instant (timezone-aware comparison) from the
  same anchor, and no unexpected deadline is produced;
- every obligation listed under expected.citations is applicable;
- no obligation listed under expected.not_applicable is applicable;
- every expected unknown is asked, and no unexpected unknown is asked.

Citation *precision* (does a cited span support a generated claim) is not measured here: the
engine emits no generated claims. It will be added when LLM-drafted cards are benchmarked.

Usage: python benchmark/runner/scorer.py [--split dev|hidden] [--json] [--no-fail]
Exit status is 1 if any scenario fails, so CI can gate on regressions.
"""

import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path
from typing import Any

from sentinelbrief.clock.engine import IST, IncidentClockEngine, IncidentProfile

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if total == 0:
        return (0.0, 1.0)
    p_hat = successes / total
    denominator = 1 + z**2 / total
    centre = (p_hat + z**2 / (2 * total)) / denominator
    spread = z * math.sqrt(p_hat * (1 - p_hat) / total + z**2 / (4 * total**2)) / denominator
    return (max(0.0, centre - spread), min(1.0, centre + spread))


def _norm_reg(name: str) -> str:
    return "".join(c for c in name.upper() if c.isalnum())


def _parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError(f"scenario timestamp lacks a UTC offset: {value}")
    return parsed


class BenchmarkScorer:
    def __init__(self, data_dir: str | Path, scenarios_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.scenarios_dir = Path(scenarios_dir)
        self.engine = IncidentClockEngine(self.data_dir)
        self.scenarios: list[dict[str, Any]] = []
        if self.scenarios_dir.is_dir():
            for path in sorted(self.scenarios_dir.glob("*.json")):
                self.scenarios.append(json.loads(path.read_text(encoding="utf-8")))

    def _profile(self, scenario: dict[str, Any]) -> IncidentProfile:
        ep = scenario["entity_profile"]
        facts = scenario["incident_facts"]
        return IncidentProfile(
            entity_class=ep["entity_class"],
            is_listed=ep.get("is_listed"),
            holds_personal_data=ep.get("holds_personal_data"),
            uses_protected_systems=ep.get("uses_protected_systems"),
            is_regulated_cloud_vps=ep.get("is_regulated_cloud_vps"),
            incident_description=facts.get("description", ""),
            incident_types=facts.get("incident_types", []),
            annexure_i_items=facts.get("annexure_i_items", []),
            when_detected=_parse_dt(facts.get("when_detected")),
            when_noticed=_parse_dt(facts.get("when_noticed")),
            when_brought_to_notice=_parse_dt(facts.get("when_brought_to_notice")),
            when_occurred=_parse_dt(facts.get("when_occurred")),
            personal_data_involved=facts.get("personal_data_involved"),
            systems_affected=facts.get("systems_affected", []),
            is_annexure_i_type=facts.get("is_annexure_i_type"),
        )

    def evaluate_scenario(self, scenario: dict[str, Any]) -> dict[str, Any]:
        expected = scenario["expected"]
        # Fixed evaluation time keeps pending/overdue status deterministic across runs.
        now = datetime.fromisoformat(f"{scenario['law_snapshot_date']}T12:00:00+05:30")
        # law_snapshot_date pins the dataset version and the evaluation time. The law's as-of
        # date is NOT forced from it: the engine must derive it from the incident, and the
        # label asserts what it should be (expected.law_as_of).
        result = self.engine.evaluate(self._profile(scenario), now=now)
        failures: list[str] = []

        predicted_regs = {_norm_reg(d.regulator) for d in result.deadlines}
        for obl_id in result.applicable_obligations:
            obl = self.engine.get_obligation(obl_id) or {}
            issuer = self.engine._issuer.get(obl.get("instrument_id", ""), "")
            if issuer:
                predicted_regs.add(_norm_reg(issuer))
        expected_regs = {_norm_reg(r) for r in expected["regulators"]}
        if predicted_regs != expected_regs:
            failures.append(
                f"regulators: expected {sorted(expected_regs)}, got {sorted(predicted_regs)}"
            )

        if "law_as_of" in expected and result.law_as_of != date.fromisoformat(
            expected["law_as_of"]
        ):
            failures.append(
                f"law_as_of: expected {expected['law_as_of']}, got {result.law_as_of.isoformat()}"
            )

        by_obl = {d.obligation_id: d for d in result.deadlines}
        matched_deadlines = 0
        for exp in expected["deadlines"]:
            got = by_obl.get(exp["obligation_id"])
            if got is None:
                failures.append(f"missing deadline for {exp['obligation_id']}")
                continue
            exp_ts = datetime.fromisoformat(exp["deadline_timestamp"])
            if got.deadline_utc != exp_ts:
                failures.append(
                    f"deadline {exp['obligation_id']}: expected {exp_ts.astimezone(IST).isoformat()}, "
                    f"got {got.deadline_ist.isoformat()}"
                )
            elif got.anchor_type != exp["anchor"]:
                failures.append(
                    f"anchor {exp['obligation_id']}: expected {exp['anchor']}, got {got.anchor_type}"
                )
            else:
                matched_deadlines += 1
        expected_ids = {e["obligation_id"] for e in expected["deadlines"]}
        for spurious in sorted(set(by_obl) - expected_ids):
            failures.append(f"unexpected deadline produced for {spurious}")

        applicable = set(result.applicable_obligations)
        for cit in expected["citations"]:
            obl_id = cit["obligation_id"]
            if obl_id not in applicable:
                failures.append(f"should be applicable but is not: {obl_id}")
                continue
            obl = self.engine.get_obligation(obl_id) or {}
            if obl.get("instrument_id") != cit["instrument_id"]:
                failures.append(
                    f"citation instrument {obl_id}: expected {cit['instrument_id']}, "
                    f"got {obl.get('instrument_id')}"
                )
            if obl.get("paragraph_ref") != cit["paragraph_ref"]:
                failures.append(
                    f"citation paragraph {obl_id}: expected {cit['paragraph_ref']}, "
                    f"got {obl.get('paragraph_ref')}"
                )
        not_applicable = {item["obligation_id"]: item["reason"] for item in result.not_applicable}
        for na in expected["not_applicable"]:
            obl_id = na["obligation_id"]
            if obl_id in applicable:
                failures.append(f"should NOT be applicable but is: {obl_id}")
            elif obl_id not in not_applicable:
                failures.append(
                    f"expected not_applicable for {obl_id}, but the engine did not mark it so"
                )

        predicted_unknowns = {
            (obl_id, u.question.lower()) for u in result.unknowns for obl_id in u.affects
        }
        matched_unknowns: set[tuple[str, str]] = set()
        for exp_u in expected["unknowns"]:
            hits = {
                p
                for p in predicted_unknowns
                if p[0] == exp_u["affects"] and exp_u["question"].lower() in p[1]
            }
            if not hits:
                failures.append(
                    f"expected unknown not asked: {exp_u['question']} ({exp_u['affects']})"
                )
            matched_unknowns |= hits
        for extra in sorted(predicted_unknowns - matched_unknowns):
            failures.append(f"unexpected unknown asked: {extra[1]} ({extra[0]})")

        return {
            "id": scenario["id"],
            "passed": not failures,
            "failures": failures,
            "is_adversarial": bool(scenario.get("adversarial_flags")),
            "deadlines_expected": len(expected["deadlines"]),
            "deadlines_matched": matched_deadlines,
        }

    def run_all(self, split: str = "dev") -> dict[str, Any]:
        chosen = [s for s in self.scenarios if s.get("split", "dev") == split]
        results = [self.evaluate_scenario(s) for s in chosen]
        total = len(results)
        passed = sum(r["passed"] for r in results)
        adv = [r for r in results if r["is_adversarial"]]
        dl_total = sum(r["deadlines_expected"] for r in results)
        dl_ok = sum(r["deadlines_matched"] for r in results)
        return {
            "split": split,
            "total": total,
            "passed": passed,
            "scenario_wilson_ci": wilson_interval(passed, total),
            "deadlines_matched": dl_ok,
            "deadlines_expected": dl_total,
            "deadline_wilson_ci": wilson_interval(dl_ok, dl_total),
            "adversarial_total": len(adv),
            "adversarial_passed": sum(r["passed"] for r in adv),
            "results": results,
        }


def _print_report(report: dict[str, Any]) -> None:
    total, passed = report["total"], report["passed"]
    lo, hi = report["scenario_wilson_ci"]
    print("=" * 64)
    print(f"BENCHMARK RESULTS (split: {report['split']})")
    print("=" * 64)
    print(f"Scenarios passed:   {passed}/{total}  Wilson 95% CI [{lo:.1%}, {hi:.1%}]")
    dlo, dhi = report["deadline_wilson_ci"]
    print(
        f"Deadlines matched:  {report['deadlines_matched']}/{report['deadlines_expected']}  "
        f"Wilson 95% CI [{dlo:.1%}, {dhi:.1%}]"
    )
    print(f"Adversarial passed: {report['adversarial_passed']}/{report['adversarial_total']}")
    print("-" * 64)
    for r in report["results"]:
        tag = " [ADVERSARIAL]" if r["is_adversarial"] else ""
        print(f"  [{'PASS' if r['passed'] else 'FAIL'}] {r['id']}{tag}")
        for failure in r["failures"]:
            print(f"        - {failure}")
    print("=" * 64)
    print("Note: one instrument (CERT-In) is loaded, so regulator identification is trivial.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the SentinelBrief benchmark")
    parser.add_argument("--split", default="dev", choices=["dev", "hidden"])
    parser.add_argument("--json", action="store_true", help="print the report as JSON")
    parser.add_argument("--no-fail", action="store_true", help="always exit 0")
    args = parser.parse_args(argv)

    scorer = BenchmarkScorer(BASE_DIR / "data", BASE_DIR / "benchmark" / "scenarios")
    report = scorer.run_all(args.split)
    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        _print_report(report)
    if report["total"] == 0:
        print("ERROR: no scenarios found for this split", file=sys.stderr)
        return 1
    return 0 if args.no_fail or report["passed"] == report["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
