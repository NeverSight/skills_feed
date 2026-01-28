---
name: clerk-nextjs-skills
description: Clerk authentication for Next.js 16 (App Router only) with proxy.ts setup, migration from middleware.ts, environment configuration, and MCP server integration.
---

## Links

- [Clerk Next.js Quickstart](https://clerk.com/docs/nextjs/getting-started/quickstart)
- [Clerk MCP Server Guide](https://clerk.com/docs/nextjs/guides/ai/mcp/build-mcp-server)
- [Clerk Next.js SDK Reference](https://clerk.com/docs/reference/nextjs/overview)
- [clerkMiddleware() Reference](https://clerk.com/docs/reference/nextjs/clerk-middleware)
- [Reading User Data](https://clerk.com/docs/nextjs/guides/users/reading)
- [Protecting Routes](https://clerk.com/docs/reference/nextjs/clerk-middleware)
- [OAuth Token Verification](https://clerk.com/docs/nextjs/guides/development/verifying-oauth-access-tokens)
- [Clerk Dashboard](https://dashboard.clerk.com/)
- [@vercel/mcp-adapter](https://github.com/vercel/mcp-adapter)
- [@clerk/mcp-tools](https://github.com/clerk/mcp-tools)
- [MCP Example Repository](https://github.com/clerk/mcp-nextjs-example)

## Quick Start

### 1. Install Dependencies (Using pnpm)

```bash
pnpm add @clerk/nextjs
# For MCP server integration, also install:
pnpm add @vercel/mcp-adapter @clerk/mcp-tools
```

### 2. Create proxy.ts (Next.js 16)

The `proxy.ts` file replaces `middleware.ts` from Next.js 15. Create it at the root or in `/src`:

```typescript
// proxy.ts (or src/proxy.ts)
import { clerkMiddleware } from '@clerk/nextjs/server'

export default clerkMiddleware()

export const config = {
  matcher: [
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    '/(api|trpc)(.*)',
  ],
}
```

### 3. Set Environment Variables

Create `.env.local` in your project root:

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_publishable_key_here
CLERK_SECRET_KEY=your_secret_key_here
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/
```

### 4. Add ClerkProvider to Layout

```typescript
// app/layout.tsx
import {
  ClerkProvider,
  SignInButton,
  SignUpButton,
  SignedIn,
  SignedOut,
  UserButton,
} from '@clerk/nextjs'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'My App',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header className="flex justify-end items-center p-4 gap-4 h-16">
            <SignedOut>
              <SignInButton />
              <SignUpButton />
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  )
}
```

### 5. Run Your App

```bash
pnpm dev
```

Visit `http://localhost:3000` and click "Sign Up" to create your first user.

## Key Concepts

### proxy.ts vs middleware.ts

- **Next.js 16 (App Router)**: Use `proxy.ts` for Clerk middleware
- **Next.js ≤15**: Use `middleware.ts` with identical code (filename only differs)
- Clerk's `clerkMiddleware()` function is the same regardless of filename
- The `matcher` configuration ensures proper route handling and performance

### Protecting Routes

By default, `clerkMiddleware()` does not protect routes—all are public. Use `auth.protect()` to require authentication:

```typescript
// Protect specific route
import { auth } from '@clerk/nextjs/server'

export default async function Page() {
  const { userId } = await auth()
  
  if (!userId) {
    // Redirect handled by clerkMiddleware
  }
  
  return <div>Protected content for {userId}</div>
}
```

Or protect all routes in `proxy.ts`:

```typescript
import { clerkMiddleware } from '@clerk/nextjs/server'

export default clerkMiddleware(async (auth, req) => {
  await auth.protect()
})
```

### Environment Variable Validation

Check for required Clerk keys before runtime:

```typescript
// lib/clerk-config.ts
export function validateClerkEnv() {
  const required = [
    'NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY',
    'CLERK_SECRET_KEY',
  ]
  
  const missing = required.filter(key => !process.env[key])
  
  if (missing.length > 0) {
    throw new Error(`Missing required Clerk environment variables: ${missing.join(', ')}`)
  }
}
```

### Accessing User Data

Use Clerk hooks in client components:

```typescript
// app/components/user-profile.tsx
'use client'

import { useUser } from '@clerk/nextjs'

export function UserProfile() {
  const { user, isLoaded } = useUser()
  
  if (!isLoaded) return <div>Loading...</div>
  
  if (!user) return <div>Not signed in</div>
  
  return (
    <div>
      <h1>{user.fullName}</h1>
      <p>{user.primaryEmailAddress?.emailAddress}</p>
    </div>
  )
}
```

Or in server components/actions:

```typescript
// app/actions.ts
'use server'

import { auth, clerkClient } from '@clerk/nextjs/server'

export async function getUserData() {
  const { userId } = await auth()
  
  if (!userId) {
    throw new Error('Unauthorized')
  }
  
  const clerk = await clerkClient()
  const user = await clerk.users.getUser(userId)
  
  return user
}
```

## Migrating from middleware.ts (Next.js 15) to proxy.ts (Next.js 16)

### Step-by-Step Migration

1. **Rename the file** from `middleware.ts` to `proxy.ts` (location remains same: root or `/src`)

2. **Keep the code identical** - No functional changes needed:
   ```typescript
   // Before (middleware.ts)
   import { clerkMiddleware } from '@clerk/nextjs/server'
   export default clerkMiddleware()
   export const config = { ... }
   
   // After (proxy.ts) - Same code
   import { clerkMiddleware } from '@clerk/nextjs/server'
   export default clerkMiddleware()
   export const config = { ... }
   ```

3. **Update Next.js version**:
   ```bash
   pnpm add next@latest
   ```

4. **Verify environment variables** are still in `.env.local` (no changes needed)

5. **Test the migration**:
   ```bash
   pnpm dev
   ```

### Troubleshooting Migration

- If routes aren't protected, ensure `proxy.ts` is in the correct location (root or `/src`)
- Check that `.env.local` has all required Clerk keys
- Clear `.next` cache if middleware changes don't take effect: `rm -rf .next && pnpm dev`
- Verify Next.js version is 16.0+: `pnpm list next`

## Building an MCP Server with Clerk

See [CLERK_MCP_SERVER_SETUP.md](references/CLERK_MCP_SERVER_SETUP.md) for complete MCP server integration.

### Quick MCP Setup Summary

1. **Install MCP dependencies**:
   ```bash
   pnpm add @vercel/mcp-adapter @clerk/mcp-tools
   ```

2. **Create MCP route** at `app/[transport]/route.ts`:
   ```typescript
   import { verifyClerkToken } from '@clerk/mcp-tools/next'
   import { createMcpHandler, withMcpAuth } from '@vercel/mcp-adapter'
   import { auth, clerkClient } from '@clerk/nextjs/server'
   
   const clerk = await clerkClient()
   
   const handler = createMcpHandler((server) => {
     server.tool(
       'get-clerk-user-data',
       'Gets data about the Clerk user that authorized this request',
       {},
       async (_, { authInfo }) => {
         const userId = authInfo!.extra!.userId! as string
         const userData = await clerk.users.getUser(userId)
         return {
           content: [{ type: 'text', text: JSON.stringify(userData) }],
         }
       },
     )
   })
   
   const authHandler = withMcpAuth(
     handler,
     async (_, token) => {
       const clerkAuth = await auth({ acceptsToken: 'oauth_token' })
       return verifyClerkToken(clerkAuth, token)
     },
     {
       required: true,
       resourceMetadataPath: '/.well-known/oauth-protected-resource/mcp',
     },
   )
   
   export { authHandler as GET, authHandler as POST }
   ```

3. **Expose OAuth metadata endpoints** (see references for complete setup)

4. **Update proxy.ts** to exclude `.well-known` endpoints:
   ```typescript
   import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server'
   
   const isPublicRoute = createRouteMatcher([
     '/.well-known/oauth-authorization-server(.*)',
     '/.well-known/oauth-protected-resource(.*)',
   ])
   
   export default clerkMiddleware(async (auth, req) => {
     if (isPublicRoute(req)) return
     await auth.protect()
   })
   ```

5. **Enable Dynamic Client Registration** in [Clerk Dashboard](https://dashboard.clerk.com/~/oauth-applications)

## Best Practices

### 1. Environment Variable Management

- Always use `.env.local` for development (never commit sensitive keys)
- Validate environment variables on application startup
- Use `NEXT_PUBLIC_` prefix ONLY for non-sensitive keys that are safe to expose
- For production, set environment variables in your deployment platform (Vercel, etc.)

### 2. Route Protection Strategies

```typescript
// Option A: Protect all routes
export default clerkMiddleware(async (auth, req) => {
  await auth.protect()
})

// Option B: Protect specific routes
import { createRouteMatcher } from '@clerk/nextjs/server'

const isProtectedRoute = createRouteMatcher(['/dashboard(.*)', '/api/user(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect()
  }
})

// Option C: Public routes with opt-in protection
const isPublicRoute = createRouteMatcher(['/sign-in(.*)', '/sign-up(.*)'])

export default clerkMiddleware(async (auth, req) => {
  if (!isPublicRoute(req)) {
    await auth.protect()
  }
})
```

### 3. MCP Server Security

- Enable **Dynamic Client Registration** in Clerk Dashboard
- Keep `.well-known` endpoints public but protect all MCP tools with OAuth
- Use `acceptsToken: 'oauth_token'` in `auth()` to require machine tokens
- OAuth tokens are free during public beta (pricing TBD)
- Always verify tokens with `verifyClerkToken()` before exposing user data

### 4. Performance & Caching

- Use `clerkClient()` for server-side user queries (cached automatically)
- Leverage React Server Components for secure user data access
- Cache user data when possible to reduce API calls
- Use `@clerk/nextjs` hooks only in Client Components (`'use client'`)

### 5. Production Deployment

- Set all environment variables in your deployment platform
- Use Clerk's production instance keys (not development keys)
- Test authentication flow in staging environment before production
- Monitor Clerk Dashboard for authentication errors
- Keep `@clerk/nextjs` updated: `pnpm update @clerk/nextjs`

## Troubleshooting

### Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Missing environment variables" | Ensure `.env.local` has `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY` |
| Middleware not protecting routes | Verify `proxy.ts` is in root or `/src` directory, not in `app/` |
| Sign-in/sign-up pages not working | Check `NEXT_PUBLIC_CLERK_SIGN_IN_URL` and `NEXT_PUBLIC_CLERK_SIGN_UP_URL` in `.env.local` |
| User data returns null | Ensure user is authenticated: check `userId` is not null before calling `getUser()` |
| MCP server OAuth fails | Enable Dynamic Client Registration in Clerk Dashboard OAuth Applications |
| Changes not taking effect | Clear `.next` cache: `rm -rf .next` and restart `pnpm dev` |
| "proxy.ts" not recognized | Verify Next.js version is 16.0+: `pnpm list next` |

### Common Next.js 16 Gotchas

- **File naming**: Must be `proxy.ts` (not `middleware.ts`) for Next.js 16
- **Location**: Place `proxy.ts` at project root or in `/src` directory, NOT in `app/`
- **Re-exports**: Config object must be exported from `proxy.ts` for matcher to work
- **Async operations**: `clerkMiddleware()` is async-ready; use `await auth.protect()` for route protection

### Debug Mode

Enable debug logging:

```typescript
// proxy.ts
import { clerkMiddleware } from '@clerk/nextjs/server'

export default clerkMiddleware((auth, req) => {
  if (process.env.DEBUG_CLERK) {
    console.log('Request URL:', req.nextUrl.pathname)
    console.log('User ID:', auth.sessionClaims?.sub)
  }
})
```

Run with debug:
```bash
DEBUG_CLERK=1 pnpm dev
```

## Related Skills

- **[mcp-server-skills](../mcp-server-skills/SKILL.md)**: General MCP server patterns with Vercel adapter
- **[nextjs16-skills](../nextjs16-skills/SKILL.MD)**: Next.js 16 features, breaking changes, and best practices
- **[authjs-skills](../authjs-skills/SKILL.md)**: Alternative authentication using Auth.js (Auth0, GitHub, etc.)

## Resources

- [Clerk Documentation](https://clerk.com/docs)
- [Clerk Support](https://clerk.com/contact/support)
- [Clerk Discord Community](https://clerk.com/discord)
- [Clerk Changelog](https://clerk.com/changelog)
- [Clerk Feedback](https://feedback.clerk.com/roadmap)
