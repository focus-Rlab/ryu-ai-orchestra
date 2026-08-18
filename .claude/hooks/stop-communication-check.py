#!/usr/bin/env python3
"""Claude Code Stop hook: observe (do not block) unexplained glossary terms.

Honest status (do not overclaim, per INCIDENT_LOG.md's own standard): this
is stage 1, observe-only. It always exits 0 and never blocks a turn from
ending. It has not been verified against a live Claude Code Stop-hook
invocation in this session -- only against hand-built fixture stdin, since a
Stop hook cannot be made to fire on itself mid-session. The stdin/transcript
parsing is defensive (multiple reasonable schema shapes, fails silently to a
debug log) precisely because that contract has not been live-confirmed here.

This is deliberately narrower than "detect any previously-flagged rule not
applied" (the full request): it only covers unexplained glossary terms
(docs/COMMUNICATION_GLOSSARY.json). Broader detection (e.g. "was corrective
feedback's underlying principle actually addressed") is not mechanically
checkable by keyword matching and is not attempted here -- that residual gap
is stated openly rather than pretended solved, matching this repository's
existing "residual open gap" precedent in INCIDENT_LOG.md.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

LOG_PATH = ROOT / "evaluations" / "action-gates" / "communication_observations.jsonl"
DEBUG_LOG_PATH = ROOT / "evaluations" / "action-gates" / "communication_observations_debug.log"


def debug(message: str) -> None:
    DEBUG_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with DEBUG_LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")


def extract_text_from_content(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def last_assistant_text(transcript_path: str) -> str | None:
    path = Path(transcript_path)
    if not path.exists():
        debug(f"transcript not found: {transcript_path}")
        return None
    last_text = None
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                message = entry.get("message") if isinstance(entry, dict) else None
                role = None
                content = None
                if isinstance(message, dict):
                    role = message.get("role")
                    content = message.get("content")
                elif isinstance(entry, dict):
                    role = entry.get("role")
                    content = entry.get("content")
                if role == "assistant" and content is not None:
                    text = extract_text_from_content(content)
                    if text.strip():
                        last_text = text
    except OSError as exc:
        debug(f"failed reading transcript: {exc}")
        return None
    return last_text


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read())
    except json.JSONDecodeError as exc:
        debug(f"failed parsing stdin: {exc}")
        return 0

    transcript_path = payload.get("transcript_path")
    if not transcript_path:
        debug("no transcript_path in stdin payload")
        return 0

    text = last_assistant_text(transcript_path)
    if not text:
        debug("no assistant text extracted; skipping check")
        return 0

    try:
        from check_communication_glossary import find_unexplained, load_glossary
        glossary_path = ROOT / "docs" / "COMMUNICATION_GLOSSARY.json"
        findings = find_unexplained(text, load_glossary(glossary_path))
    except Exception as exc:  # observe-only: never let a checker bug block the turn
        debug(f"checker error: {exc!r}")
        return 0

    if findings:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "session_id": payload.get("session_id"),
            "findings": findings,
        }
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, ensure_ascii=False) + "\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
