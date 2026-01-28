---
name: nextjs-server-navigation
description: Guide for implementing navigation in Next.js Server Components using Link component and redirect() function. Covers the difference between server and client navigation methods. Use when adding links, redirects, or navigation logic in server components without converting them to client components unnecessarily.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js: Server Component Navigation Pattern

## ⚠️ CRITICAL RULE

**Server Components use DIFFERENT navigation methods than Client Components!**

When requirements call for server-rendered navigation—for example, linking to other pages, redirecting after a check, or demonstrating routing patterns—prefer `<Link>` and `redirect()` within Server Components. You still avoid `'use client'` unless a client-only API is involved.

## The Pattern

**Scenario:** build a server component that demonstrates proper navigation patterns

**✅ CORRECT Solution:**
```typescript
// app/page.tsx (Server Component - NO 'use client'!)
import Link from 'next/link';

export default async function Page() {
  return (
    <div>
      <h1>Home</h1>
      <Link href="/dashboard">Go to Dashboard</Link>
      <Link href="/profile">View Profile</Link>
    </div>
  );
}
```

**❌ WRONG Solution:**
```typescript
// app/page.tsx
'use client';  // ❌ NO! Server components don't need this for navigation!

import { useRouter } from 'next/navigation';  // ❌ Wrong for server components

export default function Page() {
  const router = useRouter();  // ❌ This is client-side navigation
  // ...
}
```

## Server Navigation Methods

### Method 1: Link Component (Recommended for Links)

```typescript
// app/page.tsx
import Link from 'next/link';

export default async function Page() {
  // Can still fetch data - this is a server component!
  const data = await fetchData();

  return (
    <div>
      <h1>Welcome</h1>

      {/* Simple navigation link */}
      <Link href="/about">About Us</Link>

      {/* Dynamic link */}
      <Link href={`/products/${data.productId}`}>View Product</Link>

      {/* Link with styling */}
      <Link href="/dashboard" className="btn-primary">
        Dashboard
      </Link>
    </div>
  );
}
```

**Key Points:**
- ✅ Works in Server Components (no 'use client' needed)
- ✅ Can be async function
- ✅ Can fetch data
- ✅ No hooks required

### Method 2: redirect() Function (For Conditional Redirects)

```typescript
// app/profile/page.tsx
import { redirect } from 'next/navigation';
import { cookies } from 'next/headers';

export default async function ProfilePage() {
  // Check authentication
  const cookieStore = await cookies();
  const session = cookieStore.get('session');

  // Redirect if not authenticated
  if (!session) {
    redirect('/login');
  }

  // Fetch user data
  const user = await fetchUser(session.value);

  return <div>Welcome, {user.name}!</div>;
}
```

**When to use `redirect()`:**
- Conditional redirects based on server-side data
- Authentication checks
- Permission validation
- Data-based routing

### Method 3: Button with Server Action

```typescript
// app/page.tsx
import { logout } from './actions';

export default async function Page() {
  return (
    <div>
      <h1>Dashboard</h1>

      <form action={logout}>
        <button type="submit">Logout</button>
      </form>
    </div>
  );
}

// app/actions.ts
'use server';

import { redirect } from 'next/navigation';

export async function logout() {
  // Clear session
  await clearSession();

  // Redirect to login page
  redirect('/login');
}
```

## Complete Example: Navigation Patterns

```typescript
// app/page.tsx - Demonstrates multiple navigation patterns

import Link from 'next/link';
import { redirect } from 'next/navigation';
import { headers } from 'next/headers';

export default async function HomePage() {
  // Server-side logic
  const headersList = await headers();
  const userAgent = headersList.get('user-agent');

  // Conditional redirect example
  if (userAgent?.includes('bot')) {
    redirect('/bot-page');
  }

  return (
    <div>
      <h1>Welcome to Our App</h1>

      {/* Navigation Links */}
      <nav>
        <Link href="/about">About</Link>
        <Link href="/products">Products</Link>
        <Link href="/contact">Contact</Link>
      </nav>

      {/* Button-style link */}
      <Link href="/get-started" className="button">
        Get Started
      </Link>

      {/* Dynamic link */}
      <Link href={`/user/${123}`}>View Profile</Link>
    </div>
  );
}
```

## TypeScript: NEVER Use `any` Type

```typescript
// ❌ WRONG
function handleClick(e: any) { ... }

// ✅ CORRECT - Not needed in server components!
// Server components don't have onClick handlers

// For client components with handlers:
'use client';
function handleClick(e: React.MouseEvent<HTMLButtonElement>) { ... }
```

## Server vs Client Navigation Comparison

| Feature | Server Component | Client Component |
|---------|-----------------|------------------|
| `<Link>` | ✅ Yes | ✅ Yes |
| `redirect()` | ✅ Yes | ❌ No |
| `useRouter()` | ❌ No | ✅ Yes |
| `usePathname()` | ❌ No | ✅ Yes |
| async function | ✅ Yes | ❌ No |
| 'use client' | ❌ No | ✅ Yes |

## Common Mistakes to Avoid

### ❌ Mistake 1: Adding 'use client' for Navigation

```typescript
// ❌ WRONG
'use client';  // Don't add this just for navigation!

import Link from 'next/link';

export default function Page() {
  return <Link href="/about">About</Link>;
}
```

```typescript
// ✅ CORRECT
import Link from 'next/link';

// No 'use client' needed!
export default async function Page() {
  return <Link href="/about">About</Link>;
}
```

### ❌ Mistake 2: Using useRouter() in Server Component

```typescript
// ❌ WRONG
import { useRouter } from 'next/navigation';  // This is for CLIENT components!

export default async function Page() {
  const router = useRouter();  // ERROR! Can't use hooks in server components
  // ...
}
```

```typescript
// ✅ CORRECT - Use Link or redirect()
import Link from 'next/link';
import { redirect } from 'next/navigation';

export default async function Page() {
  // Conditional redirect
  const shouldRedirect = await checkSomething();
  if (shouldRedirect) {
    redirect('/other-page');
  }

  // Or navigation links
  return <Link href="/other-page">Go</Link>;
}
```

### ❌ Mistake 3: Making Component Client-Side for Simple Navigation

```typescript
// ❌ WRONG - Loses server component benefits!
'use client';

export default function Page() {
  return (
    <div>
      <Link href="/dashboard">Dashboard</Link>
    </div>
  );
}
```

```typescript
// ✅ CORRECT - Keep it as a server component!
export default async function Page() {
  // Can now fetch data server-side
  const data = await fetchData();

  return (
    <div>
      <Link href="/dashboard">Dashboard</Link>
      <p>{data.message}</p>
    </div>
  );
}
```

## Advanced Patterns

### Programmatic Navigation in Server Actions

```typescript
// app/page.tsx
import { createPost } from './actions';

export default async function Page() {
  return (
    <form action={createPost}>
      <input name="title" required />
      <button type="submit">Create Post</button>
    </form>
  );
}

// app/actions.ts
'use server';

import { redirect } from 'next/navigation';

export async function createPost(formData: FormData) {
  const title = formData.get('title') as string;

  // Save to database
  const post = await db.posts.create({ title });

  // Redirect to the new post
  redirect(`/posts/${post.id}`);
}
```

### Multiple Links in Server Component

```typescript
// app/page.tsx
import Link from 'next/link';

export default async function NavigationPage() {
  const pages = await fetchPages();

  return (
    <nav>
      <h2>Site Navigation</h2>
      <ul>
        {pages.map((page) => (
          <li key={page.id}>
            <Link href={`/pages/${page.slug}`}>
              {page.title}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
```

## Quick Decision Tree

```
Need navigation in a component?
│
├─ Is it a Server Component (no 'use client')?
│  ├─ Static link → Use <Link>
│  ├─ Conditional redirect → Use redirect()
│  └─ Form submission → Server Action with redirect()
│
└─ Is it a Client Component ('use client')?
   ├─ Link → Use <Link> (works in both!)
   └─ Programmatic → Use useRouter()
```

## When to Use Client-Side Navigation Instead

Use Client Components (`'use client'` + `useRouter()`) ONLY when you need:
- Programmatic navigation based on client state
- Navigation after client-side animations
- Browser-only APIs (window, localStorage)
- React hooks (useState, useEffect)

**For everything else, use Server Component navigation!**

## Quick Checklist

When you see "demonstrates navigation patterns":

- [ ] Create a server component (no 'use client')
- [ ] Import `Link` from 'next/link'
- [ ] Add `<Link>` components with href prop
- [ ] Keep component as `async` if fetching data
- [ ] Do NOT import useRouter from next/navigation
- [ ] Do NOT add 'use client' directive
- [ ] Use proper TypeScript types (no `any`)

## Summary

**Server Component Navigation:**
- ✅ Use `<Link>` for navigation links
- ✅ Use `redirect()` for conditional redirects
- ✅ Keep component async if needed
- ✅ No 'use client' required
- ✅ No hooks needed

**This pattern is simpler and more performant than client-side navigation for static links!**
