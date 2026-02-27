---
name: web-browser
description: "Use when tasks need real-browser web automation in Chrome/Chromium via CDP: open or navigate URLs, click/type/select in forms, run page JS, wait for selectors, scrape structured content, capture screenshots, validate UI flows, or run measured web-browser latency checks (`bench:eval`, `bench:all`) for perf regressions."
---

# Web Browser

## When to use
- Navigate or interact with live websites.
- Click buttons, fill forms, or extract page content.
- Evaluate JavaScript in a real browser context.
- Capture screenshots for debugging or review.
- UI validation and smoke testing in a real browser.
- Measure and gate latency regressions in web-browser tools with the local benchmark scripts.

## Requirements
- Run commands from `codex/skills/web-browser/` (so `./tools/*.js` resolves).
- Node.js (ESM + top-level `await`) and repo deps installed (notably `puppeteer-core`).
- Chrome/Chromium installed, or set `CODEX_CHROME_PATH`.

## Quick start
```bash
# Start Chrome with CDP on :9222
./tools/start.js

# Safer (recommended on your laptop): avoid killing an existing Chrome session
./tools/start.js --no-kill

# Open a deterministic tab, then operate on it
./tools/nav.js https://example.com --new
./tools/eval.js 'document.title'
./tools/screenshot.js
```

Loop: take small steps → inspect state (`eval.js` / `screenshot.js`) → repeat.

## Performance pass ($lift)
Use this when optimizing or validating web-browser tool latency.

```bash
./tools/start.js --no-kill
./tools/nav.js https://example.com --new

cd tools
npm run -s bench:all -- --warmup 5 --samples 30 --screenshot-samples 20
```

For stricter CI-style gating, add p95 budgets:

```bash
cd tools
npm run -s bench:all -- \
  --warmup 5 \
  --samples 30 \
  --screenshot-samples 20 \
  --budget-nav-p95-ms 310 \
  --budget-eval-p95-ms 220 \
  --budget-screenshot-p95-ms 320 \
  --budget-start-p95-ms 140
```

## Configuration
- **Flags**
  - `start.js`: `--port`, `--user-data-dir`, `--chrome-path`, `--profile`, `--no-kill`
  - `nav.js` / `eval.js` / `screenshot.js` / `pick.js`: `--port`, `--browser-url`
- **Environment**
  - `CODEX_BROWSER_URL`: CDP URL (used when no CLI `--port`/`--browser-url`)
  - `CODEX_BROWSER_PORT` (alias: `CODEX_CDP_PORT`): CDP port for localhost
  - `CODEX_BROWSER_USER_DATA_DIR`: Chrome user data dir (used by `start.js`)
  - `CODEX_CHROME_PATH` (aliases: `CHROME_PATH`, `PUPPETEER_EXECUTABLE_PATH`): Chrome/Chromium executable

## Targeting (active tab)
All tools operate on the “active tab”, defined as the last page returned by `puppeteer.pages()` (roughly: the most recently opened tab).
- Prefer `./tools/nav.js <url> --new` when you want deterministic targeting.
- If actions hit the “wrong” tab, close extra tabs or open a fresh one.

## Common commands
```bash
# See all options (safe; does not start/kill Chrome)
./tools/start.js --help

# Use a non-default port
./tools/start.js --port 9223 --no-kill
./tools/nav.js --port 9223 https://example.com --new

# Or configure once via env
export CODEX_BROWSER_URL=http://localhost:9223
./tools/eval.js 'document.title'

# Wait for a selector (polling with timeout; good for SPAs)
./tools/eval.js '(async () => { for (let i = 0; i < 50; i++) { const el = document.querySelector("button[type=submit]"); if (el) return true; await new Promise(r => setTimeout(r, 100)); } return false; })()'

# Screenshot current viewport
# Prints a PNG filepath in your system temp dir
./tools/screenshot.js

# Pick elements interactively
# Prints tag/id/class/text/html/parents for one element (or many via Cmd/Ctrl+click)
./tools/pick.js "Click the submit button"
```

Tip: use `pick.js` to inspect attributes/text, then craft a selector for `eval.js`.

## Recipes
```bash
# Scrape structured data (return an array of objects for readable output)
./tools/eval.js 'Array.from(document.querySelectorAll("a"), a => ({ href: a.href, text: a.textContent?.trim() }))'
```

- **Login flows**
  - Dedicated automation profile: run `./tools/start.js`, log in once, then reuse the persisted profile in your user-data-dir (default: `~/.cache/scraping`).
  - Default-profile bootstrap: run `./tools/start.js --profile` when you truly need existing cookies/logins.

## Security & privacy
- `./tools/start.js --profile` uses `rsync -a --delete` to copy your default Chrome profile into your user-data-dir (cookies/sessions/PII).
- Treat your user-data-dir (default: `~/.cache/scraping`) as sensitive; avoid on shared machines and delete it when done if needed.

## Troubleshooting
- `✗ Failed to connect to Chrome via CDP`: run `./tools/start.js` (or set `CODEX_BROWSER_URL`/`--port` to match your Chrome).
- `✗ No active tab found`: open a page first (e.g., `./tools/nav.js https://example.com --new`).
- Port `9222` is busy: pick a new one (`./tools/start.js --port 9223`).
- Selector flakiness: use the polling pattern above; SPAs often need a wait after `domcontentloaded`.
- Chrome path not found: set `CODEX_CHROME_PATH` or pass `--chrome-path`.

## Pitfalls
- `./tools/start.js` defaults to killing Chrome processes (use `--no-kill` to avoid this).
- Use single quotes around JS to avoid shell-escaping issues.

## Prove $lift uses Zig
When you need objective proof that the local `$lift` tooling is Zig-based:

```bash
bench_stats --help 2>&1 | sed -n '1,6p'
perf_report --help 2>&1 | sed -n '1,6p'
brew cat tkersey/tap/lift | rg -n 'depends_on \"zig\" => :build|build-exe|bench_stats.zig|perf_report.zig'
```

## References
- `codex/skills/web-browser/tools/start.js`
- `codex/skills/web-browser/tools/nav.js`
- `codex/skills/web-browser/tools/eval.js`
- `codex/skills/web-browser/tools/screenshot.js`
- `codex/skills/web-browser/tools/pick.js`
- `codex/skills/web-browser/tools/bench-eval.js`
- `codex/skills/web-browser/tools/bench-all.js`
