# Specification Traceability Matrix

Version: 0.6.1-draft
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
| Raphaelを通常セッションの主要対話窓口として標準起動 | MASTER_SPEC.md / STARTUP_CONTEXT.md / README.md / agents/raphael.md | AGENTS.md / CLAUDE.md / GEMINI.md / .github/copilot-instructions.md / .github/agents/raphael.md / NEXT_SESSION_PROMPT.md | 復元テスト対象 |
| エージェント正本のAI非依存化と環境別アダプター | MASTER_SPEC.md / README.md / agents/*.md | .claude/agents/*.md / .codex/agents/*.toml | アダプター契約テスト対象 |
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
| 文脈上明確な短文回答の解釈・不要な再質問防止・進行許可後の継続実行 | MASTER_SPEC.md / agents/raphael.md | 反映済み |
| 自発性と反対強度 | MASTER_SPEC.md / USER.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 調査・実験 | MASTER_SPEC.md / SECURITY.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 最小有能チーム原則 | MASTER_SPEC.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 複数AI意見統合 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 自己改善ループ | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| 根本原因分析・横断監査・一般化した再発防止 | MASTER_SPEC.md / README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / ROADMAP.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| 権限 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md | 反映済み |
| 隆之介の役割 | MASTER_SPEC.md / GOVERNANCE.md / USER.md | 反映済み |
| 成果物保存3段階 | MASTER_SPEC.md / GOVERNANCE.md / agents/raphael.md / RAPHAEL_INITIAL_DESIGN.md | 反映済み |
| PROJECT_STATE.jsonを変動する現在地の唯一の正本とする | MASTER_SPEC.md / README.md / GOVERNANCE.md / PROJECT_HANDOFF.md / ROADMAP.md / STARTUP_CONTEXT.md / scripts/check_project_state.py | 作業ブランチで実装・検証中 |
| 小変更のmain直接コミット例外 | MASTER_SPEC.md / README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 判断に迷う場合のブランチ優先 | MASTER_SPEC.md / README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 小変更の監査理由記録 | MASTER_SPEC.md / README.md / GOVERNANCE.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 忠実な引き継ぎ | MASTER_SPEC.md / PROJECT_HANDOFF.md / RAPHAEL_HANDOFF_PROTOCOL.md / OPERATING_GUIDE.md / agents/raphael.md | 反映済み |
| 報告・重大ミス・セキュリティ | MASTER_SPEC.md / GOVERNANCE.md / SECURITY.md / agents/raphael.md / RAPHAEL_TEST_PLAN.md | 反映済み |
| Stage 2は既存設計の監査と責任境界確定 | MASTER_SPEC.md / ROADMAP.md / README.md / PROJECT_HANDOFF.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| 旧Stage 2要求整理エージェントをStage 3へ移動 | MASTER_SPEC.md / ROADMAP.md / README.md / PROJECT_HANDOFF.md / STAGE1_STATUS.md / STAGE1_REVIEW_RESOLUTION.md | 反映済み |
| クロスモデル再現性と10件評価 | MASTER_SPEC.md / ROADMAP.md / RAPHAEL_TEST_PLAN.md / agents/raphael.md | 反映済み |
| V1汎用オーケストレーター方向 | STAGE2_DECISION_LOG.md V-01 / MASTER_SPEC.md §24 / VISION.md / ROADMAP.md / README.md / PROJECT_HANDOFF.md | 反映済み |
| V1資源・費用ゲート・初期案件 | STAGE2_DECISION_LOG.md V-02 / MASTER_SPEC.md §24 / ROADMAP.md / README.md / PROJECT_HANDOFF.md | 反映済み |
| V1承認境界・ChatGPT承認 | STAGE2_DECISION_LOG.md V-03〜V-04 / MASTER_SPEC.md §24 / GOVERNANCE.md / ROADMAP.md / README.md | 反映済み |
| V1 Week 2 Softwareドメインパックと自己改善案件 | MASTER_SPEC.md §24 / ROADMAP.md / README.md / PROJECT_HANDOFF.md / `software_domain` / docs/WEEK2_SOFTWARE_SELF_IMPROVEMENT.md | 作業ブランチで実装・検証中 |
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

過去の残存事項は再監査により次の状態へ更新した。

- PR #6およびPR #9はmainへマージ済み
- Stage 2のエージェント追加標準・監査・代表適用は完了済み
- 正式評価ログ保存先と採点重みはRAPHAEL_TEST_PLAN、RAPHAEL_TEST_LOG、evaluations/raphael/TEMPLATEに実装済み。ただしINCIDENT_LOGにより正式承認状態は未決定
- V1再編のROADMAP・README・PROJECT_HANDOFF・MASTER_SPEC・VISIONへの反映漏れを2026-07-29監査で検出し、このブランチで修正中

## 完全性ルール

- `MASTER_SPEC.md`に新しい重要項目を追加したら、本表にも追加する。
- 分割正本またはAI実行入口を変更したら、対応する行を再確認する。
- 「反映済み」とする前に、単語があるだけでなく意味と条件が保存されているか確認する。
- 完全版にしか存在しない運用必須事項を放置しない。
- 分割正本や実行入口にしか存在しない重要事項が見つかった場合、完全版への追記候補として明示する。
- 矛盾がある場合、独断で統合せず差分と推奨案を報告する。
- 現在地が変わった場合は`PROJECT_STATE.json`だけを更新し、参照文書への可変値再複製とmain不一致を自動検査する。
- 重要なStage完了前に、完全版、対応表、分割正本、実行入口、Stage文書群の同期を再確認する。


## 2026-07-29完全性監査の追加ゲート

- Stage・Week・目的・順序・成果物の変更では、会話決定→決定ログ→完全版→分割正本→README→PROJECT_HANDOFFの順に追跡する。
- 「現在地だけ更新」では同期完了としない。
- 反映済み判定はキーワードの存在ではなく、目的・範囲・条件・承認状態・順序の意味一致で行う。
- 未承認事項と実装済み事項を分離し、「実装済みだが正式承認未決定」を表現できるようにする。


## 起動時共通文脈・重要情報伝播

| 要求 | 完全版 | 分割正本 | AI入口・実行入口 | 検証 |
|---|---|---|---|---|
| 全AIの起動時必読セット | `MASTER_SPEC.md` | `STARTUP_CONTEXT.md`、`GOVERNANCE.md`、`OPERATING_GUIDE.md` | `README.md`、`AGENTS.md`、`CLAUDE.md`、`GEMINI.md`、`.github/copilot-instructions.md`、`.github/agents/raphael.md` | 全入口からREADME・STARTUP_CONTEXTへ到達 |
| 重要な長期記憶・決定・禁止・必須手順の保存判定 | `MASTER_SPEC.md` | `STARTUP_CONTEXT.md`、内容別の分割正本 | `README.md` | 分類、旧表現検索、復元テスト |
| 重要変更の全正本伝播 | `MASTER_SPEC.md` | `STARTUP_CONTEXT.md`、`GOVERNANCE.md`、`PROJECT_HANDOFF.md` | `OPERATING_GUIDE.md` | 完全版・分割正本・対応表・入口の意味照合 |
| ユーザー発言の批判的評価 | `MASTER_SPEC.md` | `USER.md`、`STARTUP_CONTEXT.md`、`GOVERNANCE.md` | 全AI入口→STARTUP_CONTEXT | 自動肯定・禁止表現・根拠説明のケーステスト |
| 一般・反復・重大ミス発生時の必須手順 | `MASTER_SPEC.md` | `GOVERNANCE.md`、`STARTUP_CONTEXT.md`、`INCIDENT_LOG.md` | `README.md`、`OPERATING_GUIDE.md` | 分類、根本原因、横断監査、一般化、成功/失敗、類似ケース再テスト、2回目の格上げ、代替経路確認 |
| 読了した規則の行動直前適用ゲート | `MASTER_SPEC.md` §12 | `GOVERNANCE.md` §9、`agents/raphael.md`、`RAPHAEL_TEST_PLAN.md` | `OPERATING_GUIDE.md`、`scripts/check_action_gate.py` | 完全計画の成功、規則欠落・架空委任・事故工程欠落の失敗、非事故類似ケース |

| 有料API・従量課金・課金可能・料金不明サービスの事前明示承認 | `MASTER_SPEC.md` §25 | `STARTUP_CONTEXT.md` §10、`GOVERNANCE.md`、`SECURITY.md`、`ROADMAP.md`、`PROJECT_HANDOFF.md` | 全AI入口→STARTUP_CONTEXT、README | 1円、課金可能0円、料金不明、予算超過承認のみ、正式5窓口のテスト |
| 隆之介向け説明・進捗報告の恒久ルール（IT初心者への配慮、専門用語・略称・独自名称の区別、報告順序） | `MASTER_SPEC.md` §27 | `agents/raphael.md`「隆之介向け説明・進捗報告のスタイル」、`USER.md`「説明への配慮」 | README「Raphaelとして作業」ルートから`agents/raphael.md`・`USER.md`へ到達 | 次回セッションでの復元テスト未実施（要フォローアップ）。3体パイロットのフェーズ5ユーザー評価（説明の分かりやすさ1/10）が確定根拠 |
| 規則全体の強制適用、成果物共有・受入、会話フィードバック自動分類 | `MASTER_SPEC.md` §28 | `GOVERNANCE.md` §9、`agents/raphael.md` | `scripts/check_action_gate.py` | 8分類欠落、未共有アプリの完了主張、未分類フィードバックを失敗させる単体テスト |
