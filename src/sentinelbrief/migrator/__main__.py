from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

from sentinelbrief.migrator.core import write_all_migrations


def main() -> None:
    parser = argparse.ArgumentParser(description="Build or score deterministic migration proposals")
    parser.add_argument("command", choices=("build", "score"))
    args = parser.parse_args()
    base = Path(__file__).resolve().parents[3]
    if args.command == "build":
        for path in write_all_migrations(base):
            print(path)
    else:
        scorer_path = base / "benchmark" / "runner" / "migrator_scorer.py"
        spec = importlib.util.spec_from_file_location("migrator_scorer", scorer_path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"could not load scorer from {scorer_path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules["migrator_scorer"] = module
        spec.loader.exec_module(module)
        module.main([])


if __name__ == "__main__":
    main()
