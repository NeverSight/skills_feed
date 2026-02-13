---
name: nextjs-caching
description: >-
  Provides expert guidance on Next.js caching behavior, including use cache directive, revalidation strategies, ISR patterns, and common pitfalls. Use when working with Next.js caching, revalidatePath, revalidateTag, use cache, or stale-while-revalidate patterns.
---

# Next.js Caching Expert Guidance

This skill provides expert-level guidance on Next.js caching behavior, focusing on the `"use cache"` directive, revalidation strategies, and Incremental Static Regeneration (ISR) patterns.

## Core Mental Models

### The "use cache" Directive

The `"use cache"` directive **marks** a component or function as cacheable—it doesn't immediately cache anything. Caching happens at build time when Next.js writes the output to the cache store. This is a fundamental distinction that affects how you reason about cache behavior.

### Automatic Static Rendering

Next.js automatically renders from top to bottom as deep as possible until it encounters something dynamic (like uncached data fetches). It then creates a "dynamic hole" for that content. You don't need to add `"use cache"` to every page—the framework handles partial static rendering automatically. Cached functions are NOT considered dynamic, so they don't create holes.

### Two-Phase Rendering

Two renders occur during the build process:
1. **Warmup render (prospective render)**: Detects if dynamic APIs are used. Anything that doesn't resolve in a microtask is considered dynamic.
2. **Final render**: Captures the actual output for the pre-rendered result.

## Key Behaviors

### ISR-Like Behavior

Adding `"use cache"` to a **page component** makes it work like ISR—the entire output gets cached instead of having dynamic holes. Caches cannot be partial at the page level. To make a route ISR-like, add `"use cache"` to the main exported component (either at the top of the file or on the component itself).

### Layout vs Page Caching

Setting `"use cache"` in a layout without setting it on the page does NOT make the page static. Each route segment controls its own caching behavior independently.

### Suspense Boundaries with "use cache"

When you use `"use cache"` on a component with a Suspense boundary (containing components that fetch data), it works like ISR. The first request triggers the Suspense boundary, shows content, then caches the result for subsequent requests. If you want the Suspense boundary to show dynamic content every time, extract static parts into separate components with their own `"use cache"` directives (or use parallel routes).

## Critical Distinctions

### Revalidation APIs

- `revalidatePath` is conceptually similar to `revalidateTag`, with the argument being path-like
- `revalidateTag` revalidates in a stale-while-revalidate manner when used in server actions
- `updateTag` works as "read-your-own-writes" by purging the previous cache immediately, but cannot be used in route handlers

### Cache Persistence

- `unstable_cache` persists across deployments
- `use cache: remote` does NOT persist across deployments
- Choose based on whether you need deployment-persistent caching

## Common Patterns

### Partial Page Caching

To cache only parts of a page while keeping others dynamic:
- Leave the page without `"use cache"`
- Add `"use cache"` to individual components
- Wrap dynamic components in Suspense boundaries as needed
- Alternative: Use parallel routes for the same effect

### Sharing Cached Values

When you need a cached value from a layout in a page, cache the function output instead of the component. Call the function again in the page to retrieve the cached value.

### Build-Time Snapshots

Every cacheable function gets a snapshot when called at build time. Using a `"use cache"`'d function in a dynamic component only guarantees a cache hit if that snapshot was captured at build time. Otherwise, it serves from in-memory cache.

## API & Configuration Details

### Dynamic API Replacement

Use `connection()` as a replacement for `unstable_noStore()`.

### Short Cache Behavior

Caches with a `stale` configuration of less than 30 seconds are considered "short cache" and won't be included in runtime prefetch.

### unstable_cache Functions

`unstable_cache` functions are considered instant (they don't create dynamic holes).

## generateStaticParams Requirements

- Export at least one param in `generateStaticParams` to actually generate a static shell for that route
- Without `generateStaticParams`, dynamic pages fail because there's no Suspense boundary when reading params
- Workaround: Add a `loading.tsx` file or wrap the body in an empty Suspense boundary
- For ISR behavior on dynamic pages, always export at least one param from `generateStaticParams`
- If no real param exists, return a placeholder and handle that case in component rendering

## Deployment Architecture

The proxy that returns the static shell runs on the edge. It returns the shell immediately and continues the request for dynamic content. If a region goes down, the proxy continues working.

## Verification

Static pages sometimes show as `ppr` in the build log. The most reliable way to verify a page is static is checking that `x-nextjs-cache` header equals `HIT` in the document request.

## References

For comprehensive details, code examples, and deep-dives into each topic:

- **references/detailed-guide.md** — Full expanded guidance with all insights organized by topic. Consult this when you need detailed explanations, edge cases, or specific implementation patterns.