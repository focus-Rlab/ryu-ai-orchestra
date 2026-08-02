"""REQ-C: CLI entry point.

Subcommands:
  validate --type {requirements|implementation|evaluation} --format {text|json} <file>
      REQ-B1 schema validation of a single artifact only.

  check --requirements <file> --implementation <file> --evaluation <file> --format {text|json}
      REQ-C2 front gate, then REQ-B1..B6 across all three artifacts.

Exit codes (REQ-C4):
  0 = zero findings (pending count does not matter)
  1 = one or more findings
  2 = fatal error (file missing / JSON parse error / unsupported
      schema_version / run_id format invalid [check, top-level only] /
      run_id duplicate [check only] / missing required CLI arguments)
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict, List, Tuple

from .common import RUN_ID_PATTERN, SCHEMA_VERSION_ALLOWED, FatalError, is_dict, norm
from .cross_checks import run_all_cross_checks
from .schema import VALIDATORS

REPORT_SCHEMA_VERSION = "1.0"


def _load_json_file(path: str, label: str) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
    except OSError as exc:
        raise FatalError(f"[{label}] file not found or unreadable: '{path}' ({exc})") from exc
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        raise FatalError(f"[{label}] JSON syntax error in '{path}': {exc}") from exc
    return data


def _check_schema_version(data: Any, label: str, path: str) -> None:
    if not is_dict(data):
        raise FatalError(f"[{label}] top-level document in '{path}' must be a JSON object")
    version = data.get("schema_version")
    if version not in SCHEMA_VERSION_ALLOWED:
        raise FatalError(
            f"[{label}] unsupported schema_version in '{path}': {version!r} "
            f"(allowed: {SCHEMA_VERSION_ALLOWED})"
        )


def _build_summary(findings: List[Dict[str, Any]], pending: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_check_id: Dict[str, int] = {}
    for item in findings + pending:
        by_check_id[item["check_id"]] = by_check_id.get(item["check_id"], 0) + 1
    return {
        "total_findings": len(findings),
        "total_pending": len(pending),
        "by_check_id": by_check_id,
    }


def _print_text_report(
    findings: List[Dict[str, Any]],
    pending: List[Dict[str, Any]],
    checked: Dict[str, Any],
    out=sys.stdout,
) -> None:
    print("=== Handoff Contract Check Report ===", file=out)
    if checked:
        print("Checked:", file=out)
        for key, value in checked.items():
            print(f"  {key}: {value}", file=out)

    print(f"\nFindings ({len(findings)}):", file=out)
    if not findings:
        print("  (none)", file=out)
    else:
        for item in findings:
            related = f" related_ids={item['related_ids']}" if item["related_ids"] else ""
            print(
                f"  - [{item['check_id']}] artifact={item['artifact']} "
                f"field_path={item['field_path']}{related}: {item['message']}",
                file=out,
            )

    print(f"\nPending ({len(pending)}):", file=out)
    if not pending:
        print("  (none)", file=out)
    else:
        for item in pending:
            related = f" related_ids={item['related_ids']}" if item["related_ids"] else ""
            print(
                f"  - [{item['check_id']}] artifact={item['artifact']} "
                f"field_path={item['field_path']}{related}: {item['message']}",
                file=out,
            )

    summary = _build_summary(findings, pending)
    print("\nSummary:", file=out)
    print(f"  total_findings: {summary['total_findings']}", file=out)
    print(f"  total_pending: {summary['total_pending']}", file=out)
    print(f"  by_check_id: {summary['by_check_id']}", file=out)


def cmd_validate(args: argparse.Namespace) -> int:
    label = args.type
    try:
        data = _load_json_file(args.file, label)
        _check_schema_version(data, label, args.file)
    except FatalError as exc:
        print(f"FATAL: {exc.message}", file=sys.stderr)
        return 2

    validator = VALIDATORS[args.type]
    findings = validator(data)

    checked = {
        "artifact_type": args.type,
        "run_id": data.get("run_id") if is_dict(data) else None,
    }

    if args.format == "json":
        report = {
            "report_schema_version": REPORT_SCHEMA_VERSION,
            "checked": checked,
            "findings": findings,
            "summary": _build_summary(findings, []),
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text_report(findings, [], checked)

    return 1 if findings else 0


def _run_front_gate(req_path: str, impl_path: str, eval_path: str) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    """REQ-C2 steps 1-4, executed strictly in order, each step covering all 3 files."""

    # Step 1: file existence + JSON parse
    errors: List[str] = []
    parsed: Dict[str, Any] = {}
    for label, path in (("requirements", req_path), ("implementation", impl_path), ("evaluation", eval_path)):
        try:
            parsed[label] = _load_json_file(path, label)
        except FatalError as exc:
            errors.append(exc.message)
    if errors:
        raise FatalError("; ".join(errors))

    # Step 2: schema_version
    errors = []
    for label, path in (("requirements", req_path), ("implementation", impl_path), ("evaluation", eval_path)):
        try:
            _check_schema_version(parsed[label], label, path)
        except FatalError as exc:
            errors.append(exc.message)
    if errors:
        raise FatalError("; ".join(errors))

    # Step 3: top-level run_id format (this file's role only; not reference fields)
    errors = []
    for label in ("requirements", "implementation", "evaluation"):
        run_id = parsed[label].get("run_id")
        if not isinstance(run_id, str) or not RUN_ID_PATTERN.match(run_id):
            errors.append(f"[{label}] top-level run_id is not a valid run-NNN identifier: {run_id!r}")
    if errors:
        raise FatalError("; ".join(errors))

    # Step 4: run_id duplication across the 3 files (normalized comparison, REQ-B0)
    normalized = {label: norm(parsed[label]["run_id"]) for label in ("requirements", "implementation", "evaluation")}
    seen: Dict[str, List[str]] = {}
    for label, value in normalized.items():
        seen.setdefault(value, []).append(label)
    duplicates = {value: labels for value, labels in seen.items() if len(labels) > 1}
    if duplicates:
        detail = "; ".join(f"run_id '{value}' shared by {labels}" for value, labels in duplicates.items())
        raise FatalError(f"duplicate run_id across artifacts: {detail}")

    return parsed["requirements"], parsed["implementation"], parsed["evaluation"]


def cmd_check(args: argparse.Namespace) -> int:
    try:
        requirements, implementation, evaluation = _run_front_gate(
            args.requirements, args.implementation, args.evaluation
        )
    except FatalError as exc:
        print(f"FATAL: {exc.message}", file=sys.stderr)
        return 2

    findings: List[Dict[str, Any]] = []
    pending: List[Dict[str, Any]] = []

    findings.extend(VALIDATORS["requirements"](requirements))
    findings.extend(VALIDATORS["implementation"](implementation))
    findings.extend(VALIDATORS["evaluation"](evaluation))

    cross_findings, cross_pending = run_all_cross_checks(requirements, implementation, evaluation)
    findings.extend(cross_findings)
    pending.extend(cross_pending)

    checked = {
        "requirements_run_id": requirements.get("run_id"),
        "implementation_run_id": implementation.get("run_id"),
        "evaluation_run_id": evaluation.get("run_id"),
    }

    if args.format == "json":
        report = {
            "report_schema_version": REPORT_SCHEMA_VERSION,
            "checked": checked,
            "findings": findings,
            "pending": pending,
            "summary": _build_summary(findings, pending),
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text_report(findings, pending, checked)

    return 1 if findings else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="handoff_checker", description="3-agent handoff contract checker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_validate = subparsers.add_parser("validate", help="validate a single artifact against its schema (REQ-B1)")
    p_validate.add_argument("--type", required=True, choices=["requirements", "implementation", "evaluation"])
    p_validate.add_argument("--format", required=False, choices=["text", "json"], default="text")
    p_validate.add_argument("file")
    p_validate.set_defaults(func=cmd_validate)

    p_check = subparsers.add_parser("check", help="cross-check all three artifacts (REQ-B0..B6)")
    p_check.add_argument("--requirements", required=True)
    p_check.add_argument("--implementation", required=True)
    p_check.add_argument("--evaluation", required=True)
    p_check.add_argument("--format", required=False, choices=["text", "json"], default="text")
    p_check.set_defaults(func=cmd_check)

    return parser


def main(argv: List[str] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
