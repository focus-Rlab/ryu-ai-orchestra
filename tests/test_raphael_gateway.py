import json
import tempfile
import unittest
from pathlib import Path

from v1_core import ExperienceStore, RaphaelGateway, RaphaelRunner


class RaphaelGatewayTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.gateway = RaphaelGateway(
            RaphaelRunner(root / "runs"), ExperienceStore(root / "experience.db")
        )

    def prepare(self, request):
        return self.gateway.prepare([{"role": "user", "content": request}])

    def assert_experience(self, request, expected_id):
        prepared = self.prepare(request)
        ids = {item.experience_id for item in prepared.experiences}
        self.assertIn("core-action-application", ids)
        self.assertIn(expected_id, ids)
        return prepared

    def test_01_every_request_applies_accumulated_experience(self):
        prepared = self.prepare("今日の予定を整理して")
        self.assertIn("experience_application_evidence", prepared.contract.requirements)

    def test_02_problem_requires_root_cause_and_prevention(self):
        prepared = self.assert_experience("同じミスがまた起きた", "root-cause-before-fix")
        self.assertIn("root_cause_evidence", prepared.contract.requirements)
        self.assertIn("prevention_evidence", prepared.contract.requirements)

    def test_03_visual_result_requires_user_acceptance(self):
        prepared = self.assert_experience("アプリの画面を完成して", "user-acceptance-separate")
        self.assertIn("user_acceptance_passed", prepared.contract.requirements)

    def test_04_paid_api_requires_approval(self):
        prepared = self.assert_experience("有料APIを契約して", "paid-action-approval")
        self.assertIn("paid_use_approval_passed", prepared.contract.requirements)

    def test_05_delete_requires_target_and_rollback(self):
        prepared = self.assert_experience("古いデータを削除して", "destructive-action-safety")
        self.assertIn("rollback_evidence", prepared.contract.requirements)

    def test_06_github_request_requires_available_path_check(self):
        prepared = self.assert_experience("GitHubでPRを作って", "github-connector-fallback")
        self.assertIn("available_path_evidence", prepared.contract.requirements)

    def test_07_state_change_requires_sync_evidence(self):
        prepared = self.assert_experience("PROJECT_STATEを現在地に同期して", "state-source-check")
        self.assertIn("state_sync_evidence", prepared.contract.requirements)

    def test_08_execution_requires_goal_alignment(self):
        prepared = self.assert_experience("この機能を実装して", "scope-before-execution")
        self.assertIn("goal_alignment_evidence", prepared.contract.requirements)

    def test_09_concise_request_requires_communication_fit(self):
        prepared = self.assert_experience("必要なことだけ短く説明して", "concise-communication")
        self.assertIn("communication_fit_evidence", prepared.contract.requirements)

    def test_10_completion_claim_requires_acceptance_evidence(self):
        prepared = self.assert_experience("これで完成として納品して", "no-premature-completion")
        self.assertIn("acceptance_evidence", prepared.contract.requirements)

    def test_missing_required_evidence_blocks_completion(self):
        prepared = self.prepare("同じ問題を直して完成して")
        result = self.gateway.finalize(prepared, json.dumps({
            "reply": "完了しました", "status": "complete",
            "evidence": {"result_evidence": "test passed"},
        }, ensure_ascii=False))
        self.assertEqual(result.status, "blocked")
        self.assertIn("root_cause_evidence", result.reply)

    def test_complete_passes_only_with_every_required_evidence(self):
        prepared = self.prepare("今日の予定を整理して")
        evidence = {name: "確認済み" for name in prepared.contract.requirements}
        result = self.gateway.finalize(prepared, json.dumps({
            "reply": "整理しました", "status": "complete", "evidence": evidence,
        }, ensure_ascii=False))
        self.assertEqual(result.status, "completed")

    def test_invalid_model_protocol_is_blocked(self):
        prepared = self.prepare("相談したい")
        result = self.gateway.finalize(prepared, "普通の文章だけ")
        self.assertEqual(result.status, "blocked")


if __name__ == "__main__":
    unittest.main()
