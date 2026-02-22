---
name: gogcli
description: Fast, script-friendly CLI for Google Workspace and Gmail. Use when you need to automate or interact with Gmail (search/send/manage emails), Google Calendar (create/manage events), Google Drive (upload/download/organize files), Google Sheets/Docs/Slides (read/write/export), Contacts, Tasks, Chat, Classroom, Groups, or Keep. Supports JSON output, multiple accounts, batch operations, and least-privilege authentication. Ideal for email automation, calendar management, file operations, data extraction, workspace administration, and integration with Google services.
---

# gogcli - Google Workspace CLI

## Overview

gogcli is a comprehensive command-line interface for Google Workspace services. It provides fast, scriptable access to Gmail, Calendar, Drive, Docs, Sheets, Slides, Contacts, Tasks, Chat, Classroom, Groups, and Keep with JSON-first output and multi-account support.

## Quick Start

### Installation

```bash
# Homebrew
brew install steipete/tap/gogcli

# From source
git clone https://github.com/steipete/gogcli.git
cd gogcli
make
```

### Initial Setup

**Prerequisites:**
- gcloud CLI installed and authenticated
- Google account (Gmail or Workspace)

**Automated setup (recommended):**

```bash
# Run setup script to enable required APIs
# Note: Set SKILL_ROOT to this skill's base directory (scripts are "$SKILL_ROOT/scripts/...").
bash "$SKILL_ROOT/scripts/setup_gcloud_project.sh" PROJECT_ID
```

**Manual setup:**

1. **Create or select Google Cloud project**:
   ```bash
   gcloud projects create PROJECT_ID --name="GoG CLI"
   gcloud config set project PROJECT_ID
   ```

2. **Enable required APIs**:
   ```bash
   # Core services
   gcloud services enable \
     gmail.googleapis.com \
     calendar-json.googleapis.com \
     drive.googleapis.com \
     people.googleapis.com \
     --project=PROJECT_ID
   ```
   
   For all services, see [references/apis.md](references/apis.md).

3. **Configure OAuth consent screen**:
   - Open: https://console.cloud.google.com/apis/credentials/consent
   - User Type: "External"
   - App name: "gog CLI"
   - Add test users: Your Gmail address
   
4. **Create OAuth client**:
   - Open: https://console.cloud.google.com/apis/credentials/oauthclient
   - Application type: "Desktop app"
   - Name: "gog-cli"
   - Download JSON credentials file

5. **Validate credentials** (optional):
   ```bash
    bash "$SKILL_ROOT/scripts/validate_credentials.sh" ~/Downloads/client_secret_*.json
   ```

6. **Store credentials**:
   ```bash
   gog auth credentials ~/Downloads/client_secret_*.json
   ```

7. **Authorize account**:
   ```bash
   gog auth add you@gmail.com
   ```
   
   If you see "Access blocked" error:
   - Ensure your email is added as test user (step 3)
   - Click "Advanced" → "Go to gog CLI (unsafe)"
   - See [references/troubleshooting.md](references/troubleshooting.md) for more

8. **Test authentication**:
   ```bash
   export GOG_ACCOUNT=you@gmail.com
   gog gmail labels list
   gog calendar calendars
   gog drive ls --max 5
   ```

## Core Capabilities

### 1. Gmail Operations

**Search and read emails:**
```bash
# Search threads
gog gmail search 'newer_than:7d' --max 10
gog gmail search 'is:unread from:alice@example.com'

# Search messages (one per email)
gog gmail messages search 'has:attachment' --max 10 --include-body

# Get thread with attachments
gog gmail thread get <threadId> --download --out-dir ./attachments

# Get Gmail web URL
gog gmail url <threadId>
```

**Send and compose:**
```bash
# Send plain text
gog gmail send --to a@b.com --subject "Hello" --body "Message"

# Send HTML
gog gmail send --to a@b.com --subject "Hello" \
  --body "Plain fallback" \
  --body-html "<p>HTML content</p>"

# Send with body from file or stdin
gog gmail send --to a@b.com --subject "Report" --body-file ./report.txt
cat message.txt | gog gmail send --to a@b.com --subject "Data" --body-file -

# Send with tracking (requires setup)
gog gmail send --to a@b.com --subject "Hello" \
  --body-html "<p>Hi!</p>" --track
```

**Manage labels and filters:**
```bash
# List/create labels
gog gmail labels list
gog gmail labels create "My Label"

# Modify thread labels
gog gmail thread modify <threadId> --add STARRED --remove INBOX

# Create filter
gog gmail filters create --from 'noreply@example.com' --add-label 'Notifications'

# Batch operations
gog gmail batch modify <msgId1> <msgId2> --add STARRED --remove INBOX
```

**Email tracking:**
```bash
# Setup tracking (generates tracking ID)
gog gmail track setup --worker-url https://gog-email-tracker.<acct>.workers.dev

# Check opens
gog gmail track opens <tracking_id>
gog gmail track opens --to recipient@example.com
```

### 2. Calendar Management

**List and search events:**
```bash
# Time-based queries
gog calendar events <calendarId> --today
gog calendar events <calendarId> --tomorrow
gog calendar events <calendarId> --week
gog calendar events <calendarId> --days 3
gog calendar events <calendarId> --from today --to friday

# Include weekday columns
gog calendar events <calendarId> --today --weekday

# All calendars
gog calendar events --all

# Search
gog calendar search "meeting" --today
```

**Create and update events:**
```bash
# Basic event
gog calendar create <calendarId> \
  --summary "Meeting" \
  --from 2025-01-15T10:00:00Z \
  --to 2025-01-15T11:00:00Z

# With attendees and location
gog calendar create <calendarId> \
  --summary "Team Sync" \
  --from 2025-01-15T14:00:00Z \
  --to 2025-01-15T15:00:00Z \
  --attendees "alice@example.com,bob@example.com" \
  --location "Zoom" \
  --send-updates all

# Recurring event with reminders
gog calendar create <calendarId> \
  --summary "Payment" \
  --from 2025-02-11T09:00:00-03:00 \
  --to 2025-02-11T09:15:00-03:00 \
  --rrule "RRULE:FREQ=MONTHLY;BYMONTHDAY=11" \
  --reminder "email:3d" \
  --reminder "popup:30m"

# Add attendees (without replacing existing)
gog calendar update <calendarId> <eventId> \
  --add-attendee "alice@example.com,bob@example.com"
```

**Special event types:**
```bash
# Focus time
gog calendar focus-time --from 2025-01-15T13:00:00Z --to 2025-01-15T14:00:00Z

# Out of office
gog calendar out-of-office --from 2025-01-20 --to 2025-01-21 --all-day

# Working location
gog calendar working-location --type office --office-label "HQ" \
  --from 2025-01-22 --to 2025-01-23
```

**Team calendars and availability:**
```bash
# Team events (Workspace)
gog calendar team <group-email> --today
gog calendar team <group-email> --week --freebusy

# Free/busy lookup
gog calendar freebusy --calendars "primary,work@example.com" \
  --from 2025-01-15T00:00:00Z \
  --to 2025-01-16T00:00:00Z

# Find conflicts
gog calendar conflicts --calendars "primary,work@example.com" --today
```

**Respond to invitations:**
```bash
gog calendar respond <calendarId> <eventId> --status accepted
gog calendar respond <calendarId> <eventId> --status declined --send-updates externalOnly
```

### 3. Drive Operations

**Search and organize:**
```bash
# List and search
gog drive ls --max 20
gog drive ls --parent <folderId>
gog drive search "invoice" --max 20

# Get metadata and URL
gog drive get <fileId>
gog drive url <fileId>

# Organize
gog drive mkdir "New Folder"
gog drive rename <fileId> "New Name"
gog drive move <fileId> --parent <destinationFolderId>
gog drive delete <fileId>
gog drive copy <fileId> "Copy Name"
```

**Upload and download:**
```bash
# Upload
gog drive upload ./path/to/file --parent <folderId>

# Download
gog drive download <fileId> --out ./file.bin

# Export Google Workspace files
gog drive download <fileId> --format pdf --out ./doc.pdf
gog drive download <fileId> --format docx --out ./doc.docx
gog drive download <fileId> --format pptx --out ./slides.pptx
```

**Permissions:**
```bash
# List permissions
gog drive permissions <fileId>

# Share
gog drive share <fileId> --email user@example.com --role reader
gog drive share <fileId> --email user@example.com --role writer

# Unshare
gog drive unshare <fileId> --permission-id <permissionId>
```

### 4. Sheets Operations

**Read data:**
```bash
# Get metadata
gog sheets metadata <spreadsheetId>

# Read range
gog sheets get <spreadsheetId> 'Sheet1!A1:B10'
```

**Write data:**
```bash
# Update cells (pipe-delimited for columns, comma for rows)
gog sheets update <spreadsheetId> 'A1' 'val1|val2,val3|val4'

# Update with JSON
gog sheets update <spreadsheetId> 'A1' --values-json '[[\"a\",\"b\"],[\"c\",\"d\"]]'

# Copy validation from another range
gog sheets update <spreadsheetId> 'Sheet1!A1:C1' 'new|row|data' \
  --copy-validation-from 'Sheet1!A2:C2'

# Append rows
gog sheets append <spreadsheetId> 'Sheet1!A:C' 'new|row|data'

# Clear range
gog sheets clear <spreadsheetId> 'Sheet1!A1:B10'
```

**Format and create:**
```bash
# Format cells
gog sheets format <spreadsheetId> 'Sheet1!A1:B2' \
  --format-json '{"textFormat":{"bold":true}}' \
  --format-fields 'userEnteredFormat.textFormat.bold'

# Create spreadsheet
gog sheets create "My Spreadsheet" --sheets "Sheet1,Sheet2"

# Export
gog sheets export <spreadsheetId> --format pdf --out ./sheet.pdf
```

### 5. Docs and Slides

**Docs:**
```bash
# Get info and extract text
gog docs info <docId>
gog docs cat <docId> --max-bytes 10000

# Create and copy
gog docs create "My Doc"
gog docs copy <docId> "My Doc Copy"

# Export
gog docs export <docId> --format pdf --out ./doc.pdf
gog docs export <docId> --format docx --out ./doc.docx
gog docs export <docId> --format txt --out ./doc.txt
```

**Slides:**
```bash
# Create and copy
gog slides create "My Deck"
gog slides copy <presentationId> "My Deck Copy"

# Export
gog slides export <presentationId> --format pptx --out ./deck.pptx
gog slides export <presentationId> --format pdf --out ./deck.pdf
```

### 6. Contacts Management

**Personal contacts:**
```bash
# List and search
gog contacts list --max 50
gog contacts search "Ada" --max 50

# Get contact
gog contacts get people/<resourceName>
gog contacts get user@example.com

# Create contact
gog contacts create \
  --given-name "John" \
  --family-name "Doe" \
  --email "john@example.com" \
  --phone "+1234567890"

# Update and delete
gog contacts update people/<resourceName> --given-name "Jane"
gog contacts delete people/<resourceName>
```

**Other contacts and directory (Workspace):**
```bash
# Other contacts (people you've interacted with)
gog contacts other list --max 50
gog contacts other search "John" --max 50

# Workspace directory
gog contacts directory list --max 50
gog contacts directory search "Jane" --max 50
```

### 7. Tasks

**Manage task lists and tasks:**
```bash
# Task lists
gog tasks lists --max 50
gog tasks lists create "My Tasks"

# Tasks
gog tasks list <tasklistId> --max 50
gog tasks get <tasklistId> <taskId>

# Create tasks
gog tasks add <tasklistId> --title "Task title"
gog tasks add <tasklistId> --title "Weekly sync" --due 2025-02-01 \
  --repeat weekly --repeat-count 4

# Manage tasks
gog tasks update <tasklistId> <taskId> --title "New title"
gog tasks done <tasklistId> <taskId>
gog tasks undo <tasklistId> <taskId>
gog tasks delete <tasklistId> <taskId>
gog tasks clear <tasklistId>
```

### 8. Chat (Workspace)

**Spaces and messages:**
```bash
# List and create spaces
gog chat spaces list
gog chat spaces find "Engineering"
gog chat spaces create "Engineering" \
  --member alice@company.com \
  --member bob@company.com

# Messages
gog chat messages list spaces/<spaceId> --max 5
gog chat messages list spaces/<spaceId> --unread
gog chat messages send spaces/<spaceId> --text "Build complete!"
gog chat messages send spaces/<spaceId> --text "Reply" \
  --thread spaces/<spaceId>/threads/<threadId>

# Direct messages
gog chat dm space user@company.com
gog chat dm send user@company.com --text "ping"
```

### 9. Classroom (Workspace for Education)

**Courses:**
```bash
# List and manage courses
gog classroom courses list
gog classroom courses get <courseId>
gog classroom courses create --name "Math 101"
gog classroom courses archive <courseId>
```

**Coursework and submissions:**
```bash
# Coursework
gog classroom coursework list <courseId>
gog classroom coursework create <courseId> \
  --title "Homework 1" \
  --type ASSIGNMENT \
  --state PUBLISHED

# Submissions
gog classroom submissions list <courseId> <courseworkId>
gog classroom submissions grade <courseId> <courseworkId> <submissionId> --grade 85
gog classroom submissions return <courseId> <courseworkId> <submissionId>
```

### 10. Groups and Keep (Workspace)

**Groups:**
```bash
# List groups
gog groups list

# List members
gog groups members engineering@company.com
```

**Keep (requires service account):**
```bash
# Setup service account first
gog auth service-account set you@yourdomain.com --key ~/service-account.json

# List and search notes
gog keep list --account you@yourdomain.com
gog keep search <query> --account you@yourdomain.com

# Get note and download attachment
gog keep get <noteId> --account you@yourdomain.com
gog keep attachment <attachmentName> --account you@yourdomain.com --out ./file.bin
```

## Authentication and Configuration

### Multiple Accounts

```bash
# Add multiple accounts
gog auth add personal@gmail.com
gog auth add work@company.com

# Use aliases
gog auth alias set work work@company.com
gog gmail search 'is:unread' --account work

# Set default
export GOG_ACCOUNT=work@company.com
gog gmail search 'is:unread'
```

### Multiple OAuth Clients (Workspace)

```bash
# Store named OAuth client
gog --client work auth credentials ~/work-client.json

# Use with account
gog --client work auth add you@company.com

# Auto-select by domain
gog --client work auth credentials ~/work.json --domain example.com
```

### Service Accounts (Workspace)

For domain-wide delegation:

1. Create service account in Google Cloud Console
2. Enable domain-wide delegation
3. Download JSON key
4. Allowlist scopes in Workspace Admin Console
5. Configure gogcli:

```bash
gog auth service-account set you@yourdomain.com --key ~/service-account.json
gog --account you@yourdomain.com auth status
```

### Service Scopes

```bash
# Request specific services
gog auth add you@gmail.com --services drive,calendar

# Read-only scopes
gog auth add you@gmail.com --services drive,calendar --readonly

# Drive scope control
gog auth add you@gmail.com --services drive --drive-scope readonly

# Add services later (force consent if needed)
gog auth add you@gmail.com --services sheets --force-consent
```

### Keyring Backend

```bash
# Show current backend
gog auth keyring

# Set backend
gog auth keyring file      # Encrypted on-disk
gog auth keyring keychain  # macOS Keychain
gog auth keyring auto      # Best available

# For non-interactive use (file backend)
export GOG_KEYRING_PASSWORD='...'
gog --no-input auth status
```

## Output Formats

### JSON Output (for scripting)

```bash
# Enable JSON output
gog gmail search 'newer_than:7d' --max 3 --json
gog calendar events primary --today --json

# Use with jq
gog --json drive ls --max 5 | jq '.files[] | select(.mimeType=="application/pdf")'

# Environment variable
export GOG_JSON=1
gog gmail search 'is:unread'
```

### Plain Text (TSV)

```bash
# Stable, parseable output
gog gmail search 'newer_than:7d' --plain
gog calendar events primary --today --plain
```

### Human-Friendly (default)

Colored tables on stdout, progress/hints on stderr.

## Common Patterns

### Email Automation

```bash
# Search and download attachments
gog gmail search 'newer_than:7d has:attachment' --max 10
gog gmail thread get <threadId> --download

# Batch label management
gog --json gmail search 'from:noreply@example.com' --max 200 | \
  jq -r '.threads[].id' | \
  xargs -n 50 gog gmail labels modify --remove UNREAD

# Archive old emails
gog --json gmail search 'older_than:1y' --max 200 | \
  jq -r '.threads[].id' | \
  xargs -n 50 gog gmail labels modify --remove INBOX
```

### Calendar Integration

```bash
# Find free time and create meeting
gog calendar freebusy --calendars "primary" \
  --from 2025-01-15T00:00:00Z --to 2025-01-16T00:00:00Z

gog calendar create primary \
  --summary "Team Standup" \
  --from 2025-01-15T10:00:00Z \
  --to 2025-01-15T10:30:00Z \
  --attendees "alice@example.com,bob@example.com"
```

### File Operations

```bash
# Search and download PDFs
gog drive search "invoice filetype:pdf" --max 20 --json | \
  jq -r '.files[] | .id' | \
  while read fileId; do
    gog drive download "$fileId"
  done
```

### Sheets Data Management

```bash
# Update sheet from CSV
cat data.csv | tr ',' '|' | \
  gog sheets update <spreadsheetId> 'Sheet1!A1'

# Read and process with jq
gog sheets get <spreadsheetId> 'Sheet1!A1:B10' --json | \
  jq '.values'
```

## Global Flags and Environment

**Flags:**
- `--account <email|alias|auto>` - Account to use
- `--client <name>` - OAuth client name
- `--json` - JSON output
- `--plain` - Plain text output (TSV)
- `--color <mode>` - Color mode (auto/always/never)
- `--force` - Skip confirmations
- `--no-input` - Never prompt (fail instead)
- `--verbose` - Verbose logging
- `--enable-commands <csv>` - Command allowlist for sandboxing

**Environment variables:**
- `GOG_ACCOUNT` - Default account
- `GOG_CLIENT` - OAuth client
- `GOG_JSON` - Default JSON output
- `GOG_PLAIN` - Default plain output
- `GOG_COLOR` - Color mode
- `GOG_TIMEZONE` - Default timezone
- `GOG_ENABLE_COMMANDS` - Command allowlist
- `GOG_KEYRING_BACKEND` - Keyring backend
- `GOG_KEYRING_PASSWORD` - Keyring password

## Reference Documentation

- **Command reference**: [references/commands.md](references/commands.md) - Comprehensive command reference with all options
- **API and scopes**: [references/apis.md](references/apis.md) - Required APIs and OAuth scopes by service
- **Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md) - Common issues and solutions

## Tips and Best Practices

1. **Use JSON output for scripting** - Combine with `jq` for powerful pipelines
2. **Set default account** - Use `GOG_ACCOUNT` to avoid repeating `--account`
3. **Use aliases** - Create short aliases for frequently used accounts
4. **Batch operations** - Use `xargs` with JSON output for bulk operations
5. **Time zones** - Use `--timezone` or `GOG_TIMEZONE` for consistent calendar output
6. **Service scopes** - Request only needed scopes with `--services`
7. **Keyring backend** - Use `file` backend for CI/containers
8. **Command sandboxing** - Use `--enable-commands` for agent runs
9. **Read-only access** - Use `--readonly` flag when appropriate
10. **Error handling** - Use `--no-input` for non-interactive scripts

## Links

- **GitHub**: https://github.com/steipete/gogcli
- **Website**: https://gogcli.sh
- **Gmail API**: https://developers.google.com/gmail/api
- **Calendar API**: https://developers.google.com/calendar
- **Drive API**: https://developers.google.com/drive
