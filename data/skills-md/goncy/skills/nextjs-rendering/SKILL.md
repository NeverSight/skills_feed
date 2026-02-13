---
name: nextjs-rendering
description: >-
  Provides expert guidance on Next.js rendering behavior, including static vs dynamic rendering, streaming, Suspense boundaries, and the prospective render system. Use when working with Next.js SSG, ISR, streaming, or server components.
---

# Next.js Rendering Expert Guidance

## Core Concepts

### Static vs Dynamic Rendering

Understand the fundamental distinction between static and dynamic rendering:

- **Static pages do not involve compute.** They are pre-built, uploaded to a CDN, and replicated to edge locations globally. This means static content remains available even if a region goes down and serves faster because it's cached near the user with no compute overhead.

- **Dynamic pages execute in a specific region** where the serverless function is configured to run. They require compute on every request, making them slower and dependent on regional availability.

- **SSG and ISR are the same rendering mode.** The only difference is whether you generate all paths upfront (SSG) or incrementally on-demand (ISR). Both produce static output.

- **Cache components can combine static and dynamic behavior,** but the page itself is still fundamentally either static or dynamic. Even with cache components, the underlying render mode matters.

### The Prospective Render System

Next.js uses a two-phase render to determine what is static vs dynamic:

1. **Warmup render (prospective render):** Next.js searches for cached instances and fills those caches. This phase identifies what can be resolved synchronously.

2. **Microtask check:** Next.js runs a second render that executes for just one tick, then aborts. Everything that resolves within that single microtask is considered "instant" and therefore static.

This two-render mechanism is how Next.js determines whether components are async or not without explicit developer annotation.

## Streaming and Suspense

### Streaming Behavior in Static Rendering

**Static content does not support streaming** because no compute is involved at request time. The entire page is pre-generated and served as a complete asset.

- **Suspense boundary fallbacks will not show when generating ISR paths.** The page is built fully before being cached, so users never see intermediate loading states.

- **Streaming only works with dynamic rendering** where the server can flush partial content while waiting for async operations.

### Enabling Streaming for Dynamic Pages

To allow the server to stream a page without requiring a complete skeleton upfront:

```jsx
<Suspense fallback={null}>
  {/* Wrap your entire HTML document */}
  <html>
    <body>{children}</body>
  </html>
</Suspense>
```

**Wrap the HTML document with an empty Suspense boundary.** Without a document element outside the boundary, there's nothing to stream—the server needs an outer shell to flush to the client.

## Determining Static vs Dynamic

### Async Dynamic APIs

Next.js uses **async dynamic APIs as signals** to determine when something must be dynamic:

- **Anything that cannot run in a single tick becomes dynamic.** If an operation requires awaiting beyond the initial microtask, Next.js marks that render as dynamic.

- **Exception: `params` can still create static routes** because `params` is called once per item returned by `generateStaticParams`. Since each invocation is synchronous within that static generation context, it's considered "instant."

```tsx
// This can still be static if generateStaticParams provides the params
export async function generateStaticParams() {
  return [{ id: '1' }, { id: '2' }];
}

export default async function Page({ params }: { params: { id: string } }) {
  // params is "instant" here because it's called once per static param
  const { id } = params;
  // ...
}
```

## Using Cache Directives

### "use cache" Behavior

Adding `"use cache"` to a page or its main component fundamentally changes its output:

```tsx
'use cache';

export default function Page() {
  // This produces static output
}
```

**When you add "use cache" to a page component, you are producing static output** that will be:
- Cached and reused
- Not streamed (served as complete HTML)
- Not have holes or Suspense boundaries that resolve at request time

Even in a dynamic app, cache directives convert specific subtrees to static behavior with all the implications of static rendering (no streaming, no runtime Suspense resolution).

## Common Pitfalls

### Expecting Streaming in Static Contexts

Do not expect Suspense fallbacks or streaming to work when:
- Generating ISR paths
- Using `"use cache"` on page components
- Building SSG routes

In all these cases, the page is fully rendered during build/revalidation, not at request time.

### Misunderstanding Regional Failures

Remember that **dynamic content fails if its configured region goes down,** while static content remains available globally. Design critical paths as static when high availability is required.

### Forgetting the Prospective Render

When debugging why something is marked as dynamic, remember that **Next.js aborts a render after one tick** to detect async work. If your code performs any async operation that doesn't resolve in a microtask, it becomes dynamic, even if it seems "fast."