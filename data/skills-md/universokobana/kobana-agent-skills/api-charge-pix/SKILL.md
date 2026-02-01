---
name: api-charge-pix
description: Guide for managing Pix charges, accounts, and payments using Kobana API. Use when the user wants to create, list, update, or cancel Pix charges, manage Pix accounts, or handle charge payments.
license: Complete terms in LICENSE.txt
metadata:
  author: Kobana
  version: "2.0"
---

# Kobana Charge API Skill

Manage Pix charges, accounts, and payments via Kobana API.

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

### Pix Accounts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/charge/pix_accounts` | List all Pix accounts |
| POST | `/v2/charge/pix_accounts` | Create a new Pix account |
| GET | `/v2/charge/pix_accounts/{uid}` | Get a specific Pix account |
| PUT | `/v2/charge/pix_accounts/{uid}` | Update a Pix account |
| DELETE | `/v2/charge/pix_accounts/{uid}` | Delete a Pix account |

### Pix Charges
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/charge/pix` | List all Pix charges |
| POST | `/v2/charge/pix` | Create a new Pix charge |
| GET | `/v2/charge/pix/{uid}` | Get a specific Pix charge |
| PUT | `/v2/charge/pix/{uid}/update` | Update a Pix charge |
| DELETE | `/v2/charge/pix/{uid}` | Delete a Pix charge |
| POST | `/v2/charge/pix/{uid}/cancel` | Cancel a Pix charge |

### Pix Commands
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/charge/pix/{pix_uid}/commands` | List commands for a Pix charge |
| GET | `/v2/charge/pix/{pix_uid}/commands/{id}` | Get a specific command |

### Charge Payments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v2/charge/payments` | List all payments |
| POST | `/v2/charge/payments` | Create a new payment |
| GET | `/v2/charge/payments/{uid}` | Get a specific payment |
| DELETE | `/v2/charge/payments/{uid}` | Delete a payment |

## Creating a Pix Charge

### Minimum Required Parameters
```json
POST /v2/charge/pix

{
  "amount": 100.50,
  "pix_account_uid": "018df180-7208-727b-...",
  "expire_at": "2026-12-02T10:03:56-03:00"
}
```

### Complete Example (Billing Pix)
```json
POST /v2/charge/pix

{
  "amount": 500.00,
  "pix_account_uid": "018df180-7208-727b-...",
  "expire_at": "2026-02-10T23:59:59-03:00",
  "registration_kind": "billing",
  "payer": {
    "document_number": "12.345.678/0001-90",
    "name": "Company LTDA",
    "email": "finance@company.com"
  },
  "fine_type": "percentage",
  "fine_percentage": 2.0,
  "interest_type": "monthly_percentage_calendar",
  "interest_percentage": 1.0,
  "discount_type": "advance_percentage_calendar",
  "discount_first_percentage": 5.0,
  "discount_first_days": 5,
  "revoke_days": 30,
  "external_id": "invoice_2026_001",
  "tags": ["monthly", "subscription"],
  "message": "Invoice January/2026"
}
```

## Pix Types

### Instant Pix (`registration_kind: "instant"`)
- Short expiration (minutes to hours)
- No interest, fines, or discounts
- Use for: e-commerce, delivery, point-of-sale

### Billing Pix (`registration_kind: "billing"`)
- Formal due date
- Supports interest, fines, discounts
- Stays active after due date (if `revoke_days` set)
- Use for: monthly invoices, subscriptions

## Important: Asynchronous Behavior

The QR Code is **NOT** returned in the initial response. Options:

1. **Poll the charge** - GET `/v2/charge/pix/{uid}` until `registration_status` is `confirmed`
2. **Use webhooks** - Configure webhook for `pix.register.confirmed` event

## Listing and Filtering

### List Pix Charges with Filters
```
GET /v2/charge/pix?status=opened&created_from=2026-01-01&per_page=50
```

| Parameter | Description |
|-----------|-------------|
| `status` | Filter by status (opened, paid, overdue, canceled) |
| `registration_status` | Filter by registration status |
| `pix_account_uid` | Filter by Pix account |
| `created_from` / `created_to` | Filter by creation date |
| `expire_from` / `expire_to` | Filter by expiration date |
| `paid_from` / `paid_to` | Filter by payment date |
| `txid` | Filter by TXID |
| `external_id` | Filter by external ID |
| `tags` | Filter by tags |
| `page` / `per_page` | Pagination |

### List Pix Accounts
```
GET /v2/charge/pix_accounts
```

## Updating and Canceling

### Update a Pix Charge
```json
PUT /v2/charge/pix/{uid}/update

{
  "amount": 550.00,
  "expire_at": "2026-02-15T23:59:59-03:00"
}
```

### Cancel a Pix Charge
```
POST /v2/charge/pix/{uid}/cancel
```

## Status Reference

### Charge Status
- `opened` - Open (initial)
- `paid` - Paid
- `overdue` - Overdue
- `canceled` - Canceled
- `generation_failed` - Registration failed

### Registration Status
- `pending` - Waiting
- `confirmed` - Ready (has QR Code)
- `rejected` / `failed` - Error

## Common Parameters

### Fine (after due date)
```json
{
  "fine_type": "percentage",  // or "amount"
  "fine_percentage": 2.0
}
```

### Interest
```json
{
  "interest_type": "monthly_percentage_calendar",
  "interest_percentage": 1.0
}
```

Interest types: `daily_amount_calendar`, `daily_percentage_calendar`, `monthly_percentage_calendar`, `yearly_percentage_calendar`, `daily_amount_business`, `daily_percentage_business`, `monthly_percentage_business`, `yearly_percentage_business`

### Discount
```json
{
  "discount_type": "advance_percentage_calendar",
  "discount_first_percentage": 5.0,
  "discount_first_days": 5
}
```

### Days Active After Due Date
```json
{
  "revoke_days": 30
}
```
**Required** when using interest or fines.

## Best Practices

1. **Poll or use webhooks** - QR Code comes asynchronously
2. **Use external_id** - Track charges in your system
3. **Set revoke_days** - Required for interest/fines
4. **Validate CPF/CNPJ** - Before sending to API
5. **Use X-Idempotency-Key header** - Prevent duplicates
6. **Test in sandbox** - Before production

## Reference Documentation

See [references/REFERENCE.md](references/REFERENCE.md) for complete API documentation including all parameters, response formats, and error codes.
