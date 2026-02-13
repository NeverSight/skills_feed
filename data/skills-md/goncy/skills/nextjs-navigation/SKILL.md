---
name: nextjs-navigation
description: >-
  Provides expert guidance on Next.js App Router navigation, prefetching behavior, and Link component configuration. Use when working with Next.js navigation, Link prefetching, or App Router routing.
---

## Link Component Prefetching Behavior

### Understanding prefetch Prop Values

The `prefetch` prop on Next.js `<Link>` components has three distinct behaviors in App Router:

**`prefetch={false}`** - Completely disables prefetching, including on hover. This is a breaking change from Pages Router, where `prefetch={false}` would still prefetch on hover. Use this when you want to prevent any prefetching whatsoever.

```tsx
<Link href="/dashboard" prefetch={false}>
  Dashboard
</Link>
```

**`prefetch={undefined}`** (default) - Only prefetches static routes. Dynamic routes are not prefetched until navigation occurs. Use this default behavior when you have a mix of static and dynamic routes and want to optimize initial load performance.

**`prefetch={true}`** - Prefetches both static and dynamic routes. Use this for critical navigation paths where you want to ensure the fastest possible navigation experience, even for dynamic content.

```tsx
<Link href="/profile/[id]" prefetch={true}>
  User Profile
</Link>
```

## Suspense Boundaries and Search Params

### Same-Page Navigation Issue

When navigating on the same page with only search parameter changes, Suspense boundaries do not re-trigger their loading states by default. This can create a poor user experience where the UI appears frozen during data refetching.

### Solution: Key-Based Suspense

Force Suspense boundaries to show loading states during search param changes by providing a unique `key` prop that includes the changing search parameter:

```tsx
// app/search/page.tsx
export default function SearchPage({ 
  searchParams 
}: { 
  searchParams: { q?: string } 
}) {
  return (
    <Suspense 
      key={searchParams.q} 
      fallback={<LoadingSpinner />}
    >
      <SearchResults query={searchParams.q} />
    </Suspense>
  )
}
```

The key change ensures React treats the Suspense boundary as a new instance, properly displaying the fallback during the transition.

## Type Safety

### Typing Page Props

Use the `PageProps` helper type to correctly type page component props in App Router:

```tsx
import type { PageProps } from 'next'

export default function Page({ params, searchParams }: PageProps) {
  // params and searchParams are properly typed
}
```

This helper provides accurate types for the `params` and `searchParams` objects passed to page components, improving type safety and developer experience.

## Component State Preservation

### cacheComponents Flag

When the `cacheComponents` experimental flag is enabled, Next.js leverages React's `<Activity>` component to maintain component state across client-side navigations:

```tsx
// next.config.js
module.exports = {
  experimental: {
    cacheComponents: true
  }
}
```

This preserves component state (such as form inputs, scroll position, or local component state) when users navigate away and return, creating a more native app-like experience. The `<Activity>` component handles the state preservation automatically without requiring manual state management.