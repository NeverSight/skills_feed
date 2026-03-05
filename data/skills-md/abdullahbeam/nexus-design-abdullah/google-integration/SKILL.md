---
name: google-integration
version: 1.1
description: "Complete Google Workspace integration (Gmail, Docs, Sheets, Calendar, Drive, Tasks, Slides). Load when user mentions 'google', 'gmail', 'email', 'google docs', 'google sheets', 'spreadsheet', 'google calendar', 'schedule meeting', 'calendar', 'google drive', 'upload file', 'download file', 'google tasks', 'todo', 'google slides', 'presentation', or any Google service operation."
---

# Google Integration

Complete Google Workspace integration with unified OAuth authentication. One login grants access to Gmail, Google Docs, Google Sheets, Google Calendar, Google Drive, Google Tasks, and Google Slides.

## Purpose

Provides a unified interface to Google Workspace services with:
- **Single authentication** - Login once, use all services
- **Shared credentials** - One OAuth setup for everything
- **Consistent patterns** - Same error handling across all services

## Included Services

| Service | Description | Operations |
|---------|-------------|------------|
| **Gmail** | Email operations | Read, send, reply, forward, drafts, labels |
| **Google Docs** | Document operations | Read, write, create, export, format |
| **Google Sheets** | Spreadsheet operations | Read, write, append, create, format |
| **Google Calendar** | Calendar operations | List events, create, update, find slots, check availability |
| **Google Drive** | File storage operations | Upload, download, share, organize folders |
| **Google Tasks** | Task management | Create, complete, organize task lists |
| **Google Slides** | Presentation operations | Create, edit slides, add text/images, export |

---

## First-Time Setup

**New users**: Say `"connect google"` to run the interactive setup wizard.

The wizard guides you through:
1. Creating a Google Cloud project
2. Enabling required APIs
3. Creating OAuth credentials
4. Authenticating with your Google account

---

## Pre-Flight Check (ALWAYS RUN FIRST)

```bash
python3 00-system/skills/google/google-master/scripts/check_google_config.py --json
```

**Exit codes:**
- **0**: Ready - all services available
- **1**: Need login - run the login command below
- **2**: Missing credentials or dependencies

**To authenticate (grants access to ALL services):**
```bash
python3 00-system/skills/google/google-master/scripts/google_auth.py --login
```

---

## Quick Start by Service

### Gmail
```bash
# List recent emails
python3 00-system/skills/google/gmail/scripts/gmail_operations.py list --max 10

# Send email (creates draft first, asks for confirmation)
python3 00-system/skills/google/gmail/scripts/gmail_operations.py send --to "user@example.com" --subject "Hello" --body "Message"
```

### Google Docs
```bash
# Read document
python3 00-system/skills/google/google-docs/scripts/docs_operations.py read <document_id>

# Create document
python3 00-system/skills/google/google-docs/scripts/docs_operations.py create "My Document" --content "Initial content"
```

### Google Sheets
```bash
# Read data
python3 00-system/skills/google/google-sheets/scripts/sheets_operations.py read <spreadsheet_id> "Sheet1!A1:D10"

# Append rows
python3 00-system/skills/google/google-sheets/scripts/sheets_operations.py append <spreadsheet_id> "Sheet1!A:D" --values '[["New", "Row", "Data"]]'
```

### Google Calendar
```bash
# List upcoming events
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py list --max 10

# Find available slots
python3 00-system/skills/google/google-calendar/scripts/calendar_operations.py find-slots --duration 30 --from "2025-12-16" --to "2025-12-20"
```

### Google Drive
```bash
# List files in root
python3 00-system/skills/google/google-drive/scripts/drive_operations.py list

# Upload file
python3 00-system/skills/google/google-drive/scripts/drive_operations.py upload ./local_file.pdf

# Download file
python3 00-system/skills/google/google-drive/scripts/drive_operations.py download <file_id> --output ./downloaded.pdf
```

### Google Tasks
```bash
# List tasks
python3 00-system/skills/google/google-tasks/scripts/tasks_operations.py tasks

# Create task
python3 00-system/skills/google/google-tasks/scripts/tasks_operations.py create "Call John" --due 2025-12-20

# Complete task
python3 00-system/skills/google/google-tasks/scripts/tasks_operations.py complete <task_id>
```

### Google Slides
```bash
# List presentations
python3 00-system/skills/google/google-slides/scripts/slides_operations.py list

# Create presentation
python3 00-system/skills/google/google-slides/scripts/slides_operations.py create "Q4 Report"

# Export to PDF
python3 00-system/skills/google/google-slides/scripts/slides_operations.py export <presentation_id> ./report.pdf
```

---

## Structure

```
google/
├── SKILL.md                          # This file (bundle overview)
├── google-connect/                   # Setup wizard (say "connect google")
│   └── SKILL.md                      # Interactive setup workflow
├── google-master/                    # Shared resources (DO NOT load directly)
│   ├── SKILL.md                      # Documentation for shared resources
│   ├── scripts/
│   │   ├── google_auth.py            # Unified OAuth for all services
│   │   └── check_google_config.py    # Pre-flight validation
│   └── references/
│       ├── setup-guide.md            # Complete setup instructions
│       └── error-handling.md         # Common errors and solutions
├── gmail/
│   ├── SKILL.md                      # Gmail-specific docs
│   └── scripts/gmail_operations.py
├── google-docs/
│   ├── SKILL.md                      # Docs-specific docs
│   └── scripts/docs_operations.py
├── google-sheets/
│   ├── SKILL.md                      # Sheets-specific docs
│   └── scripts/sheets_operations.py
├── google-calendar/
│   ├── SKILL.md                      # Calendar-specific docs
│   └── scripts/calendar_operations.py
├── google-drive/
│   ├── SKILL.md                      # Drive-specific docs
│   └── scripts/drive_operations.py
├── google-tasks/
│   ├── SKILL.md                      # Tasks-specific docs
│   └── scripts/tasks_operations.py
└── google-slides/
    ├── SKILL.md                      # Slides-specific docs
    └── scripts/slides_operations.py
```

---

## Setup

### Prerequisites
```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```

### 1. Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Enable APIs: Gmail, Docs, Sheets, Calendar, Drive, Tasks, Slides

### 2. Create OAuth Credentials
1. Go to APIs & Services > Credentials
2. Create OAuth 2.0 Client ID (Desktop app)
3. Copy the **Client ID** and **Client Secret**
4. Add to `.env` file (at Nexus root):
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_PROJECT_ID=your-project-id
   ```

### 3. Authenticate
```bash
python3 00-system/skills/google/google-master/scripts/google_auth.py --login
```

This opens a browser to grant permissions for all services at once.

For detailed setup: [google-master/references/setup-guide.md](google-master/references/setup-guide.md)

---

## Error Handling

See [google-master/references/error-handling.md](google-master/references/error-handling.md) for:
- Authentication errors (401, 403)
- Rate limiting (429)
- Permission issues
- Token refresh problems

---

## File Locations

| File | Path | Purpose |
|------|------|---------|
| OAuth credentials | `.env` (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_PROJECT_ID) | App identity |
| Access token | `01-memory/integrations/google-token.json` | User's auth token |

Both `.env` and token file are in `.gitignore` and will not be committed.

---

## Security Notes

- **Credentials** (`.env` file) - in `.gitignore`, never committed
- **Token file** (`google-token.json`) - in `.gitignore`, never committed
- Each user authenticates with their own Google account
