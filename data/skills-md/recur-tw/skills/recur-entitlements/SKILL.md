---
name: recur-entitlements
description: Implement access control and permission checking with Recur entitlements API. Use when building paywalls, checking subscription status, gating premium features, or when user mentions "paywall", "權限檢查", "entitlements", "access control", "premium features".
license: MIT
metadata:
  author: recur
  version: "0.0.7"
---

# Recur Entitlements & Access Control

You are helping implement access control using Recur's entitlements system. Entitlements let you check if a customer has access to your products (subscriptions or one-time purchases).

## Quick Start: Client-Side Check

```tsx
import { RecurProvider, useCustomer } from 'recur-tw'

// 1. Wrap app with provider and identify customer
function App() {
  return (
    <RecurProvider
      config={{ publishableKey: process.env.NEXT_PUBLIC_RECUR_PUBLISHABLE_KEY }}
      customer={{ email: 'user@example.com' }}
    >
      <MyApp />
    </RecurProvider>
  )
}

// 2. Check access anywhere in your app
function PremiumFeature() {
  const { check, isLoading } = useCustomer()

  if (isLoading) return <div>Loading...</div>

  const { allowed } = check('pro-plan')

  if (!allowed) {
    return <UpgradePrompt />
  }

  return <PremiumContent />
}
```

## Customer Identification

Identify customers using one of these methods:

```tsx
// By email (most common)
<RecurProvider customer={{ email: 'user@example.com' }}>

// By your system's user ID
<RecurProvider customer={{ externalId: 'user_123' }}>

// By Recur customer ID
<RecurProvider customer={{ id: 'cus_xxx' }}>
```

## Checking Access

### Synchronous Check (Cached)

Fast, uses cached data. Good for UI rendering.

```tsx
const { check } = useCustomer()

// Check by product slug
const { allowed, entitlement } = check('pro-plan')

// Check by product ID
const { allowed } = check('prod_xxx')

if (allowed) {
  // User has access
  // entitlement contains details like status, expiresAt
}
```

### Async Check (Live)

Fetches fresh data from API. Use for critical operations.

```tsx
const { check } = useCustomer()

// Real-time check
const { allowed, entitlement } = await check('pro-plan', { live: true })

// Good for:
// - Before processing important actions
// - After checkout to confirm access
// - When cached data might be stale
```

### Manual Refetch

```tsx
const { refetch } = useCustomer()

// After checkout completion
onPaymentComplete: async () => {
  await refetch() // Refresh entitlements
  router.push('/dashboard')
}
```

## Entitlement Response Structure

```typescript
interface Entitlement {
  product: string        // Product slug
  productId: string      // Product ID
  status: EntitlementStatus
  source: 'subscription' | 'order'  // How they got access
  sourceId: string       // Subscription/Order ID
  grantedAt: string      // When access was granted
  expiresAt: string | null  // When access expires (null = permanent)
}

type EntitlementStatus =
  | 'active'      // Subscription active
  | 'trialing'    // In trial period
  | 'past_due'    // Payment failed, in grace period
  | 'canceled'    // Cancelled but access until period end
  | 'purchased'   // One-time purchase (permanent)
```

## Server-Side Checking

### Using Server SDK

```typescript
import { Recur } from 'recur-tw/server'

const recur = new Recur(process.env.RECUR_SECRET_KEY!)

// In API route or server action
async function checkAccess(userEmail: string) {
  const { allowed, entitlement } = await recur.entitlements.check({
    product: 'pro-plan',
    customer: { email: userEmail },
  })

  if (!allowed) {
    throw new Error('Upgrade required')
  }

  return entitlement
}
```

### Using REST API Directly

```typescript
// GET /api/v1/customers/entitlements
const response = await fetch(
  `https://api.recur.tw/v1/customers/entitlements?email=${encodeURIComponent(email)}`,
  {
    headers: {
      'X-Recur-Secret-Key': process.env.RECUR_SECRET_KEY!,
    },
  }
)

const { customer, subscription, entitlements } = await response.json()
```

## Common Patterns

### Paywall Component

```tsx
function Paywall({
  children,
  product,
  fallback
}: {
  children: React.ReactNode
  product: string
  fallback?: React.ReactNode
}) {
  const { check, isLoading } = useCustomer()

  if (isLoading) {
    return <div>Loading...</div>
  }

  const { allowed } = check(product)

  if (!allowed) {
    return fallback || <UpgradePrompt product={product} />
  }

  return <>{children}</>
}

// Usage
<Paywall product="pro-plan">
  <PremiumDashboard />
</Paywall>
```

### Feature Flag Style

```tsx
function useFeature(featureProduct: string) {
  const { check, isLoading } = useCustomer()

  if (isLoading) {
    return { enabled: false, loading: true }
  }

  const { allowed, entitlement } = check(featureProduct)

  return {
    enabled: allowed,
    loading: false,
    entitlement,
    isTrial: entitlement?.status === 'trialing',
    isPastDue: entitlement?.status === 'past_due',
  }
}

// Usage
function MyComponent() {
  const { enabled, isTrial } = useFeature('pro-plan')

  if (!enabled) return <UpgradeButton />

  return (
    <>
      {isTrial && <TrialBanner />}
      <ProFeature />
    </>
  )
}
```

### API Middleware

```typescript
// middleware/requireSubscription.ts
import { Recur } from 'recur-tw/server'

const recur = new Recur(process.env.RECUR_SECRET_KEY!)

export async function requireSubscription(
  req: Request,
  product: string
) {
  const userEmail = await getUserEmail(req) // Your auth logic

  const { allowed, denial } = await recur.entitlements.check({
    product,
    customer: { email: userEmail },
  })

  if (!allowed) {
    throw new Response(JSON.stringify({
      error: 'Subscription required',
      reason: denial?.reason, // 'no_customer', 'no_entitlement', etc.
    }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    })
  }
}

// Usage in API route
export async function GET(req: Request) {
  await requireSubscription(req, 'pro-plan')

  // User has access, continue...
  return Response.json({ data: 'premium content' })
}
```

### Multiple Product Tiers

```tsx
function PricingGate() {
  const { check } = useCustomer()

  const hasPro = check('pro-plan').allowed
  const hasEnterprise = check('enterprise-plan').allowed

  if (hasEnterprise) {
    return <EnterpriseDashboard />
  }

  if (hasPro) {
    return <ProDashboard />
  }

  return <FreeDashboard />
}
```

## Handling Edge Cases

### Past Due Subscriptions

```tsx
const { allowed, entitlement } = check('pro-plan')

if (allowed && entitlement?.status === 'past_due') {
  // Show warning but allow access during grace period
  return (
    <>
      <PaymentFailedBanner />
      <PremiumContent />
    </>
  )
}
```

### Trial Subscriptions

```tsx
const { entitlement } = check('pro-plan')

if (entitlement?.status === 'trialing') {
  const trialEnds = new Date(entitlement.expiresAt!)
  const daysLeft = Math.ceil((trialEnds - Date.now()) / (1000 * 60 * 60 * 24))

  return <TrialBanner daysLeft={daysLeft} />
}
```

### Cancelled but Active

```tsx
const { entitlement } = check('pro-plan')

if (entitlement?.status === 'canceled') {
  // User cancelled but still has access until period end
  return (
    <>
      <ResubscribeBanner expiresAt={entitlement.expiresAt} />
      <PremiumContent />
    </>
  )
}
```

## Denial Reasons

When `allowed` is `false`, check the denial reason:

```typescript
const { allowed, denial } = check('pro-plan')

if (!allowed) {
  switch (denial?.reason) {
    case 'no_customer':
      // Customer not found
      return <CreateAccountPrompt />

    case 'no_entitlement':
      // No subscription to this product
      return <SubscribePrompt />

    case 'expired':
      // Subscription/access expired
      return <RenewPrompt />

    case 'insufficient_balance':
      // For credit-based products
      return <BuyCreditsPrompt />

    default:
      return <GenericUpgradePrompt />
  }
}
```

## Best Practices

1. **Use cached checks for UI** - Fast rendering, good UX
2. **Use live checks for actions** - Ensure fresh data for important operations
3. **Handle all statuses** - active, trialing, past_due, canceled
4. **Refetch after checkout** - Ensure UI updates after purchase
5. **Implement graceful degradation** - Show upgrade prompts, not errors

## Related Skills

- `/recur-quickstart` - Initial SDK setup
- `/recur-checkout` - Implement purchase flows
- `/recur-webhooks` - Sync entitlements with webhooks
