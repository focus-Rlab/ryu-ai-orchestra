"""REQ-B2 - REQ-B6 cross-artifact and single-artifact semantic checks.

These functions only run as part of the `check` command (REQ-C1: the
`validate` command performs REQ-B1 schema validation only). They are
only reached after the REQ-C2 front gate (file existence / JSON parse /
schema_version / top-level run_id format / run_id duplication) has
fully passed.

Each function returns (findings, pending) — two lists of finding dicts.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from .common import is_dict, is_list, make_finding, norm

Findings = List[Dict[str, Any]]


def _get(data: Any, *path, default=None):
    cur = data
    for key in path:
        if not is_dict(cur) or key not in cur:
            return default
        cur = cur[key]
    return cur


def check_b2_unresolved_items(requirements: Dict[str, Any], implementation: Dict[str, Any]) -> Findings:
    """REQ-B2: unresolved_items <-> resolved_unresolved_items."""
    findings: Findings = []

    req_items = _get(requirements, "unresolved_items", default=[])
    impl_items = _get(implementation, "resolved_unresolved_items", default=[])
    if not is_list(req_items):
        req_items = []
    if not is_list(impl_items):
        impl_items = []

    req_ids = {}
    for item in req_items:
        if is_dict(item) and isinstance(item.get("id"), str):
            req_ids[norm(item["id"])] = item["id"]

    for i, item in enumerate(impl_items):
        if not is_dict(item) or not isinstance(item.get("id"), str):
            continue
        norm_id = norm(item["id"])
        if norm_id not in req_ids:
            findings.append(
                make_finding(
                    "IDENTIFIER_MISMATCH",
                    "implementation",
                    f"resolved_unresolved_items[{i}].id",
                    f"resolved_unresolved_items id '{item['id']}' does not exist in requirements.unresolved_items",
                    related_ids=[item["id"]],
                )
            )
            continue

        approved_by = item.get("approved_by")
        if approved_by is None or (isinstance(approved_by, str) and norm(approved_by) == ""):
            findings.append(
                make_finding(
                    "UNAUTHORIZED_UNRESOLVED_RESOLUTION",
                    "implementation",
                    f"resolved_unresolved_items[{i}].approved_by",
                    f"unresolved item '{item['id']}' was resolved without a valid approved_by",
                    related_ids=[item["id"]],
                )
            )

    return findings


def check_b3_acceptance_criteria(
    requirements: Dict[str, Any], implementation: Dict[str, Any], evaluation: Dict[str, Any]
) -> Findings:
    """REQ-B3: acceptance_criteria <-> addressed_acceptance_criteria <-> acceptance_criteria_results."""
    findings: Findings = []

    req_ac = _get(requirements, "acceptance_criteria", default=[])
    impl_ac = _get(implementation, "addressed_acceptance_criteria", default=[])
    eval_ac = _get(evaluation, "acceptance_criteria_results", default=[])
    if not is_list(req_ac):
        req_ac = []
    if not is_list(impl_ac):
        impl_ac = []
    if not is_list(eval_ac):
        eval_ac = []

    req_ids = {}
    for item in req_ac:
        if is_dict(item) and isinstance(item.get("id"), str):
            req_ids[norm(item["id"])] = item["id"]

    impl_addressed_ids = set()
    for i, item in enumerate(impl_ac):
        if not is_dict(item) or not isinstance(item.get("id"), str):
            continue
        norm_id = norm(item["id"])
        impl_addressed_ids.add(norm_id)
        if norm_id not in req_ids:
            findings.append(
                make_finding(
                    "IDENTIFIER_MISMATCH",
                    "implementation",
                    f"addressed_acceptance_criteria[{i}].id",
                    f"addressed_acceptance_criteria id '{item['id']}' does not exist in requirements.acceptance_criteria",
                    related_ids=[item["id"]],
                )
            )

    for norm_id, raw_id in req_ids.items():
        if norm_id not in impl_addressed_ids:
            findings.append(
                make_finding(
                    "AC_NOT_ADDRESSED",
                    "implementation",
                    "addressed_acceptance_criteria",
                    f"acceptance criterion '{raw_id}' is not addressed in implementation",
                    related_ids=[raw_id],
                )
            )

    eval_tested_ids = set()
    for item in eval_ac:
        if is_dict(item) and isinstance(item.get("id"), str):
            eval_tested_ids.add(norm(item["id"]))

    for norm_id, raw_id in req_ids.items():
        if norm_id not in eval_tested_ids:
            findings.append(
                make_finding(
                    "AC_NOT_TESTED",
                    "evaluation",
                    "acceptance_criteria_results",
                    f"acceptance criterion '{raw_id}' has no corresponding evaluation result",
                    related_ids=[raw_id],
                )
            )

    return findings


def check_b4_deviations(implementation: Dict[str, Any]) -> Tuple[Findings, Findings]:
    """REQ-B4: five-state deviation classification.

    Order: first detect (5) undeclared deviations from changed_files,
    then classify each deviations[] entry into (2)/(3)/(4).
    """
    findings: Findings = []
    pending: Findings = []

    changed_files = _get(implementation, "changed_files", default=[])
    deviations = _get(implementation, "deviations", default=[])
    if not is_list(changed_files):
        changed_files = []
    if not is_list(deviations):
        deviations = []

    declared_paths = set()
    for dev in deviations:
        if not is_dict(dev):
            continue
        related_files = dev.get("related_files")
        if is_list(related_files):
            for rf in related_files:
                if isinstance(rf, str):
                    declared_paths.add(norm(rf))

    # (5) undeclared deviation
    for i, cf in enumerate(changed_files):
        if not is_dict(cf):
            continue
        if cf.get("in_scope") is False:
            path = cf.get("path")
            if isinstance(path, str) and norm(path) not in declared_paths:
                findings.append(
                    make_finding(
                        "UNDECLARED_DEVIATION",
                        "implementation",
                        f"changed_files[{i}].path",
                        f"changed file '{path}' is out of scope but not declared in any deviations[].related_files",
                        related_ids=[path],
                    )
                )

    # (2)/(3)/(4) classification of each declared deviation
    for i, dev in enumerate(deviations):
        if not is_dict(dev):
            continue
        approval_status = dev.get("approval_status")
        implementation_status = dev.get("implementation_status")
        description = dev.get("description")

        if approval_status == "approved":
            continue  # (2) no issue regardless of implementation_status
        if approval_status == "unapproved" and implementation_status == "proposed":
            pending.append(
                make_finding(
                    "PENDING_UNAPPROVED_DEVIATION",
                    "implementation",
                    f"deviations[{i}]",
                    f"deviation is unapproved and not yet implemented: {description}",
                    related_ids=[],
                )
            )
        elif approval_status == "unapproved" and implementation_status == "implemented":
            findings.append(
                make_finding(
                    "UNAPPROVED_IMPLEMENTED_DEVIATION",
                    "implementation",
                    f"deviations[{i}]",
                    f"deviation is unapproved but already implemented: {description}",
                    related_ids=[],
                )
            )
        # any other combination is already flagged as SCHEMA_INVALID
        # by schema.validate_implementation and is not re-classified here.

    return findings, pending


def check_b5_evaluation(evaluation: Dict[str, Any]) -> Findings:
    """REQ-B5: unsupported pass results and evaluation-level status inconsistencies."""
    findings: Findings = []

    ac_results = _get(evaluation, "acceptance_criteria_results", default=[])
    evidence = _get(evaluation, "evidence", default=[])
    overall_result = evaluation.get("overall_result") if is_dict(evaluation) else None
    residual_risks = _get(evaluation, "residual_risks", default=[])
    if not is_list(ac_results):
        ac_results = []
    if not is_list(evidence):
        evidence = []
    if not is_list(residual_risks):
        residual_risks = []

    evidence_ids = set()
    for e in evidence:
        if is_dict(e) and isinstance(e.get("id"), str):
            evidence_ids.add(norm(e["id"]))

    has_fail = False
    for i, item in enumerate(ac_results):
        if not is_dict(item):
            continue
        result = item.get("result")
        if result == "fail":
            has_fail = True
        if result == "pass":
            evidence_ref = item.get("evidence_ref")
            valid = isinstance(evidence_ref, str) and norm(evidence_ref) != "" and norm(evidence_ref) in evidence_ids
            if not valid:
                findings.append(
                    make_finding(
                        "UNSUPPORTED_PASS_WITHOUT_EVIDENCE",
                        "evaluation",
                        f"acceptance_criteria_results[{i}].evidence_ref",
                        f"acceptance criterion '{item.get('id')}' is marked pass without valid supporting evidence",
                        related_ids=[item.get("id")] if isinstance(item.get("id"), str) else [],
                    )
                )

    if overall_result == "pass" and has_fail:
        findings.append(
            make_finding(
                "STATUS_INCONSISTENCY",
                "evaluation",
                "overall_result",
                "overall_result is 'pass' but at least one acceptance_criteria_results entry is 'fail'",
                related_ids=[],
            )
        )

    if overall_result == "conditional_pass" and len(residual_risks) < 1:
        findings.append(
            make_finding(
                "STATUS_INCONSISTENCY",
                "evaluation",
                "residual_risks",
                "overall_result is 'conditional_pass' but residual_risks is empty",
                related_ids=[],
            )
        )

    return findings


def check_b6_identifiers_and_status(
    requirements: Dict[str, Any], implementation: Dict[str, Any], evaluation: Dict[str, Any]
) -> Findings:
    """REQ-B6: cross-artifact identifier / target / status consistency."""
    findings: Findings = []

    req_run_id = requirements.get("run_id") if is_dict(requirements) else None
    impl_run_id = implementation.get("run_id") if is_dict(implementation) else None

    impl_req_ref = _get(implementation, "requirements_ref", "requirements_run_id")
    if isinstance(impl_req_ref, str) and isinstance(req_run_id, str) and norm(impl_req_ref) != norm(req_run_id):
        findings.append(
            make_finding(
                "IDENTIFIER_MISMATCH",
                "implementation",
                "requirements_ref.requirements_run_id",
                f"requirements_ref.requirements_run_id '{impl_req_ref}' does not match requirements.run_id '{req_run_id}'",
                related_ids=[impl_req_ref, req_run_id],
            )
        )

    eval_req_ref = _get(evaluation, "verification_target", "requirements_run_id")
    if isinstance(eval_req_ref, str) and isinstance(req_run_id, str) and norm(eval_req_ref) != norm(req_run_id):
        findings.append(
            make_finding(
                "IDENTIFIER_MISMATCH",
                "evaluation",
                "verification_target.requirements_run_id",
                f"verification_target.requirements_run_id '{eval_req_ref}' does not match requirements.run_id '{req_run_id}'",
                related_ids=[eval_req_ref, req_run_id],
            )
        )

    eval_impl_ref = _get(evaluation, "verification_target", "implementation_run_id")
    if isinstance(eval_impl_ref, str) and isinstance(impl_run_id, str) and norm(eval_impl_ref) != norm(impl_run_id):
        findings.append(
            make_finding(
                "IDENTIFIER_MISMATCH",
                "evaluation",
                "verification_target.implementation_run_id",
                f"verification_target.implementation_run_id '{eval_impl_ref}' does not match implementation.run_id '{impl_run_id}'",
                related_ids=[eval_impl_ref, impl_run_id],
            )
        )

    targets = {}
    for label, artifact in (("requirements", requirements), ("implementation", implementation), ("evaluation", evaluation)):
        t = artifact.get("target") if is_dict(artifact) else None
        if isinstance(t, str):
            targets[label] = t

    normed = {label: norm(t) for label, t in targets.items()}
    distinct = set(normed.values())
    if len(distinct) > 1:
        detail = ", ".join(f"{label}='{targets[label]}'" for label in targets)
        findings.append(
            make_finding(
                "TARGET_MISMATCH",
                "cross",
                "target",
                f"target values differ across artifacts: {detail}",
                related_ids=list(targets.values()),
            )
        )

    approval_status = requirements.get("approval_status") if is_dict(requirements) else None
    if approval_status != "approved":
        findings.append(
            make_finding(
                "STATUS_INCONSISTENCY",
                "requirements",
                "approval_status",
                f"requirements.approval_status is '{approval_status}' but implementation/evaluation artifacts reference it",
                related_ids=[],
            )
        )

    completion_status = implementation.get("completion_status") if is_dict(implementation) else None
    overall_result = evaluation.get("overall_result") if is_dict(evaluation) else None
    if completion_status in ("blocked", "incomplete") and overall_result == "pass":
        findings.append(
            make_finding(
                "STATUS_INCONSISTENCY",
                "cross",
                "overall_result",
                f"implementation.completion_status is '{completion_status}' but evaluation.overall_result is 'pass'",
                related_ids=[],
            )
        )

    return findings


def run_all_cross_checks(
    requirements: Dict[str, Any], implementation: Dict[str, Any], evaluation: Dict[str, Any]
) -> Tuple[Findings, Findings]:
    """Run REQ-B2 through REQ-B6 and return (findings, pending)."""
    findings: Findings = []
    pending: Findings = []

    findings.extend(check_b2_unresolved_items(requirements, implementation))
    findings.extend(check_b3_acceptance_criteria(requirements, implementation, evaluation))

    b4_findings, b4_pending = check_b4_deviations(implementation)
    findings.extend(b4_findings)
    pending.extend(b4_pending)

    findings.extend(check_b5_evaluation(evaluation))
    findings.extend(check_b6_identifiers_and_status(requirements, implementation, evaluation))

    return findings, pending
