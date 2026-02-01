---
name: agent-slack
description: Interact with Slack workspaces - send messages, read channels, manage reactions
allowed-tools: Bash(agent-slack:*)
---

# Agent Slack

A TypeScript CLI tool that enables AI agents and humans to interact with Slack workspaces through a simple command interface. Features seamless token extraction from the Slack desktop app and multi-workspace support.

## Quick Start

```bash
# Extract credentials from Slack desktop app (zero-config)
agent-slack auth extract

# Get workspace snapshot
agent-slack snapshot

# Send a message
agent-slack message send general "Hello from AI agent!"

# List channels
agent-slack channel list
```

## Authentication

### Seamless Token Extraction

agent-slack automatically extracts your Slack credentials from the desktop app:

```bash
# Just run this - no manual token copying needed
agent-slack auth extract

# Use --debug for troubleshooting
agent-slack auth extract --debug
```

This command:
- Auto-detects your platform (macOS/Linux/Windows)
- Supports both direct download and App Store versions of Slack on macOS
- Extracts xoxc token and xoxd cookie (with v10 decryption for sandboxed apps)
- Validates tokens against Slack API before saving
- Discovers ALL logged-in workspaces
- Stores credentials securely in `~/.config/agent-messenger/`

### Multi-Workspace Support

```bash
# List all authenticated workspaces
agent-slack workspace list

# Switch to a different workspace
agent-slack workspace switch <workspace-id>

# Show current workspace
agent-slack workspace current

# Check auth status
agent-slack auth status
```

## Commands

### Message Commands

```bash
# Send a message
agent-slack message send <channel> <text>
agent-slack message send general "Hello world"

# Send a threaded reply
agent-slack message send general "Reply" --thread <ts>

# List messages
agent-slack message list <channel>
agent-slack message list general --limit 50

# Search messages across workspace
agent-slack message search <query>
agent-slack message search "project update"
agent-slack message search "from:@user deadline" --limit 50
agent-slack message search "in:#general meeting" --sort timestamp

# Get a single message by timestamp
agent-slack message get <channel> <ts>
agent-slack message get general 1234567890.123456

# Get thread replies (includes parent message)
agent-slack message replies <channel> <thread_ts>
agent-slack message replies general 1234567890.123456
agent-slack message replies general 1234567890.123456 --limit 50
agent-slack message replies general 1234567890.123456 --oldest 1234567890.000000
agent-slack message replies general 1234567890.123456 --cursor <next_cursor>

# Update a message
agent-slack message update <channel> <ts> <new-text>

# Delete a message
agent-slack message delete <channel> <ts> --force
```

### Channel Commands

```bash
# List channels (excludes archived by default)
agent-slack channel list
agent-slack channel list --type public
agent-slack channel list --type private
agent-slack channel list --include-archived

# Get channel info
agent-slack channel info <channel>
agent-slack channel info general

# Get channel history (alias for message list)
agent-slack channel history <channel> --limit 100
```

### User Commands

```bash
# List users
agent-slack user list
agent-slack user list --include-bots

# Get user info
agent-slack user info <user>

# Get current user
agent-slack user me
```

### Reaction Commands

```bash
# Add reaction
agent-slack reaction add <channel> <ts> <emoji>
agent-slack reaction add general 1234567890.123456 thumbsup

# Remove reaction
agent-slack reaction remove <channel> <ts> <emoji>

# List reactions on a message
agent-slack reaction list <channel> <ts>
```

### File Commands

```bash
# Upload file
agent-slack file upload <channel> <path>
agent-slack file upload general ./report.pdf

# List files
agent-slack file list
agent-slack file list --channel general

# Get file info
agent-slack file info <file-id>
```

### Snapshot Command

Get comprehensive workspace state for AI agents:

```bash
# Full snapshot
agent-slack snapshot

# Filtered snapshots
agent-slack snapshot --channels-only
agent-slack snapshot --users-only

# Limit messages per channel
agent-slack snapshot --limit 10
```

Returns JSON with:
- Workspace metadata
- Channels (id, name, topic, purpose)
- Recent messages (ts, text, user, channel)
- Users (id, name, profile)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "ts": "1234567890.123456",
  "text": "Hello world",
  "channel": "C123456"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-slack channel list --pretty
```

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:
- `post-message.sh` - Send messages with error handling
- `monitor-channel.sh` - Monitor channel for new messages
- `workspace-summary.sh` - Generate workspace summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "No workspace authenticated. Run: agent-slack auth extract"
}
```

Common errors:
- `NO_WORKSPACE`: No authenticated workspace
- `SLACK_API_ERROR`: Slack API returned an error
- `RATE_LIMIT`: Hit Slack rate limit (auto-retries with backoff)

## Configuration

Credentials stored in: `~/.config/agent-messenger/slack-credentials.json`

Format:
```json
{
  "current_workspace": "T123456",
  "workspaces": {
    "T123456": {
      "workspace_id": "T123456",
      "workspace_name": "My Workspace",
      "token": "xoxc-...",
      "cookie": "xoxd-..."
    }
  }
}
```

**Security**: File permissions set to 0600 (owner read/write only)

## Limitations

- No real-time events / Socket Mode
- No channel management (create/archive)
- No workspace admin operations
- No scheduled messages
- No user presence features
- Plain text messages only (no blocks/formatting in v1)

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
