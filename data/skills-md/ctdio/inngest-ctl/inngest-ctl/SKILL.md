---
name: inngest-ctl
description: |
  Inngest CLI for querying events and function runs. Use this skill when you need to:
  list Inngest events, send events, get event details, check run status, monitor job duration,
  list runs for an event, or cancel running functions. Trigger phrases include "list events",
  "send event", "event status", "run status", "check run", "cancel run", "inngest events",
  "function runs", "job status".
---

# inngest-ctl Reference

A CLI tool for interacting with Inngest events and function runs.

## Setup

### Running the CLI

```bash
# Via bunx (no install needed)
bunx @ctdio/inngest-ctl <command>

# Or create an alias
alias inngest-ctl="bunx @ctdio/inngest-ctl"
```

### Environment Variables (Required)

```bash
export INNGEST_EVENT_KEY="your-event-key"      # For sending events
export INNGEST_SIGNING_KEY="your-signing-key"  # For API queries
```

### For Local Dev Server

Use `--dev` flag:
```bash
inngest-ctl events list --dev --pretty
```

Override URL:
```bash
export INNGEST_DEV_URL="http://localhost:9000"
```

## Commands

### List Events

```bash
inngest-ctl events list [--name <name>] [--limit <n>] [--pretty] [--dev]
```

**Examples:**
```bash
inngest-ctl events list --pretty
inngest-ctl events list --name "user.signup" --limit 10 --pretty
inngest-ctl events list --dev --pretty
```

### Send Event

```bash
inngest-ctl events send --name "<name>" --data '<json>' [--id <id>] [--env <env>] [--dev]
```

**Examples:**
```bash
inngest-ctl events send --name "user.signup" --data '{"userId": "123"}'
inngest-ctl events send --name "test.event" --data '{}' --dev
inngest-ctl events send --name "order.created" --data '{"orderId": "o1"}' --env "feature/my-branch"
```

### Get Event Details

```bash
inngest-ctl events get <event-id> [--pretty] [--dev]
```

**Example:**
```bash
inngest-ctl events get 01H08W4TMBNKMEWFD0TYC532GG --pretty
```

### List Runs for Event

```bash
inngest-ctl events runs <event-id> [--pretty] [--dev]
```

**Example:**
```bash
inngest-ctl events runs 01H08W4TMBNKMEWFD0TYC532GG --pretty
```

### Get Run Status

Monitor run status and duration.

```bash
inngest-ctl runs status <run-id> [--pretty] [--dev]
```

**Example:**
```bash
inngest-ctl runs status 01H08W5TMBNKMEWFD0TYC532GH --pretty
```

### Get Run Details (Jobs/Steps)

```bash
inngest-ctl runs get <run-id> [--pretty] [--dev]
```

**Example:**
```bash
inngest-ctl runs get 01H08W5TMBNKMEWFD0TYC532GH --pretty
```

### List Runs by Event

```bash
inngest-ctl runs list --event <event-id> [--pretty] [--dev]
```

**Example:**
```bash
inngest-ctl runs list --event 01H08W4TMBNKMEWFD0TYC532GG --pretty
```

### Cancel Runs

```bash
inngest-ctl cancel --app <app> --function <fn> --started-after <time> --started-before <time> [--if <expr>]
```

**Example:**
```bash
inngest-ctl cancel --app my-app --function my-func --started-after 1h --started-before now
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--pretty` | Human-readable output with colors |
| `--output <file>` | Export results to JSON file |
| `--dev` | Use local dev server (localhost:8288) |
| `--port <port>` | Dev server port (default: 8288) |

## Common Workflows

### Local Development

```bash
# Start Inngest dev server
npx inngest-cli@latest dev

# List local events
inngest-ctl events list --dev --pretty

# Send test event
inngest-ctl events send --name "test.event" --data '{"test": true}' --dev

# Check what runs it triggered
inngest-ctl events runs <event-id> --dev --pretty

# Monitor run status
inngest-ctl runs status <run-id> --dev --pretty
```

### Debugging Function Runs

```bash
# 1. Find recent events
inngest-ctl events list --pretty

# 2. Get event details
inngest-ctl events get <event-id> --pretty

# 3. List runs triggered by the event
inngest-ctl events runs <event-id> --pretty

# 4. Check run status and duration
inngest-ctl runs status <run-id> --pretty

# 5. Get detailed job/step info
inngest-ctl runs get <run-id> --pretty
```

### Production Monitoring

```bash
# List recent events for a specific type
inngest-ctl events list --name "user.signup" --limit 50 --pretty

# Check if a specific run completed
inngest-ctl runs status <run-id> --pretty

# Export event data for analysis
inngest-ctl events list --limit 100 --output events.json
```

## Output Format

Default output is JSON. Use `--pretty` for colored human-readable output:

- Event names colored by type:
  - Red: error/fail events
  - Green: success/complete events
  - Yellow: warn events
  - Blue: default
- Run status badges: `[OK]`, `[ERR]`, `[RUN]`
- Durations show "(running)" for active runs
- Timestamps in gray
