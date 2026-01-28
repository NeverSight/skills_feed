---
name: slack-webhook
description: Send messages to Slack using Incoming Webhooks. Simple one-way messaging to a specific channel without OAuth setup.
vm0_secrets:
  - SLACK_WEBHOOK_URL
---

# Slack Incoming Webhook

Send messages to a Slack channel using Incoming Webhooks. No OAuth or bot setup required.

## When to Use

- Send notifications to a specific channel
- CI/CD notifications, alerts, status updates
- Quick integration without full Slack app setup

## Prerequisites

```bash
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXX
```

### Get Webhook URL

1. Create app: https://api.slack.com/apps → **Create New App** → **From scratch**
2. Select **Incoming Webhooks** → Toggle **On**
3. Click **Add New Webhook to Workspace**
4. Select channel → **Allow**
5. Copy Webhook URL

> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## Usage

### Simple Message

Write to `/tmp/slack_request.json`:

```json
{
  "text": "Hello, world."
}
```

Then run:

```bash
bash -c 'curl -X POST $SLACK_WEBHOOK_URL -H "Content-type: application/json" -d @/tmp/slack_request.json'
```

### With Formatting

Write to `/tmp/slack_request.json`:

```json
{
  "text": "*Bold* and _italic_ text"
}
```

Then run:

```bash
bash -c 'curl -X POST $SLACK_WEBHOOK_URL -H "Content-type: application/json" -d @/tmp/slack_request.json'
```

### With Link

Write to `/tmp/slack_request.json`:

```json
{
  "text": "Check <https://example.com|this link>"
}
```

Then run:

```bash
bash -c 'curl -X POST $SLACK_WEBHOOK_URL -H "Content-type: application/json" -d @/tmp/slack_request.json'
```

### With Blocks (Rich Layout)

Write to `/tmp/slack_request.json`:

```json
{
  "text": "New review submitted",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "Danny left the following review:"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "<https://example.com|Overlook Hotel>\n:star:\nDoors had too many axe holes."
      }
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -X POST $SLACK_WEBHOOK_URL -H "Content-type: application/json" -d @/tmp/slack_request.json'
```

### With Fields

Write to `/tmp/slack_request.json`:

```json
{
  "text": "Deployment status",
  "blocks": [
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Environment:*\nProduction"
        },
        {
          "type": "mrkdwn",
          "text": "*Status:*\nSuccess"
        }
      ]
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -X POST $SLACK_WEBHOOK_URL -H "Content-type: application/json" -d @/tmp/slack_request.json'
```

## Message Formatting

| Syntax | Result |
|--------|--------|
| `*bold*` | **bold** |
| `_italic_` | _italic_ |
| `~strike~` | ~~strike~~ |
| `` `code` `` | `code` |
| `\n` | newline |
| `<URL\|text>` | hyperlink |
| `:emoji:` | emoji |

## Shell Escaping

Messages with `!` may fail due to shell history expansion. Use heredoc:

```bash
bash -c 'curl -s -X POST $SLACK_WEBHOOK_URL -H "Content-type: application/json" -d @-' << 'EOF'
{"text":"Deploy completed! :rocket:"}
EOF
```

## Response

Success: `ok` (HTTP 200)

Errors:
- `invalid_payload` - Malformed JSON
- `no_text` - Missing `text` field
- `no_service` - Webhook disabled or invalid
- `channel_not_found` - Channel deleted
- `channel_is_archived` - Channel archived
- `action_prohibited` - Admin restriction

## Limitations

- One webhook = one channel only
- Cannot override username or icon (set in app config)
- Send only (no reading messages)
- Cannot delete messages after posting
- Rate limit: 1 message/second

For full API access, use the `slack` skill with Bot Token.

## API Reference

- Webhooks Guide: https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks
- Block Kit Builder: https://app.slack.com/block-kit-builder
- Message Formatting: https://docs.slack.dev/messaging/formatting-message-text
