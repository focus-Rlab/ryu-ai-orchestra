"""Tests for the Stop hook using hand-built fixture stdin, since a Stop hook
cannot be made to fire on itself mid-session (see the hook's own module
docstring for this honesty note: live-firing is unverified in this session).
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK_SCRIPT = ROOT / ".claude" / "hooks" / "stop-communication-check.py"
LOG_PATH = ROOT / "evaluations" / "action-gates" / "communication_observations.jsonl"


def write_transcript(tmp_path: Path, assistant_text: str) -> Path:
    transcript = tmp_path / "transcript.jsonl"
    lines = [
        {"message": {"role": "user", "content": "こんにちは"}},
        {"message": {"role": "assistant", "content": [{"type": "text", "text": assistant_text}]}},
    ]
    transcript.write_text("\n".join(json.dumps(line, ensure_ascii=False) for line in lines) + "\n", encoding="utf-8")
    return transcript


class StopHookTest(unittest.TestCase):
    def setUp(self):
        self.log_existed_before = LOG_PATH.exists()
        self.log_size_before = LOG_PATH.stat().st_size if self.log_existed_before else 0

    def run_hook(self, stdin_payload: dict) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input=json.dumps(stdin_payload), capture_output=True, text=True,
        )

    def test_never_blocks_even_with_unexplained_jargon(self):
        with tempfile.TemporaryDirectory() as tmp:
            transcript = write_transcript(Path(tmp), "デビエーションが見つかりました。")
            result = self.run_hook({"transcript_path": str(transcript), "session_id": "test-session"})
        self.assertEqual(result.returncode, 0, "Stop hook must never block (stage 1, observe-only)")

    def test_logs_finding_for_unexplained_term(self):
        with tempfile.TemporaryDirectory() as tmp:
            transcript = write_transcript(Path(tmp), "デビエーションが見つかりました。")
            self.run_hook({"transcript_path": str(transcript), "session_id": "test-session-log"})
        self.assertTrue(LOG_PATH.exists())
        new_bytes = LOG_PATH.read_bytes()[self.log_size_before:]
        self.assertIn(b"test-session-log", new_bytes)
        self.assertIn("デビエーション".encode("utf-8"), new_bytes)

    def test_does_not_log_when_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            transcript = write_transcript(Path(tmp), "こんにちは、今日は良い天気です。")
            self.run_hook({"transcript_path": str(transcript), "session_id": "test-session-clean"})
        if LOG_PATH.exists():
            new_bytes = LOG_PATH.read_bytes()[self.log_size_before:]
            self.assertNotIn(b"test-session-clean", new_bytes)

    def test_missing_transcript_path_does_not_crash_or_block(self):
        result = self.run_hook({"session_id": "no-transcript"})
        self.assertEqual(result.returncode, 0)

    def test_malformed_stdin_does_not_crash_or_block(self):
        result = subprocess.run(
            [sys.executable, str(HOOK_SCRIPT)],
            input="not json", capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0)

    def test_nonexistent_transcript_file_does_not_crash_or_block(self):
        result = self.run_hook({"transcript_path": "/nonexistent/path.jsonl", "session_id": "x"})
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
