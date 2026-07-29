from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SoftwareEvaluation:
    passed: bool
    checks: dict[str, bool]
    evidence: dict[str, Any]

    def as_verification(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "checks": self.checks,
            "evidence": self.evidence,
        }


def evaluate_software_result(result: dict[str, Any]) -> SoftwareEvaluation:
    """Evaluate only Week 2's approved invariants, without unapproved scoring."""

    checks = {
        "software_pack_used": result.get("domain_pack") == "software",
        "capabilities_selected": bool(result.get("selection", {}).get("capability_ids")),
        "local_free_tools_only": result.get("paid_services_used") is False,
        "tests_passed": result.get("tests_passed") is True,
        "generic_core_unchanged": result.get("generic_core_unchanged") is True,
        "evidence_recorded": bool(result.get("evidence")),
    }
    return SoftwareEvaluation(
        passed=all(checks.values()),
        checks=checks,
        evidence=result.get("evidence", {}),
    )
