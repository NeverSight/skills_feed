---
name: agent-browser
description: Browser automation for web tasks - scraping, form filling, testing, screenshots, data extraction. Use when tasks involve web pages, URLs, login flows, or web interaction.
---

# Browser Automation via `cloudrouter browser`

Automate browser interactions in cloud sandboxes. `cloudrouter browser` wraps [agent-browser](https://github.com/vercel-labs/agent-browser) and runs commands inside the sandbox via SSH.

**Prerequisite:** You need a running cloudrouter sandbox. Get the sandbox ID from `cloudrouter ls` or create one with `cloudrouter start .`.

## Core Workflow

Always follow this pattern: **Open -> Snapshot -> Interact -> Re-snapshot**

```bash
cloudrouter browser open <id> "https://example.com"
cloudrouter browser snapshot -i <id>         # -i = interactive elements only
cloudrouter browser click <id> @e5           # Click element ref
cloudrouter browser fill <id> @e3 "text"     # Fill input
cloudrouter browser snapshot -i <id>         # Re-snapshot after change
```

## Essential Commands

### Navigation

```bash
cloudrouter browser open <id> <url>          # Navigate to URL
cloudrouter browser back <id>                # Go back
cloudrouter browser forward <id>             # Go forward
cloudrouter browser reload <id>              # Refresh page
cloudrouter browser url <id>                 # Get current URL
cloudrouter browser title <id>               # Get page title
```

### Inspection

```bash
cloudrouter browser snapshot -i <id>         # Interactive elements only (RECOMMENDED)
cloudrouter browser snapshot <id>            # Full accessibility tree
cloudrouter browser snapshot -c <id>         # Compact output
cloudrouter browser screenshot <id>          # Screenshot (base64 to stdout)
cloudrouter browser screenshot <id> out.png  # Save screenshot to file
cloudrouter browser screenshot --full <id>   # Full page screenshot
cloudrouter browser eval <id> "document.title"  # Run JavaScript
```

### Interaction

```bash
cloudrouter browser click <id> @e1           # Click element
cloudrouter browser dblclick <id> @e1        # Double-click
cloudrouter browser fill <id> @e2 "text"     # Clear input and type text
cloudrouter browser type <id> @e2 "text"     # Type without clearing (appends)
cloudrouter browser press <id> Enter         # Press key (Enter, Tab, Escape, etc.)
cloudrouter browser hover <id> @e5           # Hover over element
cloudrouter browser focus <id> @e3           # Focus element
cloudrouter browser scroll <id> down         # Scroll down (default pixels)
cloudrouter browser scroll <id> down 500     # Scroll down 500px
cloudrouter browser scroll <id> up           # Scroll up
cloudrouter browser scrollintoview <id> "#element"  # Scroll into view (CSS selector only, NOT @e refs)
cloudrouter browser select <id> @e7 "value"  # Select dropdown option
cloudrouter browser check <id> @e8           # Check checkbox
cloudrouter browser uncheck <id> @e9         # Uncheck checkbox
cloudrouter browser upload <id> @e10 /path   # Upload file
cloudrouter browser drag <id> @e1 @e2        # Drag and drop
cloudrouter browser wait <id> @e3            # Wait for element to appear
cloudrouter browser wait <id> 2000           # Wait milliseconds
```

### Get Information

```bash
cloudrouter browser get-text <id> @e1        # Get element text
cloudrouter browser get-value <id> @e2       # Get input value
cloudrouter browser get-attr <id> @e3 href   # Get attribute
cloudrouter browser get-html <id> @e4        # Get innerHTML
cloudrouter browser get-count <id> ".item"   # Count matching elements
cloudrouter browser is-visible <id> @e1      # Check visibility
cloudrouter browser is-enabled <id> @e1      # Check if enabled
cloudrouter browser is-checked <id> @e1      # Check if checked
```

### Semantic Locators (alternative to refs)

When refs are unreliable on dynamic pages:

```bash
cloudrouter browser find <id> text "Sign In" click                 # By visible text
cloudrouter browser find <id> label "Email" fill "user@test.com"   # By label
cloudrouter browser find <id> placeholder "Search" type "query"    # By placeholder
cloudrouter browser find <id> testid "submit-btn" click            # By data-testid
```

> **Note:** `find <id> role button click` finds the FIRST button on the page — it cannot filter by name. Use `find <id> text "Button Name" click` to target a specific button. There is no `--name` flag.

### JavaScript & Debugging

```bash
cloudrouter browser eval <id> "document.title"          # Evaluate JS
cloudrouter browser console <id>                        # View console output
cloudrouter browser errors <id>                         # View JS errors
```

### Tabs & Frames

```bash
cloudrouter browser tab-list <id>                       # List tabs
cloudrouter browser tab-new <id> "https://..."          # New tab
cloudrouter browser tab-switch <id> 2                   # Switch tab
cloudrouter browser tab-close <id>                      # Close tab
cloudrouter browser frame <id> "#iframe"                # Switch to iframe
cloudrouter browser frame <id> main                     # Back to main
```

### Cookies & Storage

```bash
cloudrouter browser cookies <id>                        # List cookies
cloudrouter browser cookies-set <id> name value         # Set cookie
cloudrouter browser cookies-clear <id>                  # Clear cookies
cloudrouter browser storage-local <id>                  # Get localStorage
cloudrouter browser storage-local-set <id> key value    # Set localStorage
cloudrouter browser storage-local-clear <id>            # Clear localStorage
```

### State Management

```bash
cloudrouter browser state-save <id> /tmp/auth.json      # Save cookies + storage
cloudrouter browser state-load <id> /tmp/auth.json      # Restore state
```

### Browser Settings

```bash
cloudrouter browser set-viewport <id> 1920 1080         # Set viewport
cloudrouter browser set-device <id> "iPhone 14"         # Emulate device
cloudrouter browser set-geo <id> 37.77 -122.42          # Set geolocation
cloudrouter browser set-offline <id> on                 # Toggle offline
cloudrouter browser set-media <id> dark                 # Color scheme
```

### Network Interception

```bash
cloudrouter browser network-route <id> "**/api/*"       # Intercept requests
cloudrouter browser network-route <id> "**/ads/*" --abort  # Block requests
cloudrouter browser network-unroute <id>                # Remove routes
cloudrouter browser network-requests <id>               # List requests
```

### Dialogs

```bash
cloudrouter browser dialog-accept <id>                  # Accept alert/confirm
cloudrouter browser dialog-accept <id> "answer"         # Accept prompt with text
cloudrouter browser dialog-dismiss <id>                 # Dismiss dialog
```

## Element Selectors

- **Element refs** from snapshot: `@e1`, `@e2`, `@e3`... (preferred)
- **CSS selectors**: `#id`, `.class`, `button[type="submit"]`

Snapshot output shows `[ref=e1]` — use as `@e1` in commands.

## Common Patterns

### Login Flow

```bash
cloudrouter browser open <id> "https://app.example.com/login"
cloudrouter browser snapshot -i <id>
# → @e1 [input] Email, @e2 [input] Password, @e3 [button] Sign In
cloudrouter browser fill <id> @e1 "user@example.com"
cloudrouter browser fill <id> @e2 "password123"
cloudrouter browser click <id> @e3
cloudrouter browser wait <id> 2000
cloudrouter browser snapshot -i <id>         # Verify login success
cloudrouter browser screenshot <id> /tmp/result.png
```

### Form Submission

```bash
cloudrouter browser open <id> "https://example.com/contact"
cloudrouter browser snapshot -i <id>
cloudrouter browser fill <id> @e1 "John Doe"
cloudrouter browser fill <id> @e2 "john@email.com"
cloudrouter browser fill <id> @e3 "Hello world"
cloudrouter browser click <id> @e4           # Submit
cloudrouter browser wait <id> 2000
cloudrouter browser snapshot -i <id>         # Verify submission
```

### Data Extraction

```bash
cloudrouter browser open <id> "https://example.com/products"
cloudrouter browser snapshot <id>            # Full tree for structure
cloudrouter browser get-text <id> @e5        # Extract specific text
cloudrouter browser eval <id> "JSON.stringify([...document.querySelectorAll('.product')].map(p => p.textContent))"
```

### Multi-page Navigation

```bash
cloudrouter browser open <id> "https://example.com"
cloudrouter browser snapshot -i <id>
cloudrouter browser click <id> @e3           # Click a link
cloudrouter browser wait <id> 2000           # Wait for page load
cloudrouter browser snapshot -i <id>         # ALWAYS re-snapshot after navigation
```

### Auth State Persistence

```bash
# Login once and save state
cloudrouter browser open <id> "https://app.example.com/login"
cloudrouter browser snapshot -i <id>
cloudrouter browser fill <id> @e1 "user@example.com"
cloudrouter browser fill <id> @e2 "password"
cloudrouter browser click <id> @e3
cloudrouter browser wait <id> 2000
cloudrouter browser state-save <id> /tmp/auth.json

# Restore in future sessions
cloudrouter browser state-load <id> /tmp/auth.json
cloudrouter browser open <id> "https://app.example.com/dashboard"
```

## Critical Rules

1. **Flags go BEFORE the sandbox ID.** `cloudrouter browser snapshot -i <id>` works. `cloudrouter browser snapshot <id> -i` silently returns empty/wrong results.

2. **ALWAYS re-snapshot after navigation or clicks.** Page content changes, refs become stale.

3. **Use `-i` flag** for snapshots — interactive elements only, much more efficient.

4. **Don't mix snapshot modes.** Full `snapshot` and `snapshot -i` assign DIFFERENT ref numbers. Stick to one mode (use `-i`).

5. **Use `fill` not `type`** for form fields. `fill` clears first; `type` appends.

6. **Refs are temporary.** They reset after each snapshot. Always use fresh refs.

7. **Verify before interacting.** Check snapshot output to confirm you have the right element.

8. **Handle loading states.** If elements are missing, `wait` and re-snapshot.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Element not found / wrong element | Re-snapshot with `-i`, refs are stale |
| `snapshot <id> -i` returns empty | Put flags BEFORE id: `snapshot -i <id>` |
| Click doesn't work | Try `hover` first, then `click` |
| Page not loading | Check URL with `cloudrouter browser url <id>` |
| Browser not ready | Wait a few seconds after sandbox creation, retry |
| Refs differ between snapshots | Don't mix full and `-i` snapshots |
| Form field has old text | Use `fill` (clears first) instead of `type` |
| `find ... role button click` clicks wrong button | Use `find ... text "Button Name" click` instead |
| `find ... --name "X"` fails | There is no `--name` flag — use `text` locator |
| `npm install` EACCES error | Run `cloudrouter ssh <id> "sudo chown -R 1000:1000 /home/user/.npm"` first |
| `scrollintoview @e1` fails with "Unsupported token" | `scrollintoview` and `highlight` only accept CSS selectors (`"#id"`, `".class"`), NOT `@e` refs |
| `pkill -f` kills SSH session (exit 143/255) | `pkill -f` pattern may match the SSH session. Just run another command to recover |
| `pdf` saves to remote, not local | File saves inside sandbox (e.g. `/tmp/page.pdf`). Use `cloudrouter download` to retrieve |
| `storage-local <id> key` shows "Done" not value | Use `eval <id> "localStorage.getItem('key')"` to get a specific localStorage value |
| Stale ref error: "Action timed out" | Always re-snapshot after clicks/form submits that change the DOM |
