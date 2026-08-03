#!/usr/bin/env python3
"""Fail closed when a planned action has not been tied back to applicable rules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


COMMON_FIELDS = {
    "task",
    "action",
    "canonical_files_read",
    "applicable_rules",
    "assignment_decision",
    "required_checks",
    "stop_conditions",
}

INCIDENT_STEPS = {
    "classify",
    "root_cause",
    "impact_scope",
    "similar_case_audit",
    "generalized_prevention",
    "success_test",
    "failure_test",
    "independent_review_decision",
    "approval_boundary",
    "canonical_updates",
    "similar_but_not_identical_retest",
    "incident_record",
}


def validate(record: dict) -> list[str]:
    errors: list[str] = []
    missing = sorted(COMMON_FIELDS - record.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    for field in ("canonical_files_read", "applicable_rules", "required_checks", "stop_conditions"):
        if field in record and not isinstance(record[field], list):
            errors.append(f"{field} must be a list")
        elif field in record and not record[field]:
            errors.append(f"{field} must not be empty")

    assignment = record.get("assignment_decision")
    if not isinstance(assignment, dict):
        errors.append("assignment_decision must be an object")
    else:
        if not isinstance(assignment.get("use_agents"), bool):
            errors.append("assignment_decision.use_agents must be true or false")
        if not assignment.get("rationale"):
            errors.append("assignment_decision.rationale is required")
        if assignment.get("use_agents") and not assignment.get("assignments"):
            errors.append("agent assignments are required when use_agents is true")
        if assignment.get("use_agents") and not assignment.get("execution_evidence"):
            errors.append("agent execution evidence is required when use_agents is true")

    if record.get("action_type") in {"completion_claim", "incident_close"}:
        completion = record.get("completion_evidence")
        if not isinstance(completion, dict):
            errors.append("completion_evidence must be an object for completion claims")
        else:
            if not completion.get("verified"):
                errors.append("completion evidence must include verified checks")
            if "unverified_scope" not in completion:
                errors.append("completion evidence must state unverified_scope")

    if record.get("action_type") in {"incident_response", "incident_close"}:
        steps = set(record.get("incident_steps", []))
        missing_steps = sorted(INCIDENT_STEPS - steps)
        if missing_steps:
            errors.append(f"incident steps missing: {', '.join(missing_steps)}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    errors = validate(record)
    if errors:
        print("ACTION GATE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ACTION GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
