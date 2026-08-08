#!/usr/bin/env python3
"""Flag glossary terms used without a nearby explanation marker.

This checks a mechanically detectable proxy (an explanation marker near the
term), not whether the explanation is actually good. It only catches terms
already registered in docs/COMMUNICATION_GLOSSARY.json; it cannot detect
unregistered jargon. Both limits are intentional and stated here rather than
implied to be complete, per INCIDENT_LOG.md's "residual open gap, stated
honestly" standard.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_GLOSSARY = Path(__file__).resolve().parents[1] / "docs" / "COMMUNICATION_GLOSSARY.json"

# A term counts as explained if, within this many characters after the term,
# there is an opening paren/bracket (a gloss) or one of these defining
# phrases. This is a proxy for "was some explanation attempted nearby", not a
# correctness check on the explanation's content.
EXPLANATION_WINDOW = 40
DEFINING_PHRASES = ("とは", "を意味する", "の略", "= ", "とは、", "つまり", "(", "（")


def load_glossary(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["terms"]


def find_unexplained(text: str, terms: list[dict]) -> list[dict]:
    findings = []
    for entry in terms:
        term = entry["term"]
        for match in re.finditer(re.escape(term), text):
            window = text[match.end():match.end() + EXPLANATION_WINDOW]
            if not any(phrase in window for phrase in DEFINING_PHRASES):
                findings.append({
                    "term": term,
                    "category": entry["category"],
                    "offset": match.start(),
                    "context": text[max(0, match.start() - 20):match.end() + 20],
                })
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("text_file", type=Path, nargs="?",
                         help="File to check; reads stdin if omitted.")
    parser.add_argument("--glossary", type=Path, default=DEFAULT_GLOSSARY)
    args = parser.parse_args()

    text = args.text_file.read_text(encoding="utf-8") if args.text_file else sys.stdin.read()
    terms = load_glossary(args.glossary)
    findings = find_unexplained(text, terms)

    if findings:
        print(f"COMMUNICATION GLOSSARY: {len(findings)} unexplained term(s) found")
        for item in findings:
            print(f"- '{item['term']}' ({item['category']}) near: ...{item['context']}...")
        return 1
    print("COMMUNICATION GLOSSARY: all registered terms explained or absent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
