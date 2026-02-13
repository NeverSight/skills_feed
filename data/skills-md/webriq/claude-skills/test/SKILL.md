---
name: test
description: Test web implementations using Playwright MCP for E2E testing. Creates test reports in docs/testing/*.md. Supports email-based auth testing via Mailinator (registration, verification, password reset, notifications).
model: haiku
---

# /test - Web E2E Testing Agent

> **Model:** haiku (straightforward test execution)

## Command Flags

| Flag | Short | Description |
|------|-------|-------------|
| `--help` | `-h` | Show available commands and options |
| `--version` | `-v` | Show workflow skills version |
| `--ci` | | CI mode: headless testing with scripts |
| `--cleanup` | | Delete test scripts after run (use with --ci) |

### Flag Handling

**On `-h` or `--help`:**
```
/test - Web E2E Testing Agent

Usage:
  /test {ID}                         Interactive mode (Playwright MCP)
  /test --ci {ID}                    CI mode, keeps test scripts
  /test --ci --cleanup {ID}          CI mode, deletes scripts after
  /test --ci {ID} "instructions"     CI mode with custom instructions
  /test -h, --help                   Show this help message
  /test -v, --version                Show version

Arguments:
  {ID}    Task ID (number) or task filename (e.g., 001-auth-jwt)

Options:
  --ci        Headless mode using Playwright test runner
  --cleanup   Delete test scripts after completion (with --ci)

Examples:
  /test 1                            # Interactive visual testing
  /test 001-auth-jwt                 # Using task filename
  /test --ci 1                       # CI mode, scripts kept
  /test --ci --cleanup 1             # CI mode, scripts deleted

Next: /document {ID}
```

**On `-v` or `--version`:**
Display:
```
Workflow Skills v1.4.1
https://github.com/eljun/claude-skills
```

---

## Prerequisites

### Playwright MCP Setup (One-Time)

Interactive mode requires Playwright MCP. **No npm install needed** - Claude Code handles it automatically.

**Setup Steps:**

1. Create `.mcp.json` in your project root (not in `.claude/` or subdirectories):
   ```json
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }
   ```

2. **Restart Claude Code** (required after adding/modifying `.mcp.json`)

3. Verify MCP is active - you should see `mcp__playwright__browser_*` tools available

**How it works:**
- Claude Code reads `.mcp.json` on startup
- The `npx` command auto-downloads the package (no manual install)
- MCP server starts automatically and exposes browser control tools
- Tools like `mcp__playwright__browser_navigate`, `mcp__playwright__browser_click` become available

---

### Interactive Mode (Default)

**Playwright MCP is REQUIRED for interactive mode.** Before running tests, verify that `mcp__playwright__browser_navigate` is available as a tool. If Playwright MCP tools are not available:

1. **STOP** - Do not proceed with testing
2. **Notify the user** with this message:
   ```
   Playwright MCP is not configured. Interactive testing requires the MCP server.

   Add this to your project's .mcp.json:
   {
     "mcpServers": {
       "playwright": {
         "command": "npx",
         "args": ["@playwright/mcp@latest"]
       }
     }
   }

   Then restart Claude Code and re-run /test.

   Alternative: Use CI mode which doesn't require MCP:
   /test --ci {task-name}
   ```
3. **Do NOT fall back** to curl commands or source code inspection as a substitute for browser testing. This produces misleading test reports.

### CI Mode (`--ci` flag)

**Playwright MCP is NOT required for CI mode.** CI mode uses the standard Playwright test runner.

**Requirements for CI mode:**
```bash
# Install Playwright as dev dependency (if not already)
npm install -D @playwright/test

# Install browsers (first time only)
npx playwright install
```

CI mode generates test scripts and runs them with `npx playwright test` - no MCP server needed.

---

## CRITICAL: Mode-Specific Rules

### Interactive Mode (Default) - What NOT To Do

**DO NOT generate test script files.** Interactive mode uses Playwright MCP tools directly in the conversation - NOT by creating external test files.

**Prohibited in Interactive Mode:**
- ❌ Creating `.ts`, `.js`, or `.spec` test files (e.g., `test-app.ts`, `e2e-test.js`)
- ❌ Creating `TEST_REPORT.md`, `TEST_SUMMARY.txt` in project root
- ❌ Creating `test-screenshots/` or similar folders in project root
- ❌ Running `npx playwright test` or similar CLI commands
- ❌ Spawning subagents to run headless tests in background
- ❌ Using "CI/CD style" or "headless mode" testing workflows

**Required in Interactive Mode:**
- ✅ Use `mcp__playwright__browser_*` tools directly in conversation
- ✅ Write final report ONLY to `docs/testing/{task-name}.md`
- ✅ Interactive browser testing where you can see each step
- ✅ Take screenshots using `mcp__playwright__browser_take_screenshot` (stored in Playwright's temp directory, not project)

### CI Mode (`--ci` flag) - Allowed Actions

**CI mode IS allowed to generate test scripts**, but must follow these rules:

**Allowed in CI Mode:**
- ✅ Create test scripts in `tests/e2e/{task-name}/` (NOT project root)
- ✅ Run `npx playwright test` for headless execution
- ✅ Spawn subagents for parallel test execution
- ✅ Generate temporary screenshots during testing

**Required in CI Mode:**
- ✅ Write final report to `docs/testing/{task-name}.md`
- ✅ **MUST cleanup** all temporary artifacts after tests (see Cleanup section)
- ✅ Ask user if they want to keep test scripts for CI pipeline
- ✅ Never leave artifacts in project root

## When to Use

Invoke `/test {ID}` when:
- Task is in "Testing" status in TASKS.md
- Implementation is complete from `/implement`
- Ready to verify the feature works

**Example:** `/test 1` or `/test 001-dashboard-redesign`

### Task ID Resolution

The `{ID}` can be:
- **Numeric ID:** `1`, `2`, `3` → Looks up in TASKS.md, finds matching task document
- **Padded ID:** `001`, `002` → Same as numeric
- **Full filename:** `001-dashboard-redesign` → Direct file reference

### Syntax

```
/test {ID}                              → Interactive mode (default)
/test --ci {ID}                         → CI mode, keeps scripts (default)
/test --ci --cleanup {ID}               → CI mode, deletes scripts after test
/test --ci {ID} "instructions"          → CI mode with additional test instructions
```

**Examples:**
- `/test 1` - Interactive visual testing
- `/test --ci 2` - Headless CI testing, scripts kept for regression
- `/test --ci --cleanup 3` - CI testing, scripts deleted (minor changes)
- `/test --ci 4 "test empty cart and full cart"` - CI mode with specific scenarios

### Flag Reference

| Flag | Behavior | Use When |
|------|----------|----------|
| (none) | Interactive mode with Playwright MCP | Debugging, demos, visual verification |
| `--ci` | Headless mode, **keeps scripts** | Core features, regression protection |
| `--ci --cleanup` | Headless mode, **deletes scripts** | Minor changes, one-time verification |

---

## CRITICAL: Mode Detection (Execute FIRST)

**You MUST execute this decision tree BEFORE doing anything else:**

```
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Parse the command for --ci flag                    │
└─────────────────────────────────────────────────────────────┘
                           │
           ┌───────────────┴───────────────┐
           │                               │
           ▼                               ▼
   Has --ci flag?                    No --ci flag?
           │                               │
           │                               │
           ▼                               ▼
┌─────────────────────┐      ┌─────────────────────────────────┐
│ MODE = CI           │      │ STEP 2: Check for Playwright MCP │
│ Proceed to CI       │      │ Is mcp__playwright__browser_*    │
│ workflow            │      │ available as a tool?             │
└─────────────────────┘      └─────────────────────────────────┘
                                           │
                             ┌─────────────┴─────────────┐
                             │                           │
                             ▼                           ▼
                      Available?                  NOT Available?
                             │                           │
                             ▼                           ▼
               ┌─────────────────────┐    ┌──────────────────────────┐
               │ MODE = Interactive  │    │ **STOP IMMEDIATELY**     │
               │ Proceed to          │    │                          │
               │ Interactive workflow│    │ Display this message:    │
               └─────────────────────┘    │ "Playwright MCP is not   │
                                          │ configured. See prereqs."│
                                          │                          │
                                          │ DO NOT:                  │
                                          │ - Fall back to CI mode   │
                                          │ - Use curl/source code   │
                                          │ - Proceed with testing   │
                                          └──────────────────────────┘
```

**ABSOLUTE RULES:**
1. **No --ci flag + No Playwright MCP = STOP.** Do not proceed. Do not fall back.
2. **No --ci flag + Playwright MCP available = Interactive mode ONLY.** Never create test scripts.
3. **--ci flag present = CI mode.** Playwright MCP not required.

**How to check for Playwright MCP:**
Look for tools starting with `mcp__playwright__browser_` in your available tools. If you see tools like `mcp__playwright__browser_navigate`, `mcp__playwright__browser_click`, etc., Playwright MCP is available.

---

## Workflow

**IMPORTANT: Always execute "Mode Detection" section FIRST before following any workflow below.**

### Interactive Mode (Default) — REQUIRES Playwright MCP

**Entry condition:** No `--ci` flag AND Playwright MCP tools are available.

**If Playwright MCP is NOT available:** STOP. Do not use this workflow. Do not fall back to CI mode. Notify user to configure Playwright MCP.

```
/test {task-name}
       ↓
0. [ALREADY DONE] Mode Detection confirmed:
   - No --ci flag
   - Playwright MCP IS available
   - MODE = Interactive (locked in)
       ↓
1. Read task document for requirements
2. Check Automation field (manual | auto)
3. Read implementation for context
4. Create test plan
5. Check if email testing required (see Email Testing section)
   └── If auth keywords found → MUST use Mailinator
6. Execute tests via Playwright MCP tools directly
   ⚠️ DO NOT create test script files
   ⚠️ DO NOT run npx playwright test
   ⚠️ DO NOT spawn subagents for testing
7. If auth flow → Verify email received & confirmation works
8. Write report to docs/testing/{task-name}.md
9. Update TASKS.md with result
       ↓
┌─── Automation Mode? ───┐
│                        │
▼ Manual                 ▼ Auto
PASS → notify user       PASS → invoke /document
FAIL → notify user       FAIL → invoke /implement with test report
```

### CI/CD Mode (`--ci` flag) — Does NOT require Playwright MCP

**Entry condition:** `--ci` flag IS present in the command.

**IMPORTANT:** This mode is ONLY used when the user explicitly provides the `--ci` flag. Never auto-switch to this mode when Playwright MCP is unavailable.

```
/test --ci {task-name}
       ↓
0. [ALREADY DONE] Mode Detection confirmed:
   - --ci flag IS present
   - MODE = CI (locked in)
   - Playwright MCP: not required
       ↓
1. Read task document for requirements
2. Create test directory: tests/e2e/{task-name}/
3. Generate Playwright test script(s)
4. Run tests headlessly via: npx playwright test
5. Capture results and screenshots
6. Write report to docs/testing/{task-name}.md
7. Clean temporary artifacts (keep test scripts by default)
8. Update TASKS.md with result
       ↓
Same automation mode handling as interactive
```

```
/test --ci --cleanup {task-name}
       ↓
Same as above, but ALSO deletes tests/e2e/{task-name}/ at step 7
```

**CI Mode Advantages:**
- Parallel test execution
- Test scripts kept by default for regression testing
- Faster for large test suites
- Can spawn subagents for concurrent testing
- Accumulated tests run on every future PR

---

## CI Mode: Directory Structure (CRITICAL)

**You MUST follow this exact directory structure. Do NOT put files in wrong locations.**

```
project-root/
├── tests/
│   └── e2e/
│       └── {task-name}/           ← Test scripts go HERE (*.spec.ts)
│           ├── {task-name}.spec.ts
│           └── helpers.ts (if needed)
│
├── docs/
│   └── testing/
│       └── {task-name}.md         ← ONLY the final report goes HERE
│
└── (temporary - ALWAYS DELETE)
    ├── TEST_REPORT.md
    ├── TEST_CASES.md
    ├── TEST_SUMMARY.txt
    ├── test_results.md
    ├── test_execution_summary.md
    ├── TEST_REPORT_INDEX.md
    ├── playwright_mcp_test_log.md
    ├── test-screenshots/
    ├── test-results/
    └── playwright-report/
```

### PROHIBITED File Locations

**NEVER create these files in `docs/testing/`:**
- ❌ `docs/testing/TEST_CASES.md`
- ❌ `docs/testing/test_results.md`
- ❌ `docs/testing/test_execution_summary.md`
- ❌ `docs/testing/TEST_REPORT_INDEX.md`
- ❌ `docs/testing/playwright_mcp_test_log.md`
- ❌ `docs/testing/TEST_SUMMARY.txt`
- ❌ `docs/testing/*.spec.ts` (test scripts)

**ONLY allowed in `docs/testing/`:**
- ✅ `docs/testing/{task-name}.md` (final test report, one per task)
- ✅ `docs/testing/README.md` (if project has one)

---

## CI Mode: Artifact Management

### Default Behavior (Scripts Kept)

By default, `/test --ci {task-name}` **keeps test scripts** for regression testing:

```
tests/e2e/{task-name}/     ← KEPT for future regression testing
docs/testing/{task-name}.md ← KEPT as final test report (ONLY file in docs/testing/)
```

**Temporary artifacts are ALWAYS cleaned (run at end of every CI test):**
```bash
# Remove from project root
rm -f TEST_REPORT.md TEST_SUMMARY.txt TEST_CASES.md
rm -f test_results.md test_execution_summary.md TEST_REPORT_INDEX.md
rm -f playwright_mcp_test_log.md
rm -rf test-screenshots/ test-results/ playwright-report/
rm -f test-*.ts test-*.js *.spec.ts  # Root-level scripts

# Remove from docs/testing/ (ONLY final report should remain)
rm -f docs/testing/TEST_CASES.md
rm -f docs/testing/test_results.md
rm -f docs/testing/test_execution_summary.md
rm -f docs/testing/TEST_REPORT_INDEX.md
rm -f docs/testing/playwright_mcp_test_log.md
rm -f docs/testing/TEST_SUMMARY.txt
rm -f docs/testing/*.spec.ts
```

### With `--cleanup` Flag (Scripts Deleted)

When using `/test --ci --cleanup {task-name}`, test scripts are also deleted:

```bash
# Additional cleanup with --cleanup flag
rm -rf tests/e2e/{task-name}/

# Clean empty parent directories
rmdir tests/e2e 2>/dev/null || true
rmdir tests 2>/dev/null || true
```

### Artifact Summary

| Artifact | Location | `--ci` | `--ci --cleanup` |
|----------|----------|--------|------------------|
| Final test report | `docs/testing/{task-name}.md` | ✅ Keep | ✅ Keep |
| Test scripts | `tests/e2e/{task-name}/` | ✅ Keep | ❌ Delete |
| `TEST_CASES.md` | anywhere | ❌ Delete | ❌ Delete |
| `test_results.md` | anywhere | ❌ Delete | ❌ Delete |
| `test_execution_summary.md` | anywhere | ❌ Delete | ❌ Delete |
| `TEST_REPORT_INDEX.md` | anywhere | ❌ Delete | ❌ Delete |
| `playwright_mcp_test_log.md` | anywhere | ❌ Delete | ❌ Delete |
| `TEST_SUMMARY.txt` | anywhere | ❌ Delete | ❌ Delete |
| `test-screenshots/` | anywhere | ❌ Delete | ❌ Delete |
| `playwright-report/` | anywhere | ❌ Delete | ❌ Delete |
| `test-results/` | anywhere | ❌ Delete | ❌ Delete |

### Why Keep Scripts by Default?

```
Feature A: /test --ci auth-flow
  → tests/e2e/auth-flow/ KEPT

Feature B: /test --ci checkout
  → tests/e2e/checkout/ KEPT

Future PR touches auth code:
  → npx playwright test runs BOTH
  → Catches if new code breaks auth ✅
```

**Safe by default** - scripts accumulate for regression protection. Use `--cleanup` only for minor, one-time verifications.

---

## Auto Mode Behavior

When task document has `Automation: auto`:

### On PASS
Use Task tool to spawn document agent with **model: haiku**:
```
[AUTO] Tests PASSED. Spawning /document with haiku model...
```
`Task({ subagent_type: "general-purpose", model: "haiku", prompt: "/document {ID}" })`

### On FAIL
Use Task tool to spawn implement agent with **model: opus** (needs advanced reasoning to fix issues):
```
[AUTO] Tests FAILED. Spawning /implement with opus model for fixes...

Issues found:
1. {Issue summary}
2. {Issue summary}

Re-running implementation with fixes...
```
`Task({ subagent_type: "general-purpose", model: "opus", prompt: "/implement {ID} - Fix issues from test report: {summary}" })`

**Note:** The implement skill will receive the test report context and should focus on fixing the specific issues identified. After fixes, it will chain back to /test (with haiku).

**IMPORTANT:** For any task involving registration, login, magic links, or email verification:
- The test is NOT complete until email confirmation is verified via Mailinator
- See "Email-Based Authentication Testing" section for detailed steps

## Pre-Testing Setup

### 1. Read the Task Document (Primary Context Source)

```
docs/task/{ID}-{task-name}.md
```

**IMPORTANT — Context Efficiency:**
The task document contains all the context you need from the planning phase. Do NOT perform broad codebase exploration. Only read the specific files referenced in the task document.

Focus on:
- Requirements checklist
- Testing checklist (if provided)
- Expected behavior
- Files that were modified (listed in the task document)

### 2. Understand the Implementation

Review only the files that were changed (as listed in the task document):
- What was created?
- What was modified?
- What are the entry points?

**DO NOT** scan the entire codebase or read unrelated files. The task document already provides the necessary context.

### 3. Identify Test Scenarios

Create a test plan covering:
- Happy path (main use case)
- Edge cases
- Error handling
- Cross-platform (if applicable)

### 4. Detect If Email Testing Is Required

**CRITICAL:** Scan the task document for these keywords:
- Registration / Sign up / Create account
- Magic Link / OTP / Email verification
- Email confirmation / Confirm email
- Password reset / Forgot password
- Account activation

**If ANY of these keywords appear:**
1. **MANDATORY** - Use Mailinator for email testing (see "Email-Based Authentication Testing" section below)
2. **DO NOT** mark the test as PASS without verifying:
   - Email was received in Mailinator inbox
   - Confirmation/verification link works
   - Post-confirmation redirect is correct
3. Include "Authentication Tests" section in test report

**Example detection:**
```
Task doc says: "Magic Link authentication as primary signup method"
→ This REQUIRES email testing via Mailinator
→ Test is NOT complete until email verification is confirmed
```

---

## Testing with Playwright MCP

### Available Tools

Use the Playwright MCP tools for browser automation:

```
mcp__playwright__browser_navigate    - Go to URL
mcp__playwright__browser_snapshot    - Capture accessibility snapshot
mcp__playwright__browser_click       - Click elements
mcp__playwright__browser_type        - Type text
mcp__playwright__browser_fill_form   - Fill form fields
mcp__playwright__browser_take_screenshot - Capture screenshot
mcp__playwright__browser_console_messages - Check console
mcp__playwright__browser_network_requests - Check network
mcp__playwright__browser_wait_for    - Wait for conditions
```

### Test Execution Pattern

```typescript
// 1. Navigate to the page
mcp__playwright__browser_navigate({ url: "http://localhost:3000/path" })

// 2. Take snapshot to understand page structure
mcp__playwright__browser_snapshot()

// 3. Interact with elements (use ref from snapshot)
mcp__playwright__browser_click({ ref: "button[Submit]", element: "Submit button" })

// 4. Verify results
mcp__playwright__browser_snapshot()

// 5. Check for errors
mcp__playwright__browser_console_messages({ level: "error" })
```

### Responsive Testing

For responsive web features, resize the viewport:

```typescript
mcp__playwright__browser_resize({ width: 390, height: 844 }) // iPhone 14 Pro
mcp__playwright__browser_resize({ width: 768, height: 1024 }) // iPad
```

---

## Test Report Template

Create report in `docs/testing/{ID}-{task-name}.md`:

```markdown
# Test Report: {Task Name}

> **Task ID:** {ID}
> **Status:** PASS | FAIL | PARTIAL
> **Tested:** {Date}
> **Task Doc:** [link](../task/{ID}-{task-name}.md)

## Summary

{1-2 sentence summary of test results}

## Test Environment

- Platform: Web
- Browser: Chromium (Playwright)
- Base URL: http://localhost:3000
- Viewport: {dimensions if relevant}

## Test Results

### Requirement Tests

| # | Requirement | Status | Notes |
|---|-------------|--------|-------|
| 1 | {Requirement from task doc} | PASS/FAIL | {Details} |
| 2 | {Requirement} | PASS/FAIL | {Details} |

### Functional Tests

#### Test 1: {Test Name}
**Steps:**
1. Navigate to {page}
2. Click {element}
3. Verify {expected result}

**Result:** PASS/FAIL
**Evidence:** {Screenshot or description}

#### Test 2: {Test Name}
{Same format}

### Edge Cases

| Case | Result | Notes |
|------|--------|-------|
| Empty state | PASS/FAIL | {Details} |
| Error handling | PASS/FAIL | {Details} |
| Loading state | PASS/FAIL | {Details} |

### Console Errors

```
{Any console errors found, or "None"}
```

### Network Issues

```
{Any failed requests, or "None"}
```

## Issues Found

### Issue 1: {Title}
**Severity:** Critical | Major | Minor
**Description:** {What's wrong}
**Steps to Reproduce:**
1. Step 1
2. Step 2
**Expected:** {What should happen}
**Actual:** {What actually happens}
**Screenshot:** {If applicable}

### Issue 2: {Title}
{Same format}

## Screenshots

{Include relevant screenshots}

## Recommendations

{Any suggestions for fixes or improvements}

## Verdict

**PASS** - All requirements met, ready for documentation
OR
**FAIL** - Issues found, needs fixes (see Issues section)
OR
**PARTIAL** - Core functionality works, minor issues noted
```

---

## Update TASKS.md

### If PASS

Move to "Approved" section (pending user approval):

```markdown
## Testing

| ID | Task | Task Doc | Test Report | Status |
|----|------|----------|-------------|--------|
| 1 | Quick Actions Redesign | [001-quick-actions.md](...) | [001-quick-actions.md](docs/testing/001-quick-actions.md) | PASS - Awaiting approval |
```

### If FAIL

Keep in "Testing" with failure note:

```markdown
## Testing

| ID | Task | Task Doc | Test Report | Status |
|----|------|----------|-------------|--------|
| 1 | Quick Actions Redesign | [001-quick-actions.md](...) | [001-quick-actions.md](docs/testing/001-quick-actions.md) | FAIL - See report |
```

---

## Handoff

**Check the task document for `Automation: auto` field.**

### Manual Mode

#### On PASS
```
Testing complete: #{ID} - {Task Title}

Result: PASS
Test Report: docs/testing/{ID}-{task-name}.md

All requirements verified. Ready for your approval.

Next Steps (after approval):
  /document {ID}              # e.g., /document 1
  /document {ID}-{task-name}  # e.g., /document 001-auth-jwt
```

#### On FAIL
```
Testing complete: #{ID} - {Task Title}

Result: FAIL
Test Report: docs/testing/{ID}-{task-name}.md

Issues found:
1. {Issue summary 1}
2. {Issue summary 2}

Next Steps (fix and re-test):
  /implement {ID}             # e.g., /implement 1
  /implement {ID}-{task-name} # e.g., /implement 001-auth-jwt

Then re-run:
  /test {ID}
```

### Auto Mode

#### On PASS
```
Testing complete: #{ID} - {Task Title}

Result: PASS
Test Report: docs/testing/{ID}-{task-name}.md

[AUTO] Spawning /document with haiku model...
```
Use Task tool: `Task({ subagent_type: "general-purpose", model: "haiku", prompt: "/document {ID}" })`

#### On FAIL
```
Testing complete: #{ID} - {Task Title}

Result: FAIL
Test Report: docs/testing/{ID}-{task-name}.md

Issues found:
1. {Issue summary 1}
2. {Issue summary 2}

[AUTO] Spawning /implement with opus model for fixes...
```
Use Task tool: `Task({ subagent_type: "general-purpose", model: "opus", prompt: "/implement {ID} - Fix: {issue summaries}" })`

---

## Email-Based Authentication Testing

For testing account registration, email verification, password reset, and email notifications using temporary email services.

**CRITICAL:** Tests involving email verification, account activation, password reset, or any email-dependent flow MUST NOT be marked as PASS until the email verification is confirmed working. If email testing fails due to service limits, mark the test as **BLOCKED** and notify the user to take action.

### Supported Email Services (Priority Order)

| Priority | Service | Method | Domain | Best For |
|----------|---------|--------|--------|----------|
| 1st | **Mail.tm** | API | Dynamic (`@mail.tm`, etc.) | Primary - high limits, API-based |
| 2nd | **Mailinator** | Browser | `@mailinator.com` | Fallback - no signup required |
| 3rd | **Guerrilla Mail** | Browser | Dynamic | Fallback if others blocked |
| 4th | **TempMail** | Browser | Dynamic | Last resort |

**Always start with Mail.tm.** Only fall back to other services if Mail.tm returns rate limit errors (HTTP 429) or account creation fails.

### Email Testing Workflow

```
1. Create temporary email via Mail.tm API
2. Navigate to registration/action page
3. Fill form with temporary email
4. Poll Mail.tm API for incoming email
5. Extract verification link from email
6. Complete verification flow
7. Verify account is active
8. Include email test results in report
```

---

### Mail.tm API Reference (Primary Service)

Mail.tm provides a REST API for creating temporary emails and retrieving messages.

**Base URL:** `https://api.mail.tm`

#### Step 1: Get Available Domain

```bash
# Get list of available domains
curl https://api.mail.tm/domains

# Response example:
# { "hydra:member": [{ "id": "...", "domain": "mail.tm" }] }
```

#### Step 2: Create Temporary Account

```bash
# Create account with random address
curl -X POST https://api.mail.tm/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "address": "test-1706234567890@mail.tm",
    "password": "TestPassword123!"
  }'

# Response: { "id": "...", "address": "test-...@mail.tm" }
```

#### Step 3: Get Authentication Token

```bash
# Get JWT token for API access
curl -X POST https://api.mail.tm/token \
  -H "Content-Type: application/json" \
  -d '{
    "address": "test-1706234567890@mail.tm",
    "password": "TestPassword123!"
  }'

# Response: { "token": "eyJ..." }
```

#### Step 4: Poll for Messages

```bash
# Check inbox (poll every 3-5 seconds)
curl https://api.mail.tm/messages \
  -H "Authorization: Bearer {token}"

# Response: { "hydra:member": [{ "id": "...", "subject": "...", "from": {...} }] }
```

#### Step 5: Get Message Content

```bash
# Get full message with HTML content
curl https://api.mail.tm/messages/{messageId} \
  -H "Authorization: Bearer {token}"

# Response includes: { "html": "<html>...", "text": "..." }
# Extract verification link from html or text field
```

---

### Step-by-Step: Account Registration Test

#### Step 1: Create Mail.tm Account via Bash

```bash
# Generate unique email address
TIMESTAMP=$(date +%s)
RANDOM_STR=$(head /dev/urandom | tr -dc a-z0-9 | head -c 4)
TEST_EMAIL="test-${TIMESTAMP}-${RANDOM_STR}@mail.tm"
TEST_PASSWORD="TestPassword123!"

# Get available domain (verify mail.tm is available)
curl -s https://api.mail.tm/domains | jq '.["hydra:member"][0].domain'

# Create the temporary email account
curl -s -X POST https://api.mail.tm/accounts \
  -H "Content-Type: application/json" \
  -d "{\"address\": \"${TEST_EMAIL}\", \"password\": \"${TEST_PASSWORD}\"}"

# Get authentication token
TOKEN=$(curl -s -X POST https://api.mail.tm/token \
  -H "Content-Type: application/json" \
  -d "{\"address\": \"${TEST_EMAIL}\", \"password\": \"${TEST_PASSWORD}\"}" \
  | jq -r '.token')

echo "Test email: ${TEST_EMAIL}"
echo "Token: ${TOKEN}"
```

#### Step 2: Navigate to Registration Page

```typescript
mcp__playwright__browser_navigate({ url: "http://localhost:3000/register" })
mcp__playwright__browser_snapshot()
```

#### Step 3: Fill Registration Form

```typescript
// Get element refs from snapshot, then fill form
// Use the TEST_EMAIL created in Step 1
mcp__playwright__browser_fill_form({
  fields: [
    { name: "Email", type: "textbox", ref: "input[email]", value: TEST_EMAIL },
    { name: "Password", type: "textbox", ref: "input[password]", value: "TestPassword123!" },
    { name: "Confirm Password", type: "textbox", ref: "input[confirmPassword]", value: "TestPassword123!" }
  ]
})
mcp__playwright__browser_click({ ref: "button[Submit]", element: "Submit button" })
```

#### Step 4: Poll Mail.tm for Verification Email

```bash
# Poll for messages (repeat every 5 seconds, up to 60 seconds)
for i in {1..12}; do
  MESSAGES=$(curl -s https://api.mail.tm/messages \
    -H "Authorization: Bearer ${TOKEN}")

  COUNT=$(echo $MESSAGES | jq '.["hydra:member"] | length')

  if [ "$COUNT" -gt "0" ]; then
    echo "Email received!"
    MESSAGE_ID=$(echo $MESSAGES | jq -r '.["hydra:member"][0].id')
    break
  fi

  echo "Waiting for email... attempt $i/12"
  sleep 5
done
```

#### Step 5: Extract Verification Link

```bash
# Get full message content
MESSAGE=$(curl -s https://api.mail.tm/messages/${MESSAGE_ID} \
  -H "Authorization: Bearer ${TOKEN}")

# Extract verification link from HTML content
# Adjust the grep pattern based on your auth provider
VERIFY_LINK=$(echo $MESSAGE | jq -r '.html' | grep -oP 'href="\K[^"]*confirm[^"]*' | head -1)

# Or from text content
VERIFY_LINK=$(echo $MESSAGE | jq -r '.text' | grep -oP 'https?://[^\s]*confirm[^\s]*' | head -1)

echo "Verification link: ${VERIFY_LINK}"
```

#### Step 6: Complete Verification

```typescript
// Navigate to the verification link
mcp__playwright__browser_navigate({ url: VERIFY_LINK })
mcp__playwright__browser_snapshot()
// Should see success message or redirect to dashboard
```

---

### Password Reset Testing

```bash
# 1. Use the same Mail.tm account created earlier
# 2. Trigger password reset in the app
# 3. Poll for reset email
MESSAGES=$(curl -s https://api.mail.tm/messages \
  -H "Authorization: Bearer ${TOKEN}")

MESSAGE_ID=$(echo $MESSAGES | jq -r '.["hydra:member"][0].id')

# 4. Extract reset link
MESSAGE=$(curl -s https://api.mail.tm/messages/${MESSAGE_ID} \
  -H "Authorization: Bearer ${TOKEN}")

RESET_LINK=$(echo $MESSAGE | jq -r '.html' | grep -oP 'href="\K[^"]*reset[^"]*' | head -1)
```

---

### Email Notification Testing

For testing transactional emails (booking confirmations, notifications, etc.):

```bash
# 1. Trigger the action that sends email (e.g., make a booking via Playwright)
# 2. Poll Mail.tm for notification (may take longer)
for i in {1..24}; do  # Up to 2 minutes
  MESSAGES=$(curl -s https://api.mail.tm/messages \
    -H "Authorization: Bearer ${TOKEN}")

  # Look for specific subject
  NOTIFICATION=$(echo $MESSAGES | jq -r '.["hydra:member"][] | select(.subject | contains("Booking"))')

  if [ -n "$NOTIFICATION" ]; then
    echo "Notification received!"
    break
  fi

  sleep 5
done

# 3. Verify email content
MESSAGE_ID=$(echo $NOTIFICATION | jq -r '.id')
MESSAGE=$(curl -s https://api.mail.tm/messages/${MESSAGE_ID} \
  -H "Authorization: Bearer ${TOKEN}")

# Validate content
echo $MESSAGE | jq '.html' | grep -q "booking details" && echo "Content valid"
```

---

### Fallback: When Mail.tm Hits Rate Limits

If Mail.tm returns HTTP 429 (Too Many Requests) or account creation fails:

#### Fallback to Mailinator (Browser-based)

```typescript
// Generate Mailinator email (no account creation needed)
const testEmail = `test-${Date.now()}@mailinator.com`;
const inboxName = testEmail.split('@')[0];

// After triggering email, navigate to inbox
mcp__playwright__browser_navigate({
  url: `https://www.mailinator.com/v4/public/inboxes.jsp?to=${inboxName}`
})
mcp__playwright__browser_wait_for({ time: 10 })
mcp__playwright__browser_snapshot()

// Click on email row and extract link
mcp__playwright__browser_click({ ref: "row[YourApp]", element: "Email from app" })
mcp__playwright__browser_snapshot()
```

#### Fallback to Guerrilla Mail (Browser-based)

```typescript
// Navigate to Guerrilla Mail
mcp__playwright__browser_navigate({ url: "https://www.guerrillamail.com/" })
mcp__playwright__browser_snapshot()

// Get the generated email address from the page
// Use this address for registration
// Check inbox on the same page for incoming emails
```

---

### Troubleshooting

| Issue | Solution |
|-------|----------|
| Mail.tm 429 error | Switch to Mailinator fallback |
| Mail.tm account creation fails | Try different domain from /domains endpoint |
| Email not arriving (60s+) | Check spam, verify email was sent, try fallback |
| Mailinator rate limited | Switch to Guerrilla Mail |
| All services failing | Mark test as BLOCKED, notify user |
| Can't extract link | Check HTML/text parsing, adjust regex pattern |
| Supabase rate limiting | Wait 60s between tests, use different emails |

### When to Mark Test as BLOCKED

Mark the test as **BLOCKED** (not FAIL) when:
- All email services are rate-limited
- Cannot create temporary email account
- Email never arrives after 2+ minutes across multiple services

```markdown
**Result:** BLOCKED
**Reason:** Email service rate limits reached
**Action Required:** User must manually verify email flow or wait for rate limits to reset
```

---

### Test Report: Email Authentication Section

Add to test report when testing auth flows:

```markdown
### Authentication Tests

| Test | Email Service | Email Used | Result | Notes |
|------|---------------|------------|--------|-------|
| Registration | Mail.tm | test-xxx@mail.tm | PASS/FAIL/BLOCKED | {Details} |
| Email verification | Mail.tm | (same) | PASS/FAIL/BLOCKED | Link received in Xs |
| Password reset | Mail.tm | (same) | PASS/FAIL/BLOCKED | {Details} |
| Login after verify | - | (same) | PASS/FAIL | {Details} |

### Email Delivery

| Email Type | Service Used | Received | Time | Content Valid |
|------------|--------------|----------|------|---------------|
| Verification | Mail.tm | Yes/No | Xs | Yes/No |
| Password Reset | Mail.tm | Yes/No | Xs | Yes/No |
| Booking Confirm | Mail.tm | Yes/No | Xs | Yes/No |

### Service Fallback Log (if applicable)

| Attempt | Service | Result | Error |
|---------|---------|--------|-------|
| 1 | Mail.tm | Failed | 429 Too Many Requests |
| 2 | Mailinator | Success | - |
```

---

## Manual Testing Guidance

For features that can't be fully automated:

### What to Test Manually

- Complex user interactions
- Visual design accuracy
- Animation smoothness

### Document Manual Tests

Include in report:

```markdown
## Manual Testing Required

| Test | Instructions | Expected Result |
|------|--------------|-----------------|
| Visual accuracy | Compare to design | Matches mockup |
| Animation | Trigger X action | Smooth 60fps |
```

---

## Related Skills

| Skill | When to Use |
|-------|-------------|
| `/implement` | When tests fail, return to implement |
| `/document` | After tests pass and user approves |

## Recommended Plugins (Install Separately)

These plugins must be installed separately. **Once installed, they MUST be invoked** — do not skip them:

| Plugin | Install From | When to Invoke |
|--------|--------------|----------------|
| `vercel-react-best-practices` | [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | React/Next.js debugging |
| `supabase-postgres-best-practices` | [supabase/agent-skills](https://github.com/supabase/agent-skills) | Database-related test issues |
