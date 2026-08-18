from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from v1_core import ExperienceStore, RaphaelRunner  # noqa: E402
from v1_core.experience_store import seed_default_experiences  # noqa: E402


STATE_DIR = ROOT / ".raphael" / "cursor"
STORE = ExperienceStore(ROOT / ".raphael" / "experience.db")
RUNNER = RaphaelRunner(ROOT / ".raphael" / "runs")
seed_default_experiences(STORE)


def safe_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]", "_", value)
    return cleaned[:120] or "unknown"


def state_path(conversation_id: str) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    return STATE_DIR / f"{safe_id(conversation_id)}.json"


def load_state(conversation_id: str) -> dict[str, Any] | None:
    path = state_path(conversation_id)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(conversation_id: str, state: dict[str, Any]) -> None:
    state_path(conversation_id).write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def before_submit(data: dict[str, Any]) -> dict[str, Any]:
    prompt = str(data.get("prompt", "")).strip()
    conversation_id = str(data.get("conversation_id", "unknown"))
    experiences = STORE.match(prompt)
    requirements = tuple(dict.fromkeys(
        name for item in experiences for name in item.required_evidence
    ))
    contract = RUNNER.start(prompt, additional_requirements=requirements)
    STORE.record_start(contract.task_id, prompt, experiences)
    save_state(conversation_id, {
        "task_id": contract.task_id,
        "objective": prompt,
        "requirements": list(contract.requirements),
        "experiences": [
            {"id": item.experience_id, "title": item.title, "lesson": item.lesson}
            for item in experiences
        ],
        "evidence": {},
        "contract_delivered": False,
        "tool_events": [],
        "failures": [],
    })
    return {"continue": True}


def pre_tool(data: dict[str, Any]) -> dict[str, Any]:
    conversation_id = str(data.get("conversation_id", "unknown"))
    state = load_state(conversation_id)
    if not state:
        return {
            "permission": "deny",
            "user_message": "Raphael契約が未作成のため実行を停止しました。",
            "agent_message": "User prompt must pass beforeSubmitPrompt before tools are used.",
        }
    if not state["contract_delivered"]:
        state["contract_delivered"] = True
        save_state(conversation_id, state)
        lessons = "\n".join(
            f"- {item['title']}: {item['lesson']}" for item in state["experiences"]
        )
        requirements = ", ".join(state["requirements"])
        return {
            "permission": "deny",
            "user_message": "Raphaelが過去経験を今回の実行条件へ変換しました。",
            "agent_message": (
                f"RAPHAEL TASK CONTRACT\nTask ID: {state['task_id']}\n"
                f"Objective: {state['objective']}\nApplicable experience:\n{lessons}\n"
                f"Required evidence before completion: {requirements}\n"
                "Revise the plan to apply every item, then retry the tool."
            ),
        }
    return {"permission": "allow"}


def post_tool(data: dict[str, Any]) -> dict[str, Any]:
    conversation_id = str(data.get("conversation_id", "unknown"))
    state = load_state(conversation_id)
    if state:
        state["tool_events"].append({
            "tool_name": data.get("tool_name"),
            "tool_use_id": data.get("tool_use_id"),
        })
        save_state(conversation_id, state)
    return {}


def post_failure(data: dict[str, Any]) -> dict[str, Any]:
    conversation_id = str(data.get("conversation_id", "unknown"))
    state = load_state(conversation_id)
    if state and data.get("failure_type") != "permission_denied":
        state["failures"].append({
            "tool_name": data.get("tool_name"),
            "failure_type": data.get("failure_type"),
            "error_message": data.get("error_message"),
        })
        save_state(conversation_id, state)
    return {}


def stop(data: dict[str, Any]) -> dict[str, Any]:
    if data.get("status") != "completed":
        return {}
    conversation_id = str(data.get("conversation_id", "unknown"))
    state = load_state(conversation_id)
    if not state:
        return {"followup_message": "Raphael契約がありません。依頼を再評価してください。"}
    missing = [name for name in state["requirements"] if not state["evidence"].get(name)]
    if missing:
        return {"followup_message": (
            "完了条件が不足しています。作業を続け、実物証拠を確認してから記録してください。"
            f" Task ID: {state['task_id']} / Missing: {', '.join(missing)}"
        )}
    decision = RUNNER.finish(state["task_id"], state["evidence"])
    STORE.record_outcome(state["task_id"], "completed" if decision.passed else "blocked")
    if not decision.passed:
        return {"followup_message": "Runner検査が失敗しました。不足: " + ", ".join(decision.missing)}
    return {}


def record(task_id: str, name: str, value: str) -> int:
    for path in STATE_DIR.glob("*.json"):
        state = json.loads(path.read_text(encoding="utf-8"))
        if state.get("task_id") == task_id:
            if name not in state.get("requirements", []):
                print(f"Unknown requirement: {name}", file=sys.stderr)
                return 2
            state["evidence"][name] = value
            path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8")
            print(f"Recorded {name} for {task_id}")
            return 0
    print(f"Unknown task: {task_id}", file=sys.stderr)
    return 2


def encode_hook_output(value: dict[str, Any]) -> str:
    """Return ASCII-only JSON so Cursor can parse it on Windows code pages."""
    return json.dumps(value, ensure_ascii=True)


def hook_main() -> int:
    try:
        raw_input = sys.stdin.buffer.read()
        data = json.loads(raw_input.decode("utf-8-sig"))
        event = data.get("hook_event_name")
        handlers = {
            "beforeSubmitPrompt": before_submit,
            "preToolUse": pre_tool,
            "postToolUse": post_tool,
            "postToolUseFailure": post_failure,
            "stop": stop,
        }
        result = handlers.get(event, lambda _: {})(data)
        sys.stdout.buffer.write((encode_hook_output(result) + "\n").encode("ascii"))
        sys.stdout.buffer.flush()
        return 0
    except Exception as error:
        sys.stderr.buffer.write(
            (encode_hook_output({"error": str(error)}) + "\n").encode("ascii")
        )
        sys.stderr.buffer.flush()
        return 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")
    record_parser = subparsers.add_parser("record")
    record_parser.add_argument("--task-id", required=True)
    record_parser.add_argument("--name", required=True)
    record_parser.add_argument("--value", required=True)
    arguments = parser.parse_args()
    if arguments.command == "record":
        raise SystemExit(record(arguments.task_id, arguments.name, arguments.value))
    raise SystemExit(hook_main())
