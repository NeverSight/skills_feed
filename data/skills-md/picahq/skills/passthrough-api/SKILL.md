---
name: passthrough-api
description: Execute HTTP requests to 200+ platforms via Pica's unified Passthrough API
---

# Pica Passthrough API

Complete REST API for managing integrations, connections, and executing actions across 200+ platforms.

## Overview

The Pica API provides:
- **Core API** - Manage connectors, actions, and connections
- **Passthrough API** - Execute any action on connected platforms
- **Vault API** - Manage user connections and credentials

Base URL: `https://api.picaos.com`

## Authentication

All requests require the `x-pica-secret` header with your API key.

```bash
curl https://api.picaos.com/v1/available-connectors \
  -H "x-pica-secret: YOUR_API_KEY"
```

### Getting Your API Key

1. Create account at https://app.picaos.com
2. Go to Settings > API Keys
3. Copy your secret key

### Environments

| Environment | Description |
|-------------|-------------|
| Sandbox | Test credentials, safe for development |
| Production | Live credentials, real data |

API keys are environment-specific and cannot be transferred between environments.

---

## Core API

### List Available Connectors

Get all supported integrations.

```
GET /v1/available-connectors
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `platform` | string | - | Filter by platform (e.g., `gmail`, `slack`) |
| `authkit` | boolean | false | Only AuthKit-enabled connectors |
| `key` | string | - | Filter by connector key |
| `name` | string | - | Filter by connector name |
| `category` | string | - | Filter by category (AI, Payments, CRM, etc.) |
| `limit` | number | 20 | Results per page |
| `page` | number | 1 | Page number |

**Response:**

```json
{
  "rows": [
    {
      "id": "conn_abc123",
      "name": "Gmail",
      "key": "gmail",
      "platform": "gmail",
      "platformVersion": "1.0.0",
      "status": "generally_available",
      "description": "Send and receive emails",
      "category": "Communication",
      "image": "https://assets.picaos.com/logos/gmail.svg",
      "tags": ["email", "google"],
      "oauth": true,
      "tools": 15,
      "version": "1.0.0",
      "active": true
    }
  ],
  "total": 200,
  "pages": 10,
  "page": 1
}
```

**Example:**

```bash
# Get all AuthKit-enabled connectors
curl "https://api.picaos.com/v1/available-connectors?authkit=true&limit=100" \
  -H "x-pica-secret: YOUR_API_KEY"

# Get CRM connectors
curl "https://api.picaos.com/v1/available-connectors?category=CRM" \
  -H "x-pica-secret: YOUR_API_KEY"
```

---

### List Available Actions

Get actions for a specific platform.

```
GET /v1/available-actions/{platform}
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `platform` | string | Platform identifier (e.g., `gmail`, `hubspot`) |

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | string | - | Filter by action title |
| `key` | string | - | Filter by action key |
| `method` | string | - | Filter by HTTP method (GET, POST, PUT, PATCH, DELETE) |
| `limit` | number | 20 | Results per page |
| `page` | number | 1 | Page number |

**Response:**

```json
{
  "rows": [
    {
      "title": "Send Email",
      "key": "gmail-send-email",
      "method": "POST",
      "platform": "gmail",
      "description": "Send an email message"
    },
    {
      "title": "List Labels",
      "key": "gmail-list-labels",
      "method": "GET",
      "platform": "gmail",
      "description": "Get all labels in the mailbox"
    }
  ],
  "total": 15,
  "pages": 1,
  "page": 1
}
```

**Example:**

```bash
# Get all Gmail actions
curl "https://api.picaos.com/v1/available-actions/gmail" \
  -H "x-pica-secret: YOUR_API_KEY"

# Get only POST actions for Slack
curl "https://api.picaos.com/v1/available-actions/slack?method=POST" \
  -H "x-pica-secret: YOUR_API_KEY"
```

---

### Get Action Knowledge

Get detailed schema and parameters for a specific action.

```
GET /v1/actions/{actionId}/knowledge
```

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `actionId` | string | Action identifier (e.g., `gmail-send-email`) |

**Response:**

```json
{
  "action": {
    "id": "gmail-send-email",
    "title": "Send Email",
    "description": "Send an email message via Gmail",
    "method": "POST",
    "path": "/gmail/v1/users/me/messages/send"
  },
  "parameters": {
    "body": {
      "type": "object",
      "properties": {
        "to": {
          "type": "string",
          "description": "Recipient email address"
        },
        "subject": {
          "type": "string",
          "description": "Email subject line"
        },
        "body": {
          "type": "string",
          "description": "Email body content"
        }
      },
      "required": ["to", "subject", "body"]
    }
  },
  "examples": [
    {
      "description": "Send a simple email",
      "request": {
        "to": "recipient@example.com",
        "subject": "Hello",
        "body": "This is the email content."
      }
    }
  ]
}
```

**Example:**

```bash
curl "https://api.picaos.com/v1/actions/gmail-send-email/knowledge" \
  -H "x-pica-secret: YOUR_API_KEY"
```

---

## Vault API (Connections)

### List Connections

Get user's connected integrations.

```
GET /v1/vault/connections
```

**Query Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `key` | string | - | Comma-separated connection keys |
| `platform` | string | - | Filter by platform (e.g., `gmail`) |
| `identity` | string | - | Filter by user/team/org ID |
| `identityType` | string | - | `user`, `team`, `organization`, `project` |
| `active` | boolean | true | Filter by active status |
| `tags` | string | - | Comma-separated tags |
| `limit` | number | 20 | Results per page |
| `page` | number | 1 | Page number |

**Response:**

```json
{
  "rows": [
    {
      "id": "conn_xyz789",
      "key": "live::gmail::default::abc123",
      "name": "My Gmail",
      "type": "api",
      "platform": "gmail",
      "environment": "live",
      "identity": "user_123",
      "identityType": "user",
      "state": "operational",
      "description": "Personal Gmail account",
      "tags": ["email", "personal"],
      "version": "1.0.0",
      "active": true,
      "createdAt": "2024-01-15T10:30:00Z"
    }
  ],
  "total": 5,
  "pages": 1,
  "page": 1
}
```

**Connection States:**

| State | Description |
|-------|-------------|
| `operational` | Connection working normally |
| `degraded` | Partial functionality |
| `failed` | Connection broken, needs reauth |
| `unknown` | Status not determined |

**Example:**

```bash
# Get all connections for a user
curl "https://api.picaos.com/v1/vault/connections?identity=user_123&identityType=user" \
  -H "x-pica-secret: YOUR_API_KEY"

# Get Gmail connections only
curl "https://api.picaos.com/v1/vault/connections?platform=gmail" \
  -H "x-pica-secret: YOUR_API_KEY"
```

---

### Get Connection

Get a specific connection by ID.

```
GET /v1/vault/connections/{connectionId}
```

**Example:**

```bash
curl "https://api.picaos.com/v1/vault/connections/conn_xyz789" \
  -H "x-pica-secret: YOUR_API_KEY"
```

---

### Delete Connection

Remove a connection.

```
DELETE /v1/vault/connections/{connectionId}
```

**Example:**

```bash
curl -X DELETE "https://api.picaos.com/v1/vault/connections/conn_xyz789" \
  -H "x-pica-secret: YOUR_API_KEY"
```

---

## Passthrough API

Execute actions directly on connected platforms. Responses match the underlying API's format.

```
{METHOD} /v1/passthrough/{path}
```

**Required Headers:**

| Header | Description |
|--------|-------------|
| `x-pica-secret` | Your Pica API key |
| `x-pica-connection-key` | Connection key for the integration |

**Optional Headers:**

| Header | Description |
|--------|-------------|
| `Content-Type` | Usually `application/json` |

### Example: Send Gmail

```bash
curl -X POST "https://api.picaos.com/v1/passthrough/gmail/v1/users/me/messages/send" \
  -H "x-pica-secret: YOUR_API_KEY" \
  -H "x-pica-connection-key: live::gmail::default::abc123" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "recipient@example.com",
    "subject": "Hello from Pica",
    "body": "This email was sent via the Pica Passthrough API."
  }'
```

### Example: Post Slack Message

```bash
curl -X POST "https://api.picaos.com/v1/passthrough/slack/chat.postMessage" \
  -H "x-pica-secret: YOUR_API_KEY" \
  -H "x-pica-connection-key: live::slack::default::xyz789" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "#general",
    "text": "Hello from Pica!"
  }'
```

### Example: Create HubSpot Contact

```bash
curl -X POST "https://api.picaos.com/v1/passthrough/hubspot/crm/v3/objects/contacts" \
  -H "x-pica-secret: YOUR_API_KEY" \
  -H "x-pica-connection-key: live::hubspot::default::def456" \
  -H "Content-Type: application/json" \
  -d '{
    "properties": {
      "email": "newcontact@example.com",
      "firstname": "John",
      "lastname": "Doe"
    }
  }'
```

### Example: Get Stripe Customers

```bash
curl "https://api.picaos.com/v1/passthrough/stripe/v1/customers?limit=10" \
  -H "x-pica-secret: YOUR_API_KEY" \
  -H "x-pica-connection-key: live::stripe::default::ghi789"
```

---

## Common Patterns

### Pagination

All list endpoints support pagination:

```bash
# First page, 50 results
curl "https://api.picaos.com/v1/available-connectors?limit=50&page=1" \
  -H "x-pica-secret: YOUR_API_KEY"

# Second page
curl "https://api.picaos.com/v1/available-connectors?limit=50&page=2" \
  -H "x-pica-secret: YOUR_API_KEY"
```

### Multi-Tenant Filtering

Filter connections by identity:

```bash
# Get connections for specific user
curl "https://api.picaos.com/v1/vault/connections?identity=user_123&identityType=user" \
  -H "x-pica-secret: YOUR_API_KEY"

# Get connections for a team
curl "https://api.picaos.com/v1/vault/connections?identity=team_456&identityType=team" \
  -H "x-pica-secret: YOUR_API_KEY"
```

### Error Handling

Pica returns standard HTTP status codes:

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad request (invalid parameters) |
| 401 | Unauthorized (invalid API key) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Not found |
| 429 | Rate limited |
| 500 | Server error |

Error response format:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "The 'platform' parameter is required"
  }
}
```

---

## TypeScript Examples

### List Connectors

```typescript
async function getConnectors(category?: string) {
  const params = new URLSearchParams({ limit: "100" });
  if (category) params.set("category", category);

  const response = await fetch(
    `https://api.picaos.com/v1/available-connectors?${params}`,
    {
      headers: {
        "x-pica-secret": process.env.PICA_SECRET_KEY!,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
```

### Execute Passthrough Request

```typescript
async function sendEmail(connectionKey: string, to: string, subject: string, body: string) {
  const response = await fetch(
    "https://api.picaos.com/v1/passthrough/gmail/v1/users/me/messages/send",
    {
      method: "POST",
      headers: {
        "x-pica-secret": process.env.PICA_SECRET_KEY!,
        "x-pica-connection-key": connectionKey,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ to, subject, body }),
    }
  );

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || "Failed to send email");
  }

  return response.json();
}
```

### Get User Connections

```typescript
async function getUserConnections(userId: string) {
  const params = new URLSearchParams({
    identity: userId,
    identityType: "user",
    active: "true",
  });

  const response = await fetch(
    `https://api.picaos.com/v1/vault/connections?${params}`,
    {
      headers: {
        "x-pica-secret": process.env.PICA_SECRET_KEY!,
      },
    }
  );

  return response.json();
}
```

---

## Python Examples

### List Connectors

```python
import requests
import os

def get_connectors(category=None):
    params = {"limit": 100}
    if category:
        params["category"] = category

    response = requests.get(
        "https://api.picaos.com/v1/available-connectors",
        headers={"x-pica-secret": os.environ["PICA_SECRET_KEY"]},
        params=params,
    )
    response.raise_for_status()
    return response.json()
```

### Execute Passthrough Request

```python
def send_slack_message(connection_key, channel, text):
    response = requests.post(
        "https://api.picaos.com/v1/passthrough/slack/chat.postMessage",
        headers={
            "x-pica-secret": os.environ["PICA_SECRET_KEY"],
            "x-pica-connection-key": connection_key,
            "Content-Type": "application/json",
        },
        json={"channel": channel, "text": text},
    )
    response.raise_for_status()
    return response.json()
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid API key | Verify key at app.picaos.com/settings/api-keys |
| 403 Forbidden | Wrong environment | Check sandbox vs production key |
| Connection not found | Invalid connection key | List connections to get valid keys |
| Passthrough 400 error | Invalid request body | Check action knowledge for required params |
| Rate limited (429) | Too many requests | Implement exponential backoff |

---

## API Reference Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/available-connectors` | GET | List all supported integrations |
| `/v1/available-actions/{platform}` | GET | List actions for a platform |
| `/v1/actions/{actionId}/knowledge` | GET | Get action schema and params |
| `/v1/vault/connections` | GET | List user connections |
| `/v1/vault/connections/{id}` | GET | Get specific connection |
| `/v1/vault/connections/{id}` | DELETE | Delete connection |
| `/v1/passthrough/{path}` | ANY | Execute action on platform |

---

## Links

- Dashboard: https://app.picaos.com
- API Keys: https://app.picaos.com/settings/api-keys
- Actions Browser: https://app.picaos.com/tools
- Documentation: https://docs.picaos.com
