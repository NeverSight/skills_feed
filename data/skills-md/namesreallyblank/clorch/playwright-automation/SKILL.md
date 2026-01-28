---
name: playwright-automation
description: Browser automation via Playwright MCP - screenshots, interactions, DOM inspection
impact: HIGH
version: 1.0.0
---

# Playwright Automation

Browser automation for Clorch using Playwright MCP with persistent sessions.

## Configuration

Current setup (`~/.claude/.mcp.json`):
```json
{
  "playwright": {
    "command": "npx",
    "args": [
      "@playwright/mcp",
      "--user-data-dir", "~/.claude/browser-profile",
      "--caps", "vision,pdf",
      "--save-trace",
      "--output-dir", "~/.claude/browser-output"
    ]
  }
}
```

### Key Settings

| Flag | Purpose |
|------|---------|
| `--user-data-dir` | Persistent sessions (logins survive restarts) |
| `--caps vision,pdf` | Enable screenshots and PDF generation |
| `--save-trace` | Record trace for debugging |
| `--output-dir` | Where traces/videos/screenshots go |

---

## Core Tools

### Navigation
```
mcp__playwright__browser_navigate(url)     # Go to URL
mcp__playwright__browser_navigate_back()   # Go back
mcp__playwright__browser_tabs(action)      # list/new/close/select tabs
```

### DOM Inspection
```
mcp__playwright__browser_snapshot()        # Accessibility tree (PREFERRED)
mcp__playwright__browser_take_screenshot() # Visual capture
```

**Always prefer `browser_snapshot`** over screenshots for element interaction - it returns the accessibility tree with refs for clicking.

### Interaction
```
mcp__playwright__browser_click(element, ref)           # Click element
mcp__playwright__browser_type(element, ref, text)      # Type into input
mcp__playwright__browser_fill_form(fields)             # Fill multiple fields
mcp__playwright__browser_select_option(element, ref, values)  # Dropdown
mcp__playwright__browser_hover(element, ref)           # Hover
mcp__playwright__browser_drag(startRef, endRef)        # Drag and drop
mcp__playwright__browser_press_key(key)                # Keyboard key
```

### Advanced
```
mcp__playwright__browser_evaluate(function)            # Run JS on page
mcp__playwright__browser_file_upload(paths)            # Upload files
mcp__playwright__browser_handle_dialog(accept)         # Handle alerts
mcp__playwright__browser_wait_for(text/time)           # Wait conditions
mcp__playwright__browser_console_messages()            # Get console logs
mcp__playwright__browser_network_requests()            # Get network activity
mcp__playwright__browser_run_code(code)                # Run Playwright code
```

---

## Persistent Sessions

### First-Time Login

1. Navigate to the service (Twitter, Google, etc.)
2. Use `browser_snapshot` to see the login form
3. Fill credentials with `browser_type` / `browser_fill_form`
4. Submit and complete any 2FA
5. Session is now saved in `~/.claude/browser-profile`

### Subsequent Sessions

Sessions persist automatically. When you navigate to Twitter, you'll be logged in.

### Logout Protection

To prevent accidental logout:
- Don't click "Sign Out" links
- Be careful with `browser_click` on unknown elements

---

## Workflow Patterns

### Research Pattern
```
1. browser_navigate(url)
2. browser_snapshot() - get page structure
3. browser_click() on relevant links
4. browser_snapshot() - read content
5. Repeat as needed
```

### Form Filling Pattern
```
1. browser_navigate(url)
2. browser_snapshot() - identify form fields
3. browser_fill_form([
     {name: "email", type: "textbox", ref: "...", value: "..."},
     {name: "password", type: "textbox", ref: "...", value: "..."}
   ])
4. browser_click(submit_button)
```

### Screenshot Documentation
```
1. browser_navigate(url)
2. browser_take_screenshot(filename: "page.png")
3. browser_take_screenshot(fullPage: true, filename: "full.png")
4. browser_take_screenshot(ref: "header", element: "Header", filename: "header.png")
```

---

## Authenticated Services

Once logged in, Clorch can:

| Service | Capabilities |
|---------|--------------|
| **Twitter/X** | Read timeline, search tweets, view profiles |
| **Google** | Access Gmail, Drive, Calendar, Search with personalization |
| **GitHub** | View private repos, notifications, settings |
| **LinkedIn** | View profiles, messages, network |

### Security Notes

- Browser profile at `~/.claude/browser-profile` contains session tokens
- Protect this directory (don't share, add to .gitignore)
- Be careful with write operations (posting, deleting)

---

## Debugging

### Traces
Traces are saved to `~/.claude/browser-output`. Open with:
```bash
npx playwright show-trace ~/.claude/browser-output/trace.zip
```

### Console Messages
```
mcp__playwright__browser_console_messages(level: "error")
```

### Network Issues
```
mcp__playwright__browser_network_requests(includeStatic: false)
```

---

## Advanced Configuration

### Device Emulation
Add to MCP args:
```
"--device", "iPhone 15"
"--viewport-size", "1280x720"
```

### Geolocation
```
"--grant-permissions", "geolocation"
```
Then use `browser_evaluate` to set location.

### Proxy
```
"--proxy-server", "http://proxy:8080"
"--proxy-bypass", ".local,localhost"
```

### Headless Mode
```
"--headless"
```
Note: Headless mode won't show browser window (useful for background automation).

---

## Best Practices

1. **Use snapshot, not screenshot** for element interaction
2. **Wait for content** before interacting: `browser_wait_for(text: "...")`
3. **Handle dynamic content** by checking for loading indicators
4. **Preserve sessions** by avoiding logout actions
5. **Check network** if pages seem broken: `browser_network_requests()`
