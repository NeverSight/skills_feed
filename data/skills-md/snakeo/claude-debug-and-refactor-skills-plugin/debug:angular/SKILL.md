---
name: debug:angular
description: Debug Angular applications systematically with expert-level diagnostic techniques. This skill provides comprehensive guidance for troubleshooting dependency injection errors, change detection issues (NG0100), RxJS subscription leaks, lazy loading failures, zone.js problems, and common Angular runtime errors. Includes structured four-phase debugging methodology, Angular DevTools usage, console debugging utilities (ng.probe), and performance profiling strategies for modern Angular applications.
---

# Angular Debugging Guide

This guide provides a systematic approach to debugging Angular applications, covering common error patterns, debugging tools, and structured resolution phases.

## Common Error Patterns

### NullInjectorError

**Symptoms:**
- `NullInjectorError: No provider for <ServiceName>`
- `StaticInjectorError: No provider for <ServiceName>`
- Service injection fails at runtime

**Root Causes:**
1. Service not provided in any module or component
2. Circular dependency between services
3. Missing `@Injectable()` decorator
4. Service provided in wrong scope (lazy-loaded module vs root)

**Solutions:**
```typescript
// Solution 1: Provide in root (recommended for singletons)
@Injectable({
  providedIn: 'root'
})
export class MyService { }

// Solution 2: Provide in specific module
@NgModule({
  providers: [MyService]
})
export class FeatureModule { }

// Solution 3: Provide in component (new instance per component)
@Component({
  providers: [MyService]
})
export class MyComponent { }
```

### ExpressionChangedAfterItHasBeenCheckedError (NG0100)

**Symptoms:**
- Error appears only in development mode
- Typically occurs in `ngAfterViewInit` or `ngAfterContentInit`
- Value changes during change detection cycle

**Root Causes:**
1. Modifying component state in lifecycle hooks after change detection
2. Child component modifying parent state
3. Async operations completing during change detection

**Solutions:**
```typescript
// Solution 1: Use setTimeout to defer change
ngAfterViewInit() {
  setTimeout(() => {
    this.value = 'new value';
  });
}

// Solution 2: Use ChangeDetectorRef
constructor(private cdr: ChangeDetectorRef) {}

ngAfterViewInit() {
  this.value = 'new value';
  this.cdr.detectChanges();
}

// Solution 3: Use async pipe (preferred for observables)
// In template: {{ value$ | async }}
value$ = this.service.getValue();
```

### Common NG Error Codes (NG0100-NG0999)

| Error Code | Description | Common Fix |
|------------|-------------|------------|
| NG0100 | Expression changed after checked | Use `detectChanges()` or `setTimeout` |
| NG0200 | Circular dependency in DI | Refactor service dependencies |
| NG0201 | No provider for service | Add to providers array or use `providedIn` |
| NG0300 | Multiple components match selector | Make selectors more specific |
| NG0301 | Export not found | Check export name in directive/component |
| NG0302 | Pipe not found | Import module containing pipe |
| NG0303 | No matching element | Check selector syntax |
| NG0500 | Hydration mismatch (SSR) | Ensure server/client render same content |
| NG0910 | Unsafe binding | Sanitize or use `bypassSecurityTrust*` |
| NG0912 | Component ID collision | Unique component selectors |

### RxJS Subscription Leaks

**Symptoms:**
- Memory leaks in long-running applications
- Console warnings about destroyed components
- Multiple HTTP requests for same data
- Performance degradation over time

**Detection:**
```typescript
// Use takeUntilDestroyed (Angular 16+)
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

@Component({...})
export class MyComponent {
  private destroyRef = inject(DestroyRef);

  ngOnInit() {
    this.service.getData()
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(data => this.data = data);
  }
}

// Legacy approach with Subject
private destroy$ = new Subject<void>();

ngOnInit() {
  this.service.getData()
    .pipe(takeUntil(this.destroy$))
    .subscribe();
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
```

**RxJS Debugging Operators:**
```typescript
import { tap } from 'rxjs/operators';

this.data$.pipe(
  tap({
    next: v => console.log('Value:', v),
    error: e => console.error('Error:', e),
    complete: () => console.log('Complete')
  })
).subscribe();
```

### Lazy Loading Failures

**Symptoms:**
- `ChunkLoadError` in console
- Module fails to load on navigation
- Network errors for chunk files

**Common Causes:**
1. Incorrect path in `loadChildren`
2. Missing default export
3. Network/CDN issues
4. Cache issues after deployment

**Solutions:**
```typescript
// Correct lazy loading syntax (Angular 14+)
const routes: Routes = [
  {
    path: 'feature',
    loadChildren: () => import('./feature/feature.module')
      .then(m => m.FeatureModule)
  },
  // Standalone components (Angular 15+)
  {
    path: 'standalone',
    loadComponent: () => import('./standalone/standalone.component')
      .then(c => c.StandaloneComponent)
  }
];

// Handle chunk load errors
// In app.component.ts or error handler
constructor(private router: Router) {
  this.router.events.subscribe(event => {
    if (event instanceof NavigationError) {
      if (event.error.name === 'ChunkLoadError') {
        window.location.reload();
      }
    }
  });
}
```

### Zone.js Issues

**Symptoms:**
- Change detection not triggering
- UI not updating after async operations
- `runOutsideAngular` causing update issues

**Solutions:**
```typescript
constructor(private ngZone: NgZone) {}

// Force change detection inside Angular zone
ngOnInit() {
  someExternalLibrary.onEvent((data) => {
    this.ngZone.run(() => {
      this.data = data;
    });
  });
}

// Optimize by running outside zone (for performance-critical code)
runHeavyComputation() {
  this.ngZone.runOutsideAngular(() => {
    // Heavy computation that doesn't need CD
    const result = this.compute();

    // Re-enter zone when updating UI
    this.ngZone.run(() => {
      this.result = result;
    });
  });
}
```

### Zoneless Angular (Angular 18+)

```typescript
// For zoneless applications, use signals
import { signal, computed, effect } from '@angular/core';

@Component({
  selector: 'app-zoneless',
  template: `<p>Count: {{ count() }}</p>`
})
export class ZonelessComponent {
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  increment() {
    this.count.update(c => c + 1);
  }
}
```

## Debugging Tools

### Angular DevTools

**Installation:**
- Chrome: Install from [Chrome Web Store](https://chrome.google.com/webstore/detail/angular-devtools)
- Firefox: Install from [Firefox Add-ons](https://addons.mozilla.org/firefox/addon/angular-devtools/)

**Features:**
1. **Component Explorer**: Inspect component tree, inputs, outputs, and state
2. **Profiler**: Record and analyze change detection cycles
3. **Dependency Injection Graph**: Visualize injector hierarchy
4. **Router Tree**: Debug routing configuration

**Requirements:**
- Application must be in development mode (`ng serve`)
- For deployed apps, build with `optimization: false`

### ng.probe() (Console Debugging)

```javascript
// In browser console

// Get component instance from DOM element
ng.getComponent($0);

// Get directive instances
ng.getDirectives($0);

// Get owning component
ng.getOwningComponent($0);

// Get injector
ng.getInjector($0);

// Trigger change detection
ng.applyChanges(component);

// Get context (for embedded views)
ng.getContext($0);

// Angular 14+ debugging utilities
const appRef = ng.getInjector(document.querySelector('app-root'))
  .get(ng.coreTokens.ApplicationRef);
appRef.tick(); // Force global change detection
```

### Source Maps Configuration

```json
// angular.json
{
  "projects": {
    "my-app": {
      "architect": {
        "build": {
          "configurations": {
            "development": {
              "sourceMap": true,
              "optimization": false,
              "extractLicenses": false,
              "namedChunks": true
            },
            "production": {
              "sourceMap": {
                "scripts": true,
                "styles": true,
                "hidden": true,
                "vendor": false
              }
            }
          }
        }
      }
    }
  }
}
```

### Custom Error Handler

```typescript
// global-error-handler.ts
import { ErrorHandler, Injectable, Injector } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private injector: Injector) {}

  handleError(error: Error | HttpErrorResponse): void {
    if (error instanceof HttpErrorResponse) {
      // Server error
      console.error('HTTP Error:', error.status, error.message);
    } else {
      // Client error
      console.error('Client Error:', error.message);
      console.error('Stack:', error.stack);
    }

    // Log to external service
    const loggingService = this.injector.get(LoggingService);
    loggingService.logError(error);
  }
}

// app.module.ts
@NgModule({
  providers: [
    { provide: ErrorHandler, useClass: GlobalErrorHandler }
  ]
})
export class AppModule { }
```

### HTTP Interceptor for Debugging

```typescript
@Injectable()
export class DebugInterceptor implements HttpInterceptor {
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    const started = Date.now();

    return next.handle(req).pipe(
      tap({
        next: (event) => {
          if (event instanceof HttpResponse) {
            const elapsed = Date.now() - started;
            console.log(`${req.method} ${req.urlWithParams} - ${elapsed}ms`);
          }
        },
        error: (error) => {
          console.error(`${req.method} ${req.urlWithParams} - Error:`, error);
        }
      })
    );
  }
}
```

## The Four Phases of Angular Debugging

### Phase 1: Reproduce and Isolate

**Objective:** Consistently reproduce the issue and narrow down the scope.

**Steps:**
1. **Reproduce the error** - Get exact steps to trigger the issue
2. **Check the console** - Note full error message and stack trace
3. **Identify the component** - Which component/service is affected?
4. **Check recent changes** - Use `git diff` to see what changed

**Commands:**
```bash
# Check recent changes
git diff HEAD~5 --name-only

# Check for TypeScript errors
ng build --configuration development 2>&1 | head -50

# Check for lint issues
ng lint
```

**Console Investigation:**
```typescript
// Add strategic logging
console.group('Component State');
console.log('Inputs:', this.inputValue);
console.log('State:', this.state);
console.trace('Call stack');
console.groupEnd();
```

### Phase 2: Analyze the Error

**Objective:** Understand exactly what is failing and why.

**For DI Errors:**
```typescript
// Check injector hierarchy
const injector = TestBed.inject(Injector);
console.log('Providers:', injector);

// Verify service is provided
try {
  const service = TestBed.inject(MyService);
  console.log('Service found:', service);
} catch (e) {
  console.error('Service not found:', e);
}
```

**For Change Detection Errors:**
```typescript
// Enable change detection debugging
import { enableDebugTools } from '@angular/platform-browser';

// In main.ts
platformBrowserDynamic().bootstrapModule(AppModule)
  .then(ref => {
    const appRef = ref.injector.get(ApplicationRef);
    const componentRef = appRef.components[0];
    enableDebugTools(componentRef);
    // Access via: window.ng.profiler.timeChangeDetection()
  });
```

**For Template Errors:**
```typescript
// Use safe navigation operator
{{ user?.profile?.name }}

// Use @if with else block (Angular 17+)
@if (user) {
  <p>{{ user.name }}</p>
} @else {
  <p>Loading...</p>
}

// Use *ngIf with ng-template (legacy)
<p *ngIf="user; else loading">{{ user.name }}</p>
<ng-template #loading>Loading...</ng-template>
```

### Phase 3: Apply the Fix

**Objective:** Implement and verify the solution.

**Fix Patterns:**

```typescript
// Pattern 1: Safe observable handling
this.data$ = this.service.getData().pipe(
  catchError(error => {
    console.error('Data fetch failed:', error);
    return of(null); // Return fallback
  }),
  shareReplay(1) // Cache for multiple subscribers
);

// Pattern 2: Proper initialization
@Input() set items(value: Item[]) {
  this._items = value ?? [];
  this.updateView();
}
private _items: Item[] = [];

// Pattern 3: OnPush with immutability
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class OptimizedComponent {
  @Input() data!: ReadonlyArray<Item>;

  updateData() {
    // Create new reference to trigger CD
    this.data = [...this.data, newItem];
  }
}
```

**Verify the Fix:**
```bash
# Run affected tests
ng test --include="**/affected.component.spec.ts"

# Run e2e tests
ng e2e --spec="affected.e2e-spec.ts"

# Build to check for compilation errors
ng build --configuration production
```

### Phase 4: Prevent Regression

**Objective:** Add tests and monitoring to prevent recurrence.

**Write Targeted Tests:**
```typescript
describe('BugfixComponent', () => {
  it('should handle null input gracefully', () => {
    component.data = null;
    fixture.detectChanges();
    expect(component.displayData).toEqual([]);
  });

  it('should unsubscribe on destroy', () => {
    const subscription = component['subscription'];
    spyOn(subscription, 'unsubscribe');
    component.ngOnDestroy();
    expect(subscription.unsubscribe).toHaveBeenCalled();
  });

  it('should handle HTTP errors', fakeAsync(() => {
    spyOn(service, 'getData').and.returnValue(
      throwError(() => new Error('Network error'))
    );
    component.loadData();
    tick();
    expect(component.error).toBe('Failed to load data');
  }));
});
```

**Add Error Boundary:**
```typescript
// error-boundary.component.ts
@Component({
  selector: 'app-error-boundary',
  template: `
    @if (hasError) {
      <div class="error-fallback">
        <h2>Something went wrong</h2>
        <button (click)="retry()">Retry</button>
      </div>
    } @else {
      <ng-content></ng-content>
    }
  `
})
export class ErrorBoundaryComponent implements OnInit, ErrorHandler {
  hasError = false;

  handleError(error: Error): void {
    this.hasError = true;
    console.error('Error caught:', error);
  }

  retry(): void {
    this.hasError = false;
  }
}
```

## Quick Reference Commands

### Development

```bash
# Start development server
ng serve

# Start with specific configuration
ng serve --configuration=development

# Start with SSL
ng serve --ssl

# Open browser automatically
ng serve --open

# Specify port
ng serve --port 4201

# Disable host check (for mobile testing)
ng serve --host 0.0.0.0 --disable-host-check
```

### Building

```bash
# Development build (with source maps)
ng build --configuration development

# Production build
ng build --configuration production

# Build with stats for bundle analysis
ng build --stats-json

# Analyze bundle
npx webpack-bundle-analyzer dist/my-app/stats.json
```

### Testing

```bash
# Run all tests
ng test

# Run tests once (CI mode)
ng test --no-watch --code-coverage

# Run specific test file
ng test --include="**/my.component.spec.ts"

# Run with specific browsers
ng test --browsers=ChromeHeadless

# Debug tests in browser
ng test --browsers=Chrome

# E2E tests
ng e2e
```

### Linting and Code Quality

```bash
# Run ESLint
ng lint

# Fix auto-fixable issues
ng lint --fix

# Check specific files
ng lint --files="src/app/my.component.ts"
```

### Generating Code

```bash
# Generate component with tests
ng generate component my-component

# Generate service
ng generate service my-service

# Generate module with routing
ng generate module my-module --routing

# Dry run (preview changes)
ng generate component my-component --dry-run
```

### Cache Management

```bash
# Clear Angular cache
ng cache clean

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Debugging Specific Issues

```bash
# Check Angular version
ng version

# Update Angular
ng update @angular/core @angular/cli

# Check for outdated packages
npm outdated

# Check TypeScript configuration
npx tsc --showConfig

# Check for circular dependencies
npx madge --circular src/

# Profile memory usage
node --inspect node_modules/.bin/ng serve
```

## Performance Debugging

### Profiling Change Detection

```typescript
// Enable profiling in main.ts
import { enableProdMode } from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

platformBrowserDynamic().bootstrapModule(AppModule)
  .then(moduleRef => {
    const appRef = moduleRef.injector.get(ApplicationRef);
    const componentRef = appRef.components[0];

    // Enable debug tools
    enableDebugTools(componentRef);

    // In console: ng.profiler.timeChangeDetection()
  });
```

### OnPush Optimization

```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class PerformantComponent {
  // Use signals (Angular 16+) for reactive state
  count = signal(0);
  doubled = computed(() => this.count() * 2);

  // Or use observables with async pipe
  data$ = this.service.getData().pipe(
    shareReplay({ bufferSize: 1, refCount: true })
  );
}
```

### TrackBy for Lists

```typescript
@Component({
  template: `
    @for (item of items; track item.id) {
      <app-item [item]="item" />
    }
  `
})
export class ListComponent {
  items: Item[] = [];

  // Legacy ngFor syntax
  trackById(index: number, item: Item): number {
    return item.id;
  }
}
```

## Resources

- [Angular Error Encyclopedia](https://angular.dev/errors)
- [Angular DevTools Documentation](https://angular.dev/tools/devtools)
- [Angular Error Handling Best Practices](https://angular.dev/best-practices/error-handling)
- [RxJS Debugging Guide](https://rxjs.dev/guide/testing/marble-testing)
- [Zone.js Documentation](https://github.com/angular/angular/tree/main/packages/zone.js)
