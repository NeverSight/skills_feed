---
name: angular-ecosystem
description: Useful Angular libraries, tools, and ecosystem references for Angular development.
version: 1.0.0
tags: [angular, ecosystem]
---

# SKILL: Angular 20+ Ecosystem Master Guide

This master skill document consolidates Angular Core, v20 Control Flow, Signals, CDK, Material 3, Router, Forms, Google Maps, NgRx Signals, and RxJS Patterns into a unified architecture reference.

---

## 🏗️ 1. Core Architecture: Standalone & Zone-less

### Component Standards

- **Standalone components only**: Use `standalone: true`.
- **OnPush Change Detection**: Every component must use `changeDetection: ChangeDetectionStrategy.OnPush`.
- **Signals-first**: Use `input()`, `output()`, `model()`, `viewChild()`, and `contentChild()` (Angular 19+ syntax).
- **Control Flow**: Use `@if`, `@for (item of items; track item.id)`, `@switch`, and `@defer`. Avoid `*ngIf`, `*ngFor`.

### Dependency Injection

- Use `inject(Type)` instead of constructor injection for cleaner, more modern code.
- Provide global services/tokens in `app.config.ts`.

---

## 🚦 2. State Management: NgRx Signals

### The `signalStore` Pattern

- **Centralized State**: Define a single `signalStore` per feature module or bounded context.
- **withState**: Initialize with plain objects (use `null` instead of `undefined`).
- **withComputed**: Derived state should be pure and reactive.
- **withMethods**: Handle business logic and state transitions.

### Async Operations with `rxMethod`

- Use `rxMethod` for async side effects (API calls).
- **Concurrency Control**: Choose the right operator:
  - `switchMap`: For searches, filters (cancels previous).
  - `exhaustMap`: For form submissions (ignores concurrent clicks).
  - `concatMap`: For ordered sequential operations.
  - `mergeMap`: For independent parallel operations.
- Always use `tapResponse` from `@ngrx/operators` for structured error handling.

---

## 🧱 3. UI Component Layer: Angular Material 3 & CDK

### Material Design 3 (M3)

- **Token-based theming**: Use M3 design tokens (`--mat-sys-...`) and CSS variables.
- **Global Styles**: Defined in `styles.scss` using the modern SASS mixins.
- **Forms**: Use `<mat-form-field>` with standard validation patterns.

### Angular CDK (Component Dev Kit)

- **A11y**: Use `A11yModule`, `FocusTrap`, and `LiveAnnouncer` for accessible experiences.
- **Overlays**: Use `OverlayModule` for custom dialogs, tooltips, and floating UI.
- **Virtual Scroll**: Use `CdkVirtualScrollViewport` for large lists (>100 items).
- **Drag & Drop**: Use `@angular/cdk/drag-drop` for list reordering and board layouts.

---

## 🗺️ 4. Navigation & Mapping

### Angular Router

- **Lazy Loading**: Always use `loadChildren: () => import(...)`.
- **Functional Guards**: Replace class-based guards with functions using `inject()`.
- **Reactive Params**: Convert route parameters to signals using `toSignal(route.params)`.

### Google Maps integration

- **Lazy Loading**: Load API script dynamically via a service.
- **API Key Security**: Store keys in `environment.ts` (never hardcode).
- **Marker Clustering**: Required for >50 markers to maintain performance.

---

## 🧪 5. RxJS & Signals Interop

### The Boundary Pattern

- **Infrastructure/Ports**: Return Observables from repositories (for stream-based data).
- **Application/Facade**: Convert to Signals using `toSignal()`.
- **Cleanup**: Use `takeUntilDestroyed()` or `toSignal()` to ensure automatic unsubscription.
- **Expensive Streams**: Use `shareReplay({ bufferSize: 1, refCount: true })`.

---

## 📋 6. Form Handling: Reactive & Typed

- **Strictly Typed**: Use `FormGroup<T>`, `FormControl<T>`.
- **Validation**: Show errors only after `touched`.
- **Signals Sync**: Update the store via `onChanges` or explicit submission methods.

---

## ♿ 7. Accessibility (A11y)

- **WCAG 2.2 Level AA**: Minimum requirement.
- **Semantic HTML**: Prioritize `<nav>`, `<main>`, `<header>`, `<footer>`.
- **Keyboard Navigation**: Ensure `tabindex` and focus management are solid.
- **ARIA**: Use `aria-label`, `aria-describedby`, and `aria-live` where native HTML is insufficient.

---

> **Note**: This document is the source of truth for all Angular-related development in Black-Tortoise. Non-compliant code will be rejected by the CI pipeline.
