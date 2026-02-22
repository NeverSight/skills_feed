---
name: commit-and-pr
description: 変更をコミットしてGitHub Pull Requestを作成する。「コミットしてPRを出して」「今の作業をコミットしてプルリクを作って」「変更をプッシュしてPR出して」などのリクエストに使用。ステージング・コミットメッセージ生成・ブランチ作成・プッシュ・PR作成を一連のワークフローで処理する。コミットメッセージおよびPR本文は日本語で書く。
---

# Commit and PR

git commit → push → PR 作成のワークフローを一括で実行する。

## ワークフロー

### 1. 現状確認

以下を並行実行：

```bash
git status          # 未追跡・変更ファイルを確認
git diff HEAD       # 全差分を確認
git log --oneline -5  # 最近のコミットスタイルを把握
git branch -r       # リモートブランチの存在確認
```

### 2. ブランチ戦略

- フィーチャーブランチ上（`main`/`master` 以外）: そのまま使用。
- `main`/`master` 上: 新しいブランチを作成。変更内容からブランチ名を導出（例: `feat/add-login`、`fix/null-pointer`）。

```bash
git checkout -b <branch-name>
```

### 3. ステージング

`git add -A` より特定ファイルの指定を優先。以下は絶対に含めない：
- `.env`、シークレット、認証情報
- 未追跡の大きなバイナリ
- `.gitignore` に記載済みのビルド成果物

```bash
git add <file1> <file2> ...
```

全変更ファイルが安全な場合は `git add -A` でも可。

### 4. コミット作成

全変更を分析し、簡潔なコミットメッセージを**日本語**で作成（1〜2文、命令形、**what ではなく why** に焦点）。heredoc で渡す：

```bash
git commit -m "$(cat <<'EOF'
<要約行>

<追加コンテキスト（任意）>

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
EOF
)"
```

pre-commit hook が失敗した場合: 問題を修正して再ステージし、**新しいコミット**を作成（`--amend` 禁止）。

### 5. プッシュ → PR 作成

```bash
git push -u origin <branch-name>
```

PR を作成（**本文は日本語**で記述）。改行が `\n` のままエスケープされないよう、必ず一時ファイル経由で渡す：

```bash
cat > /tmp/pr_body.md << 'EOF'
## 背景・動機
<なぜこの変更が必要だったかの文脈>

## 概要
- <変更点1>
- <変更点2>

## レビューのポイント
- <特に見てほしい箇所や懸念点>

## テスト手順
- [ ] <CIで自動確認できないもの、手動で確認が必要なものだけ記載>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF

gh pr create --title "<簡潔なタイトル（70字以内）>" --body-file /tmp/pr_body.md
```

`--body "..."` に直接文字列を渡すと `\n` がエスケープされたまま表示される場合があるため、`--body-file` を使うこと。

PR の URL をユーザーに返す。

## 安全ルール

- `main`/`master` へのforce pushは禁止。
- ユーザーが明示的に求めない限り `--no-verify` は使わない。
- プッシュ済みのコミットを amend しない。
- 共有・保護ブランチへのプッシュ前はユーザーに確認する。
- 変更がない場合（`git status` がクリーン）はコミットしない。
