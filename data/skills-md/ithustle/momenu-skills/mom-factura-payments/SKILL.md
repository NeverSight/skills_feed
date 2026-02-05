---
name: mom-factura-payments
description: Integrate Mom Factura Payment API for Angolan payment methods (Multicaixa Express, E-kwanza, Bank Reference). Use when implementing checkout flows, processing payments, generating SAFT-AO compliant invoices, or handling product-based billing with IVA tax.
license: MIT
metadata:
  author: mom-factura
  version: "1.0"
  language: pt
---

# Mom Factura Payments Integration

Process payments for Angolan payment methods with automatic SAFT-AO invoice generation.

**Base URL:** `https://api.momenu.online`

## Authentication

All requests require the `x-api-key` header.

```
Content-Type: application/json
x-api-key: <MERCHANT_API_KEY>
```

Optional headers:
- `x-env-qa: true` - QA test environment (any origin)
- `x-dev-mode: true` - Bypass domain validation (localhost only)

## Payment Methods

### 1. Multicaixa Express (MCX) - Immediate

**POST** `/api/payment/mcx`

Immediate payment. Creates order as PAID and generates invoice on success.

Required body:
- `paymentInfo.amount` (number) - Kwanzas
- `paymentInfo.phoneNumber` (string) - Format: 244XXXXXXXXX

Optional body:
- `products` (array) - Items for detailed invoice
- `products[].id` (string), `products[].productName` (string), `products[].productPrice` (number), `products[].productQuantity` (number)
- `products[].iva` (number) - IVA rate 0-14, default 14
- `customer` (object) - `name` (string), `nif` (string), `phone` (string)
- `simulateResult` (string) - QA only: success, insufficient_balance, timeout, rejected, invalid_number

Success (200):
```json
{
  "success": true,
  "transactionId": "abc123...",
  "invoiceUrl": "https://invoice-momenu.toquemedia.net/invoices/..."
}
```

### 2. E-kwanza - Deferred

**POST** `/api/payment/ekwanza`

Deferred payment. Creates order as OPEN, returns QR code. Payment confirmation is delivered via webhook.

Required: `paymentInfo.amount`, `paymentInfo.phoneNumber`
Optional: `products`, `customer` (same as MCX)

Success (200):
```json
{
  "success": true,
  "code": "EKZ123456",
  "qrCode": "data:image/png;base64,...",
  "expirationDate": "2024-01-15T12:00:00Z",
  "paymentTimeout": 180
}
```

Payment confirmation arrives via webhook. Use `code` with status endpoint as fallback.

### 3. Bank Reference - Deferred

**POST** `/api/payment/reference`

Generates bank reference. Client pays via ATM or Internet Banking.

Required: `paymentInfo.amount`
Optional: `products`, `customer` (same as MCX)

Success (200):
```json
{
  "success": true,
  "operationId": "op-123...",
  "referenceNumber": "123456789",
  "entity": "12345",
  "dueDate": "2024-01-20"
}
```

## Amount Validation

If both `paymentInfo.amount` and `products` are provided, they must match:
- `total = SUM(productPrice * productQuantity)` for all products
- Mismatch returns error `AMOUNT_MISMATCH`
- Providing only one is valid (amount OR products)
- Providing neither returns `AMOUNT_MISMATCH`

## Webhook (Payment Confirmation)

All deferred payments (Bank Reference and E-kwanza) are confirmed via webhook. Configure the `webhook` URL in your `apiConfigs` document.

When a payment is confirmed, the API sends **two sequential events**:

**Event 1: `payment.confirmed`** — Sent immediately after order status is updated to PAID:
```json
{
  "event": "payment.confirmed",
  "merchantTransactionId": "abc123...",
  "ekwanzaTransactionId": "EKZ456...",
  "operationStatus": "1",
  "operationData": { ... }
}
```

**Event 2: `invoice.created`** — Sent after invoice PDF is generated and uploaded:
```json
{
  "event": "invoice.created",
  "merchantTransactionId": "abc123...",
  "ekwanzaTransactionId": "EKZ456...",
  "operationStatus": "1",
  "operationData": { ... },
  "invoiceUrl": "https://invoice-momenu.toquemedia.net/invoices/..."
}
```

Non-paid events (operationStatus 3, 4, 5) are sent without the `event` field for backward compatibility.

**operationStatus values:** `"1"` Paid · `"3"` Cancelled/Expired · `"4"` Failed/Refused · `"5"` Error

**Fallback (status endpoints):**

**E-kwanza:** GET `/api/payment/ekwanza/status/:code` - Returns `status: "paid"` or `"pending"`
**Reference:** GET `/api/payment/reference/status/:operationId` - Returns `payment.status`

When paid, both return `invoiceUrl`.

## Error Codes

| Code | Description |
|------|-------------|
| MISSING_API_KEY | x-api-key header missing |
| INVALID_API_KEY | Key invalid or inactive |
| DOMAIN_NOT_ALLOWED | Origin not registered |
| INVALID_AMOUNT | Invalid amount |
| AMOUNT_MISMATCH | amount != SUM(products) |
| MISSING_PHONE | Phone required (MCX/E-kwanza) |
| MISSING_RESTAURANT_ID | Merchant not identified |
| RATE_LIMIT_EXCEEDED | 100 req/min exceeded |
| PAYMENT_RATE_LIMIT_EXCEEDED | 20 payment req/min exceeded |
| INTERNAL_ERROR | Server error |

Error format: `{ "success": false, "error": "message", "code": "ERROR_CODE" }`

## Fees

2% processing fee on all payments: `feeAmount = totalAmount * 0.02`

## Notes

- Phone format: 244XXXXXXXXX (12 digits)
- IVA defaults to 14%. Use 0 for exempt.
- Invoice PDFs hosted on CDN, returned as `invoiceUrl`
- MCX is immediate; Reference and E-kwanza are confirmed via webhook (status polling as fallback)
