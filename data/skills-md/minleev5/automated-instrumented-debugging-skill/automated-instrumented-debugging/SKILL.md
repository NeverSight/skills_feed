---
name: automated-instrumented-debugging
description: A systematic debugging capability that automates evidence collection via dynamic instrumentation. Use when manual tracing is tedious or environment is restricted.
allowed-tools: replace_file_content, run_command, read_url_content
---

# Automated Instrumented Debugging

> **Core Philosophy**: Don't guess. Instrument, measure, and let the data reveal the root cause.

## Overview

This skill empowers you to debug complex issues by systematically injecting lightweight probes (`fetch` calls) into the codebase. These probes stream real-time execution data (function entries, variable states, errors) to a local debug server, allowing you to reconstruct the exact execution flow without relying on scattered console logs or interactive debuggers.

## When to Use

- **Complexity**: The bug involves data flow across 3+ functions or asynchronous chains.
- **Invisibility**: Code runs in blind environments (Docker, CI, remote servers).
- **Persistency**: You need to analyze the chronology of events post-execution.
- **Systematic Analysis**: You need hard evidence to prove a hypothesis.

## Systematic Debugging Process

Follow this 4-phase loop to resolve issues efficiently.

### Phase 1: Strategy & Setup

Don't rush to code. First, define what you need to capture.

1. **Start Server**: Ensure `bootstrap.js` is running (`node .agent/skills/automated-instrumented-debugging/scripts/bootstrap.js`).
2. **Hypothesize**: What variable or flow is likely broken?
3. **Plan Probes**: Decide where to place `#region DEBUG` blocks (Entry, Exit, Error, State).

### Phase 2: Instrumentation (The "Probe")

Inject probes using the standard templates. **Always** use the `#region DEBUG` wrapper for easy cleanup.

- **Trace Flow**: Log Function Entry/Exit to see the path.
- **Snapshot State**: Log local variables and arguments.
- **Catch Errors**: Log `try-catch` blocks in critical paths.

_(See "Instrumentation Templates" below for code patterns)_

### Phase 3: Evidence Collection & Analysis

Run the reproduction case and let the data speak.

1. **Trigger**: Run the test/script to reproduce the bug.
2. **Query**: Fetch logs via `curl http://localhost:9876/logs/{session}`.
3. **Analyze**:
   - _Did the function get called?_ (Check Entry logs)
   - _Was the data correct?_ (Check Variable logs)
   - _Where did it crash?_ (Check Error logs/Last successful log)

### Phase 4: Resolution & Cleanup

Fix the root cause and restore the codebase.

1. **Fix**: Apply the fix based on evidence.
2. **Verify**: Run tests to confirm the fix.
3. **Cleanup**: **Crucial!** Remove all `#region DEBUG` blocks using the cleanup script:
   ```bash
   node .agent/skills/automated-instrumented-debugging/scripts/cleanup.js
   ```
4. **Shutdown**: Stop the debug server if no longer needed.

## Instrumentation Templates

### 1. Function Entry (Trace Path)

```typescript
// #region DEBUG - {SESSION}
fetch('http://localhost:9876/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session: '{SESSION}',
    type: 'enter',
    fn: '{FUNC}',
    file: '{FILE_PATH}', // Use absolute path or relative to project root
    data: { arg1, arg2 }, // Snapshot arguments
  }),
}).catch(() => {});
// #endregion
```

### 2. Variable Snapshot (Inspect State)

```typescript
// #region DEBUG - {SESSION}
fetch('http://localhost:9876/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session: '{SESSION}',
    type: 'var',
    fn: '{FUNC}',
    file: '{FILE_PATH}',
    data: { varName: value },
  }),
}).catch(() => {});
// #endregion
```

### 3. Function Exit (Result & Timing)

```typescript
// #region DEBUG - {SESSION}
fetch('http://localhost:9876/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session: '{SESSION}',
    type: 'exit',
    fn: '{FUNC}',
    data: { result },
  }),
}).catch(() => {});
// #endregion
```

### 4. Error Capture (Catch & Report)

```typescript
// #region DEBUG - {SESSION}
fetch('http://localhost:9876/log', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session: '{SESSION}',
    type: 'error',
    fn: '{FUNC}',
    data: { error: err.message, stack: err.stack },
  }),
}).catch(() => {});
// #endregion
```

## Anti-Patterns

❌ **Sync Fetch Trap**: Using `fetch` without considering execution order in critical paths.
-> _Fix_: Always use `.catch(() => {})` and place probes _after_ variable definitions.

❌ **Committing Probes**: Forgetting to run `cleanup.js`.
-> _Fix_: Add `cleanup` as a mandatory step in your "Resolution & Cleanup" workflow.
