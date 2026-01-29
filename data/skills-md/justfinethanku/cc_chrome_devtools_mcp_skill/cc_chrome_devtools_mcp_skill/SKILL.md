---
name: cc_chrome_devtools_mcp_skill
description: Comprehensive Chrome DevTools automation for performance testing, Core Web Vitals measurement (INP, LCP, CLS), network monitoring, accessibility validation, responsive testing, and browser automation. Uses Chrome DevTools Protocol via MCP to provide professional-grade web application testing, debugging, and analysis capabilities including performance tracing, HAR export, device emulation, and multi-page workflows.
---

# Chrome DevTools Testing Skill

## Overview

This skill enables automated Chrome browser testing and performance analysis using the Chrome DevTools Protocol (CDP) via the chrome-devtools-mcp server. It provides access to 27 professional-grade tools for web application testing, performance measurement, accessibility validation, and browser automation.

**Key capabilities:**
- Performance analysis with Core Web Vitals (INP, LCP, CLS)
- Network monitoring and HAR export
- Accessibility tree inspection
- Responsive design testing
- Browser automation (form filling, navigation, interaction)
- Multi-tab and frame management
- Device and network condition emulation

**Browser support:** Chrome/Chromium only (stable, beta, dev, canary channels)

**Node.js requirement:** v20.19 or newer

## Quick Start

### Installation

```bash
# Add to Claude Code via CLI
claude mcp add chrome-devtools npx chrome-devtools-mcp@latest

# Verify installation
claude mcp list
```

### Basic configuration

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true",
        "--viewport=1920x1080"
      ]
    }
  }
}
```

### Important notes

- Browser auto-starts on first tool use (not on MCP connection)
- Use `--isolated=true` for security (creates temporary user data directories that auto-cleanup)
- Default behavior shares user data directory across sessions and does NOT clear between runs
- All browser content is exposed to MCP clients - avoid sensitive data

## Current Core Web Vitals (as of March 12, 2024)

Three official metrics measured at **75th percentile** of page loads:

1. **Interaction to Next Paint (INP)** - Replaced FID on March 12, 2024
   - Good: ≤ 200ms
   - Measures: Input delay + processing time + presentation delay
   - Requires: Real user interactions (field data only)

2. **Largest Contentful Paint (LCP)**
   - Good: ≤ 2.5 seconds
   - Measures: Main content loading performance

3. **Cumulative Layout Shift (CLS)**
   - Good: ≤ 0.1
   - Measures: Visual stability

**Total Blocking Time (TBT)** is NOT a Core Web Vital - it's a lab proxy metric for INP.

## Common Use Cases

### 1. Performance Testing Workflow

Measure Core Web Vitals and analyze performance bottlenecks:

```
1. Start performance trace: performance_start_trace
2. Navigate to target URL: navigate_page
3. Wait for page load: wait_for
4. Stop trace and get metrics: performance_stop_trace
5. Analyze specific insights: performance_analyze_insight
```

**Metrics captured:**
- INP (Interaction to Next Paint)
- LCP (Largest Contentful Paint) with breakdown
- CLS (Cumulative Layout Shift)
- TBT (Total Blocking Time - lab proxy)
- Document latency analysis

**Example:**
```
performance_start_trace with reload=true, autoStop=false
wait_for page to stabilize
performance_stop_trace
performance_analyze_insight with insightName="LCPBreakdown"
```

### 2. Network Monitoring and HAR Export

Capture all HTTP requests/responses with timing details:

```
1. Navigate to URL: navigate_page
2. List all network requests: list_network_requests
3. Get specific request details: get_network_request
```

**Captured data:**
- Headers, bodies, cookies
- Timing (DNS, connect, SSL, wait, receive)
- Resource types (document, stylesheet, image, script, xhr, fetch)
- Security details (protocol, cipher suite)

**Export as HAR:** Use list_network_requests to generate HTTP Archive v1.2 format

**Filter requests:**
```
list_network_requests with resourceTypes=["xhr", "fetch", "document"]
list_network_requests with pageSize=50, pageIdx=0
```

### 3. Accessibility Validation

Inspect accessibility tree for WCAG compliance:

```
1. Navigate to page: navigate_page
2. Take accessibility snapshot: take_snapshot
3. Interact with elements using UIDs
```

**Snapshot provides:**
- Unique element identifiers (UIDs)
- Accessibility roles, names, properties
- ARIA attributes and computed roles
- Screen reader compatibility analysis
- Semantic structure validation

**Example workflow:**
```
take_snapshot verbose=false (returns text-based a11y tree)
# Identify element UIDs from snapshot
click uid="element-123"
fill uid="input-456" value="test data"
```

### 4. Responsive Design Testing

Test across devices and network conditions:

```
1. Resize viewport: resize_page width=375 height=667
2. Emulate network: emulate_network throttlingOption="Slow 3G"
3. Emulate CPU: emulate_cpu throttlingRate=4
4. Take screenshot: take_screenshot fullPage=true
```

**Device emulation options:**
- Viewport dimensions and device scale factor
- Network conditions: Offline, Slow 3G, Fast 3G, Slow 4G, Fast 4G
- CPU throttling: 1-20x slowdown
- Touch emulation with max touch points

**Screenshot formats:** PNG, JPEG, WebP (with quality settings)

### 5. Browser Automation

Automated form filling, navigation, and interaction:

```
1. Take snapshot to get element UIDs: take_snapshot
2. Fill form fields: fill_form elements=[{uid, value}, ...]
3. Click buttons: click uid="submit-button"
4. Handle dialogs: handle_dialog action="accept"
5. Wait for results: wait_for text="Success"
```

**Interaction tools:**
- click (single/double-click)
- fill (input fields, textareas, selects)
- fill_form (multiple fields at once)
- hover (mouse hover)
- drag (drag-and-drop)
- upload_file (file inputs)
- handle_dialog (alerts, confirms, prompts)

**Navigation tools:**
- navigate_page (URLs, reload)
- navigate_page_history (back/forward)
- wait_for (text appearance, conditions)

### 6. Multi-Tab Management

Work with multiple pages and frames:

```
1. List open pages: list_pages
2. Create new page: new_page url="https://example.com"
3. Switch context: select_page pageIdx=1
4. Close pages: close_page pageIdx=2
```

**Frame handling:**
- Automatic attachment to child frames and workers
- Frame tree structure inspection
- Session persistence across navigation

## Advanced Workflows

### Performance Analysis with Device Emulation

```
1. resize_page width=390 height=844 (iPhone 14 Pro)
2. emulate_network throttlingOption="Fast 4G"
3. emulate_cpu throttlingRate=4
4. performance_start_trace reload=true
5. performance_stop_trace
6. performance_analyze_insight insightName="DocumentLatency"
```

### Network Analysis with Filtering

```
1. navigate_page url="https://example.com"
2. list_network_requests resourceTypes=["script", "fetch", "xhr"]
3. Filter by: pageSize=100, pageIdx=0, includePreservedRequests=true
4. get_network_request reqid=123 (detailed timing/headers/body)
```

### Accessibility Testing Pattern

```
1. navigate_page url="https://example.com"
2. take_snapshot verbose=true (full a11y tree with all properties)
3. Validate: roles, names, ARIA attributes, relationships
4. Test interactions: click, fill, keyboard navigation via UIDs
```

### Cross-Browser Viewport Testing

```
1. Define breakpoints: [320, 768, 1024, 1920]
2. For each breakpoint:
   - resize_page width=X height=Y
   - take_screenshot format="png" quality=90
   - take_snapshot (verify accessibility)
3. Compare layouts and a11y across sizes
```

## Complete Tool Reference

**27 tools available** across 6 categories:

**Input automation (8):** click, drag, fill, fill_form, handle_dialog, hover, press_key, upload_file

**Navigation (7):** close_page, list_pages, navigate_page, navigate_page_history, new_page, select_page, wait_for

**Emulation (3):** emulate_cpu, emulate_network, resize_page

**Performance (3):** performance_analyze_insight, performance_start_trace, performance_stop_trace

**Network (2):** get_network_request, list_network_requests

**Debugging (4):** evaluate_script, get_console_message, list_console_messages, take_screenshot, take_snapshot

For detailed tool parameters and examples, see TOOLS.md

For complete workflow patterns, see WORKFLOWS.md

For Core Web Vitals thresholds and measurement guide, see METRICS.md

## Configuration Options

### Connection flags

- `--browserUrl, -u <string>` - Connect to running Chrome instance (port forwarding)
- `--wsEndpoint, -w <string>` - WebSocket endpoint for Chrome connection
- `--wsHeaders <JSON>` - Custom headers for authenticated WebSocket connections

### Browser configuration

- `--headless <boolean>` - Run in headless mode (default: false)
- `--executablePath, -e <string>` - Path to custom Chrome executable
- `--channel <string>` - Chrome channel: stable, canary, beta, dev (default: stable)
- `--viewport <string>` - Initial viewport size (format: WIDTHxHEIGHT, e.g., 1280x720)

### Security and isolation

- `--isolated <boolean>` - **RECOMMENDED:** Creates temporary user-data-dir, auto-cleanup (default: false)
- `--user-data-dir <string>` - Custom user data directory
- `--acceptInsecureCerts <boolean>` - Ignore certificate errors (SECURITY RISK - dev/test only)

### Network

- `--proxyServer <string>` - Proxy server configuration

### Debugging

- `--logFile <string>` - Path for debug logs (set DEBUG=* env var for verbose logs)

### Additional

- `--chromeArg <string>` - Additional Chrome arguments (repeatable)

View all options: `npx chrome-devtools-mcp@latest --help`

## Production Configuration Examples

### Secure isolated testing

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--isolated=true",
        "--headless=true",
        "--viewport=1920x1080",
        "--channel=stable"
      ]
    }
  }
}
```

### Connect to external Chrome instance

```bash
# Launch Chrome with remote debugging
google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-profile

# Get WebSocket endpoint
curl http://127.0.0.1:9222/json/version | jq -r '.webSocketDebuggerUrl'
```

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--wsEndpoint=ws://127.0.0.1:9222/devtools/browser/<id>"
      ]
    }
  }
}
```

### Production with logging

```json
{
  "mcpServers": {
    "chrome-devtools-prod": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browserUrl=http://127.0.0.1:9222",
        "--isolated=true",
        "--logFile=/var/log/chrome-devtools-mcp.log"
      ],
      "env": {
        "DEBUG": "*"
      }
    }
  }
}
```

## Security Considerations

### Data exposure warning

**Official Chrome DevTools MCP security notice:**
> "chrome-devtools-mcp exposes content of the browser instance to the MCP clients allowing them to inspect, debug, and modify any data in the browser or DevTools. Avoid sharing sensitive or personal information that you don't want to share with MCP clients."

### Best practices

1. **Use isolated mode for sensitive workflows**
   - `--isolated=true` creates temporary user data directories
   - Automatically cleaned after browser closes
   - Prevents data persistence between sessions

2. **Certificate handling caution**
   - `--acceptInsecureCerts` is a security risk
   - Only use in development/testing environments
   - Never use with sensitive data

3. **User data directory management**
   - Default directory shared across all instances
   - Not cleared between runs
   - Contains cookies, cache, browsing history
   - Use `--isolated` or custom `--user-data-dir` for control

4. **WebSocket authentication**
   - Use `--wsHeaders` for authenticated connections
   - Example: `--wsHeaders='{"Authorization":"Bearer token"}'`
   - Only works with `--wsEndpoint`

## Technical Constraints

### Verified limitations

1. **Browser support:** Chrome/Chromium only (no Firefox, Safari, Edge legacy)

2. **Node.js requirement:** v20.19 or newer (latest maintenance LTS)

3. **Browser lifecycle:** Browser auto-starts on first tool use, NOT on MCP server connection

4. **Default persistence:** User data directory persists between runs unless `--isolated=true` is used

5. **Permission requirements:**
   - macOS Full Disk Access may be required for some MCP clients
   - Chrome needs permission to create its own sandboxes
   - May need to disable MCP client sandboxing or use external Chrome instance

6. **Screenshot formats:** Specified format (JPEG/PNG) for initial capture, final output uses WebP with PNG fallback

7. **Tool availability:** All 27 tools available immediately after connection; no progressive unlocking

## Resources and Documentation

### Official sources

- **GitHub Repository:** https://github.com/ChromeDevTools/chrome-devtools-mcp
- **npm Package:** https://www.npmjs.com/package/chrome-devtools-mcp
- **Chrome DevTools Protocol:** https://chromedevtools.github.io/devtools-protocol/

### Core Web Vitals

- **Web Vitals Overview:** https://web.dev/articles/vitals
- **INP Documentation:** https://web.dev/articles/inp
- **LCP Documentation:** https://web.dev/articles/lcp
- **CLS Documentation:** https://web.dev/articles/cls
- **INP Replacing FID (March 12):** https://web.dev/blog/inp-cwv-march-12

### Tools

- **PageSpeed Insights:** https://pagespeed.web.dev
- **Chrome User Experience Report:** https://developer.chrome.com/docs/crux
- **Lighthouse Documentation:** https://developer.chrome.com/docs/lighthouse

## Related Skill Files

- **WORKFLOWS.md** - Detailed workflow patterns and multi-step processes
- **METRICS.md** - Complete Core Web Vitals thresholds and measurement guide
- **TOOLS.md** - Comprehensive tool parameter reference and examples

## Version Information

- **MCP Server Version:** v0.5.1 (October 17, 2025)
- **Tool Count:** 27 tools
- **Core Web Vitals Update:** INP replaced FID on March 12, 2024
- **Current Metrics:** INP, LCP, CLS (TBT is lab proxy, not Core Web Vital)
