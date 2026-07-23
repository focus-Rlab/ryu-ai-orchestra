# Ryu AI Orchestra

隆之介専用のAIエージェント組織を、役割・権限・記憶・評価・セキュリティの正本として管理し、ChatGPT、Claude、Codex、Gemini、GitHub Copilot等から再利用するための基盤です。

## 現在の段階

- Version: 0.4.0-draft
- Status: Cross-model entrypoints and operating model review
- 現在の中核エージェント: Raphael
- 運用方式: GitHub正本・人間承認型の段階的オーケストレーション

## このREADMEの役割

このファイルは、すべての人間とAIが最初に読む**唯一の入口・読込ルーター**です。

新しいセッションでは原則、次の一文だけで開始できます。

> `focus-Rlab/ryu-ai-orchestra`のREADMEを入口として、今回必要な正本を読んでから作業して。

Codex、Claude Code、Gemini、GitHub Copilotでは、専用指示ファイルからこのREADMEを自動参照する構成です。

## 最低限の共通ルール

1. 会話履歴だけを正本にしない。
2. 重要提案前に関係する正本を確認する。
3. 全作業で`GOVERNANCE.md`と`SECURITY.md`を適用する。
4. mainへ直接変更せず、専用ブランチとDraft PRを使う。
5. 重要変更、削除、外部送信、公開、課金、本番反映、権限変更、mainマージは隆之介の承認後に行う。
6. 既存決定を確認せず、会話や推測だけで仕様を上書きしない。
7. 完了時は、参照した正本、変更点、検証、未解決事項、承認待ちを報告する。

## 作業別の読込ルーター

| 作業 | 必ず読むもの |
|---|---|
| すべての作業 | `README.md`、`GOVERNANCE.md`、`SECURITY.md` |
| 隆之介の希望・判断基準が重要 | 上記＋`USER.md` |
| Raphaelとして作業 | 上記＋`USER.md`、`agents/raphael.md` |
| 計画、進捗、実装順序 | 上記＋`ROADMAP.md` |
| 長期方針、目的との整合 | 上記＋`VISION.md` |
| エージェントやスキルの新設・分解・統合 | 上記＋`MASTER_SPEC.md`、`RECONSIDER.md`、`SPEC_TRACEABILITY.md` |
| 権限、正本、重要設計の変更 | 上記＋`MASTER_SPEC.md`、`RECONSIDER.md`、`SPEC_TRACEABILITY.md` |
| 過去の決定や情報落ちの確認 | `MASTER_SPEC.md`、`SPEC_TRACEABILITY.md`、関係する分割正本 |
| AIツールごとの具体的な使い方 | `OPERATING_GUIDE.md` |

必要以上に全ファイルを毎回読まず、作業に必要な範囲だけ読む。ただし、重要変更では完全版と対応表まで確認する。

## 文書構造

### 完全版・監査層

- `MASTER_SPEC.md`: 会話で確定した内容を省略せず保持する完全版基準文書
- `SPEC_TRACEABILITY.md`: 完全版の各項目と分割正本の対応表

### 日常運用の分割正本

- `VISION.md`: 北極星と長期ビジョン
- `ROADMAP.md`: 現在地、実装順序、完了条件
- `USER.md`: 隆之介の価値観、判断基準、進め方
- `RECONSIDER.md`: 将来の再検討事項、暫定事項、保留事項
- `GOVERNANCE.md`: 権限、承認、変更管理
- `SECURITY.md`: 外部アクセス、スキル、コード、成果物の安全基準
- `agents/raphael.md`: Raphael初期版の実行仕様

### AI自動読込・実行入口

- `AGENTS.md`: Codex、Copilot等で使う共通エージェント指示
- `CLAUDE.md`: Claude Code向け入口
- `GEMINI.md`: Gemini向け入口
- `.github/copilot-instructions.md`: GitHub Copilotのリポジトリ共通指示
- `.github/agents/raphael.md`: GitHub CopilotのカスタムRaphael
- `OPERATING_GUIDE.md`: ツール別の具体的な運用方法

## 文書の優先関係

- 日常作業では分割正本を使う。
- 情報欠落の確認、重要変更、実装前監査では`MASTER_SPEC.md`と`SPEC_TRACEABILITY.md`を使う。
- 完全版と分割正本が矛盾する場合、AIは勝手に片方を優先せず、差分と修正案を報告する。
- 承認された修正は、完全版・対応表・該当する分割正本へ同期する。
- AI専用入口ファイルはルールの複製元ではなく、このREADMEと正本への案内役として維持する。

## 現行仕様

現在の中核・現行仕様はRaphaelです。

旧Meta Agent Builder構想は削除済みです。将来、独立したAgent Builderが必要になった場合は、`RECONSIDER.md`の条件に基づきRaphaelが新規設計案を作成し、隆之介の承認後に追加します。旧ファイルや旧仕様を現行判断へ流用しません。

## 標準作業フロー

1. READMEから必要な正本を選ぶ。
2. 目的、範囲、完了条件、承認条件を確認する。
3. 調査、設計、実装、検証を行う。
4. 変更は専用ブランチとDraft PRで提出する。
5. 正本との整合性、セキュリティ、テスト結果を確認する。
6. 隆之介の承認後にmainへ反映する。
7. 重要な新決定は、関連する正本・完全版・対応表へ同期する。

## 次の段階

1. PR #2の内容とリポジトリ全体の冗長性監査
2. 隆之介の承認後にmainへ反映
3. Raphael初期版の実装計画作成
4. 実行環境、入出力、状態管理の決定
5. セキュリティ・承認・評価機能を含む初期実装
6. 約1か月・最低10件の実運用評価
7. 要求整理・構想具体化エージェントの設計
8. Ciel相当への進化判定
