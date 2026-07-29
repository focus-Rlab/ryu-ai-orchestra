# Claude Project Instructions

Claude CodeおよびClaudeのリポジトリ作業では、`CLAUDE.md`の自動読込後、最初に`STARTUP_CONTEXT.md`を読み、読了を確認してから`README.md`の読込ルーターに従う。読了前に分析・提案・変更を開始しない。

@STARTUP_CONTEXT.md
@README.md
@GOVERNANCE.md
@SECURITY.md

## Claude固有ルール

- Raphaelとして作業する場合は`agents/raphael.md`を追加で読む。
- 重要な設計・組織・権限・正本変更では`MASTER_SPEC.md`と`SPEC_TRACEABILITY.md`を読む。
- コードや文書変更は専用ブランチで行い、Draft PRとして提出する。
- mainへの直接変更、削除、外部送信、公開、課金、本番反映は承認なしで行わない。
- 作業開始時に、今回読むファイルと作業範囲を短く示す。
- 作業終了時に、変更、根拠、テスト、未解決事項、承認待ちを報告する。

詳細は`OPERATING_GUIDE.md`を参照する。
