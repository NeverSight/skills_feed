---
name: nextjs
description: Next.js 16 App Router performance optimization guidelines (formerly nextjs-16-app-router). This skill should be used when writing Next.js 16 code, configuring caching, implementing Server Components in Next.js, setting up App Router routing, or configuring next.config.js. This skill does NOT cover generic React 19 patterns (use react-19 skill) or non-Next.js server rendering.
---

# Next.js Community Next.js 16 App Router Best Practices

Comprehensive performance optimization guide for Next.js 16 App Router applications, maintained by the Next.js Community. Contains 40 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Next.js 16 App Router code
- Configuring caching strategies with 'use cache' directive
- Implementing server components and data fetching
- Setting up routing with parallel and intercepting routes
- Creating server actions for form handling and mutations

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Build & Bundle Optimization | CRITICAL | `build-` |
| 2 | Caching Strategy | CRITICAL | `cache-` |
| 3 | Server Components & Data Fetching | HIGH | `server-` |
| 4 | Routing & Navigation | HIGH | `route-` |
| 5 | Server Actions & Mutations | MEDIUM-HIGH | `action-` |
| 6 | Streaming & Loading States | MEDIUM | `stream-` |
| 7 | Metadata & SEO | MEDIUM | `meta-` |
| 8 | Client Components | LOW-MEDIUM | `client-` |

## Quick Reference

### 1. Build & Bundle Optimization (CRITICAL)

- `build-optimize-package-imports` - Configure optimizePackageImports for Icon Libraries
- `build-dynamic-imports` - Use Dynamic Imports for Heavy Components
- `build-barrel-files` - Avoid Barrel File Imports in App Router
- `build-turbopack-config` - Enable Turbopack File System Caching
- `build-external-packages` - Configure Server External Packages for Node Dependencies

### 2. Caching Strategy (CRITICAL)

- `cache-use-cache-directive` - Use the 'use cache' Directive for Explicit Caching
- `cache-revalidate-tag` - Use revalidateTag with cacheLife Profiles
- `cache-fetch-options` - Configure Fetch Cache Options Correctly
- `cache-revalidate-path` - Use revalidatePath for Route-Level Cache Invalidation
- `cache-react-cache` - Use React cache() for Request Deduplication
- `cache-segment-config` - Configure Route Segment Caching with Exports

### 3. Server Components & Data Fetching (HIGH)

- `server-parallel-fetching` - Fetch Data in Parallel in Server Components
- `server-component-streaming` - Stream Server Components for Progressive Loading
- `server-data-colocation` - Colocate Data Fetching with Components
- `server-preload-pattern` - Use Preload Pattern for Critical Data
- `server-avoid-client-fetching` - Avoid Client-Side Data Fetching for Initial Data
- `server-error-handling` - Handle Server Component Errors Gracefully

### 4. Routing & Navigation (HIGH)

- `route-parallel-routes` - Use Parallel Routes for Independent Content
- `route-intercepting-routes` - Use Intercepting Routes for Modal Patterns
- `route-prefetching` - Configure Link Prefetching Appropriately
- `route-proxy-ts` - Use proxy.ts for Network Boundary Logic
- `route-not-found` - Use notFound() for Missing Resources

### 5. Server Actions & Mutations (MEDIUM-HIGH)

- `action-server-action-forms` - Use Server Actions for Form Submissions
- `action-pending-states` - Show Pending States with useFormStatus
- `action-error-handling` - Handle Server Action Errors Gracefully
- `action-optimistic-updates` - Use Optimistic Updates for Instant Feedback
- `action-revalidation` - Revalidate Cache After Mutations

### 6. Streaming & Loading States (MEDIUM)

- `stream-suspense-boundaries` - Place Suspense Boundaries Strategically
- `stream-loading-tsx` - Use loading.tsx for Route-Level Loading States
- `stream-error-tsx` - Use error.tsx for Route-Level Error Boundaries
- `stream-skeleton-matching` - Match Skeleton Dimensions to Actual Content
- `stream-nested-suspense` - Nest Suspense for Progressive Disclosure

### 7. Metadata & SEO (MEDIUM)

- `meta-generate-metadata` - Use generateMetadata for Dynamic Metadata
- `meta-sitemap` - Generate Sitemaps Dynamically
- `meta-robots` - Configure Robots for Crawl Control
- `meta-opengraph-images` - Generate Dynamic OpenGraph Images

### 8. Client Components (LOW-MEDIUM)

- `client-use-client-boundary` - Minimize 'use client' Boundary Scope
- `client-children-pattern` - Pass Server Components as Children to Client Components
- `client-hydration-mismatch` - Avoid Hydration Mismatches
- `client-third-party-scripts` - Load Third-Party Scripts Efficiently

## How to Use

Read individual reference files for detailed explanations and code examples:

- [Section definitions](references/_sections.md) - Category structure and impact levels
- [Rule template](assets/templates/_template.md) - Template for adding new rules
- [build-dynamic-imports](references/build-dynamic-imports.md) - Example rule file
- [cache-use-cache-directive](references/cache-use-cache-directive.md) - Example rule file

## Related Skills

- For React 19 fundamentals, see `react-19` skill
- For data fetching patterns, see `tanstack-query` skill
- For client-side forms, see `react-hook-form` skill

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
