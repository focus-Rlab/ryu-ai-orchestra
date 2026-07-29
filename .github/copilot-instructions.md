# GitHub Copilot Repository Instructions

この自動入口を受け取ったら、最初に`STARTUP_CONTEXT.md`を読み、読了を確認してから`README.md`の読込ルーターに従う。読了前に分析・提案・変更を開始しない。

## 必須

- `STARTUP_CONTEXT.md`を第一読込対象とし、`README.md`を第二読込対象として扱う。

- 全作業で`GOVERNANCE.md`と`SECURITY.md`を適用する。
- Raphaelとして作業する場合は`agents/raphael.md`を読む。
- 重要な設計、組織、権限、正本変更では`MASTER_SPEC.md`と`SPEC_TRACEABILITY.md`を確認する。
- mainへ直接変更しない。専用ブランチとDraft PRを使う。
- 削除、mainマージ、本番反映、外部送信、公開、課金、権限変更は隆之介の承認後に行う。
- 既存決定を確認せず、会話や推測だけで仕様を上書きしない。
- 完了時は、変更内容、参照した正本、テスト結果、未解決事項、承認待ち事項を報告する。

詳細は`OPERATING_GUIDE.md`を参照する。