---
name: md-render
description: Use when asked to render, preview, or view a markdown file in the browser. Triggers on "render markdown", "preview this", "show me this document", "open in browser".
---

# Markdown Renderer

Render markdown files as beautiful dark-mode HTML and open them in the browser. Designed for viewing agent-generated documents (design docs, plans, reports).

## Quick Reference

| Situation | Action |
|-----------|--------|
| User asks to render/preview markdown | Run `md-render <file>` |
| User wants HTML output saved | Run `md-render <file> -o output.html` |
| User wants to customize styling | Edit `~/.config/agent-skills/md-render/config.json` |
| User asks to pipe markdown | `echo "# Title" \| md-render -` |

## CLI Reference

| Command | Description |
|---------|-------------|
| `md-render file.md` | Render and open in browser |
| `md-render - < file.md` | Render from stdin |
| `md-render file.md -o out.html` | Save HTML to file |
| `md-render file.md --no-open` | Generate HTML without opening browser |
| `md-render -c path.json file.md` | Use alternate config |
| `md-render --help` | Show usage |

**Exit codes:** 0 = success, 1 = error

## Rendering Features

- Dark-mode aesthetic with configurable colors, fonts, and sizing
- Collapsible table of contents (inline and slide-out panel)
- Syntax-highlighted code blocks with copy-to-clipboard button
- Copy full markdown source button (top-right)
- Clickable heading anchors (hover to reveal)
- Mermaid diagram rendering (flowcharts, sequence diagrams, state diagrams, pie charts)
- Task list checkboxes, footnotes, ==highlights==, sub~script~/super^script^
- Emoji shortcodes (:rocket: :white_check_mark:)
- Custom attributes via `{#id .class}`
- Responsive layout
- Self-contained HTML (mermaid uses CDN when enabled)

## Configuration

Config location: `~/.config/agent-skills/md-render/config.json`

Created automatically on first run from defaults. Edit to customize:
- **theme** — colors, fonts, sizing, max-width
- **features** — toggle toc, syntax highlighting, heading anchors, mermaid, browser open
