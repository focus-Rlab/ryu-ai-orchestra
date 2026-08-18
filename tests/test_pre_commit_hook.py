import subprocess
import tempfile
import unittest
from pathlib import Path

HOOK_SRC = Path(__file__).resolve().parents[1] / "scripts" / "hooks" / "pre-commit"


class PreCommitHookTest(unittest.TestCase):
    def make_repo_with_hook(self):
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
        (root / "README.md").write_text("initial\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        subprocess.run(["git", "-c", "core.hooksPath=", "commit", "-q", "-m", "initial"], cwd=root, check=True)
        return tmp, root

    def test_bare_git_commit_is_blocked_on_main(self):
        """Proves the hook fires even when git commit is called directly,
        not through scripts/safe_commit.sh — closing the bypass gap an
        independent review found in the wrapper-only control."""
        tmp, root = self.make_repo_with_hook()
        self.addCleanup(tmp.cleanup)
        (root / "README.md").write_text("changed\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "should be refused"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REFUSED", result.stdout + result.stderr)
        log = subprocess.run(
            ["git", "log", "--oneline"], cwd=root, capture_output=True, text=True, check=True
        ).stdout
        self.assertEqual(len(log.strip().splitlines()), 1, "no new commit should have been created")

    def test_bare_git_commit_succeeds_on_feature_branch(self):
        tmp, root = self.make_repo_with_hook()
        self.addCleanup(tmp.cleanup)
        subprocess.run(["git", "checkout", "-q", "-b", "feature/x"], cwd=root, check=True)
        (root / "README.md").write_text("changed\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        result = subprocess.run(
            ["git", "commit", "-m", "should succeed"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
