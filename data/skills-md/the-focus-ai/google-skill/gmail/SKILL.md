---
name: gmail
description: This skill should be used when the user asks to "read emails", "send an email", "search gmail", "list messages", "check inbox", "manage labels", "find emails from", "check my calendar", "list events", "create an event", "schedule a meeting", "send styled email", "send markdown email", "create a draft", "draft an email", or mentions Gmail/Calendar operations. Provides Gmail and Google Calendar API integration.
version: 0.9.0
---

# Gmail & Calendar Skill

Read, send, search Gmail. List, create, delete calendar events.

## First-Time Setup

Run `npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts auth` to authenticate with Google. This opens a browser for OAuth consent.

Tokens are stored per-project in `.claude/google-skill.local.json`.

## Using Your Own Credentials (Optional)

By default, this skill uses embedded OAuth credentials. To use your own Google Cloud project credentials instead:

1. Create a Google Cloud project and enable the required APIs (Gmail, Calendar, Sheets, Docs, YouTube, Drive)
2. Create OAuth 2.0 credentials (Desktop app type)
3. Download the JSON and save to `~/.config/google-skill/credentials.json`

The skill will automatically use your credentials if that file exists.

## Gmail Commands

```bash
# List messages
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts list
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts list --query="is:unread" --max=5

# Read message
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts read <message-id>

# Send email (plain text)
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send \
  --to="recipient@example.com" \
  --subject="Hello" \
  --body="Message content"

# Send HTML email
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send \
  --to="recipient@example.com" \
  --subject="Hello" \
  --body="Plain text fallback" \
  --html="<h1>Hello</h1><p>HTML content</p>"

# Send with attachments
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send \
  --to="recipient@example.com" \
  --subject="With files" \
  --body="See attached" \
  --attachment="/path/to/file.pdf,/path/to/other.docx"

# Send HTML with inline images
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send \
  --to="recipient@example.com" \
  --subject="Newsletter" \
  --body="Plain text version" \
  --html="<h1>Hello</h1><img src='cid:logo'>" \
  --inline="/path/to/logo.png:logo"

# Labels
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts labels
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts label <id> --add="IMPORTANT"

# Download as EML
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts download <message-id>

# Send markdown as styled HTML email (Focus.AI branding)
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send-md \
  --to="recipient@example.com" \
  --file="/path/to/report.md" \
  --style=client  # or "labs" for Focus.AI Labs style

# Subject defaults to first H1 in markdown, or specify explicitly:
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send-md \
  --to="recipient@example.com" \
  --file="report.md" \
  --style=labs \
  --subject="Weekly Report"

# Create as draft instead of sending:
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts send-md \
  --to="recipient@example.com" \
  --file="report.md" \
  --draft

# Create a draft email (plain text or HTML)
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts draft \
  --to="recipient@example.com" \
  --subject="Draft Subject" \
  --body="Draft content"

# Create HTML draft with attachments
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts draft \
  --to="recipient@example.com" \
  --subject="Draft with files" \
  --body="Plain text fallback" \
  --html="<h1>Hello</h1>" \
  --attachment="/path/to/file.pdf"
```

## Styled Email Templates

The `send-md` command converts markdown to beautifully styled HTML emails using Focus.AI brand guidelines:

- **client** (default): Professional style with teal accents, subtle borders, rounded corners
- **labs**: Bold experimental style with black borders, box shadows, uppercase headers

Supports: headings, bold/italic, links, code blocks, tables, lists, blockquotes, horizontal rules.

## Calendar Commands

```bash
# List calendars
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts calendars

# List upcoming events
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts events
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts events --max=20

# Get event details
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts event <event-id>

# Create event
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts create \
  --summary="Meeting" \
  --start="2026-01-15T10:00:00" \
  --end="2026-01-15T11:00:00" \
  --location="Conference Room" \
  --description="Discuss project"

# Delete event
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts delete <event-id>
```

## Search Operators (Gmail)

| Operator | Example | Description |
|----------|---------|-------------|
| `from:` | `from:alice@example.com` | From sender |
| `to:` | `to:bob@example.com` | To recipient |
| `subject:` | `subject:meeting` | Subject contains |
| `is:unread` | `is:unread` | Unread only |
| `has:attachment` | `has:attachment` | Has attachments |
| `newer_than:` | `newer_than:7d` | Within N days |
| `label:` | `label:work` | Has label |

## Output

All commands return JSON with `success` and `data` fields.

## Check Auth

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts check
```

## Help

```bash
npx tsx ${CLAUDE_PLUGIN_ROOT}/scripts/gmail.ts --help
```
