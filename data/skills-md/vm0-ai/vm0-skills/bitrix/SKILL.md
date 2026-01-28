---
name: bitrix
description: Bitrix24 REST API via curl. Use this skill to manage CRM (leads, deals, contacts), tasks, and users.
vm0_secrets:
  - BITRIX_WEBHOOK_URL
---

# Bitrix24 API

Use the Bitrix24 REST API via direct `curl` calls to **manage CRM, tasks, and users** in your Bitrix24 workspace.

> Official docs: `https://apidocs.bitrix24.com/`

---

## When to Use

Use this skill when you need to:

- **Manage CRM leads** (create, update, list, delete)
- **Manage CRM deals** and sales funnels
- **Manage CRM contacts** and companies
- **Create and manage tasks**
- **Get user information**
- **Automate business workflows**

---

## Prerequisites

1. Log in to your [Bitrix24](https://www.bitrix24.com/) workspace
2. Go to Applications → Developer Resources → Ready-made scenarios → Other → Incoming webhook
3. Create a new webhook and select the required permissions (CRM, Tasks, Users)
4. Copy the webhook URL
5. Store it in the environment variable

```bash
export BITRIX_WEBHOOK_URL="https://your-domain.bitrix24.com/rest/1/your-secret-code"
```

### Webhook URL Format

```
https://[domain]/rest/[user-id]/[secret-code]/[method].json
```

- `domain`: Your Bitrix24 address
- `user-id`: Webhook creator's ID
- `secret-code`: Authentication token (keep secure)
- `method`: API method name

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"'
> ```

## How to Use

All examples assume `BITRIX_WEBHOOK_URL` is set to your webhook base URL.

---

### 1. Get Current User

Get information about the authenticated user:

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/user.current.json"'
```

**Response:**
```json
{
  "result": {
  "ID": "1",
  "NAME": "John",
  "LAST_NAME": "Doe",
  "EMAIL": "john@example.com"
  }
}
```

---

### 2. List Users

Get a list of users in the workspace:

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/user.get.json"' | jq '.result[] | {ID, NAME, LAST_NAME, EMAIL}'
```

---

## CRM - Leads

### 3. Create a Lead

Write to `/tmp/bitrix_request.json`:

```json
{
  "fields": {
    "TITLE": "New Lead from API",
    "NAME": "John",
    "LAST_NAME": "Doe",
    "PHONE": [{"VALUE": "+1234567890", "VALUE_TYPE": "WORK"}],
    "EMAIL": [{"VALUE": "john@example.com", "VALUE_TYPE": "WORK"}]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/crm.lead.add.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

**Response:**
```json
{
  "result": 123
}
```

---

### 4. Get a Lead

Replace `<your-lead-id>` with the actual lead ID:

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.lead.get.json?id=<your-lead-id>"'
```

---

### 5. List Leads

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.lead.list.json"' | jq '.result[] | {ID, TITLE, STATUS_ID}'
```

With filter:

Write to `/tmp/bitrix_request.json`:

```json
{
  "filter": {"STATUS_ID": "NEW"},
  "select": ["ID", "TITLE", "NAME", "PHONE"]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/crm.lead.list.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

---

### 6. Update a Lead

Write to `/tmp/bitrix_request.json`:

```json
{
  "id": 123,
  "fields": {
    "STATUS_ID": "IN_PROCESS",
    "COMMENTS": "Updated via API"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/crm.lead.update.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

---

### 7. Delete a Lead

Replace `<your-lead-id>` with the actual lead ID:

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.lead.delete.json?id=<your-lead-id>"'
```

---

## CRM - Contacts

### 8. Create a Contact

Write to `/tmp/bitrix_request.json`:

```json
{
  "fields": {
    "NAME": "Jane",
    "LAST_NAME": "Smith",
    "PHONE": [{"VALUE": "+1987654321", "VALUE_TYPE": "MOBILE"}],
    "EMAIL": [{"VALUE": "jane@example.com", "VALUE_TYPE": "WORK"}]
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/crm.contact.add.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

---

### 9. List Contacts

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.contact.list.json"' | jq '.result[] | {ID, NAME, LAST_NAME}'
```

---

## CRM - Deals

### 10. Create a Deal

Write to `/tmp/bitrix_request.json`:

```json
{
  "fields": {
    "TITLE": "New Deal from API",
    "STAGE_ID": "NEW",
    "OPPORTUNITY": 5000,
    "CURRENCY_ID": "USD"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/crm.deal.add.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

---

### 11. List Deals

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.deal.list.json"' | jq '.result[] | {ID, TITLE, STAGE_ID, OPPORTUNITY}'
```

---

### 12. Update Deal Stage

Write to `/tmp/bitrix_request.json`:

```json
{
  "id": 456,
  "fields": {
    "STAGE_ID": "WON"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/crm.deal.update.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

---

## Tasks

### 13. Create a Task

Write to `/tmp/bitrix_request.json`:

```json
{
  "fields": {
    "TITLE": "New Task from API",
    "DESCRIPTION": "Task description here",
    "RESPONSIBLE_ID": 1,
    "DEADLINE": "2025-12-31"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${BITRIX_WEBHOOK_URL}/tasks.task.add.json" --header "Content-Type: application/json" -d @/tmp/bitrix_request.json'
```

---

### 14. List Tasks

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/tasks.task.list.json"' | jq '.result.tasks[] | {id, title, status}'
```

---

### 15. Complete a Task

Replace `<your-task-id>` with the actual task ID:

```bash
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/tasks.task.complete.json?taskId=<your-task-id>"'
```

---

## Get Field Definitions

Get available fields for any entity:

```bash
# Lead fields
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.lead.fields.json"'

# Contact fields
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.contact.fields.json"'

# Deal fields
bash -c 'curl -s -X GET "${BITRIX_WEBHOOK_URL}/crm.deal.fields.json"'
```

---

## Common Parameters

| Parameter | Description |
|-----------|-------------|
| `filter` | Filter results (e.g., `{"STATUS_ID": "NEW"}`) |
| `select` | Fields to return (e.g., `["ID", "TITLE"]`) |
| `order` | Sort order (e.g., `{"ID": "DESC"}`) |
| `start` | Pagination offset |

---

## Guidelines

1. **Keep webhook secret**: Never expose your webhook URL publicly
2. **Use POST for complex queries**: Filters and field selections work better with POST
3. **Check field names**: Use `*.fields.json` methods to get valid field names
4. **Rate limits**: Bitrix24 has rate limits; add delays for bulk operations
5. **Pagination**: Results are paginated; use `start` parameter for large datasets
