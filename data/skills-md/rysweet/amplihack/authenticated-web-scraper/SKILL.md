---
name: authenticated-web-scraper
description: Scrape authenticated websites from WSL2 using Edge CDP. Launches headed Edge for user auth, then headless scraping via Chrome DevTools Protocol. Use when mirroring internal wikis, docs sites, or any site requiring 2FA/SSO login.
version: 1.0.0
---

# Authenticated Web Scraper

## Purpose

Scrapes content from websites that require authentication (2FA, SSO, corporate login) by leveraging the user's Windows Edge browser via Chrome DevTools Protocol (CDP). Designed for WSL2 environments where Playwright/Puppeteer can't directly reach Windows browser ports.

## When to Use

- Mirroring internal documentation sites behind corporate auth
- Scraping content from sites requiring 2FA/SSO that can't be automated
- Extracting structured content (text, HTML, links) from authenticated web pages
- Crawling site navigation trees and following links to a configurable depth

## Architecture

```
WSL2                          Windows
┌─────────────────┐           ┌──────────────────────┐
│ Claude Code     │           │ Edge Browser          │
│                 │  kill     │ (user's profile)      │
│ 1. Kill Edge ───┼──────────>│                       │
│                 │  launch   │                       │
│ 2. Launch Edge ─┼──────────>│ --remote-debug:9222   │
│                 │           │ --debug-addr:0.0.0.0  │
│ [User auths     │           │                       │
│  in browser]    │           │ CDP WebSocket on :9222│
│                 │  cmd.exe  │                       │
│ 3. Run scraper ─┼──────────>│ node scraper.mjs      │
│                 │           │ connects localhost:9222│
│ 4. Read output <┼───────────│ writes to C:\Temp\... │
└─────────────────┘           └──────────────────────┘
```

**Key insight**: WSL2 cannot reach Windows `localhost:9222` directly. The scraper script must run on the **Windows side** via `cmd.exe /c "node script.mjs"`.

## Quick Start

When a user asks to scrape an authenticated website:

1. Kill existing Edge processes and relaunch with debug flags
2. User authenticates in the headed browser
3. Copy scraper script to Windows temp and run via `cmd.exe`
4. Script connects to CDP, navigates pages, extracts content
5. Read results from shared filesystem (`/mnt/c/Temp/...`)

## Core Workflow

### Phase 0: Prerequisites

- Node.js must be installed on Windows (`cmd.exe /c "where node"`)
- The `ws` npm package on Windows side (`cmd.exe /c "cd C:\Temp && npm install ws"`)
- Edge browser installed (check `/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe`)

### Phase 1: Launch Edge with Remote Debugging

```javascript
import { execSync, spawn } from "child_process";

// CRITICAL: Kill ALL Edge processes first, otherwise debug flags are ignored
execSync('cmd.exe /c "taskkill /F /IM msedge.exe /T"');
await sleep(3000);

const EDGE = "/mnt/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe";
spawn(
  EDGE,
  [
    "--remote-debugging-port=9222",
    "--remote-debugging-address=0.0.0.0",
    "--remote-allow-origins=*",
    targetUrl,
  ],
  { detached: true, stdio: "ignore" }
).unref();
```

### Phase 2: Verify CDP and User Auth

```bash
# Verify CDP is running (must query from Windows side)
powershell.exe -Command "Invoke-RestMethod -Uri http://localhost:9222/json/version"
```

Tell user to authenticate, then confirm they can see content.

### Phase 3: Scrape via CDP

Write a Node.js script that:

1. Queries `http://localhost:9222/json/list` for open pages
2. Connects to the target page via WebSocket (`ws` package)
3. Uses `Runtime.evaluate` to extract DOM content
4. Uses `Page.navigate` + `Page.enable` for crawling
5. Saves `.txt` (clean text), `.html` (full), `_links.json` per page

Run on Windows side:

```bash
cp script.mjs /mnt/c/Temp/scraper.mjs
cmd.exe /c "cd C:\Temp && node scraper.mjs C:\Temp\output" 2>&1
```

### Phase 4: Crawl Navigation

1. Extract sidebar/nav links from the initial page
2. Filter to same-domain pages (skip anchor links)
3. Visit each nav page, extract content + links
4. Follow discovered links one level deep (deduplicating)
5. Write summary JSON with page inventory

## CDP Command Reference

```javascript
// Navigate to a page
await cdpSend(ws, "Page.navigate", { url });

// Extract text content
await cdpSend(ws, "Runtime.evaluate", {
  expression: 'document.querySelector("main").innerText',
  returnByValue: true,
});

// Extract links as JSON
await cdpSend(ws, "Runtime.evaluate", {
  expression:
    'JSON.stringify([...document.querySelectorAll("a[href]")].map(a => ({href: a.href, text: a.textContent.trim()})))',
  returnByValue: true,
});

// Get full HTML
await cdpSend(ws, "Runtime.evaluate", {
  expression: "document.documentElement.outerHTML",
  returnByValue: true,
});
```

## Critical Details

- **Must kill Edge first**: If Edge is already running, new instances join the existing process and ignore `--remote-debugging-port`
- **WSL2 networking**: WSL2 has its own network stack; `127.0.0.1` in WSL does NOT reach Windows. Scripts must run on Windows via `cmd.exe`
- **Respectful crawling**: Add 2-second delays between page loads
- **Auth persistence**: Edge uses the user's default profile with saved sessions
- **Output path**: Use Windows paths (`C:\Temp\...`) in scripts, read via `/mnt/c/Temp/...` from WSL

## Integration Points

- Works with any documentation site behind corporate auth (SSO, SAML, FIDO2, etc.)
- Output can be fed to other skills for analysis, summarization, or knowledge base building
- Pairs well with `investigation-workflow` and `knowledge-builder` skills
