---
name: clerk-validator
description: Validate Clerk authentication configuration and detect deprecated patterns. Ensures proper proxy.ts usage (Next.js 16), ClerkProvider setup, and modern auth patterns. Use before any Clerk work or when auditing existing auth implementations.
version: 1.0.0
tags:
  - clerk
  - authentication
  - validation
  - nextjs
  - nestjs
---

# Clerk Validator

Validates Clerk authentication configuration and prevents deprecated patterns. AI assistants often generate old Clerk patterns - this skill enforces modern Clerk with Next.js 16.

## When This Activates

- Setting up Clerk authentication
- Before any auth implementation work
- Auditing existing Clerk configuration
- After AI generates Clerk code
- CI/CD pipeline validation

## Quick Start

```bash
python3 ~/.claude/skills/clerk-validator/scripts/validate.py --root .
python3 ~/.claude/skills/clerk-validator/scripts/validate.py --root . --strict
```

## What Gets Checked

### 1. Package Version

```json
// GOOD: Latest Clerk
"@clerk/nextjs": "^6.0.0"

// BAD: Old version
"@clerk/nextjs": "^4.0.0"
```

### 2. Proxy vs Middleware (Next.js 16)

**GOOD - Next.js 16:**

```typescript
// proxy.ts
import { clerkMiddleware } from "@clerk/nextjs/server";
export default clerkMiddleware();
```

**BAD - Deprecated:**

```typescript
// middleware.ts (deprecated in Next.js 16)
import { authMiddleware } from "@clerk/nextjs";  // DEPRECATED
export default authMiddleware();
```

### 3. ClerkProvider Setup

**GOOD:**

```typescript
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";

export default function RootLayout({ children }) {
  return (
    <ClerkProvider>
      <html>
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

**BAD - Missing or wrong location:**

```typescript
// Don't put in _app.tsx (Pages Router deprecated)
// Don't forget to wrap the entire app
```

### 4. Auth Import Patterns

**GOOD - Server-side:**

```typescript
import { auth } from "@clerk/nextjs/server";

export default async function Page() {
  const { userId } = await auth();
  // ...
}
```

**BAD - Old patterns:**

```typescript
// Don't use
import { getAuth } from "@clerk/nextjs/server";  // OLD
import { currentUser } from "@clerk/nextjs";     // Check version
```

### 5. Environment Variables

**Required:**

```env
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
```

**Optional but recommended:**

```env
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/onboarding
```

## Deprecated Patterns

| Deprecated | Replacement |
|------------|-------------|
| `authMiddleware()` | `clerkMiddleware()` |
| `middleware.ts` | `proxy.ts` (Next.js 16) |
| `getAuth()` | `auth()` |
| `@clerk/nextjs` < v5 | `@clerk/nextjs@latest` |
| `_app.tsx` provider | `app/layout.tsx` provider |
| `withClerkMiddleware` | `clerkMiddleware()` |

## Validation Output

```
=== Clerk Validation Report ===

Package Version: @clerk/nextjs@6.0.0 ✓

Configuration:
  ✓ ClerkProvider in app/layout.tsx
  ✓ proxy.ts with clerkMiddleware
  ✗ Found middleware.ts - should use proxy.ts for Next.js 16
  ✓ Environment variables configured

Auth Patterns:
  ✓ Using auth() from @clerk/nextjs/server
  ✗ Found deprecated authMiddleware() in 1 file

Summary: 2 issues found
```

## Modern Clerk Patterns

### Protected Routes (Server Component)

```typescript
// app/dashboard/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  return <Dashboard />;
}
```

### Protected Routes (Client Component)

```typescript
"use client";
import { useAuth } from "@clerk/nextjs";

export default function ProtectedComponent() {
  const { isLoaded, userId } = useAuth();

  if (!isLoaded) return <Loading />;
  if (!userId) return <Redirect to="/sign-in" />;

  return <Content />;
}
```

### API Routes

```typescript
// app/api/protected/route.ts
import { auth } from "@clerk/nextjs/server";
import { NextResponse } from "next/server";

export async function GET() {
  const { userId } = await auth();

  if (!userId) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  return NextResponse.json({ userId });
}
```

### NestJS Guard

```typescript
// auth/clerk.guard.ts
import { Injectable, CanActivate, ExecutionContext } from "@nestjs/common";
import { clerkClient } from "@clerk/clerk-sdk-node";

@Injectable()
export class ClerkGuard implements CanActivate {
  async canActivate(context: ExecutionContext): Promise<boolean> {
    const request = context.switchToHttp().getRequest();
    const token = this.extractToken(request);

    if (!token) return false;

    try {
      const { userId } = await clerkClient.verifyToken(token);
      request.userId = userId;
      return true;
    } catch {
      return false;
    }
  }

  private extractToken(request: any): string | null {
    const auth = request.headers.authorization;
    if (!auth?.startsWith("Bearer ")) return null;
    return auth.slice(7);
  }
}
```

## Webhook Configuration

```typescript
// app/api/webhooks/clerk/route.ts
import { Webhook } from "svix";
import { headers } from "next/headers";
import { WebhookEvent } from "@clerk/nextjs/server";

export async function POST(req: Request) {
  const WEBHOOK_SECRET = process.env.CLERK_WEBHOOK_SECRET;
  if (!WEBHOOK_SECRET) throw new Error("Missing CLERK_WEBHOOK_SECRET");

  const headerPayload = headers();
  const svix_id = headerPayload.get("svix-id");
  const svix_timestamp = headerPayload.get("svix-timestamp");
  const svix_signature = headerPayload.get("svix-signature");

  const body = await req.text();
  const wh = new Webhook(WEBHOOK_SECRET);
  const evt = wh.verify(body, {
    "svix-id": svix_id!,
    "svix-timestamp": svix_timestamp!,
    "svix-signature": svix_signature!,
  }) as WebhookEvent;

  // Handle event
  switch (evt.type) {
    case "user.created":
      // Sync to database
      break;
  }

  return new Response("OK", { status: 200 });
}
```

## CI/CD Integration

```yaml
# .github/workflows/validate.yml
- name: Validate Clerk Config
  run: |
    python3 ~/.claude/skills/clerk-validator/scripts/validate.py \
      --root . \
      --strict \
      --ci
```

## Integration

- `nextjs-validator` - Validates Next.js 16 (proxy.ts)
- `biome-validator` - Validates linting config
- `git-safety` - Ensures no secrets committed

---
