---
name: route-conversion
description: >
  Use when converting a specific page from pages/ to app/ directory, or
  migrating a route end-to-end (file structure, data fetching, metadata,
  imports). The main workhorse skill for per-route migration.
---

# Route Conversion

Convert a specific page from pages/ directory to app/ directory, handling data fetching migration, metadata extraction, and file structure changes.

## Iron Law

```
ONE ROUTE AT A TIME. VALIDATE BEFORE MOVING ON. DELETE THE OLD FILE.
```

Every route follows the full cycle: analyze → convert → validate → delete old file → build.
Skip a step? You'll ship broken code. "I'll validate later" means "I'll debug for hours later."

**Prerequisites:**
- **REQUIRED:** Run `migration-assessment` first if this is the start of a migration. No exceptions — even "simple" codebases have hidden blockers.
- **REQUIRED:** Ensure `app/layout.tsx` exists before converting any route. If it doesn't, convert `pages/_app.tsx` + `pages/_document.tsx` first.

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

**Critical version differences that affect route conversion:**
- **Next.js 14**: `params` and `searchParams` are plain objects — direct access
- **Next.js 15+**: `params` and `searchParams` are Promises — MUST `await`
- **Next.js 14**: `cookies()` is SYNCHRONOUS
- **Next.js 15+**: `cookies()` is ASYNC — MUST `await`

The examples below show patterns that work across versions. Check the version patterns file for exact syntax.

## Steps

### 1. Analyze the Source Route

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" analyze routes <pagesDir>
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform data-fetching <sourceFile>
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform imports <sourceFile> --dry-run
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform router <sourceFile>
```

### 2. Create App Router File Structure

Map the pages/ path to app/ path:
- `pages/index.tsx` → `app/page.tsx`
- `pages/about.tsx` → `app/about/page.tsx`
- `pages/blog/[slug].tsx` → `app/blog/[slug]/page.tsx`
- `pages/api/posts.ts` → `app/api/posts/route.ts`
- `pages/_app.tsx` → `app/layout.tsx` (root layout)
- `pages/_document.tsx` → `app/layout.tsx` (merge into root layout)

### 3. Migrate Data Fetching

Based on the data-fetching analysis, apply the appropriate pattern. See the `data-layer-migration` skill for detailed before/after examples of each pattern.

| Pages Router | App Router |
|-------------|------------|
| `getStaticProps` | Async server component + `fetch()` with `{ cache: 'force-cache' }` |
| `getStaticProps` + revalidate | Async server component + `{ next: { revalidate: N } }` |
| `getServerSideProps` | Async server component + `{ cache: 'no-store' }` |
| `getStaticPaths` | `export async function generateStaticParams()` |

### 4. Extract Metadata

**Before** (using `next/head`):
```tsx
import Head from 'next/head';

export default function AboutPage() {
  return (
    <>
      <Head>
        <title>About Us</title>
        <meta name="description" content="Learn about our company" />
        <meta property="og:title" content="About Us" />
      </Head>
      <h1>About Us</h1>
    </>
  );
}
```

**After** (using metadata export):
```tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'About Us',
  description: 'Learn about our company',
  openGraph: { title: 'About Us' },
};

export default function AboutPage() {
  return <h1>About Us</h1>;
}
```

For dynamic metadata (needs params or fetched data), use `generateMetadata`:
```tsx
import { Metadata } from 'next';

export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await fetch(`https://api.example.com/posts/${params.slug}`).then(r => r.json());
  return { title: post.title, description: post.excerpt };
}
```

Rules:
- Remove all `next/head` imports and `<Head>` usage
- Static metadata → `export const metadata: Metadata`
- Dynamic metadata → `export async function generateMetadata()`
- `next-seo` → replace with the metadata export API

### 5. Update Imports

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" transform imports <newFile>
```

- Rewrite `next/router` to `next/navigation`
- Remove `next/head` imports
- Update component imports for new file paths

### 6. Validate and Finalize

**This step is NOT optional. Do not proceed to the next route without completing it.**

```bash
npx tsx "$TOOLKIT_DIR/src/bin/ast-tool.ts" validate <appDir>
```

After validation passes:
1. **Delete the old pages/ file.** The route must not exist in both directories.
2. **Run `npx next build`** to catch type errors, missing exports, and boundary violations.
3. Confirm the build succeeds before claiming this route is done.

## Route Completion Checklist

Before moving to the next route, verify ALL of these:

- [ ] New `app/` file created with correct naming (`page.tsx` inside a folder)
- [ ] Data fetching migrated (no getStaticProps/getServerSideProps/getStaticPaths)
- [ ] Metadata extracted (no `next/head` or `<Head>` usage)
- [ ] Imports updated (`next/navigation`, not `next/router`)
- [ ] Validator passes with no errors
- [ ] Old `pages/` file deleted
- [ ] `npx next build` succeeds

**Cannot check all boxes? The route is not done. Fix issues before proceeding.**

## Red Flags — STOP If You Catch Yourself Thinking:

- "I'll validate all the routes at the end" — No. Validate each route individually. Batch errors compound.
- "I'll delete the old files later" — No. Delete immediately. Forgetting creates conflict errors.
- "It compiles, so it's done" — Compiling is not validating. Run the validator AND build.
- "This is a simple page, I can skip analysis" — Simple pages have hidden dependencies. Run the analyzer.
- "I don't need to run assessment first, I can see what needs migrating" — Assessment catches blockers you can't see by reading code.

## Common Pitfalls

### Wrong file naming in app/ directory
**Wrong**: `app/about.tsx` (will not be recognized as a route)
**Right**: `app/about/page.tsx` (every route needs a `page.tsx` inside a folder)
**Exception**: `app/page.tsx` is the root route (replaces `pages/index.tsx`)

### Forgetting the root layout
**Error**: `A required layout.tsx file was not found at root level`
**Fix**: The `app/` directory must have a root `layout.tsx`. Convert `pages/_app.tsx` and `pages/_document.tsx` into:
```tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

### Using `router.query` after migration
**Error**: `router.query` is undefined or doesn't exist on the App Router's router.
**Cause**: App Router's `useRouter()` (from `next/navigation`) does not have `.query`. Use `useParams()` for path parameters and `useSearchParams()` for query strings.
**Fix**:
```tsx
// Before (Pages Router)
const { slug, page } = router.query;

// After (App Router)
import { useParams, useSearchParams } from 'next/navigation';
const { slug } = useParams();
const searchParams = useSearchParams();
const page = searchParams.get('page');
```

### Missing Suspense boundary for useSearchParams()
**Error**: Page using `useSearchParams()` renders an error shell or empty HTML instead of content. Next.js logs: `useSearchParams() should be wrapped in a suspense boundary`.
**Cause**: In App Router, `useSearchParams()` in a client component triggers a client-side-only render unless wrapped in `<Suspense>`. Without it, Next.js cannot statically render the page and returns an error boundary.
**Fix**: Wrap the component using `useSearchParams()` in a `<Suspense>` boundary. The cleanest approach is a server page that wraps a client component:
```tsx
// app/search/page.tsx (server component)
import { Suspense } from 'react';
import { SearchContent } from './search-content';

export default function SearchPage() {
  return (
    <Suspense fallback={<p>Loading...</p>}>
      <SearchContent />
    </Suspense>
  );
}
```
```tsx
// app/search/search-content.tsx (client component)
'use client';
import { useSearchParams } from 'next/navigation';

export function SearchContent() {
  const searchParams = useSearchParams();
  const q = searchParams.get('q') || '';
  // ... render search results
}
```
**Rule**: EVERY use of `useSearchParams()` MUST have a `<Suspense>` boundary as an ancestor. No exceptions.

### Returning inline fallback JSX instead of notFound()
**Wrong**: When `getServerSideProps` returned `{ notFound: true }`, replacing it with inline JSX that renders "not found" text with a 200 status:
```tsx
// WRONG — returns HTTP 200 with "not found" text
export default async function UserPage({ params }) {
  const user = getUser(params.id);
  if (!user) return <p>User not found</p>; // HTTP 200!
  return <div>{user.name}</div>;
}
```
**Right**: Use `notFound()` from `next/navigation` to trigger the proper HTTP 404 response and the nearest `not-found.tsx` boundary:
```tsx
import { notFound } from 'next/navigation';

export default async function UserPage({ params }) {
  const user = getUser(params.id);
  if (!user) notFound(); // HTTP 404!
  return <div>{user.name}</div>;
}
```
**Rule**: If the original `getServerSideProps` returned `{ notFound: true }`, the migrated page MUST call `notFound()` from `next/navigation`. NEVER replace it with inline fallback JSX.

### Using manual wrapper components instead of nested layout.tsx
**Wrong**: The Pages Router code wraps every dashboard page in a `<DashboardLayout>` component. You keep doing the same in App Router:
```tsx
// WRONG — manually wrapping each page
// app/dashboard/page.tsx
import { DashboardLayout } from '@/components/DashboardLayout';
export default function DashboardPage() {
  return <DashboardLayout><h1>Dashboard</h1></DashboardLayout>;
}
// app/dashboard/settings/page.tsx
import { DashboardLayout } from '@/components/DashboardLayout';
export default function SettingsPage() {
  return <DashboardLayout><h1>Settings</h1></DashboardLayout>;
}
```
**Right**: Create a `layout.tsx` in the shared route segment. App Router renders it automatically around all child pages:
```tsx
// app/dashboard/layout.tsx — applied automatically to ALL /dashboard/* pages
export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ display: 'flex' }}>
      <aside>/* sidebar nav */</aside>
      <main>{children}</main>
    </div>
  );
}
```
```tsx
// app/dashboard/page.tsx — NO manual wrapper needed
export default function DashboardPage() {
  return <h1>Dashboard</h1>;
}
```
**Rule**: When multiple pages in `pages/section/*` all import and render the same layout wrapper component, create `app/section/layout.tsx` instead. Do NOT manually wrap each page.

### Route conflict from not deleting old file
**Error**: `Conflicting app and page file was found` or route resolves to wrong page.
**Cause**: The same route exists in both `pages/` and `app/`. Next.js does not know which to use.
**Fix**: Delete the `pages/` file immediately after converting and validating the `app/` version. Do not batch deletions — delete as part of each route's conversion cycle.
