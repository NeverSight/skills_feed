---
name: agent-browser
description: Browser automation using the agent-browser CLI. Use when user asks to browse websites, open webpages, interact with page elements, take screenshots, fill forms, click buttons, scrape content, or automate browser tasks.
license: MIT
compatibility: Requires agent-browser CLI (npm install -g agent-browser)
metadata:
  author: linuxlewis
  version: "1.0.0"
---

# Agent Browser

Browser automation using the `agent-browser` CLI - a fast, headless browser automation tool for AI agents.

## Installation

```bash
npm install -g agent-browser
agent-browser install  # Install browser binaries
```

## Quick Start

```bash
# Navigate to a URL
agent-browser open https://example.com

# Get accessibility snapshot (shows refs like @e1, @e2)
agent-browser snapshot -i

# Click using ref from snapshot
agent-browser click @e2

# Type into an element
agent-browser fill @e3 "hello world"

# Take screenshot
agent-browser screenshot output.png
```

## Workflow Pattern

1. **Open** - Navigate to the target URL
2. **Snapshot** - Get the accessibility tree to see available elements
3. **Interact** - Use refs (@e1, @e2, etc.) to interact with elements
4. **Verify** - Take a snapshot or screenshot to verify state

## Core Commands

See [references/commands.md](references/commands.md) for the complete command reference.

### Navigation
```bash
agent-browser open <url>           # Navigate to URL
agent-browser back                 # Go back
agent-browser forward              # Go forward
agent-browser reload               # Reload page
```

### Interaction
```bash
agent-browser click <sel>          # Click element (or @ref)
agent-browser fill <sel> <text>    # Clear and fill
agent-browser press <key>          # Press key (Enter, Tab, etc.)
agent-browser select <sel> <val>   # Select dropdown option
```

### Getting Information
```bash
agent-browser snapshot             # Accessibility tree with refs
agent-browser snapshot -i          # Interactive elements only
agent-browser get text <sel>       # Get element text
agent-browser get url              # Get current URL
```

### Capture
```bash
agent-browser screenshot [path]    # Take screenshot
agent-browser screenshot --full    # Full page screenshot
agent-browser pdf <path>           # Save as PDF
```

## Sessions

Use sessions to maintain browser state across commands:

```bash
agent-browser --session myproject open https://example.com
agent-browser --session myproject snapshot
agent-browser --session myproject click @e1
```

## Selectors

- **Refs**: `@e1`, `@e2` (from snapshot output) - **preferred**
- **CSS**: `#id`, `.class`, `div > span`
- **Text**: `text=Submit`
- **Role**: `role=button[name="Submit"]`

## Best Practices

1. **Always snapshot first** - Get the accessibility tree before interacting
2. **Use refs** - Prefer `@e1` refs from snapshot over CSS selectors
3. **Use sessions** - Maintain state across multiple commands
4. **Wait appropriately** - Use `wait` for dynamic content
5. **Verify actions** - Snapshot or screenshot after interactions
