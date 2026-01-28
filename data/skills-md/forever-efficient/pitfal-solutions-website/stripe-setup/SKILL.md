---
name: stripe-setup
description: Set up Stripe products, prices, and webhooks for Pitfal Solutions photography packages. Creates products for portrait sessions, event coverage, digital downloads, and prints. Use when configuring payment processing.
---

# Stripe Setup

Configure Stripe products and prices for Pitfal Solutions packages.

## Prerequisites
1. Stripe CLI installed:
   ```bash
   brew install stripe/stripe-cli/stripe
   ```

2. Login to Stripe:
   ```bash
   stripe login
   ```

3. Verify connection:
   ```bash
   stripe config --list
   ```

## Create Products

### Portrait Session
```bash
stripe products create \
  --name="Portrait Session" \
  --description="1-hour portrait photography session including 10 edited digital images"
```

### Event Coverage - Half Day
```bash
stripe products create \
  --name="Event Coverage - Half Day" \
  --description="4-hour event photography and videography coverage"
```

### Event Coverage - Full Day
```bash
stripe products create \
  --name="Event Coverage - Full Day" \
  --description="8-hour event photography and videography coverage"
```

### Digital Download Pack
```bash
stripe products create \
  --name="Digital Download Pack" \
  --description="High-resolution digital images from your session"
```

### Print - 8x10
```bash
stripe products create \
  --name="Print - 8x10" \
  --description="Professional quality 8x10 print"
```

## Create Prices
After creating products, note the product IDs and create prices:

```bash
# Portrait Session - $250
stripe prices create \
  --product="prod_XXXXX" \
  --unit-amount=25000 \
  --currency=usd

# Event Half Day - $800
stripe prices create \
  --product="prod_XXXXX" \
  --unit-amount=80000 \
  --currency=usd

# Event Full Day - $1500
stripe prices create \
  --product="prod_XXXXX" \
  --unit-amount=150000 \
  --currency=usd

# Digital Download Pack - $150
stripe prices create \
  --product="prod_XXXXX" \
  --unit-amount=15000 \
  --currency=usd

# Print 8x10 - $35
stripe prices create \
  --product="prod_XXXXX" \
  --unit-amount=3500 \
  --currency=usd
```

## Setup Webhooks (Local Development)
```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

## Setup Webhooks (Production)
```bash
stripe webhook_endpoints create \
  --url="https://pitfal.solutions/api/webhooks/stripe" \
  --enabled-events="checkout.session.completed,payment_intent.succeeded,payment_intent.payment_failed"
```

## List Products
Verify setup:
```bash
stripe products list --limit 10
stripe prices list --limit 10
```
