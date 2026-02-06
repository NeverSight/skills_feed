---
name: browser-devtools-cli
description: Automates browser interactions using Playwright for web testing, debugging, and automation. Use when the user needs to navigate websites, take screenshots, fill forms, click elements, extract page content (HTML/text), audit accessibility (ARIA/AX tree), measure Web Vitals performance, monitor console logs and HTTP requests, mock API responses, execute JavaScript in browser, inspect React components, compare UI with Figma designs, or perform non-blocking debugging with tracepoints, logpoints, and exception monitoring.
allowed-tools: Bash(browser-devtools-cli:*)
---

# Browser DevTools CLI

Command-line interface for browser automation, debugging, and testing using Playwright.

## Installation

```bash
npm install -g browser-devtools-mcp
```

## Quick Start

```bash
# Navigate to a URL
browser-devtools-cli navigation go-to --url "https://example.com"

# Take a screenshot
browser-devtools-cli content take-screenshot --name "homepage"

# Get page content as text
browser-devtools-cli content get-as-text
```

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session ID for browser state persistence | auto |
| `--json` | Output results as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |
| `--headless` | Run browser in headless mode | `true` |
| `--no-headless` | Run browser with visible window | - |
| `--persistent` | Preserve cookies/localStorage | `false` |
| `--no-persistent` | Clear state on session end | - |
| `--user-data-dir <path>` | Browser user data directory | OS temp |
| `--use-system-browser` | Use system Chrome | `false` |
| `--browser-path <path>` | Custom browser path | auto |

**AI Agent Recommended Options:**

```bash
# JSON output for parsing, quiet mode for clean output, session for state persistence
browser-devtools-cli --json --quiet --session-id "my-session" <command>
```

## Tool Domains

The CLI provides tools organized by domain:

| Domain | Description | Reference |
|--------|-------------|-----------|
| [navigation](./references/navigation.md) | Page navigation (go-to, back, forward, reload) |
| [content](./references/content.md) | Content extraction (screenshot, PDF, HTML, text) |
| [interaction](./references/interaction.md) | User interactions (click, fill, hover, scroll) |
| [a11y](./references/a11y.md) | Accessibility snapshots (ARIA, AX tree) |
| [o11y](./references/o11y.md) | Observability (Web Vitals, console, HTTP, traces) |
| [debug](./references/debug.md) | Non-blocking debugging (tracepoints, logpoints, exceptions) |
| [run](./references/run.md) | JavaScript execution (browser, sandbox) |
| [stub](./references/stub.md) | HTTP mocking (intercept, mock, clear) |
| [sync](./references/sync.md) | Synchronization (wait for network idle) |
| [react](./references/react.md) | React DevTools integration |
| [figma](./references/figma.md) | Figma design comparison |

## CLI Management Commands

### Daemon Management

```bash
browser-devtools-cli daemon status      # Check daemon status
browser-devtools-cli daemon info        # Show daemon info (version, uptime, sessions)
browser-devtools-cli daemon start       # Start daemon
browser-devtools-cli daemon stop        # Stop daemon
browser-devtools-cli daemon restart     # Restart daemon
```

### Session Management

```bash
browser-devtools-cli session list                  # List active sessions
browser-devtools-cli session info <session-id>     # Show session details
browser-devtools-cli session delete <session-id>   # Delete a session
```

### Tool Discovery

```bash
browser-devtools-cli tools list              # List all available tools
browser-devtools-cli tools search <query>    # Search tools by name or description
browser-devtools-cli tools info <tool-name>  # Show tool details and parameters
```

### Configuration

```bash
browser-devtools-cli config    # Show current configuration
```

### Updates

```bash
browser-devtools-cli update --check   # Check for updates
browser-devtools-cli update           # Check and install updates
```

## Examples

### Basic Navigation and Screenshot

```bash
# Navigate to URL
browser-devtools-cli navigation go-to --url "https://example.com"

# Take screenshot
browser-devtools-cli content take-screenshot --name "homepage"

# Get page text
browser-devtools-cli content get-as-text
```

### Form Automation

```bash
# Use same session for state persistence
SESSION="--session-id login-test"

# Navigate to login page
browser-devtools-cli $SESSION navigation go-to --url "https://app.example.com/login"

# Fill form fields
browser-devtools-cli $SESSION interaction fill --selector "#email" --value "user@example.com"
browser-devtools-cli $SESSION interaction fill --selector "#password" --value "password123"

# Submit form
browser-devtools-cli $SESSION interaction click --selector "button[type=submit]"

# Wait for navigation
browser-devtools-cli $SESSION sync wait-for-network-idle

# Capture result
browser-devtools-cli $SESSION content take-screenshot --name "dashboard"
```

### Performance Analysis

```bash
# Navigate
browser-devtools-cli navigation go-to --url "https://example.com"

# Get Web Vitals metrics
browser-devtools-cli --json o11y get-web-vitals

# Check console for errors
browser-devtools-cli --json o11y get-console-messages --types error,warn

# Analyze HTTP requests
browser-devtools-cli --json o11y get-http-requests
```

### Accessibility Audit

```bash
# Navigate
browser-devtools-cli navigation go-to --url "https://example.com"

# Get ARIA snapshot
browser-devtools-cli a11y take-aria-snapshot

# Get detailed AX tree
browser-devtools-cli --json a11y take-ax-tree-snapshot --roles button,link,textbox
```

### API Mocking

```bash
# Mock API response
browser-devtools-cli stub mock-http-response \
  --url-pattern "**/api/users" \
  --body '[{"id": 1, "name": "Test User"}]'

# Navigate and test
browser-devtools-cli navigation go-to --url "https://app.example.com"

# Clear mocks
browser-devtools-cli stub clear --all
```

### Non-Blocking Debugging

```bash
SESSION="--session-id debug-session"

# Navigate to app
browser-devtools-cli $SESSION navigation go-to --url "http://localhost:3000"

# Set tracepoint on a function
browser-devtools-cli $SESSION debug put-tracepoint \
  --url-pattern "app.js" \
  --line-number 42

# Add watch expression
browser-devtools-cli $SESSION debug add-watch --expression "this"

# Enable exception catching
browser-devtools-cli $SESSION debug put-exceptionpoint --state uncaught

# Monitor API calls
browser-devtools-cli $SESSION debug put-netpoint --url-pattern "/api/*"

# Interact with app (triggers probes)
browser-devtools-cli $SESSION interaction click --selector "#submit-btn"

# Get captured snapshots
browser-devtools-cli $SESSION --json debug get-tracepoint-snapshots
browser-devtools-cli $SESSION --json debug get-exceptionpoint-snapshots
browser-devtools-cli $SESSION --json debug get-netpoint-snapshots
```

### Shell Script for CI/CD

```bash
#!/bin/bash
set -e

CLI="browser-devtools-cli --json --quiet --session-id ci-test-$$"

# Navigate
$CLI navigation go-to --url "https://example.com"

# Wait for load
$CLI sync wait-for-network-idle

# Take screenshot
$CLI content take-screenshot --name "ci-test"

# Get Web Vitals
VITALS=$($CLI o11y get-web-vitals)
echo "Web Vitals: $VITALS"

# Check for console errors
ERRORS=$($CLI o11y get-console-messages --types error)
if [ "$ERRORS" != "[]" ]; then
  echo "Console errors found: $ERRORS"
  exit 1
fi

# Cleanup
$CLI session delete "ci-test-$$"
```

## Interactive Mode (Human Users)

For manual exploration, an interactive REPL mode is available:

```bash
browser-devtools-cli interactive
browser-devtools-cli --no-headless interactive   # With visible browser
```

| Command | Description |
|---------|-------------|
| `help` | Show available commands |
| `exit`, `quit` | Exit interactive mode |
| `<domain> <tool>` | Execute a tool |

## Shell Completions

```bash
# Generate and install completions
echo 'eval "$(browser-devtools-cli completion bash)"' >> ~/.bashrc
echo 'eval "$(browser-devtools-cli completion zsh)"' >> ~/.zshrc
```
