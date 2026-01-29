---
name: nuxt-best-practices
description: Nuxt 3/4 performance optimization and architecture guidelines for building fast, maintainable full-stack applications. This skill should be used when writing, reviewing, or refactoring Nuxt code to ensure optimal patterns. Triggers on tasks involving data fetching, server routes, auto-imports, rendering modes, or Nuxt-specific features.
license: MIT
metadata:
  author: vinayakkulkarni
  version: "1.0.0"
---

# Nuxt Best Practices

Comprehensive performance optimization guide for Nuxt 3/4 applications. Contains 40+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Nuxt pages, components, or composables
- Implementing data fetching (useFetch, useAsyncData)
- Creating server routes and API endpoints
- Organizing types, composables, and auto-imports
- Working with Nuxt modules and plugins
- Configuring rendering modes (SSR, SSG, SPA)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Data Fetching | CRITICAL | `data-` |
| 2 | Auto-Imports & Organization | CRITICAL | `imports-` |
| 3 | Server & API Routes | HIGH | `server-` |
| 4 | Rendering Modes | HIGH | `rendering-` |
| 5 | State Management | MEDIUM-HIGH | `state-` |
| 6 | Type Safety | MEDIUM | `types-` |
| 7 | Modules & Plugins | LOW-MEDIUM | `modules-` |
| 8 | Performance & Deployment | LOW | `perf-` |

## Quick Reference

### 1. Data Fetching (CRITICAL)

- `data-use-fetch` - Use useFetch/useAsyncData, never raw fetch in components
- `data-key-unique` - Always provide unique keys for data fetching
- `data-lazy-loading` - Use lazy option for non-critical data
- `data-transform` - Transform data at fetch time, not in template
- `data-error-handling` - Always handle error and pending states
- `data-refresh-patterns` - Use refresh() and clear() appropriately

### 2. Auto-Imports & Organization (CRITICAL)

- `imports-no-barrel-autoimport` - Never create barrel exports in auto-imported directories
- `imports-component-naming` - Don't duplicate folder prefix in component names
- `imports-type-locations` - Place types in dedicated directories (app/types, shared/types, server/types)
- `imports-composable-exports` - Composables export functions only, not types
- `imports-direct-composable-imports` - Use direct imports between composables

### 3. Server & API Routes (HIGH)

- `server-validated-input` - Use getValidatedQuery/readValidatedBody with Zod
- `server-route-meta` - Always add defineRouteMeta for OpenAPI docs
- `server-runtime-config` - Use useRuntimeConfig, never process.env
- `server-error-handling` - Use createError for consistent error responses
- `server-middleware-order` - Understand middleware execution order

### 4. Rendering Modes (HIGH)

- `rendering-route-rules` - Configure rendering per-route with routeRules
- `rendering-hybrid` - Use hybrid rendering for optimal performance
- `rendering-prerender` - Prerender static pages at build time
- `rendering-client-only` - Use ClientOnly for browser-specific components

### 5. State Management (MEDIUM-HIGH)

- `state-use-state` - Use useState for SSR-safe shared state
- `state-pinia-setup` - Set up Pinia correctly with Nuxt
- `state-hydration` - Handle hydration mismatches properly
- `state-computed-over-watch` - Prefer computed over watch for derived state

### 6. Type Safety (MEDIUM)

- `types-no-inline` - Never define types inline in components/composables
- `types-import-paths` - Use correct import paths (#shared, ~/, ~~/)
- `types-no-any` - Never use `any` type
- `types-zod-schemas` - Use Zod for runtime validation with type inference
- `types-strict-emits` - Use kebab-case emits with full type definitions

### 7. Modules & Plugins (LOW-MEDIUM)

- `modules-order` - Module order matters in nuxt.config
- `modules-runtime-vs-build` - Understand runtime vs build-time modules
- `plugins-client-server` - Use .client.ts and .server.ts suffixes correctly
- `plugins-provide-inject` - Use provide/inject for cross-cutting concerns

### 8. Performance & Deployment (LOW)

- `perf-bundle-analysis` - Analyze and optimize bundle size
- `perf-image-optimization` - Use nuxt/image for optimized images
- `perf-font-loading` - Configure font loading strategy
- `perf-caching-headers` - Set appropriate cache headers

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/data-use-fetch.md
rules/imports-no-barrel-autoimport.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and Nuxt-specific notes

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
