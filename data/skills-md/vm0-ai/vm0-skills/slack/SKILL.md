---
name: slack
description: Slack API for sending messages, reading channels, and managing conversations. Use this skill to post messages, upload files, and interact with Slack workspaces.
vm0_secrets:
  - SLACK_BOT_TOKEN
---

# Slack API

Send messages, read channels, and interact with Slack workspaces.

## When to Use

- Send messages to channels or users
- Read channel message history
- Upload files to Slack
- List channels and users
- Add reactions to messages

## Prerequisites

```bash
export SLACK_BOT_TOKEN=xoxb-your-bot-token
```

### Get Token

1. Create app: https://api.slack.com/apps
2. Add Bot Token Scopes (OAuth & Permissions):
  - `chat:write` - Send messages
  - `channels:read` - List public channels
  - `channels:history` - Read channel messages
  - `files:write` - Upload files
  - `users:read` - List users
  - `reactions:write` - Add reactions
3. Install to Workspace
4. Copy "Bot User OAuth Token" (`xoxb-...`)

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## Core APIs

### List Channels

```bash
bash -c 'curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" "https://slack.com/api/conversations.list?types=public_channel"' | jq '.channels[] | {id, name}'
```

Docs: https://docs.slack.dev/reference/methods/conversations.list

### Get Channel History

Replace `<channel-id>` with the actual channel ID:

```bash
bash -c 'curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" "https://slack.com/api/conversations.history?channel=<channel-id>&limit=10"' | jq '.messages[] | {ts, user, text}'
```

Docs: https://docs.slack.dev/reference/methods/conversations.history

### Send Message

Write to `/tmp/request.json`:

```json
{
  "channel": "<channel-id>",
  "text": "Hello, World"
}
```

```bash
bash -c 'curl -s -X POST "https://slack.com/api/chat.postMessage" -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" -d @/tmp/request.json'
```

Docs: https://docs.slack.dev/reference/methods/chat.postmessage

### Send with Blocks

Write to `/tmp/request.json`:

```json
{
  "channel": "<channel-id>",
  "text": "Notification",
  "blocks": [
    {
      "type": "section",
      "text": {"type": "mrkdwn", "text": "*Alert:* Something happened"}
    },
    {
      "type": "section",
      "fields": [
        {"type": "mrkdwn", "text": "*Status:*\nActive"},
        {"type": "mrkdwn", "text": "*Priority:*\nHigh"}
      ]
    }
  ]
}
```

```bash
bash -c 'curl -s -X POST "https://slack.com/api/chat.postMessage" -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" -d @/tmp/request.json'
```

Block Kit Builder: https://app.slack.com/block-kit-builder

### Reply in Thread

Write to `/tmp/request.json`:

```json
{
  "channel": "<channel-id>",
  "thread_ts": "<thread-timestamp>",
  "text": "Thread reply"
}
```

```bash
bash -c 'curl -s -X POST "https://slack.com/api/chat.postMessage" -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" -d @/tmp/request.json'
```

### Update Message

Write to `/tmp/request.json`:

```json
{
  "channel": "<channel-id>",
  "ts": "<message-timestamp>",
  "text": "Updated message"
}
```

```bash
bash -c 'curl -s -X POST "https://slack.com/api/chat.update" -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" -d @/tmp/request.json'
```

Docs: https://docs.slack.dev/reference/methods/chat.update

### Delete Message

Write to `/tmp/request.json`:

```json
{
  "channel": "<channel-id>",
  "ts": "<message-timestamp>"
}
```

```bash
bash -c 'curl -s -X POST "https://slack.com/api/chat.delete" -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" -d @/tmp/request.json'
```

### List Users

```bash
bash -c 'curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" "https://slack.com/api/users.list"' | jq '.members[] | {id, name, real_name}'
```

Docs: https://docs.slack.dev/reference/methods/users.list

### Get User by Email

Replace `<user-email>` with the actual email address:

```bash
bash -c 'curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" "https://slack.com/api/users.lookupByEmail?email=<user-email>"'
```

Docs: https://docs.slack.dev/reference/methods/users.lookupbyemail

### Upload File

```bash
curl -s -X POST 'https://slack.com/api/files.upload' -H "Authorization: Bearer $SLACK_BOT_TOKEN" -F 'channels=C1234567890' -F 'file=@/path/to/file.txt' -F 'title=My File'
```

Docs: https://docs.slack.dev/reference/methods/files.upload

### Add Reaction

Write to `/tmp/request.json`:

```json
{
  "channel": "<channel-id>",
  "timestamp": "<message-timestamp>",
  "name": "thumbsup"
}
```

```bash
bash -c 'curl -s -X POST "https://slack.com/api/reactions.add" -H "Authorization: Bearer $SLACK_BOT_TOKEN" -H "Content-Type: application/json" -d @/tmp/request.json'
```

Docs: https://docs.slack.dev/reference/methods/reactions.add

## Message Formatting

| Syntax | Result |
|--------|--------|
| `*bold*` | **bold** |
| `_italic_` | _italic_ |
| `~strike~` | ~~strike~~ |
| `` `code` `` | `code` |
| `<URL\|text>` | hyperlink |
| `<@U123>` | @mention user |
| `<#C123>` | #channel link |

## Rate Limits

- Tier 1: 1 request/second
- Tier 2: 20 requests/minute
- Tier 3: 50 requests/minute
- Tier 4: 100 requests/minute

See: https://docs.slack.dev/apis/web-api/rate-limits

## API Reference

- All Methods: https://docs.slack.dev/reference/methods
- Scopes: https://docs.slack.dev/reference/scopes
- Block Kit: https://docs.slack.dev/reference/block-kit
- App Management: https://api.slack.com/apps
