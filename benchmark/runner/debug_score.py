"""Debug scenario scoring."""
from benchmark.runner.scorer import BenchmarkScorer

scorer = BenchmarkScorer("data", "benchmark/scenarios")
for s in scorer.scenarios:
    res = scorer.evaluate_scenario(s)
    print(f"{s['id']}:")
    print(f"  passed: {res['passed']}")
    print(f"  reg_precision: {res['reg_precision']}, reg_recall: {res['reg_recall']}")
    print(f"  deadline_match: {res['deadline_match']} ({res['deadline_matches']}/{res['deadline_total']})")
    print(f"  unknown_correct: {res['unknown_correct']}")
    print(f"  predicted_deadlines: {res['predicted_deadlines']}")
    print(f"  predicted_unknowns: {res['predicted_unknowns']}")
