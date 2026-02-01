---
name: api-transfer-pix
description: Guide for managing Pix transfers using Kobana API. Use when the user wants to create, list, get, or cancel Pix transfers, manage transfer batches, or handle financial accounts.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "1.0"
---

# Kobana Transfer API Skill

Manage Pix transfers, batches, and financial accounts via Kobana API.

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

### Pix Transfers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/transfer/pix` | List all Pix transfers |
| POST | `/v2/transfer/pix` | Create a new Pix transfer |
| GET | `/v2/transfer/pix/{uid}` | Get a specific Pix transfer |
| PUT | `/v2/transfer/pix/{uid}/cancel` | Cancel a Pix transfer |

### Pix Transfer Batches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/transfer/batches` | List all transfer batches |
| POST | `/v2/transfer/pix_batches` | Create a new Pix transfer batch |
| GET | `/v2/transfer/batches/{uid}` | Get a specific batch |
| PUT | `/v2/transfer/batches/{uid}/approve` | Approve a batch |
| PUT | `/v2/transfer/batches/{uid}/reprove` | Reprove a batch |

## Creating a Pix Transfer

### Transfer by Pix Key (Minimum Required)
```json
POST /v2/transfer/pix

{
  "amount": 100.50,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "key",
  "key_type": "email",
  "key": "recipient@example.com",
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  }
}
```

### Transfer by Bank Account
```json
POST /v2/transfer/pix

{
  "amount": 500.00,
  "financial_account_uid": "018df180-7208-727b-...",
  "type": "bank_account",
  "beneficiary": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA"
  },
  "bank_account": {
    "compe_number": 341,
    "agency_number": "1234",
    "agency_digit": "5",
    "account_number": "12345",
    "account_digit": "6",
    "document_number": "12.345.678/0001-90"
  },
  "scheduled_to": "2026-02-01",
  "transfer_purpose": "98",
  "external_id": "payment_2026_001",
  "tags": ["monthly", "supplier"],
  "custom_data": {
    "invoice": "INV-2026-001"
  }
}
```

## Transfer Types

### By Pix Key (`type: "key"`)
- Requires `key_type` and `key` fields
- Key types: `cpf`, `cnpj`, `email`, `phone`, `random`
- Use for: Quick transfers when recipient's key is known

### By Bank Account (`type: "bank_account"`)
- Requires `bank_account` object with account details
- Use for: Transfers when only bank account data is available

## Important: Two-Step Flow

Pix transfers require a two-step process:

1. **Create Transfer** - `POST /v2/transfer/pix` creates a pending transfer
2. **Create Batch** - `POST /v2/transfer/pix_batches` sends transfers to the bank

### Creating a Batch
```json
POST /v2/transfer/pix_batches

{
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    { "uid": "019c0cbe-f018-717e-..." }
  ]
}
```

Or create transfers directly in the batch:
```json
POST /v2/transfer/pix_batches

{
  "financial_account_uid": "018df180-7208-727b-...",
  "transfers": [
    {
      "amount": 100.50,
      "type": "key",
      "key_type": "email",
      "key": "recipient@example.com",
      "beneficiary": {
        "document_number": "12.345.678/0001-90",
        "name": "Company LTDA"
      }
    }
  ]
}
```

## Batch Approval Workflow

Some financial accounts require manual approval:

1. **Batch created** - Status: `pending` or `awaiting_approval`
2. **Approve** - `PUT /v2/transfer/batches/{uid}/approve`
3. **Or Reprove** - `PUT /v2/transfer/batches/{uid}/reprove`

## Listing and Filtering

### List Pix Transfers
```
GET /v2/transfer/pix?status=pending&per_page=50
```

| Parameter | Description |
|-----------|-------------|
| `status` | Filter by status (pending, confirmed, rejected) |
| `registration_status` | Filter by registration status |
| `financial_account_uid` | Filter by financial account |
| `page` / `per_page` | Pagination |

### List Transfer Batches
```
GET /v2/transfer/batches?per_page=50
```

## Canceling a Transfer

```
PUT /v2/transfer/pix/{uid}/cancel
```

Only pending transfers can be canceled. This is processed asynchronously.

## Status Reference

### Transfer Status
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
- `confirmed` - All transfers confirmed
- `reproved` - Reproved

## Transfer Purpose Codes

| Code | Description |
|------|-------------|
| `20` | Supplier Payment |
| `30` | Salary Payment |
| `32` | Fees Payment |
| `90` | Benefits Payment |
| `98` | Miscellaneous Payments (default) |

## Key Types

| Type | Description | Example |
|------|-------------|---------|
| `cpf` | CPF number | `111.222.333-44` |
| `cnpj` | CNPJ number | `11.222.333/0001-44` |
| `email` | Email address | `user@example.com` |
| `phone` | Phone number | `+5511999999999` |
| `random` | Random key (EVP) | `123e4567-e89b-12d3-...` |

## Best Practices

1. **Use batches for multiple transfers** - More efficient than individual transfers
2. **Set external_id** - Track transfers in your system
3. **Schedule transfers** - Use `scheduled_to` for future-dated transfers
4. **Use X-Idempotency-Key header** - Prevent duplicates
5. **Test in sandbox** - Before production
6. **Monitor batch status** - Poll or use webhooks for status updates

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete API documentation including all parameters, response formats, and error codes.
