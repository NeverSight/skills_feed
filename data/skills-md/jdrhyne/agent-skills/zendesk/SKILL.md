---
name: zendesk
description: Zendesk Support API for searching tickets, organizations, and users. Use when working with support tickets, customer issues, or correlating support data with Salesforce accounts.
---

# Zendesk

Access Zendesk support data — tickets, organizations, users, and search.

## Setup

Store credentials in `~/.config/zendesk/credentials.json`:
```json
{
  "subdomain": "your-subdomain",
  "email": "you@company.com",
  "api_token": "YOUR_API_TOKEN"
}
```

Get your API token from: Zendesk Admin → Apps & Integrations → APIs → Zendesk API → Add API Token.

## Authentication

```bash
ZD_CREDS=~/.config/zendesk/credentials.json
ZD_SUBDOMAIN=$(jq -r '.subdomain' $ZD_CREDS)
ZD_EMAIL=$(jq -r '.email' $ZD_CREDS)
ZD_TOKEN=$(jq -r '.api_token' $ZD_CREDS)
ZD_AUTH="$ZD_EMAIL/token:$ZD_TOKEN"
ZD_BASE="https://$ZD_SUBDOMAIN.zendesk.com/api/v2"

curl -s -u "$ZD_AUTH" "$ZD_BASE/tickets.json?per_page=1"
```

## Core Operations

### List Recent Tickets
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/tickets.json?sort_by=created_at&sort_order=desc&per_page=25" | \
  jq '[.tickets[] | {id, subject, status, priority, created: .created_at, updated: .updated_at, org_id: .organization_id}]'
```

### Get Ticket Details
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/tickets/TICKET_ID.json" | jq '.ticket'
```

### Get Ticket Comments (Full Thread)
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/tickets/TICKET_ID/comments.json" | \
  jq '[.comments[] | {author_id, body: .body[0:500], created: .created_at, public}]'
```

### Search Tickets
```bash
# By status
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+status:open" | jq '.results'

# By organization name
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+organization:\"Acme Corp\"" | jq '.results'

# By subject keyword
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+subject:billing" | jq '.results'

# By date range
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+created>2025-01-01" | jq '.results'

# Combined
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+status:open+priority:high" | jq '.results'
```

### List Organizations
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/organizations.json?per_page=100" | \
  jq '[.organizations[] | {id, name, domain_names, created: .created_at}]'
```

### Search Organizations by Name
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/organizations/autocomplete.json?name=Acme" | jq '.organizations'
```

### Get Organization Details
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/organizations/ORG_ID.json" | jq '.organization'
```

### Get Tickets by Organization
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/organizations/ORG_ID/tickets.json" | \
  jq '[.tickets[] | {id, subject, status, priority, created: .created_at}]'
```

### List Users
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/users.json?per_page=100" | \
  jq '[.users[] | {id, name, email, role, organization_id}]'
```

### Search Users by Email
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/users/search.json?query=user@example.com" | jq '.users'
```

### Get User's Tickets
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/users/USER_ID/tickets/requested.json" | jq '.tickets'
```

## Ticket Statistics

### Open Tickets by Priority
```bash
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+status<solved" | \
  jq 'group_by(.priority) | map({priority: .[0].priority, count: length})'
```

### Tickets Created Today
```bash
TODAY=$(date +%Y-%m-%d)
curl -s -u "$ZD_AUTH" "$ZD_BASE/search.json?query=type:ticket+created>=$TODAY" | \
  jq '{count: .count, tickets: [.results[] | {id, subject, status, requester_id}]}'
```

## Correlating with Salesforce

To match Zendesk organizations to Salesforce accounts:

1. **By domain**: Match Zendesk org `domain_names` to Salesforce Account `Website`
2. **By name**: Match Zendesk org `name` to Salesforce Account `Name`
3. **By email domain**: Extract domain from ticket requester email

### Find Zendesk Org for Salesforce Account
```bash
ACCOUNT_NAME="Acme Corp"
curl -s -u "$ZD_AUTH" "$ZD_BASE/organizations/autocomplete.json?name=$(echo $ACCOUNT_NAME | jq -sRr @uri)" | jq '.organizations'
```

## Endpoints Reference

| Endpoint | Method | Use |
|----------|--------|-----|
| `/tickets.json` | GET | List tickets |
| `/tickets/{id}.json` | GET | Get ticket details |
| `/tickets/{id}/comments.json` | GET | Get ticket comments |
| `/search.json?query=` | GET | Search (tickets, users, orgs) |
| `/organizations.json` | GET | List organizations |
| `/organizations/{id}.json` | GET | Get org details |
| `/organizations/{id}/tickets.json` | GET | Get org's tickets |
| `/organizations/autocomplete.json?name=` | GET | Search orgs by name |
| `/users.json` | GET | List users |
| `/users/search.json?query=` | GET | Search users |
| `/users/{id}/tickets/requested.json` | GET | Get user's tickets |

## Pagination

Responses include pagination info:
```json
{
  "tickets": [...],
  "next_page": "https://...",
  "previous_page": null,
  "count": 4294
}
```

Use `page` parameter or follow `next_page` URL.

## Rate Limits

- 700 requests per minute (admin)
- 400 requests per minute (agents)
- Check `X-Rate-Limit-Remaining` header

## Search Query Syntax

| Operator | Example | Description |
|----------|---------|-------------|
| `:` | `status:open` | Exact match |
| `>` `<` `>=` `<=` | `created>2025-01-01` | Date/number comparison |
| `*` | `subject:billing*` | Wildcard |
| `""` | `"exact phrase"` | Phrase match |
| `-` | `-status:closed` | Negation |
| `type:` | `type:ticket` | Filter by type |

## Notes

- Your subdomain is the `xxx` in `xxx.zendesk.com`
- Organizations map roughly to Salesforce Accounts
- Users can be end-users (customers) or agents (staff)
- Ticket statuses: new, open, pending, hold, solved, closed
