---
name: chatwoot
description: Chatwoot customer support API via curl. Use this skill to manage contacts, conversations, and messages for multi-channel customer support.
vm0_secrets:
  - CHATWOOT_API_TOKEN
vm0_vars:
  - CHATWOOT_ACCOUNT_ID
  - CHATWOOT_BASE_URL
---

# Chatwoot

Use Chatwoot via direct `curl` calls to **manage customer support** across multiple channels (website, email, WhatsApp, etc.).

> Official docs: `https://developers.chatwoot.com/api-reference/introduction`

---

## When to Use

Use this skill when you need to:

- **Manage contacts** - create, search, and update customer profiles
- **Handle conversations** - create, assign, and track support conversations
- **Send messages** - reply to customers or add internal notes
- **List agents** - get support team information
- **Automate workflows** - integrate with CRM, ticketing, or notification systems

---

## Prerequisites

1. Set up Chatwoot (Cloud or Self-hosted)
2. Log in and go to **Profile Settings** to get your API access token
3. Note your Account ID from the URL (e.g., `/app/accounts/1/...`)

```bash
export CHATWOOT_API_TOKEN="your-api-access-token"
export CHATWOOT_ACCOUNT_ID="1"
export CHATWOOT_BASE_URL="https://app.chatwoot.com" # or your self-hosted URL
```

### API Types

| API Type | Auth | Use Case |
|----------|------|----------|
| Application API | User access_token | Agent/admin automation |
| Client API | inbox_identifier | Custom chat interfaces |
| Platform API | Platform App token | Multi-tenant management (self-hosted only) |

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

All examples use the **Application API** with user access token.

---

### 1. Create a Contact

Create a new contact in your account:

Write to `/tmp/chatwoot_request.json`:

```json
{
  "inbox_id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone_number": "+1234567890",
  "identifier": "customer_123",
  "additional_attributes": {
    "company": "Acme Inc",
    "plan": "premium"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/contacts" -H "api_access_token: ${CHATWOOT_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/chatwoot_request.json'
```

---

### 2. Search Contacts

Search contacts by email, phone, or name:

```bash
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/contacts/search?q=john@example.com" -H "api_access_token: ${CHATWOOT_API_TOKEN}"' | jq '.payload[] | {id, name, email}'
```

---

### 3. Get Contact Details

Get a specific contact by ID. Replace `<contact-id>` with the actual contact ID from the "Search Contacts" or "Create a Contact" response:

```bash
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/contacts/<contact-id>" -H "api_access_token: ${CHATWOOT_API_TOKEN}"'
```

---

### 4. Create a Conversation

Create a new conversation with a contact:

Write to `/tmp/chatwoot_request.json`:

```json
{
  "source_id": "api_conversation_123",
  "inbox_id": 1,
  "contact_id": 123,
  "status": "open",
  "message": {
    "content": "Hello! How can I help you today?"
  }
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations" -H "api_access_token: ${CHATWOOT_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/chatwoot_request.json'
```

---

### 5. List Conversations

Get all conversations with optional filters:

```bash
# List open conversations
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations?status=open" -H "api_access_token: ${CHATWOOT_API_TOKEN}"' | jq '.data.payload[] | {id, status, contact: .meta.sender.name}'
```

---

### 6. Get Conversation Details

Get details of a specific conversation. Replace `<conversation-id>` with the actual conversation ID from the "List Conversations" or "Create a Conversation" response:

```bash
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations/<conversation-id>" -H "api_access_token: ${CHATWOOT_API_TOKEN}"'
```

---

### 7. Send a Message

Send a message in a conversation. Replace `<conversation-id>` with the actual conversation ID from the "List Conversations" response:

Write to `/tmp/chatwoot_request.json`:

```json
{
  "content": "Thank you for contacting us! Let me help you with that.",
  "message_type": "outgoing",
  "private": false
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations/<conversation-id>/messages" -H "api_access_token: ${CHATWOOT_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/chatwoot_request.json'
```

---

### 8. Add Private Note

Add an internal note (not visible to customer). Replace `<conversation-id>` with the actual conversation ID from the "List Conversations" response:

Write to `/tmp/chatwoot_request.json`:

```json
{
  "content": "Customer is a VIP - handle with priority",
  "message_type": "outgoing",
  "private": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations/<conversation-id>/messages" -H "api_access_token: ${CHATWOOT_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/chatwoot_request.json'
```

---

### 9. Assign Conversation

Assign a conversation to an agent. Replace `<conversation-id>` with the actual conversation ID and `<agent-id>` with the agent ID from the "List Agents" response:

Write to `/tmp/chatwoot_request.json`:

```json
{
  "assignee_id": 1
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations/<conversation-id>/assignments" -H "api_access_token: ${CHATWOOT_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/chatwoot_request.json'
```

---

### 10. Update Conversation Status

Change conversation status (open, resolved, pending). Replace `<conversation-id>` with the actual conversation ID from the "List Conversations" response:

Write to `/tmp/chatwoot_request.json`:

```json
{
  "status": "resolved"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations/<conversation-id>/toggle_status" -H "api_access_token: ${CHATWOOT_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/chatwoot_request.json'
```

---

### 11. List Agents

Get all agents in the account:

```bash
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/agents" -H "api_access_token: ${CHATWOOT_API_TOKEN}"' | jq '.[] | {id, name, email, role, availability_status}'
```

---

### 12. List Inboxes

Get all inboxes (channels) in the account:

```bash
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/inboxes" -H "api_access_token: ${CHATWOOT_API_TOKEN}"' | jq '.payload[] | {id, name, channel_type}'
```

---

### 13. Get Conversation Counts

Get counts by status for dashboard:

```bash
bash -c 'curl -s -X GET "${CHATWOOT_BASE_URL}/api/v1/accounts/${CHATWOOT_ACCOUNT_ID}/conversations/meta" -H "api_access_token: ${CHATWOOT_API_TOKEN}"' | jq '.meta.all_count, .meta.mine_count'
```

---

## Conversation Status

| Status | Description |
|--------|-------------|
| `open` | Active conversation |
| `resolved` | Closed/completed |
| `pending` | Waiting for response |
| `snoozed` | Temporarily paused |

---

## Message Types

| Type | Value | Description |
|------|-------|-------------|
| Outgoing | `outgoing` | Agent to customer |
| Incoming | `incoming` | Customer to agent |
| Private | `private: true` | Internal note (not visible to customer) |

---

## Response Fields

### Contact
| Field | Description |
|-------|-------------|
| `id` | Contact ID |
| `name` | Contact name |
| `email` | Email address |
| `phone_number` | Phone number |
| `identifier` | External system ID |
| `custom_attributes` | Custom fields |

### Conversation
| Field | Description |
|-------|-------------|
| `id` | Conversation ID |
| `inbox_id` | Channel/inbox ID |
| `status` | Current status |
| `assignee` | Assigned agent |
| `contact` | Customer info |

### Message
| Field | Description |
|-------|-------------|
| `id` | Message ID |
| `content` | Message text |
| `message_type` | incoming/outgoing |
| `private` | Is internal note |
| `status` | sent/delivered/read/failed |

---

## Guidelines

1. **Get API token from Profile Settings**: Log into Chatwoot → Profile → Access Token
2. **Account ID is in URL**: Look at `/app/accounts/{id}/...` in your browser
3. **Inbox ID is required**: Get inbox IDs first with the list inboxes endpoint
4. **Use source_id for conversations**: Required to create conversations via API
5. **Private messages**: Set `private: true` for internal notes
6. **Self-hosted**: Change `CHATWOOT_BASE_URL` to your instance URL
7. **Webhooks recommended**: Use webhooks for real-time updates instead of polling
