# Ryu AI Orchestra

隆之介専用のAIエージェント組織を、役割・権限・記憶・評価・セキュリティの正本として管理し、ChatGPT、Claude、Codex、Gemini、GitHub Copilot等から再利用するための基盤です。

## 現在の段階

- Version: 0.9.0-draft
- Stage: V1 Week 0「正本完全性回復と実行基盤確定」
- Status: Stage 2・PR #9完了後に判明したV1ロードマップ反映漏れを専用ブランチで監査・修正中
- 現在の中核エージェント: Raphael
- 運用方式: GitHub正本・人間承認型の段階的オーケストレーション
- 完了済み: Stage 0〜Stage 2、PR #1〜#9をmainへマージ
- 現在の作業先: `agent/roadmap-and-canonical-audit`

## Raphaelの確定した位置づけ

Raphaelは秘書専用AIではない。AIオーケストラ全体を統括する最上位の中核エージェントである。

- 仕事の割り振り先: 専門エージェント
- ChatGPT、Claude、Codex、Gemini等: 担当エージェントが作業するAIモデルまたは実行環境
- Raphaelの責任: 全体判断、優先順位、タスク分解、担当エージェント選択、モデル・環境選択、統合、品質、矛盾解消、進捗、改善、組織設計
- 秘書業務: Raphaelの担当領域の一部。将来必要なら専門エージェントへ分離可能
- エージェント設計: 現時点ではRaphaelの中核機能。独立Agent Builderは未採用

## このREADMEの役割

このファイルは、すべての人間とAIが最初に読む**唯一の入口・読込ルーター**です。

新しいセッションでは原則、次の一文で開始する。

> `focus-Rlab/ryu-ai-orchestra`の`README.md`、`STARTUP_CONTEXT.md`、`PROJECT_HANDOFF.md`を最初に読み、現在の作業ブランチ・PRと今回必要な正本を確認してから作業して。

## 最低限の共通ルール

1. 会話履歴だけを正本にしない。
2. 新しいセッションは`README.md`の次に`STARTUP_CONTEXT.md`と`PROJECT_HANDOFF.md`を読む。
3. 重要提案前に関係する正本を確認する。
4. 全作業で`GOVERNANCE.md`と`SECURITY.md`を適用する。
5. 新しいStage、文書、機能、エージェント、ルールを作る前に既存責任との重複を確認する。
6. ROADMAPは変更可能だが、Stage名、目的、順序、開始条件、完了条件を独断で変更しない。理由、変更案、利点、欠点、影響、推奨案を先に隆之介へ提示する。
7. 誤字、リンク、表記、空白など、意味を変えない小変更だけmainへ直接コミットできる。それ以外は専用ブランチとDraft PRを使う。
8. 重要変更、削除、外部送信、公開、課金、本番反映、権限変更、mainマージは隆之介の承認後に行う。
9. 既存決定を確認せず、会話や推測だけで仕様を上書きしない。
10. 現行、提案、確定、保留を明確に区別する。
11. 問題が起きたら、表面症状だけでなく根本原因を特定し、類似ミスを横断監査し、一般化した再発防止を正本とテストへ反映する。
12. 実行可能な依頼では同じ計画説明を繰り返さず、先に作業し、一区切りで結果を報告する。
13. 必要ツールへの接続、権限、読取・書込可否に問題が起きた場合、その時点で制約、実行済み、未実行を報告する。
14. PRマージ、ブランチ変更、作業完了など現在地が変わった直後に`README.md`、`PROJECT_HANDOFF.md`、`ROADMAP.md`、関係PR説明を同期する。
15. 完了時は、参照した正本、変更点、検証、未解決事項、承認待ちを報告する。
16. 重要な長期記憶、決定、禁止、必須手順、承認境界、重大ミスと再発防止、その他後続AIの判断を変える内容は、最初の実装段階で正本へ分類・伝播し、全AIの起動時必読セットから到達可能にする。
17. 隆之介の発言を自動肯定せず、事実・前提・反例・不確実性・既存決定との整合性から評価する。同意目的の「正しい」「その通り」は使用しない。

## 作業別の読込ルーター

| 作業 | 必ず読むもの |
|---|---|
| すべての作業 | `README.md`、`STARTUP_CONTEXT.md`、`PROJECT_HANDOFF.md`、`GOVERNANCE.md`、`SECURITY.md` |
| 隆之介の希望・判断基準が重要 | 上記＋`USER.md` |
| Raphaelとして作業 | 上記＋`USER.md`、`agents/raphael.md` |
| 計画、進捗、実装順序 | 上記＋`ROADMAP.md` |
| 長期方針、目的との整合 | 上記＋`VISION.md` |
| エージェントやスキルの新設・分解・統合 | 上記＋`MASTER_SPEC.md`、`RECONSIDER.md`、`SPEC_TRACEABILITY.md` |
| 権限、正本、重要設計の変更 | 上記＋`MASTER_SPEC.md`、`VISION.md`、`RECONSIDER.md`、`SPEC_TRACEABILITY.md` |
| 過去の決定や情報落ちの確認 | `PROJECT_HANDOFF.md`、`MASTER_SPEC.md`、`SPEC_TRACEABILITY.md`、関係する分割正本 |
| AIツールごとの具体的な使い方 | `OPERATING_GUIDE.md` |
| Stage 1設計・引き継ぎ・評価 | `RAPHAEL_INITIAL_DESIGN.md`、`RAPHAEL_HANDOFF_PROTOCOL.md`、`RAPHAEL_TEST_PLAN.md` |

必要以上に全ファイルを毎回読まない。ただし、重要変更では完全版と対応表まで確認する。

## 文書構造

### 起動時共通文脈

- `STARTUP_CONTEXT.md`: 全AIが作業開始時に共有する重要情報の分類、必読セット、伝播・検証手順

### 現在状態・引き継ぎ

- `PROJECT_HANDOFF.md`: 現在地、確定事項、作業中PR、次の一手を復元する正本

### 完全版・監査層

- `MASTER_SPEC.md`: 確定内容を省略せず保持する完全版
- `SPEC_TRACEABILITY.md`: 完全版、分割正本、実行入口の対応表

### 日常運用の分割正本

- `VISION.md`: 北極星と長期ビジョン
- `ROADMAP.md`: 現在地、実装順序、完了条件
- `USER.md`: 隆之介の価値観、判断基準、進め方
- `RECONSIDER.md`: 将来の再検討事項、暫定事項、保留事項
- `GOVERNANCE.md`: 権限、承認、変更管理、重複防止、接続障害報告、再発防止
- `SECURITY.md`: 外部アクセス、スキル、コード、成果物の安全基準
- `agents/raphael.md`: Raphaelの現在の実行仕様

### Stage 1実行設計・評価

- `RAPHAEL_INITIAL_DESIGN.md`: Raphaelの基本実行フロー
- `RAPHAEL_HANDOFF_PROTOCOL.md`: 複数環境間の引き継ぎ形式
- `RAPHAEL_TEST_PLAN.md`: 実運用・クロスモデル・障害対応評価計画
- `STAGE1_REVIEW_BRIEF.md`: 独立レビューの履歴入口
- `STAGE1_REVIEW_RESOLUTION.md`: レビュー指摘と対応記録
- `STAGE1_STATUS.md`: Stage 1完了状態
- `STAGE2_VALIDATION.md`: Stage 2標準の代表適用・整合確認

### AI自動読込・実行入口

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.github/copilot-instructions.md`
- `.github/agents/raphael.md`
- `OPERATING_GUIDE.md`

AI専用入口は正本本文の複製元ではなく、このREADMEと関係正本への案内役とする。

## 現行仕様とロードマップ

- 最終目標: 自己改善型・分野適応型の汎用オーケストレーターRaphael
- アプリ開発: 最初の検証領域であり、最終目的ではない
- V1構造: 汎用コア／ドメインパック／ツールコネクタ／分野別評価パック
- 初月資源: 週14時間、約56時間、API上限10,000円
- 費用ゲート: 7,000円警告、9,000円高性能モデル制限、10,000円自動停止
- 最初の実案件: Raphael自身のコード・設計改善 → 小規模新規アプリ
- 現在: Week 0で会話・決定ログ・全正本の完全性を回復中
- 次: Week 1の汎用コア最小実装
- 正式承認チャネル: 現段階ではChatGPT
- mainマージ、外部公開・送信・提出、本番反映、課金等は隆之介の承認が必要
- `INCIDENT_LOG.md`に残る評価基準の正式承認は、別途未決定のまま維持

詳細は`ROADMAP.md`と`PROJECT_HANDOFF.md`を参照する。
