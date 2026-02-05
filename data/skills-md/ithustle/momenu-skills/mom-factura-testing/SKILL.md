---
name: mom-factura-testing
description: Test and debug Mom Factura Payment API integrations using QA environment and payment simulation. Use when setting up test environments, simulating payment outcomes (success, failure, timeout), debugging API errors, or validating integration before production.
license: MIT
metadata:
  author: mom-factura
  version: "1.0"
  language: pt
---

# Mom Factura Testing & QA

Test payment integrations without processing real transactions.

**Base URL:** `https://api.momenu.online`

## Enable QA Mode

Add header `x-env-qa: true` to use the test environment. Works from any origin.

For local development, also add `x-dev-mode: true` (localhost/127.0.0.1 only).

```
Content-Type: application/json
x-api-key: YOUR_API_KEY
x-env-qa: true
x-dev-mode: true
```

## Simulate Payment Results

The `simulateResult` field in the MCX endpoint body triggers specific scenarios. Only active when `x-env-qa: true`.

| Value | Behavior |
|-------|----------|
| `success` | Payment succeeds, returns transactionId and invoiceUrl |
| `insufficient_balance` | Fails: client has no balance |
| `timeout` | Fails: no response from provider |
| `rejected` | Fails: payment explicitly rejected |
| `invalid_number` | Fails: phone not registered |

Internal test phone mapping (automatic, no action needed):
- success → 244900000000
- insufficient_balance → 244900000001
- timeout → 244900000002
- rejected → 244900000003
- invalid_number → 244999999999

## Test Examples

### Successful MCX Payment

```bash
curl -X POST https://api.momenu.online/api/payment/mcx \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "x-env-qa: true" \
  -d '{"paymentInfo":{"amount":1000,"phoneNumber":"244923456789"},"simulateResult":"success"}'
```

### Insufficient Balance

```bash
curl -X POST https://api.momenu.online/api/payment/mcx \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "x-env-qa: true" \
  -d '{"paymentInfo":{"amount":5000,"phoneNumber":"244923456789"},"simulateResult":"insufficient_balance"}'
```

### Amount Validation Error

```bash
curl -X POST https://api.momenu.online/api/payment/mcx \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "x-env-qa: true" \
  -d '{"paymentInfo":{"amount":2500,"phoneNumber":"244923456789"},"products":[{"id":"1","productName":"P","productPrice":3000,"productQuantity":1}],"simulateResult":"success"}'
```

Returns: `{ "success": false, "code": "AMOUNT_MISMATCH" }`

### E-kwanza in QA (no simulateResult support)

```bash
curl -X POST https://api.momenu.online/api/payment/ekwanza \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "x-env-qa: true" \
  -d '{"paymentInfo":{"amount":2000,"phoneNumber":"244923456789"}}'
```

### Reference in QA

```bash
curl -X POST https://api.momenu.online/api/payment/reference \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -H "x-env-qa: true" \
  -d '{"paymentInfo":{"amount":10000}}'
```

## Test Helpers

### JavaScript

```javascript
const API = "https://api.momenu.online";
const headers = {
  "Content-Type": "application/json",
  "x-api-key": "YOUR_API_KEY",
  "x-env-qa": "true"
};

async function testMCX(simulateResult = "success") {
  const res = await fetch(`${API}/api/payment/mcx`, {
    method: "POST", headers,
    body: JSON.stringify({
      paymentInfo: { amount: 1000, phoneNumber: "244923456789" },
      simulateResult
    })
  });
  return res.json();
}

// Run all scenarios
for (const s of ["success","insufficient_balance","timeout","rejected","invalid_number"]) {
  testMCX(s).then(r => console.log(s, r.success ? "PASS" : "FAIL", r));
}
```

### Python

```python
import requests

API = "https://api.momenu.online"
headers = {"Content-Type": "application/json", "x-api-key": "YOUR_API_KEY", "x-env-qa": "true"}

def test_mcx(simulate="success"):
    r = requests.post(f"{API}/api/payment/mcx", json={
        "paymentInfo": {"amount": 1000, "phoneNumber": "244923456789"},
        "simulateResult": simulate
    }, headers=headers)
    return r.json()

for s in ["success", "insufficient_balance", "timeout", "rejected", "invalid_number"]:
    result = test_mcx(s)
    print(f"{s}: {'PASS' if result.get('success') else 'FAIL'} - {result}")
```

## Common Issues

| Error | Cause | Fix |
|-------|-------|-----|
| DOMAIN_NOT_ALLOWED | Origin not registered | Add `x-dev-mode: true` (localhost) or register domain |
| MISSING_API_KEY | Header missing | Check header is `x-api-key` (lowercase, hyphens) |
| AMOUNT_MISMATCH | amount != products total | Verify SUM(price*qty) == amount, or send only one |
| MISSING_PHONE | No phone for MCX/E-kwanza | Add `paymentInfo.phoneNumber` (not needed for Reference) |
| simulateResult ignored | Not in QA mode | Add header `x-env-qa: true` |
| simulateResult ignored | Wrong endpoint | Only works on MCX, not E-kwanza or Reference |

## Pre-Production Checklist

1. Remove `x-env-qa: true` header
2. Remove `x-dev-mode: true` header
3. Remove `simulateResult` from request bodies
4. Register production domain in merchant panel
5. Store API key in environment variables (never hardcode)
6. Implement error handling for all error codes
7. Implement webhook endpoint to receive payment confirmations
8. Implement status endpoint fallback for E-kwanza and Reference
9. Verify amount validation with products
10. Test with real phone numbers
