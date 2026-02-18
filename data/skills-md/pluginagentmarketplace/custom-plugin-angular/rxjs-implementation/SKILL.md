---
name: rxjs-implementation
description: Implement RxJS observables, apply operators, fix memory leaks with unsubscribe patterns, handle errors, create subjects, and build reactive data pipelines in Angular applications.
sasmp_version: "1.3.0"
bonded_agent: 03-reactive-programming
bond_type: PRIMARY_BOND
---

# RxJS Implementation Skill

## Quick Start

### Observable Basics
```typescript
import { Observable } from 'rxjs';

// Create observable
const observable = new Observable((observer) => {
  observer.next(1);
  observer.next(2);
  observer.next(3);
  observer.complete();
});

// Subscribe
const subscription = observable.subscribe({
  next: (value) => console.log(value),
  error: (error) => console.error(error),
  complete: () => console.log('Done')
});

// Unsubscribe
subscription.unsubscribe();
```

### Common Operators
```typescript
import { map, filter, switchMap, takeUntil } from 'rxjs/operators';

// Transformation
data$.pipe(
  map(user => user.name),
  filter(name => name.length > 0)
).subscribe(name => console.log(name));

// Higher-order
userId$.pipe(
  switchMap(id => this.userService.getUser(id))
).subscribe(user => console.log(user));
```

## Subjects

### Subject Types
```typescript
import { Subject, BehaviorSubject, ReplaySubject } from 'rxjs';

// Subject - No initial value
const subject = new Subject<string>();
subject.next('hello');

// BehaviorSubject - Has initial value
const behavior = new BehaviorSubject<string>('initial');
behavior.next('new value');

// ReplaySubject - Replays N values
const replay = new ReplaySubject<string>(3);
replay.next('one');
replay.next('two');
```

### Service with Subject
```typescript
@Injectable()
export class NotificationService {
  private messageSubject = new Subject<string>();
  public message$ = this.messageSubject.asObservable();

  notify(message: string) {
    this.messageSubject.next(message);
  }
}

// Usage
constructor(private notification: NotificationService) {
  this.notification.message$.subscribe(msg => {
    console.log('Notification:', msg);
  });
}
```

## Transformation Operators

```typescript
// map - Transform values
source$.pipe(
  map(user => user.name)
)

// switchMap - Switch to new observable (cancel previous)
userId$.pipe(
  switchMap(id => this.userService.getUser(id))
)

// mergeMap - Merge all results
fileIds$.pipe(
  mergeMap(id => this.downloadFile(id))
)

// concatMap - Sequential processing
tasks$.pipe(
  concatMap(task => this.processTask(task))
)

// exhaustMap - Ignore new while processing
clicks$.pipe(
  exhaustMap(() => this.longRequest())
)
```

## Filtering Operators

```typescript
// filter - Only pass matching values
data$.pipe(
  filter(item => item.active)
)

// first - Take first value
data$.pipe(first())

// take - Take N values
data$.pipe(take(5))

// takeUntil - Take until condition
data$.pipe(
  takeUntil(this.destroy$)
)

// distinct - Filter duplicates
data$.pipe(
  distinct(),
  distinctUntilChanged()
)

// debounceTime - Wait N ms
input$.pipe(
  debounceTime(300),
  distinctUntilChanged()
)
```

## Combination Operators

```typescript
import { combineLatest, merge, concat, zip } from 'rxjs';

// combineLatest - Latest from all
combineLatest([user$, settings$, theme$]).pipe(
  map(([user, settings, theme]) => ({ user, settings, theme }))
)

// merge - Values from any
merge(click$, hover$, input$)

// concat - Sequential
concat(request1$, request2$, request3$)

// zip - Wait for all
zip(form1$, form2$, form3$)

// withLatestFrom - Combine with latest
click$.pipe(
  withLatestFrom(user$),
  map(([click, user]) => ({ click, user }))
)
```

## Error Handling

```typescript
// catchError - Handle errors
data$.pipe(
  catchError(error => {
    console.error('Error:', error);
    return of(defaultValue);
  })
)

// retry - Retry on error
request$.pipe(
  retry(3),
  catchError(error => throwError(error))
)

// timeout - Timeout if no value
request$.pipe(
  timeout(5000),
  catchError(error => of(null))
)
```

## Memory Leak Prevention

### Unsubscribe Pattern
```typescript
private destroy$ = new Subject<void>();

ngOnInit() {
  this.data$.pipe(
    takeUntil(this.destroy$)
  ).subscribe(data => {
    this.processData(data);
  });
}

ngOnDestroy() {
  this.destroy$.next();
  this.destroy$.complete();
}
```

### Async Pipe (Preferred)
```typescript
// Component
export class UserComponent {
  user$ = this.userService.getUser(1);

  constructor(private userService: UserService) {}
}

// Template - Async pipe handles unsubscribe
<div>{{ user$ | async as user }}
  <p>{{ user.name }}</p>
</div>
```

## Advanced Patterns

### Share Operator
```typescript
// Hot observable - Share single subscription
readonly users$ = this.http.get('/api/users').pipe(
  shareReplay(1) // Cache last result
);

// Now multiple subscriptions use same HTTP request
this.users$.subscribe(users => {...});
this.users$.subscribe(users => {...}); // Reuses cached
```

### Scan for State
```typescript
// Accumulate state
const counter$ = clicks$.pipe(
  scan((count) => count + 1, 0)
)

// Complex state
const appState$ = actions$.pipe(
  scan((state, action) => {
    switch(action.type) {
      case 'ADD_USER': return { ...state, users: [...state.users, action.user] };
      case 'DELETE_USER': return { ...state, users: state.users.filter(u => u.id !== action.id) };
      default: return state;
    }
  }, initialState)
)
```

### Forkjoin for Multiple Requests
```typescript
// Parallel requests
forkJoin({
  users: this.userService.getUsers(),
  settings: this.settingService.getSettings(),
  themes: this.themeService.getThemes()
}).subscribe(({ users, settings, themes }) => {
  console.log('All loaded:', users, settings, themes);
})
```

## Testing Observables

```typescript
import { marbles } from 'rxjs-marbles';

it('should map values correctly', marbles((m) => {
  const source = m.hot('a-b-|', { a: 1, b: 2 });
  const expected = m.cold('x-y-|', { x: 2, y: 4 });

  const result = source.pipe(
    map(x => x * 2)
  );

  m.expect(result).toBeObservable(expected);
}));
```

## Best Practices

1. **Always unsubscribe**: Use takeUntil or async pipe
2. **Use higher-order operators**: switchMap, mergeMap, etc.
3. **Avoid nested subscriptions**: Use operators instead
4. **Share subscriptions**: Use share/shareReplay for expensive operations
5. **Handle errors**: Always include catchError
6. **Type your observables**: `Observable<User>` not just `Observable`

## Common Mistakes to Avoid

```typescript
// ❌ Wrong - Creates multiple subscriptions
this.data$.subscribe(d => {
  this.data$.subscribe(d2 => {
    // nested subscriptions!
  });
});

// ✅ Correct - Use switchMap
this.data$.pipe(
  switchMap(d => this.otherService.fetch(d))
).subscribe(result => {
  // handled
});

// ❌ Wrong - Memory leak
ngOnInit() {
  this.data$.subscribe(data => this.data = data);
}

// ✅ Correct - Unsubscribe or async
ngOnInit() {
  this.data$ = this.service.getData();
}
// In template: {{ data$ | async }}
```

## Resources

- [RxJS Documentation](https://rxjs.dev/)
- [Interactive Diagrams](https://rxmarbles.com/)
- [RxJS Operators](https://rxjs.dev/api)
