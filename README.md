# Ryu AI Orchestra

隆之介専用のAIエージェント組織を、役割・権限・記憶・評価・セキュリティの正本として管理し、ChatGPT、Claude、Codex、Gemini、GitHub Copilot等から再利用するための基盤です。

## 現在の段階

- Version: 0.5.0-draft
- Status: Stage 1完了後の役割・言語・ロードマップ整合修正中
- 現在の中核エージェント: Raphael
- 運用方式: GitHub正本・人間承認型の段階的オーケストレーション
- 作業中: Draft PR #5 / `stage2/role-language-roadmap-alignment`

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

> `focus-Rlab/ryu-ai-orchestra`の`README.md`と`PROJECT_HANDOFF.md`を最初に読み、今回必要な正本を確認してから作業して。

Codex、Claude Code、Gemini、GitHub Copilotでは、専用指示ファイルからこのREADMEを参照する構成です。

## 最低限の共通ルール

1. 会話履歴だけを正本にしない。
2. 新しいセッションは`README.md`の次に`PROJECT_HANDOFF.md`を読む。
3. 重要提案前に関係する正本を確認する。
4. 全作業で`GOVERNANCE.md`と`SECURITY.md`を適用する。
5. 新しいStage、文書、機能、エージェント、ルールを作る前に既存責任との重複を確認する。
6. ROADMAPは変更可能だが、Stage名、目的、順序、開始条件、完了条件を独断で変更しない。理由、変更案、利点、欠点、影響、推奨案を先に隆之介へ提示する。
7. 誤字、リンク、表記、空白など、意味を変えない小変更はmainへ直接コミットしてよい。それ以外は、同じ目的ごとに一つの専用ブランチとDraft PRを使う。意味を変えないか迷う場合はブランチとDraft PRを使う。
8. mainへ直接コミットした小変更は、コミットメッセージまたは報告に「意味を変えないと判断した理由」を残す。
9. 重要変更、削除、外部送信、公開、課金、本番反映、権限変更、mainマージは隆之介の承認後に行う。
10. 既存決定を確認せず、会話や推測だけで仕様を上書きしない。
11. 現行、提案、確定、保留を明確に区別する。
12. 完了時は、参照した正本、変更点、検証、未解決事項、承認待ちを報告し、重要な現在地を`PROJECT_HANDOFF.md`へ反映する。

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
| Stage 1の実行設計・引き継ぎ・評価 | `RAPHAEL_INITIAL_DESIGN.md`、`RAPHAEL_HANDOFF_PROTOCOL.md`、`RAPHAEL_TEST_PLAN.md`、`STAGE1_REVIEW_RESOLUTION.md` |

必要以上に全ファイルを毎回読まず、作業に必要な範囲だけ読む。ただし、重要変更では完全版と対応表まで確認する。

## 文書構造

### 現在状態・引き継ぎ

- `PROJECT_HANDOFF.md`: セッション変更、別AI移行、会話履歴欠落時に現在地と重要判断を復元する正本

### 完全版・監査層

- `MASTER_SPEC.md`: 会話で確定した内容を省略せず保持する完全版基準文書
- `SPEC_TRACEABILITY.md`: 完全版の各項目と分割正本の対応表

### 日常運用の分割正本

- `VISION.md`: 北極星と長期ビジョン
- `ROADMAP.md`: 現在地、実装順序、完了条件
- `USER.md`: 隆之介の価値観、判断基準、進め方
- `RECONSIDER.md`: 将来の再検討事項、暫定事項、保留事項
- `GOVERNANCE.md`: 権限、承認、変更管理、重複防止
- `SECURITY.md`: 外部アクセス、スキル、コード、成果物の安全基準
- `agents/raphael.md`: Raphael初期版の実行仕様

### Stage 1実行設計

- `RAPHAEL_INITIAL_DESIGN.md`: Raphael初期版の実行フローと役割分担
- `RAPHAEL_HANDOFF_PROTOCOL.md`: 複数環境間で文脈を忠実に渡す共通形式
- `RAPHAEL_TEST_PLAN.md`: 初期版の実運用・クロスモデル評価計画
- `STAGE1_REVIEW_BRIEF.md`: 独立レビューの入口
- `STAGE1_REVIEW_RESOLUTION.md`: Claudeレビュー指摘と対応結果
- `STAGE1_STATUS.md`: Stage 1の完了状態

### AI自動読込・実行入口

- `AGENTS.md`: Codex、Copilot等で使う共通エージェント指示
- `CLAUDE.md`: Claude Code向け入口
- `GEMINI.md`: Gemini向け入口
- `.github/copilot-instructions.md`: GitHub Copilotのリポジトリ共通指示
- `.github/agents/raphael.md`: GitHub CopilotのカスタムRaphael
- `OPERATING_GUIDE.md`: ツール別の具体的な運用方法

## 文書の優先関係

- 現在地と作業継続は`PROJECT_HANDOFF.md`で確認する。
- 日常作業では分割正本を使う。
- 情報欠落の確認、重要変更、実装前監査では`MASTER_SPEC.md`と`SPEC_TRACEABILITY.md`を使う。
- 完全版と分割正本が矛盾する場合、AIは勝手に片方を優先せず、差分と修正案を報告する。
- 承認された修正は、完全版・対応表・該当する分割正本へ同期する。
- AI専用入口ファイルはルールの複製元ではなく、このREADMEと正本への案内役として維持する。

## 現行仕様

現在の中核・現行仕様はRaphaelです。

旧Meta Agent Builder構想は削除済みです。将来、独立したAgent Builderが必要になった場合は、`RECONSIDER.md`の条件に基づきRaphaelが新規設計案を作成し、隆之介の承認後に追加します。旧ファイルや旧仕様を現行判断へ流用しません。

`GOVERNANCE.md`はすでに存在する。今後の全体設計でガバナンスをゼロから重複作成せず、必要な場合は既存文書の監査と不足補完を行う。

## 標準作業フロー

1. READMEとPROJECT_HANDOFFから現在地を確認する。
2. 必要な正本を選ぶ。
3. 目的、範囲、完了条件、承認条件を確認する。
4. 既存責任との重複を監査する。
5. 調査、設計、実装、検証を行う。
6. 小変更は監査理由を残してmainへ直接コミットできる。重要変更は一つの専用ブランチとDraft PRで提出する。
7. 正本との整合性、セキュリティ、テスト結果を確認する。
8. 隆之介の承認後に重要変更をmainへ反映する。
9. 重要な新決定は、関連する正本・完全版・対応表・PROJECT_HANDOFFへ同期する。
10. マージ済みの作業ブランチは削除し、常時存在する作業ブランチを原則1〜2本に抑える。

## 現在の未確定事項

Stage 2はまだ最終確定していない。

- 現行案: 要求整理・構想具体化エージェントをRaphaelが設計する
- 変更案: 先にAIオーケストラ全体の既存設計を監査し、重複を避けて不足と責任境界だけを補完する

ROADMAP変更は隆之介の承認前に確定しない。詳細は`PROJECT_HANDOFF.md`を参照する。