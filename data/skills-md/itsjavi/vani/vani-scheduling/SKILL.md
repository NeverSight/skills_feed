---
name: vani-scheduling
description: Schedule explicit updates with microtasks and transitions
---

# Scheduling Updates

Instructions for batching updates across independent regions with predictable timing.

## When to Use

Use this when a UI has multiple regions that should update independently or when updates are
expensive.

## Steps

1. Assign each UI region its own `Handle`.
2. Use `batch()` to coalesce update scheduling in the same tick.
3. Create a scheduler that batches updates with `queueMicrotask`.
4. Use `startTransition()` for non-urgent work to keep the UI responsive.
5. Deduplicate updates per region within a single flush.

## Arguments

- regionIds - list of region identifiers (defaults to `['content']`)
- enableTransitions - whether to include a transition path (defaults to `true`)
- schedulerName - exported scheduler name (defaults to `scheduleRegionUpdate`)

## Examples

Example 1 usage pattern:

Batch urgent updates in a microtask and update each region once per flush.

Example 2 usage pattern:

Defer expensive list filtering with `startTransition()`.

## Output

Example output:

```
Created: src/scheduler.ts
Notes: Updates are deduplicated per region.
```

## Present Results to User

Explain the scheduling policy, which updates are urgent vs transition, and list changes.
