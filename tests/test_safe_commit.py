import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "safe_commit.sh"


class SafeCommitTest(unittest.TestCase):
    def make_repo(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=root, check=True)
        (root / "README.md").write_text("initial\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=root, check=True)
        return tmp, root

    def test_refuses_commit_on_main(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        (root / "README.md").write_text("changed\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        result = subprocess.run(
            [str(SCRIPT), "-m", "should be refused"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("REFUSED", result.stderr)
        log = subprocess.run(
            ["git", "log", "--oneline"], cwd=root, capture_output=True, text=True, check=True
        ).stdout
        self.assertEqual(len(log.strip().splitlines()), 1, "no new commit should have been created")

    def test_allows_commit_on_feature_branch(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        subprocess.run(["git", "checkout", "-q", "-b", "feature/x"], cwd=root, check=True)
        (root / "README.md").write_text("changed\n", encoding="utf-8")
        subprocess.run(["git", "add", "README.md"], cwd=root, check=True)
        result = subprocess.run(
            [str(SCRIPT), "-m", "should succeed"],
            cwd=root, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        log = subprocess.run(
            ["git", "log", "--oneline"], cwd=root, capture_output=True, text=True, check=True
        ).stdout
        self.assertEqual(len(log.strip().splitlines()), 2)


if __name__ == "__main__":
    unittest.main()
