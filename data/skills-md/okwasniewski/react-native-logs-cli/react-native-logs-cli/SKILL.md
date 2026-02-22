---
name: react-native-logs-cli
description: >
  Use rn-logs to read React Native Metro logs via CDP without MCP overhead.
  Default output is plain text and safe for non-interactive agent runs.
license: MIT
metadata:
  author: okwasniewski
  version: "1.0.0"
---

# rn-logs cli

Use `rn-logs` to read React Native Metro logs via CDP without MCP overhead.
Default output is plain text and safe for non-interactive agent runs.

## When to use

- You need live Metro logs from a running RN app
- You want low-context, plain text log output

## Requirements

- Metro is running
- App is running on a simulator or device

## Core workflow

```bash
# 1. List connected apps
rn-logs apps

# 2. Stream logs
rn-logs logs --app "<id|name>"

# 3. Snapshot logs
rn-logs logs --app "<id|name>" --limit 50
```

## Command options

```bash
# Changing default port or host
rn-logs "[command]" --host "<host>"    # Metro host (default: localhost)
rn-logs "[command]" --port "<port>"    # Metro port (default: 8081)

rn-logs help
```

## Non-interactive mode

- When multiple apps are connected, you must pass `--app`.
- Output is plain text for agent-friendly consumption.

## Common failures

- `metro not reachable` -> start Metro or fix host/port
- `no apps connected` -> run app on simulator or device
- `multiple apps connected` -> pass `--app`
