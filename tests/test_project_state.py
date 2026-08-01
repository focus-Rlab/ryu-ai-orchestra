import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.check_project_state import REFERENCE_FILES, project_digest, validate


class ProjectStateTest(unittest.TestCase):
    def make_repo(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        state = {
            "schema_version": 2, "phase": "V1 Week 3", "status": "ready",
            "latest_merged_pr": 14, "verified_project_digest": "pending",
            "active_issue": 16, "active_branch": "agent/fix",
            "next_action": "review", "verified_at": "2026-07-29",
            "evidence": "connector verified",
        }
        (root / "PROJECT_STATE.json").write_text(json.dumps(state), encoding="utf-8")
        for name in REFERENCE_FILES:
            (root / name).write_text("See `PROJECT_STATE.json`.\n", encoding="utf-8")
        state["verified_project_digest"] = project_digest(root)
        (root / "PROJECT_STATE.json").write_text(json.dumps(state), encoding="utf-8")
        return tmp, root

    def test_valid_local_state_passes(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        self.assertEqual(validate(root, expected_pr=14), [])

    def test_sync_script_supports_direct_execution(self):
        result = subprocess.run(
            [sys.executable, "scripts/sync_project_state.py", "--help"],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_project_change_is_detected(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        (root / "README.md").write_text("See `PROJECT_STATE.json`.\nchanged\n")
        self.assertIn(
            "verified_project_digest does not match project content",
            validate(root, expected_pr=14),
        )

    def test_state_only_change_does_not_invalidate_digest(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        state_path = root / "PROJECT_STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state["next_action"] = "updated state only"
        state_path.write_text(json.dumps(state), encoding="utf-8")
        self.assertEqual(validate(root, expected_pr=14), [])

    def test_duplicated_mutable_state_is_detected(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        (root / "README.md").write_text(
            "See PROJECT_STATE.json\n現在の作業先: agent/old\n", encoding="utf-8"
        )
        self.assertTrue(any("duplicates mutable state" in e for e in validate(root)))


if __name__ == "__main__":
    unittest.main()
