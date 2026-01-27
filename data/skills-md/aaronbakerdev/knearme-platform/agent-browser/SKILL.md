---
name: agent-browser
description: Fast browser automation CLI for AI agents using the Vercel agent-browser tool. Use for headless browser control, web scraping, form filling, automated UI testing, or when a user asks for agent-browser/browser automation/headless browser/automate browser; optimized for the KnearMe portfolio platform (knearme-portfolio and knearme-cms).
---

# Agent Browser Skill

Use this fast browser automation CLI designed for AI agents. Use deterministic element references (`@e1`, `@e2`) from accessibility tree snapshots for reliable element targeting.

**Target:** KnearMe portfolio platform (knearme-portfolio and knearme-cms)

---

## Session Startup (REQUIRED)

Before any agent-browser commands, ensure the daemon is running. The daemon manages browser sessions and persists state between commands.

### Quick Start

```bash
# Source the helper script (sets env vars and starts daemon)
source /Users/aaronbaker/knearme-platform/.claude/skills/agent-browser/scripts/ensure-daemon.sh
```

### Manual Alternative

```bash
# Check if daemon is running
pgrep -f "agent-browser.*daemon" || (
  export AGENT_BROWSER_EXECUTABLE_PATH="$HOME/Library/Caches/ms-playwright/chromium-1200/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
  cd /Users/aaronbaker/knearme-platform/agent-browser
  nohup node dist/daemon.js > /tmp/agent-browser-daemon.log 2>&1 &
)
```

### Stop Daemon (When Done)

```bash
/Users/aaronbaker/knearme-platform/.claude/skills/agent-browser/scripts/stop-daemon.sh
```

### Troubleshooting Startup

**Mach Port Conflicts (macOS):** If Chrome is running, the headless browser may fail to launch.

Solutions:
1. Close Chrome before automation, OR
2. Use CDP mode to connect to running Chrome:
   ```bash
   # User runs this in a terminal:
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 &

   # Then connect via CDP:
   agent-browser connect 9222
   agent-browser snapshot -i  # Works
   ```

See CDP Mode section below for full details.

---

## THE ONE RULE

**After ANY action that might change the page, run `snapshot -i`**

```bash
# WRONG - refs are stale after navigation
agent-browser click @e6
agent-browser click @e2      # FAILS - e2 is from old page

# RIGHT - re-snapshot after page change
agent-browser click @e6
agent-browser wait 2000
agent-browser snapshot -i    # Get fresh refs
agent-browser click @e2      # Works
```

Expect refs to reset when the page changes; always re-snapshot.

---

## Mental Model

```
LOOK  ->  DECIDE  ->  ACT  ->  LOOK AGAIN

1. snapshot -i           # See what's on the page
2. (read output)         # Find the right ref
3. click @e3             # Take action
4. wait 2000             # Let page update
5. snapshot -i           # See new state
```

**Never act twice without looking in between.**

---

## Core Workflow

### Open and Explore

```bash
agent-browser open <url>
agent-browser snapshot -i
```

### Interact with Elements

```bash
agent-browser fill @e2 "text"    # Clear + fill input
agent-browser click @e3          # Click element
agent-browser press Enter        # Press key
```

### Verify Results

```bash
agent-browser get url                    # Check current URL
agent-browser screenshot /tmp/view.png   # Visual capture
```

### Close When Done

```bash
agent-browser close
```

---

## Quick Decision Tree

```
What mode do I need?

Running inside a sandbox (Claude Code)?
  -> Use CDP Mode - connect to user's Chrome
  -> See "CDP Mode" section below

Test with user's logged-in Chrome?
  -> Use CDP Mode - connect to user's Chrome
  -> See "CDP Mode" section below

Test multiple users in parallel?
  -> agent-browser --session user-1 open <url>
  -> See references/advanced-features.md

Debug with user watching?
  -> agent-browser --headed open <url>

Standard automation?
  -> agent-browser open <url>

Need to "see" the page?
  -> agent-browser screenshot /tmp/x.png
  -> Read /tmp/x.png
```

---

## Headed Mode (Visible Browser)

Show a visible browser window for debugging or user observation.

### Requirements

1. **Daemon must be running first** - always run `source ensure-daemon.sh` before any agent-browser commands
2. **Flag goes BEFORE the command** - `--headed` must come before `open`

### Correct Usage

```bash
# Step 1: Ensure daemon is running
source /Users/aaronbaker/knearme-platform/.claude/skills/agent-browser/scripts/ensure-daemon.sh

# Step 2: Open with --headed flag BEFORE the command
agent-browser --headed open http://localhost:3000
```

### Common Mistakes

```bash
# WRONG: --headed after URL (flag ignored, headless mode)
agent-browser open http://localhost:3000 --headed

# WRONG: No daemon running (will error: "Browser not launched")
agent-browser --headed open http://localhost:3000

# WRONG: "launch" command doesn't exist
agent-browser launch --headed

# RIGHT: Daemon first, then --headed before open
source ensure-daemon.sh
agent-browser --headed open http://localhost:3000
```

### Recommended: Use dev-browse.sh

The `dev-browse.sh` script handles daemon setup automatically:

```bash
# Starts app, ensures daemon, opens browser with --headed
/Users/aaronbaker/knearme-platform/.claude/skills/agent-browser/scripts/dev-browse.sh portfolio --headed

# With viewport preset
./dev-browse.sh portfolio --headed --mobile
```

---

## CDP Mode (Connecting to Existing Chrome)

When running inside a sandbox (like Claude Code) or needing user's auth cookies/sessions, connect to an existing Chrome instance instead of launching a new one.

**Why?** The sandbox lacks permissions to launch applications. CDP mode connects to Chrome running outside the sandbox.

### Setup (User runs in their terminal, not Claude Code)

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 --user-data-dir=/tmp/chrome-debug
```

### Connection Methods

**Method 1: Connect Once (Recommended)**

Establish connection first, then subsequent commands work without flags:

```bash
agent-browser connect 9222    # Connect to CDP - do this first
agent-browser snapshot -i     # No flag needed after connect
agent-browser click @e3       # Works automatically
agent-browser fill @e2 "text" # Works automatically
agent-browser close           # Disconnect when done
```

**Method 2: Flag on Every Command**

Pass `--cdp` on each command (more verbose):

```bash
agent-browser --cdp 9222 snapshot -i
agent-browser --cdp 9222 click @e3
agent-browser --cdp 9222 fill @e2 "text"
```

### When to Use CDP Mode

| Scenario | Use CDP? |
|----------|----------|
| Running in Claude Code sandbox | **Yes** |
| Need user's auth cookies | **Yes** |
| Debug alongside user | **Yes** |
| Test with user's extensions | **Yes** |
| Isolated/repeatable tests | No - use sessions |
| CI/CD automation | No - use headless |

### Multiple Agents in Parallel

Run multiple agents simultaneously by connecting each to a different Chrome instance:

```bash
# Terminal 1: Start Chrome on port 9223
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9223 --user-data-dir=/tmp/chrome-9223 --headless=new

# Terminal 2: Start Chrome on port 9224
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9224 --user-data-dir=/tmp/chrome-9224 --headless=new
```

Then each agent connects to its own port:

```bash
# Agent 1                          # Agent 2
agent-browser connect 9223         agent-browser connect 9224
agent-browser open <url>           agent-browser open <url>
agent-browser snapshot -i          agent-browser snapshot -i
```

See `references/advanced-features.md` for more CDP details.

---

## Essential Commands

| Action | Command |
|--------|---------|
| Open URL | `agent-browser open <url>` |
| Get refs | `agent-browser snapshot -i` |
| Click | `agent-browser click @e3` |
| Fill | `agent-browser fill @e2 "text"` |
| Type | `agent-browser type @e2 "text"` |
| Press key | `agent-browser press Enter` |
| Wait | `agent-browser wait 2000` |
| Get URL | `agent-browser get url` |
| Screenshot | `agent-browser screenshot /tmp/shot.png` |
| Close | `agent-browser close` |

For full command reference, see `references/command-reference.md`.

---

## Reality Checks (Verified 2026-01-15)

Use these **observed behaviors** from a local sweep to avoid false assumptions.

### Selector vs Ref Rules

- **Use refs (`@eN`) only with action commands** like `click`, `fill`, `type`, `check`, `uncheck`, `hover`, `drag`.
- **Use CSS selectors for `get` and `wait`**, not refs.
  - ✅ `agent-browser get value "#email"`
  - ❌ `agent-browser get value @e3`
  - ✅ `agent-browser wait "#log"`
  - ❌ `agent-browser wait @e9`

### Known Limitations

- Avoid `select <selector> <value>`; it fails with "Validation error: values: Invalid input".
- Avoid `find testid`, `find first`, `find last`, `find nth`; they fail with "Expected string, received null".
- Avoid relying on `press Control+a` for selecting text; use `fill` or `eval`.
- Expect `tab new <url>` to open `about:blank` until a manual `open`.
- Pass `--filter` when using `network requests`.
- Provide a URL pattern for `network unroute` (no default).
- Avoid `set media dark`; it errors until fixed.
- Avoid `mouse wheel`; use `scroll` instead.
- Prefer `storage local set/get`; `state load` did not restore localStorage in sweep.

### Fallback Recipes

**Select dropdown without `select`:**
```bash
agent-browser eval "const el=document.querySelector('#plan'); el.value='pro'; el.dispatchEvent(new Event('change', { bubbles: true }));"
```

**Clear + set input without `press Control+a`:**
```bash
agent-browser fill "#name" "Ada Lovelace"
```

**Find by testid when `find testid` fails:**
```bash
agent-browser click "[data-testid='submit-button']"
```

See `references/capability-matrix.md` for the full sweep results.

---

## Common Patterns

### Login Flow (KnearMe Portfolio)

```bash
agent-browser open http://localhost:3000/login
agent-browser snapshot -i
# Read output: textbox "Email" [ref=e2], textbox "Password" [ref=e4], button "Login" [ref=e6]
agent-browser fill @e2 "$TEST_USER_EMAIL"
agent-browser fill @e4 "$TEST_USER_PASSWORD"
agent-browser click @e6
agent-browser wait 2000
agent-browser get url  # Verify redirect to /dashboard
```

### Multi-Step Form

```bash
# Step 1
agent-browser snapshot -i
agent-browser fill @e1 "value"
agent-browser click @e4  # Next

# CRITICAL: Re-snapshot for step 2
agent-browser wait 1000
agent-browser snapshot -i  # NEW REFS!
agent-browser fill @e1 "new value"  # e1 is now different field
```

### Visual Verification

```bash
agent-browser screenshot /tmp/view.png
# Then use Read tool on /tmp/view.png to "see" the page
```

---

## UI Testing Approach

For effective UI testing, follow the **four-phase pattern**:

```
SETUP → ACTION → VALIDATE → RECOVERY
```

### Visual Debugging Loop

When testing UIs, leverage Claude's vision capabilities:

```bash
# 1. CAPTURE - Take screenshot at decision points
agent-browser screenshot /tmp/state-before.png

# 2. ANALYZE - Use Read tool to visually inspect
# (Claude can identify layout issues, errors, missing elements)

# 3. ACT - Perform test action
agent-browser click @e5
agent-browser wait 2000

# 4. VERIFY - Capture and analyze result
agent-browser screenshot /tmp/state-after.png
# Compare before/after, check for expected changes
```

### Key Testing Capabilities

| Capability | Command | Use Case |
|------------|---------|----------|
| Visual state | `screenshot` + Read | Layout issues, visual bugs |
| Element state | `snapshot -i` | Available interactions |
| URL verification | `get url` | Navigation testing |
| Console errors | `console` / `errors` | JS debugging |
| Network mocking | `network route` | Error state testing |
| Parallel sessions | `--session` | Multi-tier testing |

See `references/ui-testing-patterns.md` for complete testing patterns.
See `references/visual-debugging.md` for visual debugging techniques.

---

## Anti-Patterns

**Acting without looking:**
```bash
agent-browser open <url>
agent-browser click @e3  # BAD - did you check snapshot?
```

**Using refs from examples:**
```bash
# Docs say "fill @e2" but YOUR page might be different
agent-browser fill @e2 "text"  # BAD - did you verify ref?
```

**Multiple actions without re-snapshot:**
```bash
agent-browser click @e3
agent-browser click @e5  # BAD - refs may be stale
```

**Correct pattern:**
```bash
agent-browser snapshot -i      # LOOK
agent-browser click @e6        # ACT
agent-browser wait 2000        # WAIT
agent-browser snapshot -i      # LOOK AGAIN
```

---

## Bundled Resources

| Resource | Purpose |
|----------|---------|
| `references/project-context.md` | KnearMe test users, environments, key routes |
| `references/advanced-features.md` | CDP, sessions, device emulation, network mocking |
| `references/troubleshooting.md` | Error recovery patterns |
| `references/command-reference.md` | Full command documentation |
| `references/capability-matrix.md` | Verified command status and workarounds |
| `references/ui-testing-patterns.md` | Structured UI testing patterns (forms, auth, access control) |
| `references/visual-debugging.md` | Screenshot analysis and visual debugging techniques |
| `references/prompting-templates.md` | Self-prompting templates for effective testing |

---

## Remember

1. **Always snapshot before acting** - refs come from snapshot output
2. **Re-snapshot after page changes** - refs reset on navigation
3. **Read the snapshot output** - match label to ref
4. **Wait for page loads** - give time for state to settle
5. **Screenshot + Read for visual** - use Read tool to "see" the page
