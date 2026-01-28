---
name: browser-max-automation
description: Browser automation using Playwright MCP for web testing, UI verification, and form automation. Use when navigating websites, clicking elements, filling forms, taking screenshots, or testing web applications. Supports iframe operations and complex JavaScript execution.
license: Complete terms in LICENSE.txt
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Browser Max Automation

Browser automation via Playwright MCP.

## When to use

- Automating browser-based workflows or QA checks
- Verifying UI states, DOM changes, or visual regressions
- Filling forms, clicking elements, or capturing screenshots

## Prerequisites

Configure `.vscode/mcp.json`:

```json
{
  "servers": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic-ai/mcp-playwright@latest", "--browser", "chrome"]
    }
  }
}
```

## Quick Reference

| Command                   | Purpose                               |
| ------------------------- | ------------------------------------- |
| `browser_navigate`        | Open URL                              |
| `browser_snapshot`        | Get element refs (accessibility tree) |
| `browser_click`           | Click element by ref                  |
| `browser_type`            | Input text                            |
| `browser_take_screenshot` | Capture screen                        |
| `browser_wait_for`        | Wait for text/time                    |
| `browser_run_code`        | Execute JavaScript                    |

## Basic Workflow

```
1. browser_navigate(url)
2. browser_snapshot → get ref
3. browser_click/type(ref)
4. browser_snapshot → verify
```

## Commands

### Navigate

```
mcp_playwright_browser_navigate
  url: "https://example.com"
```

### Snapshot

```
mcp_playwright_browser_snapshot
```

Returns accessibility tree with `ref` values for each element.

### Click

```
mcp_playwright_browser_click
  element: "Submit button"
  ref: "f2e123"
```

### Type

```
mcp_playwright_browser_type
  element: "Username"
  ref: "f2e456"
  text: "user@example.com"
  submit: true  # Press Enter
```

### Screenshot

```
mcp_playwright_browser_take_screenshot
  filename: "result.png"
```

### Wait

```
mcp_playwright_browser_wait_for
  text: "Loading complete"  # or
  time: 3
```

### Tabs

```
mcp_playwright_browser_tabs
  action: "list" | "new" | "close" | "select"
  index: 0
```

## Advanced

### iframe Operations

```javascript
async (page) => {
  const frame1 = page.locator('iframe[name="Content"]').contentFrame();
  const frame2 = frame1.locator('iframe[title="Player"]').contentFrame();
  await frame2.getByRole("radio", { name: "Option A" }).click({ force: true });
  return "Selected";
};
```

### force: true

Use when element is covered by another (e.g., SVG overlay):

```javascript
await element.click({ force: true });
```

### When browser_run_code is disabled

Use snapshot + click instead:

```
✅ browser_snapshot → get ref → browser_click(ref)
```

## Reference

| Type       | Use Case        | Selection |
| ---------- | --------------- | --------- |
| `radio`    | Single choice   | One only  |
| `checkbox` | Multiple choice | 0 to many |
