import unittest

from scripts.check_action_gate import INCIDENT_STEPS, validate

REGISTRY = {"incidents": {"prior-1": {"root_cause_id": "same-root", "confirmed_occurrences": 1}}}


def evidence(ref="record"):
    return [{"type": "file", "ref": "GOVERNANCE.md", "result": f"verified:{ref}"}]


def completed_steps():
    return {
        step: {"status": "complete", "evidence": evidence(f"evidence:{step}")}
        for step in INCIDENT_STEPS
    }


def valid_record():
    return {
        "gate_version": 2,
        "task": "correct a process failure",
        "action": "update controls and tests",
        "action_type": "incident_response",
        "mistake_detected": True,
        "classification_basis": "User report and incident evidence confirm a mistake",
        "rule_coverage": [
            {"category": category, "status": "applicable", "reason": "required scan", "control": "gate", "evidence": "test"}
            for category in ("security", "authority", "quality", "user_communication", "state_sync", "delivery", "recovery", "agent_design")
        ],
        "deliverable_handoff": {"required": False},
        "feedback_capture": {"reviewed": True, "classification": ["mistake"]},
        "mistake_triggers": [{"type": "user_report", "evidence": [{"type": "user_report", "ref": "conversation", "result": "mistake confirmed"}]}],
        "mistake": {
            "classification": "major",
            "occurrence_count": 1,
            "root_cause_id": "instruction-application-gap",
            "prior_mistake_refs": [],
        },
        "canonical_files_read": ["STARTUP_CONTEXT.md", "GOVERNANCE.md"],
        "applicable_rules": ["GOVERNANCE.md section 9"],
        "assignment_decision": {
            "use_agents": True,
            "rationale": "independent review reduces recurrence risk",
            "assignments": ["incident auditor"],
            "execution_evidence": ["auditor report"],
        },
        "required_checks": ["success", "failure", "similar case"],
        "stop_conditions": ["meaning change requires approval"],
        "incident_steps": completed_steps(),
    }


class ActionGateTests(unittest.TestCase):
    def test_complete_incident_plan_passes(self):
        self.assertEqual(validate(valid_record()), [])

    def test_general_mistake_requires_full_response_flow(self):
        record = valid_record()
        record["mistake"] = {"classification": "general", "occurrence_count": 1, "root_cause_id": "x", "prior_mistake_refs": []}
        record["incident_steps"] = {"classify": {"status": "complete", "evidence": evidence("classification")}}
        self.assertTrue(any("incident steps missing:" in e for e in validate(record)))

    def test_mistake_cannot_hide_as_documentation_correction(self):
        record = valid_record()
        record["action_type"] = "documentation_correction"
        self.assertIn("mistake_detected actions must use a mistake response action_type", validate(record))

    def test_non_mistake_documentation_correction_passes(self):
        record = valid_record()
        record["action_type"] = "documentation_correction"
        record["mistake_detected"] = False
        record["classification_basis"] = "Spelling-only improvement; no incorrect prior action"
        record["mistake_triggers"] = [{"type": "none", "evidence": evidence("diff review")}]
        record.pop("mistake")
        record.pop("incident_steps")
        record["assignment_decision"] = {"use_agents": False, "rationale": "bounded spelling change"}
        self.assertEqual(validate(record), [])

    def test_second_occurrence_cannot_remain_general(self):
        record = valid_record()
        record["mistake"] = {"classification": "general", "occurrence_count": 2, "root_cause_id": "same-root", "prior_mistake_refs": [{"incident_id": "prior-1"}]}
        self.assertIn("a repeated mistake cannot remain classified as general", validate(record, REGISTRY))

    def test_repeated_mistake_requires_prior_reference(self):
        record = valid_record()
        record["mistake"] = {"classification": "repeated", "occurrence_count": 2, "root_cause_id": "same-root", "prior_mistake_refs": []}
        self.assertIn("repeated mistakes require prior_mistake_refs", validate(record, REGISTRY))

    def test_fake_prior_reference_fails(self):
        record = valid_record()
        record["mistake"] = {"classification": "repeated", "occurrence_count": 2, "root_cause_id": "same-root", "prior_mistake_refs": [{"incident_id": "fake"}]}
        self.assertIn("prior mistake reference is not present in the incident registry", validate(record, REGISTRY))

    def test_step_name_without_evidence_fails(self):
        record = valid_record()
        record["incident_steps"]["root_cause"] = {"status": "complete", "evidence": [{"type": "file", "ref": "x", "result": ""}]}
        self.assertIn("incident step root_cause requires complete status and structured evidence", validate(record))

    def test_mistake_false_with_user_report_fails(self):
        record = valid_record()
        record["mistake_detected"] = False
        record["action_type"] = "documentation_correction"
        record.pop("mistake"); record.pop("incident_steps")
        self.assertIn("confirmed mistake triggers require mistake_detected true", validate(record))

    def test_missing_cli_without_complete_inventory_fails(self):
        record = self.impossibility_record()
        record["execution_path_inventory"]["inventory_complete"] = False
        self.assertIn("execution path inventory must be explicitly complete", validate(record))

    def test_unknown_path_status_fails(self):
        record = self.impossibility_record()
        record["execution_path_inventory"]["paths"][0]["status"] = "unknown"
        self.assertIn("execution path status is invalid or unresolved", validate(record))

    def test_available_connector_blocks_impossibility_claim(self):
        record = self.impossibility_record()
        record["execution_path_inventory"]["paths"].append({
            "class": "configured_connector", "path": "duplicate connector", "status": "available", "reason": "write tools exposed",
            "evidence": evidence("tool registry"), "outcome_equivalent": True, "authorized": True,
        })
        self.assertIn("work cannot be called impossible while an authorized equivalent path is available", validate(record))

    def test_exhausted_complete_inventory_passes(self):
        self.assertEqual(validate(self.impossibility_record()), [])

    def test_single_path_self_declared_complete_fails(self):
        record = self.impossibility_record()
        record["execution_path_inventory"]["paths"] = record["execution_path_inventory"]["paths"][:1]
        self.assertTrue(any("execution path classes missing:" in e for e in validate(record)))

    def test_read_files_without_applicable_rules_fails(self):
        record = valid_record(); record["applicable_rules"] = []
        self.assertIn("applicable_rules must not be empty", validate(record))

    def test_agent_assignment_without_evidence_fails(self):
        record = valid_record(); record["assignment_decision"].pop("execution_evidence")
        self.assertIn("agent execution evidence is required when use_agents is true", validate(record))

    def test_completion_claim_requires_evidence(self):
        record = valid_record()
        record["action_type"] = "completion_claim"; record["mistake_detected"] = False
        record.pop("mistake"); record.pop("incident_steps")
        record["completion_evidence"] = {"verified": [], "unverified_scope": ["visual QA"]}
        self.assertIn("completion evidence must include verified checks", validate(record))

    def test_rule_scan_cannot_omit_delivery(self):
        record = valid_record()
        record["rule_coverage"] = [item for item in record["rule_coverage"] if item["category"] != "delivery"]
        self.assertTrue(any("rule coverage categories missing:" in e for e in validate(record)))

    def test_completion_cannot_claim_unshared_app(self):
        record = valid_record()
        record["action_type"] = "completion_claim"; record["mistake_detected"] = False
        record.pop("mistake"); record.pop("incident_steps")
        record["completion_evidence"] = {"verified": ["internal tests"], "unverified_scope": []}
        record["deliverable_handoff"] = {"required": True, "medium": "public URL", "acceptance_check": "user opens app"}
        self.assertIn("completion claim requires user-access evidence for deliverable handoff", validate(record))

    def test_reviewed_feedback_requires_classification(self):
        record = valid_record(); record["feedback_capture"] = {"reviewed": True}
        self.assertIn("reviewed feedback requires a classification", validate(record))

    @staticmethod
    def impossibility_record():
        record = valid_record()
        record["action_type"] = "impossibility_claim"; record["mistake_detected"] = False
        record["classification_basis"] = "No prior error; assessing present feasibility"
        record["mistake_triggers"] = [{"type": "none", "evidence": evidence("feasibility assessment")}]
        record.pop("mistake"); record.pop("incident_steps")
        record["execution_path_inventory"] = {
            "scope_basis": "Repository workflow and available tool registry were inspected",
            "inventory_complete": True,
            "paths": [
                {"class": "requested_tool", "path": "gh CLI", "status": "unavailable", "reason": "not installed", "evidence": evidence("gh --version"), "outcome_equivalent": True, "authorized": True},
                {"class": "configured_connector", "path": "GitHub connector", "status": "unavailable", "reason": "write denied", "evidence": evidence("permission response"), "outcome_equivalent": True, "authorized": True},
                {"class": "api", "path": "GitHub API", "status": "not_authorized", "reason": "no token", "evidence": evidence("credential inventory"), "outcome_equivalent": True, "authorized": False},
                {"class": "local_vcs", "path": "git push", "status": "unavailable", "reason": "no write credential", "evidence": evidence("git push result"), "outcome_equivalent": True, "authorized": True},
                {"class": "browser", "path": "GitHub web UI", "status": "unavailable", "reason": "no browser session", "evidence": evidence("browser inventory"), "outcome_equivalent": True, "authorized": True},
                {"class": "manual_handoff", "path": "user handoff", "status": "not_equivalent", "reason": "does not complete requested action", "evidence": evidence("outcome comparison"), "outcome_equivalent": False, "authorized": True},
            ],
        }
        return record


if __name__ == "__main__":
    unittest.main()
