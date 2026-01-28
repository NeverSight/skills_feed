---
name: google-calendar
description: Manage Google Calendar events and calendars. List, create, update, and delete events, check availability, and organize schedules. Use when working with Google Calendar management.
metadata:
  author: odyssey4me
  version: "0.1.0"
license: MIT
---

# Google Calendar

Interact with Google Calendar for event management, scheduling, and availability checking.

## Installation

1. **Install Python dependencies**:
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
   ```

2. **Download the skill** from [Releases](https://github.com/odyssey4me/agent-skills/releases) or use directly from this repository.

## Setup Verification

After installation, verify the skill is properly configured:

```bash
python scripts/google-calendar.py check
```

This will check:
- Python dependencies (google-auth, google-auth-oauthlib, google-api-python-client, keyring, pyyaml)
- Authentication configuration
- Connectivity to Google Calendar API

If anything is missing, the check command will provide setup instructions.

## Authentication

Google Calendar uses OAuth 2.0 for authentication. For complete setup instructions, see:

1. [GCP Project Setup Guide](../../docs/gcp-project-setup.md) - Create project, enable Calendar API
2. [Google OAuth Setup Guide](../../docs/google-oauth-setup.md) - Configure credentials

### Quick Start

1. Create `~/.config/agent-skills/google.yaml`:
   ```yaml
   oauth_client:
     client_id: your-client-id.apps.googleusercontent.com
     client_secret: your-client-secret
   ```

2. Run `python scripts/google-calendar.py check` to trigger OAuth flow and verify setup.

### OAuth Scopes

The skill requests granular scopes for different operations:

| Scope | Permission | Used For |
|-------|-----------|----------|
| `calendar.readonly` | Read calendars and events | list, get events |
| `calendar.events` | Create/edit/delete events | create, update, delete |

### Scope Errors

If you encounter "insufficient scope" errors, revoke your token and re-authenticate:

1. Revoke at https://myaccount.google.com/permissions
2. Clear token: `keyring del agent-skills google-calendar-token-json`
3. Re-run: `python scripts/google-calendar.py check`

## Commands

### check

Verify configuration and connectivity.

```bash
python scripts/google-calendar.py check
```

This validates:
- Python dependencies are installed
- Authentication is configured
- Can connect to Google Calendar API
- Displays your primary calendar information

### auth setup

Store OAuth 2.0 client credentials for custom OAuth flow.

```bash
python scripts/google-calendar.py auth setup \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

Credentials are saved to `~/.config/agent-skills/google-calendar.yaml`.

### calendars list

List all calendars for the authenticated user.

```bash
# List calendars
python scripts/google-calendar.py calendars list

# Output as JSON
python scripts/google-calendar.py calendars list --json
```

**Arguments:**
- `--json`: Output as JSON

### calendars get

Get details for a specific calendar.

```bash
# Get primary calendar
python scripts/google-calendar.py calendars get primary

# Get specific calendar by ID
python scripts/google-calendar.py calendars get CALENDAR_ID

# Output as JSON
python scripts/google-calendar.py calendars get primary --json
```

**Arguments:**
- `calendar_id`: Calendar ID or "primary" (required)
- `--json`: Output as JSON

### events list

List calendar events.

```bash
# List upcoming events
python scripts/google-calendar.py events list

# List events in specific time range
python scripts/google-calendar.py events list \
  --time-min "2026-01-24T00:00:00Z" \
  --time-max "2026-01-31T23:59:59Z"

# List events from specific calendar
python scripts/google-calendar.py events list --calendar CALENDAR_ID

# Search events
python scripts/google-calendar.py events list --query "meeting"

# List with custom max results
python scripts/google-calendar.py events list --max-results 20

# Output as JSON
python scripts/google-calendar.py events list --json
```

**Arguments:**
- `--calendar`: Calendar ID (default: "primary")
- `--time-min`: Start time (RFC3339 timestamp, e.g., "2026-01-24T00:00:00Z")
- `--time-max`: End time (RFC3339 timestamp)
- `--max-results`: Maximum number of results (default: 10)
- `--query`: Free text search query
- `--json`: Output as JSON

**Time Format Examples:**
- UTC: `2026-01-24T10:00:00Z`
- With timezone: `2026-01-24T10:00:00-05:00` (EST)
- Date only (all-day): `2026-01-24`

### events get

Get details for a specific event.

```bash
# Get event from primary calendar
python scripts/google-calendar.py events get EVENT_ID

# Get event from specific calendar
python scripts/google-calendar.py events get EVENT_ID --calendar CALENDAR_ID

# Output as JSON
python scripts/google-calendar.py events get EVENT_ID --json
```

**Arguments:**
- `event_id`: Event ID (required)
- `--calendar`: Calendar ID (default: "primary")
- `--json`: Output as JSON

### events create

Create a new calendar event.

```bash
# Create simple event with time
python scripts/google-calendar.py events create \
  --summary "Team Meeting" \
  --start "2026-01-24T10:00:00-05:00" \
  --end "2026-01-24T11:00:00-05:00"

# Create all-day event
python scripts/google-calendar.py events create \
  --summary "Conference" \
  --start "2026-01-24" \
  --end "2026-01-25" \
  --timezone "America/New_York"

# Create event with details
python scripts/google-calendar.py events create \
  --summary "Project Review" \
  --start "2026-01-24T14:00:00Z" \
  --end "2026-01-24T15:00:00Z" \
  --description "Quarterly project review meeting" \
  --location "Conference Room A" \
  --attendees "alice@example.com,bob@example.com"

# Create on specific calendar
python scripts/google-calendar.py events create \
  --calendar CALENDAR_ID \
  --summary "Event" \
  --start "2026-01-24T10:00:00Z" \
  --end "2026-01-24T11:00:00Z"

# Output as JSON
python scripts/google-calendar.py events create \
  --summary "Meeting" \
  --start "2026-01-24T10:00:00Z" \
  --end "2026-01-24T11:00:00Z" \
  --json
```

**Arguments:**
- `--summary`: Event title (required)
- `--start`: Start time - RFC3339 timestamp or YYYY-MM-DD for all-day (required)
- `--end`: End time - RFC3339 timestamp or YYYY-MM-DD for all-day (required)
- `--calendar`: Calendar ID (default: "primary")
- `--description`: Event description
- `--location`: Event location
- `--attendees`: Comma-separated list of attendee email addresses
- `--timezone`: Timezone for all-day events (e.g., "America/New_York")
- `--json`: Output as JSON

### events update

Update an existing event.

```bash
# Update event summary
python scripts/google-calendar.py events update EVENT_ID \
  --summary "Updated Meeting Title"

# Update event time
python scripts/google-calendar.py events update EVENT_ID \
  --start "2026-01-24T15:00:00Z" \
  --end "2026-01-24T16:00:00Z"

# Update multiple fields
python scripts/google-calendar.py events update EVENT_ID \
  --summary "Project Sync" \
  --location "Room B" \
  --description "Updated agenda"

# Update event on specific calendar
python scripts/google-calendar.py events update EVENT_ID \
  --calendar CALENDAR_ID \
  --summary "New Title"

# Output as JSON
python scripts/google-calendar.py events update EVENT_ID \
  --summary "Meeting" \
  --json
```

**Arguments:**
- `event_id`: Event ID (required)
- `--calendar`: Calendar ID (default: "primary")
- `--summary`: New event title
- `--start`: New start time (RFC3339 or YYYY-MM-DD)
- `--end`: New end time (RFC3339 or YYYY-MM-DD)
- `--description`: New description
- `--location`: New location
- `--json`: Output as JSON

### events delete

Delete a calendar event.

```bash
# Delete event from primary calendar
python scripts/google-calendar.py events delete EVENT_ID

# Delete event from specific calendar
python scripts/google-calendar.py events delete EVENT_ID --calendar CALENDAR_ID
```

**Arguments:**
- `event_id`: Event ID (required)
- `--calendar`: Calendar ID (default: "primary")
- `--json`: Output as JSON (for consistency, no output on success)

### freebusy

Check free/busy information for calendars.

```bash
# Check availability for primary calendar
python scripts/google-calendar.py freebusy \
  --start "2026-01-24T00:00:00Z" \
  --end "2026-01-25T00:00:00Z"

# Check multiple calendars
python scripts/google-calendar.py freebusy \
  --start "2026-01-24T08:00:00Z" \
  --end "2026-01-24T17:00:00Z" \
  --calendars "primary,calendar1@example.com,calendar2@example.com"

# Output as JSON
python scripts/google-calendar.py freebusy \
  --start "2026-01-24T00:00:00Z" \
  --end "2026-01-25T00:00:00Z" \
  --json
```

**Arguments:**
- `--start`: Start time (RFC3339 timestamp, required)
- `--end`: End time (RFC3339 timestamp, required)
- `--calendars`: Comma-separated calendar IDs (default: "primary")
- `--json`: Output as JSON

## Examples

### Verify Setup

```bash
python scripts/google-calendar.py check
```

### View upcoming events

```bash
# Next 10 events
python scripts/google-calendar.py events list

# This week's events
python scripts/google-calendar.py events list \
  --time-min "2026-01-24T00:00:00Z" \
  --time-max "2026-01-31T23:59:59Z"
```

### Create a meeting

```bash
python scripts/google-calendar.py events create \
  --summary "Team Standup" \
  --start "2026-01-25T09:00:00-05:00" \
  --end "2026-01-25T09:30:00-05:00" \
  --location "Zoom" \
  --attendees "team@example.com"
```

### Schedule an all-day event

```bash
python scripts/google-calendar.py events create \
  --summary "Company Holiday" \
  --start "2026-12-25" \
  --end "2026-12-26" \
  --timezone "America/New_York"
```

### Reschedule an event

```bash
python scripts/google-calendar.py events update EVENT_ID \
  --start "2026-01-24T14:00:00Z" \
  --end "2026-01-24T15:00:00Z"
```

### Find available time slots

```bash
python scripts/google-calendar.py freebusy \
  --start "2026-01-24T08:00:00-05:00" \
  --end "2026-01-24T17:00:00-05:00" \
  --calendars "primary,colleague@example.com"
```

### Search for events

```bash
python scripts/google-calendar.py events list --query "project review"
```

### Cancel an event

```bash
python scripts/google-calendar.py events delete EVENT_ID
```

## Date and Time Format

Google Calendar uses RFC3339 format for timestamps. See [calendar-timezones.md](references/calendar-timezones.md) for detailed timezone handling.

### Timed Events

Use RFC3339 format with timezone:

```
2026-01-24T10:00:00-05:00  # 10 AM EST
2026-01-24T10:00:00Z       # 10 AM UTC
2026-01-24T10:00:00+01:00  # 10 AM CET
```

### All-Day Events

Use date format (YYYY-MM-DD):

```
2026-01-24  # All day on January 24, 2026
```

For all-day events, you can specify a timezone using the `--timezone` argument.

## Troubleshooting

### Check command fails

Run `python scripts/google-calendar.py check` to diagnose issues. It will provide specific error messages and setup instructions.

### Authentication failed

1. Verify your OAuth client ID and client secret are correct in `~/.config/agent-skills/google.yaml`
2. Token expired or corrupted - clear and re-authenticate:
   ```bash
   keyring del agent-skills google-calendar-token-json
   python scripts/google-calendar.py check
   ```

### Permission denied

Your OAuth token may not have the necessary scopes. Revoke access at https://myaccount.google.com/permissions, clear your token, and re-authenticate.

### Import errors

Ensure dependencies are installed:
```bash
pip install --user google-auth google-auth-oauthlib google-api-python-client keyring pyyaml
```

### Event not found

Verify the event ID and calendar ID are correct. Event IDs are unique per calendar.

### Timezone issues

Always use RFC3339 format with explicit timezone offsets, or UTC (Z suffix). For all-day events, use YYYY-MM-DD format and optionally specify `--timezone`.

### Rate limiting

Google Calendar API has quota limits. If you hit rate limits, wait a few minutes before retrying. For high-volume usage, consider requesting quota increases in the Google Cloud Console.

## API Scopes

This skill requests the following OAuth scopes:

- `https://www.googleapis.com/auth/calendar.readonly` - Read calendar events and settings
- `https://www.googleapis.com/auth/calendar.events` - Create, update, and delete events

These scopes provide full calendar management capabilities while following the principle of least privilege.

## Security Notes

- **OAuth tokens** are stored securely in your system keyring
- **Client secrets** are stored in `~/.config/agent-skills/google-calendar.yaml` with file permissions 600
- **No passwords** are stored - only OAuth tokens
- **Tokens refresh automatically** when using the skill
- **Browser-based consent** ensures you approve all requested permissions

Always review OAuth consent screens before granting access to your Google Calendar.
