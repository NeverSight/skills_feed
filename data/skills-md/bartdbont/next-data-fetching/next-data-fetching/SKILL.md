---
name: next-data-fetching
description: Next.js App Router data fetching decision tree focused on TTFB-first and honest UX. Use when adding or changing data fetching logic (RSC fetch, caching, SSG/ISR, streaming Suspense), when metadata or generateMetadata depends on remote data, when dealing with user-specific auth/session data, when implementing hybrid server prefetch plus client hydration (TanStack Query), or when reviewing TTFB/LCP regressions.
---

# Next Data Fetching

## Overview

Choose where and how to fetch data in Next.js (App Router) using a consistent decision tree.
Optimize for good TTFB without lying UX: defer only what the page can be content-correct without.

## Workflow (Decision Tree)

Ask these questions in order for each dataset you introduce (or change):

1. Is the page content-correct without this data on first render?
2. Does SEO/metadata depend on it (including `generateMetadata`)?
3. Is it user-specific (auth/session/permissions)?
4. Is it static or safe-to-cache for everyone (static/semi-static)?
5. What is the expected request latency and payload size?
6. Does the data need to remain interactive after load (filters, refetch, live updates)?

Use the answers to pick one of these patterns:

- `SSG` / `ISR` for static or semi-static, non-user-specific, SEO-relevant data.
- `Blocking server fetch` for fast and small requests where blocking TTFB is acceptable.
- `Server fetch + Suspense (streaming)` when data is needed but slower, and the rest of the page can render content-correct without it.
- `Client-side fetch` when data is not needed for first render, or when it is heavy/slow and can be deferred without making the page misleading.
- `Hybrid` (server fetch + client hydrate) when initial server data is needed but the data stays interactive after load.

See `references/decision-tree.md` for the full tree (including latency/payload thresholds).

## Rules Of Thumb

- Treat Suspense as a UX choice, not a default performance trick; only stream what can load independently and does not make the page misleading.
- If data is user-specific, exclude `SSG` and `ISR`.
- If SEO/metadata depends on data, fetch on the server (and likely before render).
- When in doubt, answer: can the page be content-correct without this data?

## App Router Notes

- `cookies()` / `headers()` make a route dynamic; avoid them in static/ISR pages.
- Prefer parallel server fetching (start promises early; `Promise.all` for independent calls).
- Minimize RSC-to-client serialization; pass only what client components actually need.

## Resources

- `references/decision-tree.md` - English version of the decision tree + thresholds (with Mermaid diagram)
- `references/patterns-app-router.md` - Implementation templates for each choice (App Router)
- `references/examples.md` - Worked examples based on the team wiki
- `references/review-checklist.md` - Code review checklist (TTFB/LCP, caching, UX correctness)
- `assets/decision-tree-nl.png` - Original diagram (Dutch)
