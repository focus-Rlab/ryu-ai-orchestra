# Specification Traceability Matrix

Version: 0.4.0-draft
Owner: Ryunosuke Matsumoto

## 目的

`MASTER_SPEC.md`の各決定が、日常運用で使用する分割正本とAI実行入口のどこへ反映されているかを追跡する。

重要変更時は、本表の対応先をすべて確認する。対応先が空欄、曖昧、矛盾している場合は、実装やmain反映を止めて修正する。

| MASTER_SPEC項目 | 主な反映先 | 状態 |
|---|---|---|
| 1. 文書の役割 | README.md / GOVERNANCE.md | 反映済み |
| 2. 北極星・価値観 | VISION.md / USER.md | 反映済み |
| 2. 避けること | USER.md / agents/raphael.md | 反映済み |
| 3. 初期構成 | ROADMAP.md / RECONSIDER.md / agents/raphael.md | 反映済み |
| 3. Agent Builderの扱い | RECONSIDER.md / agents/raphael.md | 反映済み |
| 4. 全人生スコープ | USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 5. 分析・要求整理 | agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 5. タスク分解・詳細項目 | ROADMAP.md / agents/raphael.md | 反映済み |
| 5. 統合・品質管理 | agents/raphael.md | 反映済み |
| 5. ロードマップ・進捗 | ROADMAP.md / agents/raphael.md | 反映済み |
| 5. エージェント組織管理 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 6. 基本実行フロー | agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 7. 情報不足の分類・質問最適化 | USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 8. 自発性と反対強度 | USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 9. 調査・実験 | SECURITY.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 10. 最小有能チーム原則 | GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 11. 複数AI意見統合 | GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 12. 自己改善ループ | GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 13. 権限 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 14. 隆之介の役割 | GOVERNANCE.md / USER.md | 反映済み |
| 15. 成果物保存3段階 | GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 16. 正本管理 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md | 反映済み |
| 16. 小変更のmain直接コミット例外 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 16. 判断に迷う場合のブランチ優先 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 16. 小変更の監査理由記録 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 17. 忠実な引き継ぎ | RAPHAEL_HANDOFF_PROTOCOL.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 18. 報告・重大ミス・セキュリティ | GOVERNANCE.md / SECURITY.md / agents/raphael.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| 19. クロスモデル再現性と10件評価 | ROADMAP.md / RAPHAEL_TEST_PLAN.md / agents/raphael.md | 反映済み |
| 20. Ciel進化 | ROADMAP.md / RECONSIDER.md / agents/raphael.md | 反映済み |
| 21. 確定・暫定・保留 | RECONSIDER.md / ROADMAP.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| 22. Stage 1完了前チェック | ROADMAP.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| READMEを唯一の入口とする | README.md / OPERATING_GUIDE.md | 反映済み |
| Codex・Copilot共通入口 | AGENTS.md / README.md | 反映済み |
| Claude自動入口 | CLAUDE.md / README.md | 反映済み |
| Gemini自動入口 | GEMINI.md / README.md | 反映済み |
| Copilot共通指示 | .github/copilot-instructions.md / README.md | 反映済み |
| GitHub custom Raphael | .github/agents/raphael.md / agents/raphael.md | 反映済み |

## 完全性ルール

- `MASTER_SPEC.md`に新しい重要項目を追加したら、本表にも追加する。
- 分割正本またはAI実行入口を変更したら、対応する行を再確認する。
- 「反映済み」とする前に、単語があるだけでなく意味と条件が保存されているか確認する。
- 完全版にしか存在しない運用必須事項を放置しない。
- 分割正本や実行入口にしか存在しない重要事項が見つかった場合、完全版への追記候補として明示する。
- 矛盾がある場合、AIは独断で統合せず差分と推奨案を報告する。
- Stage 1を完了扱いにする前に、`MASTER_SPEC.md`、本表、`ROADMAP.md`、`USER.md`、`GOVERNANCE.md`、`OPERATING_GUIDE.md`、`agents/raphael.md`、Stage 1実行文書群の同期を再確認する。
