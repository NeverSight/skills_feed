---
name: clerk-auth
description: "Clerk authentication integration patterns for Next.js and Convex. Invoke for: user authentication, session management, JWT templates, webhook handling, middleware configuration, protected routes, Convex auth integration."
---

# Clerk Authentication Patterns

Authentication integration patterns for Clerk with Next.js and Convex backends.

## Core Concepts

### Authentication Flow
1. User authenticates via Clerk (sign-in/sign-up)
2. Clerk issues session token (JWT)
3. Frontend passes token to backend
4. Backend verifies token and extracts user identity

### Key Components
- **Clerk Dashboard**: User management, JWT templates, webhooks
- **@clerk/nextjs**: React hooks, middleware, components
- **Convex auth**: `ctx.auth.getUserIdentity()` for backend verification

## Next.js Setup

### Middleware

```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'

const isPublicRoute = createRouteMatcher([
  '/',
  '/sign-in(.*)',
  '/sign-up(.*)',
  '/api/webhooks(.*)',  // Webhooks must be public
])

export default clerkMiddleware((auth, req) => {
  if (!isPublicRoute(req)) {
    auth().protect()
  }
})

export const config = {
  matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'],
}
```

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxx
CLERK_SECRET_KEY=sk_test_xxx
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
```

**Critical**: Set on BOTH Vercel and local. Mismatch causes silent failures.

## Convex Integration

### JWT Template (Clerk Dashboard)

Create JWT template named `convex`:

```json
{
  "sub": "{{user.id}}",
  "iss": "https://clerk.your-domain.com",
  "email": "{{user.primary_email_address}}",
  "name": "{{user.full_name}}"
}
```

**Template name is case-sensitive.** Must match `convex/auth.config.ts`.

### Convex Auth Config

```typescript
// convex/auth.config.ts
export default {
  providers: [
    {
      domain: process.env.CLERK_JWT_ISSUER_DOMAIN,
      applicationID: "convex",
    },
  ],
}
```

### Backend User Identity

```typescript
// convex/users.ts
import { query, mutation } from "./_generated/server"

export const getCurrentUser = query({
  handler: async (ctx) => {
    const identity = await ctx.auth.getUserIdentity()
    if (!identity) return null

    // identity contains JWT claims:
    // - subject (Clerk user ID)
    // - email
    // - name
    return identity
  },
})
```

## Webhook Handling

### Webhook URL
Configure in Clerk Dashboard → Webhooks:
- URL: `https://your-app.com/api/webhooks/clerk`
- Events: `user.created`, `user.updated`, `user.deleted`

### Webhook Handler

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from 'svix'
import { headers } from 'next/headers'
import { WebhookEvent } from '@clerk/nextjs/server'

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET

  if (!WEBHOOK_SECRET) {
    throw new Error('Missing CLERK_WEBHOOK_SECRET')
  }

  const headerPayload = headers()
  const svix_id = headerPayload.get('svix-id')
  const svix_timestamp = headerPayload.get('svix-timestamp')
  const svix_signature = headerPayload.get('svix-signature')

  if (!svix_id || !svix_timestamp || !svix_signature) {
    return new Response('Missing svix headers', { status: 400 })
  }

  const payload = await req.json()
  const body = JSON.stringify(payload)

  const wh = new Webhook(WEBHOOK_SECRET)
  let evt: WebhookEvent

  try {
    evt = wh.verify(body, {
      'svix-id': svix_id,
      'svix-timestamp': svix_timestamp,
      'svix-signature': svix_signature,
    }) as WebhookEvent
  } catch (err) {
    console.error('Webhook verification failed:', err)
    return new Response('Invalid signature', { status: 400 })
  }

  // Handle events
  switch (evt.type) {
    case 'user.created':
      // Sync user to database
      break
    case 'user.updated':
      // Update user in database
      break
    case 'user.deleted':
      // Handle user deletion
      break
  }

  return new Response('OK', { status: 200 })
}
```

## Common Issues

### "Unauthenticated" errors
1. Check JWT template name matches config
2. Verify `CLERK_JWT_ISSUER_DOMAIN` is set
3. Ensure middleware isn't blocking auth routes

### Webhook failures
1. Verify `CLERK_WEBHOOK_SECRET` is set (not just locally)
2. Check webhook URL uses canonical domain (no redirects)
3. Ensure `/api/webhooks/*` is in public routes

### Session not persisting
1. Check cookies are being set (dev tools)
2. Verify domain configuration in Clerk Dashboard
3. Ensure HTTPS in production

## Best Practices

- **Sync users via webhooks**, not on-demand
- **Store Clerk ID** as foreign key in your database
- **Use `currentUser()`** for server components
- **Use `useUser()`** for client components
- **Protect API routes** with `auth()` in route handlers
- **Keep JWT templates minimal** (only needed claims)

## References

- `references/convex-integration.md` — Detailed Convex auth patterns
- `references/webhook-events.md` — Clerk webhook event types
- `references/troubleshooting.md` — Common issues and solutions

## Related Skills

- `billing-security` — Payment and auth security patterns
- `external-integration-patterns` — General external service integration
- `env-var-hygiene` — Environment variable management
