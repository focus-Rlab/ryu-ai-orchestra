"""Shared constants and helpers for the handoff contract checker.

REQ-B0: all string *comparisons* (identifier matching, target equality,
run_id duplicate detection, path matching, etc.) are performed on a
normalized value (leading/trailing whitespace stripped only; case is
preserved and remains significant). Normalization is used strictly
inside comparison logic. The original (raw) values read from the JSON
artifacts are never rewritten, and every report / message must echo the
raw value exactly as it appeared in the source JSON.
"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

RUN_ID_PATTERN = re.compile(r"^run-\d{3}$")
AC_ID_PATTERN = re.compile(r"^AC-\d+$")
OPEN_ID_PATTERN = re.compile(r"^OPEN-\d+$")
EVID_ID_PATTERN = re.compile(r"^EVID-\d+$")

SCHEMA_VERSION_ALLOWED = ["1.0"]

ARTIFACT_TYPES = ("requirements", "implementation", "evaluation")


def norm(value: Any) -> Any:
    """Normalize a value for comparison purposes only (REQ-B0).

    Only strings are affected (surrounding whitespace stripped). Any
    other type is returned unchanged. This function must never be used
    to mutate values that will be echoed back in a report/message.
    """
    if isinstance(value, str):
        return value.strip()
    return value


def is_str(value: Any) -> bool:
    return isinstance(value, str)


def is_non_empty_str(value: Any) -> bool:
    return isinstance(value, str) and value != ""


def is_bool(value: Any) -> bool:
    # bool is a subclass of int in Python; be explicit.
    return isinstance(value, bool)


def is_list(value: Any) -> bool:
    return isinstance(value, list)


def is_dict(value: Any) -> bool:
    return isinstance(value, dict)


def make_finding(
    check_id: str,
    artifact: str,
    field_path: str,
    message: str,
    related_ids: Optional[List[str]] = None,
) -> Dict[str, Any]:
    return {
        "check_id": check_id,
        "artifact": artifact,
        "field_path": field_path,
        "related_ids": list(related_ids) if related_ids else [],
        "message": message,
    }


class FatalError(Exception):
    """Raised for REQ-C2 front-gate failures / CLI-level fatal errors.

    Any raise of this exception must result in: stderr output, no
    report generated, exit code 2 (REQ-C4).
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
