"""Score deterministic migration proposals against the public 47-unit gold set."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if total == 0:
        return 0.0, 0.0
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = (proportion + z * z / (2 * total)) / denominator
    spread = (
        z
        * math.sqrt(proportion * (1 - proportion) / total + z * z / (4 * total * total))
        / denominator
    )
    return centre - spread, centre + spread


def score(gold: list[dict[str, Any]], proposal: dict[str, Any]) -> dict[str, Any]:
    proposed = {item["old_clause"]: item for item in proposal["mappings"]}
    hits = 0
    statuses = 0
    misses: list[dict[str, Any]] = []
    for expected in gold:
        actual = proposed.get(expected["old_clause"])
        top = actual["candidates"][0]["paragraph"] if actual and actual["candidates"] else None
        hit = actual is not None and (
            top in expected["paragraphs"]
            if expected["paragraphs"]
            else actual["status"] == "obsolete_no_successor"
        )
        status_ok = actual is not None and actual["status"] == expected["status"]
        hits += int(hit)
        statuses += int(status_ok)
        if not hit or not status_ok:
            misses.append(
                {
                    "old_clause": expected["old_clause"],
                    "expected_paragraphs": expected["paragraphs"],
                    "actual_top": top,
                    "expected_status": expected["status"],
                    "actual_status": actual["status"] if actual else None,
                    "hit": hit,
                    "status_correct": status_ok,
                }
            )
    total = len(gold)
    hit_interval = wilson(hits, total)
    status_interval = wilson(statuses, total)
    return {
        "total": total,
        "hit_at_1": hits,
        "hit_at_1_rate": hits / total,
        "hit_at_1_wilson_95": list(hit_interval),
        "status_correct": statuses,
        "status_accuracy": statuses / total,
        "status_wilson_95": list(status_interval),
        "misses": misses,
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)
    gold = json.loads((REPO / "benchmark" / "migrator_gold.json").read_text(encoding="utf-8"))
    proposal = json.loads(
        (
            REPO / "data" / "migrations" / "rbi.nbfc-it-framework.2017__rbi.nbfc-cyber.2026.json"
        ).read_text(encoding="utf-8")
    )
    result = score(gold, proposal)
    print(
        f"hit@1: {result['hit_at_1']}/{result['total']} ({result['hit_at_1_rate']:.1%}), "
        f"Wilson 95% CI [{result['hit_at_1_wilson_95'][0]:.1%}, {result['hit_at_1_wilson_95'][1]:.1%}]"
    )
    print(
        f"status accuracy: {result['status_correct']}/{result['total']} ({result['status_accuracy']:.1%}), "
        f"Wilson 95% CI [{result['status_wilson_95'][0]:.1%}, {result['status_wilson_95'][1]:.1%}]"
    )
    print("misses:")
    for miss in result["misses"]:
        print(json.dumps(miss, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
