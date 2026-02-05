---
name: cmux
description: Manage cloud development sandboxes with cmux. Create, sync, and access remote VMs. Includes browser automation via Chrome CDP for scraping, testing, and web interaction.
---

# cmux - Cloud Sandboxes for Development

cmux manages cloud sandboxes for development. Use these commands to create, manage, and access remote development environments with built-in browser automation.

## Installation

```bash
npm install -g cmux
```

## Quick Start

```bash
cmux login                      # Authenticate (opens browser)
cmux start ./my-project         # Create sandbox, sync directory → returns ID
cmux code <id>                  # Open VS Code
cmux pty <id>                   # Open terminal session
cmux sync <id> ./my-project     # Sync files via rsync
cmux computer screenshot <id>   # Take browser screenshot
cmux stop <id>                  # Stop sandbox
cmux delete <id>                # Delete sandbox
cmux ls                         # List all sandboxes
```

## Commands

### Authentication

```bash
cmux login               # Login (opens browser)
cmux logout              # Logout and clear credentials
cmux whoami              # Show current user and team
```

### Sandbox Lifecycle

```bash
cmux start [path]        # Create sandbox, optionally sync directory
cmux start -i [path]     # Create and open VS Code immediately
cmux ls                  # List all sandboxes
cmux status <id>         # Show sandbox details and URLs
cmux stop <id>           # Stop sandbox
cmux extend <id>         # Extend sandbox timeout
cmux delete <id>         # Delete sandbox permanently
cmux templates           # List available templates
```

### Access Sandbox

```bash
cmux code <id>           # Open VS Code in browser
cmux vnc <id>            # Open VNC desktop in browser
cmux pty <id>            # Interactive terminal session
```

### Work with Sandbox

```bash
cmux exec <id> "cmd"           # Run command in sandbox
cmux sync <id> <path>          # Sync local files to sandbox (rsync)
cmux sync <id> <path> --pull   # Pull files from sandbox
cmux sync <id> <path> --watch  # Watch and sync on changes
```

### Browser Automation (cmux computer)

Control Chrome browser via CDP in the sandbox's VNC desktop.

#### Navigation

```bash
cmux computer open <id> <url>    # Navigate to URL
cmux computer back <id>          # Navigate back
cmux computer forward <id>       # Navigate forward
cmux computer reload <id>        # Reload page
cmux computer url <id>           # Get current URL
cmux computer title <id>         # Get page title
```

#### Inspect Page

```bash
cmux computer snapshot <id>             # Get accessibility tree with element refs (@e1, @e2...)
cmux computer screenshot <id>           # Take screenshot (base64 to stdout)
cmux computer screenshot <id> out.png   # Save screenshot to file
```

#### Interact with Elements

```bash
cmux computer click <id> <selector>      # Click element (@e1 or CSS selector)
cmux computer type <id> "text"           # Type into focused element
cmux computer fill <id> <sel> "value"    # Clear input and fill with value
cmux computer press <id> <key>           # Press key (Enter, Tab, Escape, etc.)
cmux computer hover <id> <selector>      # Hover over element
cmux computer scroll <id> [direction]    # Scroll page (up/down/left/right)
cmux computer wait <id> <selector>       # Wait for element to appear
```

#### Element Selectors

Two ways to select elements:
- **Element refs** from snapshot: `@e1`, `@e2`, `@e3`...
- **CSS selectors**: `#id`, `.class`, `button[type="submit"]`

## Sandbox IDs

Sandbox IDs look like `cmux_abc12345`. Use the full ID when running commands. Get IDs from `cmux ls` or `cmux start` output.

## Common Workflows

### Create and develop in a sandbox

```bash
cmux start ./my-project        # Creates sandbox, syncs files
cmux code cmux_abc123          # Open VS Code
cmux exec cmux_abc123 "npm install && npm run dev"
```

### Sync workflow

```bash
cmux sync cmux_abc123 . --watch      # Watch local changes, sync automatically
cmux sync cmux_abc123 ./dist --pull  # Pull build output back
```

### Browser automation: Login to a website

```bash
cmux computer open cmux_abc123 "https://example.com/login"
cmux computer snapshot cmux_abc123
# Output: @e1 [input] Email, @e2 [input] Password, @e3 [button] Sign In

cmux computer fill cmux_abc123 @e1 "user@example.com"
cmux computer fill cmux_abc123 @e2 "password123"
cmux computer click cmux_abc123 @e3
cmux computer screenshot cmux_abc123 result.png
```

### Browser automation: Scrape data

```bash
cmux computer open cmux_abc123 "https://example.com/data"
cmux computer snapshot cmux_abc123   # Get structured accessibility tree
cmux computer screenshot cmux_abc123 # Visual capture
```

### Clean up

```bash
cmux stop cmux_abc123      # Stop (can restart later)
cmux delete cmux_abc123    # Delete permanently
```

## Tips

- Run `cmux login` first if not authenticated
- Use `--json` flag for machine-readable output
- Use `-t <team>` to override default team
- Use `-v` for verbose output
- Always run `snapshot` first to see available elements before browser automation
- Use element refs (`@e1`) for reliability over CSS selectors
