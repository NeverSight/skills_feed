---
name: dev-browser
description: Browser automation with persistent page state. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.
---

# Dev Browser Skill

Browser automation that maintains page state across script executions. Write small, focused scripts to accomplish tasks incrementally. Once you've proven out part of a workflow and there is repeated work to be done, you can write a script to do the repeated work in a single execution.

## Choosing Your Approach

- **Local/source-available sites**: Read the source code first to write selectors directly
- **Unknown page layouts**: Use `getAISnapshot()` to discover elements and `selectSnapshotRef()` to interact with them
- **Visual feedback**: Take screenshots to see what the user sees

## Setup

Two modes available. Ask the user if unclear which to use.

### Standalone Mode (Default)

Launches a new Chromium browser for fresh automation sessions.

```bash
./skills/dev-browser/server.sh &
```

**Options:**
- `--headless` - Run in headless mode (no visible browser window)
- `--stealth` - Enable anti-detection mode (default: **ON**)
- `--no-stealth` - Disable stealth mode (use plain browser)
- `--driver [playwright|patchright|auto]` - Choose browser driver (default: **auto**)
  - `auto` - Auto-install and use patchright, fallback to playwright with patches
  - `patchright` - Force use of patchright
  - `playwright` - Use standard playwright
- `--no-flaresolverr` - Disable FlareSolverr auto-start (default: **enabled** if Docker available)
- `--stop` - Stop all dev-browser services and cleanup
- `--help` - Show help message

**Wait for the `Ready` message before running scripts.**

By default, the server automatically:
1. **Installs Patchright** (if not present) for stealth automation
2. **Enables stealth mode** with browser args and runtime patches
3. **Starts FlareSolverr** Docker container for Cloudflare bypass (requires Docker)

To disable automatic features:
```bash
# Disable stealth entirely
./skills/dev-browser/server.sh --no-stealth &

# Disable FlareSolverr auto-start
./skills/dev-browser/server.sh --no-flaresolverr &

# Use plain Playwright without anti-detection
./skills/dev-browser/server.sh --no-stealth --driver playwright &
```

**Examples:**

```bash
# Default: Full anti-detection (stealth + patchright + flaresolverr)
./skills/dev-browser/server.sh &

# Headless mode with full anti-detection
./skills/dev-browser/server.sh --headless &

# Force specific driver
./skills/dev-browser/server.sh --driver patchright &

# Minimal setup without any anti-detection
./skills/dev-browser/server.sh --no-stealth --no-flaresolverr &
```

### Extension Mode

Connects to user's existing Chrome browser. Use this when:

- The user is already logged into sites and wants you to do things behind an authed experience that isn't local dev.
- The user asks you to use the extension

**Important**: The core flow is still the same. You create named pages inside of their browser.

**Start the relay server:**

```bash
cd skills/dev-browser && npm i && npm run start-extension &
```

Wait for `Waiting for extension to connect...` followed by `Extension connected` in the console. To know that a client has connected and the browser is ready to be controlled.
**Workflow:**

1. Scripts call `client.page("name")` just like the normal mode to create new pages / connect to existing ones.
2. Automation runs on the user's actual browser session

If the extension hasn't connected yet, tell the user to launch and activate it. Download link: https://github.com/SawyerHood/dev-browser/releases

## Writing Scripts

> **Run all scripts from `skills/dev-browser/` directory.** The `@/` import alias requires this directory's config.

Execute scripts inline using heredocs:

```bash
cd skills/dev-browser && npx tsx <<'EOF'
import { connect, waitForPageLoad } from "@/client.js";

const client = await connect();
// Create page with custom viewport size (optional)
const page = await client.page("example", { viewport: { width: 1920, height: 1080 } });

await page.goto("https://example.com");
await waitForPageLoad(page);

console.log({ title: await page.title(), url: page.url() });
await client.disconnect();
EOF
```

**Write to `tmp/` files only when** the script needs reuse, is complex, or user explicitly requests it.

### Key Principles

1. **Small scripts**: Each script does ONE thing (navigate, click, fill, check)
2. **Evaluate state**: Log/return state at the end to decide next steps
3. **Descriptive page names**: Use `"checkout"`, `"login"`, not `"main"`
4. **Disconnect to exit**: `await client.disconnect()` - pages persist on server
5. **Plain JS in evaluate**: `page.evaluate()` runs in browser - no TypeScript syntax

## Workflow Loop

Follow this pattern for complex tasks:

1. **Write a script** to perform one action
2. **Run it** and observe the output
3. **Evaluate** - did it work? What's the current state?
4. **Decide** - is the task complete or do we need another script?
5. **Repeat** until task is done

### No TypeScript in Browser Context

Code passed to `page.evaluate()` runs in the browser, which doesn't understand TypeScript:

```typescript
// ✅ Correct: plain JavaScript
const text = await page.evaluate(() => {
  return document.body.innerText;
});

// ❌ Wrong: TypeScript syntax will fail at runtime
const text = await page.evaluate(() => {
  const el: HTMLElement = document.body; // Type annotation breaks in browser!
  return el.innerText;
});
```

## Scraping Data

For scraping large datasets, intercept and replay network requests rather than scrolling the DOM. See [references/scraping.md](references/scraping.md) for the complete guide covering request capture, schema discovery, and paginated API replay.

## Client API

```typescript
const client = await connect();

// Get or create named page (viewport only applies to new pages)
const page = await client.page("name");
const pageWithSize = await client.page("name", { viewport: { width: 1920, height: 1080 } });

const pages = await client.list(); // List all page names
await client.close("name"); // Close a page
await client.disconnect(); // Disconnect (pages persist)

// ARIA Snapshot methods
const snapshot = await client.getAISnapshot("name"); // Get accessibility tree
const element = await client.selectSnapshotRef("name", "e5"); // Get element by ref
```

The `page` object is a standard Playwright Page.

## Waiting

```typescript
import { waitForPageLoad } from "@/client.js";

await waitForPageLoad(page); // After navigation
await page.waitForSelector(".results"); // For specific elements
await page.waitForURL("**/success"); // For specific URL
```

## Inspecting Page State

### Screenshots

```typescript
await page.screenshot({ path: "tmp/screenshot.png" });
await page.screenshot({ path: "tmp/full.png", fullPage: true });
```

### ARIA Snapshot (Element Discovery)

Use `getAISnapshot()` to discover page elements. Returns YAML-formatted accessibility tree:

```yaml
- banner:
  - link "Hacker News" [ref=e1]
  - navigation:
    - link "new" [ref=e2]
- main:
  - list:
    - listitem:
      - link "Article Title" [ref=e8]
      - link "328 comments" [ref=e9]
- contentinfo:
  - textbox [ref=e10]
    - /placeholder: "Search"
```

**Interpreting refs:**

- `[ref=eN]` - Element reference for interaction (visible, clickable elements only)
- `[checked]`, `[disabled]`, `[expanded]` - Element states
- `[level=N]` - Heading level
- `/url:`, `/placeholder:` - Element properties

**Interacting with refs:**

```typescript
const snapshot = await client.getAISnapshot("hackernews");
console.log(snapshot); // Find the ref you need

const element = await client.selectSnapshotRef("hackernews", "e2");
await element.click();
```

## Error Recovery

Page state persists after failures. Debug with:

```bash
cd skills/dev-browser && npx tsx <<'EOF'
import { connect } from "@/client.js";

const client = await connect();
const page = await client.page("hackernews");

await page.screenshot({ path: "tmp/debug.png" });
console.log({
  url: page.url(),
  title: await page.title(),
  bodyText: await page.textContent("body").then((t) => t?.slice(0, 200)),
});

await client.disconnect();
EOF
```

## Anti-Detection Features (Auto-Enabled by Default)

By default, the skill automatically enables all anti-detection features for protected sites with bot detection (Cloudflare, DataDome, etc.):

| Feature | Auto-Enable | Requirements | Usage |
|---------|-------------|--------------|-------|
| **Patchright** | ✅ Yes (Default) | npm | Auto-installed and used for stealth automation |
| **Stealth Mode** | ✅ Yes (Default) | None | Enabled by default with args + patches |
| **FlareSolverr** | ✅ Yes (Default) | Docker | Auto-started if Docker is available |

### How It Works

**Patchright Auto-Install:**
When you start the server with defaults (`./server.sh`):
1. Checks if patchright is installed
2. If not found → automatically installs it via npm
3. Uses Patchright with built-in stealth capabilities
4. Falls back to Playwright with manual patches if install fails

**Stealth Mode (Default ON):**
Stealth mode is now enabled by default and includes:
1. Modified browser launch args (removes `--enable-automation`, etc.)
2. If using Playwright: runtime patches to hide `navigator.webdriver` and other indicators
3. If using Patchright: native stealth features handle evasion automatically
4. All new pages get stealth patches applied

**FlareSolverr (Auto-Start):**
FlareSolverr Docker container is automatically started when:
1. Docker is installed and running
2. `--no-flaresolverr` flag was NOT used
3. A container named `dev-browser-flaresolverr` doesn't already exist

The container runs on port 8191 and is ready for `bypassCloudflare()` calls.

### Stopping Services

To stop all dev-browser services gracefully:

```bash
# Stop all services (server, browser, FlareSolverr Docker)
./skills/dev-browser/server.sh --stop
```

This will:
1. Stop the dev-browser HTTP server (port 9222)
2. Close all browser contexts and pages
3. Stop the FlareSolverr Docker container
4. Clean up any stale Chrome processes

### Disabling Anti-Detection

If you need a standard browser without anti-detection:

```bash
# Disable all anti-detection features
./skills/dev-browser/server.sh --no-stealth --no-flaresolverr --driver playwright
```

### Prerequisites

All anti-detection features are **auto-enabled by default** when you run `./server.sh`. No manual setup required.

**Optional: Pre-install Patchright** (to avoid install delay on first run):
```bash
cd skills/dev-browser && npm install patchright
```

**Optional: Ensure Docker is running** (for FlareSolverr auto-start):
```bash
# FlareSolverr requires Docker. If Docker is not running, the skill will skip it with a warning.
docker info
```

To completely disable anti-detection and use a standard browser:
```bash
./skills/dev-browser/server.sh --no-stealth --no-flaresolverr --driver playwright
```

### Stealth Mode

Apply runtime anti-detection patches to a page to hide automation flags:

```typescript
import { connect, applyStealthMode } from "@/client.js";

const client = await connect();
const page = await client.page("example");

// Apply stealth patches before navigating
await applyStealthMode(page);

await page.goto("https://example.com");
console.log("Page title:", await page.title());

await client.disconnect();
```

### Cloudflare Bypass

For sites protected by Cloudflare challenge pages:

```typescript
import { connect, bypassCloudflare } from "@/client.js";

const client = await connect();
const page = await client.page("protected");

// Use FlareSolverr to solve the challenge and inject cookies
await bypassCloudflare(page, "https://protected-site.com", {
  maxTimeout: 60000,
});

// Page now has valid Cloudflare session
console.log("After bypass:", await page.title());

await client.disconnect();
```

The `bypassCloudflare` function:
1. Sends the URL to FlareSolverr to solve the challenge
2. Receives authentication cookies
3. Injects cookies into the Playwright context
4. Navigates to the target URL

### Using Patchright Directly

To launch a browser with Patchright directly (for full stealth capabilities):

```typescript
import { launchBrowser, USER_AGENTS } from "@/client.js";

const context = await launchBrowser({
  usePatchright: true,
  stealth: true,
  headless: false,
  userAgent: USER_AGENTS.chrome.windows,
  viewport: { width: 1920, height: 1080 },
});

const page = await context.newPage();
await page.goto("https://example.com");
```

### Advanced: FlareSolverr Client

For more control over challenge solving, use the FlareSolverr client directly:

```typescript
import { FlareSolverrClient } from "@/client.js";

const flaresolverr = new FlareSolverrClient({
  baseUrl: "http://localhost:8191",
  defaultTimeout: 60000,
});

// Check health
await flaresolverr.health();

// Create a session for persistence
const sessionId = await flaresolverr.createSession();

// Solve URLs within the same session (cookies persist)
const result1 = await flaresolverr.solveUrl("https://site.com/page1", { sessionId });
const result2 = await flaresolverr.solveUrl("https://site.com/page2", { sessionId });

// Clean up
await flaresolverr.destroySession(sessionId);
```
