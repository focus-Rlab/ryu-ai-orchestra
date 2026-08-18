from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Experience:
    experience_id: str
    title: str
    lesson: str
    required_evidence: tuple[str, ...]
    triggers: tuple[str, ...] = ()
    always_apply: bool = False


class ExperienceStore:
    """Portable SQLite store for lessons that must affect execution."""

    def __init__(self, database_path: str | Path):
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS experiences (
                    experience_id TEXT PRIMARY KEY, title TEXT NOT NULL,
                    lesson TEXT NOT NULL, required_evidence TEXT NOT NULL,
                    triggers TEXT NOT NULL, always_apply INTEGER NOT NULL DEFAULT 0,
                    active INTEGER NOT NULL DEFAULT 1
                );
                CREATE TABLE IF NOT EXISTS interactions (
                    task_id TEXT PRIMARY KEY, request TEXT NOT NULL,
                    matched_experiences TEXT NOT NULL, outcome TEXT,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            """)

    def upsert(self, experience: Experience) -> None:
        with self._connect() as connection:
            connection.execute("""
                INSERT INTO experiences VALUES (?, ?, ?, ?, ?, ?, 1)
                ON CONFLICT(experience_id) DO UPDATE SET
                    title=excluded.title, lesson=excluded.lesson,
                    required_evidence=excluded.required_evidence,
                    triggers=excluded.triggers, always_apply=excluded.always_apply,
                    active=1
            """, (
                experience.experience_id, experience.title, experience.lesson,
                json.dumps(experience.required_evidence, ensure_ascii=False),
                json.dumps(experience.triggers, ensure_ascii=False),
                int(experience.always_apply),
            ))

    def match(self, request: str) -> list[Experience]:
        normalized = request.casefold()
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM experiences WHERE active = 1 ORDER BY experience_id"
            ).fetchall()
        result = []
        for row in rows:
            triggers = tuple(json.loads(row["triggers"]))
            if row["always_apply"] or any(t.casefold() in normalized for t in triggers):
                result.append(self._from_row(row))
        return result

    def record_start(self, task_id: str, request: str,
                     experiences: Iterable[Experience]) -> None:
        ids = [item.experience_id for item in experiences]
        with self._connect() as connection:
            connection.execute("""
                INSERT OR REPLACE INTO interactions
                (task_id, request, matched_experiences, outcome)
                VALUES (?, ?, ?, NULL)
            """, (task_id, request, json.dumps(ids, ensure_ascii=False)))

    def record_outcome(self, task_id: str, outcome: str) -> None:
        with self._connect() as connection:
            connection.execute(
                "UPDATE interactions SET outcome = ? WHERE task_id = ?",
                (outcome, task_id),
            )

    @staticmethod
    def _from_row(row: sqlite3.Row) -> Experience:
        return Experience(
            row["experience_id"], row["title"], row["lesson"],
            tuple(json.loads(row["required_evidence"])),
            tuple(json.loads(row["triggers"])), bool(row["always_apply"]),
        )


DEFAULT_EXPERIENCES = (
    Experience("core-action-application", "記録を行動条件へ変換する",
               "関連経験と今回の適用証拠を残す。",
               ("experience_application_evidence",), always_apply=True),
    Experience("root-cause-before-fix", "表面修正で終わらせない",
               "問題時は原因と再発防止を確認する。",
               ("root_cause_evidence", "prevention_evidence"),
               ("問題", "ミス", "失敗", "原因", "動かない", "なんもならん", "不具合")),
    Experience("user-acceptance-separate", "技術テストと本人受入を分ける",
               "見た目や操作を伴う成果は本人受入まで完了にしない。",
               ("user_access_evidence", "user_acceptance_passed"),
               ("画面", "アプリ", "サイト", "ui", "デザイン", "公開")),
    Experience("paid-action-approval", "有料利用を勝手に開始しない",
               "料金が発生し得る操作は事前承認を得る。",
               ("paid_use_approval_passed",), ("有料", "課金", "api", "購入", "契約")),
    Experience("destructive-action-safety", "削除前に対象と復旧性を確認する",
               "削除・初期化は対象確認と復旧手段を必須にする。",
               ("target_confirmation_evidence", "rollback_evidence"),
               ("削除", "消す", "初期化", "上書き", "delete", "reset")),
    Experience("github-connector-fallback", "GitHub連携を先に使う",
               "CLIだけで不可能と判断せず接続済み連携を確認する。",
               ("available_path_evidence",),
               ("github", "プルリク", "プッシュ", "pr", "issue", "マージ")),
    Experience("state-source-check", "現在地の正本を同期する",
               "作業前後に現在地とGitHub状態の一致を検証する。",
               ("state_sync_evidence",),
               ("現在地", "project_state", "引き継ぎ", "次の作業", "フェーズ")),
    Experience("scope-before-execution", "目的との一致を実行前に確認する",
               "新作業と根本目的の対応を証明する。",
               ("goal_alignment_evidence",),
               ("実行", "作って", "実装", "開始", "進めて")),
    Experience("concise-communication", "情報量をユーザーに合わせる",
               "混乱時や短く求められた時は必要事項だけ伝える。",
               ("communication_fit_evidence",),
               ("短く", "必要なことだけ", "しゃべりすぎ", "混乱", "わかりやすく")),
    Experience("no-premature-completion", "途中で完了と言わない",
               "受入条件と実物証拠が揃うまで完了報告を拒否する。",
               ("acceptance_evidence",),
               ("完成", "完了", "終わり", "できた", "納品")),
)


def seed_default_experiences(store: ExperienceStore) -> None:
    for experience in DEFAULT_EXPERIENCES:
        store.upsert(experience)
