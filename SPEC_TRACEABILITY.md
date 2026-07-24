# Specification Traceability Matrix

Version: 0.5.0-draft
Owner: Ryunosuke Matsumoto

## 目的

`MASTER_SPEC.md`の各決定が、日常運用で使用する分割正本とAI実行入口のどこへ反映されているかを追跡する。

重要変更時は、本表の対応先をすべて確認する。対応先が空欄、曖昧、矛盾している場合は、実装やmain反映を止めて修正する。

## 対応表

| MASTER_SPEC・重要決定 | 主な反映先 | 状態 |
|---|---|---|
| 1. 文書の役割 | README.md / GOVERNANCE.md | 反映済み |
| 2. 北極星・価値観 | VISION.md / USER.md | 反映済み |
| 2. 避けること | USER.md / agents/raphael.md | 反映済み |
| RaphaelはAIオーケストラ全体を統括する最上位エージェント | README.md / USER.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / PROJECT_HANDOFF.md | 分割正本は反映済み・MASTER_SPEC要同期 |
| 秘書業務はRaphaelの機能の一部 | README.md / USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / PROJECT_HANDOFF.md | 分割正本は反映済み・MASTER_SPEC要同期 |
| エージェントとAIモデル・実行環境の区別 | README.md / USER.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_HANDOFF_PROTOCOL.md / RAPHAEL_TEST_PLAN.md | 分割正本は反映済み・MASTER_SPEC要同期 |
| 3. Agent Builderの扱い | RECONSIDER.md / GOVERNANCE.md / agents/raphael.md / PROJECT_HANDOFF.md | 反映済み |
| 4. 全人生スコープ | USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 5. 分析・要求整理 | agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 5. タスク分解・詳細項目 | ROADMAP.md / agents/raphael.md | 反映済み |
| 5. 統合・品質管理 | agents/raphael.md | 反映済み |
| 5. ロードマップ・進捗 | ROADMAP.md / agents/raphael.md | 反映済み |
| 5. エージェント組織管理 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 6. 基本実行フロー | README.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 実行可能な依頼では説明を繰り返さず先に実行する | README.md / USER.md / PROJECT_HANDOFF.md | 反映済み |
| 必要ツールの接続・権限・読取・書込障害を即時報告する | README.md / USER.md / PROJECT_HANDOFF.md | 反映済み・GOVERNANCE / MASTER_SPEC / テストへ同期要 |
| PRマージ・ブランチ変更・作業完了直後に現在地を同期する | README.md / PROJECT_HANDOFF.md | 反映済み・GOVERNANCE / MASTER_SPECへ同期要 |
| 7. 情報不足の分類・質問最適化 | USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 8. 自発性と反対強度 | USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 9. 調査・実験 | SECURITY.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 10. 最小有能チーム原則 | GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 11. 複数AI意見統合 | GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 12. 自己改善ループ | GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 根本原因分析・横断監査・一般化した再発防止 | README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / RAPHAEL_TEST_PLAN.md | 反映済み・MASTER_SPEC要同期 |
| 13. 権限 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 14. 隆之介の役割 | GOVERNANCE.md / USER.md | 反映済み |
| 15. 成果物保存3段階 | GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 16. 正本管理 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md | 反映済み |
| PROJECT_HANDOFFを現在地・セッション引き継ぎ正本とする | README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / OPERATING_GUIDE.md | OPERATING_GUIDE・MASTER_SPEC要同期 |
| 16. 小変更のmain直接コミット例外 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 16. 判断に迷う場合のブランチ優先 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 16. 小変更の監査理由記録 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 17. 忠実な引き継ぎ | PROJECT_HANDOFF.md / RAPHAEL_HANDOFF_PROTOCOL.md / OPERATING_GUIDE.md / agents/raphael.md | OPERATING_GUIDE・agents/raphael要同期 |
| 18. 報告・重大ミス・セキュリティ | GOVERNANCE.md / SECURITY.md / agents/raphael.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| Stage 2は既存設計の監査と責任境界確定 | ROADMAP.md / README.md / PROJECT_HANDOFF.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み・MASTER_SPEC要同期 |
| 旧Stage 2要求整理エージェントをStage 3へ移動 | ROADMAP.md / README.md / PROJECT_HANDOFF.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み・MASTER_SPEC要同期 |
| 19. クロスモデル再現性と10件評価 | ROADMAP.md / RAPHAEL_TEST_PLAN.md / agents/raphael.md | 反映済み |
| 20. Ciel進化 | ROADMAP.md / RECONSIDER.md / agents/raphael.md | 反映済み |
| 21. 確定・暫定・保留 | RECONSIDER.md / ROADMAP.md / RAPHAEL_TEST_PLAN.md / PROJECT_HANDOFF.md | 反映済み |
| 22. Stage 1完了前チェック | ROADMAP.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| READMEを唯一の入口とする | README.md / OPERATING_GUIDE.md | 反映済み |
| Codex・Copilot共通入口 | AGENTS.md / README.md | 反映済み |
| Claude自動入口 | CLAUDE.md / README.md | 反映済み |
| Gemini自動入口 | GEMINI.md / README.md | 反映済み |
| Copilot共通指示 | .github/copilot-instructions.md / README.md | 反映済み |
| GitHub custom Raphael | .github/agents/raphael.md / agents/raphael.md | 反映済み |

## 今回の横断監査で確認された未同期

- `MASTER_SPEC.md`には、Raphaelを初期版の「秘書」として並列に置く古い表現、AIモデルを責任主体として扱う古い表現、Stage 2変更前の表現が残っている。
- `OPERATING_GUIDE.md`には、`PROJECT_HANDOFF.md`をセッション開始時の必読正本に含めない古い開始文と、接続障害の即時報告ルール不足がある。
- `agents/raphael.md`には、Statusと初期役割の古い表現、`PROJECT_HANDOFF.md`の必読漏れ、担当エージェントとAIモデル選択の手順不足がある。
- `ROADMAP.md`の「次の具体的行動」には、マージ済みPR #5を未完了として扱う古い記述がある。
- `GOVERNANCE.md`と`RAPHAEL_TEST_PLAN.md`には、必要ツールへの接続・権限・書込障害を即時報告する明示ルールと検証項目が不足している。

上記はDraft PR #6の同一ブランチ内で修正対象とする。修正が完了するまで、本表で該当項目を「完全反映済み」と扱わない。

## 完全性ルール

- `MASTER_SPEC.md`に新しい重要項目を追加したら、本表にも追加する。
- 分割正本またはAI実行入口を変更したら、対応する行を再確認する。
- 「反映済み」とする前に、単語があるだけでなく意味と条件が保存されているか確認する。
- 完全版にしか存在しない運用必須事項を放置しない。
- 分割正本や実行入口にしか存在しない重要事項が見つかった場合、完全版への追記候補として明示する。
- 矛盾がある場合、AIは独断で統合せず差分と推奨案を報告する。
- 現在地が変わった場合は、`README.md`、`PROJECT_HANDOFF.md`、`ROADMAP.md`と作業中PRの説明を同時に確認する。
- Stage 1を完了扱いにする前に、`MASTER_SPEC.md`、本表、`ROADMAP.md`、`USER.md`、`GOVERNANCE.md`、`OPERATING_GUIDE.md`、`agents/raphael.md`、Stage 1実行文書群の同期を再確認する。
