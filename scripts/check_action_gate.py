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
    "mistake_detected",
    "classification_basis",
}

RULE_CATEGORIES = {"security", "authority", "quality", "user_communication", "state_sync", "delivery", "recovery", "agent_design"}

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

MISTAKE_ACTION_TYPES = {"mistake_response", "incident_response", "incident_close"}
MISTAKE_CLASSES = {"general", "repeated", "major"}
PATH_STATUSES = {"available", "unavailable", "not_authorized", "not_equivalent"}
REQUIRED_PATH_CLASSES = {"requested_tool", "configured_connector", "api", "local_vcs", "browser", "manual_handoff"}
EVIDENCE_TYPES = {"file", "test", "agent_report", "user_report", "tool_result", "pr"}
MISTAKE_TRIGGER_TYPES = {"user_report", "prior_action_invalid", "test_failure", "review_failure", "policy_violation"}


def valid_evidence(items) -> bool:
    if not isinstance(items, list) or not items:
        return False
    for item in items:
        if not isinstance(item, dict) or item.get("type") not in EVIDENCE_TYPES or not item.get("ref") or not item.get("result"):
            return False
        if item.get("type") == "file" and not Path(item["ref"]).exists():
            return False
    return True


def validate(record: dict, registry: dict | None = None) -> list[str]:
    errors: list[str] = []
    missing = sorted(COMMON_FIELDS - record.keys())
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")

    if not isinstance(record.get("mistake_detected"), bool):
        errors.append("mistake_detected must be true or false")
    if not record.get("classification_basis"):
        errors.append("classification_basis is required")

    triggers = record.get("mistake_triggers")
    if not isinstance(triggers, list) or not triggers:
        errors.append("mistake_triggers must be a non-empty list")
        triggers = []
    confirmed_trigger = False
    for trigger in triggers:
        if not isinstance(trigger, dict) or not trigger.get("type") or not valid_evidence(trigger.get("evidence")):
            errors.append("each mistake trigger requires type and structured evidence")
            continue
        if trigger.get("type") in MISTAKE_TRIGGER_TYPES:
            confirmed_trigger = True
        elif trigger.get("type") != "none":
            errors.append("mistake trigger type is invalid")
    if confirmed_trigger and record.get("mistake_detected") is not True:
        errors.append("confirmed mistake triggers require mistake_detected true")
    if record.get("mistake_detected") is True and not confirmed_trigger:
        errors.append("mistake_detected true requires a confirmed mistake trigger")

    for field in ("canonical_files_read", "applicable_rules", "required_checks", "stop_conditions"):
        if field in record and not isinstance(record[field], list):
            errors.append(f"{field} must be a list")
        elif field in record and not record[field]:
            errors.append(f"{field} must not be empty")

    enforce_v2 = record.get("gate_version", 1) >= 2
    coverage = record.get("rule_coverage")
    if not enforce_v2:
        coverage = [{"category": category, "status": "not_applicable", "reason": "legacy record"} for category in RULE_CATEGORIES]
    if not isinstance(coverage, list) or not coverage:
        errors.append("rule_coverage must be a non-empty list")
    else:
        seen = set()
        for item in coverage:
            if not isinstance(item, dict) or item.get("category") not in RULE_CATEGORIES:
                errors.append("rule coverage category is invalid")
                continue
            seen.add(item["category"])
            if item.get("status") not in {"applicable", "not_applicable"} or not item.get("reason"):
                errors.append("each rule coverage item requires status and reason")
            if item.get("status") == "applicable" and (not item.get("control") or not item.get("evidence")):
                errors.append("applicable rule coverage requires control and evidence")
        missing_categories = sorted(RULE_CATEGORIES - seen)
        if missing_categories:
            errors.append(f"rule coverage categories missing: {', '.join(missing_categories)}")

    handoff = record.get("deliverable_handoff") if enforce_v2 else {"required": False}
    if not isinstance(handoff, dict) or not isinstance(handoff.get("required"), bool):
        errors.append("deliverable_handoff must state whether handoff is required")
    elif handoff["required"]:
        if not handoff.get("medium") or not handoff.get("acceptance_check"):
            errors.append("required deliverable handoff needs a medium and acceptance check")
        if record.get("action_type") == "completion_claim" and not handoff.get("user_access_evidence"):
            errors.append("completion claim requires user-access evidence for deliverable handoff")

    feedback = record.get("feedback_capture") if enforce_v2 else {"reviewed": False}
    if not isinstance(feedback, dict) or not isinstance(feedback.get("reviewed"), bool):
        errors.append("feedback_capture must state whether user feedback was reviewed")
    elif feedback["reviewed"] and not feedback.get("classification"):
        errors.append("reviewed feedback requires a classification")

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

    if record.get("action_type") == "impossibility_claim":
        inventory = record.get("execution_path_inventory")
        if not isinstance(inventory, dict):
            errors.append("impossibility claims require an execution_path_inventory")
        else:
            if not inventory.get("scope_basis"):
                errors.append("execution path inventory requires a scope_basis")
            if inventory.get("inventory_complete") is not True:
                errors.append("execution path inventory must be explicitly complete")
            paths = inventory.get("paths")
            if not isinstance(paths, list) or not paths:
                errors.append("execution path inventory requires checked paths")
            else:
                classes = [path.get("class") for path in paths if isinstance(path, dict)]
                missing_classes = sorted(REQUIRED_PATH_CLASSES - set(classes))
                if missing_classes:
                    errors.append(f"execution path classes missing: {', '.join(missing_classes)}")
                for path in paths:
                    if not isinstance(path, dict):
                        errors.append("each execution path must be an object")
                        continue
                    if path.get("status") not in PATH_STATUSES:
                        errors.append("execution path status is invalid or unresolved")
                    if path.get("class") not in REQUIRED_PATH_CLASSES:
                        errors.append("execution path class is invalid")
                    if not path.get("path") or not path.get("reason") or not valid_evidence(path.get("evidence")):
                        errors.append("each execution path requires path, reason, and structured evidence")
                    if not isinstance(path.get("outcome_equivalent"), bool):
                        errors.append("each execution path must state outcome_equivalent")
                    if not isinstance(path.get("authorized"), bool):
                        errors.append("each execution path must state authorized")
                    if (
                        path.get("status") == "available"
                        and path.get("outcome_equivalent") is True
                        and path.get("authorized") is True
                    ):
                        errors.append("work cannot be called impossible while an authorized equivalent path is available")

    is_mistake = record.get("mistake_detected") is True
    if is_mistake and record.get("action_type") not in MISTAKE_ACTION_TYPES:
        errors.append("mistake_detected actions must use a mistake response action_type")
    if record.get("action_type") in MISTAKE_ACTION_TYPES and not is_mistake:
        errors.append("mistake response action_type requires mistake_detected true")

    if is_mistake:
        mistake = record.get("mistake")
        if not isinstance(mistake, dict):
            errors.append("mistake classification is required for mistake responses")
        else:
            classification = mistake.get("classification")
            occurrence_count = mistake.get("occurrence_count")
            root_cause_id = mistake.get("root_cause_id")
            prior_refs = mistake.get("prior_mistake_refs")
            if classification not in MISTAKE_CLASSES:
                errors.append("mistake.classification must be general, repeated, or major")
            if not isinstance(occurrence_count, int) or occurrence_count < 1:
                errors.append("mistake.occurrence_count must be a positive integer")
            elif occurrence_count >= 2 and classification == "general":
                errors.append("a repeated mistake cannot remain classified as general")
            if not root_cause_id:
                errors.append("mistake.root_cause_id is required")
            if occurrence_count and occurrence_count >= 2 and not prior_refs:
                errors.append("repeated mistakes require prior_mistake_refs")
            if occurrence_count and occurrence_count >= 2 and isinstance(prior_refs, list):
                known = (registry or {}).get("incidents", {})
                covered_occurrences = 0
                for prior in prior_refs:
                    if not isinstance(prior, dict) or not prior.get("incident_id"):
                        errors.append("prior mistake references must contain an incident_id")
                        continue
                    registered = known.get(prior["incident_id"])
                    if not registered:
                        errors.append("prior mistake reference is not present in the incident registry")
                    elif registered.get("root_cause_id") != root_cause_id:
                        errors.append("prior mistake root_cause_id does not match")
                    else:
                        covered_occurrences += registered.get("confirmed_occurrences", 0)
                if covered_occurrences < occurrence_count - 1:
                    errors.append("registered prior evidence does not cover the declared occurrence count")

        steps = record.get("incident_steps")
        if not isinstance(steps, dict):
            errors.append("incident_steps must map every step to completion evidence")
            steps = {}
        missing_steps = sorted(INCIDENT_STEPS - set(steps))
        if missing_steps:
            errors.append(f"incident steps missing: {', '.join(missing_steps)}")
        for step, result in steps.items():
            if step not in INCIDENT_STEPS:
                errors.append(f"unknown incident step: {step}")
            if not isinstance(result, dict) or result.get("status") != "complete" or not valid_evidence(result.get("evidence")):
                errors.append(f"incident step {step} requires complete status and structured evidence")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    record = json.loads(args.record.read_text(encoding="utf-8"))
    registry_path = args.record.parent / "mistake_registry.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.exists() else {}
    errors = validate(record, registry)
    if errors:
        print("ACTION GATE: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("ACTION GATE: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
