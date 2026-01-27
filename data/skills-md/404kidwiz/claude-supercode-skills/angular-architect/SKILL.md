---
name: angular-architect
description: Enterprise Angular development expert specializing in Angular 16+ features, Signals, Standalone Components, and RxJS/NgRx at scale.
---

# Angular Architect

## Purpose

Provides enterprise Angular development expertise specializing in Angular 16+ features (Signals, Standalone Components), RxJS reactive programming, and NgRx state management at scale. Designs large-scale Angular applications with performance optimization and modern architectural patterns.

## When to Use

- Architecting a large-scale Angular application (Monorepo, Micro-frontends)
- Implementing Signals for fine-grained reactivity (Angular 16+)
- Migrating legacy Modules (NgModule) to Standalone Components
- Designing complex state management with NgRx or NgRx Signal Store
- Optimizing performance (Zoneless, OnPush, Hydration)
- Setting up enterprise CI/CD with Nx or Turborepo

---
---

## 2. Decision Framework

### State Management Strategy

```
What is the complexity level?
│
├─ **Local State (Component)**
│  ├─ Simple? → **Signals (`signal`, `computed`)**
│  └─ Complex streams? → **RxJS (`BehaviorSubject`)**
│
├─ **Global Shared State**
│  ├─ Lightweight? → **NgRx Signal Store** (Modern, functional)
│  ├─ Enterprise/Complex? → **NgRx Store (Redux)** (Strict actions/reducers)
│  └─ Entity Collections? → **NgRx Entity**
│
└─ **Server State**
   └─ Caching/Deduplication? → **TanStack Query (Angular)** or **RxJS + Cache Operator**
```

### Architecture Patterns

| Pattern | Use Case | Pros | Cons |
|---------|----------|------|------|
| **Standalone** | Default for 15+ | Less boilerplate, tree-shakable | Learning curve for legacy devs |
| **Nx Monorepo** | Multi-app enterprise | Shared libs, affected builds | Tooling complexity |
| **Micro-Frontends** | Different teams/stacks | Independent deployment | Runtime complexity, shared deps hell |
| **Zoneless** | High performance | No Zone.js overhead | Requires explicit Change Detection |

**Red Flags → Escalate to `performance-engineer`:**
- "ExpressionChangedAfterItHasBeenCheckedError" appearing frequently
- Bundle size > 5MB initial load
- Change detection cycles running constantly (Zone.js thrashing)
- Memory leaks in RxJS subscriptions (forgotten `takeUntilDestroyed`)

---
---

### Workflow 2: NgRx Signal Store (Modern State)

**Goal:** Manage feature state with less boilerplate than Redux.

**Steps:**

1.  **Define Store**
    ```typescript
    import { signalStore, withState, withMethods, patchState } from '@ngrx/signals';
    
    export const UserStore = signalStore(
      { providedIn: 'root' },
      withState({ users: [], loading: false, query: '' }),
      withMethods((store) => ({
        setQuery(query: string) {
          patchState(store, { query });
        },
        async loadUsers() {
          patchState(store, { loading: true });
          const users = await fetchUsers(store.query());
          patchState(store, { users, loading: false });
        }
      }))
    );
    ```

2.  **Use in Component**
    ```typescript
    export class UserListComponent {
      readonly store = inject(UserStore);
      
      constructor() {
        // Auto-load when query changes (Effect)
        effect(() => {
          this.store.loadUsers();
        });
      }
    }
    ```

---
---

### Workflow 4: Zoneless Applications (Angular 18+)

**Goal:** Remove Zone.js for smaller bundles and better debugging.

**Steps:**

1.  **Bootstrap Config**
    ```typescript
    // main.ts
    bootstrapApplication(AppComponent, {
      providers: [
        provideExperimentalZonelessChangeDetection()
      ]
    });
    ```

2.  **State Management (Signals Only)**
    -   Do NOT use `ApplicationRef.tick()` manually.
    -   Use `signal()` for all state.
    -   Events automatically trigger change detection.

3.  **Integrations**
    -   **RxJS:** Use `AsyncPipe` (still works) or `toSignal`.
    -   **Timers:** `setInterval` does NOT trigger CD automatically. Use `signal` updates inside the timer.

---
---

## Core Capabilities

### Enterprise Angular Architecture
- Designs large-scale Angular application architectures
- Implements modular design patterns (Nx monorepos, micro-frontends)
- Establishes coding standards and best practices for teams
- Creates scalable folder structures and module organization

### Modern Angular Development
- Implements Signals for fine-grained reactivity (Angular 16+)
- Migrates legacy NgModule-based code to Standalone Components
- Optimizes Change Detection with OnPush and Zoneless strategies
- Leverages new Angular features (deferrable views, hydration)

### State Management
- Designs NgRx Store architectures for enterprise applications
- Implements NgRx Signal Store for lightweight state management
- Creates custom state management solutions for complex requirements
- Integrates server state with TanStack Query or RxJS patterns

### Performance Engineering
- Optimizes bundle size with tree-shaking and lazy loading
- Implements code splitting and differential loading
- Creates performance monitoring and metrics collection
- Develops optimization strategies for large Angular applications

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Nested Subscriptions ("Callback Hell")

**What it looks like:**
```typescript
this.route.params.subscribe(params => {
  this.service.getData(params.id).subscribe(data => {
    this.data = data; // Manual assignment
  });
});
```

**Why it fails:**
-   Race conditions (if params change fast).
-   Memory leaks (if not unsubscribed).

**Correct approach:**
-   **SwitchMap:**
    ```typescript
    this.data$ = this.route.params.pipe(
      switchMap(params => this.service.getData(params.id))
    );
    ```
-   Use `AsyncPipe` or `toSignal` in template.

### ❌ Anti-Pattern 2: Logic in Templates

**What it looks like:**
```html
<div *ngIf="user.roles.includes('ADMIN') && user.active && !isLoading">
```

**Why it fails:**
-   Hard to test.
-   Runs on every change detection cycle.

**Correct approach:**
-   **Computed Signal / Getter:**
    ```typescript
    isAdmin = computed(() => this.user().roles.includes('ADMIN'));
    ```
    ```html
    <div *ngIf="isAdmin()">
    ```

### ❌ Anti-Pattern 3: Shared Module Bloat

**What it looks like:**
-   One massive `SharedModule` importing everything (Material, Utils, Components).

**Why it fails:**
-   Breaks tree-shaking.
-   Increases initial bundle size.

**Correct approach:**
-   **Standalone Components:** Import exactly what you need in the component's `imports: []` array.

---
---

## 7. Quality Checklist

**Architecture:**
-   [ ] **Standalone:** No `NgModules` for new features.
-   [ ] **Lazy Loading:** All feature routes are lazy loaded (`loadComponent`).
-   [ ] **State:** Local state uses Signals, Shared state uses Store.

**Performance:**
-   [ ] **Change Detection:** `OnPush` enabled everywhere.
-   [ ] **Bundle:** Initial bundle < 200KB.
-   [ ] **Defer:** `@defer` used for heavy components below the fold.

**Code Quality:**
-   [ ] **Strict Mode:** `strict: true` in tsconfig.
-   [ ] **No Subscriptions:** `AsyncPipe` or `toSignal` used instead of `.subscribe()`.
-   [ ] **Security:** Inputs verified, no `innerHTML` without sanitization.

## Examples

### Example 1: Enterprise E-Commerce Platform Architecture

**Scenario:** A retail company needs to architect a large-scale e-commerce platform handling 100K+ concurrent users, with separate modules for catalog, cart, checkout, and user management.

**Architecture Decisions:**
1. **Nx Monorepo Structure**: Split into apps (storefront, admin, api) and shared libraries (ui, utilities, data-access)
2. **State Management**: NgRx Signal Store for cart/user state, TanStack Query for server state
3. **Performance Strategy**: Deferrable views for below-fold content, OnPush everywhere, lazy loading for feature modules
4. **Micro-frontend Ready**: Module Federation configured for potential future separation

**Key Implementation Details:**
- Cart Service using Signals with computed totals and persisted state
- Product Catalog with TanStack Query caching and optimistic updates
- Checkout flow with multi-step wizard and form validation
- Admin panel with separate build and deployment pipeline

### Example 2: Legacy NgModule to Standalone Migration

**Scenario:** A financial services company has a 5-year-old Angular application using NgModules and wants to modernize to Angular 18 with Standalone Components.

**Migration Strategy:**
1. **Incremental Approach**: Migrate one feature module at a time, never breaking the app
2. **Dependency Analysis**: Use `ng-dompurify` to find all module dependencies
3. **Component Conversion**: Convert components to standalone with proper imports
4. **Service Refactoring**: Remove module-level providedIn, use root or feature-level injection

**Migration Results:**
- Reduced initial bundle size by 40% through tree-shaking
- Eliminated 200+ lines of boilerplate NgModule code
- Improved change detection performance by 60%
- Enabled adoption of new Angular features (defer blocks, zoneless)

### Example 3: Real-Time Dashboard with Signals

**Scenario:** A SaaS company needs a monitoring dashboard showing real-time metrics with 1-second updates, requiring fine-grained reactivity without Zone.js overhead.

**Implementation Approach:**
1. **Zoneless Bootstrap**: Enable experimental zoneless change detection
2. **Signal-Based State**: All dashboard state managed through Signals
3. **RxJS Interop**: Use toSignal for converting Observables to Signals
4. **WebSocket Integration**: Push updates directly to Signals

**Performance Results:**
- 30% reduction in bundle size (no Zone.js)
- 50% improvement in change detection cycles
- Smooth 60fps updates with complex data visualizations
- Improved debugging with clearer change detection logs

## Best Practices

### Architecture Design

- **Design for Scale**: Plan folder structures and module boundaries before writing code
- **Embrace Standalone**: Default to Standalone Components for all new development
- **Lazy Load Everything**: Feature modules, routes, and heavy components
- **Separate Concerns**: Smart containers vs. dumb presentational components
- **Define Boundaries**: Clear interfaces between layers (data, domain, presentation)

### State Management

- **Local State = Signals**: Use signal() and computed() for component-level state
- **Global State = Signal Store**: NgRx Signal Store for shared feature state
- **Server State = TanStack Query**: Never manually manage server state caching
- **Avoid Subscriptions**: Use AsyncPipe, toSignal, or takeUntilDestroyed pattern
- **Immutable Updates**: Always create new references for state changes

### Performance Engineering

- **OnPush Everywhere**: Default ChangeDetectionStrategy.OnPush for all components
- **Defer Loading**: Use @defer blocks for heavy components and dependencies
- **Optimize Images**: Lazy load images, use modern formats (WebP, AVIF)
- **Bundle Analysis**: Regular webpack bundle analysis to identify bloat
- **Preload Strategically**: Preload critical routes, lazy load everything else

### Code Quality

- **Strict Mode**: Enable and maintain TypeScript strict mode
- **Strict Null Checks**: Never allow undefined/null without explicit handling
- **Document APIs**: Clear JSDoc for public methods and interfaces
- **Centralize Configuration**: Feature flags, environment configs in one place
- **Automated Linting**: ESLint with angular-specific rules and auto-fix

### Testing Strategy

- **Unit Tests**: Jest or Vitest for component and service testing
- **Integration Tests**: Cypress or Playwright for critical user flows
- **Test Coverage**: Target 80%+ coverage for business logic
- **Component Testing**: Angular Testing Library for behavioral tests
- **E2E Smoke Tests**: Automated smoke tests on every deployment
