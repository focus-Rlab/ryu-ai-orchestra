from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPECIALISTS = ("requirements-designer", "implementer", "tester-evaluator")
TOP_LEVEL_ENTRYPOINTS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".github/copilot-instructions.md",
    ".github/agents/raphael.md",
    "NEXT_SESSION_PROMPT.md",
)


class PortableAgentEntrypointTest(unittest.TestCase):
    def test_top_level_entrypoints_restore_raphael_identity(self):
        for relative_path in TOP_LEVEL_ENTRYPOINTS:
            with self.subTest(path=relative_path):
                text = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("Raphael", text)
                self.assertIn("STARTUP_CONTEXT.md", text)

    def test_common_agent_specs_are_declared_as_canonical_and_portable(self):
        for name in SPECIALISTS:
            with self.subTest(agent=name):
                text = (ROOT / "agents" / f"{name}.md").read_text(encoding="utf-8")
                self.assertIn("AI非依存の共通正本", text)
                self.assertIn(f".codex/agents/{name}.toml", text)

    def test_codex_adapters_are_valid_and_route_to_common_specs(self):
        for name in SPECIALISTS:
            with self.subTest(agent=name):
                path = ROOT / ".codex" / "agents" / f"{name}.toml"
                with path.open("rb") as file:
                    config = tomllib.load(file)
                self.assertEqual(config["name"], name)
                self.assertTrue(config["description"])
                self.assertIn(f"agents/{name}.md", config["developer_instructions"])
                self.assertIn("共通正本", config["developer_instructions"])

    def test_environment_adapters_route_to_common_specs(self):
        for name in SPECIALISTS:
            with self.subTest(agent=name):
                claude_text = (
                    ROOT / ".claude" / "agents" / f"{name}.md"
                ).read_text(encoding="utf-8")
                codex_text = (
                    ROOT / ".codex" / "agents" / f"{name}.toml"
                ).read_text(encoding="utf-8")
                self.assertIn(f"agents/{name}.md", claude_text)
                self.assertIn(f"agents/{name}.md", codex_text)

    def test_next_session_prompt_has_no_stale_week_or_branch(self):
        text = (ROOT / "NEXT_SESSION_PROMPT.md").read_text(encoding="utf-8")
        self.assertNotIn("agent/v1-week1-general-core", text)
        self.assertNotIn("Issue #11", text)
        self.assertIn("PROJECT_STATE.json", text)
