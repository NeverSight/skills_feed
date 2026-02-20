---
name: watchlist
description: ウォッチリストの管理。銘柄の追加・削除・一覧表示。
argument-hint: "[show|add|remove|list] [name] [symbols...]  例: show my-list, add my-list 7203.T AAPL"
allowed-tools: Bash(python3 *)
---

# ウォッチリスト管理スキル

$ARGUMENTS を解析し、以下のコマンドを実行してください。

```bash
python3 /Users/kikuchihiroyuki/stock-skills/.claude/skills/watchlist/scripts/manage_watchlist.py $ARGUMENTS
```

結果をそのまま表示してください。
