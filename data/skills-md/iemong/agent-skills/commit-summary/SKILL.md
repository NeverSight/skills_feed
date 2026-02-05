---
name: commit-summary
description: |
  Gitコミットを日付ごとに集計してMarkdownテーブルで出力するスキル。
  機能: (1) 指定日のコミット一覧取得 (2) worktree含む全ブランチ対応 (3) PR番号の自動取得 (4) JST時刻でのテーブル出力
user-invocable: false
allowed-tools: Bash Read
---

# Commit Summary

日付を指定してGitコミットをMarkdownテーブル形式で集計する。

## 使い方

### 基本実行

```bash
# 今日のコミット
bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh

# 特定日のコミット
bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh 2026-01-16

# PR取得をスキップ（オフライン時）
bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh 2026-01-16 --no-pr

# 著者フィルタなし（全員分）
bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh 2026-01-16 --all-authors

# "その日のコミットログを全部"出す（pretty=fuller + --stat）
bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh 2026-01-16 --raw --all-authors

# refs/stash 等も含めて"全部"（WIP / index on ... が混ざる場合あり）
bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh 2026-01-16 --all-refs
```

### 出力例

```markdown
## 2026-01-16 のコミット一覧（frontend）

| 時間 | ブランチ/PR | コミット内容 |
|------|------------|-------------|
| 09:38 | #6535 | feat: ノートグリッドセクションを実装 |
| 10:12 | #6487 | refactor: フォローボタンをカスタムフックに分離 |
```

## 複数リポジトリの集計

複数リポジトリを一括集計する場合：

```bash
for repo in ~/Documents/works/frontend ~/Documents/works/note-ui; do
  cd "$repo" && bash ${CLAUDE_PLUGIN_ROOT}/skills/commit-summary/scripts/daily-commits.sh 2026-01-16
done
```

## 注意事項

- **worktree対応**: `git log --branches --remotes` により（stash等を除外しつつ）ブランチ由来のコミットを取得
- **PR番号**: `gh` CLIがインストールされている場合、PR一覧を1回だけ取得してPR番号を付与
- **時刻**: ローカルタイムゾーン（JST）で出力
- **依存**: Pythonは不要（`date` コマンドで翌日を計算）
