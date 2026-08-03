import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_action_gate import INCIDENT_STEPS, validate


def valid_record():
    return {
        "task": "correct a process failure",
        "action": "update controls and tests",
        "action_type": "incident_response",
        "canonical_files_read": ["STARTUP_CONTEXT.md", "GOVERNANCE.md"],
        "applicable_rules": ["GOVERNANCE.md section 9"],
        "assignment_decision": {
            "use_agents": True,
            "rationale": "independent review reduces recurrence risk",
            "assignments": ["incident auditor", "control reviewer"],
            "execution_evidence": ["/root/incident_auditor", "/root/control_reviewer"],
        },
        "required_checks": ["success", "failure", "similar case"],
        "stop_conditions": ["meaning change requires approval"],
        "incident_steps": sorted(INCIDENT_STEPS),
    }


class ActionGateTests(unittest.TestCase):
    def test_complete_incident_plan_passes(self):
        self.assertEqual(validate(valid_record()), [])

    def test_read_files_without_applicable_rules_fails(self):
        record = valid_record()
        record["applicable_rules"] = []
        self.assertIn("applicable_rules must not be empty", validate(record))

    def test_agent_name_without_real_assignment_fails(self):
        record = valid_record()
        record["assignment_decision"]["assignments"] = []
        self.assertIn(
            "agent assignments are required when use_agents is true", validate(record)
        )

    def test_agent_assignment_without_execution_evidence_fails(self):
        record = valid_record()
        record["assignment_decision"].pop("execution_evidence")
        self.assertIn(
            "agent execution evidence is required when use_agents is true", validate(record)
        )

    def test_incomplete_incident_flow_fails_closed(self):
        record = valid_record()
        record["incident_steps"] = ["root_cause", "incident_record"]
        self.assertTrue(any("incident steps missing:" in e for e in validate(record)))

    def test_similar_non_incident_action_can_pass_without_agents(self):
        record = valid_record()
        record["action_type"] = "documentation_correction"
        record.pop("incident_steps")
        record["assignment_decision"] = {
            "use_agents": False,
            "rationale": "a bounded wording correction has no independent workstream",
        }
        self.assertEqual(validate(record), [])

    def test_unverified_completion_claim_fails(self):
        record = valid_record()
        record["action_type"] = "completion_claim"
        record.pop("incident_steps")
        record["completion_evidence"] = {"verified": [], "unverified_scope": ["visual QA"]}
        self.assertIn(
            "completion evidence must include verified checks", validate(record)
        )

    def test_completion_claim_with_explicit_limits_passes(self):
        record = valid_record()
        record["action_type"] = "completion_claim"
        record.pop("incident_steps")
        record["completion_evidence"] = {
            "verified": ["unit tests"],
            "unverified_scope": ["visual QA"],
        }
        self.assertEqual(validate(record), [])


if __name__ == "__main__":
    unittest.main()
