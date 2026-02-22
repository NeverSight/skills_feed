---
name: angular-best-practices
description: |
  Angular performance optimization and best practices guidelines for change detection,
  bundle optimization, templates, RxJS, and component architecture. Use when writing,
  reviewing, or refactoring Angular code, designing component hierarchies, optimizing
  performance, or implementing reactive patterns.

license: MIT
metadata:
  author: angular-agent-kit
  version: "1.0.0"
---

# Angular Best Practices

Comprehensive performance optimization guide for Angular applications, containing 45+ rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:
- Writing new Angular components or services
- Implementing change detection strategies
- Reviewing code for performance issues
- Refactoring existing Angular code
- Optimizing bundle size or load times
- Working with RxJS observables and state management
- Implementing forms and validation
- Writing unit and integration tests

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Change Detection | CRITICAL | `cd-` |
| 2 | Bundle Size Optimization | CRITICAL | `bundle-` |
| 3 | Template Performance | HIGH | `template-` |
| 4 | RxJS & Async Operations | HIGH | `rxjs-` |
| 5 | Component Architecture | MEDIUM-HIGH | `component-` |
| 6 | HTTP & Data Fetching | MEDIUM | `http-` |
| 7 | Forms & Validation | MEDIUM | `forms-` |
| 8 | Testing & Debugging | LOW-MEDIUM | `testing-` |

## Quick Reference

### 1. Change Detection (CRITICAL)

- `cd-onpush` - Use OnPush change detection strategy
- `cd-trackby` - Always use trackBy in *ngFor
- `cd-pure-pipes` - Prefer pure pipes over methods in templates
- `cd-immutable-data` - Use immutable data patterns
- `cd-detach-reattach` - Detach change detection for heavy computations
- `cd-run-outside-angular` - Run non-UI code outside NgZone

### 2. Bundle Size Optimization (CRITICAL)

- `bundle-lazy-loading` - Lazy load feature modules
- `bundle-tree-shaking` - Ensure tree-shakeable providers
- `bundle-standalone-components` - Use standalone components
- `bundle-defer-views` - Use @defer for heavy components
- `bundle-preload-strategies` - Implement smart preloading
- `bundle-avoid-barrel-exports` - Import directly, avoid barrel files

### 3. Template Performance (HIGH)

- `template-avoid-function-calls` - Avoid function calls in templates
- `template-async-pipe` - Use async pipe instead of manual subscriptions
- `template-ng-container` - Use ng-container for structural directives
- `template-control-flow` - Use new control flow syntax (@if, @for)
- `template-optimize-ngif-ngfor` - Never use *ngIf and *ngFor on same element
- `template-image-optimization` - Use NgOptimizedImage directive

### 4. RxJS & Async Operations (HIGH)

- `rxjs-avoid-nested-subscriptions` - Never nest subscriptions
- `rxjs-unsubscribe` - Always unsubscribe (takeUntilDestroyed, DestroyRef)
- `rxjs-share-replay` - Use shareReplay for HTTP caching
- `rxjs-switchmap-vs-mergemap` - Choose correct flattening operator
- `rxjs-signals-vs-observables` - Prefer signals for synchronous state
- `rxjs-debounce-throttle` - Debounce user input events

### 5. Component Architecture (MEDIUM-HIGH)

- `component-smart-presentational` - Separate smart and presentational components
- `component-input-transforms` - Use input transforms for data conversion
- `component-output-naming` - Follow output naming conventions
- `component-content-projection` - Use content projection effectively
- `component-dynamic-components` - Load components dynamically when needed
- `component-host-directives` - Compose behavior with host directives

### 6. HTTP & Data Fetching (MEDIUM)

- `http-interceptors` - Use interceptors for cross-cutting concerns
- `http-caching` - Implement HTTP caching strategies
- `http-retry-logic` - Add retry logic for resilience
- `http-cancel-requests` - Cancel pending requests on navigation
- `http-typed-responses` - Always type HTTP responses
- `http-error-handling` - Implement centralized error handling

### 7. Forms & Validation (MEDIUM)

- `forms-reactive-over-template` - Prefer reactive forms for complex forms
- `forms-typed-forms` - Use strictly typed reactive forms
- `forms-custom-validators` - Create reusable custom validators
- `forms-async-validation` - Debounce async validators
- `forms-control-value-accessor` - Implement ControlValueAccessor correctly
- `forms-form-arrays` - Handle dynamic form arrays efficiently

### 8. Testing & Debugging (LOW-MEDIUM)

- `testing-component-harness` - Use component harnesses
- `testing-mock-services` - Mock services properly
- `testing-async-testing` - Use fakeAsync/tick for async tests
- `testing-change-detection` - Trigger change detection in tests
- `testing-marble-testing` - Use marble testing for RxJS
- `testing-performance-profiling` - Profile with Angular DevTools

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/cd-onpush.md
rules/bundle-lazy-loading.md
rules/_sections.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
