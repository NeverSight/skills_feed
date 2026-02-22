---
name: node-devtools-cli
description: CLI for debugging Node.js backend processes with non-blocking inspection. Use when the user needs to connect to Node.js processes (by PID, name, Docker, or port), set tracepoints/logpoints/exceptionpoints, capture call stacks and local variables, run JavaScript in the process context, or inspect console logs. Requires daemon; connect before other debug commands.
allowed-tools: Bash(node-devtools-cli:*)
---

# Node DevTools CLI

Command-line interface for non-blocking debugging of Node.js backend processes. Connects via the Inspector Protocol (Chrome DevTools Protocol) and provides tracepoints, logpoints, exceptionpoints, and watch expressions without pausing execution.

## Installation

Same package as browser-devtools-mcp:

```bash
npm install -g browser-devtools-mcp
```

## Quick Start

```bash
# 1. Start daemon (if not running)
node-devtools-cli daemon start

# 2. Connect to a Node.js process (by PID)
node-devtools-cli --session-id my-debug debug connect --pid 12345

# 3. Set a tracepoint on server.js line 42
node-devtools-cli --session-id my-debug debug put-tracepoint \
  --url-pattern "server.js" \
  --line-number 42

# 4. Trigger the code path (e.g., make API request to your app)
# 5. Get captured snapshots
node-devtools-cli --session-id my-debug --json debug get-tracepoint-snapshots
```

## Global Options

| Option | Description | Default |
|--------|-------------|---------|
| `--port <number>` | Daemon server port | `2020` |
| `--session-id <string>` | Session for Node connection persistence | auto |
| `--json` | Output as JSON (recommended for AI) | `false` |
| `--quiet` | Suppress log messages | `false` |
| `--verbose` | Enable debug output | `false` |
| `--timeout <ms>` | Operation timeout | `30000` |

**AI Agent Recommended:**

```bash
node-devtools-cli --json --quiet --session-id "debug-session" <command>
```

## Tool Domains

| Domain | Description | Reference |
|--------|-------------|-----------|
| [debug](./references/debug.md) | Connection, tracepoints, logpoints, exceptionpoints, watch, snapshots |
| run | JavaScript execution in connected Node process |

## Connection Methods

Connect via `debug connect` with one of:

| Method | Option | Example |
|--------|--------|---------|
| PID | `--pid <number>` | `--pid 12345` |
| Process name | `--process-name <pattern>` | `--process-name "server.js"` |
| Docker container | `--container-id` or `--container-name` | `--container-name my-api` |
| Inspector port | `--port <number>` | `--port 9229` |
| WebSocket URL | `--ws-url <url>` | `--ws-url "ws://127.0.0.1:9229/abc"` |

If the process doesn't have `--inspect` active, the CLI activates it via SIGUSR1 (no code changes). For Docker: expose port 9229 and use `--inspect=0.0.0.0:9229`.

## CLI Management Commands

### Daemon

```bash
node-devtools-cli daemon status
node-devtools-cli daemon start
node-devtools-cli daemon stop
node-devtools-cli daemon restart
node-devtools-cli daemon info
```

### Session

```bash
node-devtools-cli session list
node-devtools-cli session info <session-id>
node-devtools-cli session delete <session-id>
```

### Tools

```bash
node-devtools-cli tools list
node-devtools-cli tools search <query>
node-devtools-cli tools info <tool-name>
```

### Config & Updates

```bash
node-devtools-cli config
node-devtools-cli update --check
```

## Examples

### Connect by PID

```bash
SESSION="--session-id api-debug"

# Connect
node-devtools-cli $SESSION debug connect --pid $(pgrep -f "node server.js")

# Set tracepoint on route handler
node-devtools-cli $SESSION debug put-tracepoint \
  --url-pattern "routes/api.ts" \
  --line-number 25

# Trigger: curl http://localhost:3000/api/users
# Get snapshots
node-devtools-cli $SESSION --json debug get-tracepoint-snapshots
```

### Connect by Process Name

```bash
node-devtools-cli debug connect --process-name "api"
```

### Docker Container

```bash
# App runs in container with -p 9229:9229
node-devtools-cli debug connect \
  --container-name my-node-app \
  --host host.docker.internal \
  --port 9229
```

### Exception Catching

```bash
SESSION="--session-id exc-debug"

node-devtools-cli $SESSION debug connect --pid 12345
node-devtools-cli $SESSION debug put-exceptionpoint --state uncaught

# Trigger error in app
# Check snapshots
node-devtools-cli $SESSION --json debug get-exceptionpoint-snapshots
```

### Run JS in Node Process

```bash
# After connect
node-devtools-cli run js-in-node --script "process.memoryUsage()"
node-devtools-cli run js-in-node --script "require('os').loadavg()"
```

## Interactive Mode

```bash
node-devtools-cli interactive
```

| Command | Description |
|---------|-------------|
| `help` | Show commands |
| `exit`, `quit` | Exit |
| `debug connect` | Connect to process |
| `debug status` | Connection status |
| `<domain> <tool>` | Execute tool |

## Shell Completions

```bash
eval "$(node-devtools-cli completion bash)"
eval "$(node-devtools-cli completion zsh)"
```
