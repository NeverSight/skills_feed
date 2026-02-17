---
name: debugging
description: Debug web and Node.js applications using console inspection, network analysis, and non-blocking code debugging. Use when the user reports bugs, wants to debug JavaScript (browser or backend), inspect network requests, troubleshoot page/API issues, trace function calls, or monitor exceptions.
allowed-tools: Bash(browser-devtools-cli:*), Bash(node-devtools-cli:*)
---

# Debugging Skill

Debug web applications and Node.js backends using console inspection, network analysis, and non-blocking code debugging with tracepoints, logpoints, and exception monitoring.

## When to Use

This skill activates when:
- User reports a bug or error on a web page or backend
- User asks to debug JavaScript (frontend or Node.js)
- User wants to inspect API calls or network requests
- User needs to troubleshoot page loading or API handler issues
- User mentions console errors or warnings
- User wants to debug without breakpoints
- User needs to trace function calls or monitor variables

## Capabilities

### Console Inspection
```bash
browser-devtools-cli o11y get-console-messages
browser-devtools-cli o11y get-console-messages --types error,warn
browser-devtools-cli --json o11y get-console-messages --types error
```

### Network Analysis
```bash
browser-devtools-cli o11y get-http-requests
browser-devtools-cli --json o11y get-http-requests --resource-type fetch,xhr
browser-devtools-cli --json o11y get-http-requests --status-min 400
```

### JavaScript Execution
```bash
browser-devtools-cli run js-in-browser --script "document.title"
browser-devtools-cli run js-in-browser --script "localStorage.getItem('token')"
browser-devtools-cli run js-in-sandbox --code "return await page.evaluate(() => window.myVar)"
```

### Tracepoints (Non-Blocking)
```bash
browser-devtools-cli debug put-tracepoint --url-pattern "app.js" --line-number 42
browser-devtools-cli debug list-tracepoints
browser-devtools-cli debug remove-tracepoint --id <tracepoint-id>
browser-devtools-cli debug clear-tracepoints
```

### Logpoints
```bash
browser-devtools-cli debug put-logpoint --url-pattern "app.js" --line-number 50 --expression "user.id"
browser-devtools-cli debug list-logpoints
browser-devtools-cli debug clear-logpoints
```

### Exception Monitoring
```bash
browser-devtools-cli debug put-exceptionpoint --state uncaught
browser-devtools-cli debug put-exceptionpoint --state all
```

### DOM Mutation Monitoring
```bash
browser-devtools-cli debug put-dompoint --selector "#content" --type subtree-modified
browser-devtools-cli debug put-dompoint --selector "#element" --type attribute-modified
browser-devtools-cli debug list-dompoints
browser-devtools-cli debug clear-dompoints
```

### Network Point Monitoring
```bash
browser-devtools-cli debug put-netpoint --url-pattern "/api/*"
browser-devtools-cli debug list-netpoints
browser-devtools-cli debug clear-netpoints
```

### Watch Expressions
```bash
browser-devtools-cli debug add-watch --expression "this"
browser-devtools-cli debug add-watch --expression "user.id"
browser-devtools-cli debug list-watches
browser-devtools-cli debug clear-watches
```

### Retrieve Snapshots
```bash
browser-devtools-cli --json debug get-tracepoint-snapshots
browser-devtools-cli --json debug get-logpoint-snapshots
browser-devtools-cli --json debug get-exceptionpoint-snapshots
browser-devtools-cli --json debug get-dompoint-snapshots
browser-devtools-cli --json debug get-netpoint-snapshots
```

### Node.js Backend Debugging (node-devtools-cli)

For debugging Node.js API servers, backends, or scripts:

```bash
# 1. Connect to process (by PID, name, or Docker)
node-devtools-cli --session-id backend-debug debug connect --pid 12345
node-devtools-cli --session-id backend-debug debug connect --process-name "server.js"

# 2. Tracepoint on route handler or service
node-devtools-cli --session-id backend-debug debug put-tracepoint \
  --url-pattern "routes/api.ts" \
  --line-number 42

# 3. Exception monitoring
node-devtools-cli --session-id backend-debug debug put-exceptionpoint --state uncaught

# 4. Console logs from Node process
node-devtools-cli --session-id backend-debug --json debug get-logs
node-devtools-cli --session-id backend-debug --json debug get-logs --search "error"

# 5. Run JavaScript in the connected process
node-devtools-cli --session-id backend-debug run js-in-node --script "process.memoryUsage()"

# 6. Retrieve snapshots (after triggering the code path)
node-devtools-cli --session-id backend-debug --json debug get-tracepoint-snapshots
node-devtools-cli --session-id backend-debug --json debug get-exceptionpoint-snapshots

# 7. Status and cleanup
node-devtools-cli --session-id backend-debug debug status
node-devtools-cli debug disconnect
```

`urlPattern` in Node context matches **script file paths** (e.g., `server.js`, `routes/users.ts`). See [node-devtools-cli](../node-devtools-cli/SKILL.md) skill for full reference.

### Error Investigation
```bash
browser-devtools-cli content take-screenshot --name "error-state"
browser-devtools-cli content get-as-html --selector ".error-container"
```

## Basic Debugging Workflow

1. **Reproduce**: Navigate to the problematic page
2. **Capture**: Take screenshot of current state
3. **Inspect Console**: Check for JavaScript errors
4. **Analyze Network**: Look for failed requests
5. **Investigate**: Run diagnostic JavaScript
6. **Document**: Summarize findings with evidence

```bash
# Quick debug workflow
browser-devtools-cli navigation go-to --url "https://example.com"
browser-devtools-cli content take-screenshot --name "initial"
browser-devtools-cli --json o11y get-console-messages --types error,warn
browser-devtools-cli --json o11y get-http-requests --status-min 400
```

## Advanced Debugging Workflow (Non-Blocking)

### 1. Set Up Probes

```bash
SESSION="--session-id debug-session"

# Navigate to app
browser-devtools-cli $SESSION navigation go-to --url "http://localhost:3000"

# Tracepoint on a function
browser-devtools-cli $SESSION debug put-tracepoint \
  --url-pattern "app.js" \
  --line-number 42

# Exception monitoring
browser-devtools-cli $SESSION debug put-exceptionpoint --state uncaught

# Network monitoring
browser-devtools-cli $SESSION debug put-netpoint --url-pattern "/api/*"

# DOM mutation monitoring
browser-devtools-cli $SESSION debug put-dompoint \
  --selector "#dynamic-content" \
  --type subtree-modified
```

### 2. Add Watch Expressions

```bash
browser-devtools-cli $SESSION debug add-watch --expression "this"
browser-devtools-cli $SESSION debug add-watch --expression "user.id"
```

### 3. Interact with Application

```bash
browser-devtools-cli $SESSION interaction click --selector "#submit-btn"
browser-devtools-cli $SESSION sync wait-for-network-idle
```

### 4. Retrieve Snapshots

```bash
browser-devtools-cli $SESSION --json debug get-tracepoint-snapshots
browser-devtools-cli $SESSION --json debug get-exceptionpoint-snapshots
browser-devtools-cli $SESSION --json debug get-netpoint-snapshots
browser-devtools-cli $SESSION --json debug get-dompoint-snapshots
```

### 5. Clean Up

```bash
browser-devtools-cli $SESSION debug clear-tracepoints
browser-devtools-cli $SESSION debug clear-watches
browser-devtools-cli session delete debug-session
```

## Probe Types Summary

| Probe | Purpose | Output | CLI |
|-------|---------|--------|-----|
| Tracepoint | Function calls | Stack, locals, watches | browser-devtools-cli, node-devtools-cli |
| Logpoint | Expression values | Evaluated result | both |
| Exceptionpoint | Error catching | Error, stack trace | both |
| Dompoint | DOM mutations | Changed nodes | browser-devtools-cli only |
| Netpoint | Network calls | Request/response | browser-devtools-cli only |

## Best Practices

1. **Choose the right CLI**: Use `browser-devtools-cli` for frontend/page debugging; use `node-devtools-cli` for Node.js backend/API debugging
2. **Always check console for errors first**
3. **Filter network requests** to relevant endpoints
4. **Take screenshots** before and after actions (browser)
5. **Use source maps** for minified/bundled code
6. **Start with exceptions** to catch errors first
7. **Use logpoints** for lightweight monitoring
8. **Poll snapshots** with `--from-sequence` for efficiency
9. **Clear probes** when done to avoid overhead
10. **Document reproduction steps** clearly
