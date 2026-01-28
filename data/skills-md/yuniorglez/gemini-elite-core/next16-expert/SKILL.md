---
name: next16-expert
id: next16-expert
version: 1.2.0
description: "Senior specialist in Next.js 16.1.1, React 19.2, and Gemini Elite Standards. Focus on Proxy & Cache paradigm and PPR."
---

# ⚡ Skill: next16-expert

## Description
Senior specialist in the Next.js 16.1.1 and React 19.2 ecosystem. This skill focuses on the high-performance **Proxy & Cache** paradigm, **Partial Pre-rendering (PPR)**, and the mandatory transition from `middleware.ts` to `proxy.ts`. It provides production-ready patterns for modern full-stack development.

## Table of Contents
1. [Quick Start](#quick-start)
2. [The Proxy Revolution (`proxy.ts`)](#the-proxy-revolution-proxyts)
3. [Unified Caching (`use cache`)](#unified-caching-use-cache)
4. [React 19.2 Patterns](#react-192-patterns)
5. [Data Fetching & Mutations](#data-fetching--mutations)
6. [Component Design & Single Responsibility](#component-design--single-responsibility)
7. [The 'Do Not' List (Anti-Patterns)](#the-do-not-list-anti-patterns)
8. [Advanced References](#advanced-references)

---

## Quick Start

Initialize an Elite-grade project:

```bash
npx create-next-app@latest my-elite-app \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*"
```

**Elite Configuration (`next.config.ts`):**
```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  experimental: {
    ppr: true, // Enable Partial Pre-rendering
    dynamicIO: true, // New IO optimization for Next.js 16
    reactCompiler: true, // Stable React Compiler support
  },
  logging: {
    fetches: {
      fullUrl: true,
    },
  },
};

export default nextConfig;
```

---

## The Proxy Revolution (`proxy.ts`)

In Next.js 16, **`middleware.ts` is legacy**. All global network logic must reside in `proxy.ts`. This stabilizes the runtime and provides a clean gate for all requests.

**Standard Elite Proxy (`src/app/proxy.ts`):**
```typescript
import { nextProxy } from 'next/server';

export default nextProxy(async (request) => {
  const url = request.nextUrl;

  // Global Routing Logic
  if (url.pathname.startsWith('/api/v1')) {
    // Standardize API versioning at the proxy level
  }

  // Security Headers & Request Decoration
  request.headers.set('X-Elite-Engine', '16.1.1');
  
  const response = await fetch(request);

  // Performance Monitoring
  response.headers.set('Server-Timing', 'elite;dur=20');

  return response;
});
```
*For deep-dives into A/B testing and advanced security, see [proxy-deep-dive.md](./references/proxy-deep-dive.md).*

---

## Unified Caching (`use cache`)

Next.js 16 introduces the `use cache` directive, replacing the complexity of `revalidatePath` with explicit, function-level caching.

**Cached Data Service (`src/services/data.ts`):**
```typescript
import { cacheLife, cacheTag } from 'next/cache';

export async function getGlobalMetrics() {
  'use cache';
  cacheLife(60); // Cache for 60 seconds
  cacheTag('metrics');

  const data = await fetch('https://api.internal/metrics').then(r => r.json());
  return data;
}
```

**Invalidation Patterns:**
- `revalidateTag('metrics')`: Immediate purge.
- `updateTag('metrics')`: **Recommended**. Marks as stale and revalidates in background (SWR).

*For complex caching strategies, see [unified-caching.md](./references/unified-caching.md).*

---

## React 19.2 Patterns

Leverage the stability of React 19.2 within Next.js 16 to eliminate boilerplate.

### 1. `useActionState` for Forms
Eliminate manual loading and error states in Client Components.

```tsx
'use client';
import { useActionState } from 'react';
import { signUpAction } from '@/actions/auth';

export function SignUpForm() {
  const [state, action, isPending] = useActionState(signUpAction, null);

  return (
    <form action={action}>
      <input name="email" type="email" required />
      {state?.errors?.email && <p className="text-red-500">{state.errors.email}</p>}
      
      <button disabled={isPending}>
        {isPending ? 'Processing...' : 'Sign Up'}
      </button>
    </form>
  );
}
```

### 2. The `<Activity />` Component
Use for pre-rendering background tabs or hidden UI without performance cost.

```tsx
import { Activity } from 'react';

export function TabSystem({ activeTab }) {
  return (
    <>
      <Activity mode={activeTab === 'home' ? 'visible' : 'hidden'}>
        <HomeTab />
      </Activity>
      <Activity mode={activeTab === 'settings' ? 'visible' : 'hidden'}>
        <SettingsTab />
      </Activity>
    </>
  );
}
```

---

## Data Fetching & Mutations

### Server-First Approach (RSC)
80% of your data should be fetched in Server Components.

```tsx
// app/dashboard/page.tsx
import { getGlobalMetrics } from '@/services/data';

export default async function Page() {
  const metrics = await getGlobalMetrics(); // Direct, cached call

  return (
    <div>
      <h1>Dashboard</h1>
      <pre>{JSON.stringify(metrics, null, 2)}</pre>
    </div>
  );
}
```

### Server Actions (Mutations)
Mandatory for all POST/PATCH/DELETE operations.

```typescript
// actions/auth.ts
'use server';
import { updateTag } from 'next/cache';

export async function signUpAction(prevState: any, formData: FormData) {
  const email = formData.get('email');
  
  try {
    await db.user.create({ data: { email } });
    updateTag('users'); // Background revalidation
    return { success: true };
  } catch (e) {
    return { errors: { email: 'Invalid email' } };
  }
}
```

---

## Component Design & Single Responsibility

- **300-Line Rule**: Keep component files under 300 lines. If a component exceeds this, extract sub-components or move logic to `hooks/` or `services/`.
- **Hydration Guard**: Always protect components that depend on browser-only state.

```tsx
'use client';
import { useState, useEffect } from 'react';

export function SafeClientComponent({ children }) {
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);

  if (!mounted) return <div className="animate-pulse" />; // Placeholder
  return <>{children}</>;
}
```

---

## The 'Do Not' List (Anti-Patterns)

- **DO NOT use `middleware.ts`**: Use `proxy.ts`. `middleware.ts` is considered legacy and less performant in Next.js 16.
- **DO NOT use `revalidatePath` for simple UI updates**: Use `updateTag` within Server Actions for a better UX (Stale-While-Revalidate).
- **DO NOT access cookies in RSC without Suspense**: Accessing `cookies()` or `headers()` makes a route dynamic. Wrap the dependent component in `<Suspense>` to keep the rest of the page static (PPR).
- **DO NOT use Barrel Files (`index.ts`) for components**: This kills tree-shaking and bloats the bundle. Import directly from the component file.
- **DO NOT hardcode API URLs**: Use environment variables and the `proxy.ts` layer to manage environments.

---

## Advanced References

- [Proxy Deep Dive](./references/proxy-deep-dive.md) — Advanced routing and security.
- [Unified Caching](./references/unified-caching.md) — Master the `use cache` directive.
- [React Expert](../react-expert/SKILL.md) — For deep performance optimizations.
- [Supabase Expert](../supabase-expert/SKILL.md) — For backend and auth integration.

---
*Optimized for Next.js 16.1.1 and React 19.2. Updated: January 22, 2026 - 14:36*
