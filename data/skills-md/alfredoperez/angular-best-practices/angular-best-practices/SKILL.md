---
name: angular-best-practices
description: Curated Angular best practices for building performant, maintainable applications. Library-specific rules available as optional skills.
version: 1.0.0
author: alfredoperez
tags:
  - angular
  - typescript
  - signals
  - performance
  - testing
  - state-management
globs:
  - "**/*.ts"
  - "**/*.html"
  - "**/*.component.ts"
  - "**/*.service.ts"
---

# Angular Best Practices

Curated rules for building performant, maintainable Angular applications. Library-specific rules (NgRx, SignalStore, TanStack Query) available as optional skills.

## When to Use

Apply these practices when:
- Creating components, services, and directives
- Setting up state management with Signals
- Writing unit, component, and E2E tests
- Optimizing bundle size and runtime performance
- Implementing forms, routing, and SSR

## Categories

| Category | Rules | Impact |
|----------|-------|--------|
| Bundle Optimization | 5 | CRITICAL |
| Signals & Reactivity | 5 | HIGH |
| Change Detection | 5 | HIGH |
| Component Patterns | 4 | HIGH |
| RxJS Patterns | 5 | HIGH |
| Testing | 6 | HIGH |
| TypeScript | 14 | MEDIUM |

## Optional Library Skills

Install library-specific rules alongside this core skill:

| Library | Install Command |
|---------|----------------|
| NgRx | `npx skills add alfredoperez/angular-best-practices/skills/angular-best-practices-ngrx` |
| SignalStore | `npx skills add alfredoperez/angular-best-practices/skills/angular-best-practices-signalstore` |
| TanStack Query | `npx skills add alfredoperez/angular-best-practices/skills/angular-best-practices-tanstack` |

## Quick Reference

### Modern Angular Patterns

| Pattern | Use | Avoid |
|---------|-----|-------|
| Signal inputs | `input<T>()` | `@Input()` |
| Signal outputs | `output<T>()` | `@Output()` |
| Dependency injection | `inject()` | Constructor injection |
| Control flow | `@if`, `@for`, `@switch` | `*ngIf`, `*ngFor` |
| Class binding | `[class.active]` | `[ngClass]` |
| Change detection | `OnPush` | Default |
| Derived state | `computed()` | Getters |

### Component Template

```typescript
@Component({
  selector: 'app-user-card',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `
    @if (user(); as u) {
      <h2>{{ u.name }}</h2>
      <button (click)="selected.emit(u)">Select</button>
    }
  `,
})
export class UserCardComponent {
  user = input.required<User>();
  selected = output<User>();
}
```

### Service Template

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  private http = inject(HttpClient);

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}
```

### State with Signals

```typescript
export class CounterComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
  }
}
```

## License

MIT
