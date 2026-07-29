from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class RunState(str, Enum):
    RECEIVED = "received"
    UNDERSTOOD = "understood"
    PLANNED = "planned"
    ASSIGNED = "assigned"
    RUNNING = "running"
    BLOCKED = "blocked"
    VERIFYING = "verifying"
    RECORDED = "recorded"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


class BudgetDecision(str, Enum):
    ALLOW = "allow"
    WARN = "warn"
    RESTRICT_HIGH_PERFORMANCE = "restrict_high_performance"
    STOP_FOR_APPROVAL = "stop_for_approval"


class CostKind(str, Enum):
    LOCAL_FREE = "local_free"
    GUARANTEED_FREE = "guaranteed_free"
    PAID_OR_BILLABLE = "paid_or_billable"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class Request:
    objective: str
    constraints: tuple[str, ...] = ()
    domain: str | None = None
    estimated_cost_jpy: int = 0
    cost_kind: CostKind = CostKind.LOCAL_FREE
    requires_approval: bool = False
    id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True)
class ApprovalRecord:
    request_id: str
    channel: str
    approved: bool
    approver: str
    scope: str
    recorded_at: str = field(default_factory=utc_now)


@dataclass(frozen=True)
class ImprovementCandidate:
    title: str
    evidence: str
    proposed_change: str


@dataclass
class RunRecord:
    request: Request
    state: RunState = RunState.RECEIVED
    plan: list[str] = field(default_factory=list)
    agent: str | None = None
    environment: str | None = None
    result: Any = None
    verification: dict[str, Any] = field(default_factory=dict)
    improvements: list[ImprovementCandidate] = field(default_factory=list)
    history: list[dict[str, str]] = field(default_factory=list)
    rollback_snapshot: dict[str, Any] | None = None
    rollback_result: Any = None

    def transition(self, state: RunState, note: str) -> None:
        self.state = state
        self.history.append({"at": utc_now(), "state": state.value, "note": note})
