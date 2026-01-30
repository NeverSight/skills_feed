---
name: browser-control
description: Full browser control for authenticated web interactions using Playwright scripts
triggers:
  - "check availability"
  - "search for"
  - "log into"
  - "browse to"
  - "look up prices"
  - "check points"
  - "find deals"
  - "scrape"
  - "get current price"
  - "check hotel"
  - "check flight"
allowed-tools: Bash, Read
version: 0.1.0
---

# Browser Control Skill

Full browser automation for travel research requiring authentication or complex interactions.

## When to Activate

Use this skill when you need to:
- Access authenticated pages (Marriott, Alaska Airlines accounts)
- Check real-time availability and prices
- Scrape forum threads (FlyerTalk, Reddit)
- Interact with JavaScript-heavy travel sites
- Fill forms or perform searches on websites

## Architecture

**Script-based approach** - No MCP overhead. Scripts load only when needed.

### Prerequisites

1. **Geoffrey Chrome Profile** must be running with remote debugging:
   ```bash
   ./scripts/launch-chrome.sh
   ```

2. **Profile must have logins saved** for:
   - Marriott Bonvoy
   - Alaska Airlines Mileage Plan
   - FlyerTalk
   - TripAdvisor
   - Reddit

## Available Scripts

All scripts are in `./scripts/` and use Playwright connecting via CDP.

| Script | Purpose | Usage |
|--------|---------|-------|
| `launch-chrome.sh` | Start Geoffrey Chrome profile | `./scripts/launch-chrome.sh` |
| `navigate.js` | Navigate to URL and get page content | `bun scripts/navigate.js <url>` |
| `screenshot.js` | Take screenshot of page | `bun scripts/screenshot.js <url> [output] [--full]` |
| `extract.js` | Extract text/data from page | `bun scripts/extract.js <url> <selector> [--all]` |
| `interact.js` | Click, type, select on page | `bun scripts/interact.js <url> <action> <selector> [value]` |
| `search.js` | Search travel sites | `bun scripts/search.js <site> <query>` |

## Usage Examples

### Check Marriott Points Availability
```bash
# Navigate to Marriott search
bun scripts/navigate.js "https://www.marriott.com/search/default.mi"

# Or use the search script
bun scripts/search.js marriott "Westin Rusutsu February 2026"
```

### Get FlyerTalk Thread Content
```bash
bun scripts/extract.js "https://www.flyertalk.com/forum/thread-url" ".post-content"
```

### Screenshot Hotel Page
```bash
bun scripts/screenshot.js "https://www.marriott.com/hotels/travel/ctswi-the-westin-rusutsu-resort/" rusutsu.png
```

## Screenshot Protection & Lazy-Loading

**Auto-Resize Protection (ALL screenshots):**
- Post-capture resize using Sharp to max 7500px per dimension
- Maintains aspect ratio, prevents Claude Code API crashes
- Every screenshot guaranteed `safeToRead: true`

**Lazy-Loading Limitation (AirBnB, dynamic sites):**
- Sites with lazy-loading show grey placeholders in fullPage mode
- Images only load when scrolled into viewport
- **Solution**: Use viewport screenshots (no --full flag) or `screenshot-current.js`

```bash
# For lazy-loading sites, screenshot current viewport
bun scripts/screenshot-current.js /tmp/output.png

# Or navigate + viewport screenshot
bun scripts/screenshot.js "https://airbnb.com/..." /tmp/output.png
```

Example output:
```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Example Page",
  "screenshot": "/tmp/screenshot.png",
  "dimensions": { "width": 1920, "height": 1080 },
  "originalDimensions": { "width": 1920, "height": 1080 },
  "scaled": false,
  "safeToRead": true,
  "timestamp": "2025-11-28T..."
}
```

## Connection Details

Scripts connect to Chrome via Chrome DevTools Protocol (CDP):
- **URL**: `http://127.0.0.1:9222`
- **Profile**: `~/.chrome-geoffrey`

## Error Handling

If scripts fail to connect:
1. Ensure Chrome is running with `./scripts/launch-chrome.sh`
2. Check port 9222 is not in use: `lsof -i :9222`
3. Kill existing Chrome debugger: `pkill -f "remote-debugging-port"`

## Output Format

All scripts return JSON:
```json
{
  "success": true,
  "url": "https://example.com",
  "title": "Page Title",
  "content": "Extracted content or action result",
  "timestamp": "2025-11-22T..."
}
```

## Limitations

- Requires Geoffrey Chrome profile to be running
- Cannot bypass CAPTCHAs (uses real browser fingerprint to avoid most)
- Heavy sites may be slow
- Some sites block automation despite real browser

## Future Enhancements

- Add cookie/session export for headless runs
- 1Password CLI integration for credential rotation
- Parallel page operations
- Browser-Use (Python) for complex visual tasks
