import tempfile
import unittest
from pathlib import Path

from v1_core import RaphaelRunner


class RaphaelRunnerTest(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.run_directory = Path(self.temporary_directory.name)
        self.runner = RaphaelRunner(self.run_directory)

    def test_visual_task_contract_adds_user_delivery_requirements(self):
        contract = self.runner.start("公開アプリを作る", task_type="visual")

        self.assertEqual(
            contract.requirements,
            (
                "result_evidence",
                "user_access_evidence",
                "user_acceptance_passed",
            ),
        )

    def test_visual_task_cannot_finish_with_only_technical_test(self):
        contract = self.runner.start("公開アプリを作る", task_type="visual")

        decision = self.runner.finish(
            contract.task_id,
            {"result_evidence": "13/13 automated tests passed"},
        )

        self.assertFalse(decision.passed)
        self.assertEqual(
            decision.missing,
            ["user_access_evidence", "user_acceptance_passed"],
        )
        self.assertEqual(self.runner.load(contract.task_id)["status"], "blocked")

    def test_pending_user_acceptance_does_not_count_as_passed(self):
        contract = self.runner.start("公開アプリを作る", task_type="visual")

        decision = self.runner.finish(
            contract.task_id,
            {
                "result_evidence": "13/13 automated tests passed",
                "user_access_evidence": "https://example.test/app",
                "user_acceptance_passed": False,
            },
        )

        self.assertFalse(decision.passed)
        self.assertEqual(decision.missing, ["user_acceptance_passed"])

    def test_visual_task_finishes_after_evidence_and_user_acceptance(self):
        contract = self.runner.start("公開アプリを作る", task_type="visual")

        decision = self.runner.finish(
            contract.task_id,
            {
                "result_evidence": "13/13 automated tests passed",
                "user_access_evidence": "https://example.test/app",
                "user_acceptance_passed": True,
            },
        )

        self.assertTrue(decision.passed)
        saved = self.runner.load(contract.task_id)
        self.assertEqual(saved["status"], "completed")
        self.assertTrue(saved["completion"]["passed"])

    def test_general_task_needs_result_evidence_but_not_visual_acceptance(self):
        contract = self.runner.start("内部データを整理する")

        blocked = self.runner.finish(contract.task_id, {})
        passed = self.runner.finish(
            contract.task_id,
            {"result_evidence": "output/report.json"},
        )

        self.assertFalse(blocked.passed)
        self.assertTrue(passed.passed)

    def test_record_can_be_loaded_by_a_new_runner_process(self):
        contract = self.runner.start("履歴を保存する")

        reloaded = RaphaelRunner(self.run_directory).load(contract.task_id)

        self.assertEqual(reloaded["contract"]["objective"], "履歴を保存する")
        self.assertEqual(reloaded["status"], "ready")

    def test_task_id_cannot_escape_the_run_directory(self):
        with self.assertRaisesRegex(ValueError, "safe file name"):
            self.runner.load("../outside")


if __name__ == "__main__":
    unittest.main()
