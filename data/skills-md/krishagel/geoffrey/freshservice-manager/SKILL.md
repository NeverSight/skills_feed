---
name: freshservice-manager
description: Manage Freshservice tickets, approvals, and get team performance reports across all workspaces
triggers:
  - "freshservice"
  - "ticket"
  - "helpdesk"
  - "what happened in freshservice"
  - "tech team metrics"
  - "daily summary"
  - "weekly summary"
  - "approvals"
  - "assign to"
  - "add note to ticket"
  - "close ticket"
allowed-tools: Read, Bash
version: 0.1.0
---

# Freshservice Manager Skill

## Configuration

- **Domain**: psd401.freshservice.com
- **Agent ID**: 6000130414 (Kris Hagel)
- **Primary Workspace**: 2 (Technology)
- **API Key**: Stored in `~/Library/Mobile Documents/com~apple~CloudDocs/Geoffrey/secrets/.env`

## Workspaces

| ID | Name |
|----|------|
| 2 | Technology (primary) |
| 3 | Employee Support Services |
| 4 | Business Services |
| 5 | Teaching & Learning |
| 6 | Maintenance |
| 8 | Investigations |
| 9 | Transportation |
| 10 | Safety & Security |
| 11 | Communications |
| 13 | Software Development |

## Team Context

- **TSD Generic Account** (6000875582) - Shared by high school interns for Chromebook repairs
- **David Edwards** - Desktop Support Tech, handles most varied workload including incidents
- **Carol Winget** - Student Database Admin, PowerSchool specialist
- **Laura Durkin** - Admin Secretary, handles new students and badges

## Reports & Summaries

### Daily Summary
Get a narrative summary of what happened in Technology on a specific day.

**Natural language triggers:**
- "What happened in Freshservice yesterday?"
- "Give me today's tech summary"
- "What did the team do on Wednesday?"

**Script:** `bun get_daily_summary.js [date]`

Date options:
- `today` (default)
- `yesterday`
- Day names: `monday`, `tuesday`, `wednesday`, etc.
- `last wednesday`, `last friday`
- Specific date: `2025-11-20`

**Output includes:**
- Total tickets closed
- Breakdown by category (Chromebook, Schoology, Security Alert, etc.)
- Breakdown by agent with their tickets
- Automated ticket count (password resets)

### Weekly Summary
Get trends and metrics for the entire week.

**Natural language triggers:**
- "Weekly tech summary"
- "How did the team do this week?"
- "Give me the weekly Freshservice report"

**Script:** `bun get_weekly_summary.js [weeks_ago]`

Options:
- `0` = this week (default)
- `1` = last week
- `2` = two weeks ago

**Output includes:**
- Total closed and daily average
- Peak day and slow day
- Daily trend by volume
- Category breakdown with percentages
- Category trends (which days had spikes)
- Top agents with ticket counts and focus areas
- Agent daily breakdown

### Narrative Style

When presenting summaries, write a 1-minute narrative that:
- Highlights the main story of the day/week (outages, big pushes, etc.)
- Calls out specific people and what they handled
- Notes any concerning patterns (security alerts, cut wires, etc.)
- Converts UTC timestamps to Pacific time
- Uses specific numbers and ticket counts

## Ticket Operations

### List Tickets
```bash
bun list_tickets.js '{"workspace_id": 2, "filter": "new_and_my_open"}'
```

Filters: `new_and_my_open`, `watching`, `spam`, `deleted`, `archived`

### Search Tickets
```bash
bun search_tickets.js "status:2 AND priority:3" 2
```

Query syntax: `field:value AND/OR field:value`
Fields: `status`, `priority`, `agent_id`, `group_id`, `created_at`, `updated_at`

### Get Ticket Details
```bash
bun get_ticket.js <ticket_id>
```

### Get Service Request (with form data)
```bash
bun get_service_request.js <ticket_id>
```

Includes requester info, custom form fields, requested items.

### Create Ticket
```bash
bun create_ticket.js '<json>'
```

Required: `subject`, `description`, `email` or `requester_id`
Optional: `priority`, `status`, `workspace_id`

### Update Ticket
```bash
bun update_ticket.js <ticket_id> '<json>'
```

Can update: `status`, `priority`, `responder_id`, `group_id`

### Add Note
```bash
bun add_note.js <ticket_id> '{"body": "Note text", "private": true}'
```

Optional: `notify_emails` array to alert specific agents.

## Agent Operations

### List Agents
```bash
bun list_agents.js [query]
```

Query filters by first name, last name, or email.
Returns: id, name, email, job_title

Use this to resolve "assign to Mark" → find Mark's agent ID → update ticket.

### Get Agent by Email
```bash
bun get_agent.js <email>
```

## Approvals

### Get Pending Approvals
```bash
bun get_approvals.js [status]
```

Status: `requested` (default), `approved`, `rejected`, `cancelled`

**Note:** Freshservice API does not support approving service requests programmatically. User must approve via:
- Web UI: `https://psd401.freshservice.com/helpdesk/tickets/<id>`
- Email reply to approval request

## Common Workflows

### "Add a note to Jodi on ticket 151501"
1. Find Jodi's agent ID: `bun list_agents.js jodi` → 6000542935
2. Add note: `bun add_note.js 151501 '{"body": "...", "notify_emails": ["miloj@psd401.net"]}'`

### "Assign ticket to Mark"
1. Find Mark's ID: `bun list_agents.js mark`
2. Update ticket: `bun update_ticket.js <id> '{"responder_id": <mark_id>}'`

### "What approvals do I have?"
1. Get approvals: `bun get_approvals.js`
2. For each approval, get details: `bun get_service_request.js <ticket_id>`

### Cross-skill workflow
"Add note to ticket, create OmniFocus task, reassign ticket" - can combine Freshservice note + OmniFocus task creation + ticket update in one flow.

## Category Detection

Tickets are auto-categorized by subject keywords:
- **Password Reset**: "password reset"
- **Security Alert**: "security alert", "compromised", "breach"
- **Schoology**: "schoology"
- **PowerSchool**: "powerschool"
- **Promethean Board**: "promethean"
- **Chromebook**: "chromebook"
- **Phone/Voicemail**: "phone", "voicemail", "ext."
- **Badge Request**: "badge"
- **New Student**: "new student", "enrollee"
- **Intercom**: "intercom"
- **Raptor**: "raptor"
- **GoGuardian**: "goguardian", "go guardian"
- **Access/Login**: "login", "access", "mfa"

## Status Codes

| Code | Status |
|------|--------|
| 2 | Open |
| 3 | Pending |
| 4 | Resolved |
| 5 | Closed |

## Priority Codes

| Code | Priority |
|------|----------|
| 1 | Low |
| 2 | Medium |
| 3 | High |
| 4 | Urgent |
