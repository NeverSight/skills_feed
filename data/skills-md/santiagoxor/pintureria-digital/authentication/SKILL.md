---
name: authentication
description: Specialized skill for working with NextAuth.js authentication including session management, JWT tokens, role-based access control, and protected routes. Use when implementing authentication features, securing routes, managing user sessions, or debugging auth issues.
---

# Authentication

## Quick Start

When working with authentication:

1. Use `auth()` from `@/lib/auth` to get current session
2. Verify roles before admin operations
3. Use middleware for route protection
4. Never store tokens in localStorage (use httpOnly cookies)
5. Validate JWT tokens in API routes

## Key Files

- `auth.ts` - NextAuth.js configuration
- `src/lib/auth/` - Auth utilities
- `middleware.ts` - Route protection
- `src/app/api/auth/` - Auth API routes

## Common Patterns

### Get Current Session

```typescript
import { auth } from '@/lib/auth';

export async function GET(request: NextRequest) {
  const session = await auth();
  
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  return NextResponse.json({ user: session.user });
}
```

### Check Admin Role

```typescript
const session = await auth();

if (session?.user?.role !== 'admin') {
  return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
}
```

### Protected API Route

```typescript
import { auth } from '@/lib/auth';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  // 1. Check authentication
  const session = await auth();
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  
  // 2. Check authorization (if needed)
  if (session.user.role !== 'admin') {
    return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
  }
  
  // 3. Process request
  const body = await request.json();
  // ... business logic
}
```

### Middleware Protection

```typescript
// middleware.ts
import { auth } from '@/lib/auth';
import { NextResponse } from 'next/server';

export async function middleware(request: NextRequest) {
  const session = await auth();
  
  // Protect admin routes
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!session || session.user.role !== 'admin') {
      return NextResponse.redirect(new URL('/login', request.url));
    }
  }
  
  return NextResponse.next();
}
```

### Sign In/Out

```typescript
import { signIn, signOut } from '@/lib/auth';

// Sign in
await signIn('google', {
  callbackUrl: '/dashboard',
});

// Sign out
await signOut({
  callbackUrl: '/',
});
```

## User Roles

- `admin` - Full access
- `customer` - Regular user
- `moderator` - Limited admin access

## Session Structure

```typescript
interface Session {
  user: {
    id: string;
    email: string;
    name?: string;
    role: 'admin' | 'customer' | 'moderator';
    image?: string;
  };
  expires: string;
}
```
