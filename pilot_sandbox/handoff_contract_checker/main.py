#!/usr/bin/env python3
"""Entry point for the handoff contract checker CLI.

Usage:
    python3 main.py validate --type requirements --format text fixtures/requirements_valid.json
    python3 main.py check --requirements <f> --implementation <f> --evaluation <f> --format json

Python standard library only (REQ-C0).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from handoff_checker.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
