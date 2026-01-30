---
name: google-workspace
description: Unified Google Workspace integration for managing email, calendar, files, and communication across multiple accounts
triggers:
  # Gmail
  - "check email"
  - "read email"
  - "send email"
  - "search email"
  - "list emails"
  - "unread emails"
  - "inbox"
  # Calendar
  - "check calendar"
  - "schedule meeting"
  - "create event"
  - "what's on my calendar"
  - "free time"
  - "upcoming meetings"
  # Drive
  - "find file"
  - "search drive"
  - "list documents"
  - "open document"
  - "create document"
  # Docs/Sheets/Slides
  - "create doc"
  - "create spreadsheet"
  - "create presentation"
  - "edit document"
  # Tasks
  - "google tasks"
  - "task list"
  # Chat
  - "send chat"
  - "check chat"
allowed-tools: Read, Bash
version: 0.1.0
---

# Google Workspace Skill

## Overview

Unified Google Workspace integration for managing email, calendar, files, and communication across three accounts:

| Alias | Purpose | Email |
|-------|---------|-------|
| `psd` | Work | PSD district email |
| `kh` | Personal | Personal Gmail |
| `hrg` | Business | Consulting & real estate |

## Account Selection

### Explicit
- "check my **psd** email"
- "send email from **hrg**"
- "**kh** calendar for tomorrow"

### Inferred
Geoffrey will infer the appropriate account from context:
- Work-related → `psd`
- Personal matters → `kh`
- Business/real estate → `hrg`

## Available Operations

### Gmail

| Script | Description | Example |
|--------|-------------|---------|
| `list_messages.js` | List inbox, unread, by label | "show unread psd emails" |
| `read_message.js` | Get full message content | "read that email" |
| `send_message.js` | Compose and send | "send email to John about..." |
| `send_with_attachment.js` | Send with file attachment | "email report with PDF attached" |
| `search_messages.js` | Search with Gmail operators | "find emails from Sarah last week" |
| `get_unread_summary.js` | Unread count + top messages | "how many unread emails?" |

### Calendar

| Script | Description | Example |
|--------|-------------|---------|
| `list_events.js` | Get upcoming events | "what's on my calendar today" |
| `create_event.js` | Schedule new events | "schedule meeting tomorrow at 2pm" |
| `update_event.js` | Modify existing events | "move that meeting to 3pm" |
| `search_events.js` | Find by criteria | "find meetings with Mike" |

### Drive

| Script | Description | Example |
|--------|-------------|---------|
| `list_files.js` | Browse/search files | "find budget spreadsheet" |
| `read_file.js` | Get file content | "show me that document" |
| `create_file.js` | Create new docs/sheets | "create a new spreadsheet" |
| `upload_file.js` | Upload local file | "upload this to drive" |

### Tasks

| Script | Description | Example |
|--------|-------------|---------|
| `list_tasks.js` | Get task lists | "show my google tasks" |
| `create_task.js` | Add new task | "add task to google tasks" |
| `complete_task.js` | Mark done | "complete that task" |

### Chat

| Script | Description | Example |
|--------|-------------|---------|
| `list_spaces.js` | Get available spaces | "list chat spaces" |
| `send_message.js` | Post to space | "send message to team chat" |
| `read_messages.js` | Get chat history | "show recent chat messages" |

## Usage Patterns

### Running Scripts

All scripts use the token_manager for authentication:

```javascript
const { getAuthClient } = require('./auth/token_manager');

async function main() {
  const account = process.argv[2] || 'psd';
  const auth = await getAuthClient(account);

  // Use auth with Google API
  const gmail = google.gmail({ version: 'v1', auth });
  // ...
}
```

### Output Format

All scripts return JSON:

```json
{
  "success": true,
  "account": "psd",
  "data": { ... },
  "metadata": {
    "timestamp": "2024-01-15T10:30:00Z",
    "count": 5
  }
}
```

### Error Handling

```json
{
  "error": "Token expired",
  "account": "psd",
  "action": "Run: node token_manager.js refresh psd"
}
```

## Setup Required

Before using this skill:

1. Complete Google Cloud Console setup (see `auth/GOOGLE_CLOUD_SETUP.md`)
2. Add credentials to `~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/secrets/.env`
3. Authenticate all three accounts
4. For PSD account: allowlist OAuth app in Google Admin

## Cross-Account Operations

Some operations work across accounts:
- "Forward this to my personal email"
- "Copy this file to my work drive"
- "Add to both calendars"

## Gmail Search Operators

Support standard Gmail search:
- `from:` - sender
- `to:` - recipient
- `subject:` - subject line
- `has:attachment` - with attachments
- `after:` / `before:` - date range
- `is:unread` - unread only
- `label:` - by label

Example: "search psd email for `from:boss@psd.org after:2024-01-01 has:attachment`"

## Notes

- Access tokens expire after 1 hour (auto-refreshed)
- Refresh tokens don't expire unless revoked
- All API calls are rate-limited by Google
- Keep API has limited availability (may not be enabled)
