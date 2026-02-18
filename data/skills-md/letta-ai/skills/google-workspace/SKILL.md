---
name: google-workspace
description: Connect to Gmail and Google Calendar via OAuth 2.0. Use when users want to search/read emails, create drafts, search calendar events, check availability, or schedule meetings. Triggers on queries about email, inbox, calendar, schedule, or meetings.
license: MIT
---

# Google Workspace Integration

Gmail and Google Calendar access via shared OAuth 2.0 authentication.

## Prerequisites

1. Python 3.10+ available
2. Google Cloud project with Gmail API and Calendar API enabled
3. OAuth 2.0 credentials (`credentials.json`) downloaded
4. Required packages: `google-api-python-client`, `google-auth-httplib2`, `google-auth-oauthlib`

## OAuth Setup

### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create a new project or select existing
3. Navigate to **APIs & Services** → **Library**
4. Enable both **Gmail API** and **Google Calendar API**

### Step 2: Configure OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Select **External** user type
3. Add scopes:
   - `https://www.googleapis.com/auth/gmail.readonly`
   - `https://www.googleapis.com/auth/gmail.compose`
   - `https://www.googleapis.com/auth/gmail.modify`
   - `https://www.googleapis.com/auth/calendar.readonly`
   - `https://www.googleapis.com/auth/calendar.events`
4. Add user's email as a test user

### Step 3: Create OAuth Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Select **Desktop app** as application type
4. Download JSON and rename to `credentials.json`

### Step 4: Install Dependencies
```bash
uv add google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### Step 5: First Authentication
Run any script - it will open a browser for OAuth consent. A `token.json` is saved for future use.

---

## Gmail Operations

### Search Emails
```bash
uv run python tools/google-workspace/scripts/search_emails.py "from:someone@example.com" --credentials ./credentials.json
```

### Read Email Content
```bash
uv run python tools/google-workspace/scripts/read_email.py <message_id> --credentials ./credentials.json
```

### Create Draft
```bash
uv run python tools/google-workspace/scripts/create_draft.py \
  --to "recipient@example.com" \
  --subject "Subject line" \
  --body "Email body" \
  --credentials ./credentials.json
```

### Find Emails Needing Reply
```bash
uv run python tools/google-workspace/scripts/needs_reply.py --credentials ./credentials.json
```

---

## Calendar Operations

### List Calendars
```bash
uv run python tools/google-workspace/scripts/list_calendars.py --credentials ./credentials.json
```

### Search Events
```bash
# Search by text
uv run python tools/google-workspace/scripts/search_events.py "meeting" --credentials ./credentials.json

# Search by date range
uv run python tools/google-workspace/scripts/search_events.py --start "2024-01-15" --end "2024-01-20" --credentials ./credentials.json
```

### Check Availability
```bash
uv run python tools/google-workspace/scripts/find_busy.py \
  --start "2024-01-15T09:00:00" \
  --end "2024-01-15T17:00:00" \
  --credentials ./credentials.json
```

### Create Event
```bash
uv run python tools/google-workspace/scripts/create_event.py \
  --summary "Team Meeting" \
  --start "2024-01-15T10:00:00" \
  --end "2024-01-15T11:00:00" \
  --attendees "alice@example.com,bob@example.com" \
  --credentials ./credentials.json
```

**Options:** `--description`, `--location`, `--timezone`, `--calendar`

---

## Scripts Reference

**Gmail:**
- `gmail_auth.py` - Gmail authentication utilities
- `search_emails.py` - Search inbox with Gmail query syntax
- `read_email.py` - Read email content by message ID
- `create_draft.py` - Create draft emails
- `needs_reply.py` - Find emails awaiting response

**Calendar:**
- `calendar_auth.py` - Calendar authentication utilities
- `list_calendars.py` - List accessible calendars
- `search_events.py` - Search events by text/date
- `find_busy.py` - Check free/busy periods
- `create_event.py` - Create calendar events

## Common Workflows

### Schedule a Meeting
1. Search calendar for availability: `search_events.py --start ... --end ...`
2. Create event: `create_event.py --summary "..." --start ... --end ...`

### Reply to Important Emails
1. Find emails needing reply: `needs_reply.py`
2. Read specific email: `read_email.py <id>`
3. Create draft response: `create_draft.py --to ... --subject "Re: ..."`
