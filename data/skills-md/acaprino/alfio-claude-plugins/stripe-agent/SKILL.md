---
name: stripe-agent
description: Comprehensive Stripe integration agent for payments, subscriptions, billing, and marketplace management. Use when Claude needs to work with Stripe API for creating customers, managing subscriptions, processing payments, handling checkout sessions, setting up products/prices, managing webhooks, Connect marketplaces, metered billing, tax calculation, fraud prevention, or any payment-related task. Triggers on mentions of Stripe, payments, subscriptions, billing, checkout, invoices, payment intents, recurring payments, Connect, marketplace, SCA, 3D Secure, or disputes.
---

# Stripe Agent

This skill enables Claude to interact with Stripe's API for complete payment and subscription management.

## Prerequisites

Ensure `STRIPE_SECRET_KEY` environment variable is set. For webhook handling, also set `STRIPE_WEBHOOK_SECRET`.

```bash
export STRIPE_SECRET_KEY="sk_test_..."
export STRIPE_WEBHOOK_SECRET="whsec_..."
```

Install the Stripe SDK:
```bash
pip install stripe --break-system-packages
```

## Core Workflows

### 1. Customer Management

Create and manage customers before any payment operation.

```python
import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# Create customer
customer = stripe.Customer.create(
    email="user@example.com",
    name="John Doe",
    metadata={"user_id": "your_app_user_id"}
)

# Retrieve customer
customer = stripe.Customer.retrieve("cus_xxx")

# Update customer
stripe.Customer.modify("cus_xxx", metadata={"plan": "premium"})

# List customers
customers = stripe.Customer.list(limit=10, email="user@example.com")
```

### 2. Products and Prices

Always create Products first, then attach Prices. Use `lookup_key` for easy price retrieval.

```python
# Create product
product = stripe.Product.create(
    name="Pro Plan",
    description="Full access to all features",
    metadata={"tier": "pro"}
)

# Create recurring price (subscription)
price = stripe.Price.create(
    product=product.id,
    unit_amount=1999,  # Amount in cents (€19.99)
    currency="eur",
    recurring={"interval": "month"},
    lookup_key="pro_monthly"
)

# Create one-time price
one_time_price = stripe.Price.create(
    product=product.id,
    unit_amount=9999,
    currency="eur",
    lookup_key="pro_lifetime"
)

# Retrieve price by lookup_key
prices = stripe.Price.list(lookup_keys=["pro_monthly"])
```

### 3. Checkout Sessions (Recommended for Web)

Use Checkout Sessions for secure, hosted payment pages.

```python
# Subscription checkout
session = stripe.checkout.Session.create(
    customer="cus_xxx",  # Optional: attach to existing customer
    mode="subscription",
    line_items=[{
        "price": "price_xxx",
        "quantity": 1
    }],
    success_url="https://yourapp.com/success?session_id={CHECKOUT_SESSION_ID}",
    cancel_url="https://yourapp.com/cancel",
    metadata={"user_id": "123"}
)
# Redirect user to: session.url

# One-time payment checkout
session = stripe.checkout.Session.create(
    mode="payment",
    line_items=[{"price": "price_xxx", "quantity": 1}],
    success_url="https://yourapp.com/success",
    cancel_url="https://yourapp.com/cancel"
)
```

### 4. Subscription Management

```python
# Create subscription directly (when you have payment method)
subscription = stripe.Subscription.create(
    customer="cus_xxx",
    items=[{"price": "price_xxx"}],
    payment_behavior="default_incomplete",
    expand=["latest_invoice.payment_intent"]
)

# Retrieve subscription
sub = stripe.Subscription.retrieve("sub_xxx")

# Update subscription (change plan)
stripe.Subscription.modify(
    "sub_xxx",
    items=[{
        "id": sub["items"]["data"][0].id,
        "price": "price_new_xxx"
    }],
    proration_behavior="create_prorations"
)

# Cancel subscription
stripe.Subscription.cancel("sub_xxx")  # Immediate
# Or cancel at period end:
stripe.Subscription.modify("sub_xxx", cancel_at_period_end=True)
```

### 5. Payment Intents (Custom Integration)

Use when you need full control over the payment flow.

```python
# Create payment intent
intent = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    customer="cus_xxx",
    metadata={"order_id": "order_123"}
)
# Return intent.client_secret to frontend

# Confirm payment (server-side)
stripe.PaymentIntent.confirm(
    "pi_xxx",
    payment_method="pm_xxx"
)
```

### 6. Webhook Handling

Critical for subscription lifecycle. See `scripts/webhook_handler.py` for complete implementation.

Key events to handle:
- `checkout.session.completed` - Payment successful
- `customer.subscription.created` - New subscription
- `customer.subscription.updated` - Plan changes
- `customer.subscription.deleted` - Cancellation
- `invoice.paid` - Successful renewal
- `invoice.payment_failed` - Failed payment

```python
import stripe

def handle_webhook(payload, sig_header):
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    
    event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
    )
    
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # Fulfill order, activate subscription
        
    elif event["type"] == "invoice.payment_failed":
        invoice = event["data"]["object"]
        # Notify user, handle dunning
        
    return {"status": "success"}
```

## Firebase Integration Pattern

For Firebase + Stripe integration, see `references/firebase-integration.md`.

Quick setup:
1. Store Stripe customer_id in Firestore user document
2. Sync subscription status via webhooks to Firestore
3. Use Firebase Security Rules to check subscription status

## Common Operations Quick Reference

| Task | Method |
|------|--------|
| Create customer | `stripe.Customer.create()` |
| Start subscription | `stripe.checkout.Session.create(mode="subscription")` |
| Cancel subscription | `stripe.Subscription.cancel()` |
| Change plan | `stripe.Subscription.modify()` |
| Refund payment | `stripe.Refund.create(payment_intent="pi_xxx")` |
| Get invoices | `stripe.Invoice.list(customer="cus_xxx")` |
| Create portal session | `stripe.billing_portal.Session.create()` |

## Customer Portal (Self-Service)

Let customers manage their own subscriptions:

```python
portal_session = stripe.billing_portal.Session.create(
    customer="cus_xxx",
    return_url="https://yourapp.com/account"
)
# Redirect to: portal_session.url
```

## Testing

Use test mode keys (`sk_test_...`) and test card numbers:
- `4242424242424242` - Successful payment
- `4000000000000002` - Declined
- `4000002500003155` - Requires 3D Secure

## Error Handling

```python
try:
    # Stripe operation
except stripe.error.CardError as e:
    # Card declined
    print(f"Card error: {e.user_message}")
except stripe.error.InvalidRequestError as e:
    # Invalid parameters
    print(f"Invalid request: {e}")
except stripe.error.AuthenticationError:
    # Invalid API key
    pass
except stripe.error.StripeError as e:
    # Generic Stripe error
    pass
```

## Payment Links (No-Code Payments)

Create shareable payment links without code:

```python
# Create a payment link
payment_link = stripe.PaymentLink.create(
    line_items=[{"price": "price_xxx", "quantity": 1}],
    after_completion={"type": "redirect", "redirect": {"url": "https://yourapp.com/thanks"}}
)
# Share: payment_link.url

# Create reusable link with adjustable quantity
payment_link = stripe.PaymentLink.create(
    line_items=[{"price": "price_xxx", "adjustable_quantity": {"enabled": True, "minimum": 1, "maximum": 10}}]
)
```

## Metered & Usage-Based Billing

For API calls, seats, or consumption-based pricing:

```python
# Create metered price
metered_price = stripe.Price.create(
    product="prod_xxx",
    currency="eur",
    recurring={"interval": "month", "usage_type": "metered"},
    billing_scheme="per_unit",
    unit_amount=10,  # €0.10 per unit
    lookup_key="api_calls"
)

# Report usage (do this periodically)
stripe.SubscriptionItem.create_usage_record(
    "si_xxx",  # subscription item id
    quantity=150,
    timestamp=int(datetime.now().timestamp()),
    action="increment"  # or "set" to override
)

# Tiered pricing
tiered_price = stripe.Price.create(
    product="prod_xxx",
    currency="eur",
    recurring={"interval": "month", "usage_type": "metered"},
    billing_scheme="tiered",
    tiers_mode="graduated",  # or "volume"
    tiers=[
        {"up_to": 100, "unit_amount": 50},      # First 100: €0.50 each
        {"up_to": 1000, "unit_amount": 30},     # 101-1000: €0.30 each
        {"up_to": "inf", "unit_amount": 10}     # 1001+: €0.10 each
    ]
)
```

## Stripe Connect (Marketplaces)

Build platforms where you facilitate payments between buyers and sellers:

```python
# Create connected account (Express - recommended)
account = stripe.Account.create(
    type="express",
    country="US",
    email="seller@example.com",
    capabilities={"card_payments": {"requested": True}, "transfers": {"requested": True}}
)

# Generate onboarding link
account_link = stripe.AccountLink.create(
    account=account.id,
    refresh_url="https://yourapp.com/reauth",
    return_url="https://yourapp.com/return",
    type="account_onboarding"
)
# Redirect seller to: account_link.url

# Create payment with platform fee (destination charge)
payment_intent = stripe.PaymentIntent.create(
    amount=10000,
    currency="eur",
    application_fee_amount=1000,  # Platform takes €10
    transfer_data={"destination": "acct_xxx"}  # Seller receives €90
)

# Direct charge (charge on connected account)
payment_intent = stripe.PaymentIntent.create(
    amount=10000,
    currency="eur",
    stripe_account="acct_xxx",  # Charge on seller's account
    application_fee_amount=1000
)

# Transfer funds to connected account
transfer = stripe.Transfer.create(
    amount=5000,
    currency="eur",
    destination="acct_xxx"
)
```

## Tax Calculation (Stripe Tax)

Automatic tax calculation and collection:

```python
# Enable automatic tax in checkout
session = stripe.checkout.Session.create(
    mode="payment",
    line_items=[{"price": "price_xxx", "quantity": 1}],
    automatic_tax={"enabled": True},
    success_url="https://yourapp.com/success",
    cancel_url="https://yourapp.com/cancel"
)

# Calculate tax for payment intent
payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    automatic_payment_methods={"enabled": True},
    # Tax calculated based on customer location
)

# Tax calculation API (preview)
calculation = stripe.tax.Calculation.create(
    currency="eur",
    line_items=[{"amount": 1000, "reference": "L1"}],
    customer_details={"address": {"country": "DE"}, "address_source": "billing"}
)
```

## 3D Secure & SCA Compliance

Handle Strong Customer Authentication (required in EU/UK):

```python
# Payment intent with 3DS when required
payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    payment_method="pm_xxx",
    confirmation_method="manual",
    confirm=True,
    return_url="https://yourapp.com/return"  # For 3DS redirect
)

# Check if authentication required
if payment_intent.status == "requires_action":
    # Redirect customer to: payment_intent.next_action.redirect_to_url.url
    pass

# Force 3DS (for high-risk transactions)
payment_intent = stripe.PaymentIntent.create(
    amount=50000,
    currency="eur",
    payment_method_options={
        "card": {"request_three_d_secure": "any"}  # or "automatic"
    }
)

# Webhook: handle authentication
# Event: payment_intent.requires_action
```

**Test cards for 3DS:**
- `4000002500003155` - Requires authentication
- `4000002760003184` - Always authenticates
- `4000008260003178` - Authentication fails

## Fraud Prevention (Stripe Radar)

Built-in fraud protection with Radar:

```python
# Payment with Radar rules
payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    payment_method="pm_xxx",
    # Radar evaluates automatically
)

# Check radar outcome after payment
charge = stripe.Charge.retrieve("ch_xxx")
radar_outcome = charge.outcome
# radar_outcome.risk_level: "normal", "elevated", "highest"
# radar_outcome.risk_score: 0-100

# Custom metadata for Radar rules
payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    metadata={
        "customer_account_age": "30",  # days
        "order_count": "5"
    }
)

# Block high-risk in Radar Dashboard:
# Rule: "Block if :risk_level: = 'highest'"
# Rule: "Review if ::customer_account_age:: < 7"
```

## Dispute Handling

Manage chargebacks and disputes:

```python
# List disputes
disputes = stripe.Dispute.list(limit=10)

# Retrieve dispute details
dispute = stripe.Dispute.retrieve("dp_xxx")
# dispute.reason: "fraudulent", "duplicate", "product_not_received", etc.
# dispute.status: "needs_response", "under_review", "won", "lost"

# Submit evidence
stripe.Dispute.modify(
    "dp_xxx",
    evidence={
        "customer_name": "John Doe",
        "customer_email_address": "john@example.com",
        "shipping_tracking_number": "1Z999AA10123456784",
        "uncategorized_text": "Customer confirmed receipt via email on..."
    },
    submit=True  # Submit evidence
)

# Webhook events for disputes
# charge.dispute.created - New dispute opened
# charge.dispute.updated - Evidence submitted or status changed
# charge.dispute.closed - Dispute resolved
```

## Idempotency & Best Practices

Prevent duplicate operations:

```python
import uuid

# Idempotent request (safe to retry)
payment_intent = stripe.PaymentIntent.create(
    amount=2000,
    currency="eur",
    idempotency_key=f"order_{order_id}"  # Unique per operation
)

# For retries, use same key
try:
    payment = stripe.PaymentIntent.create(
        amount=2000,
        currency="eur",
        idempotency_key="order_123"
    )
except stripe.error.StripeError:
    # Safe to retry with same idempotency_key
    payment = stripe.PaymentIntent.create(
        amount=2000,
        currency="eur",
        idempotency_key="order_123"
    )

# Generate unique keys
def idempotency_key(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}"
```

**Best Practices:**
1. Always use idempotency keys for create/update operations
2. Store payment intent ID before confirming
3. Use webhooks as source of truth (not API responses)
4. Handle `requires_action` status for 3DS
5. Never log full card numbers or CVV
6. Use test mode for development (`sk_test_...`)

## Scripts Reference

- `scripts/setup_products.py` - Create products and prices
- `scripts/webhook_handler.py` - Flask webhook endpoint
- `scripts/sync_subscriptions.py` - Sync subscriptions to database
- `scripts/stripe_utils.py` - Common utility functions

## Additional Resources

- `references/firebase-integration.md` - Firebase + Firestore integration
- `references/api-cheatsheet.md` - Quick API reference
