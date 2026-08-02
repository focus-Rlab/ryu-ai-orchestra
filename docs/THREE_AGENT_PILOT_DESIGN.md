# 3体サブエージェントパイロット設計記録

Version: 0.1.0-draft
Date: 2026-08-01
Owner: Ryunosuke Matsumoto
統括: Raphael（Claude Code, Agent Teams不使用、プロジェクト用カスタムサブエージェント使用）

## 目的

Raphaelを上位オーケストレーターとして、Claude Codeのプロジェクト用カスタムサブエージェント機構（`.claude/agents/`）で以下3体を作成・検証する。

1. requirements-designer：要件設計エージェント
2. implementer：実装エージェント
3. tester-evaluator：テスト・評価エージェント

要件設計→実装→テスト・評価という依存関係があるため、原則として直列実行する。

## 位置づけ（Week 3との関係）

本パイロットは、進行中のIssue #15（V1 Week 3: Small app transferability validation）そのものではない。Week 3を将来実行するための**エージェント連携基盤を検証する別作業**であり、Issue #15の要件インタビュー（次の質問：アプリの目的から開始する5問）は一時停止として保持し、破棄・完了扱いにしない。詳細は`PROJECT_STATE.json`の`paused_issue`を参照する。

## 正本と実行入口の構造

既存リポジトリの原則（「AI専用入口は正本本文の複製元ではなく案内役」、`.github/agents/raphael.md`↔`agents/raphael.md`のパターン）に従い、二層構造を採用する。

| 層 | ファイル | 役割 | 正本か |
|---|---|---|---|
| 正本 | `agents/requirements-designer.md`, `agents/implementer.md`, `agents/tester-evaluator.md` | `AGENT_STANDARD.md` §8テンプレートに準拠した完全なエージェント定義 | **正**。矛盾時はこちらが優先 |
| 実行入口 | `.claude/agents/requirements-designer.md`, `.claude/agents/implementer.md`, `.claude/agents/tester-evaluator.md` | Claude Codeが実際に読み込むYAML frontmatter付きサブエージェント設定。責任境界・禁止事項の要点と正本参照指示を含む | 副。正本の要約実装であり、単なる参照リンクだけでは不十分なため、Claude Codeが確実に読み込む本文にも責任境界・禁止事項を明記した |

外部参照だけに頼らなかった理由: Claude Codeのサブエージェントはfrontmatter＋本文がそのままシステムプロンプトとして使われるため、「正本を読んで従ってください」という指示だけでは、正本の中身（禁止事項の詳細）が確実に反映される保証がない。そのため実行入口にも要点を直接記載し、詳細と齟齬があれば正本を優先する旨を明記した。

## ツール・ファイル権限：技術的強制／プロンプト規則／Raphael検査の区分

Claude Codeの`.claude/agents/*.md`における`tools:`frontmatterは、**ツール名単位の許可制であり、技術的に強制される**（未許可のツールは呼び出し自体が拒否される）。ただし以下は技術的に強制されない。

- パス単位・ディレクトリ単位の読み書き制限（`tools`はツール名のみを制御し、"このディレクトリだけ書き込み可"のような制限機構は用意されていない）
- コマンド単位の制限（Bashを許可すると、シェルコマンド全般が実行可能になり、"git pushだけ禁止"のような制限は`tools`設定だけでは行えない）

この限界を踏まえ、各エージェントの制限を3種類に区分して記載する。

| 区分 | 意味 | 担保方法 |
|---|---|---|
| 技術的強制 | Claude Codeのharnessが実行前に強制的にブロックする | `.claude/agents/*.md`の`tools:`許可リスト（未許可ツールは呼び出し自体が失敗する） |
| プロンプト規則 | エージェントへの指示として明記するが、技術的には破れる可能性がある | `.claude/agents/*.md`本文・`agents/*.md`の「行動規則」「Prohibited actions」 |
| Raphael検査 | エージェントの出力・差分・git履歴をRaphaelが事後レビューして担保する | 各実行後にRaphaelが差分・実行ログ・応答内容を確認し、`evaluations/three-agent-pilot/`へ記録する |

### エージェント別の実際の区分

| エージェント | 技術的強制 | プロンプト規則のみ（技術的には破れ得る） | Raphael検査で補完する事項 |
|---|---|---|---|
| requirements-designer | Write/Edit/Bash不許可＝実装・書き込み不能。読み取り専用（Read/Grep/Globのみ） | 曖昧点を推測で確定しないこと、実装方針を断定しないこと | 出力に実装コードが混入していないか、未確定事項が正しく検出されているか |
| implementer | Read/Write/Edit/Grep/Glob/Bash許可。**Bash経由のgit push・外部送信は技術的に禁止されていない** | git push禁止、PR作成禁止、要件外の変更禁止、外部送信禁止 | 差分内容が要件範囲内か、`git log`にpush等の禁止操作がないか、自己検証結果の妥当性 |
| tester-evaluator | Write/Edit不許可＝実装ファイルの修正不能。Read/Grep/Glob/Bash（テスト実行用）許可 | 証拠なし合格判定の禁止、自己申告への非依存 | 提示された証拠（実行ログ）が実在し判定と整合しているか |

**重要な誠実性の明記**: implementerとtester-evaluatorに付与したBashは、宣言どおりの用途（テスト・構文確認）に限定することを技術的に保証しない。これは今回のパイロットの既知の限界であり、PreToolUseフック等による強化は`agents/implementer.md`・`agents/tester-evaluator.md`の「Open questions」に将来の再検討事項として記録した。今回はRaphael（本セッション）がgit push/PR作成を自ら行い、実装・検証エージェントには行わせない運用で実質的リスクを抑える。

**追記（run-007/run-008で実地検証済み）**: requirements-designerのWrite/Edit/Bash不許可、およびtester-evaluatorのWrite/Edit不許可は、当初は`tools:`frontmatterの仕様に基づく設計上の主張だったが、本物のサブエージェント（`subagent_type`経由の直接呼び出し）に対してWrite/Editの呼び出しを意図的に試行させたところ、いずれも関数定義自体が提示されておらず呼び出し不能（tester-evaluatorのEdit試行では`Error: No such tool available: Edit`という明示的なランタイムエラー）であることを確認した。詳細は`evaluations/three-agent-pilot/RUN_LOG.md`の「技術的強制の再検証」を参照。

## 共通依頼書（ブリーフ）様式

Raphaelが各エージェントを起動する際、以下を含む依頼書を渡す。

```markdown
## 依頼書
- 実行ID:
- 宛先エージェント:
- 日時:
- 目的:
- 背景・制約:
- 入力（要件書／実装差分など、前段の成果物）:
- 期待する出力形式:
- 対象外:
- 完了条件:
```

## 受け渡し形式（ハンドオフ）

`RAPHAEL_HANDOFF_PROTOCOL.md`の簡略版を用いる。

```markdown
## ハンドオフ
- 送信エージェント:
- 受信エージェント（通常はRaphael）:
- 実行ID:
- 出力本体:
- 自己点検結果:
- 未確定事項／未解決事項:
- 情報不足検出の有無:
- Raphaelの検査結果（承認／差し戻し／隆之介確認要）:
- 次のアクション:
```

## 実行記録・テスト記録の構造

既存のRaphael本体向け評価様式（`evaluations/raphael/TEMPLATE.md`, `RAPHAEL_TEST_LOG.md`）とは混在させず、専用の軽量構造を新設する。

- `evaluations/three-agent-pilot/RUN_LOG.md`: 実行ID一覧表（日時・担当・入力概要・状態・合否）
- `evaluations/three-agent-pilot/UNIT_TESTS.md`: 単体テストの詳細記録
- `evaluations/three-agent-pilot/BOUNDARY_TESTS.md`: 境界テストの詳細記録
- `evaluations/three-agent-pilot/EVALUATION.md`: フェーズ5評価結果とユーザー評価欄（ストレッチ到達時のみ）

各実行記録には最低限、日時／担当エージェント／実際の入力／期待結果／実際の出力／使用ツール／変更ファイル／状態／合否／境界違反有無／情報不足の検出結果／差し戻し先／修正内容／再実行元の実行IDを記録する。初回失敗は記録から消さず、原因・修正・再実行の時系列を残す。

## ライフサイクル

3体とも本日は`status: sandbox`から開始する。単体・境界テストに合格した時点で`pilot`へ移行できる（`AGENT_STANDARD.md` §5）。`active`への正式採用（mainマージ・恒久運用化）は別途隆之介の承認を要する。

## 今後の要件改訂候補（フェーズ4 run-011より）

「3体間ハンドオフ契約チェッカー」（`pilot_sandbox/handoff_contract_checker/`, 要件書v3.1）の独立評価（run-011）でtester-evaluatorが発見し、隆之介が「現行実装は要件書v3.1に適合しており不具合ではない。ただし次回の要件改訂候補として記録する」と判断した事項。

- 現状、`REQ-B3`の`AC_NOT_ADDRESSED`判定は`addressed_acceptance_criteria[].id`が配列に存在するかどうかのみを見ており、`status`の値（`implemented`/`partially_implemented`/`not_implemented`）を判定に使っていない。そのため`status: "not_implemented"`のエントリがあっても、IDさえ存在すれば「対応済み」とみなされ、`AC_NOT_ADDRESSED`は発火しない
- 将来、ID存在だけでなく`status`値も判定対象とするかどうかは隆之介が決定する
- この変更を行う場合は、実装を先に変えず、要件書・チェック仕様・受入条件を先に改訂して承認を得ること（`AGENT_STANDARD.md`が定めるRaphael/requirements-designerの通常の意思決定順序どおり）

## 汎用コアとの関係

`v1_core/`・`software_domain/`は本パイロットのために変更しない。`.claude/agents/*.md`はClaude Codeのサブエージェント機構であり、`v1_core.orchestrator.Orchestrator.run`が要求するCallable群（understand/plan/select/execute/verify）には接続されていない別レイヤーである。将来、この3体をPython実行ループへ正式統合する場合は、その時点で改めて設計変更として提示する。
