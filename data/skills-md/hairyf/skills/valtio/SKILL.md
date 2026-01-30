---
name: valtio
description: Valtio proxy state management for React and vanilla JavaScript. Use when creating reactive state, managing application state, or working with proxy-based state management.
metadata:
  author: Hairyf
  version: "2026.1.29"
  source: Generated from https://github.com/pmndrs/valtio, scripts located at https://github.com/antfu/skills
---

Valtio makes proxy-state simple for React and vanilla JavaScript. It provides a minimal, flexible, and unopinionated API that turns objects into self-aware proxies, enabling fine-grained subscription and reactivity. Valtio shines at render optimization in React and is compatible with Suspense and React 18+.

> The skill is based on Valtio v2.3.0, generated at 2026-01-29.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Proxy | Create reactive state objects that track changes | [core-proxy](references/core-proxy.md) |
| useSnapshot | React hook for render-optimized state access | [core-use-snapshot](references/core-use-snapshot.md) |
| Snapshot | Create immutable snapshots for comparison and Suspense | [core-snapshot](references/core-snapshot.md) |
| Subscribe | Subscribe to state changes from anywhere | [core-subscribe](references/core-subscribe.md) |

## Utils

| Topic | Description | Reference |
|-------|-------------|-----------|
| proxyMap | Observable Map-like proxy for Map data structures | [utils-proxy-map](references/utils-proxy-map.md) |
| proxySet | Observable Set-like proxy for Set data structures | [utils-proxy-set](references/utils-proxy-set.md) |
| subscribeKey | Subscribe to changes of a specific property | [utils-subscribe-key](references/utils-subscribe-key.md) |
| DevTools | Redux DevTools Extension integration | [utils-devtools](references/utils-devtools.md) |
| Ref | Create unproxied references for special objects | [utils-ref](references/utils-ref.md) |

## Guides

| Topic | Description | Reference |
|-------|-------------|-----------|
| Component State | Isolate component state using useRef | [guides-component-state](references/guides-component-state.md) |
| Computed Properties | Create computed properties with getters and setters | [guides-computed-properties](references/guides-computed-properties.md) |
| Async | Work with promises and React Suspense | [guides-async](references/guides-async.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Actions | Organize actions for mutating state | [best-practices-actions](references/best-practices-actions.md) |
| Persistence | Persist state to localStorage or other storage | [best-practices-persistence](references/best-practices-persistence.md) |
| State Composition | Split and compose states for organization | [best-practices-state-composition](references/best-practices-state-composition.md) |
