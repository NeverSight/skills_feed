---
name: AutoSend
description: >
  AutoSend email API integration. Use when sending transactional emails,
  managing contacts, or using email templates with AutoSend.
  Triggers on: send email with autosend, autosend api, autosend contacts, email template autosend.
license: MIT
---

# AutoSend Email API

Send transactional emails, manage contacts, and use templates via REST API.

> **Using JavaScript/TypeScript?** See the [SDK Guide](references/sdk-guide.md) for TypeScript examples with the `autosendjs` package.

**Reference:** [API Guide](references/api-guide.md) | [Official API Reference](https://docs.autosend.com/api-reference/introduction)

## Prerequisites

Complete these steps before using the API:

- [ ] **Create Account** — Sign up at [autosend.com](https://autosend.com)
- [ ] **Add Domain** — Settings → Domains → Add Domain → Select AWS region ([docs](https://docs.autosend.com/domain))
- [ ] **Configure DNS** — Copy the generated records (DKIM, SPF, DMARC) to your DNS provider
- [ ] **Verify Domain** — Click "Verify Ownership" and wait for status to turn green (5-30 min)
- [ ] **Get API Key** — Settings → API Keys → Generate API Key ([docs](https://docs.autosend.com/api-keys))
- [ ] **Set Environment Variable** — `export AUTOSEND_API_KEY=as_your_key_here`

---

## Authentication

All requests require a Bearer token in the `Authorization` header:

```
Authorization: Bearer YOUR_API_KEY
```

**Base URL:** `https://api.autosend.com/v1`

All POST/PUT requests must include `Content-Type: application/json`.

---

## Email Operations

### Send Email

`POST /v1/mails/send`

Send a single transactional email.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | `object` | Yes | Sender — `{ "email": "...", "name": "..." }` |
| `to` | `object` | Yes | Recipient — `{ "email": "...", "name": "..." }` |
| `subject` | `string` | Yes | Email subject line |
| `html` | `string` | No | HTML body |
| `text` | `string` | No | Plain text body |
| `templateId` | `string` | No | Template ID (replaces html/text) |
| `dynamicData` | `object` | No | Template variable substitutions |
| `cc` | `array` | No | CC recipients — `[{ "email": "...", "name": "..." }]` |
| `bcc` | `array` | No | BCC recipients — `[{ "email": "...", "name": "..." }]` |
| `replyTo` | `object` | No | Reply-to address — `{ "email": "...", "name": "..." }` |
| `attachments` | `array` | No | File attachments — `[{ "filename": "...", "content": "..." }]` |

**Response:**

```json
{
  "success": true,
  "data": { "emailId": "email_abc123" }
}
```

---

### Bulk Send

`POST /v1/mails/bulk`

Send emails to multiple recipients with a shared sender, subject, and optional template.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `from` | `object` | Yes | Shared sender — `{ "email": "...", "name": "..." }` |
| `subject` | `string` | No | Shared subject (required unless template provides it) |
| `html` | `string` | No | Shared HTML body |
| `text` | `string` | No | Shared plain text body |
| `templateId` | `string` | No | Template ID for templated emails |
| `dynamicData` | `object` | No | Shared default template variables |
| `recipients` | `array` | Yes | Array of recipient objects (max 100) |

**Recipient object:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | `string` | Yes | Recipient email address |
| `name` | `string` | No | Recipient display name |
| `dynamicData` | `object` | No | Per-recipient variables (overrides shared) |
| `cc` | `array` | No | Per-recipient CC |
| `bcc` | `array` | No | Per-recipient BCC |

> **Limit:** Maximum 100 recipients per bulk request.

**Response:**

```json
{
  "success": true,
  "data": {
    "batchId": "batch_abc123",
    "totalRecipients": 2,
    "successCount": 2,
    "failedCount": 0
  }
}
```

---

### Templates

`POST /v1/mails/send` with `templateId`

Send templated emails by passing a `templateId` and `dynamicData` instead of (or alongside) `html`/`text`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `templateId` | `string` | Yes | Template identifier |
| `dynamicData` | `object` | No | Key-value pairs for template variables |

Common template IDs:

| Template | ID | Typical Variables |
|----------|----|-------------------|
| Order Confirmation | `tmpl_order_confirmation` | `orderNumber`, `customerName`, `orderTotal`, `estimatedDelivery` |
| Welcome Email | `tmpl_welcome` | `firstName`, `activationLink`, `supportEmail` |
| Password Reset | `tmpl_password_reset` | `resetLink`, `expiresIn` |

Templates also work with bulk send — pass `templateId` and `dynamicData` in the bulk request body.

---

## Contact Management

### Create Contact

`POST /v1/contacts`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | `string` | Yes | Contact email address |
| `firstName` | `string` | No | Contact first name |
| `lastName` | `string` | No | Contact last name |
| `userId` | `string` | No | External user ID |
| `listIds` | `array` | No | Lists to add contact to — `["list_abc", "list_xyz"]` |
| `customFields` | `object` | No | Custom field values |

**Response:**

```json
{
  "success": true,
  "data": {
    "id": "contact_abc123",
    "email": "user@example.com",
    "firstName": "Jane",
    "lastName": "Smith",
    "listIds": ["list_abc"],
    "customFields": {},
    "createdAt": "2025-01-15T00:00:00Z",
    "updatedAt": "2025-01-15T00:00:00Z"
  }
}
```

---

### Get Contact

`GET /v1/contacts/:id`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | Contact ID (path parameter) |

**Response:** Returns the contact object (same shape as Create Contact response).

---

### Upsert Contact

`POST /v1/contacts/email`

Create or update a contact by email address. If a contact with the given email exists, it is updated; otherwise a new contact is created.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `email` | `string` | Yes | Contact email address |
| `firstName` | `string` | No | Contact first name |
| `lastName` | `string` | No | Contact last name |
| `userId` | `string` | No | External user ID |
| `listIds` | `array` | No | Lists to add contact to |
| `customFields` | `object` | No | Custom field values |

**Response:** Returns the contact object (same shape as Create Contact response).

---

### Delete Contact

`DELETE /v1/contacts/:id`

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `id` | `string` | Yes | Contact ID (path parameter) |

**Response:**

```json
{
  "success": true
}
```

---

## Error Handling

All errors return JSON with an `error` object:

```json
{
  "success": false,
  "error": {
    "message": "The 'to' field is required",
    "code": "VALIDATION_FAILED",
    "details": []
  }
}
```

| Status | Code | Description |
|--------|------|-------------|
| `400` | `VALIDATION_FAILED` | Bad request — missing or invalid parameters |
| `401` | `UNAUTHORIZED` | Invalid or missing API key |
| `402` | `PAYMENT_REQUIRED` | Plan upgrade needed |
| `403` | `FORBIDDEN` | Insufficient permissions |
| `404` | `NOT_FOUND` | Resource not found |
| `429` | `RATE_LIMIT_EXCEEDED` | Too many requests — retry with backoff |
| `500` | `SERVER_ERROR` | Internal server error |

