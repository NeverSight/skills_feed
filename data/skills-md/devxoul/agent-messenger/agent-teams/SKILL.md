---
name: agent-teams
description: Interact with Microsoft Teams - send messages, read channels, manage reactions
allowed-tools: Bash(agent-teams:*)
---

# Agent Teams

A TypeScript CLI tool that enables AI agents and humans to interact with Microsoft Teams through a simple command interface. Features seamless token extraction from the Teams desktop app and multi-team support.

## TOKEN EXPIRY WARNING

**CRITICAL**: Microsoft Teams tokens expire in **60-90 minutes**! Unlike Discord/Slack, Teams tokens have a short lifespan. You MUST:

1. Check token validity before operations
2. Re-extract credentials when tokens expire
3. Handle `401 Unauthorized` errors gracefully

```bash
# Always check auth status first
agent-teams auth status

# If expired, re-extract
agent-teams auth extract
```

## Quick Start

```bash
# Extract credentials from Teams desktop app (zero-config)
agent-teams auth extract

# Get team snapshot
agent-teams snapshot

# Send a message
agent-teams message send <channel-id> "Hello from AI agent!"

# List channels
agent-teams channel list
```

## Authentication

### Seamless Token Extraction

agent-teams automatically extracts your Teams credentials from the desktop app:

```bash
# Just run this - no manual token copying needed
agent-teams auth extract

# Use --debug for troubleshooting
agent-teams auth extract --debug
```

This command:
- Auto-detects your platform (macOS/Linux/Windows)
- Extracts skypetoken_asm from Teams desktop app's Cookies SQLite database
- Validates token against Teams API before saving
- Discovers ALL joined teams
- Stores credentials securely in `~/.config/agent-messenger/`

### Multi-Team Support

```bash
# List all available teams
agent-teams team list

# Switch to a different team
agent-teams team switch <team-id>

# Show current team
agent-teams team current

# Check auth status (includes token expiry info)
agent-teams auth status
```

## Commands

### Message Commands

```bash
# Send a message
agent-teams message send <channel-id> <content>
agent-teams message send 19:abc123@thread.tacv2 "Hello world"

# List messages
agent-teams message list <channel-id>
agent-teams message list 19:abc123@thread.tacv2 --limit 50

# Get a single message by ID
agent-teams message get <channel-id> <message-id>

# Delete a message
agent-teams message delete <channel-id> <message-id> --force
```

### Channel Commands

```bash
# List channels in current team
agent-teams channel list

# Get channel info
agent-teams channel info <channel-id>
agent-teams channel info 19:abc123@thread.tacv2

# Get channel history (alias for message list)
agent-teams channel history <channel-id> --limit 100
```

### Team Commands

```bash
# List all teams
agent-teams team list

# Get team info
agent-teams team info <team-id>

# Switch active team
agent-teams team switch <team-id>

# Show current team
agent-teams team current
```

### User Commands

```bash
# List team members
agent-teams user list

# Get user info
agent-teams user info <user-id>

# Get current user
agent-teams user me
```

### Reaction Commands

```bash
# Add reaction (use emoji name)
agent-teams reaction add <channel-id> <message-id> <emoji>
agent-teams reaction add 19:abc123@thread.tacv2 1234567890 like

# Remove reaction
agent-teams reaction remove <channel-id> <message-id> <emoji>

# List reactions on a message
agent-teams reaction list <channel-id> <message-id>
```

### File Commands

```bash
# Upload file
agent-teams file upload <channel-id> <path>
agent-teams file upload 19:abc123@thread.tacv2 ./report.pdf

# List files in channel
agent-teams file list <channel-id>

# Get file info
agent-teams file info <channel-id> <file-id>
```

### Snapshot Command

Get comprehensive team state for AI agents:

```bash
# Full snapshot
agent-teams snapshot

# Filtered snapshots
agent-teams snapshot --channels-only
agent-teams snapshot --users-only

# Limit messages per channel
agent-teams snapshot --limit 10
```

Returns JSON with:
- Team metadata (id, name)
- Channels (id, name, type, description)
- Recent messages (id, content, author, timestamp)
- Members (id, displayName, email)

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "id": "19:abc123@thread.tacv2",
  "content": "Hello world",
  "author": "John Doe",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-teams channel list --pretty
```

## Key Differences from Discord/Slack

| Feature | Teams | Discord | Slack |
|---------|-------|---------|-------|
| Server terminology | Team | Guild | Workspace |
| Channel identifiers | UUID format (19:xxx@thread.tacv2) | Snowflake IDs | Channel name or ID |
| Token storage | Cookies SQLite | LevelDB | LevelDB |
| Token expiry | **60-90 minutes** | Rarely expires | Rarely expires |
| Mentions | `<at id="user-id">Name</at>` | `<@user_id>` | `<@USER_ID>` |

**Important**: Teams uses UUID-style channel IDs (like `19:abc123@thread.tacv2`). You cannot use channel names directly - use `channel list` to find IDs first.

## Common Patterns

See `references/common-patterns.md` for typical AI agent workflows.

## Templates

See `templates/` directory for runnable examples:
- `post-message.sh` - Send messages with error handling
- `monitor-channel.sh` - Monitor channel for new messages (with token refresh)
- `team-summary.sh` - Generate team summary

## Error Handling

All commands return consistent error format:

```json
{
  "error": "Not authenticated. Run \"auth extract\" first."
}
```

Common errors:
- `Not authenticated`: No valid token - run `auth extract`
- `Token expired`: Token has expired (60-90 min limit) - run `auth extract` again
- `No current team set`: Run `team switch <id>` first
- `Message not found`: Invalid message ID
- `Channel not found`: Invalid channel ID
- `401 Unauthorized`: Token expired - re-authenticate immediately

## Configuration

Credentials stored in: `~/.config/agent-messenger/teams-credentials.json`

Format:
```json
{
  "token": "skypetoken_asm_value_here",
  "token_extracted_at": "2024-01-15T10:00:00.000Z",
  "current_team": "team-uuid-here",
  "teams": {
    "team-uuid-here": {
      "team_id": "team-uuid-here",
      "team_name": "My Team"
    }
  }
}
```

**Security**: File permissions set to 0600 (owner read/write only)

## Limitations

- No real-time events / WebSocket connection
- No voice/video channel support
- No team management (create/delete channels, roles)
- No meeting support
- No webhook support
- Plain text messages only (no adaptive cards in v1)
- User tokens only (no app tokens)
- **Token expires in 60-90 minutes** - must re-authenticate frequently

## Troubleshooting

### `agent-teams: command not found`

The `agent-messenger` package is not installed. Run it directly using a package runner. Ask the user which one to use:

```bash
npx -p agent-messenger agent-teams ...
bunx -p agent-messenger agent-teams ...
pnpm dlx --package agent-messenger agent-teams ...
```

If you already know the user's preferred package runner, use it directly instead of asking.

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
