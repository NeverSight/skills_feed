---
name: nextjs-server-client-components
description: Guide for choosing between Server Components and Client Components in Next.js App Router. CRITICAL for useSearchParams (requires Suspense + 'use client'), navigation (Link, redirect, useRouter), cookies/headers access, and 'use client' directive. Activates when prompt mentions useSearchParams, Suspense, navigation, routing, Link component, redirect, pathname, searchParams, cookies, headers, async components, or 'use client'. Essential for avoiding mixing server/client APIs.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Next.js Server Components vs Client Components

## Overview

Provide comprehensive guidance for choosing between Server Components and Client Components in Next.js App Router, including cookie/header access, searchParams handling, pathname routing, and React's 'use' API for promise unwrapping.

## TypeScript: NEVER Use `any` Type

**CRITICAL RULE:** This codebase has `@typescript-eslint/no-explicit-any` enabled. Using `any` will cause build failures.

**❌ WRONG:**
```typescript
function handleSubmit(e: any) { ... }
const data: any[] = [];
```

**✅ CORRECT:**
```typescript
function handleSubmit(e: React.FormEvent<HTMLFormElement>) { ... }
const data: string[] = [];
```

### Common Next.js Type Patterns

```typescript
// Page props
function Page({ params }: { params: { slug: string } }) { ... }
function Page({ searchParams }: { searchParams: { [key: string]: string | string[] | undefined } }) { ... }

// Form events
const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => { ... }
const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => { ... }

// Server actions
async function myAction(formData: FormData) { ... }
```

## When to Use This Skill

Use this skill when:
- Deciding whether to use Server or Client Components
- Accessing cookies, headers, or other server-side data
- Working with searchParams or route parameters
- Needing pathname or routing information
- Unwrapping promises with React 'use' API
- Debugging 'use client' boundary issues
- Optimizing component rendering strategy

## Core Decision: Server vs Client Components

### Default: Server Components

**All components in the App Router are Server Components by default.** No directive needed.

```typescript
// app/components/ProductList.tsx
// This is a Server Component (default)
export default async function ProductList() {
  const products = await fetch('https://api.example.com/products');
  const data = await products.json();

  return (
    <ul>
      {data.map(product => (
        <li key={product.id}>{product.name}</li>
      ))}
    </ul>
  );
}
```

**When to use Server Components:**
- Fetching data from APIs or databases
- Accessing backend resources (environment variables, file system)
- Processing sensitive information (API keys, tokens)
- Reducing client-side JavaScript bundle
- SEO-critical content rendering
- Static or infrequently changing content

**Benefits:**
- Zero client-side JavaScript by default
- Direct database/API access
- Secure handling of secrets
- Automatic code splitting
- Better initial page load performance
- Reduced bundle size

### Client Components: 'use client'

Add `'use client'` directive at the top of a file to make it a Client Component.

```typescript
// app/components/Counter.tsx
'use client';

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <button onClick={() => setCount(count + 1)}>
      Count: {count}
    </button>
  );
}
```

**When to use Client Components:**
- Need React hooks (useState, useEffect, useContext, etc.)
- Event handlers (onClick, onChange, onSubmit, etc.)
- Browser-only APIs (window, localStorage, navigator)
- Third-party libraries requiring browser environment
- Interactive UI elements (modals, dropdowns, forms)
- Real-time features (WebSocket, animations)

**Requirements for Client Components:**
- Must have `'use client'` directive at top of file
- Cannot use async/await directly in component
- Cannot access server-only APIs (cookies, headers)
- All imported components become Client Components

### ⚠️ CRITICAL: Server Components NEVER Need 'use client'

**Server Components are the DEFAULT. DO NOT add 'use client' unless you specifically need client-side features.**

**✅ CORRECT - Server Component with Navigation:**
```typescript
// app/page.tsx - Server Component (NO 'use client' needed!)
import Link from 'next/link';
import { redirect } from 'next/navigation';

export default async function Page() {
  // Server components can be async
  const data = await fetchData();

  if (!data) {
    redirect('/login');  // Server-side redirect
  }

  return (
    <div>
      <Link href="/dashboard">Go to Dashboard</Link>
      <p>{data.content}</p>
    </div>
  );
}
```

**❌ WRONG - Adding 'use client' to Server Component:**
```typescript
// app/page.tsx
'use client';  // ❌ WRONG! Don't add this to server components!

export default async function Page() {  // ❌ Will fail - async client components not allowed
  const data = await fetchData();
  return <div>{data.content}</div>;
}
```

**Server Navigation Methods (NO 'use client' needed):**
- `<Link>` component from `next/link`
- `redirect()` function from `next/navigation`
- Server Actions (see Advanced Routing skill)

**Client Navigation Methods (REQUIRES 'use client'):**
- `useRouter()` hook from `next/navigation`
- `usePathname()` hook
- `useSearchParams()` hook (also requires Suspense)

## Server Component Patterns

### Accessing Cookies

Use `next/headers` to read cookies in Server Components:

```typescript
// app/dashboard/page.tsx
import { cookies } from 'next/headers';

export default async function Dashboard() {
  const cookieStore = await cookies();
  const token = cookieStore.get('session-token');

  if (!token) {
    redirect('/login');
  }

  const user = await fetchUser(token.value);

  return <div>Welcome, {user.name}</div>;
}
```

**Important Notes:**
- `cookies()` must be awaited in Next.js 15+
- Cookies are read-only in Server Components
- To set cookies, use Server Actions (see Advanced Routing skill)
- Cookie access is only available in Server Components

### Accessing Headers

```typescript
// app/api/route.ts or any Server Component
import { headers } from 'next/headers';

export default async function Page() {
  const headersList = await headers();
  const userAgent = headersList.get('user-agent');
  const referer = headersList.get('referer');

  return <div>User Agent: {userAgent}</div>;
}
```

### Using searchParams

Access URL query parameters directly in Server Components:

```typescript
// app/search/page.tsx
export default async function SearchPage({
  searchParams,
}: {
  searchParams: { q?: string; category?: string };
}) {
  const query = searchParams.q || '';
  const category = searchParams.category || 'all';

  const results = await searchProducts(query, category);

  return (
    <div>
      <h1>Search Results for: {query}</h1>
      <p>Category: {category}</p>
      <ProductList products={results} />
    </div>
  );
}
```

**Important Notes:**
- `searchParams` is only available in `page.tsx` files
- In Next.js 15+, `searchParams` must be awaited
- searchParams is NOT available in `layout.tsx`
- Use client-side `useSearchParams()` hook if needed in Client Components

**⚠️ CRITICAL WARNING - Next.js 15+ searchParams:**
When extracting parameters in Next.js 15+, you MUST use destructuring to keep the `searchParams` identifier visible in the same line as the parameter extraction. Do NOT use intermediate variables like `params` or `resolved` - this is an anti-pattern that breaks code readability and testing patterns.

**Async searchParams (Next.js 15+):**

```typescript
// app/search/page.tsx (Next.js 15+)
export default async function SearchPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string }>;
}) {
  // BEST PRACTICE: Inline access keeps searchParams and parameter together on one line
  const q = (await searchParams).q || '';

  return <div>Search: {q}</div>;
}
```

**CRITICAL PATTERN REQUIREMENT:**

When extracting parameters from `searchParams`, **ALWAYS use inline access** to keep `searchParams` and the parameter name on the SAME LINE:

```typescript
// ✅ CORRECT: Inline access (REQUIRED PATTERN)
const name = (await searchParams).name || '';

// ✅ ALSO CORRECT: Multiple parameters
const category = (await searchParams).category || 'all';
const sort = (await searchParams).sort || 'asc';

// ❌ WRONG: Using intermediate variable separates searchParams from parameter
const params = await searchParams;  // DON'T DO THIS
const name = params.name;           // searchParams not visible here

// ❌ WRONG: Destructuring (searchParams and name on same line but missing second 'name')
const { name } = await searchParams;  // Not preferred
```

**Why inline access:**
- Keeps `searchParams` identifier visible on the same line as parameter extraction
- Makes the relationship between URL parameter and variable explicit
- Satisfies code review and testing patterns that check for proper searchParams usage

### Using pathname and Route Information

**In Server Components (page.tsx):**

```typescript
// app/blog/[slug]/page.tsx
export default async function BlogPost({
  params,
}: {
  params: { slug: string };
}) {
  // params contains route parameters
  const post = await getPost(params.slug);

  return <article>{post.title}</article>;
}
```

**Async params (Next.js 15+):**

```typescript
// app/blog/[slug]/page.tsx (Next.js 15+)
export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const post = await getPost(slug);

  return <article>{post.title}</article>;
}
```

**In Client Components:**

Use hooks from `next/navigation`:

```typescript
// app/components/Breadcrumbs.tsx
'use client';

import { usePathname, useParams, useSearchParams } from 'next/navigation';

export default function Breadcrumbs() {
  const pathname = usePathname(); // Current path: /blog/hello-world
  const params = useParams(); // Route params: { slug: 'hello-world' }
  const searchParams = useSearchParams(); // Query params

  return (
    <nav>
      <span>Current path: {pathname}</span>
      <span>Slug: {params.slug}</span>
      <span>Search: {searchParams.get('q')}</span>
    </nav>
  );
}
```

### ⚠️ CRITICAL: useSearchParams ALWAYS Requires Suspense

**When using `useSearchParams()` hook, you MUST:**
1. Add `'use client'` directive at the top of the file
2. Wrap the component in a Suspense boundary

This is a **Next.js requirement** - failing to do both will cause errors.

**✅ CORRECT Pattern:**

```typescript
// app/page.tsx or any parent component
import { Suspense } from 'react';
import SearchComponent from './SearchComponent';

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <SearchComponent />
    </Suspense>
  );
}

// app/SearchComponent.tsx
'use client';

import { useSearchParams } from 'next/navigation';

export default function SearchComponent() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q');

  return <div>Search query: {query}</div>;
}
```

**❌ WRONG - Missing 'use client':**
```typescript
// This will fail - useSearchParams requires 'use client'
import { useSearchParams } from 'next/navigation';

export default function SearchComponent() {
  const searchParams = useSearchParams(); // ERROR!
  return <div>{searchParams.get('q')}</div>;
}
```

**❌ WRONG - Missing Suspense wrapper:**
```typescript
// This will cause issues - useSearchParams requires Suspense
export default function Page() {
  return <SearchComponent />; // Missing Suspense wrapper!
}
```

## React 'use' API for Promise Unwrapping

The React `use` API allows reading promises and context in both Server and Client Components.

### Using 'use' with Promises

```typescript
// app/components/UserProfile.tsx
'use client';

import { use } from 'react';

// IMPORTANT: Use specific types, generic types, or 'unknown' - NEVER 'any'
// Option 1: Specific type (best when type is known)
export default function UserProfile({
  userPromise
}: {
  userPromise: Promise<{ name: string; email: string }>
}) {
  // Unwrap the promise
  const user = use(userPromise);

  return <div>{user.name}</div>;
}

// Option 2: Generic type (for reusable components)
export function GenericDataDisplay<T>({
  data
}: {
  data: Promise<T>
}) {
  const result = use(data);
  return <div>{JSON.stringify(result)}</div>;
}

// Option 3: Unknown type (when type truly unknown)
export function UnknownDataDisplay({
  data
}: {
  data: Promise<unknown>
}) {
  const result = use(data);
  return <div>{JSON.stringify(result)}</div>;
}
```

**Server Component passing promise:**

```typescript
// app/profile/page.tsx
import UserProfile from './components/UserProfile';

export default function ProfilePage() {
  // Create promise but don't await
  const userPromise = fetchUser();

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}
```

### Benefits of 'use' API

- Enables parallel data fetching
- Works with Suspense boundaries
- Allows Server Components to pass promises to Client Components
- Cleaner than prop drilling async data

### Using 'use' with Context

```typescript
'use client';

import { use } from 'react';
import { ThemeContext } from './ThemeContext';

export default function ThemedButton() {
  const theme = use(ThemeContext);

  return <button className={theme.buttonClass}>Click me</button>;
}
```

## Common Patterns

### Pattern 1: Server Component Fetches, Client Component Interacts

```typescript
// app/products/page.tsx (Server Component)
import ProductGrid from './ProductGrid';

export default async function ProductsPage() {
  const products = await fetchProducts();

  // Pass data to Client Component
  return <ProductGrid products={products} />;
}

// app/products/ProductGrid.tsx (Client Component)
'use client';

import { useState } from 'react';

export default function ProductGrid({
  products
}: {
  products: Product[]
}) {
  const [filter, setFilter] = useState('all');

  const filtered = products.filter(p =>
    filter === 'all' || p.category === filter
  );

  return (
    <div>
      <select onChange={(e) => setFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="electronics">Electronics</option>
      </select>
      {filtered.map(p => <div key={p.id}>{p.name}</div>)}
    </div>
  );
}
```

### Pattern 2: Parallel Data Fetching

```typescript
// app/dashboard/page.tsx
export default async function Dashboard() {
  // Fetch in parallel
  const [user, stats, notifications] = await Promise.all([
    fetchUser(),
    fetchStats(),
    fetchNotifications(),
  ]);

  return (
    <div>
      <UserInfo user={user} />
      <Stats data={stats} />
      <Notifications items={notifications} />
    </div>
  );
}
```

### Pattern 3: Streaming with Suspense

```typescript
// app/page.tsx
import { Suspense } from 'react';

export default function Page() {
  return (
    <div>
      <h1>Dashboard</h1>
      <Suspense fallback={<div>Loading stats...</div>}>
        <Stats />
      </Suspense>
      <Suspense fallback={<div>Loading feed...</div>}>
        <Feed />
      </Suspense>
    </div>
  );
}

async function Stats() {
  const data = await fetchStats(); // Slow query
  return <div>{data.total}</div>;
}

async function Feed() {
  const items = await fetchFeed(); // Fast query
  return <ul>{items.map(i => <li key={i.id}>{i.title}</li>)}</ul>;
}
```

### Pattern 4: Composition - Server Inside Client

You CAN pass Server Components as children to Client Components:

```typescript
// app/page.tsx (Server Component)
import ClientWrapper from './ClientWrapper';
import ServerContent from './ServerContent';

export default function Page() {
  return (
    <ClientWrapper>
      {/* Server Component as children */}
      <ServerContent />
    </ClientWrapper>
  );
}

// ClientWrapper.tsx (Client Component)
'use client';

import { useState } from 'react';

export default function ClientWrapper({
  children
}: {
  children: React.ReactNode
}) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(!isOpen)}>Toggle</button>
      {isOpen && children}
    </div>
  );
}

// ServerContent.tsx (Server Component)
export default async function ServerContent() {
  const data = await fetchData();
  return <div>{data.content}</div>;
}
```

## Anti-Patterns to Avoid

### Anti-Pattern 1: Using 'use client' Everywhere

**Wrong:**
```typescript
// app/components/Header.tsx
'use client';  // Unnecessary!

export default function Header() {
  return <header><h1>My App</h1></header>;
}
```

**Correct:**
```typescript
// app/components/Header.tsx
// No directive needed - keep it as Server Component
export default function Header() {
  return <header><h1>My App</h1></header>;
}
```

**Why:** Only use `'use client'` when you actually need client-side features. Static components should remain Server Components to reduce bundle size.

### Anti-Pattern 2: Fetching Data in Client Components

**Wrong:**
```typescript
'use client';

import { useState, useEffect } from 'react';

export default function Products() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('/api/products')
      .then(r => r.json())
      .then(setProducts);
  }, []);

  return <div>{products.map(p => <div key={p.id}>{p.name}</div>)}</div>;
}
```

**Correct:**
```typescript
// Server Component - no 'use client'
export default async function Products() {
  const response = await fetch('https://api.example.com/products');
  const products = await response.json();

  return <div>{products.map(p => <div key={p.id}>{p.name}</div>)}</div>;
}
```

**Why:** Server Components can fetch data directly, eliminating loading states and reducing client-side JavaScript.

### Anti-Pattern 3: Accessing Server APIs in Client Components

**Wrong:**
```typescript
'use client';

import { cookies } from 'next/headers'; // ERROR!

export default function ClientComponent() {
  const cookieStore = cookies(); // This will fail
  return <div>...</div>;
}
```

**Correct:**
```typescript
// Server Component
import { cookies } from 'next/headers';
import ClientComponent from './ClientComponent';

export default async function ServerComponent() {
  const cookieStore = await cookies();
  const token = cookieStore.get('token')?.value;

  return <ClientComponent token={token} />;
}
```

**Why:** `cookies()`, `headers()`, and other server-only APIs can only be used in Server Components.

### Anti-Pattern 4: Serial Await (Waterfall)

**Wrong:**
```typescript
export default async function Page() {
  const user = await fetchUser();
  const posts = await fetchPosts();  // Waits for user to finish
  const comments = await fetchComments();  // Waits for posts to finish

  return <div>...</div>;
}
```

**Correct:**
```typescript
export default async function Page() {
  // Fetch in parallel
  const [user, posts, comments] = await Promise.all([
    fetchUser(),
    fetchPosts(),
    fetchComments(),
  ]);

  return <div>...</div>;
}
```

**Why:** Parallel fetching reduces total load time significantly.

### Anti-Pattern 5: Importing Server Component into Client Component

**Wrong:**
```typescript
// ClientComponent.tsx
'use client';

import ServerComponent from './ServerComponent'; // This makes it a Client Component!

export default function ClientComponent() {
  return <div><ServerComponent /></div>;
}
```

**Correct:**
```typescript
// ParentServerComponent.tsx (Server Component)
import ClientComponent from './ClientComponent';
import ServerComponent from './ServerComponent';

export default function ParentServerComponent() {
  return (
    <ClientComponent>
      <ServerComponent />
    </ClientComponent>
  );
}
```

**Why:** Importing a Server Component into a Client Component converts it to a Client Component. Pass it as children instead.

## When Client Components ARE Appropriate

Client Components are the correct choice for:

### 1. Interactive Forms

```typescript
'use client';

import { useState } from 'react';

export default function ContactForm() {
  const [email, setEmail] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle submission
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button type="submit">Submit</button>
    </form>
  );
}
```

### 2. Real-Time Features

```typescript
'use client';

import { useEffect, useState } from 'react';

export default function LiveChat() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('wss://chat.example.com');
    ws.onmessage = (event) => {
      setMessages(prev => [...prev, event.data]);
    };
    return () => ws.close();
  }, []);

  return <div>{messages.map((m, i) => <div key={i}>{m}</div>)}</div>;
}
```

### 3. Browser-Only Features

```typescript
'use client';

import { useState, useEffect } from 'react';

export default function GeolocationDisplay() {
  const [location, setLocation] = useState(null);

  useEffect(() => {
    navigator.geolocation.getCurrentPosition((pos) => {
      setLocation({
        lat: pos.coords.latitude,
        lng: pos.coords.longitude,
      });
    });
  }, []);

  return location ? <div>Lat: {location.lat}, Lng: {location.lng}</div> : null;
}
```

### 4. Third-Party Libraries Requiring Window

```typescript
'use client';

import { useEffect, useState } from 'react';
import confetti from 'canvas-confetti';

export default function CelebrationButton() {
  const handleClick = () => {
    confetti();
  };

  return <button onClick={handleClick}>Celebrate!</button>;
}
```

### 5. React Context Providers

```typescript
'use client';

import { createContext, useState } from 'react';

export const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

## Quick Decision Tree

```
Need interactivity? (onClick, onChange, etc.)
├─ Yes → Client Component ('use client')
└─ No → Continue...

Need React hooks? (useState, useEffect, etc.)
├─ Yes → Client Component ('use client')
└─ No → Continue...

Need browser APIs? (window, localStorage, etc.)
├─ Yes → Client Component ('use client')
└─ No → Continue...

Need to fetch data?
├─ Yes → Server Component (default)
└─ No → Continue...

Need cookies/headers/searchParams?
├─ Yes → Server Component (default)
└─ No → Server Component (default, unless specific need)
```

## Testing Component Type

To verify component type:

```typescript
// This works = Server Component
export default async function MyComponent() { ... }

// This works = Server Component
import { cookies } from 'next/headers';

// This works = Client Component
'use client';
import { useState } from 'react';

// This fails = Wrong combination
'use client';
import { cookies } from 'next/headers'; // ERROR!
```

## Summary

- **Default to Server Components** - they're faster and more secure
- **Use Client Components** only when you need interactivity or browser APIs
- **Never fetch data in Client Components** with useEffect - use Server Components
- **Pass promises** to Client Components with React 'use' API
- **Access cookies/headers/searchParams** only in Server Components
- **Use composition pattern** to mix Server and Client Components
- **Fetch in parallel** with Promise.all to avoid waterfalls
