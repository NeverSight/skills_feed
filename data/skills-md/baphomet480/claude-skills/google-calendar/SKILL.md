---
name: google-calendar
description: Full CRUD Google Calendar interactions — list, get, search, create, update, delete events, list calendars, and quick-add.
---

# Google Calendar Skill

Full CRUD Calendar management for AI agents. List, create, update, delete, search events, and manage multiple calendars.

## Features

- **List**: See upcoming events with optional time range and text filtering.
- **Get**: Fetch a single event by ID with full details.
- **Search**: Free-text search across events.
- **Create**: Schedule events with attendees, location, timezone, and all-day support.
- **Update**: Patch existing events (only provided fields change).
- **Delete**: Remove events.
- **Quick Add**: Create events from natural language (e.g. "Lunch with Yoda tomorrow noon").
- **Calendars**: List all available calendars.

## Prerequisites

1.  **Google Cloud Project** with **Google Calendar API** enabled.
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
      --scopes https://www.googleapis.com/auth/calendar,https://www.googleapis.com/auth/cloud-platform
    ```

    Then verify:

    ```bash
    uv run skills/google-calendar/scripts/google_calendar.py verify
    ```

2.  **Alternative (credentials.json)**:
    - Place `credentials.json` in `~/.calendar_credentials/`.
    - Run `uv run skills/google-calendar/scripts/google_calendar.py setup`

## Usage

### List Upcoming Events

```bash
# Next 5 events
uv run skills/google-calendar/scripts/google_calendar.py list --limit 5

# Events this week
uv run skills/google-calendar/scripts/google_calendar.py list \
  --after "2026-02-16T00:00:00Z" \
  --before "2026-02-22T23:59:59Z"

# Events matching text
uv run skills/google-calendar/scripts/google_calendar.py list --query "Council"
```

### Get a Single Event

```bash
uv run skills/google-calendar/scripts/google_calendar.py get --id "abc123"
```

### Search Events

```bash
uv run skills/google-calendar/scripts/google_calendar.py search --query "Training" --limit 5
```

### Create an Event

```bash
# Timed event
uv run skills/google-calendar/scripts/google_calendar.py create \
  --summary "Jedi Council Meeting" \
  --start "2026-05-04T10:00:00" \
  --end "2026-05-04T11:00:00" \
  --description "Discussing the prophecy." \
  --location "Council Chamber, Coruscant" \
  --attendees yoda@dagobah.net mace@jedi.org

# All-day event
uv run skills/google-calendar/scripts/google_calendar.py create \
  --summary "May the 4th Celebration" \
  --start "2026-05-04" \
  --end "2026-05-05" \
  --all-day
```

### Update an Event

Only provided fields change (patch semantics):

```bash
uv run skills/google-calendar/scripts/google_calendar.py update \
  --id "abc123" \
  --summary "Updated: Jedi Council Meeting" \
  --start "2026-05-04T14:00:00" \
  --end "2026-05-04T15:00:00"
```

### Delete an Event

```bash
uv run skills/google-calendar/scripts/google_calendar.py delete --id "abc123"
```

### Quick Add (Natural Language)

```bash
uv run skills/google-calendar/scripts/google_calendar.py quick \
  --text "Lunch with Padmé tomorrow at noon at Dex's Diner"
```

### List All Calendars

```bash
uv run skills/google-calendar/scripts/google_calendar.py calendars
```

## JSON Output

**Event:**

```json
{
  "id": "abc123",
  "summary": "Jedi Council Meeting",
  "description": "Discussing the prophecy.",
  "location": "Council Chamber, Coruscant",
  "start": {
    "dateTime": "2026-05-04T10:00:00-07:00",
    "timeZone": "America/Phoenix"
  },
  "end": {
    "dateTime": "2026-05-04T11:00:00-07:00",
    "timeZone": "America/Phoenix"
  },
  "status": "confirmed",
  "attendees": [
    { "email": "yoda@dagobah.net", "responseStatus": "needsAction" }
  ],
  "htmlLink": "https://calendar.google.com/..."
}
```
