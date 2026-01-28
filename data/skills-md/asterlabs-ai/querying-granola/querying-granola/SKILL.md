---
name: querying-granola
description: Queries local Granola meeting cache for meeting history, context, and attendee information. Use when preparing for meetings, researching past interactions with a person or company, finding past discussions on a topic, tracking engagement, or when user mentions Granola, meeting notes, meeting history, or attendees.
---

# Querying Granola

Query the local Granola meeting cache. Requires Python 3.

**Note**: This reads from an unofficial local cache file, not a Granola API. The cache format could change with Granola updates.

**Run this script** to query meetings:

```bash
python3 skills/querying-granola/scripts/granola.py <command> [args]
```

Do not read the script source; execute it with the commands below.

## Primary Commands (search by title/notes/attendee names)

| Command | Purpose |
|---------|---------|
| `client <name>` | Get meetings matching name in title, notes, or attendee names/emails |
| `search <query>` | Search by keyword in title, notes, or attendees |
| `context <title>` | Get full notes + transcript for a specific meeting |

## Domain-Based Commands (require @domain.com in attendee list)

| Command | Purpose |
|---------|---------|
| `profile <domain>` | Company/org profile with contacts and meeting history |
| `active [N]` | Most active domains in last N days (default 30) |
| `stale [N]` | Domains with no meetings in N+ days (default 60) |
| `domains` | Meeting counts by email domain |

## Other Commands

| Command | Purpose |
|---------|---------|
| `timeline <query>` | Meeting frequency over time (visual bar chart) |
| `recent [N]` | List N most recent meetings (default 20) |
| `people` | Meeting counts by person |

## Workflows

### Before a meeting

```
Progress:
- [ ] Run profile for company/person context
- [ ] Run search for recent meeting history
- [ ] Identify key topics and contacts
- [ ] Check for unresolved action items
```

1. `profile domain.com` → contacts, meeting count, recent notes
2. `search "PersonName"` or `client "CompanyName"` → recent meeting notes
3. Review for action items, open questions

### Engagement tracking

```
Progress:
- [ ] Check active domains for recent engagement
- [ ] Check stale domains for follow-up opportunities
- [ ] Review timeline for engagement patterns
```

1. `active 30` → who you've been meeting with recently
2. `stale 60` → contacts you haven't met with in a while
3. `timeline "name"` → meeting frequency over time

## Output Examples

**profile** returns: meeting count, date range, contacts with meeting counts, recent meeting previews.

**timeline** returns: monthly bar chart showing meeting frequency with sample titles.

**active/stale** returns: domain, meeting count, top contacts.

## Data Sources

The script extracts from multiple cache sections:

| Source | Contains |
|--------|----------|
| `documents` | Meeting title, date, user-typed notes, basic attendees |
| `documentPanels` | AI-generated summaries (comprehensive meeting notes) |
| `meetingsMetadata` | Enriched attendee info with company names |
| `transcripts` | Raw meeting transcripts (~8 recent meetings cached locally) |

**Notes priority**: AI summaries are preferred over user-typed notes when available (more comprehensive).

**Company names**: Displayed as `Name <email> @ Company` when enriched data exists.

**Transcripts**: Only available for recent meetings; displayed in `context` command when present.

## Limitations

**Domain-based commands** (`active`, `stale`, `profile`) only work when attendee emails are captured in the meeting invite. If you join someone else's meeting link (their Zoom/Meet), their email may not be in your attendee list. Use `search` or `client` by name/title for these cases.

**Transcripts** are only cached locally for recent meetings (~8). Older meetings won't have transcript data available.
