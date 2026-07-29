import unittest

from software_domain import SoftwareDomainPack, evaluate_software_result
from software_domain.models import SoftwareWorkKind
from software_domain.tools import LOCAL_SOFTWARE_TOOLS
from v1_core import Orchestrator, Request, RunState
from v1_core.models import CostKind


def successful_case(task, plan, selection):
    return {
        "domain_pack": "software",
        "objective": task.objective,
        "plan": plan,
        "selection": {
            "agent_role": selection.agent_role,
            "environment": selection.environment,
            "capability_ids": selection.capability_ids,
            "tool_ids": selection.tool_ids,
        },
        "paid_services_used": False,
        "tests_passed": True,
        "generic_core_unchanged": True,
        "evidence": {"comparison": "baseline lacked a software adapter"},
    }


class SoftwareDomainPackTest(unittest.TestCase):
    def setUp(self):
        self.pack = SoftwareDomainPack()

    def test_understands_self_improvement_as_software_work(self):
        task = self.pack.understand(
            Request(
                objective="Improve, test, and document Raphael software design",
                domain="software",
            )
        )
        self.assertIn(SoftwareWorkKind.IMPLEMENTATION, task.work_kinds)
        self.assertIn(SoftwareWorkKind.TESTING, task.work_kinds)
        self.assertIn(SoftwareWorkKind.DOCUMENTATION, task.work_kinds)

    def test_rejects_non_software_domain(self):
        with self.assertRaises(ValueError):
            self.pack.understand(
                Request(objective="write a novel", domain="fiction")
            )

    def test_selection_uses_only_registered_local_free_tools(self):
        task = self.pack.understand(
            Request(objective="Improve and test Raphael", domain="software")
        )
        selection = self.pack.selection_for(task)
        self.assertEqual(selection.environment, "local-python")
        self.assertTrue(selection.tool_ids)
        for tool_id in selection.tool_ids:
            tool = LOCAL_SOFTWARE_TOOLS[tool_id]
            self.assertEqual(tool.cost_kind, CostKind.LOCAL_FREE)
            self.assertFalse(tool.network_access)

    def test_generic_core_runs_with_injected_software_callbacks(self):
        core = Orchestrator()
        request = Request(
            objective="Improve, test, and document Raphael software design",
            domain="software",
        )
        record = core.run(request, **self.pack.callbacks(successful_case))
        self.assertEqual(record.state, RunState.COMPLETED)
        self.assertEqual(record.agent, "software-engineer")
        self.assertEqual(record.environment, "local-python")
        self.assertTrue(record.verification["passed"])
        self.assertEqual(core.spent_jpy, 0)

    def test_evaluation_fails_when_generic_core_was_changed(self):
        result = successful_case(
            self.pack.understand(
                Request(objective="Improve Raphael", domain="software")
            ),
            [],
            self.pack.selection_for(
                self.pack.understand(
                    Request(objective="Improve Raphael", domain="software")
                )
            ),
        )
        result["generic_core_unchanged"] = False
        evaluation = evaluate_software_result(result)
        self.assertFalse(evaluation.passed)
        self.assertFalse(evaluation.checks["generic_core_unchanged"])

    def test_evaluation_fails_when_paid_service_was_used(self):
        task = self.pack.understand(
            Request(objective="Improve Raphael", domain="software")
        )
        result = successful_case(task, [], self.pack.selection_for(task))
        result["paid_services_used"] = True
        self.assertFalse(evaluate_software_result(result).passed)


if __name__ == "__main__":
    unittest.main()
