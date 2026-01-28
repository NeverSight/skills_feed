---
name: stripe-expert
description: Senior Payment Solutions Architect for Stripe (2026). Specialized in secure checkout flows, complex billing models (usage-based/hybrid), global tax compliance via Stripe Tax, and high-performance Next.js 16 integration. Expert in building PCI-compliant, idempotent, and resilient payment systems using Checkout Sessions, Payment Elements, and Server Actions.
---

# 💳 Skill: stripe-expert (v1.0.0)

## Executive Summary
Senior Payment Solutions Architect for Stripe (2026). Specialized in secure checkout flows, complex billing models (usage-based/hybrid), global tax compliance via Stripe Tax, and high-performance Next.js 16 integration. Expert in building PCI-compliant, idempotent, and resilient payment systems using Checkout Sessions, Payment Elements, and Server Actions.

---

## 📋 The Conductor's Protocol

1.  **Integration Choice**: Prioritize **Checkout Sessions** (hosted or embedded) for 90% of use cases. Use **Payment Element** only when extreme UI customization is required.
2.  **Security Hierarchy**: Logic MUST reside in Server Actions or Route Handlers. Never trust client-side price or quantity data.
3.  **Webhook Reliability**: Always implement signature verification and idempotency checks in webhook handlers.
4.  **Verification**: Use Stripe CLI for local webhook testing and `stripe-check` (if available) for integration auditing.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Server Actions First (Next.js 16)
As of 2026, all session creation and sensitive logic must use Server Actions.
- **Rule**: Never expose Secret Keys to the client.
- **Initialization**: Use `loadStripe` as a singleton to optimize performance.

### 2. Automated Compliance (Stripe Tax & Billing)
- **Rule**: Enable `automatic_tax` in all Checkout Sessions to handle global nexus and VAT/GST automatically.
- **Metering**: Use **Billing Meters** for usage-based SaaS models. Send usage events asynchronously to avoid blocking user flows.

### 3. Idempotency & Resilience
- **Rule**: All mutation requests to Stripe (session creation, payment intents) MUST include an `idempotency_key`.
- **Webhooks**: Handlers must return a `200 OK` immediately after recording the event to avoid Stripe retries during long-running processing.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Quick Start: Secure Checkout Session (React 19 / Next.js 16)
```tsx
// app/actions/stripe.ts
"use server";

import Stripe from "stripe";
import { headers } from "next/headers";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-12-18.acacia", // Always use the latest pinned version
});

export async function createCheckoutSession(priceId: string) {
  const origin = headers().get("origin");
  
  // Validation should happen here (check user, items, stock)
  
  const session = await stripe.checkout.sessions.create({
    line_items: [{ price: priceId, quantity: 1 }],
    mode: "subscription",
    success_url: `${origin}/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${origin}/canceled`,
    automatic_tax: { enabled: true }, // 2026 Standard
  }, {
    idempotencyKey: `checkout_${priceId}_${Date.now()}`, // Prevent double-clicks
  });

  return { url: session.url };
}
```

### Advanced Pattern: Usage-Based Billing Meter
```typescript
// server/usage.ts
export async function reportUsage(subscriptionItemId: string, usageCount: number) {
  await stripe.billing.meterEvents.create({
    event_name: "api_call",
    payload: {
      value: usageCount.toString(),
      stripe_customer_id: "cus_...",
    },
  });
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use the legacy **Charges API**. Always use PaymentIntents or Checkout Sessions.
2.  **DO NOT** use the **Card Element** (single line). Use the **Payment Element** for multi-method support.
3.  **DO NOT** store raw card data on your servers. It violates PCI compliance and increases risk.
4.  **DO NOT** rely on the `success_url` for business logic completion. Only use **Webhooks** for fulfillment.
5.  **DO NOT** pass specific `payment_method_types`. Enable **Dynamic Payment Methods** in the Dashboard.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Checkout vs. Payment Element](./references/integration-types.md)**: When to use which and how to customize.
- **[Billing & Metered Pricing](./references/billing-models.md)**: Tiers, overages, and consumption-based revenue.
- **[Global Tax & Compliance](./references/tax-compliance.md)**: Stripe Tax, VAT, and invoice generation.
- **[Webhook Engineering](./references/webhooks.md)**: Verification, idempotency, and fulfillment logic.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/verify-webhooks.ts`: Utility to simulate and test local webhook handlers.
- `scripts/sync-prices.py`: Syncs your local product DB with the Stripe Dashboard.

---

## 🎓 Learning Resources
- [Stripe Documentation](https://docs.stripe.com/)
- [Stripe API Reference](https://docs.stripe.com/api)
- [Stripe Samples (GitHub)](https://github.com/stripe-samples)

---
*Updated: January 23, 2026 - 17:35*
