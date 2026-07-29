# Ryu AI Orchestra

隆之介専用のAIエージェント組織を、役割・権限・記憶・評価・セキュリティの正本として管理し、ChatGPT、Claude、Codex、Gemini、GitHub Copilot等から再利用するための基盤です。

## 現在の段階

- Version: 0.8.0-draft
- Stage: Stage 2「AIオーケストラ既存設計の監査と責任境界確定」
- Status: PR #5マージ後の横断再監査・同期漏れ修正を完了し、Draft PR #6の承認待ち
- 現在の中核エージェント: Raphael
- 運用方式: GitHub正本・人間承認型の段階的オーケストレーション
- 完了済み: PR #5をmainへマージ
- 作業中: Draft PR #6 / `stage2/post-merge-audit-fix`

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

> `focus-Rlab/ryu-ai-orchestra`の`README.md`と`PROJECT_HANDOFF.md`を最初に読み、現在の作業ブランチ・PRと今回必要な正本を確認してから作業して。

## 最低限の共通ルール

1. 会話履歴だけを正本にしない。
2. 新しいセッションは`README.md`の次に`PROJECT_HANDOFF.md`を読む。
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

## 作業別の読込ルーター

| 作業 | 必ず読むもの |
|---|---|
| すべての作業 | `README.md`、`PROJECT_HANDOFF.md`、`GOVERNANCE.md`、`SECURITY.md` |
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

### AI自動読込・実行入口

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`
- `.github/copilot-instructions.md`
- `.github/agents/raphael.md`
- `OPERATING_GUIDE.md`

AI専用入口は正本本文の複製元ではなく、このREADMEと関係正本への案内役とする。

## 現行仕様とロードマップ

- Raphael: AIオーケストラ全体の最上位統括エージェント
- Stage 2: `AIオーケストラ既存設計の監査と責任境界確定`
- Stage 2への変更: 隆之介の承認済み
- 旧Stage 2「要求整理・構想具体化エージェント」: Stage 3へ移動
- Stage 3の専門エージェント設計主体: Raphael
- PR #5: mainへマージ済み
- PR #6: 過去の横断再監査・同期漏れ修正。main側の現在状態を基準に扱う
- PR #7: incident logをmainへ統合済み
- PR #8: Stage 2決定ログの一部をmainへ統合済み
- 現在のStage 2作業ブランチ: `stage2/agent-governance`
- Stage 2設計質問: 完了
- 現在作業: 正本同期、整合監査、代表例確認、main統合準備
- mainへのマージ: 隆之介の明示承認待ち

詳細は`ROADMAP.md`と`PROJECT_HANDOFF.md`を参照する。
