# Ryu AI Orchestra

隆之介専用のAIエージェント組織を、役割・手順・記憶・評価基準として外部保存し、Claude、Codex、Geminiなど複数のAIから再利用するための基盤です。

## 現在の段階

- Version: 0.1.0
- Status: Foundation
- 最初の中核エージェント: Meta Agent Builder
- 運用方式: 人間承認型の手動オーケストレーション

## 基本原則

1. チャット履歴をエージェント本体にしない。
2. 現在有効なルールをMarkdownの正本として管理する。
3. AIは改善案を出すが、正本の変更は隆之介が承認する。
4. 役割、モデル、記憶、ツールを分離する。
5. 最初から完璧を目指さず、実運用の結果から更新する。

## ディレクトリ

- `AGENTS.md`: 全エージェント共通ルール
- `agents/`: 役割ごとの設計書
- `skills/`: 再利用可能な作業手順
- `memory/`: 隆之介の好みや組織全体の学習
- `projects/`: プロジェクト固有の仕様・判断・進捗
- `governance/`: 更新、承認、バージョン管理のルール
- `templates/`: 新規エージェントや振り返りの雛形

## 最初の使い方

1. `agents/meta-agent-builder/AGENT.md` をAIに読ませる。
2. 作りたいエージェントの目的を伝える。
3. Meta Agent Builderが作成した設計案を確認する。
4. 承認したファイルだけ `agents/` に追加する。
5. 実際に使い、`templates/RETROSPECTIVE.md` で振り返る。
6. 改善案をPull Requestまたは変更案として管理する。
