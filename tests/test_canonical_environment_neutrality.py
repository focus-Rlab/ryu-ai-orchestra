import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_canonical_environment_neutrality import scan_text  # noqa: E402

SCRIPT = ROOT / "scripts" / "check_canonical_environment_neutrality.py"
HOOK_SRC = ROOT / "scripts" / "hooks" / "pre-commit"


class ScanTextTest(unittest.TestCase):
    def test_flags_the_actual_incident_phrase(self):
        """The exact trigger phrase from INCIDENT_LOG.md's 2026-08-07 incident."""
        text = "## Prohibited\n\n常に禁止: 画像生成\n"
        findings = scan_text(text, "agents/clarifier.md")
        self.assertTrue(findings)

    def test_flags_english_always_prohibited(self):
        text = "Image generation is always prohibited for this role.\n"
        findings = scan_text(text, "agents/clarifier.md")
        self.assertTrue(findings)

    def test_does_not_flag_scoped_pilot_language(self):
        """Matches the existing, already-audited safe pattern in
        agents/*.md: scoping a preference to 'this pilot' rather than
        asserting it as universal."""
        text = "今回のパイロットでは単一環境固定とする。\n"
        findings = scan_text(text, "agents/implementer.md")
        self.assertEqual(findings, [])

    def test_does_not_flag_ordinary_text(self):
        text = "Raphaelは隆之介の主要な対話窓口です。\n"
        findings = scan_text(text, "agents/raphael.md")
        self.assertEqual(findings, [])

    def test_known_limit_similar_but_unlisted_phrasing_not_caught(self):
        """States the known limit honestly: only the registered phrase
        patterns are matched, not open-ended semantic equivalents."""
        text = "この機能は一切利用できません。\n"
        findings = scan_text(text, "agents/clarifier.md")
        self.assertEqual(findings, [], "unregistered phrasing is out of scope by design")


class CliTest(unittest.TestCase):
    def run_cli(self, text: str) -> subprocess.CompletedProcess:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "agent.md"
            path.write_text(text, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(path), "--root", tmp],
                capture_output=True, text=True,
            )

    def test_cli_fails_on_violation(self):
        result = self.run_cli("常に禁止: 画像生成\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("FAIL", result.stdout)

    def test_cli_passes_when_clean(self):
        result = self.run_cli("Raphaelは隆之介の主要な対話窓口です。\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("PASS", result.stdout)


class PreCommitHookIntegrationTest(unittest.TestCase):
    def make_repo_with_hook_and_checker(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=root, check=True)
        hooks_dir = root / "myhooks"
        hooks_dir.mkdir()
        installed = hooks_dir / "pre-commit"
        installed.write_text(HOOK_SRC.read_text(encoding="utf-8"), encoding="utf-8")
        installed.chmod(0o755)
        subprocess.run(["git", "config", "core.hooksPath", "myhooks"], cwd=root, check=True)

        scripts_dir = root / "scripts"
        scripts_dir.mkdir()
        (scripts_dir / "check_canonical_environment_neutrality.py").write_text(
            SCRIPT.read_text(encoding="utf-8"), encoding="utf-8"
        )
        agents_dir = root / "agents"
        agents_dir.mkdir()
        (root / "README.md").write_text("initial\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "-c", "core.hooksPath=", "commit", "-q", "-m", "initial"], cwd=root, check=True)
        subprocess.run(["git", "checkout", "-q", "-b", "feature/x"], cwd=root, check=True)
        return tmp, root, agents_dir

    def test_hook_refuses_commit_with_contaminated_agent_file(self):
        tmp, root, agents_dir = self.make_repo_with_hook_and_checker()
        self.addCleanup(tmp.cleanup)
        (agents_dir / "clarifier.md").write_text("常に禁止: 画像生成\n", encoding="utf-8")
        subprocess.run(["git", "add", "agents/clarifier.md"], cwd=root, check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "add clarifier"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REFUSED", result.stdout + result.stderr)

    def test_hook_allows_commit_with_clean_agent_file(self):
        tmp, root, agents_dir = self.make_repo_with_hook_and_checker()
        self.addCleanup(tmp.cleanup)
        (agents_dir / "clarifier.md").write_text("Raphaelの担当領域を補助する。\n", encoding="utf-8")
        subprocess.run(["git", "add", "agents/clarifier.md"], cwd=root, check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "add clarifier"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_hook_ignores_non_agent_files(self):
        tmp, root, agents_dir = self.make_repo_with_hook_and_checker()
        self.addCleanup(tmp.cleanup)
        (root / "NOTES.md").write_text("常に禁止: 画像生成\n", encoding="utf-8")
        subprocess.run(["git", "add", "NOTES.md"], cwd=root, check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "add notes"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
