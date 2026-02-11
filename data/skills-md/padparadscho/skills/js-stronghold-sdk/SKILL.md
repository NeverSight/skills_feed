---
name: js-stronghold-sdk
description: Guide for integrating and building with the Stronghold Pay JS SDK and REST API for payment processing. Use when working with Stronghold Pay payment integration, accepting ACH/bank debit payments, linking bank accounts, creating charges/tips, generating PayLinks, or building checkout flows — in sandbox or live environments. Covers Stronghold.Pay.JS drop-in UI, REST API v2 endpoints, PayLink hosted payment pages, customer token management, and payment source handling.
---

# Stronghold Pay JS SDK & REST API

Stronghold Pay is a payment infrastructure platform enabling online and in-store payment acceptance via ACH/bank debit. Two integration paths exist:

1. **Stronghold.Pay.JS SDK** — Frontend drop-in UI components for payment source linking, charges, and tips
2. **REST API v2** — Server-side API for full control over customers, charges, payment sources, and PayLinks

## Integration Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Frontend   │────▶│  Your Backend    │────▶│  Stronghold API  │
│  (Pay.JS)   │     │  (Secret Key)    │     │  api.stronghold  │
│             │     │                  │     │  pay.com         │
│ publishable │     │ SH-SECRET-KEY    │     │                  │
│ key only    │     │ header           │     │                  │
└─────────────┘     └──────────────────┘     └──────────────────┘
```

- **Frontend** uses the publishable key (`pk_sandbox_...` / `pk_live_...`) and customer tokens
- **Backend** uses the secret key (`sk_sandbox_...` / `sk_live_...`) via `SH-SECRET-KEY` header
- Customer tokens are generated server-side, passed to frontend, and expire after 12 hours

## Quick Start

### 1. Include the SDK

```html
<head>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://api.strongholdpay.com/v2/js"></script>
</head>
```

### 2. Initialize the client

```js
const strongholdPay = Stronghold.Pay({
  publishableKey: "pk_sandbox_...",
  environment: "sandbox", // 'sandbox' or 'live'
  integrationId: "integration_...",
});
```

### 3. Generate a customer token (server-side)

```bash
curl --request GET \
  --url https://api.strongholdpay.com/v2/customers/{customer_id}/token \
  --header 'SH-SECRET-KEY: sk_sandbox_...' \
  --header 'Accept: application/json'
```

Response:

```json
{
  "response_id": "resp_...",
  "time": "2024-01-15T12:00:00Z",
  "status_code": 200,
  "result": {
    "token": "<jwt>",
    "expiry": "2024-01-16T00:00:00Z"
  }
}
```

### 4. Use SDK methods with the token

```js
// Link a bank account
strongholdPay.addPaymentSource(customerToken, {
  onSuccess: (paymentSource) => {
    /* save paymentSource.id */
  },
  onExit: () => {
    /* user cancelled */
  },
  onError: (err) => {
    /* handle error */
  },
});

// Create a charge
strongholdPay.charge(customerToken, {
  charge: {
    amount: 4995, // $49.95 in cents
    currency: "usd",
    paymentSourceId: "payment_source_...",
    externalId: "order_123", // optional
  },
  authorizeOnly: false,
  onSuccess: (charge) => {
    /* charge.id */
  },
  onExit: () => {},
  onError: (err) => {},
});
```

## Environments

| Environment | Publishable Key  | Secret Key       | API Base                        |
| ----------- | ---------------- | ---------------- | ------------------------------- |
| Sandbox     | `pk_sandbox_...` | `sk_sandbox_...` | `https://api.strongholdpay.com` |
| Live        | `pk_live_...`    | `sk_live_...`    | `https://api.strongholdpay.com` |

Keys are found on the Developers page of the [Stronghold Dashboard](https://dashboard.strongholdpay.com/).

## Sandbox Testing

Use fake bank accounts in sandbox. Test credentials for aggregators:

| Aggregator | Username              | Password      |
| ---------- | --------------------- | ------------- |
| Plaid      | `user_good`           | `pass_good`   |
| Yodlee     | `YodTest.site16441.2` | `site16441.2` |

Refer to [Plaid sandbox docs](https://plaid.com/docs/sandbox/test-credentials) for additional test credentials and institutions (e.g., First Platypus Bank).

## Fraud Prevention

Include the Stronghold.Pay.JS script on **every page** of the site (not just checkout) to enable real-time transaction intelligence for fraud detection and chargeback prevention.

## Core Concepts

- **Customer** — End user making payments. Created via API, identified by `customer_id`
- **Customer Token** — JWT (12-hour TTL) authorizing frontend SDK calls for a specific customer
- **Payment Source** — A linked bank account. Created via `addPaymentSource` or `bank_link` PayLink
- **Charge** — A payment from customer to merchant. Amounts in cents (e.g., `4995` = $49.95)
- **Tip** — An additional payment associated with a charge
- **PayLink** — A hosted URL for payment flows without frontend SDK integration
- **authorizeOnly** — When `true`, charges/tips reach `authorized` state without immediate capture; use the Capture Charge API to capture later

## Detailed References

- **JS SDK methods, callbacks, arguments**: See [references/sdk-reference.md](references/sdk-reference.md)
- **REST API v2 endpoints and authentication**: See [references/rest-api.md](references/rest-api.md)
- **PayLink hosted payment pages**: See [references/paylink.md](references/paylink.md)
- **Error types and codes**: See [references/errors.md](references/errors.md)

## SHx Token (Stellar Blockchain)

SHx is Stronghold's utility token on the Stellar blockchain. It connects to the payment ecosystem as a **rewards mechanism** — merchants and customers earn SHx through the Stronghold Rewards Program based on transaction volume processed through the payment network. SHx is also used for governance voting and merchant financing liquidity. There are no direct SDK/API methods for SHx interaction; it operates as a background incentive layer on top of the payment infrastructure.

## Key Links

- [Stronghold Developer Docs](https://docs.strongholdpay.com/)
- [SDK Tutorials](https://tutorials.strongholdpay.com/sdk)
- [PayLink Tutorials](https://tutorials.strongholdpay.com/paylink)
- [Use Case Demo](https://tutorials.strongholdpay.com/use-cases)
- [API Reference v2](https://docs.strongholdpay.com/docs/stronghold-pay/YXBpOjE5ODIyMjc1-api-reference-v2)
- [Stronghold Dashboard](https://dashboard.strongholdpay.com/)
