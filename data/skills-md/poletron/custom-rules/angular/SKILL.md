---
name: angular
description: >
  Angular best practices with TypeScript, RxJS, and modern patterns.
  Trigger: When building Angular applications with TypeScript.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with angular"

## When to Use

Use this skill when:
- Building Angular 16+ applications
- Using standalone components
- Working with RxJS observables
- Implementing reactive forms

---

## Critical Patterns

### Standalone Components (REQUIRED)

```typescript
// ✅ ALWAYS: Use standalone components (Angular 16+)
@Component({
  selector: 'app-user-card',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <div class="card">
      <h2>{{ user.name }}</h2>
    </div>
  `
})
export class UserCardComponent {
  @Input({ required: true }) user!: User;
}
```

### Signals (RECOMMENDED)

```typescript
// ✅ Use signals for reactive state (Angular 16+)
@Component({...})
export class CounterComponent {
  count = signal(0);
  doubleCount = computed(() => this.count() * 2);
  
  increment() {
    this.count.update(n => n + 1);
  }
}
```

### RxJS Best Practices (REQUIRED)

```typescript
// ✅ ALWAYS: Use async pipe, avoid manual subscriptions
@Component({
  template: `
    <div *ngFor="let user of users$ | async">
      {{ user.name }}
    </div>
  `
})
export class UsersComponent {
  users$ = this.userService.getUsers();
}

// ❌ NEVER: Manual subscribe without cleanup
ngOnInit() {
  this.userService.getUsers().subscribe(users => {
    this.users = users;  // Memory leak risk!
  });
}
```

---

## Decision Tree

```
Need component state?      → Use signals
Need shared state?         → Use service with BehaviorSubject
Need HTTP data?            → Use HttpClient + async pipe
Need form validation?      → Use Reactive Forms
Need lazy loading?         → Use loadComponent()
```

---

## Code Examples

### Reactive Forms

```typescript
@Component({...})
export class UserFormComponent {
  form = new FormGroup({
    name: new FormControl('', [Validators.required]),
    email: new FormControl('', [Validators.required, Validators.email]),
  });
  
  onSubmit() {
    if (this.form.valid) {
      this.userService.create(this.form.value);
    }
  }
}
```

### Service with State

```typescript
@Injectable({ providedIn: 'root' })
export class CartService {
  private items = new BehaviorSubject<CartItem[]>([]);
  items$ = this.items.asObservable();
  
  addItem(item: CartItem) {
    this.items.next([...this.items.value, item]);
  }
}
```

---

## Commands

```bash
ng new myapp --standalone
ng serve
ng generate component users
ng build --configuration production
ng test
```
