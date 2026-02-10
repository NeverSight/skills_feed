---
name: vibe-check
description: Browser automation for AI agents. Use when the user needs to navigate websites, read page content, fill forms, click elements, take screenshots, or manage browser tabs.
---

# Vibium Browser Automation — CLI Reference

The `vibe-check` CLI automates Chrome via the command line. The browser auto-launches on first use (daemon mode keeps it running between commands).

```
vibe-check navigate <url> → vibe-check text → vibe-check screenshot -o shot.png
```

## Commands

### Navigation
- `vibe-check navigate <url>` — go to a page
- `vibe-check url` — print current URL
- `vibe-check title` — print page title

### Reading Content
- `vibe-check text` — get all page text
- `vibe-check text "<selector>"` — get text of a specific element
- `vibe-check html` — get page HTML (use `--outer` for outerHTML)
- `vibe-check find "<selector>"` — element info (tag, text, bounding box)
- `vibe-check find-all "<selector>"` — all matching elements (`--limit N`)
- `vibe-check eval "<js>"` — run JavaScript and print result
- `vibe-check screenshot -o file.png` — capture screenshot

### Interaction
- `vibe-check click "<selector>"` — click an element
- `vibe-check type "<selector>" "<text>"` — type into an input
- `vibe-check hover "<selector>"` — hover over an element
- `vibe-check scroll [direction]` — scroll page (`--amount N`, `--selector`)
- `vibe-check keys "<combo>"` — press keys (Enter, Control+a, Shift+Tab)
- `vibe-check select "<selector>" "<value>"` — pick a dropdown option

### Waiting
- `vibe-check wait "<selector>"` — wait for element (`--state visible|hidden|attached`, `--timeout ms`)

### Tabs
- `vibe-check tabs` — list open tabs
- `vibe-check tab-new [url]` — open new tab
- `vibe-check tab-switch <index|url>` — switch tab
- `vibe-check tab-close [index]` — close tab

### Daemon
- `vibe-check daemon start` — start background browser
- `vibe-check daemon status` — check if running
- `vibe-check daemon stop` — stop daemon

## Global Flags

| Flag | Description |
|------|-------------|
| `--headless` | Hide browser window |
| `--json` | Output as JSON |
| `--oneshot` | One-shot mode (no daemon) |
| `-v, --verbose` | Debug logging |
| `--wait-open N` | Wait N seconds after navigation |
| `--wait-close N` | Keep browser open N seconds before closing |

## Daemon vs Oneshot

By default, commands connect to a **daemon** — a background process that keeps the browser alive between commands. This is fast and lets you chain commands against the same page.

Use `--oneshot` (or `VIBIUM_ONESHOT=1`) to launch a fresh browser for each command, then tear it down. Useful for CI or one-off scripts.

## Common Patterns

**Read a page:**
```sh
vibe-check navigate https://example.com
vibe-check text
```

**Fill a form:**
```sh
vibe-check navigate https://example.com/login
vibe-check type "input[name=email]" "user@example.com"
vibe-check type "input[name=password]" "secret"
vibe-check click "button[type=submit]"
```

**Extract structured data:**
```sh
vibe-check navigate https://example.com
vibe-check eval "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href))"
```

**Multi-tab workflow:**
```sh
vibe-check tab-new https://docs.example.com
vibe-check text "h1"
vibe-check tab-switch 0
```

## Tips

- All click/type/hover actions auto-wait for the element to be actionable
- Use `vibe-check find` to inspect an element before interacting
- Use `vibe-check text "<selector>"` to read specific sections
- `vibe-check eval` is the escape hatch for complex DOM queries
- Screenshots save to the current directory by default (`-o` to change)
