from __future__ import annotations

from collections.abc import Callable
from typing import Any

from v1_core.models import Request

from .evaluation import evaluate_software_result
from .models import (
    SoftwareCapability,
    SoftwareSelection,
    SoftwareTask,
    SoftwareWorkKind,
)
from .tools import LOCAL_SOFTWARE_TOOLS


CAPABILITIES: tuple[SoftwareCapability, ...] = (
    SoftwareCapability(
        id="software-analysis",
        agent_role="software-engineer",
        work_kinds=(SoftwareWorkKind.REVIEW,),
        required_tools=("rg", "git-diff"),
        description="Inspect requirements, architecture boundaries, and repository changes.",
    ),
    SoftwareCapability(
        id="python-implementation",
        agent_role="software-engineer",
        work_kinds=(SoftwareWorkKind.IMPLEMENTATION,),
        required_tools=("rg", "git-diff", "python-compile"),
        description="Implement small Python changes inside an approved work branch.",
    ),
    SoftwareCapability(
        id="python-verification",
        agent_role="software-quality-reviewer",
        work_kinds=(SoftwareWorkKind.TESTING,),
        required_tools=("python-unittest", "python-compile", "git-diff"),
        description="Verify Python behavior, compilation, and change isolation.",
    ),
    SoftwareCapability(
        id="technical-documentation",
        agent_role="software-engineer",
        work_kinds=(SoftwareWorkKind.DOCUMENTATION,),
        required_tools=("rg", "git-diff"),
        description="Record software design, evidence, and handoff state.",
    ),
)


class SoftwareDomainPack:
    """Software policy and capability selection kept outside the generic core."""

    domain = "software"

    def understand(self, request: Request) -> SoftwareTask:
        if request.domain not in (None, self.domain):
            raise ValueError(f"Software pack cannot handle domain={request.domain!r}")

        objective = request.objective.lower()
        work_kinds: list[SoftwareWorkKind] = [SoftwareWorkKind.REVIEW]
        if any(word in objective for word in ("implement", "build", "improve", "fix")):
            work_kinds.append(SoftwareWorkKind.IMPLEMENTATION)
        if any(word in objective for word in ("test", "verify", "improve", "fix")):
            work_kinds.append(SoftwareWorkKind.TESTING)
        if any(word in objective for word in ("document", "record", "improve")):
            work_kinds.append(SoftwareWorkKind.DOCUMENTATION)

        ordered_kinds = tuple(dict.fromkeys(work_kinds))
        capability_ids = tuple(
            capability.id
            for capability in CAPABILITIES
            if any(kind in capability.work_kinds for kind in ordered_kinds)
        )
        return SoftwareTask(
            objective=request.objective,
            constraints=request.constraints,
            work_kinds=ordered_kinds,
            required_capabilities=capability_ids,
        )

    def plan(self, task: SoftwareTask) -> list[str]:
        steps = [
            "Inspect software requirements and repository boundaries",
            "Select the minimum software capabilities and local tools",
        ]
        if SoftwareWorkKind.IMPLEMENTATION in task.work_kinds:
            steps.append("Implement the isolated software change")
        if SoftwareWorkKind.TESTING in task.work_kinds:
            steps.append("Run software-specific verification")
        if SoftwareWorkKind.DOCUMENTATION in task.work_kinds:
            steps.append("Record evidence and improvement comparison")
        return steps

    def select(self, task: SoftwareTask, plan: list[str]) -> tuple[str, str]:
        del plan
        selected = self.selection_for(task)
        return selected.agent_role, selected.environment

    def selection_for(self, task: SoftwareTask) -> SoftwareSelection:
        selected = tuple(
            capability
            for capability in CAPABILITIES
            if capability.id in task.required_capabilities
        )
        tool_ids = tuple(
            dict.fromkeys(
                tool_id
                for capability in selected
                for tool_id in capability.required_tools
            )
        )
        for tool_id in tool_ids:
            tool = LOCAL_SOFTWARE_TOOLS[tool_id]
            if tool.network_access or tool.cost_kind.value != "local_free":
                raise ValueError(f"Non-local-free tool selected: {tool_id}")
        roles = {capability.agent_role for capability in selected}
        agent_role = (
            "software-engineer"
            if "software-engineer" in roles
            else "software-quality-reviewer"
        )
        return SoftwareSelection(
            agent_role=agent_role,
            environment="local-python",
            capability_ids=tuple(capability.id for capability in selected),
            tool_ids=tool_ids,
        )

    def callbacks(
        self,
        execute_case: Callable[
            [SoftwareTask, list[str], SoftwareSelection], dict[str, Any]
        ],
    ) -> dict[str, Callable[..., Any]]:
        selections: dict[int, SoftwareSelection] = {}

        def select(task: SoftwareTask, plan: list[str]) -> tuple[str, str]:
            selection = self.selection_for(task)
            selections[id(task)] = selection
            return selection.agent_role, selection.environment

        def execute(
            task: SoftwareTask,
            plan: list[str],
            agent: str,
            environment: str,
        ) -> dict[str, Any]:
            selection = selections[id(task)]
            if (agent, environment) != (
                selection.agent_role,
                selection.environment,
            ):
                raise ValueError("Core assignment differs from software selection")
            return execute_case(task, plan, selection)

        return {
            "understand": self.understand,
            "plan": self.plan,
            "select": select,
            "execute": execute,
            "verify": lambda result: evaluate_software_result(
                result
            ).as_verification(),
        }
