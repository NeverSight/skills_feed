---
name: pilotty
description: Automates terminal TUI applications (vim, htop, lazygit, dialog) through managed PTY sessions. Use when the user needs to interact with terminal apps, edit files in vim/nano, navigate TUI menus, click terminal buttons/checkboxes, or automate CLI workflows with interactive prompts.
allowed-tools: Bash(pilotty:*)
---

# Terminal Automation with pilotty

## CRITICAL: Argument Positioning

**All flags (`--name`, `-s`, `--format`, etc.) MUST come BEFORE positional arguments:**

```bash
# CORRECT - flags before command/arguments
pilotty spawn --name myapp vim file.txt
pilotty key -s myapp Enter
pilotty snapshot -s myapp --format text

# WRONG - flags after command (they get passed to the app, not pilotty!)
pilotty spawn vim file.txt --name myapp   # FAILS: --name goes to vim
pilotty key Enter -s myapp                # FAILS: -s goes nowhere useful
```

This is the #1 cause of agent failures. When in doubt: **flags first, then command/args**.

---

## Quick start

```bash
pilotty spawn vim file.txt        # Start TUI app in managed session
pilotty wait-for "file.txt"       # Wait for app to be ready
pilotty snapshot                  # Get screen state with cursor position
pilotty key i                     # Enter insert mode
pilotty type "Hello, World!"      # Type text
pilotty key Escape                # Exit insert mode
pilotty kill                      # End session
```

## Core workflow

1. **Spawn**: `pilotty spawn <command>` starts the app in a background PTY
2. **Wait**: `pilotty wait-for <text>` ensures the app is ready
3. **Snapshot**: `pilotty snapshot` returns screen state with text content and cursor position
4. **Interact**: Use keyboard commands (`key`, `type`) or click at coordinates (`click <row> <col>`)
5. **Re-snapshot**: After screen changes, snapshot again to see updated state

## Commands

### Session management

```bash
pilotty spawn <command>           # Start TUI app (e.g., pilotty spawn htop)
pilotty spawn --name myapp <cmd>  # Start with custom session name (--name before command)
pilotty kill                      # Kill default session
pilotty kill -s myapp             # Kill specific session
pilotty list-sessions             # List all active sessions
pilotty daemon                    # Manually start daemon (usually auto-starts)
pilotty stop                      # Stop daemon and all sessions
pilotty examples                  # Show end-to-end workflow example
```

### Screen capture

```bash
pilotty snapshot                  # Full JSON with text content
pilotty snapshot --format compact # JSON without text field
pilotty snapshot --format text    # Plain text with cursor indicator
pilotty snapshot -s myapp         # Snapshot specific session
```

### Input

```bash
pilotty type "hello"              # Type text at cursor
pilotty type -s myapp "text"      # Type in specific session

pilotty key Enter                 # Press Enter
pilotty key Ctrl+C                # Send interrupt
pilotty key Escape                # Send Escape
pilotty key Tab                   # Send Tab
pilotty key F1                    # Function key
pilotty key Alt+F                 # Alt combination
pilotty key Up                    # Arrow key
pilotty key -s myapp Ctrl+S       # Key in specific session
```

### Interaction

```bash
pilotty click 5 10                # Click at row 5, col 10
pilotty click -s myapp 10 20      # Click in specific session
pilotty scroll up                 # Scroll up 1 line
pilotty scroll down 5             # Scroll down 5 lines
pilotty scroll up 10 -s myapp     # Scroll in specific session
```

### Terminal control

```bash
pilotty resize 120 40             # Resize terminal to 120 cols x 40 rows
pilotty resize 80 24 -s myapp     # Resize specific session

pilotty wait-for "Ready"          # Wait for text to appear (30s default)
pilotty wait-for "Error" -r       # Wait for regex pattern
pilotty wait-for "Done" -t 5000   # Wait with 5s timeout
pilotty wait-for "~" -s editor    # Wait in specific session
```

## Global options

| Option | Description |
|--------|-------------|
| `-s, --session <name>` | Target specific session (default: "default") |
| `--format <fmt>` | Snapshot format: full, compact, text |
| `-t, --timeout <ms>` | Timeout for wait-for (default: 30000) |
| `-r, --regex` | Treat wait-for pattern as regex |
| `--name <name>` | Session name for spawn command |

### Environment variables

```bash
PILOTTY_SESSION="mysession"       # Default session name
PILOTTY_SOCKET_DIR="/tmp/pilotty" # Override socket directory
RUST_LOG="debug"                  # Enable debug logging
```

## Snapshot output

The `snapshot` command returns structured JSON:

```json
{
  "snapshot_id": 42,
  "size": { "cols": 80, "rows": 24 },
  "cursor": { "row": 5, "col": 10, "visible": true },
  "text": "... plain text content ..."
}
```

Use `--format text` for a plain text view with cursor indicator:

```
--- Terminal 80x24 | Cursor: (5, 10) ---
bash-3.2$ [_]
```

The `[_]` shows cursor position. Use the text content to understand screen state and navigate with keyboard commands.

## Navigation approach

pilotty uses keyboard-first navigation, just like a human would:

```bash
# 1. Take snapshot to see the screen
pilotty snapshot --format text

# 2. Navigate using keyboard
pilotty key Tab           # Move to next element
pilotty key Enter         # Activate/select
pilotty key Escape        # Cancel/back
pilotty key Up            # Move up in list/menu

# 3. Type text when needed
pilotty type "search term"
pilotty key Enter

# 4. Click at coordinates for mouse-enabled TUIs
pilotty click 5 10        # Click at row 5, col 10
```

**Key insight**: Parse the snapshot text to understand what's on screen, then use keyboard commands to navigate. This works reliably across all TUI applications.

## Example: Edit file with vim

```bash
# 1. Spawn vim
pilotty spawn --name editor vim /tmp/hello.txt

# 2. Wait for vim to load
pilotty wait-for -s editor "hello.txt"

# 3. Enter insert mode
pilotty key -s editor i

# 4. Type content
pilotty type -s editor "Hello from pilotty!"

# 5. Exit insert mode
pilotty key -s editor Escape

# 6. Save and quit
pilotty type -s editor ":wq"
pilotty key -s editor Enter

# 7. Verify session ended
pilotty list-sessions
```

## Example: Dialog interaction

```bash
# 1. Spawn dialog (--name before command)
pilotty spawn --name dialog dialog --yesno "Continue?" 10 40

# 2. Get snapshot to see the dialog
pilotty snapshot -s dialog --format text
# Shows: < Yes > and < No > buttons

# 3. Navigate with keyboard
pilotty key -s dialog Tab      # Move to next button
pilotty key -s dialog Enter    # Activate selected button

# Or click at coordinates if you know the button position
pilotty click -s dialog 8 15   # Click at row 8, col 15
```

## Example: Monitor with htop

```bash
# 1. Spawn htop
pilotty spawn --name monitor htop

# 2. Wait for display
pilotty wait-for -s monitor "CPU"

# 3. Take snapshot to see current state
pilotty snapshot -s monitor --format text

# 4. Send commands
pilotty key -s monitor F9    # Kill menu
pilotty key -s monitor q     # Quit

# 5. Kill session
pilotty kill -s monitor
```

## Sessions

Each session is isolated with its own:
- PTY (pseudo-terminal)
- Screen buffer
- Child process

```bash
# Run multiple apps (--name must come before the command)
pilotty spawn --name monitoring htop
pilotty spawn --name editor vim file.txt

# Target specific session
pilotty snapshot -s monitoring
pilotty key -s editor Ctrl+S

# List all
pilotty list-sessions

# Kill specific
pilotty kill -s editor
```

The first session spawned without `--name` is automatically named `default`.

> **Important:** The `--name` flag must come **before** the command. Everything after the command is passed as arguments to that command.

## Daemon architecture

pilotty uses a background daemon for session management:

- **Auto-start**: Daemon starts on first command
- **Auto-stop**: Shuts down after 5 minutes with no sessions
- **Session cleanup**: Sessions removed when process exits (within 500ms)
- **Shared state**: Multiple CLI calls share sessions

You rarely need to manage the daemon manually.

## Error handling

Errors include actionable suggestions:

```json
{
  "code": "SESSION_NOT_FOUND",
  "message": "Session 'abc123' not found",
  "suggestion": "Run 'pilotty list-sessions' to see available sessions"
}
```

```json
{
  "code": "SPAWN_FAILED",
  "message": "Failed to spawn process: command not found",
  "suggestion": "Check that the command exists and is in PATH"
}
```

## Common patterns

### Wait then act

```bash
pilotty spawn my-app
pilotty wait-for "Ready"    # Ensure app is ready
pilotty snapshot            # Then snapshot
```

### Check state before action

```bash
pilotty snapshot --format text | grep "Error"  # Check for errors
pilotty key Enter                               # Then proceed
```

### Retry on timeout

```bash
pilotty wait-for "Ready" -t 5000 || {
  pilotty snapshot --format text   # Check what's on screen
  # Adjust approach based on actual state
}
```

## Deep-dive documentation

For detailed patterns and edge cases, see:

| Reference | Description |
|-----------|-------------|
| [references/session-management.md](references/session-management.md) | Multi-session patterns, isolation, cleanup |
| [references/key-input.md](references/key-input.md) | Complete key combinations reference |

## Ready-to-use templates

Executable workflow scripts:

| Template | Description |
|----------|-------------|
| [templates/vim-workflow.sh](templates/vim-workflow.sh) | Edit file with vim, save, exit |
| [templates/dialog-interaction.sh](templates/dialog-interaction.sh) | Handle dialog/whiptail prompts |
| [templates/multi-session.sh](templates/multi-session.sh) | Parallel TUI orchestration |

Usage:
```bash
./templates/vim-workflow.sh /tmp/myfile.txt "File content here"
./templates/dialog-interaction.sh
./templates/multi-session.sh
```
