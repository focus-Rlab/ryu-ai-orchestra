# Repository Agent Instructions

このリポジトリで作業するAIエージェントは、最初に`README.md`と`STARTUP_CONTEXT.md`を読み、そこにある読込ルーターに従う。

## 必須ルール

0. `STARTUP_CONTEXT.md`を起動時必読として扱う。

1. `README.md`を唯一の入口として扱う。
2. 全作業で`GOVERNANCE.md`と`SECURITY.md`を適用する。
3. Raphaelとして作業する場合は`agents/raphael.md`を読む。
4. 計画、進捗、実装順序に関わる場合は`ROADMAP.md`を読む。
5. 重要な設計、権限、組織変更、正本変更では`MASTER_SPEC.md`と`SPEC_TRACEABILITY.md`を読む。
6. 既存決定を会話記憶だけで上書きしない。
7. mainへ直接変更しない。専用ブランチとDraft PRを使う。
8. 削除、mainマージ、本番反映、外部送信、公開、課金、権限変更は隆之介の承認後に行う。
9. 作業完了時は、読んだ正本、変更内容、未解決事項、承認が必要な事項を報告する。

詳細な使い方は`OPERATING_GUIDE.md`を参照する。