---
name: recur-checkout
description: Implement Recur checkout flows including embedded, modal, and redirect modes. Use when adding payment buttons, checkout forms, subscription purchase flows, or when user mentions "checkout", "結帳", "付款按鈕", "embedded checkout".
license: MIT
metadata:
  author: recur
  version: "0.0.7"
---

# Recur Checkout Integration

You are helping implement Recur checkout flows. Recur supports multiple checkout modes for different use cases.

## Checkout Modes

| Mode | Best For | User Experience |
|------|----------|-----------------|
| `embedded` | SPA apps | Form renders inline in your page |
| `modal` | Quick purchases | Form appears in a dialog overlay |
| `redirect` | Simple integration | Full page redirect to Recur |

## Basic Implementation

### Using useRecur Hook

```tsx
import { useRecur } from 'recur-tw'

function CheckoutButton({ productId }: { productId: string }) {
  const { checkout, isLoading } = useRecur()

  const handleClick = async () => {
    await checkout({
      productId,
      // Or use productSlug: 'pro-plan'

      // Optional: Pre-fill customer info
      customerEmail: 'user@example.com',
      customerName: 'John Doe',

      // Optional: Link to your user system
      externalCustomerId: 'user_123',

      // Callbacks
      onPaymentComplete: (result) => {
        console.log('Success!', result)
        // result.id - Subscription/Order ID
        // result.status - 'ACTIVE', 'TRIALING', etc.
      },
      onPaymentFailed: (error) => {
        console.error('Failed:', error)
        return { action: 'retry' } // or 'close' or 'custom'
      },
      onPaymentCancel: () => {
        console.log('User cancelled')
      },
    })
  }

  return (
    <button onClick={handleClick} disabled={isLoading}>
      {isLoading ? 'Processing...' : 'Subscribe'}
    </button>
  )
}
```

### Using useSubscribe Hook (with state management)

```tsx
import { useSubscribe } from 'recur-tw'

function SubscribeButton({ productId }: { productId: string }) {
  const { subscribe, isLoading, error, subscription } = useSubscribe()

  const handleClick = () => {
    subscribe({
      productId,
      onPaymentComplete: (sub) => {
        // Subscription created successfully
        router.push('/dashboard')
      },
    })
  }

  if (subscription) {
    return <p>Subscribed! ID: {subscription.id}</p>
  }

  return (
    <>
      <button onClick={handleClick} disabled={isLoading}>
        Subscribe
      </button>
      {error && <p className="error">{error.message}</p>}
    </>
  )
}
```

## Embedded Mode Setup

For embedded mode, you need a container element:

```tsx
// In RecurProvider config
<RecurProvider
  config={{
    publishableKey: process.env.NEXT_PUBLIC_RECUR_PUBLISHABLE_KEY,
    checkoutMode: 'embedded',
    containerElementId: 'recur-checkout-container',
  }}
>
  {children}
</RecurProvider>

// In your checkout page
function CheckoutPage() {
  return (
    <div>
      <h1>Complete Your Purchase</h1>
      {/* Recur will render the payment form here */}
      <div id="recur-checkout-container" />
    </div>
  )
}
```

## Handling 3D Verification

Recur handles 3D Secure automatically. For mobile apps or specific flows:

```tsx
await checkout({
  productId,
  // These URLs are used when 3D verification requires redirect
  successUrl: 'https://yourapp.com/checkout/success',
  cancelUrl: 'https://yourapp.com/checkout/cancel',
})
```

## Product Types

Recur supports different product types:

```tsx
// Subscription (recurring)
checkout({ productId: 'prod_subscription_xxx' })

// One-time purchase
checkout({ productId: 'prod_onetime_xxx' })

// Credits (prepaid wallet)
checkout({ productId: 'prod_credits_xxx' })

// Donation (variable amount)
checkout({ productId: 'prod_donation_xxx' })
```

## Listing Products

```tsx
import { useProducts } from 'recur-tw'

function PricingPage() {
  const { products, isLoading } = useProducts({
    type: 'SUBSCRIPTION', // Filter by type
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div className="pricing-grid">
      {products.map(product => (
        <PricingCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

## Payment Failed Handling

```tsx
onPaymentFailed: (error) => {
  // error.code tells you what went wrong
  switch (error.code) {
    case 'CARD_DECLINED':
      return { action: 'retry' }
    case 'INSUFFICIENT_FUNDS':
      return {
        action: 'custom',
        customTitle: '餘額不足',
        customMessage: '請使用其他付款方式',
      }
    default:
      return { action: 'close' }
  }
}
```

## Server-Side Checkout (API)

For server-rendered apps or custom flows:

```typescript
// Create checkout session
const response = await fetch('https://api.recur.tw/v1/checkouts', {
  method: 'POST',
  headers: {
    'X-Recur-Secret-Key': process.env.RECUR_SECRET_KEY,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    productId: 'prod_xxx',
    customerEmail: 'user@example.com',
    successUrl: 'https://yourapp.com/success',
    cancelUrl: 'https://yourapp.com/cancel',
  }),
})

const { checkoutUrl } = await response.json()
// Redirect user to checkoutUrl
```

## Checkout Result Structure

```typescript
interface CheckoutResult {
  id: string              // Subscription or Order ID
  status: string          // 'ACTIVE', 'TRIALING', 'PENDING'
  productId: string
  amount: number          // In cents (e.g., 29900 = NT$299)
  billingPeriod?: string  // 'MONTHLY', 'YEARLY' for subscriptions
  currentPeriodEnd?: string  // ISO date
  trialEndsAt?: string    // ISO date if trial
}
```

## Best Practices

1. **Always handle all callbacks** - onPaymentComplete, onPaymentFailed, onPaymentCancel
2. **Show loading states** - Use isLoading to disable buttons during checkout
3. **Pre-fill customer info** - Reduces friction if you already have user data
4. **Use externalCustomerId** - Links Recur customers to your user system
5. **Test in sandbox first** - Use `pk_test_` keys during development

## Related Skills

- `/recur-quickstart` - Initial SDK setup
- `/recur-webhooks` - Receive payment notifications
- `/recur-entitlements` - Check subscription access
