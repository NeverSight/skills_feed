---
name: angular-best-practices-legacy
description: Angular 12-16 performance optimization guidelines with NgModules, RxJS patterns, and classic template syntax (*ngIf, *ngFor). Use when maintaining or working with pre-v17 Angular codebases. Triggers on tasks involving Angular components, services, modules, or performance improvements in legacy projects.
license: MIT
metadata:
  author: community
  version: "1.0.0"
---

# Angular Best Practices (Legacy: v12-16)

Comprehensive performance optimization guide for Angular 12-16 applications using NgModule-based architecture and RxJS-centric patterns. Contains 30+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Maintaining Angular 12-16 codebases
- Using NgModule-based architecture
- Working with *ngIf, *ngFor directives
- Using RxJS for state management
- Using class-based HTTP interceptors
- Reviewing code for performance issues

## Key Patterns (v12-16)

- **NgModules** - Feature modules for organization
- **BehaviorSubject** - Reactive state management
- **Subject + takeUntil** - Subscription cleanup pattern
- **Class-based interceptors** - HTTP handling with implements HttpInterceptor
- ***ngFor / *ngIf** - Structural directives with trackBy
- **loadChildren** - Module-based lazy loading

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
| 8 | General Performance | LOW-MEDIUM | `perf-` |

## Quick Reference

### 1. Change Detection (CRITICAL)

- `change-rxjs-state` - Use BehaviorSubject with OnPush for reactive state
- `change-onpush` - Use OnPush change detection strategy
- `change-detach-reattach` - Detach change detector for heavy operations
- `change-run-outside-zone` - Run non-UI code outside NgZone

### 2. Bundle & Lazy Loading (CRITICAL)

- `bundle-ngmodule` - Organize code into feature NgModules
- `bundle-scam` - Use Single Component Angular Modules pattern
- `bundle-lazy-routes` - Lazy load routes with loadChildren
- `bundle-preload` - Preload routes for perceived speed
- `bundle-no-barrel-imports` - Avoid barrel files, use direct imports

### 3. RxJS Optimization (HIGH)

- `rxjs-async-pipe` - Use async pipe instead of manual subscriptions
- `rxjs-takeuntil` - Use takeUntil with destroy$ Subject for cleanup
- `rxjs-share-replay` - Share observables to avoid duplicate requests
- `rxjs-operators` - Use efficient RxJS operators
- `rxjs-mapping-operators` - Use correct mapping operators (switchMap vs exhaustMap)
- `rxjs-no-nested-subscribe` - Avoid nested subscriptions

### 4. Template Performance (HIGH)

- `template-trackby` - Use trackBy function with *ngFor
- `template-pure-pipes` - Use pure pipes for expensive transformations
- `template-ng-optimized-image` - Use NgOptimizedImage for image optimization
- `template-no-function-calls` - Avoid function calls in templates
- `template-virtual-scroll` - Use virtual scrolling for large lists

### 5. Dependency Injection (MEDIUM-HIGH)

- `di-provided-in-root` - Use providedIn: 'root' for singleton services
- `di-injection-token` - Use InjectionToken for non-class dependencies
- `di-factory-providers` - Use factory providers for complex initialization

### 6. HTTP & Caching (MEDIUM)

- `http-interceptors` - Use class-based interceptors for cross-cutting concerns
- `http-transfer-state` - Use TransferState for SSR hydration

### 7. Forms Optimization (MEDIUM)

- `forms-reactive` - Use reactive forms instead of template-driven
- `forms-typed` - Use typed FormGroup for type safety

### 8. General Performance (LOW-MEDIUM)

- `perf-memory-leaks` - Prevent memory leaks (timers, listeners, subscriptions)
- `perf-web-workers` - Offload heavy computation to Web Workers
- `arch-smart-dumb-components` - Use Smart/Dumb component pattern

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/change-rxjs-state.md
rules/bundle-ngmodule.md
rules/rxjs-takeuntil.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
