---
name: outlit-sdk
description: Integrate Outlit SDK for customer journey tracking and analytics. Triggers when users need to add Outlit to React, Next.js, Vue, Svelte, Angular, Astro, Node.js, Express, or Fastify apps. Covers SDK installation (@outlit/browser, @outlit/node), auth provider integration (Clerk, NextAuth, Supabase, Auth0, Firebase), GDPR consent management, event tracking, user lifecycle events (activate, engaged, inactive), customer billing status (trialing, paid, churned), and Stripe webhook integration.
---

# Outlit Integration

Guides complete integration of Outlit SDK into web applications and Node.js servers, from installation through production deployment.

## Overview

Outlit is a customer journey platform that tracks users from anonymous visitors through their complete lifecycle as paying customers. This skill helps integrate the Outlit SDK by:

1. Analyzing the project structure
2. Installing the appropriate SDK package
3. Setting up framework-specific configuration
4. Integrating with authentication providers
5. Implementing consent management (GDPR compliance)
6. Adding custom event tracking

## Installation

To add this skill to your Claude Code environment:

```sh
npx add-skill outlitai/outlit-agent-skills
# or
bunx add-skill outlitai/outlit-agent-skills
```

## Integration Workflow

### Step 1: Analyze Project

Run the project detection script to understand the environment:

```bash
python scripts/detect_project.py [project_path]
```

This detects:
- Framework (React, Next.js, Vue, Node.js, etc.)
- Package manager (npm, yarn, pnpm, bun)
- TypeScript vs JavaScript
- Existing auth provider
- Current Outlit installation

**Use the detection results to guide all subsequent steps.**

### Step 2: Install SDK

Use the installation script or manual installation:

```bash
# Using script
./scripts/install_sdk.sh @outlit/browser

# Or manually with detected package manager
npm install @outlit/browser    # For browser apps
npm install @outlit/node       # For Node.js servers
npm install @outlit/core       # For custom implementations
```

**Package Selection:**
- `@outlit/browser` — React, Next.js, Vue, Svelte, Angular, static sites
- `@outlit/node` — Express, Fastify, NestJS, serverless functions
- `@outlit/core` — Custom implementations, shared utilities

### Step 3: Add Public Key

Users need to add their Outlit public key to environment variables:

**Browser apps:**
```bash
# .env.local or .env
NEXT_PUBLIC_OUTLIT_KEY=pk_xxx      # Next.js
REACT_APP_OUTLIT_KEY=pk_xxx        # Create React App
VITE_OUTLIT_KEY=pk_xxx             # Vite
```

**Server apps:**
```bash
# .env
OUTLIT_KEY=pk_xxx
```

Users get their public key from Outlit dashboard → Settings → Website Tracking.

### Step 4: Framework-Specific Setup

Choose the appropriate setup based on the detected framework. See [frameworks.md](references/frameworks.md) for complete patterns.

#### React

Copy template from `assets/react/OutlitProvider.tsx` and modify as needed:

```tsx
import { OutlitProvider } from '@outlit/browser/react'

function App() {
  return (
    <OutlitProvider publicKey={import.meta.env.VITE_OUTLIT_KEY}>
      <YourApp />
    </OutlitProvider>
  )
}
```

#### Next.js App Router

Copy template from `assets/nextjs/layout.tsx`:

```tsx
// app/layout.tsx
import { OutlitProvider } from '@outlit/browser/react'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <OutlitProvider publicKey={process.env.NEXT_PUBLIC_OUTLIT_KEY!}>
          {children}
        </OutlitProvider>
      </body>
    </html>
  )
}
```

#### Next.js Pages Router

Copy template from `assets/nextjs/_app.tsx`.

#### Node.js / Express

Copy templates from `assets/node/`:
- `outlit.config.ts` — Core configuration
- `express-middleware.ts` — Express middleware (if using Express)

For other frameworks, consult [frameworks.md](references/frameworks.md) reference.

### Step 5: Auth Integration (If Detected)

If an auth provider was detected, integrate it with Outlit. See [auth-providers.md](references/auth-providers.md) for patterns.

**Common pattern:**

```tsx
<OutlitProvider
  publicKey="pk_xxx"
  user={currentUser ? {
    email: currentUser.email,
    userId: currentUser.id,
    traits: { name: currentUser.name }
  } : null}
>
  {children}
</OutlitProvider>
```

**Supported auth providers:**
- Clerk
- NextAuth / Auth.js
- Supabase
- Auth0
- Firebase Auth
- Custom solutions

### Step 6: Consent Management (Optional)

For GDPR compliance, implement consent management. See [consent-management.md](references/consent-management.md).

**Basic pattern:**

```tsx
<OutlitProvider
  publicKey="pk_xxx"
  autoTrack={hasConsent}  // Only track if consent granted
>
  {!hasConsent && <ConsentBanner />}
  {children}
</OutlitProvider>
```

Copy `assets/react/ConsentBanner.tsx` template for a ready-to-use consent banner.

### Step 7: Custom Event Tracking

Help users implement custom event tracking based on their needs.

**Browser example:**

```tsx
import { useOutlit } from '@outlit/browser/react'

function MyComponent() {
  const { track, user } = useOutlit()

  const handleUpgrade = () => {
    track('subscription_upgraded', { plan: 'pro' })
    user.activate({ milestone: 'upgraded' })
  }

  return <button onClick={handleUpgrade}>Upgrade</button>
}
```

**Server example:**

```ts
import { outlit } from '@/lib/outlit'

outlit.track({
  email: 'user@example.com',
  eventName: 'subscription_created',
  properties: { plan: 'pro' }
})

await outlit.flush()
```

See [patterns.md](references/patterns.md) for event taxonomy and best practices.

### Step 8: Verify Installation

Guide users to verify the installation:

1. **Check Network Tab:**
   - Open DevTools → Network
   - Look for requests to `app.outlit.ai/api/i/v1/...`
   - Status 200 = working correctly

2. **Check Outlit Dashboard:**
   - Visit Outlit dashboard
   - Navigate to Events or Live View
   - Verify events appear in real-time

3. **Test Key Features:**
   - Pageviews (automatic)
   - Form submissions (automatic if enabled)
   - Custom events (manual tracking)
   - User identification

## Common Customizations

### Custom Tracking Hook

For React apps, copy `assets/react/useTracking.ts` for a custom hook with common tracking operations.

### Server-Side Webhooks

For billing integration, copy `assets/node/stripe-webhook.ts` as a starting point for Stripe webhooks.

Modify for other providers (Paddle, Chargebee, etc.) following the same pattern:
- Extract customer email/ID
- Track billing events
- Update customer status (trialing, paid, churned)
- Always flush before response

### API Routes

For Next.js apps, copy `assets/nextjs/api-route.ts` or `assets/nextjs/server-action.ts` for server-side tracking.

## Troubleshooting

### No Events in Dashboard

1. Verify public key has correct framework prefix (`NEXT_PUBLIC_`, `VITE_`, `REACT_APP_`)
2. Confirm `OutlitProvider` wraps entire app
3. Check `isTrackingEnabled()` if using consent management
4. Network tab: requests should go to `app.outlit.ai/api/i/v1/...`

### Events Not Linked to Users

Call `identify()` or `setUser()` immediately after signup/login.

### Server-Side Events Missing

Always `await outlit.flush()` before function returns (especially serverless).

## Quick Reference

For complete API documentation, see [api-reference.md](references/api-reference.md).

**Key imports:**

```ts
// Browser (React)
import { OutlitProvider, useOutlit } from '@outlit/browser/react'

// Node.js
import { Outlit } from '@outlit/node'
```

## Resources

### References

Load these references as needed for detailed guidance:

- **[frameworks.md](references/frameworks.md)** — Framework-specific integration patterns (React, Next.js, Vue, Express, etc.)
- **[auth-providers.md](references/auth-providers.md)** — Auth provider integration (Clerk, NextAuth, Supabase, Auth0, etc.)
- **[consent-management.md](references/consent-management.md)** — GDPR-compliant consent management patterns
- **[api-reference.md](references/api-reference.md)** — Complete API reference for all SDK methods
- **[patterns.md](references/patterns.md)** — Best practices, event taxonomy, webhooks, error handling

### Scripts

- **`detect_project.py`** — Analyze project structure and environment
- **`install_sdk.sh`** — Install Outlit SDK with detected package manager

### Templates

Ready-to-use code templates in `assets/`:

- **`react/`** — OutlitProvider, useTracking hook, ConsentBanner
- **`nextjs/`** — App Router layout, Pages Router _app, API routes, Server Actions
- **`node/`** — Configuration, Express middleware, Stripe webhooks

## Best Practices

1. **Identify Early**: Call `identify()` as soon as user info is available
2. **Include Both IDs**: Provide both email and userId for identity resolution
3. **Flush in Serverless**: Always `await outlit.flush()` before function exits
4. **Track Lifecycle**: Use `user.activate()`, `customer.paid()` for milestones
5. **Use snake_case**: Event names like `subscription_created`, not `SubscriptionCreated`

## Implementation Checklist

Use this checklist to ensure complete integration:

- [ ] SDK installed (`@outlit/browser` or `@outlit/node`)
- [ ] Public key added to environment variables
- [ ] Provider/initialization added to root component/file
- [ ] Auth integration implemented (if applicable)
- [ ] Consent management added (for EU users)
- [ ] Custom events identified and implemented
- [ ] User lifecycle events added (activate, paid, churned)
- [ ] Installation verified in dashboard
- [ ] TypeScript types working correctly
- [ ] Error handling implemented
- [ ] Documentation added for team

