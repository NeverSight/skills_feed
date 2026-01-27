---
name: payment-integration
description: Expert in integrating payment gateways (Stripe, PayPal, Adyen) and designing PCI-compliant billing architectures. Use when implementing checkout flows, subscriptions, or payment processing. Triggers include "Stripe", "PayPal", "payment gateway", "checkout", "subscription billing", "PCI compliance", "payment processing".
---

# Payment Integration

## Purpose
Provides expertise in integrating payment gateways and designing PCI-compliant billing systems. Specializes in implementing checkout flows, subscription management, and payment processing with providers like Stripe, PayPal, and Adyen.

## When to Use
- Integrating Stripe, PayPal, or other payment gateways
- Implementing checkout and payment flows
- Building subscription billing systems
- Ensuring PCI-DSS compliance
- Handling payment webhooks
- Implementing payment retry logic
- Setting up multi-currency payments
- Building invoicing systems

## Quick Start
**Invoke this skill when:**
- Integrating payment gateways (Stripe, PayPal, Adyen)
- Building checkout or subscription flows
- Designing PCI-compliant payment systems
- Implementing webhook handlers for payments
- Setting up recurring billing

**Do NOT invoke when:**
- General ledger/accounting systems → use `/fintech-engineer`
- API design without payment focus → use `/api-designer`
- Frontend checkout UI only → use `/frontend-design`
- Security audit → use `/security-auditor`

## Decision Framework
```
Payment Use Case?
├── One-time Purchase
│   └── Stripe Checkout / PayPal Buttons
├── Subscription
│   └── Stripe Billing / Recurly
├── Marketplace/Split Payments
│   └── Stripe Connect / PayPal Commerce
├── Enterprise/B2B
│   └── Invoicing with NET terms
└── Global Payments
    └── Adyen / Multi-gateway strategy
```

## Core Workflows

### 1. Stripe Integration
1. Set up Stripe account and API keys
2. Create products and prices
3. Implement Checkout Session or Elements
4. Handle payment confirmation
5. Set up webhook endpoint
6. Process webhook events (succeeded, failed)

### 2. Subscription Billing
1. Define subscription plans and pricing
2. Create customer in payment provider
3. Implement subscription creation flow
4. Handle trial periods
5. Manage upgrades/downgrades
6. Implement dunning for failed payments

### 3. Webhook Handling
1. Create secure webhook endpoint
2. Verify webhook signatures
3. Make handlers idempotent
4. Process events in order
5. Handle retry scenarios
6. Log all webhook events

## Best Practices
- Never store full card numbers—use tokenization
- Always verify webhook signatures
- Implement idempotency for payment operations
- Use test mode thoroughly before production
- Handle all payment states (pending, succeeded, failed)
- Store payment provider IDs for reconciliation

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Storing card numbers | PCI violation | Use tokenization |
| No webhook verification | Security risk | Verify signatures |
| Synchronous payment only | Poor UX, timeouts | Async with webhooks |
| Missing idempotency | Duplicate charges | Idempotency keys |
| No retry logic | Lost revenue | Implement dunning |
