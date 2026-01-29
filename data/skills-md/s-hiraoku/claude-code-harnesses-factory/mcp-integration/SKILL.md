---
name: mcp-integration
description: This skill guides connecting MCP servers to Claude Code plugins for external service integration. Use when configuring MCP servers, setting up authentication, or integrating external tools.
---

# MCP Integration

## Overview

Connect Model Context Protocol servers to Claude Code plugins to expose external service capabilities as tools.

## Configuration Methods

### Dedicated .mcp.json (Recommended)

```json
{
  "mcpServers": {
    "my-server": {
      "type": "stdio",
      "command": "node",
      "args": ["server.js"],
      "env": {
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

### Inline in plugin.json

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "my-server": { ... }
  }
}
```

## Server Types

### stdio (Local Process)
```json
{
  "type": "stdio",
  "command": "npx",
  "args": ["-y", "@anthropic/mcp-server"]
}
```

### HTTP (REST API)
```json
{
  "type": "http",
  "url": "https://api.example.com/mcp",
  "headers": {
    "Authorization": "Bearer ${API_TOKEN}"
  }
}
```

### SSE (Server-Sent Events)
```json
{
  "type": "sse",
  "url": "https://mcp.example.com/sse",
  "headers": {
    "X-API-Key": "${API_KEY}"
  }
}
```

### WebSocket
```json
{
  "type": "websocket",
  "url": "wss://mcp.example.com/ws"
}
```

## Environment Variables

Use `${VAR_NAME}` for dynamic values:

```json
{
  "env": {
    "DATABASE_URL": "${DATABASE_URL}",
    "API_KEY": "${API_KEY}"
  }
}
```

## Plugin Portability

Use `${CLAUDE_PLUGIN_ROOT}` for relative paths:

```json
{
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/server/index.js"]
}
```

## Security Best Practices

1. **Use HTTPS/WSS** - Never use HTTP for remote servers
2. **Never hardcode tokens** - Use environment variables
3. **Pre-allow specific tools** - Avoid wildcards in permissions
4. **Document required variables** - List in README

## Testing

```bash
# Verify MCP configuration
/mcp

# Check server status
/mcp status
```

## Workflow

1. Select server type based on deployment
2. Create `.mcp.json` configuration
3. Use `${CLAUDE_PLUGIN_ROOT}` for portability
4. Document environment variables
5. Test locally via `/mcp` command
6. Configure tool permissions
7. Handle authentication and errors
