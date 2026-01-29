---
name: fakturoid
description: Czech invoicing API integration for Fakturoid. Use when the user needs to create, manage, or retrieve invoices, contacts/subjects, or expenses from Fakturoid. Supports OAuth 2.0 authentication, invoice creation with Czech tax compliance (IČO, DIČ, VAT), PDF downloads, payment tracking, expense management, inventory, recurring invoices, webhooks, and invoice templates (generators). Triggers on mentions of Fakturoid, Czech invoicing, IČO/DIČ, or invoice management tasks.
---

# Fakturoid API v3

Czech invoicing service API integration - comprehensive reference for building integrations.

## Quick Start

### Environment Setup
```bash
export FAKTUROID_CLIENT_ID="your-client-id"
export FAKTUROID_CLIENT_SECRET="your-client-secret"
export FAKTUROID_ACCOUNT_SLUG="your-account-slug"
```

### Authenticate
```bash
python scripts/auth.py credentials --save
```

### Create Invoice
```bash
python scripts/invoice.py create --subject-id 123 --lines '[
  {"name": "Consulting", "quantity": 8, "unit_name": "hours", "unit_price": 2000, "vat_rate": 21}
]'
```

---

## API Basics

| Setting | Value |
|---------|-------|
| **Base URL** | `https://app.fakturoid.cz/api/v3` |
| **Account URL** | `https://app.fakturoid.cz/api/v3/accounts/{slug}` |
| **Auth** | OAuth 2.0 (Client Credentials or Authorization Code) |
| **Pagination** | 40 records per page |
| **Rate Limit** | 400 requests per 60 seconds |

### Required Headers

```http
User-Agent: YourAppName (your@email.com)
Authorization: Bearer {access_token}
Content-Type: application/json
Accept: application/json
```

---

## Scripts Reference

### Core Scripts

| Script | Commands | Description |
|--------|----------|-------------|
| `auth.py` | credentials, refresh, revoke, status | OAuth token management |
| `subject.py` | list, get, search, create, update, delete, lookup-ico | Contact management |
| `invoice.py` | list, get, search, create, update, delete, action, pdf, pay, pay-delete | Invoice operations |
| `expense.py` | list, get, search, create, update, delete, action, pay, pay-delete | Expense tracking |
| `generator.py` | list, get, create, update, delete | Invoice templates |

### Additional Scripts

| Script | Commands | Description |
|--------|----------|-------------|
| `user.py` | get, list | User and account info |
| `bank_account.py` | list | Bank account listing |
| `inventory.py` | list-items, get-item, create-item, list-moves, create-move | Inventory management |
| `recurring.py` | list, get, create, update, delete, pause, activate | Recurring invoices |
| `inbox.py` | list, upload, send-to-ocr, download, delete | OCR file processing |
| `event.py` | list, list-paid | Activity log |
| `todo.py` | list, toggle | Task management |
| `message.py` | send | Send invoice emails |
| `webhook.py` | list, get, create, update, delete | Webhook management |

---

## Common Workflows

### Create Invoice for New Customer
```bash
# 1. Create subject
python scripts/subject.py create --name "Acme s.r.o." --ico 12345678 --dic CZ12345678

# 2. Create invoice (use returned subject ID)
python scripts/invoice.py create --subject-id 456 --lines '[
  {"name": "Web development", "quantity": 40, "unit_name": "hours", "unit_price": 1500, "vat_rate": 21}
]'

# 3. Mark as sent and download PDF
python scripts/invoice.py action 789 mark_as_sent
python scripts/invoice.py pdf 789 --output invoice.pdf
```

### Record Expense from Supplier
```bash
# 1. Ensure supplier exists
python scripts/subject.py create --name "Supplier Ltd" --type supplier --ico 87654321

# 2. Create expense
python scripts/expense.py create --subject-id 321 --original-number "FV-2024-0456" --lines '[
  {"name": "Office supplies", "quantity": 10, "unit_name": "ks", "unit_price": 450, "vat_rate": 21}
]'
```

### Setup Monthly Recurring Invoice
```bash
python scripts/recurring.py create --name "Monthly Hosting" --subject-id 123 \
  --start-date 2024-02-01 --months-period 1 --send-email \
  --lines '[{"name": "Web hosting - {MMMM} {YYYY}", "unit_price": 500, "vat_rate": 21}]'
```

### Process Inbox File with OCR
```bash
# Upload and send to OCR
python scripts/inbox.py upload invoice.pdf --send-to-ocr

# Check status
python scripts/inbox.py list
```

---

## Enums Reference

### Document Types

| Value | Czech | Description |
|-------|-------|-------------|
| `invoice` | Faktura | Standard invoice |
| `proforma` | Zálohová faktura | Advance payment request |
| `partial_proforma` | Částečná záloha | Legacy partial advance |
| `correction` | Dobropis | Credit note |
| `tax_document` | Daňový doklad | Tax receipt for proforma payment |
| `final_invoice` | Vyúčtovací faktura | Final invoice from tax documents |

### Invoice Status

| Value | Description |
|-------|-------------|
| `open` | New, unpaid, not sent |
| `sent` | Sent to client, not overdue |
| `overdue` | Past due date |
| `paid` | Fully paid |
| `cancelled` | Cancelled (VAT payers only) |
| `uncollectible` | Marked as bad debt |

### Expense Status

| Value | Description |
|-------|-------------|
| `open` | Received, not paid |
| `overdue` | Past due date |
| `paid` | Fully paid |

### VAT Modes

| Value | Czech | Description |
|-------|-------|-------------|
| `vat_payer` | Plátce DPH | Standard VAT payer |
| `non_vat_payer` | Neplátce DPH | Non-VAT payer |
| `identified_person` | Identifikovaná osoba | EU VAT identified person |

### VAT Price Modes

| Value | Description |
|-------|-------------|
| `without_vat` | Prices entered without VAT |
| `from_total_with_vat` | Calculate VAT from total with VAT |

### VAT Rates

| Value | Rate | Description |
|-------|------|-------------|
| `standard` | 21% | Standard rate |
| `reduced` | 12% | First reduced rate |
| `reduced2` | 10% | Second reduced rate |
| `zero` | 0% | Zero VAT |

### Payment Methods

| Value | Description |
|-------|-------------|
| `bank` | Bank transfer |
| `cash` | Cash payment |
| `cod` | Cash on delivery |
| `card` | Card payment |
| `paypal` | PayPal |
| `custom` | Custom (see `custom_payment_method`) |

### Languages

| Value | Language |
|-------|----------|
| `cz` | Czech |
| `sk` | Slovak |
| `en` | English |
| `de` | German |
| `fr` | French |
| `it` | Italian |
| `es` | Spanish |
| `ru` | Russian |
| `pl` | Polish |
| `hu` | Hungarian |
| `ro` | Romanian |

### Subject Types

| Value | Description |
|-------|-------------|
| `customer` | Customer only |
| `supplier` | Supplier only |
| `both` | Both customer and supplier |

### Invoice Actions

| Action | Description |
|--------|-------------|
| `mark_as_sent` | Mark invoice as sent |
| `cancel` | Cancel invoice |
| `undo_cancel` | Revert cancellation |
| `lock` | Lock from editing |
| `unlock` | Unlock for editing |
| `mark_as_uncollectible` | Mark as bad debt |
| `undo_uncollectible` | Revert uncollectible |

### Expense Actions

| Action | Description |
|--------|-------------|
| `lock` | Lock from editing |
| `unlock` | Unlock for editing |

### OSS Modes (EU One Stop Shop)

| Value | Description |
|-------|-------------|
| `disabled` | OSS disabled |
| `service` | OSS for services |
| `goods` | OSS for goods |

### Proforma Followup Documents

| Value | Description |
|-------|-------------|
| `final_invoice_paid` | Auto-create paid invoice |
| `final_invoice` | Manual invoice creation |
| `tax_document` | Auto-create tax document |
| `none` | No followup document |

### OCR Status

| Value | Description |
|-------|-------------|
| `created` | OCR requested |
| `processing` | OCR in progress |
| `processing_failed` | OCR failed |
| `processing_rejected` | File rejected |
| `processed` | Successfully processed |

---

## Czech-Specific Fields

| API Field | Czech | Example |
|-----------|-------|---------|
| `registration_no` | IČO | `12345678` |
| `vat_no` | DIČ | `CZ12345678` |
| `local_vat_no` | SK DIČ | `1234567890` |
| `taxable_fulfillment_due` | DUZP | `2024-01-15` |
| `transferred_tax_liability` | Přenesená daňová povinnost | `true` |
| `supply_code` | Kód předmětu plnění | `4` |

---

## Line Item Structure

```json
{
  "name": "Service description",
  "quantity": 10,
  "unit_name": "hours",
  "unit_price": 1500,
  "vat_rate": 21,
  "inventory_item_id": 123,
  "sku": "PROD-001"
}
```

### Line Operations

| Operation | Method |
|-----------|--------|
| Add line | Omit `id` |
| Update line | Include `id` |
| Delete line | Include `id` and `_destroy: true` |

---

## References

### Core Documentation
- [api-reference.md](references/api-reference.md) - Complete endpoint catalog
- [authentication.md](references/authentication.md) - OAuth 2.0 guide with code examples
- [error-handling.md](references/error-handling.md) - Error codes and handling

### Resource Documentation
- [invoices.md](references/invoices.md) - Invoice management
- [invoice-payments.md](references/invoice-payments.md) - Payment operations
- [invoice-messages.md](references/invoice-messages.md) - Email sending
- [subjects.md](references/subjects.md) - Contact management
- [expenses.md](references/expenses.md) - Expense tracking
- [expense-payments.md](references/expense-payments.md) - Expense payments
- [generators.md](references/generators.md) - Invoice templates
- [recurring-generators.md](references/recurring-generators.md) - Automated invoicing
- [inventory.md](references/inventory.md) - Stock management
- [webhooks.md](references/webhooks.md) - Event notifications

### Additional Resources
- [users.md](references/users.md) - User and account info
- [account.md](references/account.md) - Account settings
- [bank-accounts.md](references/bank-accounts.md) - Bank accounts
- [number-formats.md](references/number-formats.md) - Invoice numbering
- [inbox-files.md](references/inbox-files.md) - OCR processing
- [events.md](references/events.md) - Activity log
- [todos.md](references/todos.md) - Task management
- [czech-invoicing.md](references/czech-invoicing.md) - Czech tax compliance

---

## Error Handling

| Status | Meaning | Action |
|--------|---------|--------|
| 400 | Bad Request | Check date formats, User-Agent header |
| 401 | Unauthorized | Refresh OAuth token |
| 402 | Payment Required | Fakturoid account blocked |
| 403 | Forbidden | Permission denied, resource limits |
| 404 | Not Found | Resource doesn't exist |
| 422 | Validation Error | Check `errors` field for details |
| 429 | Rate Limited | Wait for `X-RateLimit` reset |
| 503 | Unavailable | Maintenance, retry later |

---

## Token Management

```bash
# Get new token
python scripts/auth.py credentials --save

# Check token status
python scripts/auth.py status

# Refresh expired token (Authorization Code flow)
python scripts/auth.py refresh

# Revoke token
python scripts/auth.py revoke
```

Token file: `~/.fakturoid/token.json`

---

## Rate Limiting

Headers on every response:
```http
X-RateLimit-Policy: default;q=400;w=60
X-RateLimit: default;r=398;t=55
```

- `q=400`: Max 400 requests
- `w=60`: Per 60 seconds window
- `r=398`: Remaining requests
- `t=55`: Seconds until reset

When exceeded: `429 Too Many Requests` - wait for reset.
