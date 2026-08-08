#!/usr/bin/env python3
"""Flag environment-specific facts written as if they were universal rules.

Root cause this closes: INCIDENT_LOG.md "environment-specific facts written
into AI-agnostic canonical agent files (2026-08-07)". That incident's actual
trigger phrase was "always prohibited: image generation" written into a
canonical agents/*.md draft, reasoning from this session's connected
connectors rather than the role itself.

This is a heuristic phrase-pattern check, not general semantic
understanding: it catches known absolute-prohibition/absolute-availability
phrasing, not every possible way environment-specific reasoning could leak
into canonical text. Stated honestly rather than implied to be complete.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CANONICAL_GLOBS = ("agents/*.md",)

ABSOLUTE_MARKERS = (
    r"常に禁止",
    r"常に不可",
    r"常に利用可能",
    r"\balways prohibited\b",
    r"\balways available\b",
    r"\bnever available\b",
)

ENVIRONMENT_NAMES = (
    "Claude Code", "ChatGPT", "Codex", "Gemini", "GitHub Copilot", "Copilot",
    "Figma", "Slack", "Notion", "Linear",
)


def scan_text(text: str, path: str) -> list[str]:
    findings = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        for marker_pattern in ABSOLUTE_MARKERS:
            if re.search(marker_pattern, line, re.IGNORECASE):
                findings.append(
                    f"{path}:{line_no}: absolute-availability phrasing "
                    f"({marker_pattern!r}) in a canonical file — confirm this "
                    f"is true of the role itself, not this session's current "
                    f"connectors, and cite the environment-adapter file if it "
                    f"is environment-specific: {line.strip()!r}"
                )
        for env_name in ENVIRONMENT_NAMES:
            if env_name in line and any(
                re.search(marker_pattern, line, re.IGNORECASE) for marker_pattern in ABSOLUTE_MARKERS
            ):
                findings.append(
                    f"{path}:{line_no}: environment name '{env_name}' combined "
                    f"with absolute phrasing in a canonical file: {line.strip()!r}"
                )
    return findings


def resolve_targets(root: Path, explicit_paths: list[Path]) -> list[Path]:
    if explicit_paths:
        return explicit_paths
    targets: list[Path] = []
    for pattern in CANONICAL_GLOBS:
        targets.extend(sorted(root.glob(pattern)))
    return targets


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", type=Path, nargs="*",
                         help="Specific files to check; defaults to agents/*.md under --root.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    targets = resolve_targets(args.root, args.paths)
    all_findings: list[str] = []
    for target in targets:
        if not target.exists():
            continue
        text = target.read_text(encoding="utf-8")
        rel = str(target.relative_to(args.root)) if target.is_absolute() else str(target)
        all_findings.extend(scan_text(text, rel))

    if all_findings:
        print("CANONICAL ENVIRONMENT NEUTRALITY: FAIL")
        for item in all_findings:
            print(f"- {item}")
        return 1
    print("CANONICAL ENVIRONMENT NEUTRALITY: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
