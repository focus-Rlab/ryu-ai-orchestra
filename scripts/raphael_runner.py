#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from v1_core.runner import RaphaelRunner


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Raphael task completion runner")
    command.add_argument("--run-directory", default=".raphael/runs")
    subcommands = command.add_subparsers(dest="command", required=True)

    start = subcommands.add_parser("start")
    start.add_argument("objective")
    start.add_argument("--task-type", choices=("general", "visual"), default="general")

    finish = subcommands.add_parser("finish")
    finish.add_argument("task_id")
    finish.add_argument("--evidence", required=True, help="JSON object")
    return command


def main() -> int:
    args = parser().parse_args()
    runner = RaphaelRunner(args.run_directory)
    if args.command == "start":
        contract = runner.start(args.objective, task_type=args.task_type)
        print(json.dumps({"contract": contract.__dict__}, ensure_ascii=False, indent=2))
        return 0

    try:
        evidence = json.loads(args.evidence)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"invalid evidence JSON: {exc}"}))
        return 2
    if not isinstance(evidence, dict):
        print(json.dumps({"error": "evidence must be a JSON object"}))
        return 2

    decision = runner.finish(args.task_id, evidence)
    print(json.dumps(decision.__dict__, ensure_ascii=False, indent=2))
    return 0 if decision.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
