---
name: browse
description: Control Chrome browser via CLI for testing, automation, and debugging. Use when the user needs browser automation, screenshots, form filling or page inspection.
---

# Browse Browser Automation

Control Chrome browser via CLI.

## CLI Quick Reference

```bash
browse --help                    # Full help
browse <group>                   # Group help (tab, scroll, page, wait, dialog, emulate, form, perf)
browse --list                    # All 60+ tools
browse --find <term>             # Search tools
```

## Core Workflow

```bash
# 1. Navigate to page
browse navigate "https://example.com"

# 2. Read page to get element refs
browse page.read

# 3. Click by ref or coordinates
browse click --ref "e1"
browse click --x 100 --y 200

# 4. Type text
browse type --text "hello"

# 5. Screenshot
browse screenshot --output /tmp/shot.png
```

## Tab Management

```bash
browse tab.list
browse tab.new "https://google.com"
browse tab.switch 12345
browse tab.close 12345

# Named tabs (aliases)
browse tab.name myapp            # Name current tab
browse tab.switch myapp          # Switch by name
browse tab.named                 # List named tabs
```

## Window Management

```bash
browse window.list                              # List all windows
browse window.new                               # New window
browse window.new --url "https://example.com"   # New window with URL
browse window.new --incognito                   # New incognito window
browse window.focus 12345                       # Focus window by ID
browse window.close 12345                       # Close window
browse window.resize --width 1920 --height 1080 # Resize current window
```

## Input Methods

```bash
# CDP method (real events) - default
browse type --text "hello"
browse click --x 100 --y 200

# JS method (DOM manipulation) - for contenteditable
browse type --text "hello" --selector "#input" --method js

# Keys
browse key Enter
browse key "cmd+a"
browse key.repeat --key Tab --count 5           # Repeat key presses
```

## Page Inspection

```bash
browse page.read                 # Accessibility tree with refs (viewport only)
browse page.read --ref e5        # Get specific element details
browse page.read --all           # All elements (may hit 50K char limit on large pages)
browse page.text                 # Full page text content (no limit)
browse page.state                # Modals, loading state, scroll info
```

**When to use which:**
- **`page.text`** - Get full page text content. No size limit. Best for reading/understanding page content.
- **`page.read`** - Get element refs for visible viewport. Use when you need to interact (click, type).
- **`page.read --all`** - All elements with refs. Can fail on large pages (50K char limit).

**Note:** `page.read` returns only elements in the visible viewport. Refs remain valid for off-screen elements - you can still `click e5` even after scrolling. Use `scroll.to --ref e5` to bring an element into view.

## Scrolling

```bash
browse scroll down               # Scroll down (default amount)
browse scroll up                 # Scroll up
browse scroll down --amount 5    # Scroll down more (1-10)
browse scroll.bottom             # Scroll to bottom of page
browse scroll.top                # Scroll to top of page
browse scroll.to --ref e5        # Scroll element into view
browse scroll.info               # Get scroll position
```

## Waiting

```bash
browse wait 2                    # Wait 2 seconds
browse wait.element ".loaded"    # Wait for element
browse wait.network              # Wait for network idle
browse wait.url "/success"       # Wait for URL pattern
browse wait.dom --stable 100     # Wait for DOM stability
browse wait.load                 # Wait for page load complete
```

## Dialog Handling

```bash
browse dialog.info               # Get current dialog type/message
browse dialog.accept             # Accept (OK)
browse dialog.accept --text "response"  # Accept prompt with text
browse dialog.dismiss            # Dismiss (Cancel)
```

## Device/Network Emulation

```bash
# Network throttling
browse emulate.network slow-3g   # Presets: slow-3g, fast-3g, 4g, offline
browse emulate.network reset     # Disable throttling

# CPU throttling  
browse emulate.cpu 4             # 4x slower
browse emulate.cpu 1             # Reset

# Device emulation
browse emulate.device "iPhone 14"
browse emulate.device --list     # List available devices

# Geolocation
browse emulate.geo --lat 37.7749 --lon -122.4194
browse emulate.geo --clear
```

## Form Automation

```bash
browse page.read                 # Get element refs first

# Fill by ref
browse form.fill --data '[{"ref":"e1","value":"John"},{"ref":"e2","value":"john@example.com"}]'

# Checkboxes: true/false
browse form.fill --data '[{"ref":"e7","value":true}]'
```

## File Upload

```bash
browse upload --ref e5 --files "/path/to/file.txt"
browse upload --ref e5 --files "/path/file1.txt,/path/file2.txt"
```

## Network Inspection

```bash
browse network                   # List captured requests
browse network --stream          # Real-time network events
browse network.body --id "req-123"  # Get response body
browse network.clear             # Clear captured requests
```

## Console

```bash
browse console                   # Get console messages
browse console --stream          # Real-time console
browse console --stream --level error  # Errors only
```

## JavaScript Execution

```bash
browse js "return document.title"
browse js "document.querySelector('.btn').click()"
```

## Iframe Handling

```bash
browse frame.list                # List frames with IDs
browse frame.js --id "FRAME_ID" --code "return document.title"
```

## Performance

```bash
browse perf.metrics              # Current metrics snapshot
browse perf.start                # Start trace
browse perf.stop                 # Stop and get results
```

## Screenshots

```bash
browse screenshot                           # To stdout (base64)
browse screenshot --output /tmp/shot.png    # Save to file
browse screenshot --selector ".card"        # Element only
browse screenshot --full-page               # Full page scroll capture
```

## Cookies & Storage

```bash
browse cookies                   # List cookies for current page
browse cookies --domain .google.com
browse cookie.set --name "token" --value "abc123"
browse cookie.delete --name "token"
```

## History & Bookmarks

```bash
browse history --query "github" --max 20
browse bookmarks --query "docs"
browse bookmark.add --url "https://..." --title "My Bookmark"
```

## Health Checks & Smoke Tests

```bash
browse health --url "http://localhost:3000"
browse smoke --urls "http://localhost:3000" "http://localhost:3000/about"
browse smoke --urls "..." --screenshot /tmp/smoke
```

## Error Diagnostics

```bash
# Auto-capture screenshot + console on failure
browse wait.element ".missing" --auto-capture --timeout 2000
# Saves to /tmp/browse-error-*.png
```

## Common Options

```bash
--tab-id <id>         # Target specific tab
--json                # Raw JSON output  
--auto-capture        # Screenshot + console on error
--timeout <ms>        # Override default timeout
```

## Tips

1. **First CDP operation is slow** (~5-8s) - debugger attachment overhead, subsequent calls fast
2. **Use refs from page.read** for reliable element targeting over CSS selectors
3. **JS method for contenteditable** - Modern editors (Notion, etc.) need `--method js`
4. **Named tabs for multi-step tasks** - `tab.name app` then `tab.switch app`
5. **Auto-capture for debugging** - `--auto-capture` saves diagnostics on failure
