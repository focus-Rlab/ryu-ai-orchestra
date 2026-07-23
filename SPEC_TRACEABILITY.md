# Specification Traceability Matrix

Version: 0.2.0-draft
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
| 4.1 分析・要求整理 | agents/raphael.md | 反映済み |
| 4.2 タスク分解・詳細項目 | ROADMAP.md / agents/raphael.md | 反映済み |
| 4.3 統合・品質管理 | agents/raphael.md | 反映済み |
| 4.4 ロードマップ・進捗 | ROADMAP.md / agents/raphael.md | 反映済み |
| 4.5 エージェント組織管理 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 5. 情報不足の分類 | agents/raphael.md | 反映済み |
| 6. 質問管理 | USER.md / agents/raphael.md | 反映済み |
| 7. 調査 | SECURITY.md / agents/raphael.md | 反映済み |
| 8. 実験 | agents/raphael.md | 反映済み |
| 9. 権限 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 10. 隆之介の役割 | GOVERNANCE.md / USER.md | 反映済み |
| 11. 報告形式 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 12. 重大ミス・再発防止 | GOVERNANCE.md / agents/raphael.md | 反映済み |
| 13. セキュリティ | SECURITY.md / GOVERNANCE.md / agents/raphael.md | 反映済み |
| 14. 正本管理 | README.md / GOVERNANCE.md / OPERATING_GUIDE.md | 反映済み |
| 15. 初期版評価 | ROADMAP.md / agents/raphael.md | 反映済み |
| 16. Ciel進化 | ROADMAP.md / RECONSIDER.md / agents/raphael.md | 反映済み |
| 17. 確定・暫定・保留 | RECONSIDER.md / ROADMAP.md | 反映済み |
| 18. 実装前チェック | ROADMAP.md / OPERATING_GUIDE.md | 反映済み |
| 19. 実装順序 | ROADMAP.md | 反映済み |
| READMEを唯一の入口とする | README.md / OPERATING_GUIDE.md | 反映済み・MASTER_SPEC追記候補 |
| Codex・Copilot共通入口 | AGENTS.md / README.md | 反映済み・MASTER_SPEC追記候補 |
| Claude自動入口 | CLAUDE.md / README.md | 反映済み・MASTER_SPEC追記候補 |
| Gemini自動入口 | GEMINI.md / README.md | 反映済み・MASTER_SPEC追記候補 |
| Copilot共通指示 | .github/copilot-instructions.md / README.md | 反映済み・MASTER_SPEC追記候補 |
| GitHub custom Raphael | .github/agents/raphael.md / agents/raphael.md | 反映済み・MASTER_SPEC追記候補 |
| AIツールの使い分け | OPERATING_GUIDE.md | 反映済み・MASTER_SPEC追記候補 |
| セッション終了時の引き継ぎ | OPERATING_GUIDE.md / GOVERNANCE.md | 反映済み・MASTER_SPEC追記候補 |

## 完全性ルール

- `MASTER_SPEC.md`に新しい重要項目を追加したら、本表にも追加する。
- 分割正本またはAI実行入口を変更したら、対応する行を再確認する。
- 「反映済み」とする前に、単語があるだけでなく意味と条件が保存されているか確認する。
- 完全版にしか存在しない運用必須事項を放置しない。
- 分割正本や実行入口にしか存在しない重要事項が見つかった場合、完全版への追記候補として明示する。
- 矛盾がある場合、AIは独断で統合せず差分と推奨案を報告する。
