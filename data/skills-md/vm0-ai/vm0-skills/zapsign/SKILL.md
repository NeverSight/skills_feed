---
name: zapsign
description: ZapSign electronic signature API via curl. Use this skill to create documents for signature, manage signers, and track signing status.
vm0_secrets:
  - ZAPSIGN_API_TOKEN
---

# ZapSign

Use ZapSign via direct `curl` calls to **create and manage electronic signatures** with legal validity.

> Official docs: `https://docs.zapsign.com.br/english`

---

## When to Use

Use this skill when you need to:

- **Create documents** for electronic signature (PDF, DOCX, or Markdown)
- **Add signers** to documents with various authentication methods
- **Track signing status** and get signed documents
- **Send automatic notifications** via email or WhatsApp
- **Collect biometric verification** (selfie, document photo, facial recognition)

---

## Prerequisites

1. Sign up at [ZapSign](https://app.zapsign.com.br/) (Production) or [Sandbox](https://sandbox.app.zapsign.com.br/)
2. Go to Settings > Integrations > ZAPSIGN API
3. Copy your API token

```bash
export ZAPSIGN_API_TOKEN="your-api-token"
```

### Environments

| Environment | API Endpoint | Legal Validity |
|-------------|--------------|----------------|
| Sandbox | `https://sandbox.api.zapsign.com.br` | No |
| Production | `https://api.zapsign.com.br` | Yes |

### Pricing

- Sandbox: Free for testing (no legal validity)
- Production: Requires API plan, pay per document

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq .
> ```

## How to Use

All examples use the **sandbox** environment. For production, replace `sandbox.api.zapsign.com.br` with `api.zapsign.com.br`.

---

### 1. Create Document from PDF URL

Create a document for signature from a public PDF URL:

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Employment Contract",
  "url_pdf": "https://example.com/contract.pdf",
  "lang": "en",
  "signers": [
    {
      "name": "John Doe",
      "email": "john@example.com",
      "auth_mode": "assinaturaTela",
      "send_automatic_email": true
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, sign_url: .signers[0].sign_url}'
```

---

### 2. Create Document from Base64

Create a document from base64-encoded PDF:

```bash
# First, encode your PDF to base64
BASE64_PDF=$(base64 -i document.pdf)
```

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Contract",
  "base64_pdf": "${BASE64_PDF}",
  "signers": [
    {
      "name": "Jane Smith",
      "email": "jane@example.com"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, signers}'
```

---

### 3. Create Document from Markdown

Create a document directly from Markdown text (great for AI integrations):

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Service Agreement",
  "markdown_text": "# Service Agreement\n\nThis agreement is between **Company A** and **Client B**.\n\n## Terms\n\n1. Service will be provided for 12 months\n2. Payment is due monthly\n\n---\n\nSignature: ________________",
  "signers": [
    {
      "name": "Client Name",
      "email": "client@example.com"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, original_file}'
```

---

### 4. Create Document with Multiple Signers

Create a document with signing order:

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Multi-party Contract",
  "url_pdf": "https://example.com/contract.pdf",
  "signature_order_active": true,
  "signers": [
    {
      "name": "First Signer",
      "email": "first@example.com",
      "order_group": 1,
      "send_automatic_email": true
    },
    {
      "name": "Second Signer",
      "email": "second@example.com",
      "order_group": 2,
      "send_automatic_email": true
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, signature_order_active}'
```

---

### 5. Create Document with Expiration

Create a document with a deadline for signing:

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Limited Time Offer",
  "url_pdf": "https://example.com/offer.pdf",
  "date_limit_to_sign": "2025-12-31T23:59:59Z",
  "signers": [
    {
      "name": "Customer",
      "email": "customer@example.com"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, date_limit_to_sign}'
```

---

### 6. Get Document Details

Retrieve document status and signer information. Replace `<your-document-token>` with the actual document token:

```bash
bash -c 'curl -s -X GET "https://sandbox.api.zapsign.com.br/api/v1/docs/<your-document-token>/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}"' | jq '{name, status, original_file, signed_file, signers: [.signers[] | {name, status, signed_at}]}''
```

---

### 7. Add Signer to Existing Document

Add a new signer to an existing document. Replace `<your-document-token>` with the actual document token:

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Additional Signer",
  "email": "additional@example.com",
  "auth_mode": "assinaturaTela",
  "send_automatic_email": true
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/<your-document-token>/add-signer/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, sign_url, status}'
```

---

### 8. Create Document with WhatsApp Notification

Send signing link via WhatsApp (costs credits):

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "Contract via WhatsApp",
  "url_pdf": "https://example.com/contract.pdf",
  "signers": [
    {
      "name": "Mobile User",
      "phone_country": "1",
      "phone_number": "5551234567",
      "send_automatic_whatsapp": true,
      "auth_mode": "tokenWhatsapp"
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, signers}'
```

---

### 9. Create Document with Biometric Verification

Require facial recognition during signing:

Write to `/tmp/zapsign_request.json`:

```json
{
  "name": "High Security Contract",
  "url_pdf": "https://example.com/contract.pdf",
  "signers": [
    {
      "name": "Verified Signer",
      "email": "verified@example.com",
      "selfie_validation_type": "liveness-document-match",
      "require_document_photo": true
    }
  ]
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://sandbox.api.zapsign.com.br/api/v1/docs/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}" -H "Content-Type: application/json" -d @/tmp/zapsign_request.json' | jq '{token, status, signers: [.signers[] | {name, selfie_validation_type}]}''
```

---

### 10. Delete a Document

Delete a document. Replace `<your-document-token>` with the actual document token:

```bash
bash -c 'curl -s -X DELETE "https://sandbox.api.zapsign.com.br/api/v1/docs/<your-document-token>/" -H "Authorization: Bearer ${ZAPSIGN_API_TOKEN}"'
```

---

## Authentication Modes

| Mode | Description | Cost |
|------|-------------|------|
| `assinaturaTela` | On-screen signature (default) | Free |
| `tokenEmail` | Email verification token | Free |
| `assinaturaTela-tokenEmail` | Signature + email token | Free |
| `tokenSms` | SMS verification token | Free |
| `assinaturaTela-tokenSms` | Signature + SMS token | Free |
| `tokenWhatsapp` | WhatsApp verification token | $0.10 |
| `assinaturaTela-tokenWhatsapp` | Signature + WhatsApp token | $0.10 |

---

## Biometric Validation Types

| Type | Description | Cost |
|------|-------------|------|
| `liveness-document-match` | Face + document match | $0.50 |
| `identity-verification` | Full identity verification (CO, MX, CL, PE) | $1.00 |
| `identity-verification-global` | Global identity verification | $0.90 |

---

## Document Status

| Status | Description |
|--------|-------------|
| `pending` | Document is awaiting signatures |
| `signed` | All signers have signed |

## Signer Status

| Status | Description |
|--------|-------------|
| `new` | Signer created, hasn't viewed |
| `link-opened` | Signer opened the link |
| `signed` | Signer completed signing |

---

## Response Fields

| Field | Description |
|-------|-------------|
| `token` | Document unique identifier |
| `status` | Document status (pending/signed) |
| `original_file` | URL to original PDF (expires in 60 min) |
| `signed_file` | URL to signed PDF (expires in 60 min) |
| `signers[].token` | Signer unique identifier |
| `signers[].sign_url` | Direct signing link for signer |
| `signers[].signed_at` | Timestamp when signer signed |

---

## Guidelines

1. **Use Sandbox for testing**: Always test in sandbox first - it's free and has no legal validity
2. **Store tokens**: Save `token` and `signers[].token` for future API calls
3. **File URLs expire**: `original_file` and `signed_file` URLs expire in 60 minutes
4. **Use webhooks**: Instead of polling, set up webhooks for real-time notifications
5. **WhatsApp costs credits**: Each WhatsApp notification costs $0.10
6. **Biometrics cost credits**: Facial recognition and identity verification require credits
7. **Production requires plan**: Production environment requires an active API plan
