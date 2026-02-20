---
name: agent-slackbot
description: Interact with Slack workspaces using bot tokens - send messages, read channels, manage reactions
allowed-tools: Bash(agent-slackbot:*)
---

# Agent SlackBot

A TypeScript CLI tool that enables AI agents and humans to interact with Slack workspaces using bot tokens (xoxb-). Unlike agent-slack which extracts user tokens from the desktop app, agent-slackbot uses standard Slack Bot tokens for server-side and CI/CD integrations.

## Quick Start

```bash
# Set your bot token
agent-slackbot auth set xoxb-your-bot-token

# Or set with a custom bot identifier for multi-bot setups
agent-slackbot auth set xoxb-your-bot-token --bot deploy --name "Deploy Bot"

# Verify authentication
agent-slackbot auth status

# Send a message
agent-slackbot message send C0ACZKTDDC0 "Hello from bot!"

# List channels
agent-slackbot channel list
```

## Authentication

### Bot Token Setup

agent-slackbot uses Slack Bot tokens (xoxb-) which you get from the Slack App configuration:

```bash
# Set bot token (validates against Slack API before saving)
agent-slackbot auth set xoxb-your-bot-token

# Set with a custom bot identifier
agent-slackbot auth set xoxb-your-bot-token --bot deploy --name "Deploy Bot"

# Check auth status
agent-slackbot auth status

# Clear stored credentials
agent-slackbot auth clear
```

### Multi-Bot Management

Store multiple bot tokens and switch between them:

```bash
# Add multiple bots
agent-slackbot auth set xoxb-deploy-token --bot deploy --name "Deploy Bot"
agent-slackbot auth set xoxb-alert-token --bot alert --name "Alert Bot"

# List all stored bots
agent-slackbot auth list

# Switch active bot
agent-slackbot auth use deploy

# Use a specific bot for one command (without switching)
agent-slackbot message send C0ACZKTDDC0 "Alert!" --bot alert

# Remove a stored bot
agent-slackbot auth remove deploy

# Disambiguate bots with same ID across workspaces
agent-slackbot auth use T123456/deploy
```

The `--bot <id>` flag is available on all commands to override the active bot for a single invocation.

### Getting a Bot Token

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Create New App (or select existing)
3. Go to **OAuth & Permissions**
4. Add required bot token scopes (see below)
5. Install app to workspace
6. Copy the **Bot User OAuth Token** (starts with `xoxb-`)

### Required Bot Token Scopes

| Scope | Used For |
|-------|----------|
| `chat:write` | Sending messages |
| `channels:history` | Reading public channel messages |
| `channels:read` | Listing public channels |
| `channels:join` | Joining public channels |
| `groups:history` | Reading private channel messages |
| `groups:read` | Listing private channels |
| `users:read` | Listing users |
| `users:read.email` | Reading user email addresses |
| `reactions:write` | Adding/removing reactions |
| `reactions:read` | Listing reactions |

### Environment Variables (CI/CD)

For CI/CD pipelines, set these environment variables instead of using `auth set`:

```bash
export E2E_SLACKBOT_TOKEN=xoxb-your-bot-token
export E2E_SLACKBOT_WORKSPACE_ID=T123456
export E2E_SLACKBOT_WORKSPACE_NAME="My Workspace"
```

## Commands

### Message Commands

```bash
# Send a message
agent-slackbot message send <channel> <text>
agent-slackbot message send C0ACZKTDDC0 "Hello world"

# Send a threaded reply
agent-slackbot message send C0ACZKTDDC0 "Reply" --thread <ts>

# List messages
agent-slackbot message list <channel>
agent-slackbot message list C0ACZKTDDC0 --limit 50

# Get a single message by timestamp
agent-slackbot message get <channel> <ts>

# Get thread replies (includes parent message)
agent-slackbot message replies <channel> <thread_ts>
agent-slackbot message replies C0ACZKTDDC0 1234567890.123456 --limit 50

# Update a message (bot's own messages only)
agent-slackbot message update <channel> <ts> <new-text>

# Delete a message (bot's own messages only)
agent-slackbot message delete <channel> <ts> --force
```

### Channel Commands

```bash
# List channels the bot can see
agent-slackbot channel list
agent-slackbot channel list --limit 50

# Get channel info
agent-slackbot channel info <channel>
agent-slackbot channel info C0ACZKTDDC0
```

### User Commands

```bash
# List users
agent-slackbot user list
agent-slackbot user list --limit 50

# Get user info
agent-slackbot user info <user-id>
```

### Reaction Commands

```bash
# Add reaction
agent-slackbot reaction add <channel> <ts> <emoji>
agent-slackbot reaction add C0ACZKTDDC0 1234567890.123456 thumbsup

# Remove reaction
agent-slackbot reaction remove <channel> <ts> <emoji>
```

## Output Format

### JSON (Default)

All commands output JSON by default for AI consumption:

```json
{
  "ts": "1234567890.123456",
  "channel": "C0ACZKTDDC0",
  "text": "Hello world"
}
```

### Pretty (Human-Readable)

Use `--pretty` flag for formatted output:

```bash
agent-slackbot channel list --pretty
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
  "error": "No credentials. Run \"auth set\" first."
}
```

Common errors:
- `missing_token`: No credentials configured
- `invalid_token_type`: Token is not a bot token (must start with xoxb-)
- `not_in_channel`: Bot needs to join the channel first
- `slack_webapi_rate_limited_error`: Hit rate limit (auto-retries with backoff)

## Configuration

Credentials stored in: `~/.config/agent-messenger/slackbot-credentials.json`

Format:
```json
{
  "current": {
    "workspace_id": "T123456",
    "bot_id": "deploy"
  },
  "workspaces": {
    "T123456": {
      "workspace_id": "T123456",
      "workspace_name": "My Workspace",
      "bots": {
        "deploy": {
          "bot_id": "deploy",
          "bot_name": "Deploy Bot",
          "token": "xoxb-..."
        },
        "alert": {
          "bot_id": "alert",
          "bot_name": "Alert Bot",
          "token": "xoxb-..."
        }
      }
    }
  }
}
```

**Security**: File permissions set to 0600 (owner read/write only)

## Key Differences from agent-slack

| Feature | agent-slack | agent-slackbot |
|---------|------------|----------------|
| Token type | User token (xoxc-) | Bot token (xoxb-) |
| Token source | Auto-extracted from desktop app | Manual from Slack App config |
| Message search | Yes | No (requires user token) |
| File operations | Yes | No |
| Snapshot | Yes | No |
| Edit/delete messages | Any message | Bot's own messages only |
| Workspace management | Multi-workspace | Multi-bot, multi-workspace |
| CI/CD friendly | Requires desktop app | Yes (just set token) |

## Limitations

- No real-time events / Socket Mode
- No message search (requires user token scope)
- No file upload/download
- No workspace snapshot
- Bot can only edit/delete its own messages
- Bot must be invited to private channels
- No scheduled messages
- Plain text messages only (no blocks/formatting)

## Troubleshooting

### `agent-slackbot: command not found`

**`agent-slackbot` is NOT the npm package name.** The npm package is `agent-messenger`.

If the package is installed globally, use `agent-slackbot` directly:

```bash
agent-slackbot message send general "Hello"
```

If the package is NOT installed, use `bunx agent-messenger slackbot`:

```bash
bunx agent-messenger slackbot message send general "Hello"
```

**NEVER run `bunx agent-slackbot`** — it will fail or install a wrong package since `agent-slackbot` is not the npm package name.

## References

- [Authentication Guide](references/authentication.md)
- [Common Patterns](references/common-patterns.md)
