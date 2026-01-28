---
name: m365-calendar
description: Read, create, and manage Microsoft 365 calendar events via Graph API. Supports meeting invitations with attendees and Teams meetings.
---

# Microsoft 365 Calendar

CLI tool for Microsoft 365 Calendar via Microsoft Graph API.

## Setup

Uses the same client/tenant from m365mail. Just authenticate with calendar scope:

```bash
# Authenticate (device code flow)
m365cal auth
```

If you haven't set up m365mail yet, do that first — the calendar tool shares its config.

### Required Permissions

In your Entra ID app, add these Graph permissions:
- `Calendars.ReadWrite` (delegated)

## Commands

### View Events

```bash
m365cal today                     # Today's events
m365cal tomorrow                  # Tomorrow's events
m365cal week                      # Next 7 days
m365cal range 2024-01-15          # Specific date
m365cal range 2024-01-15 2024-01-20  # Date range
m365cal show <event_id>           # Event details
```

### Create Events

```bash
# Simple event
m365cal create -s "Team standup" --start "2024-01-15 09:00" -d 30

# With location
m365cal create -s "Lunch" --start "2024-01-15 12:00" -d 60 -l "Cafe"

# With attendees (sends invitations automatically)
m365cal create -s "Project review" --start "2024-01-15 14:00" -d 60 \
  -a alice@company.com bob@company.com \
  -o carol@company.com

# Teams meeting with attendees
m365cal create -s "Sprint planning" --start "2024-01-15 10:00" -d 90 \
  -a team@company.com --teams

# All-day event
m365cal create -s "Conference" --start "2024-01-20" --all-day
```

### Update Events

```bash
m365cal update <event_id> --subject "New title"
m365cal update <event_id> --start "2024-01-15 15:00"
m365cal update <event_id> -l "Room 201"
```

Updates with attendees automatically send update notifications.

### Delete/Cancel Events

```bash
m365cal delete <event_id>                    # Silent delete
m365cal delete <event_id> -m "Rescheduling"  # Cancel with message to attendees
```

### Respond to Invitations

```bash
m365cal respond <event_id> accept
m365cal respond <event_id> tentative -m "Might be late"
m365cal respond <event_id> decline --silent  # Don't notify organizer
```

### List Calendars

```bash
m365cal calendars
m365cal calendars --json
```

## Options

- `-v, --verbose`: Show more details
- `--json`: Output as JSON (for scripting)
- `-d, --duration`: Duration in minutes (default: 60)
- `-a, --attendees`: Required attendees (emails)
- `-o, --optional`: Optional attendees
- `-t, --teams`: Create Teams meeting
- `-l, --location`: Location
- `-b, --body`: Description/notes

## Meeting Invitations

When you create or update an event with attendees, Microsoft Graph automatically:
1. Sends meeting invitations via email
2. Adds the event to attendees' calendars (pending acceptance)
3. Sends update/cancellation notices when changed

No need to use m365mail separately — invitations are built into the calendar API.

## Event IDs

Events are identified by long IDs. Commands accept:
- Full ID
- ID prefix (first 8+ chars usually unique)

## Token Storage

- Config (shared): `~/.m365mail/config.json`
- Calendar tokens: `~/.m365calendar/token_cache.json`

## Troubleshooting

**"No cached token"**: Run `m365cal auth`

**"Run m365mail setup first"**: Calendar shares credentials with mail. Set up mail first.

**Permission denied**: Ensure `Calendars.ReadWrite` permission is granted in Entra ID.
