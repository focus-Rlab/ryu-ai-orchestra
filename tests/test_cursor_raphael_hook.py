import importlib.util
import tempfile
import unittest
from pathlib import Path

from v1_core import ExperienceStore, RaphaelRunner


HOOK_PATH = Path(__file__).parents[1] / ".cursor" / "hooks" / "raphael_hook.py"
SPEC = importlib.util.spec_from_file_location("raphael_cursor_hook", HOOK_PATH)
hook = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(hook)


class CursorRaphaelHookTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        hook.STATE_DIR = root / "cursor"
        hook.STORE = ExperienceStore(root / "experience.db")
        hook.RUNNER = RaphaelRunner(root / "runs")
        hook.seed_default_experiences(hook.STORE)
        self.base = {"conversation_id": "conversation-1"}

    def test_prompt_creates_contract_from_accumulated_experience(self):
        result = hook.before_submit({**self.base, "prompt": "同じミスを直して"})
        state = hook.load_state("conversation-1")
        self.assertTrue(result["continue"])
        self.assertIn("root_cause_evidence", state["requirements"])
        self.assertIn("prevention_evidence", state["requirements"])

    def test_first_tool_is_denied_and_contract_is_sent_to_agent(self):
        hook.before_submit({**self.base, "prompt": "この機能を実装して"})
        first = hook.pre_tool(self.base)
        second = hook.pre_tool(self.base)
        self.assertEqual(first["permission"], "deny")
        self.assertIn("RAPHAEL TASK CONTRACT", first["agent_message"])
        self.assertEqual(second["permission"], "allow")

    def test_tool_is_denied_when_prompt_gate_was_bypassed(self):
        result = hook.pre_tool(self.base)
        self.assertEqual(result["permission"], "deny")

    def test_stop_auto_continues_until_evidence_is_recorded(self):
        hook.before_submit({**self.base, "prompt": "予定を整理して"})
        state = hook.load_state("conversation-1")
        blocked = hook.stop({**self.base, "status": "completed"})
        self.assertIn("followup_message", blocked)
        for requirement in state["requirements"]:
            self.assertEqual(hook.record(state["task_id"], requirement, "verified"), 0)
        passed = hook.stop({**self.base, "status": "completed"})
        self.assertEqual(passed, {})

    def test_unknown_evidence_cannot_be_recorded(self):
        hook.before_submit({**self.base, "prompt": "予定を整理して"})
        state = hook.load_state("conversation-1")
        result = hook.record(state["task_id"], "invented_evidence", "fake")
        self.assertEqual(result, 2)


if __name__ == "__main__":
    unittest.main()
