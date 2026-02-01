---
name: agentmail-mcp
description: AgentMail MCP server for email tools in AI assistants. Use when setting up AgentMail with Claude Desktop, Cursor, VS Code, Windsurf, or other MCP-compatible clients. Provides tools for inbox management, sending/receiving emails, and thread handling.
---

# AgentMail MCP Server

Connect AgentMail to any MCP-compatible AI client. Three setup options available.

## Prerequisites

Get your API key from [console.agentmail.to](https://console.agentmail.to).

---

## Option 1: Remote MCP (Simplest)

No installation required. Connect directly to the hosted MCP server.

**URL:** `https://mcp.agentmail.to`

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "AgentMail": {
      "url": "https://mcp.agentmail.to",
      "env": {
        "AGENTMAIL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

---

## Option 2: Local npm Package

Run the MCP server locally via npx.

```json
{
  "mcpServers": {
    "AgentMail": {
      "command": "npx",
      "args": ["-y", "agentmail-mcp"],
      "env": {
        "AGENTMAIL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

### Tool Selection

Load only specific tools with the `--tools` argument:

```json
{
  "mcpServers": {
    "AgentMail": {
      "command": "npx",
      "args": [
        "-y",
        "agentmail-mcp",
        "--tools",
        "send_message,reply_to_message,list_inboxes"
      ],
      "env": {
        "AGENTMAIL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

---

## Option 3: Local Python Package

Install and run the Python MCP server.

```bash
pip install agentmail-mcp
```

### Claude Desktop

Config location:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "AgentMail": {
      "command": "/path/to/your/.venv/bin/agentmail-mcp",
      "env": {
        "AGENTMAIL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

Find your path:

```bash
# Activate your virtual environment, then:
which agentmail-mcp
```

### Run Standalone

```bash
export AGENTMAIL_API_KEY=your-api-key
agentmail-mcp
```

---

## Available Tools

| Tool               | Description                     |
| ------------------ | ------------------------------- |
| `create_inbox`     | Create a new email inbox        |
| `list_inboxes`     | List all inboxes                |
| `get_inbox`        | Get inbox details by ID         |
| `delete_inbox`     | Delete an inbox                 |
| `send_message`     | Send an email from an inbox     |
| `reply_to_message` | Reply to an existing message    |
| `list_threads`     | List email threads in an inbox  |
| `get_thread`       | Get thread details and messages |
| `get_attachment`   | Download an attachment          |
| `update_message`   | Update message labels           |

---

## Client Configuration

### Cursor, VS Code, Windsurf

Add the same MCP server entry in your client config file:

Cursor: `.cursor/mcp.json`  
VS Code: `.vscode/mcp.json`  
Windsurf: MCP config file

```json
{
  "mcpServers": {
    "AgentMail": {
      "command": "npx",
      "args": ["-y", "agentmail-mcp"],
      "env": {
        "AGENTMAIL_API_KEY": "YOUR_API_KEY"
      }
    }
  }
}
```

---

## Compatible Clients

The AgentMail MCP server works with any MCP-compatible client:

- Claude Desktop
- Cursor
- VS Code
- Windsurf
- Cline
- Goose
- Raycast
- ChatGPT
- Amazon Q
- Codex
- Gemini CLI
- LibreChat
- Roo Code
- And more...

---

## Example Usage

Once configured, you can ask your AI assistant:

- "Create a new inbox for support emails"
- "Send an email to john@example.com with subject 'Hello'"
- "Check my inbox for new messages"
- "Reply to the latest email thanking them"
- "List all my email threads"
- "Download the attachment from the last message"

---

## Troubleshooting

### "Command not found"

Ensure npm/npx is in your PATH, or use the full path:

```json
"command": "/usr/local/bin/npx"
```

### "Invalid API key"

Verify your API key is correct and has the necessary permissions.

### Python package not found

Use the full path to the agentmail-mcp executable in your virtual environment:

```bash
# Find the path
source /path/to/venv/bin/activate
which agentmail-mcp
```
