---
name: playwriter
description: Controls Chrome browser via Playwright MCP for web automation, testing, screenshots, and scraping. Use when explicitly asked to "use playwriter".
---

# Playwriter

Browser automation via MCP. Requires Chrome extension installed and clicked on target tab.

## Tools

### execute
Run Playwright code with access to `page`, `context`, `state` (persistent), and utility functions.

```js
// Single-line format with semicolons
await page.goto('https://example.com', { waitUntil: 'domcontentloaded' });
```

### reset
Reset CDP connection when errors occur or pages show as `about:blank`.

## Core Patterns

### Check Page State (do this after actions)
```js
console.log('url:', page.url()); console.log(await accessibilitySnapshot({ page }).then(x => x.split('\n').slice(0, 30).join('\n')));
```

### Click Elements (use aria-ref from snapshot)
```js
await page.locator('aria-ref=e13').click();
```

### Fill Input
```js
await page.locator('input[name="email"]').fill('test@example.com');
```

### Screenshot
```js
await page.screenshot({ path: 'shot.png', scale: 'css' });
```

### Visual Screenshot with Labels
```js
await screenshotWithAccessibilityLabels({ page });
```

## Utility Functions

| Function | Purpose |
|----------|---------|
| `accessibilitySnapshot({ page, search? })` | Get structured text of interactive elements |
| `screenshotWithAccessibilityLabels({ page })` | Screenshot with Vimium-style element labels |
| `getCleanHTML({ locator })` | Get cleaned semantic HTML |
| `getLatestLogs({ page?, count?, search? })` | Retrieve browser console logs |
| `waitForPageLoad({ page })` | Smart load detection |
| `getCDPSession({ page })` | Send raw CDP commands |

## Rules

- **Multiple calls**: Break complex logic into separate execute calls
- **Never close**: Don't call `browser.close()` or `context.close()`
- **No bringToFront**: Never call unless user asks
- **Always verify**: Check page state after clicks/navigation
- **Persist data**: Use `state.myVar = value` across calls
