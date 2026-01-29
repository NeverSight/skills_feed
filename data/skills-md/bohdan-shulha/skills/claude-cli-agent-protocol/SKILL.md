---
name: claude-cli-agent-protocol
description: >-
  Guidance for integrating Claude Code CLI in agent/headless mode: required stream-json flags, NDJSON protocol, control_request/control_response tool approvals, and process management. Use when building a host that drives Claude CLI or troubleshooting permission prompts and tool approvals.
---

# Claude CLI Agent Protocol

## Overview

Enable reliable, bidirectional integration with Claude Code CLI via NDJSON, including tool approval handling, permission mode control, and long-lived process management.

## Required CLI Flags

Use these flags to enable stream-json I/O and tool approval control:

```bash
claude \
  --output-format stream-json \
  --input-format stream-json \
  --verbose \
  --permission-prompt-tool stdio
```

Notes:
- `--permission-prompt-tool stdio` is required for control_request/control_response. Without it, tools auto-deny in non-interactive mode.
- Do not use `-p` with a prompt. Send user messages via stdin.

## Message Protocol (NDJSON)

All stdin/stdout messages are newline-delimited JSON with a `type` field.

Send a user message:

```json
{"type":"user","message":{"role":"user","content":[{"type":"text","text":"your prompt here"}]}}
```

Core stdout message types:
- `system` - session init (model, tools, session_id, cwd)
- `assistant` - responses and tool invocations
- `user` - tool results returned to Claude
- `result` - completion with cost/token data
- `control_request` - tool approval request

## Tool Approval Protocol

When a tool needs approval, CLI emits:

```json
{
  "type": "control_request",
  "request_id": "req_abc123",
  "request": {
    "subtype": "can_use_tool",
    "tool_name": "Bash",
    "input": {"command": "git add -A", "description": "Stage all changes"},
    "decision_reason": "Command not in allowlist",
    "tool_use_id": "toolu_xyz"
  }
}
```

Fields:
- `tool_name`: The tool being invoked (Bash, Read, Edit, Write, etc.)
- `input`: Tool-specific input (Bash has `command` and `description`, file tools have `file_path`)
- `decision_reason`: Why permission is required (e.g., "Path is outside allowed working directories")

Allow (must include `updatedInput` with the original or modified input):

```json
{
  "type": "control_response",
  "response": {
    "subtype": "success",
    "request_id": "req_abc123",
    "response": {
      "behavior": "allow",
      "updatedInput": {"command": "git add -A", "description": "Stage all changes"}
    }
  }
}
```

Deny (must include `message`):

```json
{
  "type": "control_response",
  "response": {
    "subtype": "success",
    "request_id": "req_abc123",
    "response": {"behavior": "deny", "message": "User denied this action"}
  }
}
```

Key rules:
- `request_id` must match the incoming request.
- For `allow`: `updatedInput` is required (pass the original `input` from the request, or a modified version).
- For `deny`: `message` is required (cannot be omitted).
- CLI blocks waiting for a response (default timeout ~60s).

## Permission Modes vs prompt tool

- `--permission-prompt-tool stdio` is what enables control_request.
- `--permission-mode delegate` only limits tool availability; it does not delegate approvals.

Dynamic mode switching (mid-session):

```json
{
  "type": "control_request",
  "request_id": "unique-id",
  "request": {
    "subtype": "set_permission_mode",
    "mode": "plan"
  }
}
```

Response:

```json
{
  "type": "control_response",
  "response": {
    "subtype": "success",
    "request_id": "unique-id"
  }
}
```

## Process Management

- Keep one CLI process alive across turns.
- Write user messages to stdin; read assistant/control messages from stdout.
- Do not start a new process per message; keep stdin open.

## Cost Tracking

The final `result` message includes `total_cost_usd`, token counts, and a `permission_denials` list if any tool actions were denied.

## Debugging

Enable debug logs via environment variable or flag:

```bash
DEBUG_CLAUDE_AGENT_SDK=1 claude ...
```

or `--debug`.

## References

- Headless mode docs: https://code.claude.com/docs/en/headless
- Agent SDK permissions: https://platform.claude.com/docs/en/agent-sdk/permissions
- Agent SDK user input: https://platform.claude.com/docs/en/agent-sdk/user-input
- CLI reference: https://code.claude.com/docs/en/cli-reference
- Stream-json / control protocol gist: https://gist.github.com/SamSaffron/603648958a8c18ceae34939a8951d417

## SDK Protocol Discovery (unknown behaviors/messages)

If the CLI emits unexpected message types or behaviors, inspect the TypeScript SDK:

1) Download and extract the SDK package:

```bash
cd /tmp && npm pack @anthropic-ai/claude-code && tar -xzf *.tgz
```

2) Check TypeScript definitions for message and control types:

```bash
grep -E "subtype|type.*request|Request.*=" package/sdk.d.ts
```

3) Inspect the minified implementation for hidden flags or protocol handling:

```bash
rg -n "control_request|control_response|permission-prompt-tool|set_permission_mode" package/sdk.mjs
```

Key files:
- `package/sdk.d.ts` — readable type definitions (preferred)
- `package/sdk.mjs` — minified implementation (fallback for undocumented flags)

Search targets:
- `SDKControlRequest` / `SDKControlResponse`
- `PermissionMode` enum
- `StdinMessage` / `StdoutMessage`
