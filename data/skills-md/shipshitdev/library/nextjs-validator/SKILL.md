---
name: nextjs-validator
description: Validate Next.js 16 configuration and detect/prevent deprecated patterns. Ensures proxy.ts usage, Turbopack, Cache Components, and App Router best practices. Use before any Next.js work or when auditing existing projects.
version: 1.0.0
tags:
  - nextjs
  - validation
  - frontend
  - react
  - turbopack
---

# Next.js Validator

Validates Next.js 16 configuration and prevents deprecated patterns. AI assistants often generate Next.js 14/15 patterns - this skill enforces Next.js 16.

## When This Activates

- Setting up a new Next.js project
- Before any Next.js development work
- Auditing existing Next.js projects
- After AI generates Next.js code
- CI/CD pipeline validation

## Quick Start

```bash
python3 ~/.claude/skills/nextjs-validator/scripts/validate.py --root .
python3 ~/.claude/skills/nextjs-validator/scripts/validate.py --root . --strict
```

## What Gets Checked

### 1. Package Version

```json
// GOOD: v16+
"next": "^16.0.0"

// BAD: v15 or earlier
"next": "^15.0.0"
```

### 2. Proxy vs Middleware

**GOOD - Next.js 16:**

```typescript
// proxy.ts (Node.js runtime - REQUIRED)
import { createProxy } from 'next/proxy';
export const proxy = createProxy();
```

**BAD - Deprecated:**

```typescript
// middleware.ts (Edge runtime - DEPRECATED)
export function middleware() { }
```

### 3. App Router Structure

**GOOD:**

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Home page
├── (routes)/           # Route groups
│   ├── dashboard/
│   │   └── page.tsx
│   └── settings/
│       └── page.tsx
└── api/                # API routes (optional)
```

**BAD - Pages Router (deprecated):**

```
pages/
├── _app.tsx
├── index.tsx
└── api/
```

### 4. Cache Components & `use cache`

**GOOD - Next.js 16:**

```typescript
// app/dashboard/page.tsx
'use cache';

export default async function Dashboard() {
  const data = await fetch('/api/data');
  return <DashboardView data={data} />;
}
```

### 5. Server Actions

**GOOD:**

```typescript
// app/actions.ts
'use server';

export async function createItem(formData: FormData) {
  // Server-side logic
}
```

### 6. Turbopack Configuration

**GOOD - Default in Next.js 16:**

```json
// next.config.ts (Turbopack is default, no config needed)
```

**BAD - Disabling Turbopack:**

```json
// Don't disable unless absolutely necessary
experimental: {
  turbo: false  // BAD
}
```

### 7. Config File Format

**GOOD - TypeScript config:**

```typescript
// next.config.ts
import type { NextConfig } from 'next';

const config: NextConfig = {
  // ...
};

export default config;
```

**BAD - JavaScript config:**

```javascript
// next.config.js - Prefer .ts
module.exports = { }
```

## Deprecated Patterns to Avoid

| Deprecated (v15-) | Replacement (v16+) |
|-------------------|-------------------|
| `middleware.ts` | `proxy.ts` |
| `getServerSideProps` | Server Components + `use cache` |
| `getStaticProps` | Server Components + `use cache` |
| `getStaticPaths` | `generateStaticParams` |
| `_app.tsx` | `app/layout.tsx` |
| `_document.tsx` | `app/layout.tsx` |
| `pages/` directory | `app/` directory |
| `next/router` | `next/navigation` |
| `useRouter()` (pages) | `useRouter()` from `next/navigation` |

## Next.js 16 Features to Use

### Cache Components

```typescript
'use cache';

// Entire component cached
export default async function CachedPage() {
  const data = await fetchData();
  return <View data={data} />;
}
```

### Partial Pre-Rendering (PPR)

```typescript
// next.config.ts
const config: NextConfig = {
  experimental: {
    ppr: true,
  },
};
```

### Next.js DevTools MCP

AI-assisted debugging with contextual insight:

```typescript
// Enable in development
// Works with Claude Code and other MCP-compatible tools
```

### Parallel Routes

```
app/
├── @modal/
│   └── login/
│       └── page.tsx
├── @sidebar/
│   └── default.tsx
└── layout.tsx
```

### Intercepting Routes

```
app/
├── feed/
│   └── page.tsx
├── photo/
│   └── [id]/
│       └── page.tsx
└── @modal/
    └── (.)photo/
        └── [id]/
            └── page.tsx
```

## Validation Output

```
=== Next.js 16 Validation Report ===

Package Version: next@16.1.0 ✓

File Structure:
  ✓ Using app/ directory (App Router)
  ✗ Found pages/ directory - migrate to App Router
  ✓ Found proxy.ts
  ✗ Found middleware.ts - migrate to proxy.ts

Patterns:
  ✓ Using Server Components
  ✗ Found getServerSideProps in 2 files
  ✓ Using next/navigation

Config:
  ✓ next.config.ts (TypeScript)
  ✓ Turbopack enabled (default)

Summary: 2 issues found
  - Migrate pages/ to app/ directory
  - Replace middleware.ts with proxy.ts
```

## Migration Guide

### From middleware.ts to proxy.ts

**Before (v15):**

```typescript
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(request) {
  // Edge runtime
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*'],
};
```

**After (v16):**

```typescript
// proxy.ts
import { createProxy } from 'next/proxy';

export const proxy = createProxy({
  // Node.js runtime
  async handle(request) {
    // Full Node.js APIs available
    return request;
  },
  matcher: ['/dashboard/:path*'],
});
```

### From getServerSideProps to Server Components

**Before:**

```typescript
// pages/dashboard.tsx
export async function getServerSideProps() {
  const data = await fetchData();
  return { props: { data } };
}

export default function Dashboard({ data }) {
  return <View data={data} />;
}
```

**After:**

```typescript
// app/dashboard/page.tsx
export default async function Dashboard() {
  const data = await fetchData();
  return <View data={data} />;
}
```

## CI/CD Integration

```yaml
# .github/workflows/validate.yml
- name: Validate Next.js 16
  run: |
    python3 ~/.claude/skills/nextjs-validator/scripts/validate.py \
      --root . \
      --strict \
      --ci
```

## Integration

- `tailwind-validator` - Validate Tailwind v4 config
- `biome-validator` - Validate Biome 2.3+ config
- `clerk-validator` - Validate Clerk auth setup
