---
name: workos-api-widgets
description: WorkOS Widgets API endpoints — generate widget tokens and manage widget configuration.
---

<!-- refined:sha256:eda510c1c51f -->

# WorkOS Widgets API Reference

## Step 1: Fetch Documentation

**STOP. WebFetch the relevant docs for latest implementation details before proceeding.**

- https://workos.com/docs/reference/widgets
- https://workos.com/docs/reference/widgets/get-token

## Overview

The Widgets API provides a **single endpoint** for generating short-lived access tokens that authorize embedded widget components. Widgets let users manage their organization settings (SSO, Directory Sync, Audit Logs, etc.) directly in your application without leaving your UI.

## Endpoint Catalog

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/widgets/token` | Generate a widget access token for a specific organization |

## Authentication

All Widgets API calls require:

```bash
Authorization: Bearer <WORKOS_API_KEY>
```

Your API key must start with `sk_` (secret key). Find it in the WorkOS Dashboard under API Keys.

## Operation Decision Tree

**Goal: Embed a widget in your application**

1. User clicks "Manage SSO" (or similar) in your UI
2. Backend calls `POST /widgets/token` with `organization_id` + `widget_scope`
3. Return token to frontend
4. Frontend renders widget component with token
5. Token expires after 10 minutes (default) — generate a new token if needed

## Request Pattern: Generate Token

### Endpoint

```
POST https://api.workos.com/widgets/token
Content-Type: application/json
Authorization: Bearer sk_test_...
```

### Required Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `organization_id` | string | The WorkOS organization ID (starts with `org_`) |
| `widget_scope` | string | Widget type: `sso`, `dsync`, `audit_logs`, or `log_streams` |

### Optional Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `expires_in` | integer | Token lifetime in seconds | `600` (10 min) |

### Example Request

```bash
curl -X POST https://api.workos.com/widgets/token \
  -H "Authorization: Bearer sk_test_..." \
  -H "Content-Type: application/json" \
  -d '{
    "organization_id": "org_01H5K5Z4J8T9D3G2F1N6M8V7C4",
    "widget_scope": "sso",
    "expires_in": 600
  }'
```

### Example Response (Success)

```json
{
  "token": "widget_01H5K5ZABC123XYZ...",
  "expires_at": "2024-01-15T12:45:00.000Z"
}
```

## Response Patterns

### Success (200 OK)

```json
{
  "token": "string",        // Pass this to the widget component
  "expires_at": "string"    // ISO 8601 timestamp
}
```

### Error Responses

| Status | Cause | Fix |
|--------|-------|-----|
| `400` | Missing required field (`organization_id` or `widget_scope`) | Include all required parameters in request body |
| `400` | Invalid `widget_scope` value | Use one of: `sso`, `dsync`, `audit_logs`, `log_streams` |
| `401` | Invalid or missing API key | Check `Authorization: Bearer sk_...` header is correct |
| `404` | Organization not found | Verify `organization_id` exists in your WorkOS environment |
| `429` | Rate limit exceeded | Retry after delay (see `Retry-After` header) |
| `500` | WorkOS server error | Retry request with exponential backoff |

### Error Response Format

```json
{
  "error": "invalid_request",
  "error_description": "organization_id is required"
}
```

## Rate Limits

- **Default limit**: 600 requests per minute per API key
- **On limit hit**: Returns `429` with `Retry-After` header (seconds until reset)
- **Strategy**: Implement exponential backoff (start with 1s, double on each retry)

## Token Lifecycle

1. **Generation**: Call `POST /widgets/token` from your backend
2. **Expiration**: Default 10 minutes (customizable via `expires_in`)
3. **Refresh**: Tokens cannot be refreshed — generate a new token when expired
4. **Security**: Tokens are single-use per widget session — do NOT reuse across users

## SDK Usage (Node.js)

```javascript
import { WorkOS } from '@workos-inc/node';

const workos = new WorkOS(process.env.WORKOS_API_KEY);

// Generate widget token
const { token } = await workos.widgets.getToken({
  organizationId: 'org_01H5K5Z4J8T9D3G2F1N6M8V7C4',
  widgetScope: 'sso',
  expiresIn: 600
});

// Return token to frontend
res.json({ token });
```

## Verification Commands

### Test Token Generation

```bash
# Replace with your actual API key and organization ID
export WORKOS_API_KEY="sk_test_..."
export ORG_ID="org_01H5K5Z4J8T9D3G2F1N6M8V7C4"

curl -X POST https://api.workos.com/widgets/token \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"organization_id\": \"$ORG_ID\",
    \"widget_scope\": \"sso\"
  }"
```

**Expected output**: JSON with `token` and `expires_at` fields.

### Verify Token Format

```bash
# Extract token from response
TOKEN=$(curl -s -X POST https://api.workos.com/widgets/token \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"organization_id\": \"$ORG_ID\", \"widget_scope\": \"sso\"}" \
  | jq -r '.token')

echo "Token: $TOKEN"
# Should start with "widget_"
```

## Common Integration Patterns

### Backend Route (Express)

```javascript
app.post('/api/widget-token', async (req, res) => {
  const { organizationId } = req.body;
  
  try {
    const { token } = await workos.widgets.getToken({
      organizationId,
      widgetScope: 'sso'
    });
    res.json({ token });
  } catch (error) {
    if (error.status === 404) {
      return res.status(404).json({ error: 'Organization not found' });
    }
    res.status(500).json({ error: 'Failed to generate token' });
  }
});
```

### Frontend Token Consumption

```javascript
// Fetch token from your backend
const response = await fetch('/api/widget-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ organizationId: 'org_...' })
});

const { token } = await response.json();

// Pass token to widget component (exact usage depends on widget type)
```

## Troubleshooting

### "organization_id is required"

**Cause**: Request body missing `organization_id` field.  
**Fix**: Ensure JSON body includes `{"organization_id": "org_..."}`

### "Invalid widget_scope"

**Cause**: `widget_scope` is not one of the allowed values.  
**Fix**: Use `sso`, `dsync`, `audit_logs`, or `log_streams`.

### Token expired immediately

**Cause**: `expires_in` set too low or clock skew.  
**Fix**: Use default 600 seconds or higher. Check server time sync.

### 401 Unauthorized

**Cause**: API key missing, malformed, or wrong environment (test vs production).  
**Fix**: Verify `Authorization: Bearer sk_test_...` header matches your WorkOS environment.

## Related Skills

- **workos-widgets** — Widget integration patterns and frontend setup
- **workos-api-sso** — SSO configuration API (what the SSO widget manages)
- **workos-api-directory-sync** — Directory Sync API (what the dsync widget manages)
- **workos-api-audit-logs** — Audit Logs API (what the audit_logs widget manages)
- **workos-api-organization** — Organization management API
