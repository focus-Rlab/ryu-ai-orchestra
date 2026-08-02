"""Automated tests for the handoff contract checker.

Each test_ac<N> method corresponds to acceptance criterion AC-<N> from
the approved requirements v3.1 (run-010). AC-24 (independent
tester-evaluator verification) is out of scope for this file per the
requirements' role split (REQ-D).

Tests invoke the real CLI (main.py) as a subprocess, which exercises
the full stack (argument parsing, front gate, schema validation,
cross-artifact checks, report formatting, exit codes) exactly the way
an external caller would use it.

Run with:
    python3 -m unittest discover -s pilot_sandbox/handoff_contract_checker/tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / "main.py"
FIXTURES = ROOT / "fixtures"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def run_cli(args):
    result = subprocess.run(
        [sys.executable, str(MAIN)] + args,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr


def fx(name: str) -> str:
    return str(FIXTURES / name)


def run_check_json(req, impl, ev):
    code, out, err = run_cli(
        ["check", "--requirements", fx(req), "--implementation", fx(impl), "--evaluation", fx(ev), "--format", "json"]
    )
    report = json.loads(out) if out.strip() else None
    return code, report, err


def run_validate_json(artifact_type, filename):
    code, out, err = run_cli(["validate", "--type", artifact_type, "--format", "json", fx(filename)])
    report = json.loads(out) if out.strip() else None
    return code, report, err


def check_ids(items):
    return {item["check_id"] for item in items}


class SchemaValidationTests(unittest.TestCase):
    """REQ-B1 via `validate` (AC-1, AC-2, AC-22, AC-26)."""

    def test_ac01_missing_required_field(self):
        code, report, err = run_validate_json("requirements", "requirements_missing_field.json")
        self.assertEqual(code, 1, msg=err)
        self.assertIn("SCHEMA_INVALID", check_ids(report["findings"]))
        self.assertTrue(any(f["field_path"] == "constraints" for f in report["findings"]))

    def test_ac02_missing_purpose(self):
        code, report, err = run_validate_json("requirements", "requirements_missing_purpose.json")
        self.assertEqual(code, 1, msg=err)
        matches = [f for f in report["findings"] if f["field_path"] == "purpose"]
        self.assertTrue(matches, "expected a SCHEMA_INVALID finding for field_path 'purpose'")
        self.assertEqual(matches[0]["check_id"], "SCHEMA_INVALID")

    def test_ac22_implemented_deviation_empty_related_files(self):
        code, report, err = run_validate_json("implementation", "implementation_implemented_deviation_no_related_files.json")
        self.assertEqual(code, 1, msg=err)
        matches = [f for f in report["findings"] if "related_files" in f["field_path"]]
        self.assertTrue(matches)
        self.assertTrue(all(f["check_id"] == "SCHEMA_INVALID" for f in matches))

    def test_ac26_validate_bad_run_id_format_is_nonfatal(self):
        code, report, err = run_validate_json("requirements", "requirements_bad_run_id_format.json")
        self.assertEqual(code, 1, msg=f"expected non-fatal exit code 1, got {code}; stderr={err}")
        matches = [f for f in report["findings"] if f["field_path"] == "run_id"]
        self.assertTrue(matches)
        self.assertEqual(matches[0]["check_id"], "SCHEMA_INVALID")


class CrossCheckTests(unittest.TestCase):
    """REQ-B2 - REQ-B6 via `check` (AC-3 .. AC-11, AC-16 .. AC-21)."""

    def test_ac03_unauthorized_unresolved_resolution(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_unauthorized_resolution.json", "evaluation_valid.json"
        )
        self.assertIn("UNAUTHORIZED_UNRESOLVED_RESOLUTION", check_ids(report["findings"]), msg=err)
        self.assertEqual(code, 1)

    def test_ac04_authorized_resolution_no_finding(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_valid.json", "evaluation_valid.json"
        )
        self.assertNotIn("UNAUTHORIZED_UNRESOLVED_RESOLUTION", check_ids(report["findings"]), msg=err)

    def test_ac05_ac_not_addressed(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_ac_not_addressed.json", "evaluation_valid.json"
        )
        self.assertIn("AC_NOT_ADDRESSED", check_ids(report["findings"]), msg=err)
        matches = [f for f in report["findings"] if f["check_id"] == "AC_NOT_ADDRESSED"]
        self.assertEqual(matches[0]["related_ids"], ["AC-2"])
        self.assertEqual(code, 1)

    def test_ac06_undeclared_deviation(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_undeclared_deviation.json", "evaluation_valid.json"
        )
        self.assertIn("UNDECLARED_DEVIATION", check_ids(report["findings"]), msg=err)
        self.assertEqual(code, 1)

    def test_ac07_declared_deviation_no_undeclared_finding(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_declared_deviation_covered.json", "evaluation_valid.json"
        )
        self.assertNotIn("UNDECLARED_DEVIATION", check_ids(report["findings"]), msg=err)

    def test_ac08_pass_without_evidence(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_valid.json", "evaluation_pass_without_evidence.json"
        )
        self.assertIn("UNSUPPORTED_PASS_WITHOUT_EVIDENCE", check_ids(report["findings"]), msg=err)
        matches = [f for f in report["findings"] if f["check_id"] == "UNSUPPORTED_PASS_WITHOUT_EVIDENCE"]
        self.assertEqual(len(matches), 2)  # AC-1 (mismatched ref) and AC-2 (empty ref)
        self.assertEqual(code, 1)

    def test_ac09_requirements_run_id_mismatch(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_run_id_mismatch.json", "evaluation_valid.json"
        )
        matches = [
            f
            for f in report["findings"]
            if f["check_id"] == "IDENTIFIER_MISMATCH" and f["field_path"] == "requirements_ref.requirements_run_id"
        ]
        self.assertTrue(matches, msg=err)
        self.assertEqual(code, 1)

    def test_ac10_target_mismatch(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_target_mismatch.json", "evaluation_valid.json"
        )
        self.assertIn("TARGET_MISMATCH", check_ids(report["findings"]), msg=err)
        self.assertEqual(code, 1)

    def test_ac11_status_inconsistency_unapproved_requirements(self):
        code, report, err = run_check_json(
            "requirements_not_approved.json", "implementation_valid.json", "evaluation_valid.json"
        )
        matches = [
            f for f in report["findings"] if f["check_id"] == "STATUS_INCONSISTENCY" and f["artifact"] == "requirements"
        ]
        self.assertTrue(matches, msg=err)
        self.assertEqual(code, 1)

    def test_ac16_target_whitespace_ignored(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_target_whitespace.json", "evaluation_valid.json"
        )
        self.assertNotIn("TARGET_MISMATCH", check_ids(report["findings"]), msg=err)

    def test_ac17_report_preserves_raw_values(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_run_id_ref_whitespace.json", "evaluation_valid.json"
        )
        # format violation is reported (raw, un-trimmed value echoed verbatim)
        matches = [
            f
            for f in report["findings"]
            if f["check_id"] == "SCHEMA_INVALID" and f["field_path"] == "requirements_ref.requirements_run_id"
        ]
        self.assertTrue(matches, msg=err)
        self.assertIn("run-100 ", matches[0]["message"])  # raw value with trailing space preserved
        # normalization prevents a spurious IDENTIFIER_MISMATCH for the same field
        mismatch_matches = [
            f
            for f in report["findings"]
            if f["check_id"] == "IDENTIFIER_MISMATCH" and f["field_path"] == "requirements_ref.requirements_run_id"
        ]
        self.assertEqual(mismatch_matches, [])
        # reference-field format violation must NOT be escalated to fatal in `check`
        self.assertEqual(code, 1, msg=f"expected non-fatal exit code 1, got {code}; stderr={err}")

    def test_ac18_no_deviations_zero_deviation_findings(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_valid.json", "evaluation_valid.json"
        )
        deviation_related = {"UNDECLARED_DEVIATION", "PENDING_UNAPPROVED_DEVIATION", "UNAPPROVED_IMPLEMENTED_DEVIATION"}
        self.assertEqual(check_ids(report["findings"] + report["pending"]) & deviation_related, set(), msg=err)
        self.assertEqual(code, 0)

    def test_ac19_approved_deviation_zero_findings(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_approved_deviation.json", "evaluation_valid.json"
        )
        self.assertEqual(report["findings"], [], msg=err)
        self.assertEqual(report["pending"], [], msg=err)
        self.assertEqual(code, 0)

    def test_ac20_unapproved_proposed_deviation_is_pending(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_unapproved_proposed_deviation.json", "evaluation_valid.json"
        )
        self.assertIn("PENDING_UNAPPROVED_DEVIATION", check_ids(report["pending"]), msg=err)
        self.assertEqual(report["findings"], [])
        self.assertEqual(code, 0)

    def test_ac21_unapproved_implemented_deviation_is_finding(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_unapproved_implemented_deviation.json", "evaluation_valid.json"
        )
        self.assertIn("UNAPPROVED_IMPLEMENTED_DEVIATION", check_ids(report["findings"]), msg=err)
        self.assertEqual(code, 1)


class HappyPathAndFatalErrorTests(unittest.TestCase):
    """AC-12 .. AC-15, AC-25, AC-27."""

    def test_ac12_happy_path_zero_findings_zero_pending(self):
        code, report, err = run_check_json("requirements_valid.json", "implementation_valid.json", "evaluation_valid.json")
        self.assertEqual(report["findings"], [], msg=err)
        self.assertEqual(report["pending"], [], msg=err)
        self.assertEqual(code, 0)
        self.assertEqual(report["summary"]["total_findings"], 0)
        self.assertEqual(report["summary"]["total_pending"], 0)

    def test_ac13_file_not_found(self):
        code, out, err = run_cli(
            [
                "check",
                "--requirements",
                fx("requirements_valid.json"),
                "--implementation",
                fx("this_file_does_not_exist.json"),
                "--evaluation",
                fx("evaluation_valid.json"),
                "--format",
                "json",
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(out.strip(), "", "no report should be generated on a fatal front-gate error")
        self.assertTrue(err.strip())

    def test_ac14_json_syntax_error(self):
        code, out, err = run_cli(
            [
                "check",
                "--requirements",
                fx("invalid_json.json"),
                "--implementation",
                fx("implementation_valid.json"),
                "--evaluation",
                fx("evaluation_valid.json"),
                "--format",
                "json",
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(out.strip(), "")
        self.assertTrue(err.strip())

    def test_ac15_unsupported_schema_version(self):
        code, out, err = run_cli(
            [
                "check",
                "--requirements",
                fx("requirements_unsupported_schema_version.json"),
                "--implementation",
                fx("implementation_valid.json"),
                "--evaluation",
                fx("evaluation_valid.json"),
                "--format",
                "json",
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(out.strip(), "")
        self.assertTrue(err.strip())

    def test_ac25_run_id_duplicate_is_fatal(self):
        code, out, err = run_cli(
            [
                "check",
                "--requirements",
                fx("requirements_valid.json"),
                "--implementation",
                fx("implementation_duplicate_run_id.json"),
                "--evaluation",
                fx("evaluation_valid.json"),
                "--format",
                "json",
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(out.strip(), "")
        self.assertIn("duplicate", err.lower())

    def test_ac27_malformed_duplicate_run_id_is_format_error_not_duplicate(self):
        code, out, err = run_cli(
            [
                "check",
                "--requirements",
                fx("requirements_bad_run_id_format.json"),
                "--implementation",
                fx("implementation_bad_run_id_shared.json"),
                "--evaluation",
                fx("evaluation_valid.json"),
                "--format",
                "json",
            ]
        )
        self.assertEqual(code, 2)
        self.assertEqual(out.strip(), "")
        self.assertNotIn("duplicate run_id", err.lower(), "format check must precede duplicate check (REQ-C2 order)")
        self.assertIn("run-nnn", err.lower())


class CliArgumentTests(unittest.TestCase):
    def test_check_missing_required_argument_exits_2(self):
        code, out, err = run_cli(
            [
                "check",
                "--requirements",
                fx("requirements_valid.json"),
                "--implementation",
                fx("implementation_valid.json"),
                # --evaluation intentionally omitted
                "--format",
                "json",
            ]
        )
        self.assertEqual(code, 2)


class CoverageMetaTest(unittest.TestCase):
    """AC-23: every detection check_id defined by REQ-B has at least one
    dedicated automated test exercising it somewhere in this file."""

    EXPECTED_CHECK_IDS = {
        "SCHEMA_INVALID",
        "UNAUTHORIZED_UNRESOLVED_RESOLUTION",
        "IDENTIFIER_MISMATCH",
        "AC_NOT_ADDRESSED",
        "AC_NOT_TESTED",
        "UNDECLARED_DEVIATION",
        "PENDING_UNAPPROVED_DEVIATION",
        "UNAPPROVED_IMPLEMENTED_DEVIATION",
        "UNSUPPORTED_PASS_WITHOUT_EVIDENCE",
        "STATUS_INCONSISTENCY",
        "TARGET_MISMATCH",
    }

    def test_ac23_all_check_ids_are_exercised(self):
        from handoff_checker import common, cross_checks, schema  # noqa: F401

        # Every check_id string literal used by the implementation.
        import inspect

        source = inspect.getsource(cross_checks) + inspect.getsource(schema)
        used_ids = {cid for cid in self.EXPECTED_CHECK_IDS if f'"{cid}"' in source}
        self.assertEqual(
            used_ids,
            self.EXPECTED_CHECK_IDS,
            "every REQ-B check_id must be implemented and therefore testable",
        )


class BonusCrossCheckCoverageTests(unittest.TestCase):
    """Additional coverage beyond the 27 ACs, for the check_ids that
    REQ-B defines but that are not directly named by an AC number
    (AC_NOT_TESTED, IDENTIFIER_MISMATCH on other fields, the
    completion_status/overall_result STATUS_INCONSISTENCY branch).
    Not required by the AC list, kept to increase confidence."""

    def test_extra_ac_not_tested(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_valid.json", "evaluation_ac_not_tested.json"
        )
        self.assertIn("AC_NOT_TESTED", check_ids(report["findings"]), msg=err)

    def test_extra_completion_status_blocked_but_overall_pass(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_blocked_status.json", "evaluation_valid.json"
        )
        matches = [f for f in report["findings"] if f["check_id"] == "STATUS_INCONSISTENCY" and f["artifact"] == "cross"]
        self.assertTrue(matches, msg=err)

    def test_extra_conditional_pass_requires_residual_risks_not_schema_invalid(self):
        code, report, err = run_check_json(
            "requirements_valid.json", "implementation_valid.json", "evaluation_conditional_pass_no_risks.json"
        )
        status_matches = [
            f for f in report["findings"] if f["check_id"] == "STATUS_INCONSISTENCY" and f["field_path"] == "residual_risks"
        ]
        self.assertTrue(status_matches, msg=err)
        # residual_risks emptiness must NOT also be flagged as SCHEMA_INVALID
        # (REQ-B5 owns this condition exclusively; see schema.py docstring)
        schema_matches = [f for f in report["findings"] if f["check_id"] == "SCHEMA_INVALID" and f["field_path"] == "residual_risks"]
        self.assertEqual(schema_matches, [])


if __name__ == "__main__":
    unittest.main()
