---
name: mcp-client
description: Universal MCP client for connecting to any MCP server with progressive disclosure. Wraps MCP servers as skills to avoid context window bloat from tool definitions. Use when interacting with external MCP servers (Zapier, Sequential Thinking, GitHub, filesystem, etc.), listing available tools, or executing MCP tool calls. Triggers on requests like "connect to Zapier", "use MCP server", "list MCP tools", "call Zapier action", "use sequential thinking", or any MCP server interaction.
---

# Universal MCP Client

Connect to any MCP server with progressive disclosure - load tool schemas on-demand instead of dumping thousands of tokens into context upfront.

## Skill Location

This skill is located at: `.claude/skills/mcp-client/`

**Script path:** `.claude/skills/mcp-client/scripts/mcp_client.py`

## Configuration

The script looks for config in this order:
1. `MCP_CONFIG_PATH` env var (custom path)
2. **`references/mcp-config.json`** (this skill's config - recommended)
3. `.mcp.json` in project root
4. `~/.claude.json`

**Your config file:** `.claude/skills/mcp-client/references/mcp-config.json`

Edit this file to add your API keys. The example file (`example-mcp-config.json`) is kept as a reference template.

**If the user hasn't provided their Zapier API key yet, ask them for it.**

## Running Commands

All commands use the script at `.claude/skills/mcp-client/scripts/mcp_client.py`:

```bash
# List configured servers
python .claude/skills/mcp-client/scripts/mcp_client.py servers

# List tools from a server
python .claude/skills/mcp-client/scripts/mcp_client.py tools <server_name>

# Call a tool
python .claude/skills/mcp-client/scripts/mcp_client.py call <server> <tool> '{"arg": "value"}'
```

## Workflow

1. **Check config exists** - Run `servers` command. If error, create `.mcp.json`
2. **List servers** - See what MCP servers are configured
3. **List tools** - Get tool schemas from a specific server
4. **Call tool** - Execute a tool with arguments

## Commands Reference

| Command | Description |
|---------|-------------|
| `servers` | List all configured MCP servers |
| `tools <server>` | List tools with full parameter schemas |
| `call <server> <tool> '<json>'` | Execute a tool with arguments |

## Example: Zapier

```bash
# 1. List servers to confirm Zapier is configured
python .claude/skills/mcp-client/scripts/mcp_client.py servers

# 2. List Zapier tools
python .claude/skills/mcp-client/scripts/mcp_client.py tools zapier

# 3. Call a Zapier tool
python .claude/skills/mcp-client/scripts/mcp_client.py call zapier <tool_name> '{"param": "value"}'
```

## Example: Sequential Thinking

```bash
# 1. List tools
python .claude/skills/mcp-client/scripts/mcp_client.py tools sequential-thinking

# 2. Use sequential thinking
python .claude/skills/mcp-client/scripts/mcp_client.py call sequential-thinking sequentialthinking '{"thought": "Breaking down the problem...", "thoughtNumber": 1, "totalThoughts": 5, "nextThoughtNeeded": true}'
```

## Config Format

Config file format (`references/mcp-config.json`):

```json
{
  "mcpServers": {
    "zapier": {
      "url": "https://mcp.zapier.com/api/v1/connect",
      "api_key": "your-api-key"
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

**Transport detection:**
- `url` + `api_key` → FastMCP with Bearer auth (Zapier)
- `command` + `args` → stdio (local servers like sequential-thinking)
- `url` ending in `/sse` → SSE transport
- `url` ending in `/mcp` → Streamable HTTP

## Error Handling

Errors return JSON:
```json
{"error": "message", "type": "configuration|validation|connection"}
```

- `configuration` - Config file not found. Create `.mcp.json`
- `validation` - Invalid server or tool name
- `connection` - Failed to connect to server

## Dependencies

```bash
pip install mcp fastmcp
```

## References

- `references/example-mcp-config.json` - Template config file
- `references/mcp-servers.md` - Common server configurations
- `references/python-mcp-sdk.md` - Python SDK documentation
