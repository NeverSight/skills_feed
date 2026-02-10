---
name: validation-doctor
description: Diagnose MCP validation dependencies (Brave Search, Chrome DevTools) and output exact setup snippets.
---

# Validation Doctor

## Diagnostics

1. **Chrome DevTools MCP**
   - Probe by calling `list_pages` (may appear as `mcp6_list_pages` depending on the client).

2. **Brave Search MCP**
   - Probe by calling `brave_web_search` with a trivial query and `count=1`.

## Status Report

| Component | Status | Action Required |
|-----------|--------|-----------------|
| Market Validator (Brave) | ✅ / ❌ | [Config Snippet / None] |
| Technical Validator (Chrome) | ✅ / ❌ | [Config Snippet / None] |

## Setup Snippets

### Chrome DevTools (NPX)
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

### Brave Search (NPX)
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@brave/brave-search-mcp-server", "--transport", "stdio"],
      "env": {
        "BRAVE_API_KEY": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

## Runtime Policy

- If `chrome-devtools` is unavailable, allow `fetch` fallback but mark results as **Low Confidence**.
- If `brave-search` is unavailable, do not claim competitor positioning; only score the page itself.
