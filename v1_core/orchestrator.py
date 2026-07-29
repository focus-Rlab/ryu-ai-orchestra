from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from typing import Any

from .approvals import has_formal_approval
from .budget import BudgetPolicy
from .models import (
    ApprovalRecord,
    BudgetDecision,
    CostKind,
    ImprovementCandidate,
    Request,
    RunRecord,
    RunState,
)


class Orchestrator:
    """Domain-neutral minimum execution loop."""

    def __init__(self, spent_jpy: int = 0, budget_policy: BudgetPolicy | None = None):
        self.spent_jpy = spent_jpy
        self.budget_policy = budget_policy or BudgetPolicy()
        self.approvals: list[ApprovalRecord] = []
        self.runs: dict[str, RunRecord] = {}
        self._rollback_handlers: dict[str, Callable[[Any], Any]] = {}

    def record_approval(self, approval: ApprovalRecord) -> None:
        self.approvals.append(approval)

    def run(
        self,
        request: Request,
        *,
        understand: Callable[[Request], dict[str, Any]],
        plan: Callable[[dict[str, Any]], list[str]],
        select: Callable[[dict[str, Any], list[str]], tuple[str, str]],
        execute: Callable[[dict[str, Any], list[str], str, str], Any],
        verify: Callable[[Any], dict[str, Any]],
        undo: Callable[[Any], Any] | None = None,
    ) -> RunRecord:
        record = RunRecord(request=request)
        self.runs[request.id] = record
        record.transition(RunState.RECEIVED, "Request normalized")

        paid_or_uncertain = (
            request.estimated_cost_jpy > 0
            or request.cost_kind in {CostKind.PAID_OR_BILLABLE, CostKind.UNKNOWN}
        )
        record.verification["cost_kind"] = request.cost_kind.value
        if paid_or_uncertain and not has_formal_approval(
            request.id, "paid_service", self.approvals
        ):
            record.transition(
                RunState.BLOCKED,
                "Paid, billable, or cost-uncertain service requires Ryunosuke's prior explicit approval",
            )
            return record

        decision = self.budget_policy.decide(
            self.spent_jpy, request.estimated_cost_jpy
        )
        record.verification["budget_decision"] = decision.value
        if decision is BudgetDecision.STOP_FOR_APPROVAL and not has_formal_approval(
            request.id, "budget_override", self.approvals
        ):
            record.transition(
                RunState.BLOCKED,
                "Budget stop requires Ryunosuke approval through an accepted AI channel",
            )
            return record

        if request.requires_approval and not has_formal_approval(
            request.id, "execution", self.approvals
        ):
            record.transition(
                RunState.BLOCKED,
                "Execution requires Ryunosuke approval through an accepted AI channel",
            )
            return record

        understood = understand(request)
        record.transition(RunState.UNDERSTOOD, "Objective and constraints understood")
        record.plan = plan(understood)
        record.transition(RunState.PLANNED, "Plan created")
        record.agent, record.environment = select(understood, record.plan)
        record.transition(RunState.ASSIGNED, "Agent and environment selected")
        if (
            decision is BudgetDecision.RESTRICT_HIGH_PERFORMANCE
            and record.environment.lower() == "high-performance"
        ):
            record.transition(
                RunState.BLOCKED,
                "High-performance environment restricted at projected budget",
            )
            return record

        record.rollback_snapshot = deepcopy(
            {"spent_jpy": self.spent_jpy, "state": record.state.value}
        )
        if undo is not None:
            self._rollback_handlers[request.id] = undo
        try:
            record.transition(RunState.RUNNING, "Execution started")
            record.result = execute(
                understood, record.plan, record.agent, record.environment
            )
            self.spent_jpy += request.estimated_cost_jpy
            record.transition(RunState.VERIFYING, "Result submitted for verification")
            record.verification.update(verify(record.result))
            if not record.verification.get("passed", False):
                record.transition(RunState.FAILED, "Verification failed")
                record.improvements.append(
                    ImprovementCandidate(
                        title="Verification failure",
                        evidence=str(record.verification),
                        proposed_change="Review the injected capability or plan.",
                    )
                )
                return record
            record.transition(RunState.RECORDED, "Evidence and result recorded")
            record.transition(RunState.COMPLETED, "Execution loop completed")
            return record
        except Exception as exc:
            record.verification["error"] = repr(exc)
            record.transition(RunState.FAILED, "Execution raised an exception")
            return record

    def rollback(self, request_id: str) -> RunRecord:
        record = self.runs[request_id]
        if record.rollback_snapshot is None:
            raise ValueError("No rollback snapshot exists")
        handler = self._rollback_handlers.get(request_id)
        if handler is not None and record.result is not None:
            record.rollback_result = handler(record.result)
        self.spent_jpy = int(record.rollback_snapshot["spent_jpy"])
        record.transition(
            RunState.ROLLED_BACK,
            "Registered side effects reversed and budget state restored",
        )
        return record
