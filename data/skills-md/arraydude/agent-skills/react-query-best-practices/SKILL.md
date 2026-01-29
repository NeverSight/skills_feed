---
name: react-query-best-practices
description: React Query v4 (TanStack Query) best practices, patterns, and troubleshooting. Use when working with useQuery, useMutation, query invalidation, caching, WebSocket integration, or any async state management in React. Based on TkDodo's comprehensive blog series.
license: MIT
metadata:
  author: arraydude
  version: "1.0.0"
  reactQueryVersion: "4.x"
---

# React Query Best Practices

> **Important:** This guide targets **React Query v4**. Some patterns may differ in v5.

Comprehensive guide for React Query v4 (TanStack Query) based on TkDodo's authoritative blog series. Contains 24 rules across 7 categories, prioritized by impact.

## When to Apply

Reference these guidelines when:
- Implementing new queries or mutations
- Integrating WebSockets with React Query
- Setting up query invalidation patterns
- Debugging React Query behavior
- Optimizing render performance
- TypeScript integration questions

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Query Keys & Patterns | CRITICAL | `query-` |
| 2 | Mutations & Updates | CRITICAL | `mutation-` |
| 3 | Caching Strategy | HIGH | `cache-` |
| 4 | WebSocket Integration | HIGH | `websocket-` |
| 5 | TypeScript Integration | MEDIUM | `typescript-` |
| 6 | Testing Patterns | MEDIUM | `testing-` |
| 7 | Common Pitfalls | MEDIUM | `troubleshoot-` |
| 8 | Migration to v5 | HIGH | `migration-` |

## Quick Reference

### 1. Query Keys & Patterns (CRITICAL)

- `query-keys-as-dependencies` - Include all queryFn params in queryKey
- `query-key-factory` - Use factory pattern for consistent key generation
- `query-select-transforms` - Use select option for data transformations
- `query-status-check-order` - Check data first, then error, then loading
- `query-tracked-properties` - Only destructure properties you use
- `query-placeholder-vs-initial` - Know when to use each approach
- `query-dependent-enabled` - Use enabled option for dependent queries

### 2. Mutations & Updates (CRITICAL)

- `mutation-prefer-mutate` - Use mutate() with callbacks over mutateAsync()
- `mutation-invalidation` - Invalidate queries after mutations
- `mutation-direct-cache-update` - Update cache directly when appropriate
- `mutation-optimistic-updates` - Show success immediately, rollback on failure
- `mutation-callback-separation` - Query logic in hook, UI effects in component

### 3. Caching Strategy (HIGH)

- `cache-stale-time` - Set appropriate staleTime for your domain
- `cache-refetch-triggers` - Keep refetch triggers enabled in production

### 4. WebSocket Integration (HIGH)

- `websocket-event-invalidation` - Use events to trigger invalidation
- `websocket-stale-time-infinity` - Set staleTime: Infinity for WS-managed data
- `websocket-reconnection` - Invalidate stale queries on reconnect

### 5. TypeScript Integration (MEDIUM)

- `typescript-infer-dont-specify` - Let TypeScript infer, type the queryFn
- `typescript-zod-validation` - Use Zod for runtime validation

### 6. Testing Patterns (MEDIUM)

- `testing-fresh-client` - Create fresh QueryClient per test
- `testing-msw-mocking` - Use MSW for network mocking

### 7. Common Pitfalls (MEDIUM)

- `troubleshoot-copy-to-state` - Never copy query data to local state
- `troubleshoot-missing-key-deps` - Include all dependencies in query key
- `troubleshoot-fetch-not-reject` - Handle HTTP errors with fetch

### 8. Migration to v5 (HIGH)

- `migration-cache-time-to-gc-time` - cacheTime renamed to gcTime
- `migration-query-callbacks-removed` - onSuccess/onError/onSettled removed from useQuery
- `migration-suspense-hooks` - New useSuspenseQuery, useSuspenseInfiniteQuery hooks

## Core Mental Model

1. **React Query is NOT a data fetching library** - it's an async state manager
2. **Server state != Client state** - never mix them in global state managers
3. **Stale-while-revalidate** - show cached data immediately, fetch in background
4. **Query keys are dependencies** - include all variables used in queryFn

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/query-key-factory.md
rules/mutation-invalidation.md
rules/websocket-event-invalidation.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example
- Correct code example

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
