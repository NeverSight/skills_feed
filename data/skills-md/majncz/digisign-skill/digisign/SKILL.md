---
name: digisign
description: Czech electronic signature API integration for DigiSign. Use when the user needs to create, send, and manage digital signature envelopes, upload documents for signing, track signature status, or integrate embedded signing flows. Supports multiple signature types, webhooks for status tracking, and Czech Bank iD verification. Triggers on mentions of DigiSign, elektronicky podpis, digital signatures, envelope signing, or document signing workflows.
---

# DigiSign API

Czech electronic signature service REST API integration. This skill provides both CLI scripts for quick operations and comprehensive API documentation for implementing DigiSign into your applications.

## API Overview

### Base URLs
| Environment | URL | Purpose |
|-------------|-----|---------|
| Production | `https://api.digisign.org` | Live operations |
| Staging | `https://api.staging.digisign.org` | Testing (contact podpora@digisign.cz for access) |
| OpenAPI Docs | `https://api.digisign.org/api/docs` | Interactive documentation |
| OpenAPI JSON | `https://api.digisign.org/api/docs.json` | Import to Postman |

### Authentication
DigiSign uses Bearer token authentication (RFC 6750).

**Step 1: Exchange credentials for token**
```http
POST /api/auth-token
Content-Type: application/json

{
  "accessKey": "your-access-key",
  "secretKey": "your-secret-key"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "exp": 1682572132,
  "iat": 1682485732
}
```

**Step 2: Use token in all subsequent requests**
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...
```

Token is valid for ~24 hours. Get a new one when expired.

### API Key Setup
1. Log into DigiSign selfcare at https://app.digisign.org
2. Go to Settings > For Developers > API Keys
3. Click "New API Key" and configure permissions
4. Save `accessKey` and `secretKey` securely (shown only once)

## Response Formats

### Pagination
All list endpoints return paginated responses:

```json
{
  "items": [...],
  "count": 127,
  "page": 1,
  "itemsPerPage": 30
}
```

**Query parameters:**
- `page` - Page number (default: 1)
- `itemsPerPage` - Items per page (default: 30, max: 500)

### Filtering
List endpoints support filter operators as query parameters:

| Operator | Example | Description |
|----------|---------|-------------|
| `[eq]` | `status[eq]=completed` | Equals |
| `[neq]` | `status[neq]=draft` | Not equals |
| `[in]` | `status[in][]=sent&status[in][]=completed` | In array |
| `[contains]` | `name[contains]=contract` | Contains string |
| `[starts_with]` | `email[starts_with]=john` | Starts with |
| `[gt]` | `createdAt[gt]=2024-01-01` | Greater than |
| `[gte]` | `createdAt[gte]=2024-01-01` | Greater than or equal |
| `[lt]` | `validTo[lt]=2024-12-31` | Less than |
| `[lte]` | `validTo[lte]=2024-12-31` | Less than or equal |

### Sorting
```
order[createdAt]=desc
order[updatedAt]=asc
```

Available sort fields: `createdAt`, `updatedAt`, `validTo`, `completedAt`, `cancelledAt`, `declinedAt`

### Error Responses
```json
{
  "type": "https://tools.ietf.org/html/rfc2616#section-10",
  "title": "An error occurred",
  "status": 400,
  "violations": [
    {
      "propertyPath": "email",
      "message": "This value is not a valid email address."
    }
  ]
}
```

### HTTP Status Codes
| Status | Meaning |
|--------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No content (successful delete) |
| 400 | Bad request - check `violations` field |
| 401 | Authentication failed - get new token |
| 403 | Forbidden - insufficient permissions |
| 404 | Resource not found |
| 422 | Validation error - check `violations` |
| 429 | Rate limit exceeded |

### Important API Notes
- **Omitting an attribute** in request body = don't change it (for updates)
- **Sending `null`** = explicitly set to null (may error if not nullable)
- **HATEOAS**: Responses include `_actions` and `_links` for navigation
- **Localization**: Set `Accept-Language: en|cs|sk|pl` for localized error messages

## Core Workflow

The typical envelope signing workflow has 7 steps:

| # | Step | Endpoint |
|---|------|----------|
| 1 | Authenticate | `POST /api/auth-token` |
| 2 | Create envelope | `POST /api/envelopes` |
| 3 | Add documents | `POST /api/files` + `POST /api/envelopes/{id}/documents` |
| 4 | Add recipients | `POST /api/envelopes/{id}/recipients` |
| 5 | Add signature tags | `POST /api/envelopes/{id}/tags` or `/tags/by-placeholder` |
| 6 | Send envelope | `POST /api/envelopes/{id}/send` |
| 7 | Download signed docs | `GET /api/envelopes/{id}/download` |

### Example: Create and Send Envelope

```javascript
// 1. Authenticate
const tokenRes = await fetch('https://api.digisign.org/api/auth-token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    accessKey: process.env.DIGISIGN_ACCESS_KEY,
    secretKey: process.env.DIGISIGN_SECRET_KEY
  })
});
const { token } = await tokenRes.json();

const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};

// 2. Create envelope
const envelopeRes = await fetch('https://api.digisign.org/api/envelopes', {
  method: 'POST',
  headers,
  body: JSON.stringify({
    name: 'Contract Agreement',
    emailBody: 'Please review and sign the attached contract.'
  })
});
const envelope = await envelopeRes.json();

// 3. Upload file
const formData = new FormData();
formData.append('file', fs.createReadStream('contract.pdf'));
const fileRes = await fetch('https://api.digisign.org/api/files', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData
});
const file = await fileRes.json();

// 4. Add document to envelope
await fetch(`https://api.digisign.org/api/envelopes/${envelope.id}/documents`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    file: `/api/files/${file.id}`,
    name: 'Contract'
  })
});

// 5. Add recipient
const recipientRes = await fetch(`https://api.digisign.org/api/envelopes/${envelope.id}/recipients`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    role: 'signer',
    name: 'John Doe',
    email: 'john@example.com'
  })
});
const recipient = await recipientRes.json();

// 6. Add signature tag (by placeholder)
await fetch(`https://api.digisign.org/api/envelopes/${envelope.id}/tags/by-placeholder`, {
  method: 'POST',
  headers,
  body: JSON.stringify({
    recipient: `/api/envelopes/${envelope.id}/recipients/${recipient.id}`,
    type: 'signature',
    placeholder: '{{sign_here}}',
    positioning: 'center'
  })
});

// 7. Send envelope
await fetch(`https://api.digisign.org/api/envelopes/${envelope.id}/send`, {
  method: 'POST',
  headers
});
```

## Enums Reference

### Envelope Statuses
| Status | Description |
|--------|-------------|
| `draft` | Not yet sent, can be edited |
| `sent` | Sent, waiting for signatures |
| `completed` | All recipients signed |
| `expired` | Deadline passed without completion |
| `declined` | Signer declined to sign |
| `disapproved` | Approver disapproved |
| `cancelled` | Cancelled by sender |

### Recipient Roles
| Role | Description |
|------|-------------|
| `signer` | Remote signer - receives email with signing link |
| `in_person` | Signs in person on intermediary's device |
| `cc` | Copy recipient - receives completed documents only |
| `approver` | Approves or rejects document |
| `autosign` | Automatic signature with company seal |
| `semi_autosign` | Triggered automatic signature via API call |

### Recipient Statuses
| Status | Description |
|--------|-------------|
| `draft` | Not yet sent |
| `sent` | Invitation sent |
| `delivered` | Opened the signing link |
| `signed` | Completed signing |
| `declined` | Declined to sign |
| `disapproved` | Disapproved (for approvers) |
| `cancelled` | Cancelled |
| `authFailed` | Authentication failed (3 attempts exhausted) |

### Signature Types
| Type | Description |
|------|-------------|
| `simple` | Simple electronic signature |
| `biometric` | Handwritten signature capture |
| `bank_id_sign` | Bank iD Sign (qualified, Czech) |
| `certificate` | Certificate-based signature |

### Authentication Methods
| Method | Description |
|--------|-------------|
| `none` | No authentication required |
| `sms` | SMS code verification |
| `bank_id` | Bank iD verification (Czech national identity) |

### Tag Types
| Type | Description |
|------|-------------|
| `signature` | Signature field (required for signers) |
| `approval` | Approval stamp field |
| `text` | Text input field |
| `document` | ID document photos field |
| `attachment` | File attachment field |
| `checkbox` | Checkbox field |
| `radio_button` | Radio button (use with group) |
| `date_of_signature` | Auto-filled signature date |

### Tag Positioning
| Position | Description |
|----------|-------------|
| `top_left` | Tag top-left at placeholder top-left |
| `top_center` | Tag top-center at placeholder top-center |
| `top_right` | Tag top-right at placeholder top-right |
| `middle_left` | Tag middle-left at placeholder middle-left |
| `center` | Tag center at placeholder center |
| `middle_right` | Tag middle-right at placeholder middle-right |
| `bottom_left` | Tag bottom-left at placeholder bottom-left |
| `bottom_center` | Tag bottom-center at placeholder bottom-center |
| `bottom_right` | Tag bottom-right at placeholder bottom-right |

### Channels
| Channel | Description |
|---------|-------------|
| `email` | Notifications via email |
| `sms` | Notifications via SMS |

## Webhook Events

### Envelope Events
| Event | Description |
|-------|-------------|
| `envelopeSent` | Envelope was sent |
| `envelopeCompleted` | All signatures completed |
| `envelopeExpired` | Deadline passed |
| `envelopeDeclined` | Signer declined |
| `envelopeDisapproved` | Approver disapproved |
| `envelopeCancelled` | Cancelled by sender |
| `envelopeDeleted` | Envelope deleted |

### Recipient Events
| Event | Description |
|-------|-------------|
| `recipientSent` | Invitation sent to recipient |
| `recipientDelivered` | Recipient opened the link |
| `recipientNonDelivered` | Delivery failed (bad email, etc.) |
| `recipientAuthFailed` | Auth attempts exhausted |
| `recipientSigned` | Recipient signed |
| `recipientDownloaded` | Downloaded completed docs |
| `recipientDeclined` | Declined to sign |
| `recipientDisapproved` | Disapproved |
| `recipientCanceled` | Recipient cancelled |

### Webhook Payload Format
```json
{
  "id": "3974d252-b027-46df-9fd8-ddae54bc9ab9",
  "event": "envelopeCompleted",
  "name": "envelope.completed",
  "time": "2021-06-07T14:07:23+02:00",
  "entityName": "envelope",
  "entityId": "4fcf171c-4522-4a53-8a72-784e1dd36c2a",
  "data": {
    "status": "completed"
  }
}
```

### Webhook Signature Verification
Header format: `Signature: t={timestamp},s={signature}`

```python
import hmac
import hashlib
import time

def verify_webhook(signature_header, body, secret):
    # Parse header
    parts = dict(p.split('=') for p in signature_header.split(','))
    timestamp = int(parts['t'])
    signature = parts['s']

    # Check timestamp (5 minute window)
    if abs(time.time() - timestamp) > 300:
        raise Exception('Request too old - possible replay attack')

    # Verify signature
    expected = hmac.new(
        secret.encode(),
        f"{timestamp}.{body}".encode(),
        hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise Exception('Invalid signature')

    return True
```

### Webhook Retry Schedule
12 attempts over ~7 days if delivery fails:

| Attempt | 1 | 2 | 3 | 4 | 5 | 6-12 |
|---------|---|---|---|---|---|------|
| Delay | 5m | 10m | 30m | 1h | 2h | 24h each |

## CLI Scripts Reference

For quick operations, use the bundled Python scripts:

| Script | Commands | Description |
|--------|----------|-------------|
| `auth.py` | get-token, status, clear | Token management |
| `envelope.py` | list, get, create, update, delete, send, cancel, download, download-url | Envelope operations |
| `document.py` | upload, add, list, get, update, delete, download, download-url | Document management |
| `recipient.py` | list, add, get, update, delete, resend, autosign | Recipient management |
| `tag.py` | list, add, add-by-placeholder, get, update, delete | Signature tag operations |
| `webhook.py` | list, create, get, update, delete, test, attempts, resend, verify-signature | Webhook management |
| `embed.py` | envelope, recipient, signing, detail | Embedding URLs |

### Environment Variables
```bash
export DIGISIGN_ACCESS_KEY="your-access-key"
export DIGISIGN_SECRET_KEY="your-secret-key"
# Optional: use staging for testing
export DIGISIGN_API_URL="https://api.staging.digisign.org"
```

### Quick Start with Scripts
```bash
# Authenticate
python scripts/auth.py get-token --save

# List envelopes
python scripts/envelope.py list

# Create and send envelope
python scripts/envelope.py create --name "Contract" --email-body "Please sign"
python scripts/document.py upload contract.pdf
python scripts/document.py add <envelope_id> --file-id <file_id> --name "Contract"
python scripts/recipient.py add <envelope_id> --role signer --name "John Doe" --email "john@example.com"
python scripts/tag.py add-by-placeholder <envelope_id> --recipient <rec_id> --type signature --placeholder "{{sign}}"
python scripts/envelope.py send <envelope_id> --yes
```

## Czech-Specific Notes

### Bank iD (Bankovni identita)
Czech national identity verification system through participating banks.
- Use `authenticationOnOpen: "bank_id"` or `authenticationOnSignature: "bank_id"`
- Verifies signer identity through their online banking
- Required for qualified electronic signatures

### Qualified Electronic Signature
For legally binding signatures in Czech Republic:
- Set `signatureType: "bank_id_sign"`
- Requires Bank iD verification
- Compliant with eIDAS regulation

### Audit Log (Protokol)
Every envelope includes a detailed audit log:
- Download with `GET /api/envelopes/{id}/download?include_log=true`
- Or get only the log: `GET /api/envelopes/{id}/download?output=only_log`

### Timestamping
Enable qualified timestamps on documents:
- Set `timestampDocuments: true` in envelope properties
- Available authorities: `ica_tsa` (I.CA)

## Cost Warning

DigiSign charges per envelope **sent**. These operations are FREE:
- Creating/editing draft envelopes
- Uploading documents
- Managing recipients and tags
- Webhook setup
- Generating embed URLs
- Listing and reading resources

**BILLING TRIGGER**: `POST /api/envelopes/{id}/send` - sends real emails and incurs charges.

## References

Detailed documentation for each resource:
- [authentication.md](references/authentication.md) - Token exchange and management
- [api-reference.md](references/api-reference.md) - Complete endpoint reference
- [envelopes.md](references/envelopes.md) - Envelope lifecycle and attributes
- [recipients.md](references/recipients.md) - Recipient roles and options
- [tags.md](references/tags.md) - Tag positioning and types
- [webhooks.md](references/webhooks.md) - Event list and verification
- [embedding.md](references/embedding.md) - Embedded signing integration
