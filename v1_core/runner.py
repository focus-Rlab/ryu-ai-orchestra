from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from .models import utc_now


@dataclass(frozen=True)
class TaskContract:
    task_id: str
    objective: str
    task_type: str
    requirements: tuple[str, ...]
    created_at: str


@dataclass
class CompletionDecision:
    passed: bool
    missing: list[str] = field(default_factory=list)


class RaphaelRunner:
    """Small, portable gate between a request and a completion claim.

    Runtime records are plain JSON so the same contract can be checked from
    Codex, Claude Code, GitHub Actions, or a future execution environment.
    """

    GENERAL_REQUIREMENTS = ("result_evidence",)
    VISUAL_REQUIREMENTS = (
        "user_access_evidence",
        "user_acceptance_passed",
    )

    def __init__(self, run_directory: str | Path):
        self.run_directory = Path(run_directory)
        self.run_directory.mkdir(parents=True, exist_ok=True)

    def start(
        self,
        objective: str,
        *,
        task_type: str = "general",
        task_id: str | None = None,
        additional_requirements: tuple[str, ...] = (),
    ) -> TaskContract:
        if task_type not in {"general", "visual"}:
            raise ValueError("task_type must be 'general' or 'visual'")

        requirements = list(self.GENERAL_REQUIREMENTS)
        if task_type == "visual":
            requirements.extend(self.VISUAL_REQUIREMENTS)
        for requirement in additional_requirements:
            if requirement and requirement not in requirements:
                requirements.append(requirement)

        contract = TaskContract(
            task_id=task_id or str(uuid4()),
            objective=objective,
            task_type=task_type,
            requirements=tuple(requirements),
            created_at=utc_now(),
        )
        self._write(
            contract.task_id,
            {
                "contract": asdict(contract),
                "status": "ready",
                "completion": None,
            },
        )
        return contract

    def finish(self, task_id: str, evidence: dict[str, Any]) -> CompletionDecision:
        record = self.load(task_id)
        requirements = record["contract"]["requirements"]
        missing = [name for name in requirements if not self._satisfied(name, evidence)]
        decision = CompletionDecision(passed=not missing, missing=missing)

        record["status"] = "completed" if decision.passed else "blocked"
        record["completion"] = {
            "checked_at": utc_now(),
            "evidence": evidence,
            "passed": decision.passed,
            "missing": decision.missing,
        }
        self._write(task_id, record)
        return decision

    def load(self, task_id: str) -> dict[str, Any]:
        path = self._path(task_id)
        if not path.exists():
            raise KeyError(f"Unknown task_id: {task_id}")
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _satisfied(requirement: str, evidence: dict[str, Any]) -> bool:
        value = evidence.get(requirement)
        if requirement.endswith("_passed"):
            return value is True
        return isinstance(value, str) and bool(value.strip())

    def _path(self, task_id: str) -> Path:
        if not task_id or task_id in {".", ".."} or Path(task_id).name != task_id:
            raise ValueError("task_id must be a single safe file name")
        return self.run_directory / f"{task_id}.json"

    def _write(self, task_id: str, record: dict[str, Any]) -> None:
        self._path(task_id).write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
