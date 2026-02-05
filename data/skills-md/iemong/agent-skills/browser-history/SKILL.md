---
name: browser-history
description: |
  Arcブラウザの履歴を取得してMarkdown形式で出力するスキル。
  使用タイミング: (1) 最近見たサイトを確認したい (2) 履歴から特定のURLを探したい
user-invocable: false
allowed-tools: Bash Read
---

# Browser History Skill

Arcブラウザの履歴をMarkdown形式で取得する。

## 使用方法

### 基本（直近100件）

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/browser-history/scripts/get_history.sh
```

### 件数指定

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/browser-history/scripts/get_history.sh 50
```

### 日付フィルター

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/browser-history/scripts/get_history.sh 100 2025-01-19
```

### プロファイル指定

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/browser-history/scripts/get_history.sh 100 "" "Profile 1"
```

### 日付＋プロファイル指定

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/browser-history/scripts/get_history.sh 100 2025-01-19 "Profile 1"
```

## 出力形式

Markdownテーブル形式で出力：

| 日時 | タイトル | URL |
|------|----------|-----|
| 2025-01-19 15:30 | Example Site | https://example.com |

## 注意事項

- Arcが起動中はDBがロックされるため、一時ファイルにコピーして読み取る
- last_visit_timeはWebKitタイムスタンプ（1601年からのマイクロ秒）
