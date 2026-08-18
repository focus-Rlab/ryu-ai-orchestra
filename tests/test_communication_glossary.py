import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from check_communication_glossary import find_unexplained, load_glossary  # noqa: E402

GLOSSARY_PATH = ROOT / "docs" / "COMMUNICATION_GLOSSARY.json"
SCRIPT = ROOT / "scripts" / "check_communication_glossary.py"


class GlossaryDataTest(unittest.TestCase):
    def test_glossary_terms_have_required_fields_and_valid_category(self):
        data = json.loads(GLOSSARY_PATH.read_text(encoding="utf-8"))
        categories = set(data["categories"])
        self.assertTrue(data["terms"], "glossary must not be empty")
        for entry in data["terms"]:
            self.assertIn("term", entry)
            self.assertIn("category", entry)
            self.assertIn("source", entry)
            self.assertIn(entry["category"], categories)

    def test_seeded_terms_from_2026_08_01_evaluation_are_present(self):
        terms = {entry["term"] for entry in load_glossary(GLOSSARY_PATH)}
        for expected in ("スポットチェック", "フィクスチャ", "デビエーション", "クローズ", "REQ"):
            self.assertIn(expected, terms)


class FindUnexplainedTest(unittest.TestCase):
    def setUp(self):
        self.terms = load_glossary(GLOSSARY_PATH)

    def test_unexplained_term_is_flagged(self):
        text = "今回はデビエーションが1件ありました。"
        findings = find_unexplained(text, self.terms)
        self.assertTrue(any(f["term"] == "デビエーション" for f in findings))

    def test_term_with_parenthetical_gloss_is_not_flagged(self):
        text = "今回はデビエーション（要件からの逸脱）が1件ありました。"
        findings = find_unexplained(text, self.terms)
        self.assertFalse(any(f["term"] == "デビエーション" for f in findings))

    def test_term_with_defining_phrase_is_not_flagged(self):
        text = "REQとは、要件書の各項目に振られた管理番号のことです。"
        findings = find_unexplained(text, self.terms)
        self.assertFalse(any(f["term"] == "REQ" for f in findings))

    def test_absent_term_produces_no_finding(self):
        text = "今日は天気がいいですね。"
        findings = find_unexplained(text, self.terms)
        self.assertEqual(findings, [])

    def test_unregistered_jargon_is_not_caught(self):
        """States the known limit honestly: only registered terms are checked."""
        text = "今回はハンドオフコントラクトチェッカーを使いました。"
        findings = find_unexplained(text, self.terms)
        self.assertEqual(findings, [], "unregistered terms are out of scope by design")


class CliTest(unittest.TestCase):
    def run_cli(self, text: str) -> subprocess.CompletedProcess:
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
            fh.write(text)
            path = fh.name
        return subprocess.run(
            [sys.executable, str(SCRIPT), path],
            capture_output=True, text=True,
        )

    def test_cli_exits_nonzero_on_unexplained_term(self):
        result = self.run_cli("スポットチェックを行いました。")
        self.assertEqual(result.returncode, 1)
        self.assertIn("スポットチェック", result.stdout)

    def test_cli_exits_zero_when_clean(self):
        result = self.run_cli("今日は天気がいいですね。")
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
