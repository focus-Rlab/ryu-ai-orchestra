"""REQ-A schema definitions and REQ-B1 schema validation.

Each validate_* function returns a list of finding dicts (check_id is
always SCHEMA_INVALID). Nothing here mutates the input data; only the
raw values already present in the JSON are echoed back in messages.

REQ-A3 states two conditional constraints as part of the evaluation
schema itself:

  * evaluation.acceptance_criteria_results[].evidence_ref required and
    consistent with evidence[].id when result == "pass"
  * evaluation.residual_risks non-empty when overall_result ==
    "conditional_pass"

REQ-B5 separately assigns these same real-world conditions their own,
more specific, semantic check IDs (UNSUPPORTED_PASS_WITHOUT_EVIDENCE /
STATUS_INCONSISTENCY). Requirements v3.1 does not state a rule
suppressing one check in favor of the other, so both are implemented
independently and, per Raphael/Ryunosuke direction (run-010 review),
BOTH findings are intentionally reported together when the same
underlying data violates both: SCHEMA_INVALID here (REQ-B1, format/
structural validation of REQ-A3) and UNSUPPORTED_PASS_WITHOUT_EVIDENCE
/ STATUS_INCONSISTENCY from REQ-B5 (cross_checks.py, semantic
validation, `check` command only). This means `validate --type
evaluation` now also reports SCHEMA_INVALID for these two conditions
even though REQ-B5 itself is only exercised by `check`.

All other constraints stated in REQ-A (including the deviations
related_files-non-empty-when-implemented rule, which REQ-B4 itself
explicitly labels a schema constraint / SCHEMA_INVALID, see AC-22) are
validated here as well.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .common import (
    AC_ID_PATTERN,
    EVID_ID_PATTERN,
    OPEN_ID_PATTERN,
    RUN_ID_PATTERN,
    SCHEMA_VERSION_ALLOWED,
    is_bool,
    is_dict,
    is_list,
    is_non_empty_str,
    is_str,
    make_finding,
    norm,
)

_ARTIFACT_TYPE_ENUM = {
    "requirements": "requirements",
    "implementation": "implementation",
    "evaluation": "evaluation",
}


def _f(check_findings, artifact, field_path, message):
    check_findings.append(make_finding("SCHEMA_INVALID", artifact, field_path, message))


def validate_common_header(data: Any, artifact: str, expected_artifact_type: str) -> List[Dict[str, Any]]:
    """Validate the common header fields shared by all three artifacts.

    `artifact` is the report-facing artifact label ("requirements" /
    "implementation" / "evaluation"), used for finding[].artifact.
    """
    findings: List[Dict[str, Any]] = []

    if not is_dict(data):
        _f(findings, artifact, "$", "top-level document must be a JSON object")
        return findings

    # schema_version
    if "schema_version" not in data:
        _f(findings, artifact, "schema_version", "required field 'schema_version' is missing")
    elif not is_str(data["schema_version"]):
        _f(findings, artifact, "schema_version", "'schema_version' must be a string")
    elif data["schema_version"] not in SCHEMA_VERSION_ALLOWED:
        _f(findings, artifact, "schema_version", f"'schema_version' must be one of {SCHEMA_VERSION_ALLOWED}")

    # artifact_type
    if "artifact_type" not in data:
        _f(findings, artifact, "artifact_type", "required field 'artifact_type' is missing")
    elif not is_str(data["artifact_type"]):
        _f(findings, artifact, "artifact_type", "'artifact_type' must be a string")
    elif data["artifact_type"] != expected_artifact_type:
        _f(
            findings,
            artifact,
            "artifact_type",
            f"'artifact_type' must be '{expected_artifact_type}', got '{data['artifact_type']}'",
        )

    # run_id (top-level). Format validated here for REQ-B1 / validate command
    # purposes (AC-26). In the `check` command flow this top-level value is
    # already guaranteed well-formed by the REQ-C2 front gate before this
    # function ever runs against it, so this branch is effectively inert
    # (never fires) for `check`, and remains fully active for `validate`.
    if "run_id" not in data:
        _f(findings, artifact, "run_id", "required field 'run_id' is missing")
    elif not is_str(data["run_id"]):
        _f(findings, artifact, "run_id", "'run_id' must be a string")
    elif not RUN_ID_PATTERN.match(data["run_id"]):
        _f(findings, artifact, "run_id", f"'run_id' does not match ^run-\\d{{3}}$: '{data['run_id']}'")

    # target
    if "target" not in data:
        _f(findings, artifact, "target", "required field 'target' is missing")
    elif not is_non_empty_str(data["target"]):
        _f(findings, artifact, "target", "'target' must be a non-empty string")

    return findings


def _check_run_id_ref_field(findings, artifact, field_path, value):
    if value is None:
        _f(findings, artifact, field_path, f"required field '{field_path}' is missing")
        return
    if not is_str(value):
        _f(findings, artifact, field_path, f"'{field_path}' must be a string")
        return
    if not RUN_ID_PATTERN.match(value):
        _f(findings, artifact, field_path, f"'{field_path}' does not match ^run-\\d{{3}}$: '{value}'")


def validate_requirements(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    artifact = "requirements"
    findings = validate_common_header(data, artifact, "requirements")
    if not is_dict(data):
        return findings

    # purpose
    if "purpose" not in data:
        _f(findings, artifact, "purpose", "required field 'purpose' is missing")
    elif not is_non_empty_str(data["purpose"]):
        _f(findings, artifact, "purpose", "'purpose' must be a non-empty string")

    # scope_in
    if "scope_in" not in data:
        _f(findings, artifact, "scope_in", "required field 'scope_in' is missing")
    elif not is_list(data["scope_in"]):
        _f(findings, artifact, "scope_in", "'scope_in' must be an array")
    else:
        if len(data["scope_in"]) < 1:
            _f(findings, artifact, "scope_in", "'scope_in' must contain at least 1 element")
        for i, item in enumerate(data["scope_in"]):
            if not is_str(item):
                _f(findings, artifact, f"scope_in[{i}]", "elements of 'scope_in' must be strings")

    # scope_out
    if "scope_out" not in data:
        _f(findings, artifact, "scope_out", "required field 'scope_out' is missing")
    elif not is_list(data["scope_out"]):
        _f(findings, artifact, "scope_out", "'scope_out' must be an array")
    else:
        for i, item in enumerate(data["scope_out"]):
            if not is_str(item):
                _f(findings, artifact, f"scope_out[{i}]", "elements of 'scope_out' must be strings")

    # acceptance_criteria
    if "acceptance_criteria" not in data:
        _f(findings, artifact, "acceptance_criteria", "required field 'acceptance_criteria' is missing")
    elif not is_list(data["acceptance_criteria"]):
        _f(findings, artifact, "acceptance_criteria", "'acceptance_criteria' must be an array")
    else:
        ac_list = data["acceptance_criteria"]
        if len(ac_list) < 1:
            _f(findings, artifact, "acceptance_criteria", "'acceptance_criteria' must contain at least 1 element")
        seen_ids = set()
        for i, item in enumerate(ac_list):
            base = f"acceptance_criteria[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "id" not in item:
                _f(findings, artifact, f"{base}.id", "required field 'id' is missing")
            elif not is_str(item["id"]):
                _f(findings, artifact, f"{base}.id", "'id' must be a string")
            elif not AC_ID_PATTERN.match(item["id"]):
                _f(findings, artifact, f"{base}.id", f"'id' does not match ^AC-\\d+$: '{item['id']}'")
            else:
                key = item["id"].strip()
                if key in seen_ids:
                    _f(findings, artifact, f"{base}.id", f"duplicate acceptance_criteria id: '{item['id']}'")
                seen_ids.add(key)
            if "description" not in item:
                _f(findings, artifact, f"{base}.description", "required field 'description' is missing")
            elif not is_non_empty_str(item["description"]):
                _f(findings, artifact, f"{base}.description", "'description' must be a non-empty string")

    # constraints
    if "constraints" not in data:
        _f(findings, artifact, "constraints", "required field 'constraints' is missing")
    elif not is_list(data["constraints"]):
        _f(findings, artifact, "constraints", "'constraints' must be an array")
    else:
        for i, item in enumerate(data["constraints"]):
            if not is_str(item):
                _f(findings, artifact, f"constraints[{i}]", "elements of 'constraints' must be strings")

    # unresolved_items
    if "unresolved_items" not in data:
        _f(findings, artifact, "unresolved_items", "required field 'unresolved_items' is missing")
    elif not is_list(data["unresolved_items"]):
        _f(findings, artifact, "unresolved_items", "'unresolved_items' must be an array")
    else:
        seen_ids = set()
        for i, item in enumerate(data["unresolved_items"]):
            base = f"unresolved_items[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "id" not in item:
                _f(findings, artifact, f"{base}.id", "required field 'id' is missing")
            elif not is_str(item["id"]):
                _f(findings, artifact, f"{base}.id", "'id' must be a string")
            elif not OPEN_ID_PATTERN.match(item["id"]):
                _f(findings, artifact, f"{base}.id", f"'id' does not match ^OPEN-\\d+$: '{item['id']}'")
            else:
                key = item["id"].strip()
                if key in seen_ids:
                    _f(findings, artifact, f"{base}.id", f"duplicate unresolved_items id: '{item['id']}'")
                seen_ids.add(key)
            if "description" not in item:
                _f(findings, artifact, f"{base}.description", "required field 'description' is missing")
            elif not is_str(item["description"]):
                _f(findings, artifact, f"{base}.description", "'description' must be a string")
            if "decision_owner" not in item:
                _f(findings, artifact, f"{base}.decision_owner", "required field 'decision_owner' is missing")
            elif item["decision_owner"] not in ("raphael", "ryunosuke"):
                _f(
                    findings,
                    artifact,
                    f"{base}.decision_owner",
                    f"'decision_owner' must be 'raphael' or 'ryunosuke', got '{item['decision_owner']}'",
                )

    # approval_status
    approval_enum = ("draft", "pending_raphael_review", "pending_ryunosuke_approval", "approved", "rejected")
    if "approval_status" not in data:
        _f(findings, artifact, "approval_status", "required field 'approval_status' is missing")
    elif data["approval_status"] not in approval_enum:
        _f(
            findings,
            artifact,
            "approval_status",
            f"'approval_status' must be one of {approval_enum}, got '{data['approval_status']}'",
        )

    return findings


def validate_implementation(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    artifact = "implementation"
    findings = validate_common_header(data, artifact, "implementation")
    if not is_dict(data):
        return findings

    # requirements_ref
    if "requirements_ref" not in data:
        _f(findings, artifact, "requirements_ref", "required field 'requirements_ref' is missing")
    elif not is_dict(data["requirements_ref"]):
        _f(findings, artifact, "requirements_ref", "'requirements_ref' must be an object")
    else:
        ref = data["requirements_ref"]
        if "requirements_run_id" not in ref:
            _f(
                findings,
                artifact,
                "requirements_ref.requirements_run_id",
                "required field 'requirements_run_id' is missing",
            )
        else:
            _check_run_id_ref_field(
                findings, artifact, "requirements_ref.requirements_run_id", ref["requirements_run_id"]
            )

    # addressed_acceptance_criteria
    status_enum = ("implemented", "partially_implemented", "not_implemented")
    if "addressed_acceptance_criteria" not in data:
        _f(
            findings,
            artifact,
            "addressed_acceptance_criteria",
            "required field 'addressed_acceptance_criteria' is missing",
        )
    elif not is_list(data["addressed_acceptance_criteria"]):
        _f(findings, artifact, "addressed_acceptance_criteria", "'addressed_acceptance_criteria' must be an array")
    else:
        for i, item in enumerate(data["addressed_acceptance_criteria"]):
            base = f"addressed_acceptance_criteria[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "id" not in item:
                _f(findings, artifact, f"{base}.id", "required field 'id' is missing")
            elif not is_str(item["id"]):
                _f(findings, artifact, f"{base}.id", "'id' must be a string")
            elif not AC_ID_PATTERN.match(item["id"]):
                _f(findings, artifact, f"{base}.id", f"'id' does not match ^AC-\\d+$: '{item['id']}'")
            if "status" not in item:
                _f(findings, artifact, f"{base}.status", "required field 'status' is missing")
            elif item["status"] not in status_enum:
                _f(findings, artifact, f"{base}.status", f"'status' must be one of {status_enum}, got '{item['status']}'")
            if "note" in item and item["note"] is not None and not is_str(item["note"]):
                _f(findings, artifact, f"{base}.note", "'note' must be a string if present")

    # changed_files
    change_type_enum = ("added", "modified", "deleted")
    if "changed_files" not in data:
        _f(findings, artifact, "changed_files", "required field 'changed_files' is missing")
    elif not is_list(data["changed_files"]):
        _f(findings, artifact, "changed_files", "'changed_files' must be an array")
    else:
        for i, item in enumerate(data["changed_files"]):
            base = f"changed_files[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "path" not in item:
                _f(findings, artifact, f"{base}.path", "required field 'path' is missing")
            elif not is_non_empty_str(item["path"]):
                _f(findings, artifact, f"{base}.path", "'path' must be a non-empty string")
            if "change_type" not in item:
                _f(findings, artifact, f"{base}.change_type", "required field 'change_type' is missing")
            elif item["change_type"] not in change_type_enum:
                _f(
                    findings,
                    artifact,
                    f"{base}.change_type",
                    f"'change_type' must be one of {change_type_enum}, got '{item['change_type']}'",
                )
            if "in_scope" not in item:
                _f(findings, artifact, f"{base}.in_scope", "required field 'in_scope' is missing")
            elif not is_bool(item["in_scope"]):
                _f(findings, artifact, f"{base}.in_scope", "'in_scope' must be a boolean")

    # verifications_run
    result_enum = ("pass", "fail", "not_run")
    if "verifications_run" not in data:
        _f(findings, artifact, "verifications_run", "required field 'verifications_run' is missing")
    elif not is_list(data["verifications_run"]):
        _f(findings, artifact, "verifications_run", "'verifications_run' must be an array")
    else:
        for i, item in enumerate(data["verifications_run"]):
            base = f"verifications_run[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "command" not in item:
                _f(findings, artifact, f"{base}.command", "required field 'command' is missing")
            elif not is_str(item["command"]):
                _f(findings, artifact, f"{base}.command", "'command' must be a string")
            if "result" not in item:
                _f(findings, artifact, f"{base}.result", "required field 'result' is missing")
            elif item["result"] not in result_enum:
                _f(findings, artifact, f"{base}.result", f"'result' must be one of {result_enum}, got '{item['result']}'")

    # deviations
    if "deviations" not in data:
        _f(findings, artifact, "deviations", "required field 'deviations' is missing")
    elif not is_list(data["deviations"]):
        _f(findings, artifact, "deviations", "'deviations' must be an array")
    else:
        for i, item in enumerate(data["deviations"]):
            base = f"deviations[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "description" not in item:
                _f(findings, artifact, f"{base}.description", "required field 'description' is missing")
            elif not is_str(item["description"]):
                _f(findings, artifact, f"{base}.description", "'description' must be a string")
            if "reason" not in item:
                _f(findings, artifact, f"{base}.reason", "required field 'reason' is missing")
            elif not is_str(item["reason"]):
                _f(findings, artifact, f"{base}.reason", "'reason' must be a string")

            implementation_status = item.get("implementation_status")
            related_files = item.get("related_files")
            if "related_files" not in item:
                _f(findings, artifact, f"{base}.related_files", "required field 'related_files' is missing")
            elif not is_list(related_files):
                _f(findings, artifact, f"{base}.related_files", "'related_files' must be an array")
            else:
                for j, rf in enumerate(related_files):
                    if not is_str(rf):
                        _f(findings, artifact, f"{base}.related_files[{j}]", "elements must be strings")
                if implementation_status == "implemented" and len(related_files) < 1:
                    _f(
                        findings,
                        artifact,
                        f"{base}.related_files",
                        "'related_files' must contain at least 1 element when implementation_status is 'implemented'",
                    )

            approval_status = item.get("approval_status")
            if "approval_status" not in item:
                _f(findings, artifact, f"{base}.approval_status", "required field 'approval_status' is missing")
            elif approval_status not in ("approved", "unapproved"):
                _f(
                    findings,
                    artifact,
                    f"{base}.approval_status",
                    f"'approval_status' must be 'approved' or 'unapproved', got '{approval_status}'",
                )

            approved_by = item.get("approved_by")
            if approval_status == "approved":
                if "approved_by" not in item or approved_by is None:
                    _f(
                        findings,
                        artifact,
                        f"{base}.approved_by",
                        "'approved_by' is required when approval_status is 'approved'",
                    )
                elif approved_by not in ("raphael", "ryunosuke"):
                    _f(
                        findings,
                        artifact,
                        f"{base}.approved_by",
                        f"'approved_by' must be 'raphael' or 'ryunosuke', got '{approved_by}'",
                    )
            elif "approved_by" in item and approved_by is not None:
                if approved_by not in ("raphael", "ryunosuke"):
                    _f(
                        findings,
                        artifact,
                        f"{base}.approved_by",
                        f"'approved_by' must be 'raphael' or 'ryunosuke' if present, got '{approved_by}'",
                    )

            if "implementation_status" not in item:
                _f(
                    findings,
                    artifact,
                    f"{base}.implementation_status",
                    "required field 'implementation_status' is missing",
                )
            elif implementation_status not in ("proposed", "implemented"):
                _f(
                    findings,
                    artifact,
                    f"{base}.implementation_status",
                    f"'implementation_status' must be 'proposed' or 'implemented', got '{implementation_status}'",
                )

    # resolved_unresolved_items
    if "resolved_unresolved_items" not in data:
        _f(findings, artifact, "resolved_unresolved_items", "required field 'resolved_unresolved_items' is missing")
    elif not is_list(data["resolved_unresolved_items"]):
        _f(findings, artifact, "resolved_unresolved_items", "'resolved_unresolved_items' must be an array")
    else:
        for i, item in enumerate(data["resolved_unresolved_items"]):
            base = f"resolved_unresolved_items[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "id" not in item:
                _f(findings, artifact, f"{base}.id", "required field 'id' is missing")
            elif not is_str(item["id"]):
                _f(findings, artifact, f"{base}.id", "'id' must be a string")
            elif not OPEN_ID_PATTERN.match(item["id"]):
                _f(findings, artifact, f"{base}.id", f"'id' does not match ^OPEN-\\d+$: '{item['id']}'")
            if "resolution" not in item:
                _f(findings, artifact, f"{base}.resolution", "required field 'resolution' is missing")
            elif not is_str(item["resolution"]):
                _f(findings, artifact, f"{base}.resolution", "'resolution' must be a string")
            if "approved_by" not in item:
                _f(findings, artifact, f"{base}.approved_by", "required field 'approved_by' is missing")
            elif item["approved_by"] not in ("raphael", "ryunosuke"):
                _f(
                    findings,
                    artifact,
                    f"{base}.approved_by",
                    f"'approved_by' must be 'raphael' or 'ryunosuke', got '{item['approved_by']}'",
                )
            if "approval_reference" in item and item["approval_reference"] is not None:
                if not is_str(item["approval_reference"]):
                    _f(findings, artifact, f"{base}.approval_reference", "'approval_reference' must be a string if present")

    # open_issues
    if "open_issues" not in data:
        _f(findings, artifact, "open_issues", "required field 'open_issues' is missing")
    elif not is_list(data["open_issues"]):
        _f(findings, artifact, "open_issues", "'open_issues' must be an array")
    else:
        for i, item in enumerate(data["open_issues"]):
            if not is_str(item):
                _f(findings, artifact, f"open_issues[{i}]", "elements of 'open_issues' must be strings")

    # completion_status
    completion_enum = ("complete", "incomplete", "blocked")
    if "completion_status" not in data:
        _f(findings, artifact, "completion_status", "required field 'completion_status' is missing")
    elif data["completion_status"] not in completion_enum:
        _f(
            findings,
            artifact,
            "completion_status",
            f"'completion_status' must be one of {completion_enum}, got '{data['completion_status']}'",
        )

    return findings


def validate_evaluation(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    artifact = "evaluation"
    findings = validate_common_header(data, artifact, "evaluation")
    if not is_dict(data):
        return findings

    # verification_target
    if "verification_target" not in data:
        _f(findings, artifact, "verification_target", "required field 'verification_target' is missing")
    elif not is_dict(data["verification_target"]):
        _f(findings, artifact, "verification_target", "'verification_target' must be an object")
    else:
        vt = data["verification_target"]
        if "requirements_run_id" not in vt:
            _f(
                findings,
                artifact,
                "verification_target.requirements_run_id",
                "required field 'requirements_run_id' is missing",
            )
        else:
            _check_run_id_ref_field(
                findings, artifact, "verification_target.requirements_run_id", vt["requirements_run_id"]
            )
        if "implementation_run_id" not in vt:
            _f(
                findings,
                artifact,
                "verification_target.implementation_run_id",
                "required field 'implementation_run_id' is missing",
            )
        else:
            _check_run_id_ref_field(
                findings, artifact, "verification_target.implementation_run_id", vt["implementation_run_id"]
            )

    # Pre-scan evidence ids (raw + normalized) so acceptance_criteria_results
    # below can validate evidence_ref cross-references. This is intentionally
    # independent of the 'evidence' block's own validity below (REQ-A3 does
    # not make evidence_ref's schema check conditional on 'evidence' itself
    # being fully schema-valid).
    _raw_evidence = data.get("evidence")
    evidence_ids_normalized = set()
    if is_list(_raw_evidence):
        for _e in _raw_evidence:
            if is_dict(_e) and isinstance(_e.get("id"), str):
                evidence_ids_normalized.add(norm(_e["id"]))

    # acceptance_criteria_results (min length 0; 1+ is only "recommended", not enforced)
    result_enum = ("pass", "fail", "not_tested")
    if "acceptance_criteria_results" not in data:
        _f(
            findings,
            artifact,
            "acceptance_criteria_results",
            "required field 'acceptance_criteria_results' is missing",
        )
    elif not is_list(data["acceptance_criteria_results"]):
        _f(findings, artifact, "acceptance_criteria_results", "'acceptance_criteria_results' must be an array")
    else:
        for i, item in enumerate(data["acceptance_criteria_results"]):
            base = f"acceptance_criteria_results[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "id" not in item:
                _f(findings, artifact, f"{base}.id", "required field 'id' is missing")
            elif not is_str(item["id"]):
                _f(findings, artifact, f"{base}.id", "'id' must be a string")
            elif not AC_ID_PATTERN.match(item["id"]):
                _f(findings, artifact, f"{base}.id", f"'id' does not match ^AC-\\d+$: '{item['id']}'")
            if "result" not in item:
                _f(findings, artifact, f"{base}.result", "required field 'result' is missing")
            elif item["result"] not in result_enum:
                _f(findings, artifact, f"{base}.result", f"'result' must be one of {result_enum}, got '{item['result']}'")
            if "evidence_ref" in item and item["evidence_ref"] is not None and not is_str(item["evidence_ref"]):
                _f(findings, artifact, f"{base}.evidence_ref", "'evidence_ref' must be a string if present")
            # REQ-A3: evidence_ref is required and must reference an existing
            # evidence[].id whenever result == "pass" (REQ-B0-normalized
            # comparison). This is a schema-level (structural) requirement
            # and is validated independently of REQ-B5's semantic check of
            # the same condition (see module docstring); both findings are
            # intentionally reported together when violated.
            if item.get("result") == "pass":
                evidence_ref = item.get("evidence_ref")
                if (
                    not isinstance(evidence_ref, str)
                    or norm(evidence_ref) == ""
                    or norm(evidence_ref) not in evidence_ids_normalized
                ):
                    _f(
                        findings,
                        artifact,
                        f"{base}.evidence_ref",
                        "'evidence_ref' is required and must match an existing evidence[].id when result is 'pass'",
                    )

    # executed_steps
    if "executed_steps" not in data:
        _f(findings, artifact, "executed_steps", "required field 'executed_steps' is missing")
    elif not is_list(data["executed_steps"]):
        _f(findings, artifact, "executed_steps", "'executed_steps' must be an array")
    else:
        for i, item in enumerate(data["executed_steps"]):
            base = f"executed_steps[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "command_or_procedure" not in item:
                _f(findings, artifact, f"{base}.command_or_procedure", "required field 'command_or_procedure' is missing")
            elif not is_str(item["command_or_procedure"]):
                _f(findings, artifact, f"{base}.command_or_procedure", "'command_or_procedure' must be a string")
            if "output_summary" not in item:
                _f(findings, artifact, f"{base}.output_summary", "required field 'output_summary' is missing")
            elif not is_str(item["output_summary"]):
                _f(findings, artifact, f"{base}.output_summary", "'output_summary' must be a string")

    # evidence
    if "evidence" not in data:
        _f(findings, artifact, "evidence", "required field 'evidence' is missing")
    elif not is_list(data["evidence"]):
        _f(findings, artifact, "evidence", "'evidence' must be an array")
    else:
        seen_ids = set()
        for i, item in enumerate(data["evidence"]):
            base = f"evidence[{i}]"
            if not is_dict(item):
                _f(findings, artifact, base, "element must be an object")
                continue
            if "id" not in item:
                _f(findings, artifact, f"{base}.id", "required field 'id' is missing")
            elif not is_str(item["id"]):
                _f(findings, artifact, f"{base}.id", "'id' must be a string")
            elif not EVID_ID_PATTERN.match(item["id"]):
                _f(findings, artifact, f"{base}.id", f"'id' does not match ^EVID-\\d+$: '{item['id']}'")
            else:
                key = item["id"].strip()
                if key in seen_ids:
                    _f(findings, artifact, f"{base}.id", f"duplicate evidence id: '{item['id']}'")
                seen_ids.add(key)
            if "description" not in item:
                _f(findings, artifact, f"{base}.description", "required field 'description' is missing")
            elif not is_str(item["description"]):
                _f(findings, artifact, f"{base}.description", "'description' must be a string")
            if "source" not in item:
                _f(findings, artifact, f"{base}.source", "required field 'source' is missing")
            elif not is_str(item["source"]):
                _f(findings, artifact, f"{base}.source", "'source' must be a string")

    # overall_result
    overall_enum = ("pass", "fail", "conditional_pass")
    if "overall_result" not in data:
        _f(findings, artifact, "overall_result", "required field 'overall_result' is missing")
    elif data["overall_result"] not in overall_enum:
        _f(
            findings,
            artifact,
            "overall_result",
            f"'overall_result' must be one of {overall_enum}, got '{data['overall_result']}'",
        )

    # residual_risks (min length 0 in general; REQ-A3 additionally requires
    # 1+ when overall_result == "conditional_pass". This schema-level check
    # is validated independently of REQ-B5's semantic STATUS_INCONSISTENCY
    # check of the same condition, see module docstring; both findings are
    # intentionally reported together when violated.)
    if "residual_risks" not in data:
        _f(findings, artifact, "residual_risks", "required field 'residual_risks' is missing")
    elif not is_list(data["residual_risks"]):
        _f(findings, artifact, "residual_risks", "'residual_risks' must be an array")
    else:
        for i, item in enumerate(data["residual_risks"]):
            if not is_str(item):
                _f(findings, artifact, f"residual_risks[{i}]", "elements of 'residual_risks' must be strings")
        if data.get("overall_result") == "conditional_pass" and len(data["residual_risks"]) < 1:
            _f(
                findings,
                artifact,
                "residual_risks",
                "'residual_risks' must contain at least 1 element when overall_result is 'conditional_pass'",
            )

    return findings


VALIDATORS = {
    "requirements": validate_requirements,
    "implementation": validate_implementation,
    "evaluation": validate_evaluation,
}
