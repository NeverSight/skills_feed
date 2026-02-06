---
name: debug:nextjs
description: Debug Next.js issues systematically. Use when encountering SSR errors, hydration mismatches like "Text content did not match", routing issues with App Router or Pages Router, build failures, dynamic import problems, API route errors, middleware issues, caching and revalidation problems, or performance bottlenecks. Covers both Pages Router and App Router architectures.
---

# Next.js Debugging Guide

This guide provides a systematic approach to debugging Next.js applications, covering common error patterns, debugging tools, and resolution strategies for both development and production environments.

## Common Error Patterns

### 1. Hydration Mismatches

**Symptoms:**
```
Warning: Text content did not match. Server: '...' Client: '...'
Warning: Expected server HTML to contain a matching <div> in <div>
Hydration failed because the initial UI does not match what was rendered on the server
```

**Common Causes:**
- Using `Date.now()`, `Math.random()`, or timestamps in render
- Browser-only APIs accessed during SSR (`window`, `localStorage`, `document`)
- Conditional rendering based on client-only state
- Extension-injected HTML elements
- Invalid HTML nesting (e.g., `<p>` inside `<p>`, `<div>` inside `<p>`)

**Solutions:**
```tsx
// BAD: Causes hydration mismatch
function Component() {
  return <p>Current time: {new Date().toLocaleString()}</p>
}

// GOOD: Use useEffect for client-only values
'use client'
import { useState, useEffect } from 'react'

function Component() {
  const [time, setTime] = useState<string>('')

  useEffect(() => {
    setTime(new Date().toLocaleString())
  }, [])

  return <p>Current time: {time || 'Loading...'}</p>
}

// GOOD: Suppress hydration warning for intentional mismatches
<time suppressHydrationWarning>
  {new Date().toLocaleString()}
</time>
```

### 2. Server/Client Component Confusion

**Symptoms:**
```
Error: useState only works in Client Components. Add the "use client" directive
Error: You're importing a component that needs useEffect. It only works in a Client Component
Error: createContext only works in Client Components
```

**Understanding the Boundary:**
```tsx
// Server Component (default in App Router)
// - Can't use hooks (useState, useEffect, etc.)
// - Can't use browser APIs
// - CAN use async/await directly
// - CAN access backend resources directly

// app/page.tsx (Server Component)
async function Page() {
  const data = await db.query('SELECT * FROM posts') // Direct DB access
  return <PostList posts={data} />
}

// Client Component
// - CAN use hooks
// - CAN use browser APIs
// - Must be marked with 'use client'

// components/Counter.tsx
'use client'
import { useState } from 'react'

export function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}
```

**Context Provider Pattern:**
```tsx
// providers/theme-provider.tsx
'use client'
import { createContext, useContext, useState } from 'react'

const ThemeContext = createContext<{ theme: string } | null>(null)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState('light')
  return (
    <ThemeContext.Provider value={{ theme }}>
      {children}
    </ThemeContext.Provider>
  )
}

// app/layout.tsx (Server Component that uses Client Provider)
import { ThemeProvider } from '@/providers/theme-provider'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
```

### 3. Dynamic Import Issues

**Symptoms:**
```
Error: Element type is invalid. Received undefined
Module not found errors in production
Components rendering as null
```

**Solutions:**
```tsx
// Dynamic import with SSR disabled (for browser-only libraries)
import dynamic from 'next/dynamic'

const MapComponent = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <p>Loading map...</p>
})

// Dynamic import with named exports
const Modal = dynamic(() =>
  import('@/components/Modal').then(mod => mod.Modal)
)

// Dynamic import with error handling
const Chart = dynamic(
  () => import('@/components/Chart').catch(err => {
    console.error('Failed to load Chart:', err)
    return () => <div>Failed to load chart</div>
  }),
  { ssr: false }
)
```

### 4. API Route Errors

**App Router (Route Handlers):**
```tsx
// app/api/users/route.ts
import { NextRequest, NextResponse } from 'next/server'

// GET is cached by default - use dynamic to opt out
export const dynamic = 'force-dynamic'

export async function GET(request: NextRequest) {
  try {
    const searchParams = request.nextUrl.searchParams
    const id = searchParams.get('id')

    const data = await fetchUser(id)
    return NextResponse.json(data)
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    // Validate body...
    const result = await createUser(body)
    return NextResponse.json(result, { status: 201 })
  } catch (error) {
    if (error instanceof SyntaxError) {
      return NextResponse.json(
        { error: 'Invalid JSON' },
        { status: 400 }
      )
    }
    throw error
  }
}
```

**Common API Route Issues:**
```tsx
// ISSUE: Route Handler cached unexpectedly
// SOLUTION: Force dynamic rendering
export const dynamic = 'force-dynamic'
export const revalidate = 0

// ISSUE: Can't access cookies/headers
// SOLUTION: Import from next/headers
import { cookies, headers } from 'next/headers'

export async function GET() {
  const cookieStore = await cookies()
  const token = cookieStore.get('token')

  const headersList = await headers()
  const userAgent = headersList.get('user-agent')
}

// ISSUE: CORS errors
// SOLUTION: Add CORS headers
export async function GET() {
  const response = NextResponse.json({ data: 'test' })
  response.headers.set('Access-Control-Allow-Origin', '*')
  response.headers.set('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  return response
}

export async function OPTIONS() {
  return new NextResponse(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  })
}
```

### 5. Build Failures

**Common Build Errors:**

```bash
# Type errors during build
Error: Type error: Property 'x' does not exist on type 'y'
# Solution: Fix TypeScript errors or use type assertions

# Module resolution failures
Error: Module not found: Can't resolve '@/components/...'
# Solution: Check tsconfig.json paths and next.config.js

# Static generation failures
Error: getStaticPaths is required for dynamic SSG pages
# Solution: Add getStaticPaths or use generateStaticParams

# Image optimization errors
Error: Invalid src prop on next/image
# Solution: Configure domains in next.config.js
```

**next.config.js Debugging:**
```js
/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable verbose build output
  logging: {
    fetches: {
      fullUrl: true,
    },
  },

  // Debug image domains
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },

  // Analyze bundle size
  webpack: (config, { isServer }) => {
    if (process.env.ANALYZE) {
      const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer')
      config.plugins.push(
        new BundleAnalyzerPlugin({
          analyzerMode: 'static',
          reportFilename: isServer
            ? '../analyze/server.html'
            : './analyze/client.html',
        })
      )
    }
    return config
  },
}

module.exports = nextConfig
```

### 6. Middleware Issues

**Symptoms:**
```
Middleware triggered unexpectedly
Infinite redirect loops
Middleware not executing
Edge runtime compatibility errors
```

**Debugging Middleware:**
```tsx
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  // Debug: Log all middleware invocations
  console.log('Middleware:', request.method, request.nextUrl.pathname)

  // Check if this path should be handled
  const pathname = request.nextUrl.pathname

  // Skip static files and API routes if needed
  if (
    pathname.startsWith('/_next') ||
    pathname.startsWith('/api') ||
    pathname.includes('.')
  ) {
    return NextResponse.next()
  }

  // Example: Auth check
  const token = request.cookies.get('token')?.value

  if (!token && pathname.startsWith('/dashboard')) {
    const url = new URL('/login', request.url)
    url.searchParams.set('from', pathname)
    return NextResponse.redirect(url)
  }

  return NextResponse.next()
}

// Limit middleware to specific paths
export const config = {
  matcher: [
    // Match all paths except static files
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

### 7. Caching and Revalidation Issues

**Symptoms:**
```
Stale data after updates
Pages not revalidating
Unexpected cache hits/misses
```

**Solutions:**
```tsx
// Force dynamic rendering (no cache)
export const dynamic = 'force-dynamic'
export const revalidate = 0

// Time-based revalidation
export const revalidate = 60 // Revalidate every 60 seconds

// On-demand revalidation
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache'
import { NextRequest } from 'next/server'

export async function POST(request: NextRequest) {
  const { path, tag, secret } = await request.json()

  if (secret !== process.env.REVALIDATION_SECRET) {
    return Response.json({ error: 'Invalid secret' }, { status: 401 })
  }

  if (path) {
    revalidatePath(path)
  }
  if (tag) {
    revalidateTag(tag)
  }

  return Response.json({ revalidated: true, now: Date.now() })
}

// Using fetch with cache tags
async function getPosts() {
  const res = await fetch('https://api.example.com/posts', {
    next: { tags: ['posts'], revalidate: 3600 }
  })
  return res.json()
}
```

## Debugging Tools

### 1. VS Code Debugger Setup

Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Next.js: debug server-side",
      "type": "node-terminal",
      "request": "launch",
      "command": "npm run dev"
    },
    {
      "name": "Next.js: debug client-side",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000"
    },
    {
      "name": "Next.js: debug full stack",
      "type": "node",
      "request": "launch",
      "program": "${workspaceFolder}/node_modules/.bin/next",
      "args": ["dev"],
      "skipFiles": ["<node_internals>/**"],
      "serverReadyAction": {
        "action": "debugWithChrome",
        "pattern": "- Local:.+(https?://.+)",
        "uriFormat": "%s",
        "webRoot": "${workspaceFolder}"
      }
    }
  ]
}
```

### 2. Next.js 16.1+ Debug Flag

```bash
# Enable Node.js debugger directly
next dev --inspect

# With specific port
next dev --inspect=9229

# Break on first line
next dev --inspect-brk
```

### 3. Chrome DevTools

```bash
# Start with debugging
NODE_OPTIONS='--inspect' npm run dev

# Then open in Chrome:
# chrome://inspect
```

### 4. React DevTools

- Install browser extension
- Use Components tab to inspect component hierarchy
- Use Profiler tab to identify re-render issues
- Enable "Highlight updates when components render"

### 5. Next.js Error Overlay

The development error overlay provides:
- Full stack traces with source maps
- Component stack for React errors
- Quick links to open files in editor

Configure editor integration in `next.config.js`:
```js
module.exports = {
  experimental: {
    // Open files in VS Code
    serverActions: {
      bodySizeLimit: '2mb',
    },
  },
}
```

## The Four Phases of Next.js Debugging

### Phase 1: Reproduce and Isolate

**Steps:**
1. Reproduce the issue consistently
2. Determine if it's client-side, server-side, or build-time
3. Check if it occurs in development, production, or both
4. Isolate to a minimal reproduction

**Commands:**
```bash
# Test in development
npm run dev

# Test production build locally
npm run build && npm run start

# Check for TypeScript errors
npx tsc --noEmit

# Check for ESLint errors
npm run lint
```

### Phase 2: Gather Information

**Client-Side:**
```tsx
// Add debug logging
'use client'
import { useEffect } from 'react'

export function DebugComponent({ data }: { data: unknown }) {
  useEffect(() => {
    console.log('Component mounted with data:', data)
    console.log('Window location:', window.location.href)
    console.log('User agent:', navigator.userAgent)
  }, [data])

  return null
}
```

**Server-Side:**
```tsx
// app/page.tsx
export default async function Page() {
  console.log('Server rendering page')
  console.log('Environment:', process.env.NODE_ENV)
  console.log('Request time:', new Date().toISOString())

  const data = await fetchData()
  console.log('Fetched data:', JSON.stringify(data, null, 2))

  return <div>...</div>
}
```

**Request/Response Debugging:**
```tsx
// middleware.ts
export function middleware(request: NextRequest) {
  console.log('=== Request Debug ===')
  console.log('URL:', request.url)
  console.log('Method:', request.method)
  console.log('Headers:', Object.fromEntries(request.headers))
  console.log('Cookies:', request.cookies.getAll())

  const response = NextResponse.next()

  // Add debug header
  response.headers.set('X-Debug-Time', Date.now().toString())

  return response
}
```

### Phase 3: Analyze and Diagnose

**Check Build Output:**
```bash
# Analyze bundle
ANALYZE=true npm run build

# Check static/dynamic pages
npm run build
# Look for:
# - Static (SSG) pages: filled circle
# - Server-rendered (SSR): lambda
# - ISR pages: filled circle with revalidation time
```

**Check Network Requests:**
```tsx
// Wrap fetch for debugging
const originalFetch = global.fetch
global.fetch = async (...args) => {
  const [url, options] = args
  console.log('Fetch:', url, options?.method || 'GET')

  const start = Date.now()
  const response = await originalFetch(...args)
  const duration = Date.now() - start

  console.log('Response:', response.status, `${duration}ms`)
  return response
}
```

### Phase 4: Fix and Verify

**Common Fix Patterns:**

```tsx
// Fix 1: Add error boundary
// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  console.error('Error boundary caught:', error)

  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}

// Fix 2: Add loading state
// app/loading.tsx
export default function Loading() {
  return <div>Loading...</div>
}

// Fix 3: Handle async errors properly
async function getData() {
  try {
    const res = await fetch('...')
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}: ${res.statusText}`)
    }
    return res.json()
  } catch (error) {
    console.error('getData failed:', error)
    // Return fallback or re-throw
    return { error: true, data: null }
  }
}
```

## Quick Reference Commands

### Development
```bash
# Start development server
npm run dev
next dev

# Start with debugging
next dev --inspect
NODE_OPTIONS='--inspect' npm run dev

# Start with Turbopack (faster HMR)
next dev --turbopack

# Clear Next.js cache
rm -rf .next
```

### Building
```bash
# Production build
npm run build
next build

# Build with verbose output
NEXT_DEBUG=1 npm run build

# Analyze bundle size
ANALYZE=true npm run build
```

### Linting and Type Checking
```bash
# Run ESLint
npm run lint
next lint

# Fix ESLint errors
next lint --fix

# Type check
npx tsc --noEmit

# Type check with watch mode
npx tsc --noEmit --watch
```

### Production Testing
```bash
# Start production server
npm run start
next start

# Start on specific port
next start -p 3001

# Test production build locally
npm run build && npm run start
```

### Cache Management
```bash
# Clear all caches
rm -rf .next node_modules/.cache

# Clear just build cache
rm -rf .next

# Clear fetch cache (App Router)
# Add to fetch: { cache: 'no-store' }
# Or: export const revalidate = 0
```

### Debugging Specific Issues
```bash
# Check for circular dependencies
npx madge --circular --extensions ts,tsx ./app

# Find large dependencies
npx source-map-explorer .next/static/chunks/*.js

# Check bundle composition
npx @next/bundle-analyzer
```

## Environment-Specific Debugging

### Development vs Production Differences

```tsx
// Check environment
const isDev = process.env.NODE_ENV === 'development'
const isProd = process.env.NODE_ENV === 'production'

// Development-only logging
if (isDev) {
  console.log('Debug info:', data)
}

// Production error reporting
if (isProd && error) {
  // Send to error tracking service
  Sentry.captureException(error)
}
```

### Environment Variables
```bash
# Check env vars are loaded
console.log('Env check:', {
  NODE_ENV: process.env.NODE_ENV,
  API_URL: process.env.NEXT_PUBLIC_API_URL,
  // Note: Only NEXT_PUBLIC_* vars are available client-side
})
```

## Performance Debugging

### Web Vitals Monitoring
```tsx
// app/layout.tsx
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <SpeedInsights />
      </body>
    </html>
  )
}

// Custom Web Vitals reporting
// pages/_app.tsx (Pages Router)
export function reportWebVitals(metric) {
  console.log(metric.name, metric.value)
  // Send to analytics
}
```

### React Profiler
```tsx
import { Profiler } from 'react'

function onRenderCallback(
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) {
  console.log(`${id} ${phase}: ${actualDuration.toFixed(2)}ms`)
}

export default function App() {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      <MainComponent />
    </Profiler>
  )
}
```

## Sources and References

This guide was compiled using information from:

- [Next.js Official Debugging Guide](https://nextjs.org/docs/app/guides/debugging)
- [Next.js 16.1 Release Notes](https://nextjs.org/blog/next-16-1)
- [Vercel: Common Next.js App Router Mistakes](https://vercel.com/blog/common-mistakes-with-the-next-js-app-router-and-how-to-fix-them)
- [Next.js Error Handling Documentation](https://nextjs.org/docs/app/getting-started/error-handling)
- [8 Tips for Debugging Next.js Applications](https://www.bretcameron.com/blog/eight-tips-for-debugging-next-js-applications)
- [How to Debug Next.js with VS Code](https://tymick.me/blog/debug-nextjs-with-vs-code)
- [Debugging Next.js Like a Pro](https://medium.com/@farihatulmaria/debugging-next-js-like-a-pro-tools-and-techniques-for-production-grade-apps-b8818c66c953)
- [10 Common Next.js Bugs and How to Fix Them](https://medium.com/@sureshdotariya/10-common-next-js-bugs-and-how-to-fix-them-in-2025-4ac3cc8c7581)
- [Next.js 15 Error Handling Best Practices](https://devanddeliver.com/blog/frontend/next-js-15-error-handling-best-practices-for-code-and-routes)
