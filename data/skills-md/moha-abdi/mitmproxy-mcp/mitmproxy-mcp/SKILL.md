---
name: mitmproxy-mcp
description: Analyze, intercept, and replay HTTP/HTTPS traffic through mitmproxy. Gives you 20 MCP tools for traffic analysis, request replay, interception control, and proxy configuration. Use when debugging APIs, testing security, or understanding how an application talks to its backend.
---

# mitmproxy-mcp

HTTP/HTTPS traffic analysis, interception, and replay through mitmproxy.

## Prerequisites

- mitmproxy running with the mitmproxy-mcp addon loaded
- MCP server available at `http://localhost:9011/sse` (SSE transport)

If the MCP server is not connected, tell the user to start mitmproxy first:

```bash
mitmproxy      # or mitmweb, or mitmdump
```

The addon and MCP server start automatically if configured in `~/.mitmproxy/config.yaml`.

## When to Use This Skill

- User asks to inspect, debug, or analyze HTTP traffic
- User wants to replay or modify an HTTP request
- User wants to intercept requests matching a pattern
- User needs to export captured traffic (HAR format)
- User is doing API debugging or security testing

## Available Tools (20)

### Flow Tools -- querying captured traffic

- `get_flows` -- list captured flows with optional filtering by method, URL pattern, or status code. Supports `limit` and `offset` for pagination.
- `get_flow_by_id` -- get full request and response details for a single flow
- `search_flows` -- search flows by regex pattern across URL, method, status, and headers
- `get_flow_request` -- get only the request portion of a flow
- `get_flow_response` -- get only the response portion of a flow
- `get_flow_count` -- count of currently stored flows
- `clear_flows` -- clear all stored flows
- `export_flows` -- export flows to HAR 1.2 format. Optionally pass specific flow IDs.

### Replay Tools -- sending and modifying requests

- `replay_request` -- replay a captured request exactly as-is. Returns a new flow with the response.
- `send_request` -- send a new HTTP request. Parameters: `url` (required), `method` (default GET), `headers`, `body`.
- `modify_and_send` -- take an existing flow, change its method/url/headers/body, and send it. Useful for testing variations.
- `duplicate_flow` -- clone a flow without sending it. Useful for before/after comparisons.

### Intercept Tools -- pausing and controlling live traffic

- `set_intercept_filter` -- set a mitmproxy filter expression to intercept matching requests. Uses mitmproxy filter syntax: `~u example.com`, `~m POST`, `~u api & ~m GET`. Pass empty string to disable.
- `get_intercepted_flows` -- list flows currently paused by interception
- `resume_flow` -- resume a single intercepted flow
- `resume_all` -- resume all intercepted flows
- `drop_flow` -- drop/kill an intercepted flow without forwarding it

### Config Tools -- proxy settings

- `get_options` -- get current mitmproxy option values. Pass specific keys or get curated defaults.
- `set_option` -- set a mitmproxy option at runtime. Some dangerous options (listen_host, listen_port, mode, server, ssl_insecure) are blocked.
- `get_status` -- get proxy status: version, listen address, mode, flow count, intercept settings.

## Workflow Patterns

### Basic traffic inspection

1. Make sure mitmproxy is running and proxying the target traffic
2. Use `get_flows` to see what has been captured
3. Use `get_flow_by_id` to drill into specific requests/responses
4. Use `search_flows` with a regex to find specific patterns

### Replaying and modifying requests

1. Find the flow you want with `get_flows` or `search_flows`
2. Use `replay_request` to resend it exactly
3. Or use `modify_and_send` to change headers, body, or URL before sending
4. Compare the original and modified responses

### Intercepting live traffic

1. Set a filter with `set_intercept_filter` (e.g. `~u api.example.com & ~m POST`)
2. Wait for matching requests -- they will be paused
3. Use `get_intercepted_flows` to see what is waiting
4. Use `resume_flow` or `drop_flow` to control each one
5. Use `set_intercept_filter` with empty string to stop intercepting

## Important Notes

- Sensitive data redaction is off by default. Enable with `mcp_redact: true` in mitmproxy config to redact tokens, passwords, API keys, and JWTs
- Request/response bodies are truncated to 10KB to prevent context overflow
- All data is in-memory only -- cleared when mitmproxy stops
- The proxy stores up to 1000 flows by default (oldest evicted first)
