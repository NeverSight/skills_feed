---
name: unicon-mcp
description: Help users connect the Unicon MCP server to Claude Desktop, Cursor, and other MCP clients. Use when setting up MCP config, verifying installs, debugging MCP connection issues, or using Unicon tools for icon search and generation through AI assistants.
license: MIT
compatibility: Requires MCP-compatible client (Claude Desktop, Cursor, or similar)
metadata:
  author: webrenew
  version: "1.0.0"
  website: https://unicon.webrenew.com
  repository: https://github.com/WebRenew/unicon
---

# Unicon MCP

Use the Unicon MCP server to search and generate icon components through AI assistants like Claude Desktop and Cursor.

## Quick Start

### Claude Desktop

1. Open `~/Library/Application Support/Claude/claude_desktop_config.json`
2. Add:

```json
{
  "mcpServers": {
    "unicon": {
      "command": "npx",
      "args": ["-y", "@webrenew/unicon-mcp-server"]
    }
  }
}
```

3. Fully quit and restart Claude Desktop.

### Cursor

1. Open **Settings > MCP Servers**
2. Add the same JSON config shown above
3. Restart Cursor

## Verify Installation

- Claude Desktop: look for the plug icon, ensure `unicon` appears
- Cursor: run `claude mcp list` if using Claude Code

## Common Prompts

- "Search for dashboard icons in Lucide"
- "Get React component for lucide:arrow-right"
- "Generate Vue components for social media icons"
- "List available icon libraries"

## Available Tools

### search_icons

Search through 19,000+ icons with optional filters.

**Parameters**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes | Search term |
| `source` | No | Filter by library |
| `category` | No | Filter by category |
| `limit` | No | Max results (default: 20) |
| `includeCode` | No | Return code with results |
| `strokeWidth` | No | Stroke width when includeCode=true |
| `normalizeStrokes` | No | Normalize stroke widths, skipping fill icons |

### get_icon

Return code for a single icon in a requested format.

**Parameters**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `iconId` | Yes | Icon ID (e.g., "lucide:home") |
| `format` | No | svg, react, vue, svelte, json |
| `size` | No | Icon size in pixels |
| `strokeWidth` | No | Stroke width |
| `normalizeStrokes` | No | Normalize stroke widths, skipping fill icons |

### get_multiple_icons

Fetch up to 50 icons at once in a shared format.

**Parameters**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `iconIds` | Yes | Array of icon IDs |
| `format` | No | Output format |
| `size` | No | Icon size in pixels |
| `strokeWidth` | No | Stroke width |
| `normalizeStrokes` | No | Normalize stroke widths, skipping fill icons |

### get_starter_pack

Get curated icon packs for common use cases.

**Parameters**
| Parameter | Required | Description |
|-----------|----------|-------------|
| `packId` | Yes | Pack identifier |
| `format` | No | Output format |
| `size` | No | Icon size in pixels |
| `strokeWidth` | No | Stroke width |
| `normalizeStrokes` | No | Normalize stroke widths, skipping fill icons |

## Resources

The MCP server exposes these resources:

| URI | Description |
|-----|-------------|
| `unicon://sources` | Library metadata (names, icon counts) |
| `unicon://categories` | Available category list |
| `unicon://stats` | Overall icon statistics |

## Troubleshooting

### Server not appearing

1. Fully quit the app (Cmd+Q on macOS)
2. Verify config JSON syntax is valid
3. Restart the application
4. Check for error logs

### Slow first start

The first `npx` run downloads the package. Subsequent runs use cache.

### Icons not found

Run `search_icons` with your query to verify the icon ID exists. Format is `source:name` (e.g., `lucide:home`).

### Connection errors

1. Ensure you have Node.js 18+ installed
2. Check internet connectivity
3. Try running manually: `npx @webrenew/unicon-mcp-server`
