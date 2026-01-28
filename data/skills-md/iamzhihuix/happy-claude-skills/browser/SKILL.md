---
name: browser
description: Minimal Chrome DevTools Protocol tools for browser automation and scraping. Use when you need to start Chrome, navigate pages, execute JavaScript, take screenshots, or interactively pick DOM elements. Triggers include "browse website", "scrape page", "take screenshot", "automate browser", "extract DOM", "web scraping".
---

# Browser Tools

Minimal CDP tools for collaborative site exploration and scraping.

**Credits**: Based on [Mario Zechner](https://mariozechner.at)'s article [What if you don't need MCP?](https://mariozechner.at/posts/2025-11-02-what-if-you-dont-need-mcp/), adapted from [Factory.ai](https://docs.factory.ai/guides/skills/browser).

## Setup

Before first use, install dependencies:

```bash
npm install --prefix skills/browser
```

## Start Chrome

```bash
./skills/browser/scripts/start.js              # Fresh profile
./skills/browser/scripts/start.js --profile    # Copy your profile (cookies, logins)
```

Start Chrome on `:9222` with remote debugging.

## Navigate

```bash
./skills/browser/scripts/nav.js https://example.com
./skills/browser/scripts/nav.js https://example.com --new
```

Navigate current tab or open new tab.

## Evaluate JavaScript

```bash
./skills/browser/scripts/eval.js 'document.title'
./skills/browser/scripts/eval.js 'document.querySelectorAll("a").length'
```

Execute JavaScript in active tab (async context).

**IMPORTANT**: The code must be a single expression or use IIFE for multiple statements:

- Single expression: `'document.title'`
- Multiple statements: `'(() => { const x = 1; return x + 1; })()'`
- Avoid newlines in the code string - keep it on one line

## Screenshot

```bash
./skills/browser/scripts/screenshot.js
```

Screenshot current viewport, returns temp file path.

## Pick Elements

```bash
./skills/browser/scripts/pick.js "Click the submit button"
```

Interactive element picker. Click to select, Cmd/Ctrl+Click for multi-select, Enter to finish.

## Workflow

1. **Start Chrome** with `start.js --profile` to mirror your authenticated state.
2. **Drive navigation** via `nav.js https://target.app` or open secondary tabs with `--new`.
3. **Inspect the DOM** using `eval.js` for quick counts, attribute checks, or extracting JSON payloads.
4. **Capture artifacts** with `screenshot.js` for visual proof or `pick.js` when you need precise selectors or text snapshots.

## Usage Notes

- Start Chrome first before using other tools
- The `--profile` flag syncs your actual Chrome profile so you're logged in everywhere
- JavaScript evaluation runs in an async context in the page
- Pick tool allows you to visually select DOM elements by clicking on them
