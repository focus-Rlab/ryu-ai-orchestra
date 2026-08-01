#!/usr/bin/env python3
"""Offline consistency checks for the canonical project state."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

REQUIRED = {
    "schema_version", "phase", "status", "latest_merged_pr",
    "verified_project_digest", "active_issue", "active_branch",
    "next_action", "verified_at", "evidence",
}
REFERENCE_FILES = (
    "README.md", "PROJECT_HANDOFF.md", "ROADMAP.md", "STARTUP_CONTEXT.md",
)

EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache"}
EXCLUDED_FILES = {"PROJECT_STATE.json"}


def project_digest(root: Path) -> str:
    """Hash project content without the state file that stores the hash."""
    try:
        result = subprocess.run(
            ["git", "ls-files", "-z"], cwd=root, check=True,
            capture_output=True,
        )
        paths = [root / item.decode() for item in result.stdout.split(b"\0") if item]
    except (OSError, subprocess.CalledProcessError):
        paths = [path for path in root.rglob("*") if path.is_file()]

    digest = hashlib.sha256()
    for path in sorted(paths, key=lambda item: item.relative_to(root).as_posix()):
        relative = path.relative_to(root)
        if relative.name in EXCLUDED_FILES:
            continue
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        digest.update(relative.as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"
FORBIDDEN_PATTERNS = (
    re.compile(r"Current working branch:", re.I),
    re.compile(r"現在の作業先:"),
    re.compile(r"main最新確認済みマージ:"),
    re.compile(r"Status:\s*PR\s*#\d+", re.I),
)


def validate(root: Path, expected_digest: str | None = None,
             expected_pr: int | None = None) -> list[str]:
    errors: list[str] = []
    state_path = root / "PROJECT_STATE.json"
    try:
        state = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"PROJECT_STATE.json cannot be read: {exc}"]
    missing = REQUIRED - state.keys()
    if missing:
        errors.append(f"missing state fields: {sorted(missing)}")
    if not isinstance(state.get("latest_merged_pr"), int):
        errors.append("latest_merged_pr must be an integer")
    actual_digest = expected_digest or project_digest(root)
    if state.get("verified_project_digest") != actual_digest:
        errors.append("verified_project_digest does not match project content")
    if expected_pr is not None and state.get("latest_merged_pr") != expected_pr:
        errors.append("latest_merged_pr does not match supplied merged PR")

    for name in REFERENCE_FILES:
        path = root / name
        if not path.exists():
            errors.append(f"missing reference file: {name}")
            continue
        text = path.read_text(encoding="utf-8")
        if "PROJECT_STATE.json" not in text:
            errors.append(f"{name} does not reference PROJECT_STATE.json")
        for pattern in FORBIDDEN_PATTERNS:
            if pattern.search(text):
                errors.append(
                    f"{name} duplicates mutable state: {pattern.pattern}"
                )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--expected-digest")
    parser.add_argument("--expected-pr", type=int)
    args = parser.parse_args()
    errors = validate(args.root, args.expected_digest, args.expected_pr)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    print("Project state consistency: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
