---
name: browser-automation
description: Control Chrome browser with AI using MCP protocol. Use when users want to automate browser tasks, take screenshots, fill forms, click elements, navigate pages, search browsing history, manage bookmarks, or perform any browser-based automation. Works with your existing Chrome browser and login sessions.
---

# Browser Automation (Chrome MCP Server)

Turn your Chrome browser into your intelligent assistant - Let AI take control of your browser.

## When to Use This Skill

Use this skill when the user:

- Wants to automate browser tasks (clicking, filling forms, navigating)
- Needs to take screenshots of web pages or elements
- Wants to extract content from web pages
- Asks to search browsing history or manage bookmarks
- Needs to monitor network requests
- Wants AI to interact with websites using their existing login sessions

## Installation

### Step 1: Install the Native Bridge

```bash
npm install -g mcp-chrome-bridger
# or
pnpm install -g mcp-chrome-bridger
mcp-chrome-bridger register
```

### Step 2: Install Chrome Extension

Download from [GitHub Releases](https://github.com/femto/mcp-chrome/releases):

1. Download `mcp-chrome-extension-vX.X.X.zip`
2. Open Chrome → `chrome://extensions/`
3. Enable "Developer mode"
4. Click "Load unpacked" and select the extracted folder
5. Click the extension icon → Click "Connect"

### Step 3: Configure MCP Client

Add to your MCP client configuration:

**Streamable HTTP (Recommended):**

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "type": "http",
      "url": "http://127.0.0.1:12306/mcp"
    }
  }
}
```

**STDIO (Alternative):**

```json
{
  "mcpServers": {
    "chrome-mcp-server": {
      "command": "npx",
      "args": ["mcp-chrome-bridger", "stdio"]
    }
  }
}
```

## Available Tools (20+)

### Browser Management

| Tool | Description |
|------|-------------|
| `get_windows_and_tabs` | List all browser windows and tabs |
| `chrome_navigate` | Navigate to URLs, control viewport |
| `chrome_switch_tab` | Switch active tab |
| `chrome_close_tabs` | Close specific tabs |
| `chrome_go_back_or_forward` | Browser history navigation |

### Screenshots

| Tool | Description |
|------|-------------|
| `chrome_screenshot` | Capture full page, viewport, or specific elements |

### Content Analysis

| Tool | Description |
|------|-------------|
| `chrome_get_web_content` | Extract HTML/text from pages |
| `chrome_get_interactive_elements` | Find clickable elements |
| `search_tabs_content` | AI-powered semantic search across tabs |
| `chrome_console` | Capture browser console output |

### Interaction

| Tool | Description |
|------|-------------|
| `chrome_click_element` | Click elements via CSS selector |
| `chrome_fill_or_select` | Fill forms and select options |
| `chrome_keyboard` | Simulate keyboard input |

### Data Management

| Tool | Description |
|------|-------------|
| `chrome_history` | Search browsing history |
| `chrome_bookmark_search` | Find bookmarks |
| `chrome_bookmark_add` | Add new bookmarks |
| `chrome_bookmark_delete` | Delete bookmarks |

### Network

| Tool | Description |
|------|-------------|
| `chrome_network_capture_start/stop` | Monitor network requests |
| `chrome_network_request` | Send HTTP requests with browser cookies |

## Example Usage

### Navigate and Screenshot

```
User: "Take a screenshot of github.com"

AI uses:
1. chrome_navigate(url: "https://github.com")
2. chrome_screenshot(fullPage: true)
```

### Fill a Form

```
User: "Login to my account on example.com"

AI uses:
1. chrome_navigate(url: "https://example.com/login")
2. chrome_fill_or_select(selector: "#email", value: "user@example.com")
3. chrome_fill_or_select(selector: "#password", value: "...")
4. chrome_click_element(selector: "button[type=submit]")
```

### Search History

```
User: "Find all pages I visited about React hooks last week"

AI uses:
1. chrome_history(text: "React hooks", startTime: "1 week ago")
```

### Extract Content

```
User: "What does this page say about pricing?"

AI uses:
1. chrome_get_web_content()
2. Analyzes the extracted content
```

## Advantages Over Playwright

| Feature | Playwright MCP | Chrome MCP Server |
|---------|---------------|-------------------|
| Browser Instance | New browser process | Your existing Chrome |
| Login Sessions | Need to re-login | Uses existing sessions |
| User Settings | Clean environment | Your bookmarks, extensions, settings |
| Startup Time | Slow (launch browser) | Instant (extension already loaded) |
| Resource Usage | Heavy | Lightweight |

## Multi-Client Support

Multiple AI clients can connect simultaneously:

- Claude Code
- Cursor
- Kiro
- Any MCP-compatible client

Each client gets its own session while sharing the same Chrome browser.

## Troubleshooting

### Extension Not Connecting

1. Check extension is enabled in `chrome://extensions/`
2. Click extension icon → Verify "Connected" status
3. Restart Chrome if needed

### Port Already in Use

The server automatically handles port conflicts. If issues persist:

```bash
lsof -i :12306
kill <PID>
```

## Resources

- GitHub: https://github.com/femto/mcp-chrome
- npm: https://www.npmjs.com/package/mcp-chrome-bridger
- Releases: https://github.com/femto/mcp-chrome/releases
