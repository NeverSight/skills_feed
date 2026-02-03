---
name: stripe-integration
description: Implement Stripe payments, webhooks, and subscriptions correctly first time
---

# Stripe Integration

Consistent Stripe implementation following best practices.

## Key Components

### Payment Flows
- Checkout sessions
- Payment intents
- SCA/3DS handling

### Webhooks (Critical)
- checkout.session.completed
- customer.subscription.created/updated/deleted
- invoice.paid/payment_failed

### Subscriptions
- Products and prices
- Lifecycle management
- Trial periods

## Security Checklist
- [ ] API keys as environment variables
- [ ] Webhook signatures validated
- [ ] Server-side amount calculations
- [ ] HTTPS for all requests

## Usage
```
"Use Stripe integration skill to add monthly/annual subscriptions"
```

## Webhook Testing
```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```
