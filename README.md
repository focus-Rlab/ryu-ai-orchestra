# Ryu AI Orchestra

隆之介専用のAIオーケストラを、役割・権限・記憶・評価基準・安全基準として外部保存し、複数のAIから再利用できる形にするための基盤です。

## 現在地

- Version: 0.2.0-draft
- Status: Raphael Foundation Draft
- 最初の中核エージェント: Raphael
- 運用方式: 人間承認型オーケストレーション
- 作業ブランチ: `agent/raphael-foundation`

## 北極星

AIを活用してサービス・アプリ・事業を生み出し、独立して稼ぐ。最終的に、時間・場所・お金・関わる相手を自分で選べる自由を得る。

## 正本

- `VISION.md`: 長期ビジョン、価値観、判断原則
- `ROADMAP.md`: 実装順序、現在地、完了条件
- `USER.md`: 隆之介に関する共通判断情報
- `RECONSIDER.md`: 保留事項、再検討条件
- `GOVERNANCE.md`: 権限、承認、変更、安全管理
- `agents/raphael.md`: ラファエル初期版の正式仕様
- `SECURITY.md`: 外部アクセス、スキル、コード、成果物の安全基準

## 補助構成

- `AGENTS.md`: 全エージェント共通ルール
- `agents/`: 役割ごとの設計書
- `skills/`: 再利用可能な作業手順
- `memory/`: 隆之介の好みや組織全体の学習
- `projects/`: プロジェクト固有の仕様・判断・進捗
- `governance/`: 詳細な運用ルール
- `templates/`: 新規エージェントや振り返りの雛形

## 旧構想の扱い

既存のMeta Agent Builderは削除せず、将来のAgent Builder候補として保持する。初期中核はRaphaelとし、Raphaelが分析、統合、品質管理、進捗管理、エージェント設計・改善・統合・分解を担う。

## 次の段階

1. 正本草案の整合性確認
2. Raphael初期版の実装計画作成
3. 最低10件・約1か月の実運用評価設計
4. 隆之介の承認後にmainへ反映
