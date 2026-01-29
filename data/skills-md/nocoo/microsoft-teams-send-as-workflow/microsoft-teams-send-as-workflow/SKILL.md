---
name: microsoft-teams-send-as-workflow
description: Send messages and Adaptive Cards to Microsoft Teams via Incoming Webhook. Use when user requests to send notifications, alerts, or formatted cards to Teams channels. Triggers include requests to post to Teams, Teams webhook, Teams notification, Teams card, or any request to send messages to Microsoft Teams channels.
---

# Microsoft Teams Post

Send messages and Adaptive Cards to Microsoft Teams channels using Incoming Webhook URLs.

## Prerequisites

Users need a Webhook URL from Teams. Guide them to create one if missing:

1. In Teams, go to the target channel
2. Open **Workflows** app (search from Apps or click three dots below input)
3. Find template: **"Post to a channel when a webhook request is received"**
4. Name the workflow (e.g., "CLI Notification Bot")
5. Select target Team and Channel
6. Copy the generated HTTP POST URL

## Quick Start

The bundled script `scripts/send_teams.py` handles all message types.

```bash
python3 scripts/send_teams.py <WEBHOOK_URL> --text "Hello Teams!"
```

## Message Types

### Simple Text Message

For basic notifications and alerts.

```bash
python3 scripts/send_teams.py <WEBHOOK_URL> -t "🚀 Deployment completed successfully"
```

### Adaptive Card

For rich formatted cards with titles, facts, images, and buttons. Pass JSON as string or file.

Inline JSON:
```bash
python3 scripts/send_teams.py <WEBHOOK_URL> -c '{
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "type": "AdaptiveCard",
  "version": "1.4",
  "body": [
    {
      "type": "TextBlock",
      "text": "Build Report",
      "weight": "Bolder",
      "size": "Medium"
    },
    {
      "type": "FactSet",
      "facts": [
        {"title": "Project", "value": "Backend API"},
        {"title": "Status", "value": "✅ Success"},
        {"title": "Duration", "value": "45s"}
      ]
    }
  ]
}'
```

From JSON file:
```bash
python3 scripts/send_teams.py <WEBHOOK_URL> -c card.json
```

### Raw Payload

For custom message structures not covered by text or card modes.

```bash
python3 scripts/send_teams.py <WEBHOOK_URL> -r '{"type": "message", "text": "Custom"}'
```

## Common Patterns

### Build/Deployment Notification

```bash
python3 scripts/send_teams.py <WEBHOOK_URL> -c '{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "body": [
    {"type": "TextBlock", "text": "Deployment Notification", "weight": "Bolder", "size": "Medium"},
    {"type": "TextBlock", "text": "Project: my-app deployed to production", "wrap": true}
  ],
  "actions": [
    {"type": "Action.OpenUrl", "title": "View Logs", "url": "https://ci.example.com/logs/123"}
  ]
}'
```

### Alert with Facts

```bash
python3 scripts/send_teams.py <WEBHOOK_URL> -c '{
  "type": "AdaptiveCard",
  "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
  "version": "1.4",
  "body": [
    {"type": "TextBlock", "text": "⚠️ Alert Summary", "weight": "Bolder"},
    {
      "type": "FactSet",
      "facts": [
        {"title": "Severity", "value": "High"},
        {"title": "Service", "value": "api-gateway"},
        {"title": "Time", "value": "2026-01-23 09:45:00 UTC"}
      ]
    }
  ]
}'
```

## Script Reference

`scripts/send_teams.py`

| Argument | Description |
|----------|-------------|
| `webhook_url` | Teams Incoming Webhook URL (required positional) |
| `-t, --text TEXT` | Send simple text message |
| `-c, --card CARD` | Send Adaptive Card (JSON string or .json file) |
| `-r, --raw RAW` | Send raw custom payload (JSON string or .json file) |
| `-v, --verbose` | Enable verbose output |

Exit codes: 0 on success, 1 on failure.

## Error Handling

The script reports errors clearly:

- `❌ HTTP Error: 401` - Invalid webhook URL
- `❌ HTTP Error: 400` - Malformed JSON or invalid card schema
- `❌ URL Error` - Network connectivity issue
- `✅ Message sent successfully` - Confirmed delivery

For 4xx errors, the response body is printed to help diagnose schema issues.

### Suspended Workflow

If you receive errors indicating the workflow is "suspended" or "inactive":

1. Open Power Automate in your browser:
   - https://make.powerautomate.com
   - OR your org's URL: https://<your-org>.powerautomate.com

2. Go to **My flows** / **Workflows**

3. Find your workflow (look for "Suspended" status)

4. Click → **Resume** / **Activate** / **Turn on**

5. Retry sending your message
