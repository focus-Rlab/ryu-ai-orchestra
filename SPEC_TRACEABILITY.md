# Specification Traceability Matrix

Version: 0.6.0-draft
Owner: Ryunosuke Matsumoto

## 目的

`MASTER_SPEC.md`の各決定が、日常運用で使用する分割正本とAI実行入口のどこへ反映されているかを追跡する。

重要変更時は、本表の対応先をすべて確認する。対応先が空欄、曖昧、矛盾している場合は、実装やmain反映を止めて修正する。

## 対応表

| MASTER_SPEC・重要決定 | 主な反映先 | 状態 |
|---|---|---|
| 文書の役割 | README.md / GOVERNANCE.md | 反映済み |
| 北極星・価値観 | VISION.md / USER.md | 反映済み |
| 避けること | MASTER_SPEC.md / USER.md / agents/raphael.md | 反映済み |
| RaphaelはAIオーケストラ全体を統括する最上位エージェント | MASTER_SPEC.md / README.md / USER.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / PROJECT_HANDOFF.md | 反映済み |
| 秘書業務はRaphaelの機能の一部 | MASTER_SPEC.md / README.md / USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / PROJECT_HANDOFF.md | 反映済み |
| エージェントとAIモデル・実行環境の区別 | MASTER_SPEC.md / README.md / USER.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_HANDOFF_PROTOCOL.md / RAPHAEL_TEST_PLAN.md / OPERATING_GUIDE.md | 反映済み |
| Agent Builderの扱い | MASTER_SPEC.md / RECONSIDER.md / GOVERNANCE.md / agents/raphael.md / PROJECT_HANDOFF.md | 反映済み |
| 全人生スコープ | MASTER_SPEC.md / USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 分析・要求整理 | MASTER_SPEC.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| タスク分解・詳細項目 | MASTER_SPEC.md / ROADMAP.md / agents/raphael.md | 反映済み |
| 統合・品質管理 | MASTER_SPEC.md / agents/raphael.md | 反映済み |
| ロードマップ・進捗 | MASTER_SPEC.md / ROADMAP.md / agents/raphael.md | 反映済み |
| エージェント組織管理 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md | 反映済み |
| 基本実行フロー | MASTER_SPEC.md / README.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / OPERATING_GUIDE.md | 反映済み |
| 実行可能な依頼では説明を繰り返さず先に実行する | MASTER_SPEC.md / README.md / USER.md / GOVERNANCE.md / PROJECT_HANDOFF.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_TEST_PLAN.md / OPERATING_GUIDE.md | 反映済み |
| 必要ツールの接続・権限・読取・書込障害を即時報告する | MASTER_SPEC.md / README.md / USER.md / GOVERNANCE.md / PROJECT_HANDOFF.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_HANDOFF_PROTOCOL.md / RAPHAEL_TEST_PLAN.md / OPERATING_GUIDE.md | 反映済み |
| PRマージ・ブランチ変更・作業完了直後に現在地を同期する | MASTER_SPEC.md / README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / ROADMAP.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_HANDOFF_PROTOCOL.md / RAPHAEL_TEST_PLAN.md / OPERATING_GUIDE.md | 反映済み |
| 情報不足の分類・質問最適化 | MASTER_SPEC.md / USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 自発性と反対強度 | MASTER_SPEC.md / USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 調査・実験 | MASTER_SPEC.md / SECURITY.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 最小有能チーム原則 | MASTER_SPEC.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 複数AI意見統合 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 自己改善ループ | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 根本原因分析・横断監査・一般化した再発防止 | MASTER_SPEC.md / README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / ROADMAP.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| 権限 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md | 反映済み |
| 隆之介の役割 | MASTER_SPEC.md / GOVERNANCE.md / USER.md | 反映済み |
| 成果物保存3段階 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| PROJECT_HANDOFFを現在地・セッション引き継ぎ正本とする | MASTER_SPEC.md / README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / OPERATING_GUIDE.md / RAPHAEL_HANDOFF_PROTOCOL.md | 反映済み |
| 小変更のmain直接コミット例外 | MASTER_SPEC.md / README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 判断に迷う場合のブランチ優先 | MASTER_SPEC.md / README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 小変更の監査理由記録 | MASTER_SPEC.md / README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 忠実な引き継ぎ | MASTER_SPEC.md / PROJECT_HANDOFF.md / RAPHAEL_HANDOFF_PROTOCOL.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 報告・重大ミス・セキュリティ | MASTER_SPEC.md / GOVERNANCE.md / SECURITY.md / agents/raphael.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| Stage 2は既存設計の監査と責任境界確定 | MASTER_SPEC.md / ROADMAP.md / README.md / PROJECT_HANDOFF.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| 旧Stage 2要求整理エージェントをStage 3へ移動 | MASTER_SPEC.md / ROADMAP.md / README.md / PROJECT_HANDOFF.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| クロスモデル再現性と10件評価 | MASTER_SPEC.md / ROADMAP.md / RAPHAEL_TEST_PLAN.md / agents/raphael.md | 反映済み |
| Ciel進化 | MASTER_SPEC.md / ROADMAP.md / RECONSIDER.md / agents/raphael.md | 反映済み |
| 確定・暫定・保留 | RECONSIDER.md / ROADMAP.md / RAPHAEL_TEST_PLAN.md / PROJECT_HANDOFF.md | 反映済み |
| Stage 1完了・後続訂正 | ROADMAP.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| READMEを唯一の入口とする | README.md / OPERATING_GUIDE.md | 反映済み |
| Codex・Copilot共通入口 | AGENTS.md / README.md | 反映済み |
| Claude自動入口 | CLAUDE.md / README.md | 反映済み |
| Gemini自動入口 | GEMINI.md / README.md | 反映済み |
| Copilot共通指示 | .github/copilot-instructions.md / README.md | 反映済み |
| GitHub custom Raphael | .github/agents/raphael.md / agents/raphael.md | 反映済み |

| Stage 2記憶ガバナンス | STAGE2_DECISION_LOG.md M-06〜M-09 / AGENT_STANDARD.md §§11,14 / GOVERNANCE.md §19 / MASTER_SPEC.md §23 | 反映済み |
| 信頼・代理判断・重要変更・緊急停止 | STAGE2_DECISION_LOG.md T-03,C-04,I-04,D-03 / AGENT_STANDARD.md §12 / GOVERNANCE.md §19 / MASTER_SPEC.md §23 | 反映済み |
| 試用・評価・統合・退役・引き継ぎ | STAGE2_DECISION_LOG.md T-04〜T-08 / AGENT_STANDARD.md §13 / agents/raphael.md / MASTER_SPEC.md §23 | 反映済み |
| Stage 2代表適用検証 | STAGE2_VALIDATION.md / AGENT_STANDARD.md | 合格 |

## 今回の横断監査結果

接続が途切れた可能性が高い会話区間まで遡り、PR #5変更対象、主要正本、Stage 1設計・引き継ぎ・評価文書を再監査した。

修正済み:

- 完全版に残ったRaphaelの古い役割表現
- AIモデルを責任主体として扱う古い表現
- 旧Stage 2を維持する記述
- マージ済みPR #5を作業中とする現在地
- PROJECT_HANDOFFの必読漏れ
- ツール接続・権限・読取・書込障害の報告ルール不足
- 実行可能な依頼で説明を繰り返す問題
- PRマージ後の現在地同期ゲート不足
- 接続障害・現在地同期・実行優先の評価テスト不足

Stage 2の確定設計を追加同期し、決定ログ、Agent Standard、完全版、ガバナンス、Raphael仕様の意味対応を確認した。

残存事項:

- Draft PR #6はmain未反映であり、隆之介の承認が必要
- Stage 2本体の新規エージェント追加標準・監査成果物はPR #6マージ後に実装する
- 正式評価ログ保存先、採点重み等は引き続き未確定

## 完全性ルール

- `MASTER_SPEC.md`に新しい重要項目を追加したら、本表にも追加する。
- 分割正本またはAI実行入口を変更したら、対応する行を再確認する。
- 「反映済み」とする前に、単語があるだけでなく意味と条件が保存されているか確認する。
- 完全版にしか存在しない運用必須事項を放置しない。
- 分割正本や実行入口にしか存在しない重要事項が見つかった場合、完全版への追記候補として明示する。
- 矛盾がある場合、独断で統合せず差分と推奨案を報告する。
- 現在地が変わった場合は、`README.md`、`PROJECT_HANDOFF.md`、`ROADMAP.md`、関係PR説明を同時に確認する。
- 重要なStage完了前に、完全版、対応表、分割正本、実行入口、Stage文書群の同期を再確認する。
