---
name: gmail
description: Full CRUD Gmail interactions — search, read, draft, send, reply, reply-all, forward, trash, labels, and attachments.
---

# Gmail Skill

Full CRUD Gmail management for AI agents. Search, read, compose, reply, forward, and manage messages.

## Features

- **Search**: Advanced filtering using Gmail query syntax (from, to, subjects, labels, date ranges).
- **Read**: Fetch full message body, headers, and metadata.
- **Thread**: Read entire conversation threads.
- **Draft**: Create draft emails for the user to review.
- **Send**: Send emails directly.
- **Reply**: Reply to the sender of a message.
- **Reply All**: Reply to all recipients (sender + To + Cc, minus self).
- **Forward**: Forward a message with attribution header to new recipients.
- **Trash / Untrash**: Move messages to/from the trash.
- **Labels**: List labels. Add/remove labels on messages.
- **Attachments**: List and download message attachments.

## Prerequisites

1.  **Google Cloud Project** with **Gmail API** enabled.
2.  **OAuth 2.0 Credentials** — either `gcloud` ADC or `credentials.json`.

## Setup

### ⚡ Quick Setup (Recommended)

Set up Gmail, Calendar, and Contacts all at once:

```bash
uv run ~/.agents/skills/gmail/scripts/setup_workspace.py
```

### Manual Setup

1.  **Using gcloud ADC**:

    ```bash
    gcloud auth application-default login \
      --scopes https://mail.google.com/,https://www.googleapis.com/auth/cloud-platform
    ```

    Then verify:

    ```bash
    uv run skills/gmail/scripts/gmail.py verify
    ```

2.  **Alternative (credentials.json)**:
    - Place `credentials.json` in `~/.gmail_credentials/`.
    - Run `uv run skills/gmail/scripts/gmail.py setup`

## Usage

### Search for Emails

```bash
# Find unread emails from Obi-Wan
uv run skills/gmail/scripts/gmail.py search --query "from:obiwan@jedi.org is:unread"

# Find emails with attachments about Death Star plans
uv run skills/gmail/scripts/gmail.py search --query "has:attachment subject:plans" --limit 5
```

### Read a Single Message (Full Body)

```bash
uv run skills/gmail/scripts/gmail.py read --id "18e..."
```

### Read an Entire Thread

```bash
uv run skills/gmail/scripts/gmail.py thread --id "18e..."
```

### Create a Draft

**Safest option** — creates a draft for the user to review before sending.

```bash
uv run skills/gmail/scripts/gmail.py draft \
  --to "yoda@dagobah.net" \
  --subject "Training Schedule" \
  --body "Master, when shall we begin the next session?" \
  --cc "mace@jedi.org"
```

### Send an Email Directly

```bash
uv run skills/gmail/scripts/gmail.py send \
  --to "yoda@dagobah.net" \
  --subject "Urgent: Sith Sighting" \
  --body "Master, I sense a disturbance in the Force."
```

### Reply to a Message

```bash
# Reply (creates a draft by default)
uv run skills/gmail/scripts/gmail.py reply --id "18e..." --body "Acknowledged, Master."

# Reply and send immediately
uv run skills/gmail/scripts/gmail.py reply --id "18e..." --body "Acknowledged." --send
```

### Reply to All

```bash
uv run skills/gmail/scripts/gmail.py reply-all --id "18e..." --body "Council noted." --send
```

### Forward a Message

```bash
# Forward with a note (creates a draft by default)
uv run skills/gmail/scripts/gmail.py forward \
  --id "18e..." \
  --to "luke@tatooine.net" \
  --body "FYI — see the original message below."

# Forward and send immediately
uv run skills/gmail/scripts/gmail.py forward \
  --id "18e..." \
  --to "luke@tatooine.net" \
  --send
```

### Trash / Untrash

```bash
uv run skills/gmail/scripts/gmail.py trash --id "18e..."
uv run skills/gmail/scripts/gmail.py untrash --id "18e..."
```

### Label Management

```bash
# List all labels
uv run skills/gmail/scripts/gmail.py labels

# Add/remove labels
uv run skills/gmail/scripts/gmail.py modify-labels --id "18e..." --add STARRED --remove UNREAD
```

### Download Attachments

```bash
uv run skills/gmail/scripts/gmail.py attachments --id "18e..." --output-dir ./downloads
```

## Safety Guidelines

1.  **Prefer `draft` over `send`** for new compositions — let the user review first.
2.  **Reply/Forward defaults to draft** — use `--send` flag only when explicitly requested.
3.  **Trash is reversible** — messages can be untrashed. Permanent deletion is intentionally not exposed.
4.  **Threading**: Reply, reply-all, and forward use proper `In-Reply-To` and `References` headers so Gmail threads them correctly.

## JSON Output Structure

All commands produce JSON for easy parsing.

**Search Result:**

```json
[
  {
    "id": "18e...",
    "threadId": "18e...",
    "snippet": "Help me, Obi-Wan Kenobi...",
    "from": "Leia Organa <leia@alderaan.gov>",
    "to": "obiwan@jedi.org",
    "subject": "Urgent Message",
    "date": "Mon, 13 Feb 2026 10:00:00 -0700",
    "labels": ["INBOX", "UNREAD"]
  }
]
```

**Read Result (includes full body):**

```json
{
  "id": "18e...",
  "threadId": "18e...",
  "body": "Full message text...",
  "attachments": [
    { "filename": "plans.pdf", "mimeType": "application/pdf", "size": "42000" }
  ]
}
```
