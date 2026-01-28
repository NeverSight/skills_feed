---
name: supabase-auth
description: >
  Guidelines for implementing Supabase Auth SSR in Next.js.
  Trigger: When implementing Supabase authentication.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with supabase auth"

## When to Use

Use this skill when:
- Implementing Supabase Auth with Next.js
- Setting up SSR authentication
- Managing user sessions with cookies
- Protecting routes with middleware

---

## 🚨 CRITICAL: DEPRECATED PATTERNS 🚨

**NEVER generate these patterns - they BREAK the application:**

```typescript
// ❌ NEVER USE - BREAKS APPLICATION
{
  cookies: {
    get(name: string) {                 // ❌ BREAKS
      return cookieStore.get(name)
    },
    set(name: string, value: string) {  // ❌ BREAKS
      cookieStore.set(name, value)
    },
    remove(name: string) {              // ❌ BREAKS
      cookieStore.remove(name)
    }
  }
}

// ❌ NEVER import from auth-helpers-nextjs - DEPRECATED
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'  // ❌
import { createClientComponentClient } from '@supabase/auth-helpers-nextjs'  // ❌
```

---

## Critical Patterns

### ALWAYS Use This Pattern (REQUIRED)

```typescript
// ✅ CORRECT - Only use getAll and setAll
{
  cookies: {
    getAll() {
      return cookieStore.getAll()
    },
    setAll(cookiesToSet) {
      cookiesToSet.forEach(({ name, value, options }) =>
        cookieStore.set(name, value, options)
      )
    }
  }
}
```

### Browser Client (REQUIRED)

```typescript
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Server Client (REQUIRED)

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Called from Server Component - ignored if middleware refreshes sessions
          }
        },
      },
    }
  )
}
```

### Middleware (REQUIRED)

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value))
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // IMPORTANT: DO NOT REMOVE auth.getUser()
  const { data: { user } } = await supabase.auth.getUser()

  if (
    !user &&
    !request.nextUrl.pathname.startsWith('/login') &&
    !request.nextUrl.pathname.startsWith('/auth')
  ) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    return NextResponse.redirect(url)
  }

  // MUST return supabaseResponse as-is to avoid session sync issues
  return supabaseResponse
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

---

## Decision Tree

```
Need browser client?       → Use createBrowserClient from @supabase/ssr
Need server client?        → Use createServerClient with getAll/setAll
Need route protection?     → Use middleware with auth.getUser()
Need OAuth?                → Use signInWithOAuth
Need magic link?           → Use signInWithOtp
```

---

## Code Examples

### Sign Up / Sign In

```typescript
// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'secure-password',
});

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'secure-password',
});

// Sign out
await supabase.auth.signOut();
```

### Session Management

```typescript
// Get current session
const { data: { session } } = await supabase.auth.getSession();

// Listen to auth changes
supabase.auth.onAuthStateChange((event, session) => {
  if (event === 'SIGNED_IN') {
    // Handle sign in
  }
});
```

---

## AI Verification Checklist

Before generating code, VERIFY:
1. ✅ Using ONLY `getAll` and `setAll`?
2. ✅ Importing from `@supabase/ssr`?
3. ❌ Any `get`, `set`, or `remove`? → FIX
4. ❌ Importing from `auth-helpers-nextjs`? → FIX

**Consequences of incorrect implementation:**
- Breaks in production
- Fails to maintain session state
- Causes authentication loops
- Security vulnerabilities
