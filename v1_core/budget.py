from dataclasses import dataclass

from .models import BudgetDecision


@dataclass(frozen=True)
class BudgetPolicy:
    warning_jpy: int = 7_000
    restriction_jpy: int = 9_000
    stop_jpy: int = 10_000

    def decide(self, spent_jpy: int, estimated_cost_jpy: int) -> BudgetDecision:
        projected = spent_jpy + estimated_cost_jpy
        if projected >= self.stop_jpy:
            return BudgetDecision.STOP_FOR_APPROVAL
        if projected >= self.restriction_jpy:
            return BudgetDecision.RESTRICT_HIGH_PERFORMANCE
        if projected >= self.warning_jpy:
            return BudgetDecision.WARN
        return BudgetDecision.ALLOW
