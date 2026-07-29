# Next Session Prompt

Copy and paste the block below into a new session.

```text
GitHubの`focus-Rlab/ryu-ai-orchestra`を開き、`agent/roadmap-and-canonical-audit`を作業ブランチとして扱ってください。

最初にREADME.md、STARTUP_CONTEXT.md、PROJECT_HANDOFF.md、GOVERNANCE.md、SECURITY.md、ROADMAP.md、STAGE2_DECISION_LOG.md、AGENT_STANDARD.md、MASTER_SPEC.md、SPEC_TRACEABILITY.md、INCIDENT_LOG.md、docs/CANONICAL_AUDIT_2026-07-29.mdを確認してください。

現在はV1 Week 0「正本完全性回復と実行基盤確定」です。Stage 2とPR #9は完了済みですが、会話で確定したV1ロードマップ再編がmainの正本群へ伝播していなかったため、専用ブランチで横断監査・修正しています。

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
1. 監査報告の全項目が実ファイルと一致するか再検証する。
2. 古いPR、ブランチ、Stage、未決定表記が残っていないか検索する。
3. V1確定事項が完全版・分割正本・入口・引き継ぎ・対応表で意味一致するか確認する。
4. 未承認の評価基準を勝手に承認済みにしない。
5. Draft PRの最終差分と残存リスクを隆之介へ報告する。
6. mainへのマージは行わない。
```
