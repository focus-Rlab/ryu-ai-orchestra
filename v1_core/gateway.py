from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from .experience_store import Experience, ExperienceStore, seed_default_experiences
from .runner import CompletionDecision, RaphaelRunner, TaskContract


@dataclass(frozen=True)
class PreparedRequest:
    contract: TaskContract
    experiences: tuple[Experience, ...]
    messages: tuple[dict[str, Any], ...]


@dataclass(frozen=True)
class GatewayReply:
    task_id: str
    reply: str
    status: str
    decision: CompletionDecision | None


class RaphaelGateway:
    """Mandatory policy layer placed between the chat UI and any model."""

    def __init__(self, runner: RaphaelRunner, store: ExperienceStore):
        self.runner = runner
        self.store = store
        seed_default_experiences(store)

    def prepare(self, messages: list[dict[str, Any]]) -> PreparedRequest:
        request = self._latest_user_message(messages)
        experiences = tuple(self.store.match(request))
        requirements = tuple(dict.fromkeys(
            requirement
            for experience in experiences
            for requirement in experience.required_evidence
        ))
        contract = self.runner.start(request, additional_requirements=requirements)
        self.store.record_start(contract.task_id, request, experiences)
        policy = self._policy_message(contract, experiences)
        prepared_messages = ({"role": "system", "content": policy}, *messages)
        return PreparedRequest(contract, experiences, tuple(prepared_messages))

    def finalize(self, prepared: PreparedRequest, model_content: str) -> GatewayReply:
        try:
            envelope = json.loads(model_content)
        except json.JSONDecodeError:
            return GatewayReply(
                prepared.contract.task_id,
                "安全確認に必要な形式でAIが回答しなかったため、完了扱いにせず停止しました。",
                "blocked", None,
            )
        reply = str(envelope.get("reply", "")).strip()
        status = envelope.get("status", "working")
        evidence = envelope.get("evidence", {})
        if status != "complete":
            self.store.record_outcome(prepared.contract.task_id, "working")
            return GatewayReply(prepared.contract.task_id, reply, "working", None)
        if not isinstance(evidence, dict):
            evidence = {}
        decision = self.runner.finish(prepared.contract.task_id, evidence)
        outcome = "completed" if decision.passed else "blocked"
        self.store.record_outcome(prepared.contract.task_id, outcome)
        if not decision.passed:
            reply = "完了条件が不足しているため停止しました。不足: " + "、".join(decision.missing)
        return GatewayReply(prepared.contract.task_id, reply, outcome, decision)

    @staticmethod
    def _latest_user_message(messages: list[dict[str, Any]]) -> str:
        for message in reversed(messages):
            if message.get("role") == "user" and isinstance(message.get("content"), str):
                return message["content"].strip()
        raise ValueError("A user message is required")

    @staticmethod
    def _policy_message(contract: TaskContract,
                        experiences: tuple[Experience, ...]) -> str:
        lessons = "\n".join(f"- {item.title}: {item.lesson}" for item in experiences)
        requirements = ", ".join(contract.requirements)
        return f"""あなたはRaphaelとして対応する。以下は助言ではなく実行条件。
Task ID: {contract.task_id}
今回適用する経験:
{lessons}

回答は必ずJSONオブジェクト1個だけにする:
{{"reply":"ユーザーに見せる日本語", "status":"working または complete", "evidence":{{}}}}
complete とする場合、evidence に次を実物証拠として全て含める:
{requirements}
証拠がない、ユーザー承認待ち、実行していない場合は working とする。"""
