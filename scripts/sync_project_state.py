#!/usr/bin/env python3
"""Update explicit post-merge facts in the single state source."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

try:
    from scripts.check_project_state import project_digest
except ModuleNotFoundError:  # Support direct `python scripts/...` execution.
    from check_project_state import project_digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--merged-pr", required=True, type=int)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--status", required=True)
    parser.add_argument("--active-issue", required=True, type=int)
    parser.add_argument("--active-branch", required=True)
    parser.add_argument("--next-action", required=True)
    parser.add_argument("--evidence", required=True)
    parser.add_argument(
        "--paused-issue", type=int, default=None,
        help="Issue number paused in favor of the active work, if any.",
    )
    parser.add_argument(
        "--paused-note", default=None,
        help="What was completed and what remains on the paused issue, so it "
             "is not lost when active work switches away from it.",
    )
    parser.add_argument(
        "--clear-paused", action="store_true",
        help="Explicitly clear paused_issue/paused_note (resume completed).",
    )
    args = parser.parse_args()
    path = args.root / "PROJECT_STATE.json"
    state = json.loads(path.read_text(encoding="utf-8"))
    state.update({
        "phase": args.phase,
        "status": args.status,
        "latest_merged_pr": args.merged_pr,
        "schema_version": 2,
        "verified_project_digest": project_digest(args.root),
        "active_issue": args.active_issue,
        "active_branch": args.active_branch,
        "next_action": args.next_action,
        "verified_at": date.today().isoformat(),
        "evidence": args.evidence,
    })
    if args.clear_paused:
        state["paused_issue"] = None
        state["paused_note"] = None
    else:
        if args.paused_issue is not None:
            state["paused_issue"] = args.paused_issue
        if args.paused_note is not None:
            state["paused_note"] = args.paused_note
    state.pop("verified_main_commit", None)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")
    print(f"Updated {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
