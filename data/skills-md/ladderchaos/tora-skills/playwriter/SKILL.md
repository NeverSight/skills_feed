---
name: playwriter
description: Browser automation via Playwriter MCP - works as a Chrome extension with full Playwright API access. Use for browser testing, web scraping, form filling, and any browser interaction.
mcp:
  playwriter:
    command: npx
    args: ["-y", "playwriter@latest"]
---

# Playwriter Browser Automation

Browser automation via Chrome extension with full Playwright API access.

## Prerequisites

1. Install Chrome extension: https://chromewebstore.google.com/detail/playwriter-mcp/jfeammnjpkecdekppnclgkkffahnhfhe
2. Click extension icon on tabs to control (turns green when connected)

## Usage

Use the `execute` tool to run Playwright code:

```javascript
// Navigate
await page.goto('http://localhost:5173')

// Screenshot with accessibility labels
await screenshotWithAccessibilityLabels({ page })

// Click using aria-ref
await page.locator('aria-ref=e5').click()

// Fill form
await page.fill('input[name="email"]', 'test@example.com')
```

## Key Features

- Single `execute` tool with full Playwright API
- Less context window usage than traditional browser MCPs
- Works with your existing Chrome extensions
- Can bypass automation detection
