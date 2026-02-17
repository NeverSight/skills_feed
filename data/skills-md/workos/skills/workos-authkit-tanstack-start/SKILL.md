---
name: workos-authkit-tanstack-start
description: Integrate WorkOS AuthKit with TanStack Start applications. Full-stack TypeScript with server functions. Use when project uses TanStack Start, @tanstack/start, or vinxi.
---

# WorkOS AuthKit for TanStack Start

## Decision Tree

```
1. Fetch README (BLOCKING)
   ├── Extract package name from install command
   └── README is source of truth for ALL code patterns

2. Detect directory structure
   ├── src/ (TanStack Start v1.132+, default)
   └── app/ (legacy vinxi-based projects)

3. Follow README install/setup exactly
   └── Do not invent commands or patterns
```

## Fetch SDK Documentation (BLOCKING)

**STOP - Do not proceed until complete.**

WebFetch: `https://github.com/workos/authkit-tanstack-start/blob/main/README.md`

From README, extract:

1. Package name: `@workos/authkit-tanstack-react-start`
2. Use that exact name for all imports

**README overrides this skill if conflict.**

## Pre-Flight Checklist

- [ ] README fetched and package name extracted
- [ ] `@tanstack/start` or `@tanstack/react-start` in package.json
- [ ] Identify directory structure: `src/` (modern) or `app/` (legacy)
- [ ] Environment variables set (see below)

## Directory Structure Detection

**Modern TanStack Start (v1.132+)** uses `src/`:

```
src/
├── start.ts              # Middleware config (CRITICAL)
├── router.tsx            # Router setup
├── routes/
│   ├── __root.tsx        # Root layout
│   ├── api.auth.callback.tsx  # OAuth callback (flat route)
│   └── ...
```

**Legacy (vinxi-based)** uses `app/`:

```
app/
├── start.ts or router.tsx
├── routes/
│   └── api/auth/callback.tsx  # OAuth callback (nested route)
```

**Detection:**

```bash
ls src/routes 2>/dev/null && echo "Modern (src/)" || echo "Legacy (app/)"
```

## Environment Variables

| Variable                 | Format       | Required |
| ------------------------ | ------------ | -------- |
| `WORKOS_API_KEY`         | `sk_...`     | Yes      |
| `WORKOS_CLIENT_ID`       | `client_...` | Yes      |
| `WORKOS_REDIRECT_URI`    | Full URL     | Yes      |
| `WORKOS_COOKIE_PASSWORD` | 32+ chars    | Yes      |

Generate password if missing: `openssl rand -base64 32`

Default redirect URI: `http://localhost:3000/api/auth/callback`

## Middleware Configuration (CRITICAL)

**authkitMiddleware MUST be configured or auth will fail silently.**

Create or update `src/start.ts` (or `app/start.ts` for legacy):

```typescript
import { authkitMiddleware } from '@workos/authkit-tanstack-react-start';

export default {
  requestMiddleware: [authkitMiddleware()],
};
```

Alternative pattern with createStart:

```typescript
import { createStart } from '@tanstack/react-start';
import { authkitMiddleware } from '@workos/authkit-tanstack-react-start';

export default createStart({
  requestMiddleware: [authkitMiddleware()],
});
```

### Verification Checklist

- [ ] `authkitMiddleware` imported from `@workos/authkit-tanstack-react-start`
- [ ] Middleware in `requestMiddleware` array
- [ ] File exports the config (default export or named `startInstance`)

Verify: `grep -r "authkitMiddleware" src/ app/ 2>/dev/null`

## Callback Route (CRITICAL)

Path must match `WORKOS_REDIRECT_URI`. For `/api/auth/callback`:

**Modern (flat routes):** `src/routes/api.auth.callback.tsx`
**Legacy (nested routes):** `app/routes/api/auth/callback.tsx`

```typescript
import { createFileRoute } from '@tanstack/react-router';
import { handleCallbackRoute } from '@workos/authkit-tanstack-react-start';

export const Route = createFileRoute('/api/auth/callback')({
  server: {
    handlers: {
      GET: handleCallbackRoute(),
    },
  },
});
```

**Key points:**

- Use `handleCallbackRoute()` - do not write custom OAuth logic
- Route path string must match the URI path exactly
- This is a server-only route (no component needed)

## Protected Routes

Use `getAuth()` in route loaders to check authentication:

```typescript
import { createFileRoute, redirect } from '@tanstack/react-router';
import { getAuth, getSignInUrl } from '@workos/authkit-tanstack-react-start';

export const Route = createFileRoute('/dashboard')({
  loader: async () => {
    const { user } = await getAuth();
    if (!user) {
      const signInUrl = await getSignInUrl();
      throw redirect({ href: signInUrl });
    }
    return { user };
  },
  component: Dashboard,
});
```

## Sign Out Route

```typescript
import { createFileRoute, redirect } from '@tanstack/react-router';
import { signOut } from '@workos/authkit-tanstack-react-start';

export const Route = createFileRoute('/signout')({
  loader: async () => {
    await signOut();
    throw redirect({ href: '/' });
  },
});
```

## Client-Side Hooks (Optional)

Only needed if you want reactive auth state in components.

**1. Add AuthKitProvider to root:**

```typescript
// src/routes/__root.tsx
import { AuthKitProvider } from '@workos/authkit-tanstack-react-start/client';

function RootComponent() {
  return (
    <AuthKitProvider>
      <Outlet />
    </AuthKitProvider>
  );
}
```

**2. Use hooks in components:**

```typescript
import { useAuth } from '@workos/authkit-tanstack-react-start/client';

function Profile() {
  const { user, isLoading } = useAuth();
  // ...
}
```

**Note:** Server-side `getAuth()` is preferred for most use cases.

## Error Recovery

### "AuthKit middleware is not configured"

**Cause:** `authkitMiddleware()` not in start.ts
**Fix:** Create/update `src/start.ts` with middleware config
**Verify:** `grep -r "authkitMiddleware" src/`

### "Module not found" for SDK

**Cause:** Wrong package name or not installed
**Fix:** `pnpm add @workos/authkit-tanstack-react-start`
**Verify:** `ls node_modules/@workos/authkit-tanstack-react-start`

### Callback 404

**Cause:** Route file path doesn't match WORKOS_REDIRECT_URI
**Fix:**

- URI `/api/auth/callback` → file `src/routes/api.auth.callback.tsx` (flat) or `app/routes/api/auth/callback.tsx` (nested)
- Route path string in `createFileRoute()` must match exactly

### getAuth returns undefined user

**Cause:** Middleware not configured or not running
**Fix:** Ensure `authkitMiddleware()` is in start.ts requestMiddleware array

### "Cookie password too short"

**Cause:** WORKOS_COOKIE_PASSWORD < 32 chars
**Fix:** `openssl rand -base64 32`, update .env

### Build fails with route type errors

**Cause:** Route tree not regenerated after adding routes
**Fix:** `pnpm dev` to regenerate `routeTree.gen.ts`

## SDK Exports Reference

**Server (main export):**

- `authkitMiddleware()` - Request middleware
- `handleCallbackRoute()` - OAuth callback handler
- `getAuth()` - Get current session
- `signOut()` - Sign out user
- `getSignInUrl()` / `getSignUpUrl()` - Auth URLs
- `switchToOrganization()` - Change org context

**Client (`/client` subpath):**

- `AuthKitProvider` - Context provider
- `useAuth()` - Auth state hook
- `useAccessToken()` - Token management
