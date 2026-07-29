#!/usr/bin/env python3
"""Update explicit post-merge facts in the single state source."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--main-commit", required=True)
    parser.add_argument("--merged-pr", required=True, type=int)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--active-issue", required=True, type=int)
    parser.add_argument("--active-branch", required=True)
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--evidence", required=True)
    args = parser.parse_args()
    path = args.root / "PROJECT_STATE.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    state.update({
        "phase": args.phase,
        "status": args.status,
        "latest_merged_pr": args.merged_pr,
        "verified_main_commit": args.main_commit,
        "active_issue": args.active_issue,
        "active_branch": args.active_branch,
        "next_action": args.next_action,
        "verified_at": date.today().isoformat(),
        "evidence": args.evidence,
    })
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print(f"Updated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
