---
name: twenty
description: Open-source CRM API for managing people, companies, notes, tasks and custom objects
vm0_secrets:
  - TWENTY_API_KEY
vm0_vars:
  - TWENTY_API_URL
---

# Twenty CRM

Open-source modern CRM platform. Manage people, companies, opportunities, notes, and tasks via REST or GraphQL API.

> Official docs: https://docs.twenty.com/developers/api-and-webhooks/api

---

## When to Use

Use this skill when you need to:

- Manage contacts (people) and companies
- Track opportunities and deals
- Create notes and tasks
- Sync CRM data with other systems
- Query CRM metadata and custom fields
- Set up webhooks for CRM events

---

## Prerequisites

1. Create an account at https://app.twenty.com/
2. Go to **Settings → APIs & Webhooks** to generate an API key

Set environment variables:

```bash
# For Twenty Cloud
export TWENTY_API_KEY="your-api-key"
export TWENTY_API_URL="https://api.twenty.com"

# For self-hosted instances
export TWENTY_API_URL="https://your-domain.com"
```

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

### 1. List Companies

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/companies" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.companies[:3]'
```

**With pagination:**

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/companies?limit=10&offset=0" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.companies'
```

### 2. Create a Company

Write to `/tmp/twenty_request.json`:

```json
{
  "name": "Acme Corp",
  "domainName": "acme.com",
  "address": "123 Main St, San Francisco, CA"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${TWENTY_API_URL}/rest/companies" --header "Authorization: Bearer ${TWENTY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/twenty_request.json'
```

### 3. List People (Contacts)

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/people" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.people[:3]'
```

### 4. Create a Person

Write to `/tmp/twenty_request.json`:

```json
{
  "name": {
    "firstName": "John",
    "lastName": "Doe"
  },
  "email": "john@example.com",
  "phone": "+1234567890"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${TWENTY_API_URL}/rest/people" --header "Authorization: Bearer ${TWENTY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/twenty_request.json'
```

### 5. Get a Specific Record

> **Note:** Replace `{companyId}` and `{personId}` with actual IDs obtained from the "List Companies" or "List People" endpoints above (look for the `id` field in the response).

```bash
# Get company by ID
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/companies/{companyId}" --header "Authorization: Bearer ${TWENTY_API_KEY}"'

# Get person by ID
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/people/{personId}" --header "Authorization: Bearer ${TWENTY_API_KEY}"'
```

### 6. Update a Record

> **Note:** Replace `{companyId}` with an actual company ID from the "List Companies" endpoint above.

Write to `/tmp/twenty_request.json`:

```json
{
  "name": "Acme Corporation",
  "employees": 500
}
```

Then run:

```bash
bash -c 'curl -s -X PATCH "${TWENTY_API_URL}/rest/companies/{companyId}" --header "Authorization: Bearer ${TWENTY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/twenty_request.json'
```

### 7. Delete a Record

> **Note:** Replace `{companyId}` with an actual company ID from the "List Companies" endpoint above.

```bash
curl -s -X DELETE "${TWENTY_API_URL}/rest/companies/{companyId}" --header "Authorization: Bearer ${TWENTY_API_KEY}"
```

### 8. List Notes

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/notes" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.notes[:3]'
```

### 9. Create a Note

Write to `/tmp/twenty_request.json`:

```json
{
  "title": "Meeting Notes",
  "body": "Discussed Q1 roadmap and budget allocation."
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${TWENTY_API_URL}/rest/notes" --header "Authorization: Bearer ${TWENTY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/twenty_request.json'
```

### 10. List Tasks

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/tasks" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.tasks[:3]'
```

### 11. Create a Task

Write to `/tmp/twenty_request.json`:

```json
{
  "title": "Follow up with client",
  "dueAt": "2025-01-15T10:00:00Z",
  "status": "TODO"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${TWENTY_API_URL}/rest/tasks" --header "Authorization: Bearer ${TWENTY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/twenty_request.json'
```

### 12. Get Metadata (Object Schema)

List all object types and their fields:

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/metadata/objects" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.objects[] | {name: .nameSingular, fields: [.fields[].name]}'
```

**Get metadata for a specific object:**

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/metadata/objects/companies" --header "Authorization: Bearer ${TWENTY_API_KEY}"'
```

### 13. GraphQL Query

Write to `/tmp/twenty_request.json`:

```json
{
  "query": "query { companies(first: 5) { edges { node { id name domainName } } } }"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${TWENTY_API_URL}/graphql" --header "Authorization: Bearer ${TWENTY_API_KEY}" --header "Content-Type: application/json" -d @/tmp/twenty_request.json' | jq '.data.companies.edges'
```

---

## API Endpoints

| Category | Endpoint | Description |
|----------|----------|-------------|
| **Core Objects** | `/rest/companies` | Manage companies |
| | `/rest/people` | Manage contacts |
| | `/rest/opportunities` | Manage deals/opportunities |
| | `/rest/notes` | Manage notes |
| | `/rest/tasks` | Manage tasks |
| | `/rest/activities` | Activity timeline |
| **Metadata** | `/rest/metadata/objects` | List all object schemas |
| | `/rest/metadata/objects/{name}` | Get specific object schema |
| | `/rest/metadata/picklists` | Get dropdown field options |
| **GraphQL** | `/graphql` | GraphQL endpoint |

---

## Query Parameters

| Parameter | Description |
|-----------|-------------|
| `limit` | Number of records to return (default: 20) |
| `offset` | Number of records to skip |
| `filter` | Filter conditions (JSON) |
| `orderBy` | Sort order |

**Example with filters:**

```bash
bash -c 'curl -s -X GET "${TWENTY_API_URL}/rest/companies?filter={\"name\":{\"like\":\"%Acme%\"}}" --header "Authorization: Bearer ${TWENTY_API_KEY}"' | jq '.data.companies'
```

---

## Response Format

```json
{
  "data": {
  "companies": [
  {
  "id": "uuid",
  "name": "Company Name",
  "domainName": "example.com",
  "createdAt": "2025-01-01T00:00:00Z",
  "updatedAt": "2025-01-01T00:00:00Z"
  }
  ]
  },
  "pageInfo": {
  "hasNextPage": true,
  "endCursor": "cursor-string"
  }
}
```

---

## Guidelines

1. **API Playground**: Test API calls at Settings → APIs & Webhooks in the Twenty app
2. **Rate Limits**: Cloud has rate limits; self-hosted has no limits
3. **GraphQL**: Use GraphQL for complex queries with relationships
4. **REST**: Use REST for simple CRUD operations
5. **Custom Objects**: Twenty supports custom objects; use metadata API to discover schema
6. **Webhooks**: Set up webhooks at Settings → APIs & Webhooks for real-time events

---

## Resources

- **API Docs**: https://docs.twenty.com/developers/api-and-webhooks/api
- **Webhooks**: https://docs.twenty.com/developers/api-and-webhooks/webhooks
- **GitHub**: https://github.com/twentyhq/twenty
- **Discord**: https://discord.gg/cx5n4Jzs57
