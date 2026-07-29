import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_project_state import REFERENCE_FILES, validate


class ProjectStateTest(unittest.TestCase):
    def make_repo(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        state = {
            "schema_version": 1, "phase": "V1 Week 3", "status": "ready",
            "latest_merged_pr": 14, "verified_main_commit": "526384c",
            "active_issue": 16, "active_branch": "agent/fix",
            "next_action": "review", "verified_at": "2026-07-29",
            "evidence": "connector verified",
        }
        (root / "PROJECT_STATE.json").write_text(json.dumps(state), encoding="utf-8")
        for name in REFERENCE_FILES:
            (root / name).write_text("See `PROJECT_STATE.json`.\n", encoding="utf-8")
        return tmp, root

    def test_valid_local_state_passes(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        self.assertEqual(validate(root, "526384c", 14), [])

    def test_stale_main_is_detected(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        self.assertIn(
            "verified_main_commit does not match supplied main HEAD",
            validate(root, "different-head", 14),
        )

    def test_duplicated_mutable_state_is_detected(self):
        tmp, root = self.make_repo()
        self.addCleanup(tmp.cleanup)
        (root / "README.md").write_text(
            "See PROJECT_STATE.json\n現在の作業先: agent/old\n", encoding="utf-8"
        )
        self.assertTrue(any("duplicates mutable state" in e for e in validate(root)))


if __name__ == "__main__":
    unittest.main()
