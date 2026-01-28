---
name: agent-rdp
description: Controls Windows Remote Desktop sessions for automation, testing, and remote administration. Use when the user needs to connect to Windows machines via RDP, take screenshots, click, type, or interact with remote Windows desktops.
allowed-tools: Bash(agent-rdp:*)
---

# Windows Remote Desktop Control with agent-rdp

## Quick start

```bash
agent-rdp connect --host <ip> -u <user> -p <pass> --enable-win-automation
agent-rdp automate snapshot -i              # See interactive elements
agent-rdp automate click "@e5"              # Click button by ref
agent-rdp automate fill "@e7" "Hello"       # Type into field
agent-rdp disconnect
```

## Core workflow

1. Connect with automation: `agent-rdp connect --host <ip> -u <user> -p <pass> --enable-win-automation`
2. Snapshot: `agent-rdp automate snapshot -i` (get accessibility tree with refs)
3. Act: `agent-rdp automate click @e5` or `agent-rdp automate fill @e7 "text"`
4. Repeat: snapshot → act → snapshot → act...

## Troubleshooting

### Element not in snapshot with `-i`

Try without `-i` flag - some elements aren't marked as interactive but are still actionable:
```bash
agent-rdp automate snapshot              # Full tree, no filtering
agent-rdp automate snapshot -d 5         # Limit depth if too large
```

### Element not in accessibility tree at all

Some UI elements (WebView content, certain dialogs, toast notifications) don't appear in the accessibility tree. Use OCR as a last resort:

1. Take screenshot to identify what you need: `agent-rdp screenshot -o screen.png`
2. Use locate to find coordinates: `agent-rdp locate "Button Text"`
3. Click using returned coordinates: `agent-rdp mouse click <x> <y>`

## Commands

### Connection
```bash
agent-rdp connect --host 192.168.1.100 -u Admin -p secret
agent-rdp connect --host 192.168.1.100 -u Admin --password-stdin  # Read password from stdin
agent-rdp connect --host 192.168.1.100 --width 1920 --height 1080
agent-rdp connect --host 192.168.1.100 --drive /tmp/share:Share   # Map local directory
agent-rdp disconnect
```

### Screenshot
```bash
agent-rdp screenshot                      # Save to ./screenshot.png
agent-rdp screenshot -o desktop.png       # Save to specific file
agent-rdp screenshot --format jpeg        # JPEG format
```

### Mouse
```bash
agent-rdp mouse click 500 300             # Left click at (500, 300)
agent-rdp mouse right-click 500 300       # Right click
agent-rdp mouse double-click 500 300      # Double click
agent-rdp mouse move 100 200              # Move cursor
agent-rdp mouse drag 100 100 500 500      # Drag from (100,100) to (500,500)
```

### Keyboard
```bash
agent-rdp keyboard type "Hello World"     # Type text (supports Unicode)
agent-rdp keyboard press "ctrl+c"         # Key combination
agent-rdp keyboard press "alt+tab"        # Switch windows
agent-rdp keyboard press "ctrl+shift+esc" # Task manager
agent-rdp keyboard press "win+r"          # Run dialog
agent-rdp keyboard press enter            # Single key (use press, not key)
agent-rdp keyboard press escape
agent-rdp keyboard press f5
```

### Scroll
```bash
agent-rdp scroll up --amount 3            # Scroll up 3 notches
agent-rdp scroll down --amount 5          # Scroll down 5 notches
agent-rdp scroll left
agent-rdp scroll right
```

### Clipboard
```bash
agent-rdp clipboard set "Text to paste"   # Set clipboard (paste on Windows)
agent-rdp clipboard get                   # Get clipboard (after copy on Windows)
```

### Drive mapping
```bash
# Map at connect time
agent-rdp connect --host <ip> -u <user> -p <pass> --drive /local/path:DriveName

# List mapped drives
agent-rdp drive list
```

### Session management
```bash
agent-rdp session list                    # List active sessions
agent-rdp session info                    # Current session info
agent-rdp --session work connect ...      # Named session
agent-rdp --session work screenshot       # Use named session
```

### Wait
```bash
agent-rdp wait 2000                       # Wait 2 seconds
```

### Locate (OCR)
```bash
agent-rdp locate "Cancel"                 # Find lines containing "Cancel"
agent-rdp locate "Save*" --pattern        # Glob pattern matching
agent-rdp locate --all                    # Get all text on screen
agent-rdp locate "OK" --json              # JSON output with coordinates
```

Returns text lines with bounding boxes and center coordinates for clicking:
```
Found 1 line(s) containing 'Cancel':
  'Cancel' at (650, 420) size 45x14 - center: (672, 427)

To click the first match: agent-rdp mouse click 672 427
```

### UI Automation
```bash
# Connect with automation enabled
agent-rdp connect --host 192.168.1.100 -u Admin -p secret --enable-win-automation

# Snapshot - get accessibility tree (refs always included)
agent-rdp automate snapshot                # Full desktop tree
agent-rdp automate snapshot -i             # Interactive elements only
agent-rdp automate snapshot -c             # Compact (remove empty elements)
agent-rdp automate snapshot -d 5           # Limit depth to 5 levels
agent-rdp automate snapshot -s "~*Notepad*"# Scope to a window/element
agent-rdp automate snapshot -f             # Start from focused element
agent-rdp automate snapshot -i -c -d 3     # Combine options

# Pattern-based element operations (use selectors: @eN, #automationId, .className, or name)
agent-rdp automate click "#SaveButton"    # Click button
agent-rdp automate click "@e5"            # Click by ref number
agent-rdp automate click "@e5" -d         # Double-click (for file list items)
agent-rdp automate select "@e10"          # Select item (SelectionItemPattern)
agent-rdp automate select "@e5" --item "Option 1"  # Select item by name in container
agent-rdp automate toggle "@e7"           # Toggle checkbox (TogglePattern)
agent-rdp automate toggle "@e7" --state on  # Set specific state
agent-rdp automate expand "@e3"           # Expand menu/tree (ExpandCollapsePattern)
agent-rdp automate collapse "@e3"         # Collapse menu/tree
agent-rdp automate context-menu "@e5"     # Open context menu (Shift+F10)
agent-rdp automate focus <selector>       # Focus element
agent-rdp automate get <selector>         # Get element properties

# Text input
agent-rdp automate fill <selector> "text" # Clear and fill text (ValuePattern)
agent-rdp automate clear <selector>       # Just clear

# Scrolling
agent-rdp automate scroll <selector> --direction down --amount 3

# Window operations
agent-rdp automate window list
agent-rdp automate window focus "~*Notepad*"
agent-rdp automate window maximize
agent-rdp automate window minimize
agent-rdp automate window restore
agent-rdp automate window close "~*Notepad*"

# Run commands/apps (best way to open apps)
agent-rdp automate run "notepad.exe"                                        # Open Notepad
agent-rdp automate run "Start-Process ms-settings:" --wait                  # Open Settings
agent-rdp automate run "calc.exe"                                           # Open Calculator
agent-rdp automate run "Get-Process" --wait --process-timeout 5000          # With 5s timeout

# Wait for element
agent-rdp automate wait-for <selector> --timeout 5000
agent-rdp automate wait-for <selector> --state visible

# Status
agent-rdp automate status
```

**Selector syntax:**
- `@e5` or `@5` - Reference number from snapshot (e prefix recommended)
- `#SaveButton` - Automation ID
- `.Edit` - Win32 class name
- `~*pattern*` - Name with wildcard
- `File` - Element name (exact match)

**Snapshot output format:**
```
- Window "Notepad" [ref=e1, id=Notepad]
  - MenuBar "Application" [ref=e2]
    - MenuItem "File" [ref=e3]
  - Edit "Text Editor" [ref=e5, value="Hello"]
```

## JSON output

Add `--json` for machine-readable output:
```bash
agent-rdp --json clipboard get
agent-rdp --json session info
agent-rdp --json automate snapshot
```

## Example: Open PowerShell and run command

```bash
agent-rdp connect --host 192.168.1.100 -u Admin -p secret
agent-rdp wait 3000                       # Wait for desktop
agent-rdp keyboard press "win+r"          # Open Run dialog
agent-rdp wait 1000
agent-rdp keyboard type "powershell"
agent-rdp keyboard press enter
agent-rdp wait 2000                       # Wait for PowerShell
agent-rdp keyboard type "Get-Process"
agent-rdp keyboard press enter
agent-rdp screenshot --output result.png
agent-rdp disconnect
```

## Example: File transfer via mapped drive

```bash
# Connect with local directory mapped
agent-rdp connect --host 192.168.1.100 -u Admin -p secret --drive /tmp/transfer:Transfer

# On Windows, access files at \\tsclient\Transfer
agent-rdp keyboard press "win+r"
agent-rdp wait 500
agent-rdp keyboard type "\\\\tsclient\\Transfer"
agent-rdp keyboard press enter
```

## Example: Automate Notepad with UI Automation

```bash
# Connect with automation enabled
agent-rdp connect --host 192.168.1.100 -u Admin -p secret --enable-win-automation

# Open Notepad
agent-rdp automate run "notepad.exe"
agent-rdp wait 2000

# Get accessibility snapshot (refs are always included)
agent-rdp automate snapshot -i            # Interactive elements only

# Type text into the edit control (use ref from snapshot)
agent-rdp automate fill "@e5" "Hello from automation!"

# Use File menu to save - expand menu, then invoke menu item
agent-rdp automate expand "File"          # Expand menu (ExpandCollapsePattern)
agent-rdp wait 500
agent-rdp automate click "Save As..."     # Click menu item

# Wait for Save dialog
agent-rdp automate wait-for "#FileNameControlHost" --timeout 5000

# Fill filename and save
agent-rdp automate fill "#FileNameControlHost" "test.txt"
agent-rdp automate click "#1"             # Click Save button
```

## Environment variables

```bash
export AGENT_RDP_HOST=192.168.1.100
export AGENT_RDP_PORT=3389
export AGENT_RDP_USERNAME=Administrator
export AGENT_RDP_PASSWORD=secret
export AGENT_RDP_SESSION=default
agent-rdp connect    # Uses env vars for connection
```

## Debugging with WebSocket streaming

```bash
# Enable streaming viewer on port 9224
agent-rdp --stream-port 9224 connect --host 192.168.1.100 -u Admin -p secret

# Open web viewer in browser
agent-rdp view --port 9224

# Or manually access WebSocket at ws://localhost:9224 (broadcasts JPEG frames)
```

## Tips

**Prefer `automate fill` over `keyboard type`** when automation is enabled—it's lossless (no dropped characters) and faster.

### Opening applications

Use `automate run` to launch apps directly:
```bash
agent-rdp automate run "notepad.exe"
agent-rdp automate run "calc.exe"
agent-rdp automate run "Start-Process ms-settings:" --wait   # Settings
agent-rdp automate run "explorer.exe C:\\"                   # File Explorer
```

## Limitations

**IMPORTANT: Read these limitations carefully before attempting automation tasks.**

### UI Automation cannot access WebViews
- The Windows Start menu search, Edge browser content, Electron app content, and other WebView-based UIs are NOT accessible via `automate snapshot`.
- **Workaround**: Use `Win+R` (Run dialog) or `automate run` to launch programs directly instead of navigating through the Start menu.

### UI Automation cannot handle UAC dialogs
- User Account Control elevation prompts run on a secure desktop isolated from UI Automation.
- UAC dialogs will NOT appear in `automate snapshot` output.
- **Workaround**: Use `locate` command (OCR) to find button text and `mouse click` to interact. This is unreliable but may work for simple Yes/No dialogs.

### OCR (`locate`) is not highly reliable
- The `locate` command uses OCR which can misread characters, miss text entirely, or return imprecise coordinates.
- Use it as a last resort when UI Automation cannot access elements.
- Always verify coordinates before clicking critical buttons.

### DO NOT estimate coordinates from screenshots (Claude only)
- **Claude models in non-computer-use mode (like Claude Code) are very bad at pixel counting.**
- Do NOT look at a screenshot and try to guess coordinates - the estimates will likely be wrong.
- **Note**: Gemini models are generally good at pixel coordinate estimation.
- If you need vision-based coordinate detection with Claude, the user must implement a harness using Claude's [Computer Use Tool](https://docs.anthropic.com/en/docs/agents-and-tools/computer-use).

### Recommended workflow when UI Automation fails
1. First, always try `automate snapshot` (with and without `-i` flag)
2. If element not found, try `locate "text"` to find via OCR
3. Use coordinates from `locate` output with `mouse click`
4. **Never** estimate coordinates by looking at screenshots
