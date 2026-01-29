---
name: headed-fetcher
description: ボット対策で保護されたページをPlaywrightのheadedブラウザで取得します。WebFetchが403エラーを返す場合や、Cloudflareチャレンジが表示される場合に使用してください。
license: MIT
compatibility:
  - uv
  - playwright
metadata:
  version: 1.0.0
  author: drillan
---

# headed-fetcher

WebページをPlaywrightで取得し、Markdown形式に変換するClaude Codeスキル。

## When to Use

- `WebFetch`ツールが403エラーを返す場合
- Cloudflareなどのボット対策が表示される場合
- JavaScriptを実行しないとコンテンツが表示されないサイト

## Setup

```bash
./scripts/setup.sh
```

## Usage

```bash
# 基本的な使用方法
uv run scripts/fetch.py https://example.com

# ファイルに出力
uv run scripts/fetch.py https://example.com -o output.md

# 特定要素のみを抽出
uv run scripts/fetch.py https://example.com --selector "article"

# ボット対策サイト用（headedモード）
uv run scripts/fetch.py https://protected-site.com --headed
```

## Claude Code Integration

スキルがインストールされたディレクトリから実行する場合は、`cd`ではなく`uv run --directory`オプションを使用してください：

```bash
# 推奨: --directory オプションを使用
uv run --directory $SKILL_DIR scripts/fetch.py <URL> [options]

# 例（スキルが ~/.claude/skills/headed-fetcher にインストールされている場合）
uv run --directory ~/.claude/skills/headed-fetcher scripts/fetch.py https://example.com --headed
```

**重要**: `cd $SKILL_DIR && uv run ...` の形式は使用しないでください。

## Options

| Option | Description |
|--------|-------------|
| `-o FILE` | ファイルに出力 |
| `--selector CSS` | CSSセレクタで要素を抽出 |
| `--headed` | headedモードで実行 |
| `--timeout N` | タイムアウト秒数（デフォルト: 30） |
| `--wait-until` | 待機条件（load/domcontentloaded/networkidle） |
| `--no-block-images` | 画像読み込みを有効化 |
| `--no-block-fonts` | フォント読み込みを有効化 |
| `--no-block-media` | メディア読み込みを有効化 |

## Output Format

```yaml
---
url: https://example.com
title: Page Title
fetched_at: 2026-01-24T12:34:56Z
---

# Page Heading

Content in Markdown...
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Network error (timeout, DNS, connection) |
| 2 | Selector not found |
| 3 | Markdown conversion error |

## Detailed Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for advanced usage and troubleshooting.
