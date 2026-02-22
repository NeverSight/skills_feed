---
name: nuqs
description: >
  Type-safe URL query state management with nuqs 2.x. Use when writing or
  reviewing code that uses useQueryState, useQueryStates, URL search params,
  query parameters, nuqs parsers, createLoader, createSearchParamsCache,
  createSerializer, or URL state in Next.js, React, Remix, React Router,
  or TanStack Router.
---

# nuqs Best Practices

Type-safe URL query state management with nuqs 2.x. Contains rules across 8 categories, prioritized by impact.

## Rule Categories

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Parser Configuration | CRITICAL | `parser-` |
| 2 | Adapter & Setup | CRITICAL | `setup-` |
| 3 | State Management | HIGH | `state-` |
| 4 | Server Integration | HIGH | `server-` |
| 5 | Performance | MEDIUM | `perf-` |
| 6 | History & Navigation | MEDIUM | `history-` |
| 7 | Debugging & Testing | LOW-MEDIUM | `debug-` |
| 8 | Advanced Patterns | LOW | `advanced-` |

## Quick Reference

### 1. Parser Configuration (CRITICAL)

- [`parser-typed`](references/parser-typed.md) — Use typed parsers for non-string values
- [`parser-with-default`](references/parser-with-default.md) — Use withDefault for non-nullable state
- [`parser-enum-literals`](references/parser-enum-literals.md) — Use literal/enum parsers for constrained values
- [`parser-array-format`](references/parser-array-format.md) — Choose correct array parser format
- [`parser-json-validation`](references/parser-json-validation.md) — Validate JSON parser with Standard Schema
- [`parser-date-format`](references/parser-date-format.md) — Select appropriate date parser
- [`parser-index-offset`](references/parser-index-offset.md) — Use parseAsIndex for 1-based URL display
- [`parser-hex-colors`](references/parser-hex-colors.md) — Use parseAsHex for color values
- [`parser-custom`](references/parser-custom.md) — Create custom parsers for complex types

### 2. Adapter & Setup (CRITICAL)

- [`setup-adapter`](references/setup-adapter.md) — Wrap app with correct NuqsAdapter
- [`setup-client-hooks`](references/setup-client-hooks.md) — Add 'use client' for hooks
- [`setup-server-imports`](references/setup-server-imports.md) — Import server utilities from nuqs/server
- [`setup-shared-parsers`](references/setup-shared-parsers.md) — Define shared parsers in a dedicated file

### 3. State Management (HIGH)

- [`state-use-query-states`](references/state-use-query-states.md) — Use useQueryStates for related parameters
- [`state-functional-updates`](references/state-functional-updates.md) — Use functional updates for derived state
- [`state-clear-with-null`](references/state-clear-with-null.md) — Clear URL parameters with null
- [`state-controlled-inputs`](references/state-controlled-inputs.md) — Handle controlled input value properly
- [`state-avoid-derived`](references/state-avoid-derived.md) — Avoid derived state from URL parameters
- [`state-options-inheritance`](references/state-options-inheritance.md) — Use withOptions for parser-level config
- [`state-setter-return`](references/state-setter-return.md) — Use setter return value for URL access

### 4. Server Integration (HIGH)

- [`server-create-loader`](references/server-create-loader.md) — Use createLoader for page-level server parsing
- [`server-search-params-cache`](references/server-search-params-cache.md) — Use createSearchParamsCache for nested RSC access
- [`server-shallow-false`](references/server-shallow-false.md) — Use shallow:false to trigger server re-renders
- [`server-use-transition`](references/server-use-transition.md) — Integrate useTransition for loading states
- [`server-share-parsers`](references/server-share-parsers.md) — Share parsers between client and server
- [`server-next15-async`](references/server-next15-async.md) — Handle async searchParams in Next.js 15+

### 5. Performance (MEDIUM)

- [`perf-limit-url-updates`](references/perf-limit-url-updates.md) — Throttle/debounce URL updates
- [`perf-clear-on-default`](references/perf-clear-on-default.md) — Use clearOnDefault for clean URLs
- [`perf-avoid-rerender`](references/perf-avoid-rerender.md) — Memoize components using URL state
- [`perf-serialize-utility`](references/perf-serialize-utility.md) — Use createSerializer for link URLs

### 6. History & Navigation (MEDIUM)

- [`history-push-navigation`](references/history-push-navigation.md) — Use history:push for navigation-like state
- [`history-replace-ephemeral`](references/history-replace-ephemeral.md) — Use history:replace for ephemeral state
- [`history-scroll-behavior`](references/history-scroll-behavior.md) — Control scroll behavior on URL changes
- [`history-back-sync`](references/history-back-sync.md) — Handle browser back/forward navigation

### 7. Debugging & Testing (LOW-MEDIUM)

- [`debug-enable-logging`](references/debug-enable-logging.md) — Enable debug logging for troubleshooting
- [`debug-common-errors`](references/debug-common-errors.md) — Diagnose common nuqs errors
- [`debug-testing`](references/debug-testing.md) — Test components and hooks with URL state

### 8. Advanced Patterns (LOW)

- [`advanced-url-keys`](references/advanced-url-keys.md) — Use urlKeys for shorter URL param names
- [`advanced-eq-function`](references/advanced-eq-function.md) — Implement eq function for object parsers
- [`advanced-adapter-props`](references/advanced-adapter-props.md) — Configure NuqsAdapter global defaults and URL middleware
- [`advanced-standard-schema`](references/advanced-standard-schema.md) — Use createStandardSchemaV1 and inferParserType
- [`advanced-optimistic-search-params`](references/advanced-optimistic-search-params.md) — useOptimisticSearchParams for Remix/React Router
