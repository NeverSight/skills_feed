---
name: agent-browser
description: Browser automation for web testing, form filling, screenshots, and data extraction. Use when navigating websites, interacting with web pages, filling forms, taking screenshots, testing web applications, or extracting information from web pages.
license: Apache-2.0
compatibility:
  - claude-code
  - claude-desktop
  - gemini-cli
  - aider
metadata:
  version: "1.0.0"
  author: bentossell
  repository: https://github.com/bentossell/skill-agent-browser
allowed-tools:
  - bash
  - computer
---

# Browser Automation with agent-browser

Headless browser automation CLI for AI agents. Fast Rust CLI with Node.js fallback.

## Installation

```bash
npm install -g agent-browser
agent-browser install  # Download Chromium
```

## Quick Start

```bash
agent-browser open <url>        # Navigate to page
agent-browser snapshot -i       # Get interactive elements with refs
agent-browser click @e1         # Click element by ref
agent-browser fill @e2 "text"   # Fill input by ref
agent-browser close             # Close browser
```

## Core Workflow

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
3. **Interact** using refs from the snapshot
4. **Re-snapshot** after navigation or significant DOM changes

## Commands

### Navigation

```bash
agent-browser open <url>      # Navigate to URL
agent-browser back            # Go back
agent-browser forward         # Go forward  
agent-browser reload          # Reload page
agent-browser close           # Close browser
```

### Snapshot (Page Analysis)

```bash
agent-browser snapshot        # Full accessibility tree
agent-browser snapshot -i     # Interactive elements only (recommended)
agent-browser snapshot -c     # Compact output
agent-browser snapshot -d 3   # Limit depth to 3
```

### Interactions (Use @refs from Snapshot)

```bash
agent-browser click @e1                    # Click
agent-browser dblclick @e1                 # Double-click
agent-browser fill @e1 "text"              # Fill input
agent-browser type @e1 "text"              # Type character by character
agent-browser select @e1 "option"          # Select dropdown option
agent-browser check @e1                    # Check checkbox
agent-browser uncheck @e1                  # Uncheck checkbox
agent-browser hover @e1                    # Hover over element
agent-browser focus @e1                    # Focus element
agent-browser press Enter                  # Press key
agent-browser scroll @e1 down 200          # Scroll element
```

### Screenshots & Media

```bash
agent-browser screenshot page.png          # Full page screenshot
agent-browser screenshot @e1 element.png   # Element screenshot
agent-browser pdf output.pdf               # Save page as PDF
```

### Getting Data

```bash
agent-browser get text @e1                 # Get element text
agent-browser get value @e1                # Get input value
agent-browser get attr @e1 href            # Get attribute
agent-browser get html @e1                 # Get inner HTML
agent-browser eval "document.title"        # Run JavaScript
```

### Waiting

```bash
agent-browser wait --load networkidle      # Wait for network idle
agent-browser wait --url "**/dashboard"    # Wait for URL pattern
agent-browser wait --text "Success"        # Wait for text to appear
agent-browser wait @e1                     # Wait for element
agent-browser wait @e1 --hidden            # Wait for element to hide
```

### Sessions (Parallel Browsers)

```bash
agent-browser --session test1 open site-a.com
agent-browser --session test2 open site-b.com
agent-browser session list
```

### Authentication State

```bash
agent-browser state save auth.json         # Save cookies/storage
agent-browser state load auth.json         # Restore state
```

## Example: Form Submission

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: textbox "Email" [ref=e1], textbox "Password" [ref=e2], button "Submit" [ref=e3]

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Example: Login and Save State

```bash
# Login once
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "username"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json

# Later: restore authenticated session
agent-browser state load auth.json
agent-browser open https://app.example.com/dashboard
```

## Example: Content Review

Review a web page by taking snapshots and interacting:

```bash
# Open page to review
agent-browser open http://localhost:3456/cookbook/what-is-cli/

# Get interactive elements
agent-browser snapshot -i
# Output shows buttons, links, inputs with refs

# Test interactive elements
agent-browser click @e75  # Click a suggestion button

# Take screenshot for visual review
agent-browser screenshot review.png

# Re-snapshot to verify state changed
agent-browser snapshot -i
```

## Alternative Selectors

When refs aren't available, use CSS selectors or semantic search:

```bash
agent-browser click "#submit"
agent-browser fill "#email" "test@example.com"
agent-browser find role button click --name "Submit"
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
```

## JSON Output

Add `--json` for machine-readable output:

```bash
agent-browser snapshot -i --json
agent-browser get text @e1 --json
```

## Debugging

```bash
agent-browser open example.com --headed  # Show browser window
agent-browser console                    # View console messages
agent-browser errors                     # View page errors
```

## Tips

1. **Always snapshot first** - Get refs before interacting
2. **Re-snapshot after navigation** - Refs change when page updates
3. **Use `-i` flag** - Interactive-only snapshots are cleaner
4. **Save auth state** - Avoid re-logging in for each session
5. **Use `--json`** - When parsing output programmatically
