---
name: agent-browser
description: Use Agent Browser CLI for headless browser automation and E2E testing. Invoke when user needs to automate browser tasks, run E2E tests, capture screenshots, interact with web pages, or perform web scraping tasks.
allowed-tools: Bash, Read, Write, Glob
---

# Agent Browser CLI

Agent Browser is a fast headless browser automation CLI designed for AI agents. Use it for E2E testing, web automation, and browser-based tasks.

## Quick Start

```bash
# Navigate and capture state
agent-browser open https://example.com
agent-browser snapshot -i    # Get interactive elements with refs (@e1, @e2, etc.)
agent-browser click @e2      # Click by reference
agent-browser screenshot page.png
agent-browser close
```

## Core Commands

### Navigation
```bash
agent-browser open <url>        # Navigate to URL
agent-browser back              # Go back
agent-browser forward           # Go forward
agent-browser reload            # Reload page
agent-browser close             # Close browser
```

### Element Interaction
```bash
agent-browser click <sel>       # Click element (CSS selector or @ref)
agent-browser dblclick <sel>    # Double-click
agent-browser type <sel> <text> # Type into element (appends)
agent-browser fill <sel> <text> # Clear and fill (replaces)
agent-browser press <key>       # Press key (Enter, Tab, Control+a)
agent-browser hover <sel>       # Hover over element
agent-browser focus <sel>       # Focus element
agent-browser check <sel>       # Check checkbox
agent-browser uncheck <sel>     # Uncheck checkbox
agent-browser select <sel> <val> # Select dropdown option
agent-browser drag <src> <dst>  # Drag and drop
agent-browser upload <sel> <files...> # Upload files
```

### Scrolling
```bash
agent-browser scroll <dir> [px] # Scroll (up/down/left/right)
agent-browser scrollintoview <sel> # Scroll element into view
```

### Waiting
```bash
agent-browser wait <sel>        # Wait for element to appear
agent-browser wait 2000         # Wait milliseconds
```

### Capture
```bash
agent-browser screenshot [path]   # Take screenshot
agent-browser screenshot --full   # Full page screenshot
agent-browser pdf <path>          # Save as PDF
agent-browser snapshot            # Get accessibility tree with refs
agent-browser snapshot -i         # Interactive elements only
agent-browser snapshot -c         # Compact (remove empty elements)
agent-browser snapshot -d 3       # Limit depth
```

### Get Information
```bash
agent-browser get text <sel>      # Get element text
agent-browser get html <sel>      # Get element HTML
agent-browser get value <sel>     # Get input value
agent-browser get attr <name> <sel> # Get attribute
agent-browser get title           # Get page title
agent-browser get url             # Get current URL
agent-browser get count <sel>     # Count matching elements
agent-browser get box <sel>       # Get bounding box
```

### Check State
```bash
agent-browser is visible <sel>    # Check if visible
agent-browser is enabled <sel>    # Check if enabled
agent-browser is checked <sel>    # Check if checked
```

### Find Elements
```bash
agent-browser find role button click          # Find by role and click
agent-browser find text "Submit" click        # Find by text and click
agent-browser find label "Email" fill "test@example.com"
agent-browser find placeholder "Search..." fill "query"
agent-browser find testid "submit-btn" click
```

### JavaScript Execution
```bash
agent-browser eval "document.title"                    # Get title
agent-browser eval "window.scrollTo(0, 0)"            # Scroll to top
agent-browser eval "localStorage.getItem('token')"    # Get storage
```

### Session Management
```bash
agent-browser --session mytest open example.com  # Use isolated session
agent-browser session                            # Show current session
agent-browser session list                       # List active sessions
```

### Tab Management
```bash
agent-browser tab new              # Open new tab
agent-browser tab list             # List tabs
agent-browser tab 2                # Switch to tab 2
agent-browser tab close            # Close current tab
```

### Network
```bash
agent-browser network requests              # View network requests
agent-browser network requests --clear      # Clear requests
agent-browser network route "*/api/*" --abort  # Block API calls
agent-browser set offline on                # Enable offline mode
agent-browser set headers '{"Auth": "token"}'  # Set headers
```

### Browser Settings
```bash
agent-browser set viewport 1920 1080        # Set viewport size
agent-browser set device "iPhone 12"        # Emulate device
agent-browser set geo 37.7749 -122.4194     # Set geolocation
agent-browser set media dark                # Enable dark mode
```

### Debug
```bash
agent-browser console              # View console logs
agent-browser errors               # View page errors
agent-browser highlight <sel>      # Highlight element
agent-browser trace start          # Start recording trace
agent-browser trace stop trace.zip # Stop and save trace
```

## Session Isolation

Always use `--session` flag for isolated testing:

```bash
# Create isolated session for E2E test
export AGENT_BROWSER_SESSION="e2e-test-$(date +%s)"

agent-browser open https://app.example.com
agent-browser snapshot -i
agent-browser fill @e5 "user@test.com"
agent-browser fill @e6 "password123"
agent-browser click @e7
agent-browser wait "[data-testid='dashboard']"
agent-browser screenshot results/login-success.png
agent-browser close
```

## E2E Testing Pattern

```bash
#!/bin/bash
# Example E2E test script

SESSION="test-$(date +%s)"
RESULTS_DIR="./test-results"
mkdir -p "$RESULTS_DIR"

# Setup
agent-browser --session "$SESSION" open "$BASE_URL"

# Test login flow
agent-browser --session "$SESSION" snapshot -i
agent-browser --session "$SESSION" fill "[name='email']" "$TEST_EMAIL"
agent-browser --session "$SESSION" fill "[name='password']" "$TEST_PASSWORD"
agent-browser --session "$SESSION" click "[type='submit']"
agent-browser --session "$SESSION" wait "[data-testid='dashboard']" || {
    agent-browser --session "$SESSION" screenshot "$RESULTS_DIR/login-failed.png"
    exit 1
}
agent-browser --session "$SESSION" screenshot "$RESULTS_DIR/login-success.png"

# Verify dashboard elements
TITLE=$(agent-browser --session "$SESSION" get text "h1")
if [[ "$TITLE" != *"Dashboard"* ]]; then
    echo "FAIL: Dashboard title not found"
    exit 1
fi

# Cleanup
agent-browser --session "$SESSION" close
echo "PASS: Login test completed"
```

## Key Options

| Option | Description |
|--------|-------------|
| `--session <name>` | Isolated browser session |
| `--headed` | Show browser window (not headless) |
| `--json` | JSON output format |
| `--full`, `-f` | Full page screenshot |
| `--cdp <port>` | Connect via Chrome DevTools Protocol |
| `--debug` | Enable debug output |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `AGENT_BROWSER_SESSION` | Default session name |
| `AGENT_BROWSER_EXECUTABLE_PATH` | Custom browser path |
| `AGENT_BROWSER_STREAM_PORT` | WebSocket streaming port |

## Best Practices

1. **Always use sessions** for test isolation
2. **Use snapshots** to get element refs before interactions
3. **Wait for elements** before interacting with dynamic content
4. **Take screenshots** at key checkpoints for debugging
5. **Clean up sessions** with `close` when done
6. **Use `--headed`** during development to see what's happening

## Common Workflows

### Form Submission
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
agent-browser fill "[name='email']" "user@example.com"
agent-browser fill "[name='message']" "Hello world"
agent-browser click "[type='submit']"
agent-browser wait ".success-message"
agent-browser screenshot form-submitted.png
```

### Authentication Testing
```bash
agent-browser open https://app.example.com/login
agent-browser fill "#email" "test@example.com"
agent-browser fill "#password" "testpass123"
agent-browser click "button[type='submit']"
agent-browser wait "[data-auth='true']"
agent-browser get text ".user-name"
```

### Web Scraping
```bash
agent-browser open https://example.com/products
agent-browser get text ".product-title" --json
agent-browser get attr "href" ".product-link" --json
agent-browser screenshot products.png --full
```
