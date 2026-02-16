---
name: qa-use
description: E2E testing and browser automation with qa-use CLI. Use when the user needs to run tests, verify features, automate browser interactions, or debug test failures.
allowed-tools: Bash(qa-use *)
---

# qa-use

E2E testing and browser automation for AI-driven development workflows.

## Critical Insight: Plugin Commands as Shortcuts

**For AI Harnesses (codex, opencode, etc.):**

Plugin commands (slash commands like `/qa-use:verify`) are **convenience shortcuts** that wrap CLI workflows. Harnesses with only the Bash tool can access ALL functionality via CLI commands documented below.

**Pattern throughout this document:**
- **CLI Workflow**: Step-by-step CLI commands (works for ALL harnesses)
- **Plugin Shortcut**: Optional slash command (convenience)

## Core Workflow

### 1. Browser Control & Session Lifecycle

**CLI Workflow:**
```bash
# Create browser session
qa-use browser create --viewport desktop

# For localhost testing
qa-use browser create --tunnel --no-headless

# Navigate
qa-use browser goto https://example.com

# Snapshot to get element refs (ALWAYS do this before interacting)
qa-use browser snapshot

# Interact by ref
qa-use browser click e3
qa-use browser fill e5 "text"

# Close
qa-use browser close
```

**Plugin Shortcut:**
```
/qa-use:explore https://example.com
```
(Wraps create + goto + snapshot with autonomous exploration)

**Critical:** Always run `snapshot` before your **first** interaction on a page. Never guess element refs.

**Snapshot Diff Feature (use it to avoid unnecessary snapshots):**
After each action (goto, click, fill, etc.), the browser automatically shows DOM changes:
- **Summary**: "5 elements added, 1 element modified"
- **Added elements**: `+ [e54] generic "Thanks for agreeing!"` (green)
- **Modified elements**: `~ [e18] checkbox "I agree..."` with `+attrs: checked, active` (yellow)
- **Removed elements**: `- [e99] button "Submit"` (red)

**When you can skip a full `snapshot`:** If the diff output from your last action already shows the element ref you need to interact with next, use it directly — no need for an intermediate `snapshot`. For example, if clicking a button shows `+ [e54] button "Submit"` in the diff, you can `click e54` immediately.

**When you still need a full `snapshot`:** Run `snapshot` when you need to find elements that weren't in the diff (e.g., pre-existing elements you haven't interacted with yet), or when the diff was truncated (shows "... and N more changes").

### 2. Understanding Blocks

**What are blocks?**

Blocks are atomic recorded interactions from a browser session. They are:
- Automatically captured during any browser interaction (click, fill, goto, scroll, etc.)
- Stored server-side with the session
- Retrieved via `qa-use browser get-blocks`
- The foundation for test generation

**Why blocks matter:**
- **Record-once, replay-many**: Interactive recording becomes automated test
- **AI-friendly**: Agents can analyze blocks to understand user intent
- **Version control**: Blocks stored with session enable test iteration
- **Bridge CLI → Tests**: Natural workflow from exploration to automation

**How blocks work:**

```bash
# 1. Create session and interact
qa-use browser create --tunnel --no-headless
qa-use browser goto https://example.com
qa-use browser snapshot        # Returns: [ref=e1] button
qa-use browser click e1        # Records as block
qa-use browser fill e5 "text"  # Records as block

# 2. Retrieve blocks (JSON array)
qa-use browser get-blocks
# Returns:
# [
#   {"type": "goto", "url": "...", "timestamp": "..."},
#   {"type": "click", "ref": "e1", "timestamp": "..."},
#   {"type": "fill", "ref": "e5", "value": "text", "timestamp": "..."}
# ]

# 3. Generate test YAML from blocks
qa-use browser generate-test -n "my_test" -o qa-tests/my_test.yaml

# 4. Run generated test
qa-use test run my_test
```

**Plugin Shortcut:**
```
/qa-use:record start my_test
# ... perform interactions ...
/qa-use:record stop
```
(Wraps the interactive workflow with AI-powered test generation)

### 3. Test Management

**CLI Workflow:**
```bash
# Run test by name
qa-use test run login

# Run with autofix (AI self-healing)
qa-use test run login --autofix

# Validate syntax
qa-use test validate login

# Show test details
qa-use test info login

# List test runs
qa-use test runs --status failed
```

**Plugin Shortcut:**
```
/qa-use:test-run login --autofix
```
(Convenience shortcut for common test execution)

### 4. Test Sync Lifecycle

**CLI Workflow:**
```bash
# Pull tests from cloud
qa-use test sync pull

# Push all local tests to cloud
qa-use test sync push --all

# Push specific test
qa-use test sync push --id <uuid>

# Force push (overwrite conflicts)
qa-use test sync push --force

# Compare local vs cloud
qa-use test diff login.yaml
```

**No Plugin Shortcut** - Use CLI commands directly

## Essential Commands

### Browser Session Management

| Command | Description |
|---------|-------------|
| `qa-use browser create` | Create remote browser session |
| `qa-use browser create --tunnel` | Create local browser with API tunnel |
| `qa-use browser create --no-headless` | Show browser window (tunnel mode only) |
| `qa-use browser create --viewport <size>` | Set viewport: `desktop`, `tablet`, `mobile` |
| `qa-use browser create --ws-url <url>` | Connect to existing WebSocket browser |
| `qa-use browser create --after-test-id <uuid>` | Run a test first, then become interactive |
| `qa-use browser create --var <key=value>` | Override app config variables (repeatable) |
| `qa-use browser list` | List active sessions |
| `qa-use browser status` | Show current session details (app_url, recording_url, etc.) |
| `qa-use browser close` | Close active session |

Sessions auto-persist in `~/.qa-use.json`. One active session = no `-s` flag needed.

### Navigation

| Command | Description |
|---------|-------------|
| `qa-use browser goto <url>` | Navigate to URL |
| `qa-use browser back` | Go back |
| `qa-use browser forward` | Go forward |
| `qa-use browser reload` | Reload page |

### Element Interaction

| Command | Description |
|---------|-------------|
| `qa-use browser click <ref>` | Click element by ref |
| `qa-use browser click --text "Button"` | Click by semantic description |
| `qa-use browser fill <ref> "value"` | Fill input field |
| `qa-use browser type <ref> "text"` | Type with delays (for autocomplete) |
| `qa-use browser press <key>` | Press key (e.g., `Enter`, `Tab`) |
| `qa-use browser check <ref>` | Check checkbox |
| `qa-use browser uncheck <ref>` | Uncheck checkbox |
| `qa-use browser select <ref> "option"` | Select dropdown option |
| `qa-use browser hover <ref>` | Hover over element |
| `qa-use browser scroll down 500` | Scroll by pixels |
| `qa-use browser scroll-into-view <ref>` | Scroll element into view |
| `qa-use browser drag <ref> --target <ref>` | Drag element to target |
| `qa-use browser mfa-totp [ref] <secret>` | Generate TOTP code (optionally fill) |
| `qa-use browser upload <ref> <file>...` | Upload file(s) to input |

### Inspection & Snapshot Diff

| Command | Description |
|---------|-------------|
| `qa-use browser snapshot` | Get full ARIA tree with element refs (use only when diff output is insufficient) |
| `qa-use browser url` | Get current URL |
| `qa-use browser screenshot` | Save screenshot.png |
| `qa-use browser screenshot file.png` | Save to custom path |
| `qa-use browser screenshot --base64` | Output base64 to stdout |
| `qa-use browser evaluate <expression>` | Execute JavaScript in browser context |

The snapshot-diff feature automatically displays DOM changes after each browser action:
- **Added elements**: Shown with `+` prefix and green color — these refs are immediately usable
- **Modified elements**: Shown with `~` prefix and yellow color, including attribute changes (`+attrs: checked`)
- **Removed elements**: Shown with `-` prefix and red color — do NOT use these refs

Use diff output to interact with newly appeared elements directly, without running a full `snapshot` first.

### Test Operations

| Command | Description |
|---------|-------------|
| `qa-use test run <name>` | Run test by name |
| `qa-use test run --all` | Run all tests |
| `qa-use test run <name> --tunnel` | Run with local browser tunnel |
| `qa-use test run <name> --autofix` | Enable AI self-healing |
| `qa-use test run <name> --update-local` | Persist AI fixes to file |
| `qa-use test run <name> --download` | Download assets to `/tmp/qa-use/downloads/` |
| `qa-use test run <name> --var key=value` | Override variable |
| `qa-use test validate <name>` | Validate test syntax |
| `qa-use test list` | List available tests |
| `qa-use test info <name>` | Show test details (steps, tags, description) |
| `qa-use test info --id <uuid>` | Show cloud test details by ID |
| `qa-use test runs [name]` | List test run history |
| `qa-use test runs --id <uuid>` | Filter runs by test ID |
| `qa-use test runs --status failed` | Filter runs by status |
| `qa-use test init` | Initialize test directory |
| `qa-use test sync pull` | Pull tests from cloud |
| `qa-use test sync push --all` | Push all local tests to cloud |
| `qa-use test sync push --id <uuid>` | Push specific test |
| `qa-use test sync push --force` | Push tests, overwriting conflicts |
| `qa-use test diff <file>` | Compare local vs cloud test |
| `qa-use test schema [path]` | View test definition schema |

### Logs & Debugging

| Command | Description |
|---------|-------------|
| `qa-use browser logs console` | View console logs from session |
| `qa-use browser logs console -s <id>` | View logs from specific/closed session |
| `qa-use browser logs network` | View network request logs |
| `qa-use browser logs network -s <id>` | View network logs from specific session |

### Test Generation

| Command | Description |
|---------|-------------|
| `qa-use browser generate-test` | Generate test YAML from recorded session |
| `qa-use browser generate-test -s <id>` | Generate from specific session |
| `qa-use browser generate-test -n <name>` | Specify test name |
| `qa-use browser generate-test -o <path>` | Specify output path |
| `qa-use browser get-blocks` | Get recorded interaction blocks (JSON) |

### Waiting

| Command | Description |
|---------|-------------|
| `qa-use browser wait <ms>` | Fixed wait |
| `qa-use browser wait-for-selector ".class"` | Wait for selector |
| `qa-use browser wait-for-load` | Wait for page load |

### Variable Overrides

Use `--var` to override app config variables at runtime. Common variables:

| Variable | Description |
|----------|-------------|
| `base_url` | Base URL for the app (e.g., preview deployment URL) |
| `login_url` | Login page URL |
| `login_username` | Username/email for authentication |
| `login_password` | Password for authentication |

Example with ephemeral preview URL:
```bash
qa-use browser create --after-test-id <login-test-uuid> \
  --var base_url=https://preview-123.example.com \
  --var login_url=https://preview-123.example.com/auth/login
```

## Common Patterns

### Pattern 1: Feature Verification

**CLI Workflow:**
```bash
# 1. Search for existing test
qa-use test list | grep "login"

# 2. Run test with autofix
qa-use test run login --autofix

# 3. Debug failures
qa-use browser logs console
```

**Plugin Shortcut:**
```
/qa-use:verify "login works with valid credentials"
```
(Wraps the above CLI workflow with AI-powered test discovery and analysis)

### Pattern 2: Record & Generate Test

**CLI Workflow:**
```bash
# 1. Create session
qa-use browser create --tunnel --no-headless

# 2. Navigate and interact
qa-use browser goto https://example.com
qa-use browser snapshot
qa-use browser click e1
qa-use browser fill e5 "test"

# 3. Generate test from blocks
qa-use browser get-blocks
qa-use browser generate-test -n "my_test"

# 4. Run test
qa-use test run my_test
```

**Plugin Shortcut:**
```
/qa-use:record start my_test
# ... perform interactions ...
/qa-use:record stop
```

### Pattern 3: Authenticated Exploration

**CLI Workflow:**
```bash
# Create session that runs login test first
qa-use browser create --after-test-id <login-test-uuid>

# Session now authenticated, explore
qa-use browser goto /dashboard
qa-use browser snapshot
```

**Plugin Shortcut:**
```
/qa-use:explore /dashboard
```
(Automatically handles auth detection and session creation)

### Pattern 4: Edit Existing Test

**CLI Workflow:**
```bash
# 1. Open test file in editor
vim qa-tests/login.yaml

# 2. Validate syntax
qa-use test validate login

# 3. Run to verify
qa-use test run login
```

**Plugin Shortcut:**
```
/qa-use:record edit login
```
(AI-assisted editing with validation)

### Pattern 5: Using Snapshot Diff to Avoid Unnecessary Snapshots

**CLI Workflow:**
```bash
# Create session and navigate
qa-use browser create --tunnel --no-headless
qa-use browser goto https://evals.desplega.ai/checkboxes

# goto shows diff — initial page load shows all elements:
# Changes: 45 elements added
# + [e18] checkbox "I agree to the terms and conditions"
# + [e19] generic "I agree to the terms and conditions"

# ✅ Use ref from diff directly — no snapshot needed!
qa-use browser click e18

# Diff shows what changed:
# Changes: 5 elements added, 1 element modified
# + [e54] generic "Thanks for agreeing!"
# + [e55] link "Terms and Conditions"
# ~ [e18] checkbox "I agree to the terms and conditions"
#     +attrs: active, checked

# ✅ Can click e55 directly from diff output — no snapshot needed!
qa-use browser click e55

# ❌ Need to find an element NOT in the diff? Now run snapshot:
qa-use browser snapshot
```

**Key principle:** Use diff output as your primary source of element refs after actions. Only fall back to `snapshot` when you need to find elements that weren't in the diff.

**Benefits:**
- Fewer API calls = faster automation
- Diff refs are always fresh (just returned from the server)
- Instantly see what changed (new elements, attribute changes, removals)

**No Plugin Shortcut** - Automatic feature in all browser commands

## CI/CD Integration

### Running Tests in CI

**Environment Variables:**
```bash
export QA_USE_API_KEY="your-api-key"
export QA_USE_REGION="us"  # Optional: "us" or "auto"
```

**Basic Test Execution:**
```bash
# Run all tests
qa-use test run --all

# Run specific tag
qa-use test run --tag smoke

# Exit codes: 0 = pass, 1 = fail
```

### GitHub Actions Example

```yaml
name: QA Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - name: Install qa-use
        run: npm install -g @desplega.ai/qa-use
      - name: Run tests
        run: qa-use test run --all
        env:
          QA_USE_API_KEY: ${{ secrets.QA_USE_API_KEY }}
```

### Test Artifacts

**Screenshots:**
- Automatically saved on failure
- Location: `/tmp/qa-use/downloads/` (local) or cloud (remote)

**Logs:**
- Console logs: `qa-use browser logs console -s <session-id>`
- Network logs: `qa-use browser logs network -s <session-id>`

## Advanced Topics

### Localhost Testing (Tunnel Mode)

**When to use tunnel mode:**

```
Testing localhost (http://localhost:3000)?
  ├─ YES → Use --tunnel
  │   └─ qa-use browser create --tunnel [--no-headless]
  │       (Starts local Playwright, creates localtunnel, keeps running)
  │
  └─ NO (Public URL) → Use remote browser (default)
      └─ qa-use browser create
          (Uses desplega.ai cloud browser via WebSocket)
```

**The `--tunnel` flag is a binary choice:**
- **Local tunnel mode**: Playwright on your machine + localtunnel
- **Remote mode**: WebSocket URL to cloud-hosted browser

**For test execution:**
```bash
# Local app
qa-use test run my_test --tunnel [--headful]

# Public app
qa-use test run my_test
```

**Plugin shortcuts handle tunnel detection automatically:**
```
/qa-use:explore http://localhost:3000
/qa-use:record start local_test
```

See [references/localhost-testing.md](references/localhost-testing.md) for troubleshooting.

### Session Persistence

Sessions are stored in `~/.qa-use.json` and have:
- **TTL**: 30 minutes (default)
- **Auto-resolve**: One active session = no `-s` flag needed
- **Cleanup**: Automatic on timeout or explicit `browser close`

### Block Limitations

**What's captured:**
- goto, click, fill, type, check, uncheck, select, hover
- scroll, scroll-into-view, drag, upload, press

**What's NOT captured:**
- Assertions (must be added manually)
- Waits (inferred from timing, may need adjustment)
- Complex interactions (multi-drag, hover sequences)

**Manual editing:** Edit generated YAML to add assertions and refine selectors.

### WebSocket Sessions

**Sharing sessions across processes:**
```bash
# Process 1: Create session
qa-use browser create --tunnel
# Output: ws://localhost:12345/browser/abc123

# Process 2: Connect to session
qa-use browser goto https://example.com --ws-url ws://localhost:12345/browser/abc123
```

## Deep-Dive References

| Document | Description |
|----------|-------------|
| [browser-commands.md](references/browser-commands.md) | Complete browser CLI reference with all flags |
| [test-format.md](references/test-format.md) | Full test YAML specification |
| [localhost-testing.md](references/localhost-testing.md) | Tunnel setup for local development |
| [failure-debugging.md](references/failure-debugging.md) | Failure classification and diagnostics |
| [ci.md](references/ci.md) | CI/CD integration patterns and examples |

## Templates

| Template | Description |
|----------|-------------|
| [basic-test.yaml](templates/basic-test.yaml) | Simple navigation and assertion |
| [auth-flow.yaml](templates/auth-flow.yaml) | Login flow with credentials |
| [form-test.yaml](templates/form-test.yaml) | Form submission with validation |

## Test Format Overview

```yaml
name: Login Test
description: Validates login functionality with valid credentials
tags:
  - smoke
  - auth
app_config: <app-config-id>
variables:
  email: test@example.com
  password: secret123
depends_on: setup-test  # Optional
steps:
  - action: goto
    url: /login
  - action: fill
    target: email input
    value: $email
  - action: click
    target: login button
  - action: to_be_visible
    target: dashboard
```

See [references/test-format.md](references/test-format.md) for complete specification.

## Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `browser navigate <url>` | `browser goto <url>` |
| `browser destroy` | `browser close` |
| `browser close <session-id>` | `browser close` |
| Guessing element refs | Use refs from diff output or `snapshot` |
| Running `snapshot` after every action | Use diff output; only `snapshot` when needed |
| Testing localhost without `--tunnel` | Use `--tunnel` flag |
| `test sync --pull` | `test sync pull` (subcommand, not flag) |
| `test sync --push` | `test sync push` (subcommand, not flag) |

## npx Alternative

All commands use `qa-use` assuming global install. For one-off use:
```bash
npx @desplega.ai/qa-use browser <command>
```
