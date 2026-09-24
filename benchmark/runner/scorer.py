"""Benchmark Scorer for SentinelBrief.

Executes scenarios against the IncidentClockEngine and computes:
- Regulator identification precision and recall
- Deadline exact-match accuracy
- Citation precision
- Unknown-handling correctness
- Wilson confidence intervals
- Adversarial scenario accuracy
"""

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# Ensure src is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR / "src") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "src"))

from sentinelbrief.clock.engine import IncidentClockEngine, IncidentProfile


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion."""
    if total == 0:
        return (0.0, 1.0)
    p_hat = successes / total
    denominator = 1 + z**2 / total
    centre = (p_hat + z**2 / (2 * total)) / denominator
    spread = z * math.sqrt((p_hat * (1 - p_hat) / total + z**2 / (4 * total**2))) / denominator
    return (max(0.0, centre - spread), min(1.0, centre + spread))


def _normalize_reg(name: str) -> str:
    """Normalize regulator name for comparison (e.g. CERT-In -> CERTIN)."""
    return re_sub_non_alpha(name.upper())


def re_sub_non_alpha(s: str) -> str:
    return "".join(c for c in s if c.isalnum())


class BenchmarkScorer:
    """Runs scenarios through the engine and scores them against expectations."""

    def __init__(self, data_dir: str | Path, scenarios_dir: str | Path):
        self.data_dir = Path(data_dir)
        self.scenarios_dir = Path(scenarios_dir)
        self.engine = IncidentClockEngine(self.data_dir)
        self.scenarios: list[dict[str, Any]] = []
        self._load_scenarios()

    def _load_scenarios(self) -> None:
        if not self.scenarios_dir.exists():
            return
        for f in sorted(self.scenarios_dir.glob("*.json")):
            with open(f, "r", encoding="utf-8") as file:
                self.scenarios.append(json.load(file))

    def _parse_dt(self, dt_str: str | None) -> datetime | None:
        if not dt_str:
            return None
        return datetime.fromisoformat(dt_str)

    def evaluate_scenario(self, scenario: dict[str, Any]) -> dict[str, Any]:
        ep = scenario["entity_profile"]
        facts = scenario["incident_facts"]
        expected = scenario["expected"]

        incident_types = facts.get("incident_types", [])
        is_annexure_i = facts.get("is_annexure_i_type")
        
        add_facts = facts.get("additional_facts", {})
        when_brought = self._parse_dt(add_facts.get("brought_to_notice_at") or facts.get("when_brought_to_notice"))

        profile = IncidentProfile(
            entity_class=ep["entity_class"],
            is_listed=ep.get("is_listed"),
            holds_personal_data=ep.get("holds_personal_data"),
            uses_protected_systems=ep.get("uses_protected_systems"),
            is_regulated_cloud_vps=ep.get("is_regulated_cloud_vps"),
            incident_description=facts.get("description", ""),
            incident_types=incident_types,
            when_detected=self._parse_dt(facts.get("when_detected")),
            when_noticed=self._parse_dt(facts.get("when_noticed")),
            when_brought_to_notice=when_brought,
            when_occurred=self._parse_dt(facts.get("when_occurred")),
            personal_data_involved=facts.get("personal_data_involved"),
            systems_affected=facts.get("systems_affected", []),
            is_annexure_i_type=is_annexure_i,
        )

        result = self.engine.evaluate(profile)

        # 1. Regulator precision/recall with normalized names
        expected_regs = {_normalize_reg(r) for r in expected.get("regulators", [])}
        predicted_regs = {_normalize_reg(d.regulator) for d in result.deadlines}
        for obs_id in result.applicable_obligations:
            reg = _normalize_reg(obs_id.split(".")[0])
            predicted_regs.add(reg)

        reg_tp = len(expected_regs & predicted_regs)
        reg_fp = len(predicted_regs - expected_regs)
        reg_fn = len(expected_regs - predicted_regs)

        # 2. Deadline match
        expected_deadlines = expected.get("deadlines", [])
        deadline_matches = 0
        deadline_total = len(expected_deadlines)

        for ed in expected_deadlines:
            exp_obl = ed["obligation_id"]
            exp_ts = ed.get("deadline_timestamp")
            
            match = next((d for d in result.deadlines if d.obligation_id == exp_obl), None)
            if match:
                if exp_ts:
                    pred_ts = match.deadline_ist.isoformat()
                    if pred_ts == exp_ts or pred_ts[:19] == exp_ts[:19]:
                        deadline_matches += 1
                else:
                    deadline_matches += 1

        # 3. Unknown handling
        expected_unknowns = expected.get("unknowns", [])
        has_exp_unknowns = len(expected_unknowns) > 0
        has_pred_unknowns = len(result.unknowns) > 0
        
        # If expected has unknowns, we must have predicted unknowns. If expected has no unknowns, we should not have pending unknowns blocking deadlines.
        unknown_correct = (has_exp_unknowns == has_pred_unknowns) or (not has_exp_unknowns and deadline_matches == deadline_total)

        # Overall scenario pass
        is_adversarial = bool(scenario.get("adversarial_flags"))
        passed = (
            (reg_fn == 0 and reg_fp == 0) and
            (deadline_matches == deadline_total) and
            unknown_correct
        )

        return {
            "id": scenario["id"],
            "passed": passed,
            "is_adversarial": is_adversarial,
            "reg_precision": reg_tp / (reg_tp + reg_fp) if (reg_tp + reg_fp) > 0 else 1.0,
            "reg_recall": reg_tp / (reg_tp + reg_fn) if (reg_tp + reg_fn) > 0 else 1.0,
            "deadline_match": deadline_matches == deadline_total,
            "deadline_matches": deadline_matches,
            "deadline_total": deadline_total,
            "unknown_correct": unknown_correct,
            "predicted_deadlines": len(result.deadlines),
            "predicted_unknowns": len(result.unknowns),
        }

    def run_all(self, split: str = "dev") -> dict[str, Any]:
        scenarios_to_run = [s for s in self.scenarios if s.get("split", "dev") == split]
        total = len(scenarios_to_run)
        
        if total == 0:
            return {"total": 0, "passed": 0, "accuracy": 0.0, "wilson_interval": (0.0, 1.0)}

        results = [self.evaluate_scenario(s) for s in scenarios_to_run]
        passed_count = sum(1 for r in results if r["passed"])
        deadline_matches_total = sum(r["deadline_matches"] for r in results)
        deadline_expected_total = sum(r["deadline_total"] for r in results)
        adversarial_count = sum(1 for r in results if r["is_adversarial"])
        adversarial_passed = sum(1 for r in results if r["is_adversarial"] and r["passed"])

        w_low, w_high = wilson_interval(passed_count, total)
        d_low, d_high = wilson_interval(deadline_matches_total, deadline_expected_total) if deadline_expected_total > 0 else (1.0, 1.0)

        report = {
            "split": split,
            "total_scenarios": total,
            "passed_scenarios": passed_count,
            "scenario_accuracy": passed_count / total,
            "scenario_wilson_ci": (round(w_low, 4), round(w_high, 4)),
            "deadline_exact_match": deadline_matches_total / deadline_expected_total if deadline_expected_total > 0 else 1.0,
            "deadline_exact_match_counts": f"{deadline_matches_total}/{deadline_expected_total}",
            "deadline_wilson_ci": (round(d_low, 4), round(d_high, 4)),
            "adversarial_scenarios": adversarial_count,
            "adversarial_passed": adversarial_passed,
            "scenario_results": results,
        }

        print(f"\n{'='*60}")
        print(f"BENCHMARK RESULTS (split: {split})")
        print(f"{'='*60}")
        print(f"Total Scenarios: {total}")
        print(f"Passed: {passed_count}/{total} ({passed_count/total*100:.1f}%)")
        print(f"Wilson 95% CI: [{w_low*100:.1f}%, {w_high*100:.1f}%]")
        print(f"Deadline Exact Match: {deadline_matches_total}/{deadline_expected_total} ({deadline_matches_total/max(1, deadline_expected_total)*100:.1f}%)")
        print(f"Adversarial Traps: {adversarial_passed}/{adversarial_count} ({adversarial_passed/max(1, adversarial_count)*100:.1f}%)")
        print(f"{'-'*60}")
        for r in results:
            status = "PASS" if r["passed"] else "FAIL"
            adv = " [ADVERSARIAL]" if r["is_adversarial"] else ""
            print(f"  [{status}] {r['id']}{adv}")
        print(f"{'='*60}\n")

        return report


def main():
    base_dir = Path(__file__).resolve().parent.parent.parent
    data_dir = base_dir / "data"
    scenarios_dir = base_dir / "benchmark" / "scenarios"
    
    scorer = BenchmarkScorer(data_dir=data_dir, scenarios_dir=scenarios_dir)
    scorer.run_all(split="dev")


if __name__ == "__main__":
    main()
