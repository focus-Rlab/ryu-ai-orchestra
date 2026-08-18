# Cursor Raphael 強制実行

## 目的

文章として読ませるだけだった過去経験を、Cursorでの実行条件へ変換します。

## 自動で起きること

1. 隆之介がCursorへ依頼を送る
2. HookがSQLiteから関連経験を取得し、タスク契約を作る
3. Agentが最初にツールを使おうとした時、その実行を一度拒否する
4. 拒否理由として、適用すべき経験と完了に必要な証拠をAgentへ渡す
5. Agentは契約を反映して作業を再開する
6. 証拠不足のまま終わろうとすると、stop Hookが続きを自動送信する

## 強制力

- Prompt Hookを通っていないツール実行は拒否
- Hookが壊れた場合も、実行前Hookは `failClosed` で拒否
- 未登録の証拠名は保存拒否
- 実物証拠が揃うまで完了ループを最大3回継続

V0では証拠内容の真偽を全種類自動判定できません。テスト結果、GitHub状態、実ファイルなど
機械確認できる証拠から、順次検証器を追加します。

## Cursorでの利用

1. GitHubから最新版の `main` を取得する
2. Cursorで `ryu-ai-orchestra` フォルダを開く
3. Workspace Trustを許可する
4. 新しいAgentチャットで依頼する

`.cursor/hooks.json` と `.cursor/rules/raphael.mdc` は自動で読み込まれます。反映されない場合は
Cursorを一度再起動します。
