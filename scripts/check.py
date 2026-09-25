"""Run every quality gate exactly as CI does and print one summary.

Usage: uv run python scripts/check.py

All gates always run (a failure does not hide later ones). Exit status is 1 if any gate fails.
Paste this script's summary output into HANDOFF.md; do not summarise it from memory.
"""

import re
import subprocess
import sys
import time

GATES: list[tuple[str, list[str]]] = [
    ("pytest", ["uv", "run", "pytest", "-q"]),
    ("ruff check", ["uv", "run", "ruff", "check", "src/", "tests/", "benchmark/", "scripts/"]),
    (
        "ruff format",
        ["uv", "run", "ruff", "format", "--check", "src/", "tests/", "benchmark/", "scripts/"],
    ),
    ("mypy (strict)", ["uv", "run", "mypy", "src/sentinelbrief/"]),
    ("validate_all", ["uv", "run", "python", "-m", "sentinelbrief.verify.validate_all"]),
    ("benchmark dev", ["uv", "run", "python", "benchmark/runner/scorer.py", "--split", "dev"]),
]

_HEADLINE = re.compile(
    r"(\d+ passed.*|All checks passed!|\d+ files already formatted|Success: no issues.*"
    r"|All obligations and citations passed.*|Scenarios passed:.*)"
)


def main() -> int:
    results: list[tuple[str, bool, str, float]] = []
    for name, command in GATES:
        start = time.time()
        proc = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")
        elapsed = time.time() - start
        output = (proc.stdout or "") + (proc.stderr or "")
        headline = next(
            (m.group(1) for line in reversed(output.splitlines()) if (m := _HEADLINE.search(line))),
            output.strip().splitlines()[-1] if output.strip() else "(no output)",
        )
        results.append((name, proc.returncode == 0, headline.strip(), elapsed))
        if proc.returncode != 0:
            print(f"--- {name} FAILED ---\n{output[-3000:]}\n")

    print("=" * 78)
    print("GATE SUMMARY")
    print("=" * 78)
    for name, ok, headline, elapsed in results:
        print(f"{'PASS' if ok else 'FAIL':4s}  {name:16s} {elapsed:5.1f}s  {headline}")
    failed = [name for name, ok, _, _ in results if not ok]
    print("=" * 78)
    print("ALL GATES PASSED" if not failed else f"FAILED: {', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
