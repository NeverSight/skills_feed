---
name: recur-quickstart
description: Quick setup guide for Recur payment integration. Use when starting a new Recur integration, setting up API keys, installing the SDK, or when user mentions "integrate Recur", "setup Recur", "Recur 串接", "金流設定".
license: MIT
metadata:
  author: recur
  version: "0.0.7"
---

# Recur Quickstart

You are helping a developer integrate Recur, Taiwan's subscription payment platform (similar to Stripe Billing).

## Step 1: Install SDK

```bash
pnpm add recur-tw
# or
npm install recur-tw
```

## Step 2: Get API Keys

API keys are available in the Recur dashboard at `app.recur.tw` → Settings → Developers.

**Key formats:**
- `pk_test_xxx` - Publishable key (frontend, safe to expose)
- `sk_test_xxx` - Secret key (backend only, never expose)
- `pk_live_xxx` / `sk_live_xxx` - Production keys

**Environment variables to set:**
```bash
RECUR_PUBLISHABLE_KEY=pk_test_xxx
RECUR_SECRET_KEY=sk_test_xxx
```

## Step 3: Add Provider (React)

Wrap your app with `RecurProvider`:

```tsx
import { RecurProvider } from 'recur-tw'

export default function App({ children }) {
  return (
    <RecurProvider
      config={{
        publishableKey: process.env.NEXT_PUBLIC_RECUR_PUBLISHABLE_KEY,
      }}
    >
      {children}
    </RecurProvider>
  )
}
```

## Step 4: Create Your First Checkout

```tsx
import { useRecur } from 'recur-tw'

function PricingButton({ productId }: { productId: string }) {
  const { checkout } = useRecur()

  const handleCheckout = async () => {
    await checkout({
      productId,
      onPaymentComplete: (subscription) => {
        console.log('Payment successful!', subscription)
      },
      onPaymentFailed: (error) => {
        console.error('Payment failed:', error)
      },
    })
  }

  return <button onClick={handleCheckout}>Subscribe</button>
}
```

## Step 5: Set Up Webhooks

Create a webhook endpoint to receive payment notifications. See the `recur-webhooks` skill for detailed instructions.

## Quick Verification Checklist

- [ ] SDK installed (`pnpm list recur-tw`)
- [ ] Environment variables set
- [ ] RecurProvider wrapping app
- [ ] Test checkout works in sandbox
- [ ] Webhook endpoint configured

## Common Issues

### "Invalid API key"
- Check key format: must start with `pk_test_`, `sk_test_`, `pk_live_`, or `sk_live_`
- Ensure using publishable key for frontend, secret key for backend

### "Product not found"
- Verify product exists in Recur dashboard
- Check you're using correct environment (sandbox vs production)

### Checkout not appearing
- Ensure `RecurProvider` wraps your app
- Check browser console for errors
- Verify publishable key is correct

## Next Steps

- `/recur-checkout` - Learn checkout flow options
- `/recur-webhooks` - Set up payment notifications
- `/recur-entitlements` - Implement access control

## Resources

- [Recur Documentation](https://recur.tw/docs)
- [SDK on npm](https://www.npmjs.com/package/recur-tw)
- [API Reference](https://recur.tw/docs/api)
