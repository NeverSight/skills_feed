---
name: teya
description: Teya payment integration guide covering POSLink (cloud-based terminal integration), All-In-One (single-device Android), E-Commerce APIs (hosted checkout, payment links), and Payments Gateway. Includes decision trees, authentication patterns, test cards, and certification guidance.
---

# Teya Payment Integration Skill

Complete reference for integrating with Teya's payment ecosystem, covering terminal integrations, e-commerce APIs, and SDK implementations.

## Quick Decision Tree: Which Integration Do You Need?

```
Need to accept payments?
├── In-person (card present)?
│   ├── ePOS on separate device from terminal?
│   │   └── → POSLink Integration (cloud-based, Android/Windows)
│   │       See: references/epos-sdk/overview.md
│   │       See: references/poslink/overview.md
│   │
│   └── ePOS and terminal on same device?
│       └── → All-In-One Integration (Android only)
│           See: references/epos-sdk/all-in-one-introduction.md
│
└── Online (card not present)?
    ├── Need hosted checkout page?
    │   └── → E-Commerce API - Hosted Checkout
    │       See: references/apis/e-commerce-introduction.md
    │
    ├── Need to send payment links?
    │   └── → E-Commerce API - Payment Links
    │       See: references/apis/e-commerce-introduction.md
    │
    └── PCI compliant and want direct processing?
        └── → E-Commerce API - Direct Transactions
            See: references/apis/e-commerce-introduction.md
```

## Integration Overview

### 1. POSLink (Cloud Terminal Integration)

**Use when:** Your ePOS runs on a separate device (tablet, PC) from the payment terminal.

**Platforms:** Android, Windows (iOS planned)

**Key features:**
- Cloud-based communication between ePOS and terminal
- SDK handles OAuth authentication and token refresh
- Pre-built payment UI screens
- Minimal setup required

**Getting started:**
1. Register at [partner.teya.xyz](https://partner.teya.xyz) (staging) or [partner.teya.com](https://partner.teya.com) (production)
2. Create OAuth application (Device Code Flow)
3. Get Client ID and Client Secret (per partner, not per merchant)
4. Request mock payment app APK from Partnership Manager
5. Integrate SDK into your application

**References:**
- [ePOS SDK Overview](references/epos-sdk/overview.md)
- [POSLink Getting Started](references/epos-sdk/poslink-getting-started.md)
- [POSLink Overview](references/poslink/overview.md)
- [POSLink Design](references/poslink/design.md)
- [POSLink Testing](references/poslink/test.md)
- [POSLink FAQ](references/poslink/faq.md)
- [POSLink Certification](references/poslink/get-certified.md)

### 2. All-In-One Integration

**Use when:** Your ePOS app runs on the same Android device as the payment terminal.

**Platforms:** Android only (Sunmi, PAX terminals)

**Key features:**
- Single-device workflow
- Apps communicate via deeplinks
- Receipt printing via Sunmi/PAX SDKs
- No cloud dependency for device communication

**Getting started:**
1. Request debug terminal from Partnership Manager
2. Specify terminal model (Sunmi or PAX)
3. Get test merchant account assigned to terminal
4. Integrate SDK using provided guides

**References:**
- [ePOS SDK Overview](references/epos-sdk/overview.md)
- [All-In-One Introduction](references/epos-sdk/all-in-one-introduction.md)

### 3. E-Commerce API (Online Payments)

**Use when:** You need to accept online payments (card not present).

**Options:**
- **Hosted Checkout** - Redirect customers to Teya's secure payment page (best for most merchants)
- **Payment Links** - Send payment links via email/SMS for remote collection
- **Direct Processing** - Full control for PCI-compliant systems

**Getting started:**
1. Get Teya merchant account from your representative
2. Access Business Portal: [business.teya.xyz](https://business.teya.xyz) (staging) or [business.teya.com](https://business.teya.com) (production)
3. Create API credentials under store settings → Integrations
4. Configure webhooks for payment notifications
5. Implement OAuth token exchange

**References:**
- [E-Commerce Introduction](references/apis/e-commerce-introduction.md)

### 4. Payments Gateway API

**Use when:** You're building card-present processing with direct API integration (advanced).

**Supports:**
- Card-present transactions (EMV, contactless)
- Pre-authorization and capture flows
- Refunds and reversals
- MOTO transactions
- SoftPOS transactions

**References:**
- [Payments Overview](references/apis/payments-overview.md)
- [Test Cards](references/apis/test-cards.md)

### 5. POSLink REST API

**Use when:** You need programmatic access to stores, terminals, and receipt printing.

**Features:**
- Payment request management
- Store configuration
- Terminal monitoring
- Receipt printing (JSON and image formats)

**References:**
- [POSLink API](references/apis/poslink-api.md)

## Authentication

All Teya APIs use OAuth 2.0:

**Environments:**
- **Staging:** https://id.teya.xyz/oauth/v2/oauth-token
- **Production:** https://id.teya.com/oauth/v2/oauth-token

**Token lifetimes:**
- Production: 15 minutes
- Staging: 24 hours

**Example token request:**
```bash
curl -X POST 'https://id.teya.com/oauth/v2/oauth-token' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=client_credentials' \
  -d 'client_id=<CLIENT_ID>' \
  -d 'client_secret=<CLIENT_SECRET>' \
  -d 'scope=checkout/sessions/create refunds/create'
```

## Test Cards

| Brand | Number | Use Case |
|-------|--------|----------|
| Visa | 4242424242424242 | General testing |
| Mastercard | 5555555555554444 | Mastercard testing |
| Amex | 378282246310005 | Amex testing |
| Mastercard | 2223600089700011 | DCC testing (EUR) |

- Use any 3-digit CVV (4-digit for Amex)
- Use any future expiry date
- Test cards only work in staging environments

See [Test Cards Reference](references/apis/test-cards.md) for complete list.

## Important Notes

### Amount Format
All amounts are in **minor units** (cents/pence):
- €1.00 = 100
- €50.00 = 5000
- $25.99 = 2599

### Currency Format
ISO-4217 3-letter codes: EUR, USD, GBP, etc.

### Environment URLs
- Staging domains: `*.teya.xyz`
- Production domains: `*.teya.com`

### Idempotency
Always use `Idempotency-Key` headers to prevent duplicate transactions.

## Certification Process (POSLink)

1. **Design** - Plan integration architecture
2. **Develop** - Implement authentication and payment flows
3. **Test** - Validate integration thoroughly
4. **Get Certified** - Schedule certification and go live

See [Integration Checklist](references/poslink/integration-checklist.md) and [Get Certified](references/poslink/get-certified.md).

## Support

- **Partnership Manager** - For terminal requests, test accounts, APKs
- **Teya Representative** - For merchant account setup
- **Developer Portal** - [partner.teya.xyz](https://partner.teya.xyz) / [partner.teya.com](https://partner.teya.com)
- **Documentation** - [docs.teya.com](https://docs.teya.com)

## File Index

### APIs
- [references/apis/payments-overview.md](references/apis/payments-overview.md) - Payments Gateway API
- [references/apis/poslink-api.md](references/apis/poslink-api.md) - POSLink REST API
- [references/apis/e-commerce-introduction.md](references/apis/e-commerce-introduction.md) - E-Commerce APIs
- [references/apis/test-cards.md](references/apis/test-cards.md) - Test card numbers

### ePOS SDK
- [references/epos-sdk/overview.md](references/epos-sdk/overview.md) - SDK overview and integration options
- [references/epos-sdk/glossary.md](references/epos-sdk/glossary.md) - Terminology
- [references/epos-sdk/poslink-getting-started.md](references/epos-sdk/poslink-getting-started.md) - POSLink quick start
- [references/epos-sdk/all-in-one-introduction.md](references/epos-sdk/all-in-one-introduction.md) - All-In-One integration

### POSLink Guides
- [references/poslink/overview.md](references/poslink/overview.md) - POSLink overview
- [references/poslink/design.md](references/poslink/design.md) - Integration design
- [references/poslink/test.md](references/poslink/test.md) - Testing guide
- [references/poslink/faq.md](references/poslink/faq.md) - Frequently asked questions
- [references/poslink/get-certified.md](references/poslink/get-certified.md) - Certification process
- [references/poslink/integration-checklist.md](references/poslink/integration-checklist.md) - Pre-launch checklist
- [references/poslink/cancel-payment-request.md](references/poslink/cancel-payment-request.md) - Cancel payments
