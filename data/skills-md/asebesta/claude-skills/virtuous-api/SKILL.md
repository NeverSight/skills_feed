---
name: virtuous-api
description: Virtuous CRM API integration reference for building donor management features. Use when writing code that interacts with the Virtuous API, including fetchers, normalizers, or any backend integration with Virtuous donor data. Covers Contacts, Individuals, Gifts, Projects, Campaigns, Events, Grants, Tasks, and Webhooks.
---

# Virtuous API

Reference for integrating with the Virtuous CRM REST API.

## Base URL

```
https://api.virtuoussoftware.com
```

## Authentication

Two methods available:

**API Keys (recommended for integrations):**
```
Authorization: Bearer <api-key>
```
Keys created in Virtuous UI, last 15 years.

**OAuth Tokens (for user-based interactions):**
```bash
curl -d "grant_type=password&username=EMAIL&password=PASSWORD" -X POST https://api.virtuoussoftware.com/Token
```
Tokens last 15 days, refresh tokens last 365 days.

## Rate Limits

- **1,500 requests/hour**
- Response headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## API Categories

| Category | Description |
|----------|-------------|
| Account/Permissions | Auth tokens, organizations, permissions |
| Contacts/Individuals | Donor records, addresses, methods, notes, tags, relationships |
| Giving | Gifts, designations, asks, pledges, recurring gifts, premiums |
| Campaigns | Campaigns, communications, segments |
| Projects | Project management, expenses, notes, roles |
| Events | Event management, attendees |
| Grants | Grant tracking and queries |
| Tasks | Task creation and queries |
| Webhooks | Event subscriptions |

## Key Endpoints

### Contacts
```
GET    /api/Contact/:contactId           # Get single contact
POST   /api/Contact/Query                # Query contacts (bulk)
POST   /api/Contact/Transaction          # Import contact (recommended)
```

### Gifts
```
GET    /api/Gift/:giftId                 # Get single gift
POST   /api/Gift/Query                   # Query gifts (bulk)
POST   /api/Gift/Transaction             # Import gift (recommended)
GET    /api/Gift/ByContact/:contactId    # Gifts for contact
```

### Recurring Gifts
```
GET    /api/RecurringGift/:id
POST   /api/RecurringGift/Query
GET    /api/RecurringGift/ByContact/:contactId
```

### Projects
```
GET    /api/Project/:projectId
POST   /api/Project/Query
```

### Tasks
```
POST   /api/Task                         # Create task
POST   /api/Task/Query                   # Query tasks
GET    /api/Task/Types                   # Get task types
```

## Best Practices

1. **Use Transaction Endpoints** for Gifts and Contacts to avoid duplicates
2. **Use Webhooks** instead of polling for updates
3. **Use Bulk Endpoints** (Query) when fetching multiple records
4. **Check Response Messages** on non-200 status codes

## Full API Reference

For complete endpoint specifications, request/response schemas, and examples, search the Postman collection (do not read the full file):

```
references/Virtuous.postman_collection.json
```

Search patterns (use grep):
- Endpoint by name: `grep '"name":.*Gift'`
- HTTP method: `grep '"method": "POST"'`
- URL paths: `grep '"path":'`
- Response examples: `grep '"body":'`

## Disclaimer

This skill is not affiliated with, endorsed by, or sponsored by Virtuous. It references publicly available API documentation for educational and integration purposes. The information may be outdated or incomplete. Always refer to the official Virtuous documentation for the most current API specifications.
