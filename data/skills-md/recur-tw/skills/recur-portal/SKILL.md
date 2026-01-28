---
name: recur-portal
description: Implement Customer Portal for subscription self-service. Use when building account pages, letting customers manage subscriptions, update payment methods, view billing history, or when user mentions "customer portal", "帳戶管理", "訂閱管理", "更新付款方式", "self-service".
license: MIT
metadata:
  author: recur
  version: "0.0.7"
---

# Recur Customer Portal Integration

You are helping implement Recur's Customer Portal, which allows subscribers to self-manage their subscriptions without contacting support.

## What is Customer Portal?

Customer Portal is a hosted page where your customers can:
- View active subscriptions and billing history
- Update payment methods
- Cancel or reactivate subscriptions
- Switch between plans (upgrade/downgrade)

## When to Use

| Scenario | Solution |
|----------|----------|
| "Add account management page" | Create portal session and redirect |
| "Let users update their card" | Portal handles payment method updates |
| "Users need to cancel subscription" | Portal provides self-service cancellation |
| "Show billing history" | Portal displays invoices and payments |

## Quick Start: Create Portal Session

Portal sessions are created server-side (requires Secret Key).

### Using Server SDK

```typescript
import { Recur } from 'recur-tw/server'

const recur = new Recur(process.env.RECUR_SECRET_KEY!)

// Create portal session - identify customer by email, ID, or externalId
const session = await recur.portal.sessions.create({
  email: 'customer@example.com',  // or customer: 'cus_xxx' or externalId: 'user_123'
  returnUrl: 'https://yourapp.com/account',
})

// Redirect customer to portal
redirect(session.url)
```

### Customer Identification

You can identify customers using one of these methods (in priority order):

```typescript
// By Recur customer ID (highest priority)
await recur.portal.sessions.create({
  customer: 'cus_xxx',
  returnUrl: 'https://yourapp.com/account',
})

// By your system's user ID
await recur.portal.sessions.create({
  externalId: 'user_123',
  returnUrl: 'https://yourapp.com/account',
})

// By email (lowest priority)
await recur.portal.sessions.create({
  email: 'customer@example.com',
  returnUrl: 'https://yourapp.com/account',
})
```

## Next.js Implementation

### API Route (App Router)

```typescript
// app/api/portal/route.ts
import { Recur } from 'recur-tw/server'
import { auth } from '@/lib/auth'  // Your auth solution
import { NextResponse } from 'next/server'

const recur = new Recur(process.env.RECUR_SECRET_KEY!)

export async function POST() {
  const session = await auth()

  if (!session?.user?.email) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  try {
    const portalSession = await recur.portal.sessions.create({
      email: session.user.email,
      returnUrl: `${process.env.NEXT_PUBLIC_APP_URL}/account`,
    })

    return NextResponse.json({ url: portalSession.url })
  } catch (error) {
    console.error('Portal session error:', error)
    return NextResponse.json(
      { error: 'Failed to create portal session' },
      { status: 500 }
    )
  }
}
```

### Server Action

```typescript
// app/actions/portal.ts
'use server'

import { Recur } from 'recur-tw/server'
import { auth } from '@/lib/auth'
import { redirect } from 'next/navigation'

const recur = new Recur(process.env.RECUR_SECRET_KEY!)

export async function openPortal() {
  const session = await auth()

  if (!session?.user?.email) {
    throw new Error('Unauthorized')
  }

  const portalSession = await recur.portal.sessions.create({
    email: session.user.email,
    returnUrl: `${process.env.NEXT_PUBLIC_APP_URL}/account`,
  })

  redirect(portalSession.url)
}
```

### Portal Button Component

```tsx
// components/portal-button.tsx
'use client'

import { useState } from 'react'

export function PortalButton() {
  const [isLoading, setIsLoading] = useState(false)

  const handleClick = async () => {
    setIsLoading(true)
    try {
      const response = await fetch('/api/portal', { method: 'POST' })
      const { url, error } = await response.json()

      if (error) throw new Error(error)

      window.location.href = url
    } catch (error) {
      console.error('Failed to open portal:', error)
      alert('無法開啟帳戶管理頁面，請稍後再試')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <button onClick={handleClick} disabled={isLoading}>
      {isLoading ? '載入中...' : '管理訂閱'}
    </button>
  )
}
```

### Using Server Action with Button

```tsx
// components/portal-button-action.tsx
'use client'

import { openPortal } from '@/app/actions/portal'

export function PortalButton() {
  return (
    <form action={openPortal}>
      <button type="submit">管理訂閱</button>
    </form>
  )
}
```

## Portal Session Response

```typescript
interface PortalSession {
  id: string              // Session ID (e.g., 'portal_sess_xxx')
  object: 'portal.session'
  url: string             // URL to redirect customer to
  customer: string        // Customer ID
  returnUrl: string       // URL to return after portal exit
  status: 'active' | 'expired'
  expiresAt: string       // ISO 8601 (sessions last 1 hour)
  accessedAt: string | null
  createdAt: string
}
```

## Using REST API Directly

If not using the SDK:

```typescript
const response = await fetch('https://api.recur.tw/v1/portal/sessions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.RECUR_SECRET_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'customer@example.com',
    return_url: 'https://yourapp.com/account',
  }),
})

const { url } = await response.json()
// Redirect to url
```

## Common Patterns

### Account Page with Portal Link

```tsx
// app/account/page.tsx
import { auth } from '@/lib/auth'
import { PortalButton } from '@/components/portal-button'

export default async function AccountPage() {
  const session = await auth()

  return (
    <div>
      <h1>帳戶設定</h1>
      <p>Email: {session?.user?.email}</p>

      <section>
        <h2>訂閱管理</h2>
        <p>管理您的訂閱、更新付款方式、查看帳單記錄</p>
        <PortalButton />
      </section>
    </div>
  )
}
```

### Conditional Portal Access

```tsx
// Only show portal button if user has subscription
function SubscriptionSection({ hasSubscription }: { hasSubscription: boolean }) {
  if (!hasSubscription) {
    return (
      <div>
        <p>您目前沒有訂閱</p>
        <a href="/pricing">查看方案</a>
      </div>
    )
  }

  return (
    <div>
      <p>您目前的訂閱：Pro 方案</p>
      <PortalButton />
    </div>
  )
}
```

## Portal Configuration

Configure portal behavior in Recur Dashboard → Settings → Customer Portal:

- **Default Return URL**: Where to redirect after leaving portal
- **Allowed Actions**: Enable/disable cancel, update payment, switch plan
- **Branding**: Custom logo and colors

## Security Notes

1. **Server-side only**: Portal sessions require Secret Key (sk_xxx)
2. **Short-lived**: Sessions expire in 1 hour
3. **One-time use**: Each session URL should only be used once
4. **Verify user**: Always authenticate the user before creating a portal session

## Error Handling

```typescript
try {
  const session = await recur.portal.sessions.create({
    email: userEmail,
    returnUrl: returnUrl,
  })
  redirect(session.url)
} catch (error) {
  if (error.code === 'customer_not_found') {
    // Customer doesn't exist in Recur
    // Maybe they haven't subscribed yet
    redirect('/pricing')
  }

  if (error.code === 'missing_return_url') {
    // returnUrl is required
    console.error('Missing return URL')
  }

  throw error
}
```

## Related Skills

- `/recur-quickstart` - Initial SDK setup
- `/recur-checkout` - Implement purchase flows
- `/recur-entitlements` - Check subscription access
