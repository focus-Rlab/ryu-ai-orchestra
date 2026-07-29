import unittest

from v1_core import ApprovalRecord, Orchestrator, Request, RunState
from v1_core.budget import BudgetPolicy
from v1_core.models import BudgetDecision


def capabilities():
    return dict(
        understand=lambda request: {
            "objective": request.objective,
            "constraints": request.constraints,
        },
        plan=lambda understood: [f"Deliver {understood['objective']}"],
        select=lambda understood, plan: ("worker-agent", "test-environment"),
        execute=lambda understood, plan, agent, environment: {"artifact": "ok"},
        verify=lambda result: {"passed": result["artifact"] == "ok"},
    )


class BudgetPolicyTest(unittest.TestCase):
    def test_all_thresholds(self):
        policy = BudgetPolicy()
        self.assertEqual(policy.decide(0, 6_999), BudgetDecision.ALLOW)
        self.assertEqual(policy.decide(0, 7_000), BudgetDecision.WARN)
        self.assertEqual(
            policy.decide(0, 9_000), BudgetDecision.RESTRICT_HIGH_PERFORMANCE
        )
        self.assertEqual(
            policy.decide(0, 10_000), BudgetDecision.STOP_FOR_APPROVAL
        )


class OrchestratorTest(unittest.TestCase):
    def test_happy_path_is_domain_neutral(self):
        core = Orchestrator()
        request = Request(objective="produce a private artifact", estimated_cost_jpy=10)
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.COMPLETED)
        self.assertEqual(record.agent, "worker-agent")
        self.assertEqual(core.spent_jpy, 10)

    def test_budget_stop_requires_ryunosuke_approval(self):
        core = Orchestrator(spent_jpy=9_500)
        request = Request(objective="expensive task", estimated_cost_jpy=500)
        blocked = core.run(request, **capabilities())
        self.assertEqual(blocked.state, RunState.BLOCKED)

        core.record_approval(
            ApprovalRecord(
                request_id=request.id,
                channel="chatgpt",
                approved=True,
                approver="Ryunosuke Matsumoto",
                scope="budget_override",
            )
        )
        completed = core.run(request, **capabilities())
        self.assertEqual(completed.state, RunState.COMPLETED)

    def test_warning_is_recorded_without_blocking(self):
        core = Orchestrator(spent_jpy=6_900)
        request = Request(objective="warning task", estimated_cost_jpy=100)
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.COMPLETED)
        self.assertEqual(record.verification["budget_decision"], "warn")

    def test_high_performance_environment_is_restricted_at_9000(self):
        core = Orchestrator(spent_jpy=8_900)
        request = Request(objective="restricted task", estimated_cost_jpy=100)
        caps = capabilities()
        caps["select"] = lambda understood, plan: (
            "worker-agent",
            "high-performance",
        )
        record = core.run(request, **caps)
        self.assertEqual(record.state, RunState.BLOCKED)
        self.assertEqual(
            record.verification["budget_decision"], "restrict_high_performance"
        )

    def test_each_supported_ai_channel_accepts_ryunosuke_approval(self):
        for channel in ("chatgpt", "gemini", "claude", "codex", "claude code"):
            with self.subTest(channel=channel):
                core = Orchestrator()
                request = Request(
                    objective="protected task", requires_approval=True
                )
                core.record_approval(
                    ApprovalRecord(
                        request_id=request.id,
                        channel=channel,
                        approved=True,
                        approver="Ryunosuke Matsumoto",
                        scope="execution",
                    )
                )
                record = core.run(request, **capabilities())
                self.assertEqual(record.state, RunState.COMPLETED)

    def test_unaccepted_channel_is_not_formal_approval(self):
        core = Orchestrator()
        request = Request(objective="protected task", requires_approval=True)
        core.record_approval(
            ApprovalRecord(
                request_id=request.id,
                channel="github",
                approved=True,
                approver="Ryunosuke Matsumoto",
                scope="execution",
            )
        )
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.BLOCKED)

    def test_ai_or_other_person_cannot_approve_for_ryunosuke(self):
        for approver in ("Claude", "Raphael", "focus-RLab"):
            with self.subTest(approver=approver):
                core = Orchestrator()
                request = Request(
                    objective="protected task", requires_approval=True
                )
                core.record_approval(
                    ApprovalRecord(
                        request_id=request.id,
                        channel="claude",
                        approved=True,
                        approver=approver,
                        scope="execution",
                    )
                )
                record = core.run(request, **capabilities())
                self.assertEqual(record.state, RunState.BLOCKED)

    def test_failed_verification_records_improvement(self):
        core = Orchestrator()
        request = Request(objective="bad output")
        caps = capabilities()
        caps["verify"] = lambda result: {"passed": False, "reason": "mismatch"}
        record = core.run(request, **caps)
        self.assertEqual(record.state, RunState.FAILED)
        self.assertEqual(len(record.improvements), 1)

    def test_rollback_restores_cost(self):
        core = Orchestrator(spent_jpy=100)
        request = Request(objective="reversible task", estimated_cost_jpy=50)
        record = core.run(request, **capabilities())
        self.assertEqual(core.spent_jpy, 150)
        core.rollback(record.request.id)
        self.assertEqual(core.spent_jpy, 100)
        self.assertEqual(record.state, RunState.ROLLED_BACK)


if __name__ == "__main__":
    unittest.main()
