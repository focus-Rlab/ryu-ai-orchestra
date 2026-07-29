import unittest

from v1_core import ApprovalRecord, CostKind, Orchestrator, Request, RunState
from v1_core.budget import BudgetPolicy
from v1_core.models import BudgetDecision


def capabilities(artifact_store=None):
    def execute(understood, plan, agent, environment):
        result = {"artifact": "ok"}
        if artifact_store is not None:
            artifact_store.append(result)
        return result

    return dict(
        understand=lambda request: {
            "objective": request.objective,
            "constraints": request.constraints,
        },
        plan=lambda understood: [f"Deliver {understood['objective']}"],
        select=lambda understood, plan: ("worker-agent", "test-environment"),
        execute=execute,
        verify=lambda result: {"passed": result["artifact"] == "ok"},
    )


def approve(core, request, scope, channel="chatgpt"):
    core.record_approval(
        ApprovalRecord(
            request_id=request.id,
            channel=channel,
            approved=True,
            approver="Ryunosuke Matsumoto",
            scope=scope,
        )
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
    def test_free_local_simulated_case_completes_end_to_end(self):
        core = Orchestrator()
        request = Request(objective="produce a private local artifact")
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.COMPLETED)
        self.assertEqual(
            [item["state"] for item in record.history],
            [
                "received",
                "understood",
                "planned",
                "assigned",
                "running",
                "verifying",
                "recorded",
                "completed",
            ],
        )
        self.assertEqual(core.spent_jpy, 0)

    def test_any_positive_cost_is_blocked_without_prior_paid_service_approval(self):
        core = Orchestrator()
        request = Request(objective="one yen task", estimated_cost_jpy=1)
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.BLOCKED)
        self.assertEqual(core.spent_jpy, 0)

    def test_billable_or_unknown_service_is_blocked_even_at_zero_estimated_cost(self):
        for cost_kind in (CostKind.PAID_OR_BILLABLE, CostKind.UNKNOWN):
            with self.subTest(cost_kind=cost_kind):
                core = Orchestrator()
                request = Request(objective="external task", cost_kind=cost_kind)
                record = core.run(request, **capabilities())
                self.assertEqual(record.state, RunState.BLOCKED)

    def test_paid_service_needs_separate_prior_approval_from_budget_override(self):
        core = Orchestrator(spent_jpy=9_500)
        request = Request(
            objective="expensive task",
            estimated_cost_jpy=500,
            cost_kind=CostKind.PAID_OR_BILLABLE,
        )
        approve(core, request, "budget_override")
        blocked = core.run(request, **capabilities())
        self.assertEqual(blocked.state, RunState.BLOCKED)

        approve(core, request, "paid_service")
        completed = core.run(request, **capabilities())
        self.assertEqual(completed.state, RunState.COMPLETED)

    def test_warning_is_recorded_after_paid_service_approval(self):
        core = Orchestrator(spent_jpy=6_900)
        request = Request(objective="warning task", estimated_cost_jpy=100)
        approve(core, request, "paid_service")
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.COMPLETED)
        self.assertEqual(record.verification["budget_decision"], "warn")

    def test_high_performance_environment_is_restricted_at_9000(self):
        core = Orchestrator(spent_jpy=8_900)
        request = Request(objective="restricted task", estimated_cost_jpy=100)
        approve(core, request, "paid_service")
        caps = capabilities()
        caps["select"] = lambda understood, plan: (
            "worker-agent",
            "high-performance",
        )
        record = core.run(request, **caps)
        self.assertEqual(record.state, RunState.BLOCKED)

    def test_each_supported_ai_channel_accepts_ryunosuke_approval(self):
        for channel in ("chatgpt", "gemini", "claude", "codex", "claude code"):
            with self.subTest(channel=channel):
                core = Orchestrator()
                request = Request(objective="protected task", requires_approval=True)
                approve(core, request, "execution", channel=channel)
                record = core.run(request, **capabilities())
                self.assertEqual(record.state, RunState.COMPLETED)

    def test_unaccepted_channel_is_not_formal_approval(self):
        core = Orchestrator()
        request = Request(objective="protected task", requires_approval=True)
        approve(core, request, "execution", channel="github")
        record = core.run(request, **capabilities())
        self.assertEqual(record.state, RunState.BLOCKED)

    def test_ai_or_other_person_cannot_approve_for_ryunosuke(self):
        for approver in ("Claude", "Raphael", "focus-RLab"):
            with self.subTest(approver=approver):
                core = Orchestrator()
                request = Request(objective="protected task", requires_approval=True)
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

    def test_rollback_reverses_registered_side_effect_and_cost(self):
        artifacts = []
        core = Orchestrator(spent_jpy=100)
        request = Request(objective="reversible task", estimated_cost_jpy=50)
        approve(core, request, "paid_service")
        caps = capabilities(artifacts)
        caps["undo"] = lambda result: artifacts.remove(result) or "artifact removed"
        record = core.run(request, **caps)
        self.assertEqual(core.spent_jpy, 150)
        self.assertEqual(len(artifacts), 1)

        core.rollback(record.request.id)
        self.assertEqual(core.spent_jpy, 100)
        self.assertEqual(artifacts, [])
        self.assertEqual(record.rollback_result, "artifact removed")
        self.assertEqual(record.state, RunState.ROLLED_BACK)


    def test_rollback_handler_failure_does_not_claim_success(self):
        core = Orchestrator(spent_jpy=100)
        request = Request(objective="reversible", estimated_cost_jpy=50)
        approve(core, request, "paid_service")
        caps = capabilities()
        caps["undo"] = lambda result: (_ for _ in ()).throw(RuntimeError("undo failed"))
        record = core.run(request, **caps)
        core.rollback(request.id)
        self.assertEqual(record.state, RunState.ROLLBACK_FAILED)
        self.assertIn("RuntimeError", record.rollback_error)
        self.assertEqual(core.spent_jpy, 150)

    def test_missing_rollback_handler_does_not_claim_reversal(self):
        core = Orchestrator()
        request = Request(objective="produces result")
        record = core.run(request, **capabilities())
        with self.assertRaisesRegex(ValueError, "No rollback handler"):
            core.rollback(request.id)
        self.assertEqual(record.state, RunState.COMPLETED)

    def test_double_rollback_is_rejected(self):
        artifacts = []
        core = Orchestrator()
        request = Request(objective="reversible")
        caps = capabilities(artifacts)
        caps["undo"] = lambda result: artifacts.remove(result)
        record = core.run(request, **caps)
        core.rollback(request.id)
        self.assertEqual(record.state, RunState.ROLLED_BACK)
        with self.assertRaisesRegex(ValueError, "already completed"):
            core.rollback(request.id)


if __name__ == "__main__":
    unittest.main()
