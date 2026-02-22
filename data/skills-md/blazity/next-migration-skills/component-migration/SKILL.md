---
name: component-migration
description: >
  Use when adding 'use client' directives, splitting mixed components into
  server + client parts, or fixing RSC boundary errors like "useState only
  works in a Client Component." Also for migrating interactive UI (forms,
  modals, event handlers) to App Router.
---

# Component Migration

Migrate components for RSC (React Server Component) compatibility. Determine which components need `'use client'` directives and which can remain server components.

## Toolkit Setup

This skill requires the `nextjs-migration-toolkit` skill to be installed. All migration skills depend on it for AST analysis.

```bash
TOOLKIT_DIR="$(cd "$(dirname "$SKILL_PATH")/../nextjs-migration-toolkit" && pwd)"
if [ ! -f "$TOOLKIT_DIR/package.json" ]; then
  echo "ERROR: nextjs-migration-toolkit is not installed." >&2
  echo "Run: npx skills add blazity/next-migration-skills -s nextjs-migration-toolkit" >&2
  echo "Then retry this skill." >&2
  exit 1
fi
bash "$TOOLKIT_DIR/scripts/setup.sh" >/dev/null
```

## Version-Specific Patterns

Before applying any migration patterns, check the target Next.js version. Read `.migration/target-version.txt` if it exists, or ask the user.

Then read the corresponding version patterns file:

```bash
SKILL_DIR="$(cd "$(dirname "$SKILL_PATH")" && pwd)"
cat "$SKILL_DIR/../version-patterns/nextjs-<version>.md"
```

**Critical version differences that affect component migration:**
- **Next.js 14**: `params` and `searchParams` in page components are plain objects
- **Next.js 15+**: `params` and `searchParams` are Promises — async pages must `await` them, client pages must use `use()` from React

## Steps

### 1. Inventory All Components

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze components <srcDir>
```

### 2. Review Classification

For each component classified as "client":
- Review the client indicators (hooks, events, browser APIs)
- Determine if the entire component needs to be client, or if it can be split

### 3. Apply Client Directives

For components that must be client components:
- Add `'use client';` as the first line of the file
- Ensure all imports used by the client component are also client-compatible

### 4. Split Components Where Possible

If a component has both server and client parts:
- Extract the interactive part into a separate client component
- Keep the data-fetching and static rendering in the server component
- Import the client component into the server component

**Before — mixed component (Pages Router):**
```tsx
import { useState } from 'react';
import { useRouter } from 'next/router';

export default function ProductPage({ product }) {
  const router = useRouter();
  const [qty, setQty] = useState(1);

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <input type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} />
      <button onClick={() => alert(`Added ${qty}`)}>Add to Cart</button>
      <button onClick={() => router.back()}>Back</button>
    </div>
  );
}
```

**After — split into server + client (App Router):**

`app/products/[id]/page.tsx` (server component):
```tsx
import { Metadata } from 'next';
import { ProductActions } from './product-actions';

export async function generateMetadata({ params }): Promise<Metadata> {
  const product = await fetch(`https://api.example.com/products/${params.id}`,
    { cache: 'no-store' }).then(r => r.json());
  return { title: product.name };
}

export default async function ProductPage({ params }) {
  const product = await fetch(`https://api.example.com/products/${params.id}`,
    { cache: 'no-store' }).then(r => r.json());

  return (
    <div>
      <h1>{product.name}</h1>
      <p>{product.description}</p>
      <ProductActions />
    </div>
  );
}
```

`app/products/[id]/product-actions.tsx` (client component):
```tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export function ProductActions() {
  const router = useRouter();
  const [qty, setQty] = useState(1);

  return (
    <>
      <input type="number" value={qty} onChange={(e) => setQty(Number(e.target.value))} />
      <button onClick={() => alert(`Added ${qty}`)}>Add to Cart</button>
      <button onClick={() => router.back()}>Back</button>
    </>
  );
}
```

Key points in the split:
- Server component does the data fetching (async, no hooks)
- Client component handles all interactivity (useState, onClick, useRouter)
- `useRouter` import changes from `next/router` to `next/navigation`
- Props passed across the boundary must be serializable (no functions or Date objects)

### 5. Update Props

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze props <componentFile>
```

- Ensure props passed from server to client components are serializable
- No functions, classes, or Date objects as props across the boundary
- Convert non-serializable props to serializable alternatives

### 6. Validate Components

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" validate <appDir>
```

Check that:
- All files using client features have `'use client'`
- No server-only imports in client components
- No `next/router` usage (should be `next/navigation`)

## Common Pitfalls

### "You're importing a component that needs useState"
**Error**: `It only works in a Client Component but none of its parents are marked with "use client"`
**Cause**: A server component imports a component that uses hooks/events, but neither file has `'use client'`.
**Fix**: Add `'use client'` to the component that uses the hook — NOT to the page that imports it. The directive marks the boundary; everything imported by a client component is also client.

### Adding 'use client' too broadly
**Wrong**: Adding `'use client'` to a page component just because it imports one interactive child.
**Right**: Add `'use client'` only to the interactive component. Keep the page as a server component and import the client component into it.
**Rule of thumb**: Push `'use client'` as deep as possible in the component tree.

### Passing non-serializable props across the boundary
**Error**: `Functions cannot be passed directly to Client Components unless you explicitly expose it by marking it with "use server"`
**Cause**: A server component passes a function, Date object, or class instance as a prop to a client component.
**Fix**: Convert to serializable alternatives:
- Functions → Use server actions (`'use server'`) or pass data and let the client component create its own handlers
- Date objects → Pass as ISO string, parse in client
- Class instances → Pass as plain object

### The "children" pattern for mixing server + client
When a client component needs to render server content, use the children pattern:
```tsx
// layout.tsx (server component)
import { ClientShell } from './client-shell';
import { ServerContent } from './server-content';

export default function Layout() {
  return (
    <ClientShell>
      <ServerContent />   {/* Server component passed as children */}
    </ClientShell>
  );
}
```
This works because `children` is a React node (serializable), not a component reference.

### NEVER convert getServerSideProps data into useEffect + fetch
**Wrong**: Page had `getServerSideProps` providing data as props. You make the whole page `'use client'` and fetch data in a `useEffect` + `useState`:
```tsx
// WRONG — "use client" page with useEffect
'use client';
import { useState, useEffect } from 'react';

export default function AnalyticsPage() {
  const [data, setData] = useState(null);
  useEffect(() => {
    fetch('/api/analytics').then(r => r.json()).then(setData);
  }, []);
  if (!data) return <p>Loading...</p>;
  return <div>{data.pageViews}</div>;
}
```
**Why this is broken**: The HTTP response contains only "Loading..." — real data appears only after JavaScript executes on the client. This destroys SSR, breaks SEO, and fails any test that checks the server-rendered HTML for data content.

**Right**: Split into an async server component (fetches data) and a client component (handles interactivity). Data appears in the initial HTML response.
```tsx
// app/analytics/page.tsx (server component — NO 'use client')
import { getAnalyticsData } from '@/lib/analytics';
import { AnalyticsView } from './analytics-view';

export default async function AnalyticsPage() {
  const data = getAnalyticsData();
  return <AnalyticsView data={data} />;
}
```
```tsx
// app/analytics/analytics-view.tsx (client component)
'use client';
import { useState } from 'react';

export function AnalyticsView({ data }: { data: AnalyticsData }) {
  const [view, setView] = useState<'overview' | 'pages'>('overview');
  return (
    <div>
      <button onClick={() => setView('overview')}>Overview</button>
      <button onClick={() => setView('pages')}>Top Pages</button>
      {view === 'overview' ? <p>{data.pageViews}</p> : <p>...</p>}
    </div>
  );
}
```
**Rule**: If the original page had `getServerSideProps` or `getStaticProps`, the data fetching MUST stay in a server component. NEVER move it into `useEffect`. The only code that goes into the client component is the interactive UI (useState, onClick, etc.), receiving data as props.
