---
name: slack-messaging
description: Use when asked to send or read Slack messages, check Slack channels, test Slack integrations, or interact with a Slack workspace from the command line.
user-invocable: false
allowed-tools: Bash(slackcli:*, curl:*)
---

# Slack Messaging via slackcli

Send and read Slack messages from the command line using `slackcli` (shaharia-lab/slackcli).

## Installation

Download the binary:

```bash
curl -sL -o /usr/local/bin/slackcli \
  "https://github.com/shaharia-lab/slackcli/releases/download/v0.1.1/slackcli-linux"
chmod +x /usr/local/bin/slackcli
```

macOS (Intel): replace `slackcli-linux` with `slackcli-macos`
macOS (Apple Silicon): replace with `slackcli-macos-arm64`

## Authentication

slackcli uses browser session tokens (xoxc + xoxd) - no Slack app creation required.

### Interactive Setup

```bash
./scripts/extract-tokens <workspace-url>
```

This walks the user through extracting tokens from browser DevTools.

### Manual Setup

```bash
slackcli auth login-browser \
  --xoxd="xoxd-..." \
  --xoxc="xoxc-..." \
  --workspace-url=https://your-workspace.slack.com
```

### Verify Auth

```bash
slackcli auth list
```

## Finding Channels

Use `slackcli conversations list` to discover channels and their IDs:

```bash
# List all channels
slackcli conversations list

# Filter output
slackcli conversations list | grep -i "channel-name"
```

## Sending Messages

```bash
# Send to a channel (use channel ID from conversations list)
slackcli messages send --recipient-id=C0XXXXXXXX --message="Hello from CLI"

# Send to a DM (use user's DM channel ID)
slackcli messages send --recipient-id=D0XXXXXXXX --message="Hey"

# Reply in a thread
slackcli messages send --recipient-id=C0XXXXXXXX --message="Thread reply" --thread-ts=1769756026.624319
```

The `--recipient-id` is always a channel ID (C...) or DM channel ID (D...).

## Reading Messages

```bash
# Read last N messages from a channel
slackcli conversations read C0XXXXXXXX --limit=10

# Read as JSON (for parsing)
slackcli conversations read C0XXXXXXXX --limit=10 --json

# Read a thread
slackcli conversations read C0XXXXXXXX --thread-ts=1769756026.624319
```

## Listing Channels

```bash
slackcli conversations list
```

Returns all public channels, private channels, and DMs with their IDs.

## Testing Slack Integrations

To verify a bot or integration posted a message correctly:

```bash
# Read the channel, check for the expected message
slackcli conversations read CHANNEL_ID --limit=5 --json | jq '.messages[] | select(.text | contains("expected text"))'
```

To send a test message and verify the round-trip:

```bash
# Send
slackcli messages send --recipient-id=CHANNEL_ID --message="integration test $(date +%s)"

# Read back
slackcli conversations read CHANNEL_ID --limit=1 --json
```

## Multiple Workspaces

slackcli supports multiple workspaces. Run the auth flow for each workspace you need:

```bash
# Add first workspace
./scripts/extract-tokens https://workspace-one.slack.com

# Add second workspace
./scripts/extract-tokens https://workspace-two.slack.com

# List all authenticated workspaces
slackcli auth list
```

When sending messages, slackcli automatically routes to the correct workspace based on the channel ID.

## Token Notes

- Browser tokens (xoxc/xoxd) act as the logged-in user, not a bot
- Messages sent appear as the user, not an app
- Tokens expire when the user logs out of the browser session
- To refresh: re-extract tokens from a logged-in browser session
- All workspace credentials are stored at `~/.config/slackcli/workspaces.json`
