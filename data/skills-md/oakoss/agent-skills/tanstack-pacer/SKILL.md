---
name: tanstack-pacer
description: 'TanStack Pacer for rate limiting, throttling, debouncing, and async queuing. Use when controlling execution frequency, managing API rate limits, debouncing user input, or queuing async tasks. Use for pacer, throttle, debounce, rate-limit, queue, async-throttle, rate-limiting.'
license: MIT
metadata:
  author: oakoss
  version: '1.1'
  source: 'https://tanstack.com/pacer/latest'
---

# TanStack Pacer

## Overview

TanStack Pacer is a lightweight, type-safe library for controlling function execution timing through debouncing, throttling, rate limiting, queuing, and batching. It provides framework-agnostic core classes with dedicated React hooks at multiple abstraction levels (instance, callback, state, value).

**When to use:** Debouncing search input, throttling scroll/resize handlers, enforcing API rate limits, queuing async tasks with concurrency control, batching multiple operations into single requests.

**When NOT to use:** Simple one-off delays (use `setTimeout`), server-side rate limiting at the infrastructure level (use middleware/API gateway), complex job scheduling (use a task queue like BullMQ).

## Quick Reference

| Pattern           | API                                         | Key Points                                                 |
| ----------------- | ------------------------------------------- | ---------------------------------------------------------- |
| Debounce function | `Debouncer` / `debounce(fn, opts)`          | Waits for inactivity; no `maxWait` option by design        |
| Throttle function | `Throttler` / `throttle(fn, opts)`          | Even spacing; `leading` and `trailing` both default `true` |
| Rate limit        | `RateLimiter` / `rateLimit(fn, opts)`       | Fixed or sliding window; rejects calls over limit          |
| Queue items       | `Queuer` / `queue(fn, opts)`                | FIFO default; supports LIFO, priority, expiration          |
| Async queue       | `AsyncQueuer` / `asyncQueue(fn, opts)`      | Concurrency control, retry, error callbacks                |
| Async batch       | `AsyncBatcher` / `asyncBatch(fn, opts)`     | Collects items, processes as batch after wait/maxSize      |
| React debounce    | `useDebouncer` / `useDebouncedCallback`     | Instance hook vs simple callback hook                      |
| React throttle    | `useThrottler` / `useThrottledCallback`     | Instance hook vs simple callback hook                      |
| React rate limit  | `useRateLimiter` / `useRateLimitedCallback` | Instance hook vs simple callback hook                      |
| React queue       | `useQueuer` / `useQueuedState`              | Instance hook vs state-integrated hook                     |
| React async queue | `useAsyncQueuer` / `useAsyncQueuedState`    | Concurrency + state management                             |
| React batch       | `useBatcher` / `useAsyncBatcher`            | Sync and async batching hooks                              |
| State hooks       | `useDebouncedState`, `useThrottledState`    | Integrate with React state directly                        |
| Value hooks       | `useDebouncedValue`, `useThrottledValue`    | Create derived debounced/throttled values                  |

## Common Mistakes

| Mistake                                 | Correct Pattern                                                              |
| --------------------------------------- | ---------------------------------------------------------------------------- |
| Using `maxWait` on Debouncer            | Debouncer has no `maxWait`; use Throttler for evenly spaced execution        |
| Creating instances inside render        | Create with hooks (`useDebouncer`, `useThrottler`) to manage lifecycle       |
| Ignoring `maybeExecute` return          | Rate limiter and throttler may reject calls; check state or use callbacks    |
| Using debounce when throttle is needed  | Debounce waits for pause; throttle guarantees max-once-per-interval          |
| Not cleaning up on unmount              | React hooks handle cleanup automatically; manual instances need `cancel()`   |
| Using Queuer when items can be dropped  | Queuers process every item; use throttle/debounce if dropping is acceptable  |
| Fixed window when sliding is needed     | Fixed windows allow bursts at boundaries; sliding window gives smoother rate |
| Forgetting `onReject` on RateLimiter    | Rejected calls are silent by default; add `onReject` for user feedback       |
| Not passing `enabled: false` to disable | All utilities support `enabled` option to temporarily disable processing     |

## Delegation

> If the `tanstack-query` skill is available, delegate data fetching and cache management tasks to it. TanStack Pacer complements Query for controlling request frequency.
> Otherwise, recommend: `npx skills add oakoss/agent-skills --skill tanstack-query`

- **Execution timing patterns**: Use this skill
- **Data fetching and caching**: Delegate to `tanstack-query`
- **Component architecture**: Delegate to framework-specific skills

## References

- [Throttle and debounce patterns](references/throttle-debounce.md)
- [Rate limiting patterns](references/rate-limiting.md)
- [Queuing and async queuing](references/queuing.md)
- [React hooks and integration](references/react-integration.md)
