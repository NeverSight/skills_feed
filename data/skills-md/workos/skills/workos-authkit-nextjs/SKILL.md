---
name: workos-authkit-nextjs
description: Integrate WorkOS AuthKit with Next.js App Router (13+). Server-side rendering required.
---

# WorkOS AuthKit for Next.js

## Step 1: Fetch SDK Documentation (BLOCKING)

**STOP. Do not proceed until complete.**

WebFetch: `https://github.com/workos/authkit-nextjs/blob/main/README.md`

The README is the source of truth. If this skill conflicts with README, follow README.

## Step 2: Pre-Flight Validation

### Project Structure

- Confirm `next.config.js` or `next.config.mjs` exists
- Confirm `package.json` contains `"next"` dependency

### Environment Variables

Check `.env.local` for:

- `WORKOS_API_KEY` - starts with `sk_`
- `WORKOS_CLIENT_ID` - starts with `client_`
- `NEXT_PUBLIC_WORKOS_REDIRECT_URI` - valid callback URL
- `WORKOS_COOKIE_PASSWORD` - 32+ characters

## Step 3: Install SDK

Detect package manager, install SDK package from README.

**Verify:** SDK package exists in node_modules before continuing.

## Step 4: Version Detection (Decision Tree)

Read Next.js version from `package.json`:

```
Next.js version?
  |
  +-- 16+ --> Create proxy.ts at project root
  |
  +-- 15   --> Create middleware.ts (cookies() is async - handlers must await)
  |
  +-- 13-14 --> Create middleware.ts (cookies() is sync)
```

**Critical:** File MUST be at project root (or `src/` if using src directory). Never in `app/`.

**Next.js 15+ async note:** All route handlers and middleware accessing cookies must be async and properly await cookie operations. This is a breaking change from Next.js 14.

Middleware/proxy code: See README for `authkitMiddleware()` export pattern.

### Existing Middleware (IMPORTANT)

If `middleware.ts` already exists with custom logic (rate limiting, logging, headers, etc.), use the **`authkit()` composable function** instead of `authkitMiddleware`.

**Pattern for composing with existing middleware:**

```typescript
import { NextRequest, NextResponse } from 'next/server';
import { authkit, handleAuthkitHeaders } from '@workos-inc/authkit-nextjs';

export default async function middleware(request: NextRequest) {
  // 1. Get auth session and headers from AuthKit
  const { session, headers, authorizationUrl } = await authkit(request);
  const { pathname } = request.nextUrl;

  // 2. === YOUR EXISTING MIDDLEWARE LOGIC ===
  // Rate limiting, logging, custom headers, etc.
  const rateLimitResult = checkRateLimit(request);
  if (!rateLimitResult.allowed) {
    return new NextResponse('Too Many Requests', { status: 429 });
  }

  // 3. Protect routes - redirect to auth if needed
  if (pathname.startsWith('/dashboard') && !session.user && authorizationUrl) {
    return handleAuthkitHeaders(request, headers, { redirect: authorizationUrl });
  }

  // 4. Continue with AuthKit headers properly handled
  return handleAuthkitHeaders(request, headers);
}
```

**Key functions:**

- `authkit(request)` - Returns `{ session, headers, authorizationUrl }` for composition
- `handleAuthkitHeaders(request, headers, options?)` - Ensures AuthKit headers pass through correctly
- For rewrites, use `partitionAuthkitHeaders()` and `applyResponseHeaders()` (see README)

**Critical:** Always return via `handleAuthkitHeaders()` to ensure `withAuth()` works in pages.

## Step 5: Create Callback Route

Parse `NEXT_PUBLIC_WORKOS_REDIRECT_URI` to determine route path:

```
URI path          --> Route location
/auth/callback    --> app/auth/callback/route.ts
/callback         --> app/callback/route.ts
```

Use `handleAuth()` from SDK. Do not write custom OAuth logic.

**CRITICAL for Next.js 15+:** The route handler MUST be async and properly await handleAuth():

```typescript
// CORRECT - Next.js 15+ requires async route handlers
export const GET = handleAuth();

// If handleAuth returns a function, ensure it's awaited in request context
```

Check README for exact usage. If build fails with "cookies outside request scope", the handler is likely missing async/await.

## Step 6: Provider Setup (REQUIRED)

**CRITICAL:** You MUST wrap the app in `AuthKitProvider` in `app/layout.tsx`.

This is required for:

- Client-side auth state via `useAuth()` hook
- Consistent auth UX across client/server boundaries
- Proper migration from Auth0 (which uses client-side auth)

```tsx
// app/layout.tsx
import { AuthKitProvider } from '@workos-inc/authkit-nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthKitProvider>{children}</AuthKitProvider>
      </body>
    </html>
  );
}
```

Check README for exact import path - it may be a subpath export like `@workos-inc/authkit-nextjs/components`.

**Do NOT skip this step** even if using server-side auth patterns elsewhere.

## Step 7: UI Integration

Add auth UI to `app/page.tsx` using SDK functions. See README for `getUser`, `getSignInUrl`, `signOut` usage.

## Verification Checklist (ALL MUST PASS)

Run these commands to confirm integration. **Do not mark complete until all pass:**

```bash
# 1. Check middleware/proxy exists (one should match)
ls proxy.ts middleware.ts src/proxy.ts src/middleware.ts 2>/dev/null

# 2. CRITICAL: Check AuthKitProvider is in layout (REQUIRED)
grep "AuthKitProvider" app/layout.tsx || echo "FAIL: AuthKitProvider missing from layout"

# 3. Check callback route exists
find app -name "route.ts" -path "*/callback/*"

# 4. Build succeeds
npm run build
```

**If check #2 fails:** Go back to Step 6 and add AuthKitProvider. This is not optional.

## Error Recovery

### "cookies was called outside a request scope" (Next.js 15+)

**Most common cause:** Route handler not properly async or missing await.

Fix for callback route:

1. Check that `handleAuth()` is exported directly: `export const GET = handleAuth();`
2. If using custom wrapper, ensure it's `async` and awaits any cookie operations
3. Verify authkit-nextjs SDK version supports Next.js 15+ (check README for compatibility)
4. **Never** call `cookies()` at module level - only inside request handlers

This error causes OAuth codes to expire ("invalid_grant"), so fix the handler first.

### "middleware.ts not found"

- Check: File at project root or `src/`, not inside `app/`
- Check: Filename matches Next.js version (proxy.ts for 16+, middleware.ts for 13-15)

### "Cannot use getUser in client component"

- Check: Component has no `'use client'` directive, or
- Check: Move auth logic to server component/API route

### "Module not found" for SDK import

- Check: SDK installed before writing imports
- Check: SDK package directory exists in node_modules

### "withAuth route not covered by middleware"

- Check: Middleware/proxy file exists at correct location
- Check: Matcher config includes the route path

### Build fails after AuthKitProvider

- Check: README for correct import path (may be subpath export)
- Check: No client/server boundary violations

### NEXT*PUBLIC* prefix issues

- Client components need `NEXT_PUBLIC_*` prefix
- Server components use plain env var names
