# Next Session Prompt

Copy and paste the block below into a new session.

```text
GitHubの`focus-Rlab/ryu-ai-orchestra`を開き、`agent/v1-week1-general-core`を作業ブランチとして扱ってください。

最初にSTARTUP_CONTEXT.mdを読み、読了を確認してからREADME.md、PROJECT_HANDOFF.md、GOVERNANCE.md、SECURITY.md、ROADMAP.md、STAGE2_DECISION_LOG.md、AGENT_STANDARD.md、MASTER_SPEC.md、SPEC_TRACEABILITY.md、INCIDENT_LOG.md、docs/CANONICAL_AUDIT_2026-07-29.mdを確認してください。

現在はV1 Week 1「汎用コア最小実装」です。PR #10はmainへマージ済みで、Week 0のマージ後検証も完了しています。Issue #11に従い、分野非依存の実行ループ、予算、承認、検証、改善候補、ロールバックを実装・検証してください。

再質問しない確定事項:
- 最終目標は自己改善型・分野適応型の汎用オーケストレーターRaphael
- アプリ開発は最初の検証領域であり最終目的ではない
- V1は汎用コア、ドメインパック、ツールコネクタ、分野別評価パックを分離
- 週14時間、初月約56時間、API上限10,000円
- 7,000円警告、9,000円高性能モデル制限、10,000円自動停止
- 最初の案件はRaphael自身のコード・設計改善、その後に小規模新規アプリ
- 正式承認チャネルは現段階ではChatGPTのみ
- mainマージは隆之介が行う

次に行うこと:
1. Issue #11とWeek 1の完了条件を確認する。
2. `v1_core/`と`tests/test_v1_core.py`を確認し、模擬案件の状態遷移・承認・予算・ロールバックを検証する。
3. 分野固有ロジックがコアへ混入していないか監査する。
4. 未承認の評価基準を勝手に承認済みにしない。
5. Draft PRで差分、テスト、残存リスクを隆之介へ報告する。
6. mainへのマージは行わない。
```
