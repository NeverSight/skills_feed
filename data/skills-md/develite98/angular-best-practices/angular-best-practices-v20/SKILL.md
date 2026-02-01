---
name: angular-best-practices-v20
description: Angular 20+ performance optimization guidelines with Signals, httpResource, signal inputs/outputs, @defer, and native control flow (@if, @for). Use when writing, reviewing, or refactoring modern Angular code. Triggers on tasks involving Angular components, services, data fetching, bundle optimization, or performance improvements.
license: MIT
metadata:
  author: community
  version: "2.0.0"
---

# Angular Best Practices (v20+)

Comprehensive performance optimization guide for Angular 20+ applications with modern features like Signals, httpResource, signal inputs/outputs, @defer blocks, and native control flow syntax. Contains 35+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Angular 20+ components
- Using Signals for reactive state (signal, computed, linkedSignal, effect)
- Using httpResource/resource for data fetching
- Using signal inputs/outputs instead of decorators
- Implementing @defer for lazy loading
- Using native control flow (@if, @for, @switch)
- Implementing SSR with incremental hydration
- Reviewing code for performance issues

## Key Features (v20+)

- **Signals** - Fine-grained reactivity (signal, computed, linkedSignal, effect)
- **httpResource** - Signal-based HTTP with automatic loading states
- **Signal inputs/outputs** - input(), output() replacing decorators
- **@defer** - Template-level lazy loading with hydration triggers
- **@for / @if** - Native control flow with required track
- **Standalone by default** - No standalone: true needed
- **Host bindings** - host object instead of @HostBinding decorators
- **Functional interceptors** - Simpler HTTP interceptors
- **takeUntilDestroyed** - Built-in subscription cleanup
- **Incremental hydration** - @defer (hydrate on ...) for SSR

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Change Detection | CRITICAL | `change-` |
| 2 | Bundle & Lazy Loading | CRITICAL | `bundle-` |
| 3 | RxJS Optimization | HIGH | `rxjs-` |
| 4 | Template Performance | HIGH | `template-` |
| 5 | Dependency Injection | MEDIUM-HIGH | `di-` |
| 6 | HTTP & Caching | MEDIUM | `http-` |
| 7 | Forms Optimization | MEDIUM | `forms-` |
| 8 | General Performance | LOW-MEDIUM | `ssr-` |

## Quick Reference

### 1. Change Detection (CRITICAL)

- `change-signals` - Use Signals instead of BehaviorSubject for reactive state
- `change-onpush` - Use OnPush change detection strategy
- `change-detach-reattach` - Detach change detector for heavy operations
- `change-run-outside-zone` - Run non-UI code outside NgZone
- `component-signal-io` - Use signal inputs/outputs instead of @Input/@Output decorators
- `signal-computed-pure` - Keep computed() pure, no side effects
- `signal-effect-patterns` - Use effect() correctly, avoid anti-patterns
- `signal-linkedsignal` - Use linkedSignal for derived + writable state

### 2. Bundle & Lazy Loading (CRITICAL)

- `bundle-standalone` - Use standalone components (default in v20+)
- `bundle-lazy-routes` - Lazy load routes with loadComponent/loadChildren
- `bundle-defer` - Use @defer blocks for heavy components
- `bundle-preload` - Preload routes on hover/focus for perceived speed
- `bundle-no-barrel-imports` - Avoid barrel files, use direct imports

### 3. RxJS Optimization (HIGH)

- `rxjs-async-pipe` - Use async pipe instead of manual subscriptions
- `rxjs-takeuntil` - Use takeUntilDestroyed for automatic cleanup
- `rxjs-share-replay` - Share observables to avoid duplicate requests
- `rxjs-operators` - Use efficient RxJS operators
- `rxjs-mapping-operators` - Use correct mapping operators (switchMap vs exhaustMap)
- `rxjs-no-nested-subscribe` - Avoid nested subscriptions

### 4. Template Performance (HIGH)

- `template-trackby` - Use track function in @for loops (required in v20+)
- `template-pure-pipes` - Use pure pipes for expensive transformations
- `template-ng-optimized-image` - Use NgOptimizedImage for image optimization
- `template-no-function-calls` - Avoid function calls in templates
- `template-virtual-scroll` - Use virtual scrolling for large lists

### 5. Dependency Injection (MEDIUM-HIGH)

- `di-provided-in-root` - Use providedIn: 'root' for singleton services
- `di-injection-token` - Use InjectionToken for non-class dependencies
- `di-factory-providers` - Use factory providers for complex initialization
- `directive-host-composition` - Use hostDirectives for composition

### 6. HTTP & Caching (MEDIUM)

- `http-resource` - Use httpResource/resource for signal-based data fetching
- `http-interceptors` - Use functional interceptors for cross-cutting concerns
- `http-transfer-state` - Use TransferState for SSR hydration
- `routing-signal-inputs` - Use signal-based route inputs

### 7. Forms Optimization (MEDIUM)

- `forms-reactive` - Use reactive forms with typed FormGroup

### 8. General Performance (LOW-MEDIUM)

- `ssr-hydration` - Use incremental hydration with @defer (hydrate on ...)
- `perf-memory-leaks` - Prevent memory leaks (timers, listeners, subscriptions)
- `perf-web-workers` - Offload heavy computation to Web Workers
- `arch-smart-dumb-components` - Use Smart/Dumb component pattern

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/change-signals.md
rules/bundle-defer.md
rules/http-resource.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
