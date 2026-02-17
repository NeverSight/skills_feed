---
name: tool-x-article-publisher
description: 'Publish Markdown to X (Twitter) Articles as a draft (never auto-publish). Use when the user asks to publish/post an article to X Articles, convert Markdown to X Articles rich text, or mentions "X article", "publish to X", "post to Twitter articles". Converts Markdown → HTML, pastes rich text, and inserts images deterministically.'
---

# X Article Publisher

Publish Markdown content into X (Twitter) Articles as a **draft**, preserving formatting via rich text paste and deterministic image insertion.

## Hard Rules (Safety)

1. **Never auto-publish** (draft only; user publishes manually).
2. **User must be logged in** before automation starts.
3. **First image = cover image** (if any).

## Prerequisites

- Browser automation available (Playwright MCP or equivalent)
- X account can access Articles (Premium / Premium Plus)
- macOS recommended (clipboard helper uses Cocoa)
- Python 3.9+ with:
  - `pip install Pillow pyobjc-framework-Cocoa`

## Inputs / Outputs (Recommended)

Inputs (paths only):
- `article_md_path`: Markdown file to publish
- Optional: `run_dir` for artifacts (otherwise use `/tmp/`)

Outputs (recommended artifacts):
- `/tmp/x_article.json` (parsed structure)
- `/tmp/x_article.html` (HTML body for paste)
- Optional: `run_dir/evidence/x-article-draft.md` (what was done + links)

## Bundled Scripts

Installed path (typical):
- `~/.claude/skills/tool-x-article-publisher/scripts/parse_markdown.py`
- `~/.claude/skills/tool-x-article-publisher/scripts/copy_to_clipboard.py`

## Runbook (Step-by-step)

Follow: [`references/runbook.md`](references/runbook.md)
