---
name: fast-playwright
description: Fast, persistent, and token-optimized browser automation using Playwright. Supports navigation, clicking, typing, screenshots, batch execution, and more. Use when working with web pages, browser automation, or when the user mentions browsing, clicking, or web scraping.
---

# Fast Playwright

This skill provides a persistent, headless browser environment optimized for LLM agents.
It keeps the browser open between calls to enable fast interactions.

## Setup

Run the installation script once to set up dependencies and download browsers:
```bash
node scripts/install.js
```

## Usage

All tools are executed via `client.js`. Arguments must be valid JSON.

```bash
node scripts/client.js <tool_name> '<json_args>'
```

### Options

| Option | Description |
|--------|-------------|
| `--session <id>` | Use isolated browser session (for multi-agent) |
| `--headed` | Show browser window (default: headless) |
| `--sessions` | List active sessions |
| `--stop` | Stop the server |

### Multi-Agent Session Isolation

Each session gets its own isolated browser context (cookies, storage, page state):

```bash
# Agent A uses session "agent-a"
node scripts/client.js --session agent-a browser_navigate '{"url": "https://site-a.com"}'

# Agent B uses session "agent-b" (completely isolated)
node scripts/client.js --session agent-b browser_navigate '{"url": "https://site-b.com"}'

# List active sessions
node scripts/client.js --sessions

# Without --session, uses shared "default" session
node scripts/client.js browser_navigate '{"url": "https://example.com"}'
```

Sessions auto-expire after 15 minutes of inactivity.

### Headed Mode (Visible Browser)

Add `--headed` to see the browser window:
```bash
node scripts/client.js --headed browser_navigate '{"url": "https://example.com"}'
```

Note: The server must be restarted to switch between headed/headless modes:
```bash
node scripts/client.js --stop
```

## Token Optimization

Most tools accept an `expectation` object to control output size:
```json
{
  "expectation": {
    "includeSnapshot": false,
    "diffOptions": { "enabled": true }
  }
}
```

## Tools Reference

### Navigation

#### `browser_navigate`
Navigate to a URL.
```bash
node scripts/client.js browser_navigate '{"url": "https://example.com"}'
```

#### `browser_navigate_back`
Go back to previous page.
```bash
node scripts/client.js browser_navigate_back '{}'
```

#### `browser_navigate_forward`
Go forward to next page.
```bash
node scripts/client.js browser_navigate_forward '{}'
```

### Interaction

#### `browser_click`
Click an element. Supports CSS, text, role selectors.
```bash
node scripts/client.js browser_click '{"selectors": [{"css": "button.submit"}]}'
```

#### `browser_type`
Type text into an element.
```bash
node scripts/client.js browser_type '{"selectors": [{"css": "#search"}], "text": "query"}'
```

#### `browser_press_key`
Press a keyboard key.
```bash
node scripts/client.js browser_press_key '{"key": "Enter"}'
```

#### `browser_hover`
Hover over an element.
```bash
node scripts/client.js browser_hover '{"selectors": [{"css": ".menu-item"}]}'
```

#### `browser_drag`
Drag and drop between elements.
```bash
node scripts/client.js browser_drag '{"startSelectors": [{"css": "#source"}], "endSelectors": [{"css": "#target"}]}'
```

#### `browser_select_option`
Select option in dropdown.
```bash
node scripts/client.js browser_select_option '{"selectors": [{"css": "select#country"}], "values": ["US"]}'
```

#### `browser_file_upload`
Upload files to file input.
```bash
node scripts/client.js browser_file_upload '{"paths": ["/path/to/file.pdf"]}'
```

#### `browser_handle_dialog`
Handle alert/confirm/prompt dialogs.
```bash
node scripts/client.js browser_handle_dialog '{"accept": true}'
```

### Page State

#### `browser_snapshot`
Get accessibility snapshot of current page.
```bash
node scripts/client.js browser_snapshot '{}'
```

#### `browser_take_screenshot`
Take a screenshot.
```bash
node scripts/client.js browser_take_screenshot '{"filename": "page.png"}'
```

#### `browser_evaluate`
Evaluate JavaScript on page.
```bash
node scripts/client.js browser_evaluate '{"function": "() => document.title"}'
```

#### `browser_console_messages`
Get console messages.
```bash
node scripts/client.js browser_console_messages '{}'
```

#### `browser_network_requests`
Get network requests.
```bash
node scripts/client.js browser_network_requests '{}'
```

### Element Discovery

#### `browser_find_elements`
Find elements by text, role, tag, or attributes.
```bash
node scripts/client.js browser_find_elements '{"searchCriteria": {"text": "Submit"}}'
```

#### `browser_inspect_html`
Extract and analyze HTML content.
```bash
node scripts/client.js browser_inspect_html '{"selectors": [{"css": "main"}]}'
```

### Tab Management

#### `browser_tab_list`
List all open tabs.
```bash
node scripts/client.js browser_tab_list '{}'
```

#### `browser_tab_new`
Open a new tab.
```bash
node scripts/client.js browser_tab_new '{"url": "https://example.com"}'
```

#### `browser_tab_select`
Select a tab by index.
```bash
node scripts/client.js browser_tab_select '{"index": 0}'
```

#### `browser_tab_close`
Close a tab.
```bash
node scripts/client.js browser_tab_close '{}'
```

### Browser Control

#### `browser_resize`
Resize browser window.
```bash
node scripts/client.js browser_resize '{"width": 1920, "height": 1080}'
```

#### `browser_close`
Close the browser.
```bash
node scripts/client.js browser_close '{}'
```

#### `browser_install`
Install the configured browser.
```bash
node scripts/client.js browser_install '{}'
```

### Utilities

#### `browser_wait_for`
Wait for text to appear/disappear or time to pass.
```bash
node scripts/client.js browser_wait_for '{"text": "Loading complete"}'
node scripts/client.js browser_wait_for '{"textGone": "Loading..."}'
node scripts/client.js browser_wait_for '{"time": 2}'
```

#### `browser_diagnose`
Analyze page complexity and performance.
```bash
node scripts/client.js browser_diagnose '{}'
```

### Batch Execution

#### `browser_batch_execute`
Execute multiple steps in sequence. Highly recommended for forms.
```bash
node scripts/client.js browser_batch_execute '{
  "steps": [
    {"tool": "browser_type", "arguments": {"selectors": [{"css": "#user"}], "text": "me"}},
    {"tool": "browser_type", "arguments": {"selectors": [{"css": "#pass"}], "text": "123"}},
    {"tool": "browser_click", "arguments": {"selectors": [{"css": "#login"}]}}
  ]
}'
```

## Selector Types

All interaction tools support multiple selector strategies:

- **CSS**: `{"css": "#id"}`, `{"css": ".class"}`, `{"css": "button[type=submit]"}`
- **Role**: `{"role": "button"}`, `{"role": "textbox", "text": "Search"}`
- **Text**: `{"text": "Click me"}`
- **Ref**: `{"ref": "e3"}` (from previous snapshot)

Multiple selectors act as fallbacks:
```json
{"selectors": [{"css": "#submit"}, {"role": "button", "text": "Submit"}]}
```
