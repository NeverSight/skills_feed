---
name: angular-20-control-flow
description: Angular 20 built-in control flow syntax (@if, @for, @switch, @defer) for modern template programming. Use when writing templates with conditional rendering, loops, switch statements, or lazy loading components. Replaces *ngIf, *ngFor, *ngSwitch with new block syntax for better performance and type safety.
license: MIT
---

# Angular 20 Control Flow Skill

## Rules

### Control Flow Syntax
- Use `@if` / `@else` / `@else if` for conditional rendering
- Use `@for` with mandatory `track` expression for list iteration
- Use `@switch` / `@case` / `@default` for multi-branch conditionals
- Use `@defer` for lazy loading and code splitting
- MUST NOT use structural directives: `*ngIf`, `*ngFor`, `*ngSwitch`

### @for Track Expression
- Every `@for` loop MUST include a `track` expression
- Track by unique ID: `track item.id`
- Track by index for static lists: `track $index`
- MUST NOT track by object reference

### @defer Loading States
- Use appropriate trigger: `on viewport`, `on interaction`, `on idle`, `on immediate`, `on timer(Xs)`, `on hover`
- Use `@loading (minimum Xms)` to prevent UI flashing
- Use `@placeholder (minimum Xms)` for minimum display time

### Signal Integration
- Control flow conditions MUST use signal invocation: `@if (signal())`
- MUST NOT use plain properties without signal invocation

### Context Variables
- Available in `@for`: `$index`, `$first`, `$last`, `$even`, `$odd`, `$count`

---

## Context

### Purpose
This skill provides comprehensive guidance on **Angular 20's built-in control flow syntax**, which introduces new template syntax (@if, @for, @switch, @defer) that replaces structural directives with better performance, type safety, and developer experience.

### What is Angular Control Flow?

Angular 20 introduces new built-in control flow syntax:
- **@if / @else**: Conditional rendering (replaces *ngIf)
- **@for**: List iteration with tracking (replaces *ngFor)
- **@switch / @case**: Multi-branch conditionals (replaces *ngSwitch)
- **@defer**: Lazy loading and code splitting (new feature)
- **@empty**: Fallback for empty collections
- **@placeholder / @loading / @error**: Defer states

### When to Use This Skill

Use Angular 20 Control Flow when:
- Writing templates with conditional rendering
- Iterating over lists or arrays
- Implementing switch/case logic in templates
- Lazy loading components or content blocks
- Handling loading states and error boundaries
- Optimizing bundle size with deferred loading
- Migrating from *ngIf, *ngFor, *ngSwitch to modern syntax

### Core Control Flow Blocks

#### 1. @if - Conditional Rendering

**Basic Usage:**
```typescript
@Component({
  template: `
    @if (isLoggedIn()) {
      <div>Welcome back, {{ username() }}!</div>
    }
  `
})
export class WelcomeComponent {
  isLoggedIn = signal(false);
  username = signal('User');
}
```

**@if with @else:**
```typescript
@Component({
  template: `
    @if (user()) {
      <app-dashboard [user]="user()" />
    } @else {
      <app-login />
    }
  `
})
export class AppComponent {
  user = signal<User | null>(null);
}
```

**@if with @else if:**
```typescript
@Component({
  template: `
    @if (status() === 'loading') {
      <app-spinner />
    } @else if (status() === 'error') {
      <app-error [message]="errorMessage()" />
    } @else if (status() === 'success') {
      <app-content [data]="data()" />
    } @else {
      <app-empty-state />
    }
  `
})
export class DataComponent {
  status = signal<'loading' | 'error' | 'success' | 'idle'>('idle');
  errorMessage = signal('');
  data = signal<any[]>([]);
}
```

**Type Narrowing:**
```typescript
@Component({
  template: `
    @if (item(); as currentItem) {
      <!-- currentItem is type-narrowed here -->
      <div>{{ currentItem.name }}</div>
      <div>{{ currentItem.description }}</div>
    }
  `
})
export class ItemComponent {
  item = signal<Item | null>(null);
}
```

#### 2. @for - List Iteration

**Basic @for Loop:**
```typescript
@Component({
  template: `
    <ul>
      @for (item of items(); track item.id) {
        <li>{{ item.name }}</li>
      }
    </ul>
  `
})
export class ListComponent {
  items = signal([
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' },
    { id: 3, name: 'Item 3' }
  ]);
}
```

**@for with Index and Context:**
```typescript
@Component({
  template: `
    <div class="items">
      @for (item of items(); track item.id; let idx = $index, first = $first, last = $last) {
        <div class="item" [class.first]="first" [class.last]="last">
          <span class="index">{{ idx + 1 }}.</span>
          <span class="name">{{ item.name }}</span>
        </div>
      }
    </div>
  `
})
export class IndexedListComponent {
  items = signal<Item[]>([]);
}
```

**Available Context Variables:**
- `$index` - Current index (0-based)
- `$first` - True if first item
- `$last` - True if last item
- `$even` - True if even index
- `$odd` - True if odd index
- `$count` - Total number of items

**@for with @empty:**
```typescript
@Component({
  template: `
    <div class="product-list">
      @for (product of products(); track product.id) {
        <app-product-card [product]="product" />
      } @empty {
        <div class="empty-state">
          <p>No products available</p>
          <button (click)="loadProducts()">Refresh</button>
        </div>
      }
    </div>
  `
})
export class ProductListComponent {
  products = signal<Product[]>([]);
}
```

**Track By Best Practices:**
```typescript
// ✅ Good - Track by unique ID
@for (user of users(); track user.id) {
  <app-user-card [user]="user" />
}

// ✅ Good - Track by index for static lists
@for (tab of tabs; track $index) {
  <button>{{ tab }}</button>
}

// ❌ Bad - Track by object reference (will cause unnecessary re-renders)
@for (item of items(); track item) {
  <div>{{ item.name }}</div>
}
```

#### 3. @switch - Multi-branch Conditionals

**Basic @switch:**
```typescript
@Component({
  template: `
    @switch (userRole()) {
      @case ('admin') {
        <app-admin-panel />
      }
      @case ('moderator') {
        <app-moderator-panel />
      }
      @case ('user') {
        <app-user-panel />
      }
      @default {
        <app-guest-panel />
      }
    }
  `
})
export class RoleBasedComponent {
  userRole = signal<'admin' | 'moderator' | 'user' | 'guest'>('guest');
}
```

**@switch with Complex Conditions:**
```typescript
@Component({
  template: `
    @switch (connectionStatus()) {
      @case ('connected') {
        <div class="status online">
          <mat-icon>check_circle</mat-icon>
          Connected
        </div>
      }
      @case ('connecting') {
        <div class="status pending">
          <mat-spinner diameter="20"></mat-spinner>
          Connecting...
        </div>
      }
      @case ('disconnected') {
        <div class="status offline">
          <mat-icon>error</mat-icon>
          Disconnected
        </div>
      }
      @case ('error') {
        <div class="status error">
          <mat-icon>warning</mat-icon>
          Connection Error
        </div>
      }
      @default {
        <div class="status unknown">Unknown Status</div>
      }
    }
  `
})
export class ConnectionStatusComponent {
  connectionStatus = signal<'connected' | 'connecting' | 'disconnected' | 'error'>('disconnected');
}
```

#### 4. @defer - Lazy Loading and Code Splitting

**Basic Deferred Loading:**
```typescript
@Component({
  template: `
    @defer {
      <app-heavy-component />
    } @placeholder {
      <div class="skeleton">Loading...</div>
    }
  `
})
export class DeferredComponent {}
```

**Defer with Loading State:**
```typescript
@Component({
  template: `
    @defer {
      <app-video-player [src]="videoUrl" />
    } @loading (minimum 500ms) {
      <div class="loading-spinner">
        <mat-spinner></mat-spinner>
        <p>Loading video player...</p>
      </div>
    } @placeholder {
      <div class="video-placeholder">
        <mat-icon>play_circle</mat-icon>
      </div>
    } @error {
      <div class="error-state">
        <p>Failed to load video player</p>
        <button (click)="retry()">Retry</button>
      </div>
    }
  `
})
export class VideoComponent {
  videoUrl = signal('https://example.com/video.mp4');
}
```

**Defer Triggers:**

```typescript
// Viewport trigger - Load when visible
@defer (on viewport) {
  <app-below-fold-content />
}

// Interaction trigger - Load on click
@defer (on interaction) {
  <app-modal-content />
}

// Idle trigger - Load when browser is idle
@defer (on idle) {
  <app-analytics-widget />
}

// Immediate trigger - Load immediately
@defer (on immediate) {
  <app-critical-content />
}

// Timer trigger - Load after delay
@defer (on timer(5s)) {
  <app-delayed-content />
}

// Hover trigger - Load on hover
@defer (on hover) {
  <app-tooltip-content />
}

// Combined triggers
@defer (on viewport; on idle) {
  <app-content />
}
```

**Prefetching:**
```typescript
// Prefetch when idle
@defer (on viewport; prefetch on idle) {
  <app-article-content />
}

// Prefetch on hover
@defer (on interaction; prefetch on hover) {
  <app-modal />
}
```

**Defer with Minimum Loading Time:**
```typescript
@Component({
  template: `
    @defer (on viewport) {
      <app-chart [data]="chartData()" />
    } @loading (minimum 1s) {
      <!-- Show loading for at least 1 second to avoid flashing -->
      <div class="chart-skeleton"></div>
    } @placeholder (minimum 500ms) {
      <!-- Show placeholder for at least 500ms -->
      <div class="chart-placeholder"></div>
    }
  `
})
export class ChartComponent {
  chartData = signal<ChartData[]>([]);
}
```

### Migration from Old Syntax

#### ngIf → @if
```typescript
// Before (Angular 19 and earlier)
<div *ngIf="isVisible">Content</div>
<div *ngIf="user; else loading">{{ user.name }}</div>

// After (Angular 20+)
@if (isVisible()) {
  <div>Content</div>
}

@if (user(); as currentUser) {
  <div>{{ currentUser.name }}</div>
} @else {
  <ng-container [ngTemplateOutlet]="loading" />
}
```

#### ngFor → @for
```typescript
// Before
<li *ngFor="let item of items; trackBy: trackById">{{ item.name }}</li>

// After
@for (item of items(); track item.id) {
  <li>{{ item.name }}</li>
}
```

#### ngSwitch → @switch
```typescript
// Before
<div [ngSwitch]="status">
  <div *ngSwitchCase="'success'">Success!</div>
  <div *ngSwitchCase="'error'">Error!</div>
  <div *ngSwitchDefault>Loading...</div>
</div>

// After
@switch (status()) {
  @case ('success') {
    <div>Success!</div>
  }
  @case ('error') {
    <div>Error!</div>
  }
  @default {
    <div>Loading...</div>
  }
}
```

### Best Practices

#### 1. Use Signals with Control Flow
```typescript
// ✅ Good - Reactive with signals
export class Component {
  items = signal<Item[]>([]);
  isLoading = signal(false);
}

@Component({
  template: `
    @if (isLoading()) {
      <spinner />
    } @else {
      @for (item of items(); track item.id) {
        <item-card [item]="item" />
      }
    }
  `
})
```

#### 2. Always Use track in @for
```typescript
// ✅ Good - Proper tracking
@for (user of users(); track user.id) {
  <user-card [user]="user" />
}

// ❌ Bad - Missing track (will cause error)
@for (user of users()) {
  <user-card [user]="user" />
}
```

### 3. Leverage @defer for Performance
```typescript
// ✅ Good - Defer heavy components
@defer (on viewport) {
  <app-complex-chart />
} @placeholder {
  <div class="chart-skeleton"></div>
}

// ✅ Good - Defer analytics
@defer (on idle) {
  <app-analytics-tracker />
}
```

### 4. Use @empty for Better UX
```typescript
// ✅ Good - Handle empty state
@for (item of items(); track item.id) {
  <item-card [item]="item" />
} @empty {
  <empty-state message="No items found" />
}
```

### 5. Type Narrowing with @if
```typescript
// ✅ Good - Type narrowing
@if (user(); as currentUser) {
  <!-- currentUser is guaranteed non-null here -->
  <div>{{ currentUser.email }}</div>
}
```

## 🔧 Advanced Patterns

### Nested Control Flow
```typescript
@Component({
  template: `
    @if (data(); as currentData) {
      @for (category of currentData.categories; track category.id) {
        <div class="category">
          <h3>{{ category.name }}</h3>
          @for (item of category.items; track item.id) {
            <div class="item">{{ item.title }}</div>
          } @empty {
            <p>No items in this category</p>
          }
        </div>
      }
    } @else {
      <app-loading />
    }
  `
})
```

### Conditional Deferred Loading
```typescript
@Component({
  template: `
    @if (shouldLoadHeavyComponent()) {
      @defer (on viewport) {
        <app-heavy-component [config]="config()" />
      } @loading {
        <skeleton-loader />
      }
    }
  `
})
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Syntax error with @ blocks | Ensure Angular 20+ and update compiler |
| @for without track error | Always add `track` expression to @for |
| @defer not lazy loading | Check bundle config and verify component is in separate chunk |
| Type errors with @if | Use `as` alias for type narrowing |
| @empty not showing | Ensure collection signal returns empty array, not undefined |

## 📖 References

- [Angular Control Flow Guide](https://angular.dev/guide/templates/control-flow)
- [Angular Defer Guide](https://angular.dev/guide/defer)
- [Migration Guide](https://angular.dev/reference/migrations/control-flow)

---

## 📂 Recommended Placement

**Project-level skill:**
```
/.github/skills/angular-20-control-flow/SKILL.md
```

Copilot will load this when working with Angular 20 control flow syntax.
