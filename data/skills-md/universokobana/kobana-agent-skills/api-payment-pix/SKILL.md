---
name: api-payment-pix
description: Guide for paying Pix charges using Kobana API. Use when the user wants to pay Pix invoices, decode QR codes, or manage Pix payments from financial accounts.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "1.0"
---

# Kobana Payment API Skill

Pay Pix charges, decode QR codes, and manage Pix payments via Kobana API.

## Base URLs

```
Production: https://api.kobana.com.br
Sandbox:    https://api-sandbox.kobana.com.br
```

## Authentication

```
Authorization: Bearer {your_api_token}
```

## API Endpoints Overview

### Pix Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/payment/pix` | List all Pix payments |
| POST | `/v2/payment/pix` | Create a new Pix payment |
| GET | `/v2/payment/pix/{uid}` | Get a specific Pix payment |
| PUT | `/v2/payment/pix/{uid}/cancel` | Cancel a Pix payment |

### Pix Decoding
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/v2/payment/pix/decode` | Decode a Pix EMV (QR code/copy-paste) |

### Payment Batches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/payment/batches` | List all payment batches |
| POST | `/v2/payment/pix_batches` | Create a Pix payment batch |
| GET | `/v2/payment/batches/{uid}` | Get a specific batch |
| PUT | `/v2/payment/batches/{uid}/approve` | Approve a batch |
| PUT | `/v2/payment/batches/{uid}/reprove` | Reprove a batch |

## Paying a Pix Charge

### Step 1: Decode the Pix EMV (Optional but Recommended)

Before paying, decode the QR code to validate the charge data:

```json
POST /v2/payment/pix/decode

{
  "emv": "00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000..."
}
```

**Response:**
```json
{
  "status": 200,
  "data": {
    "type": "static",
    "key": "recipient@example.com",
    "key_type": "email",
    "merchant_name": "Company LTDA",
    "merchant_city": "São Paulo",
    "amount": 150.00,
    "txid": "PAYMENT123456",
    "description": "Invoice January 2026"
  }
}
```

### Step 2: Create the Payment

**By EMV (QR Code/Copy-Paste):**
```json
POST /v2/payment/pix

{
  "financial_account_uid": "018df180-7208-727b-...",
  "emv": "00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000...",
  "amount": 150.00,
  "scheduled_to": "2026-01-31",
  "external_id": "payment_001"
}
```

**By Pix Key (Static Pix):**
```json
POST /v2/payment/pix

{
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "key",
  "key_type": "email",
  "key": "recipient@example.com",
  "amount": 150.00,
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "external_id": "payment_001"
}
```

## Payment Types

### By EMV (Dynamic Pix)
- Use when you have a QR code or copy-paste string
- Amount may be fixed by the charge
- Most common for invoices and bills

### By Pix Key (Static Pix)
- Use when paying directly to a Pix key
- You define the amount
- Use for donations, tips, or manual payments

## Important: Two-Step Flow

Pix payments require a two-step process:

1. **Create Payment** - `POST /v2/payment/pix` creates a pending payment
2. **Create Batch** - `POST /v2/payment/pix_batches` sends payments to the bank

### Creating a Batch
```json
POST /v2/payment/pix_batches

{
  "financial_account_uid": "018df180-7208-727b-...",
  "payments": [
    { "uid": "019c0cbe-f018-717e-..." }
  ]
}
```

Or create payments directly in the batch:
```json
POST /v2/payment/pix_batches

{
  "financial_account_uid": "018df180-7208-727b-...",
  "payments": [
    {
      "emv": "00020126580014br.gov.bcb.pix...",
      "amount": 150.00
    }
  ]
}
```

## Batch Approval Workflow

Some financial accounts require manual approval:

1. **Batch created** - Status: `pending` or `awaiting_approval`
2. **Approve** - `PUT /v2/payment/batches/{uid}/approve`
3. **Or Reprove** - `PUT /v2/payment/batches/{uid}/reprove`

## Listing and Filtering

### List Pix Payments
```
GET /v2/payment/pix?status=pending&per_page=50
```

| Parameter | Description |
|-----------|-------------|
| `status` | Filter by status (pending, confirmed, rejected) |
| `registration_status` | Filter by registration status |
| `financial_account_uid` | Filter by financial account |
| `created_from` / `created_to` | Filter by creation date |
| `page` / `per_page` | Pagination |

### List Payment Batches
```
GET /v2/payment/batches?per_page=50
```

## Canceling a Payment

```
PUT /v2/payment/pix/{uid}/cancel
```

Only pending payments can be canceled. This is processed asynchronously.

## Status Reference

### Payment Status
- `pending` - Pending (initial)
- `awaiting_approval` - Awaiting approval
- `approved` - Approved
- `confirmed` - Confirmed by bank
- `rejected` - Rejected by bank
- `reproved` - Reproved (canceled before sending)

### Registration Status
- `pending` - Waiting for registration
- `requested` - Sent to bank
- `confirmed` - Confirmed at bank
- `rejected` - Rejected by bank
- `failed` - Registration failed

### Batch Status
- `pending` - Pending (initial)
- `awaiting_approval` - Awaiting approval
- `approved` - Approved
- `confirmed` - All payments confirmed
- `reproved` - Reproved

## Pix Types

| Type | Description |
|------|-------------|
| `static` | Static Pix - Fixed key, variable amount |
| `dynamic` | Dynamic Pix - Generated for specific charge with fixed amount |
| `dynamic_due_date` | Dynamic Pix with due date (Pix Cobrança) |

## Key Types

| Type | Description | Example |
|------|-------------|---------|
| `cpf` | CPF number | `111.222.333-44` |
| `cnpj` | CNPJ number | `11.222.333/0001-44` |
| `email` | Email address | `user@example.com` |
| `phone` | Phone number | `+5511999999999` |
| `random` | Random key (EVP) | `123e4567-e89b-12d3-...` |

## Best Practices

1. **Decode before paying** - Validate the charge data before creating payment
2. **Use batches for multiple payments** - More efficient than individual payments
3. **Set external_id** - Track payments in your system
4. **Schedule payments** - Use `scheduled_to` for future-dated payments
5. **Use X-Idempotency-Key header** - Prevent duplicates
6. **Test in sandbox** - Before production
7. **Monitor batch status** - Poll or use webhooks for status updates

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete API documentation including all parameters, response formats, and error codes.
