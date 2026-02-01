---
name: typescript-best-practices
description: Guides TypeScript best practices for type safety, code organization, and maintainability. Use this skill when configuring TypeScript projects, deciding on typing strategies, writing async code, or reviewing TypeScript code quality.
---

# TypeScript Best Practices

Comprehensive guide to writing clean, type-safe, and maintainable TypeScript code.

## When to Use

- Configuring a new TypeScript project
- Deciding between interface vs type alias
- Writing async/await code
- Reviewing TypeScript code quality
- Avoiding common TypeScript pitfalls

## 1. Project Configuration

Always enable `strict` mode for maximum type safety:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
  }
}
```

**Why strict mode matters:**
- Catches bugs at compile time instead of runtime
- Forces explicit handling of null/undefined
- Prevents implicit `any` types from sneaking in

## 2. Type System Best Practices

### Use Type Inference

Let TypeScript infer types when obvious:

```typescript
// Good - inference works fine
const name = 'Alice';
const count = 42;
const items = ['a', 'b', 'c'];

// Bad - redundant annotations
const name: string = 'Alice';
const count: number = 42;
```

### Be Explicit for Public APIs

```typescript
// Good - explicit for function signatures
function calculateTotal(items: CartItem[], taxRate: number): number {
  return items.reduce((sum, item) => sum + item.price, 0) * (1 + taxRate);
}

// Good - explicit for class properties
class UserService {
  private readonly cache: Map<string, User>;
  
  constructor(private api: ApiClient) {
    this.cache = new Map();
  }
}
```

### Interface vs Type Alias

**Use `interface` for:**
- Object shapes that can be extended
- Public API contracts
- Declaration merging needs

```typescript
interface User {
  id: string;
  name: string;
}

interface Admin extends User {
  permissions: string[];
}
```

**Use `type` for:**
- Unions and intersections
- Tuples
- Mapped types
- Primitive aliases

```typescript
type Status = 'pending' | 'approved' | 'rejected';
type Point = [number, number];
type ReadonlyUser = Readonly<User>;
```

### Avoid `any` - Use `unknown` with Type Guards

```typescript
// Bad - defeats type checking
function process(data: any) {
  return data.toUpperCase(); // No error, but might crash
}

// Good - use unknown with type guards
function process(data: unknown): string {
  if (typeof data === 'string') {
    return data.toUpperCase();
  }
  throw new Error('Expected string');
}

// Good - use generics for flexibility
function identity<T>(value: T): T {
  return value;
}
```

## 3. Code Organization

### File Naming Convention

Use lowercase with dots for clarity:

```
src/
├── user/
│   ├── user.service.ts
│   ├── user.model.ts
│   ├── user.controller.ts
│   └── index.ts          # Barrel file
├── auth/
│   ├── auth.service.ts
│   └── index.ts
└── types/
    └── index.ts
```

### Barrel Files for Clean Exports

```typescript
// user/index.ts
export { UserService } from './user.service';
export { User, CreateUserDto } from './user.model';
export { UserController } from './user.controller';
```

```typescript
// Consumer imports cleanly
import { UserService, User } from './user';
```

## 4. Functions Best Practices

### Explicit Parameter Types

```typescript
// Good - clear contract
function greet(name: string, greeting = 'Hello'): string {
  return `${greeting}, ${name}!`;
}

// Good - use rest parameters for variable arguments
function sum(...numbers: number[]): number {
  return numbers.reduce((a, b) => a + b, 0);
}
```

### Single Responsibility

```typescript
// Bad - function does too much
function processUser(user: User) {
  // validates, transforms, saves, and sends email
}

// Good - split into focused functions
function validateUser(user: User): ValidationResult { ... }
function transformUser(user: User): TransformedUser { ... }
function saveUser(user: TransformedUser): Promise<void> { ... }
function sendWelcomeEmail(user: User): Promise<void> { ... }
```

### Guard Clauses for Early Returns

```typescript
// Good - guard clauses
function processOrder(order: Order | null): ProcessedOrder {
  if (!order) throw new Error('Order required');
  if (order.items.length === 0) throw new Error('Order must have items');
  if (order.status !== 'pending') throw new Error('Order already processed');
  
  // Main logic here - no nesting
  return { ...order, status: 'processed' };
}
```

## 5. Async/Await Patterns

### Always Handle Errors

```typescript
// Good - explicit error handling
async function fetchUser(id: string): Promise<User> {
  try {
    const response = await api.get(`/users/${id}`);
    return response.data;
  } catch (error) {
    if (error instanceof NotFoundError) {
      throw new UserNotFoundError(id);
    }
    throw error;
  }
}
```

### Use Promise.all for Parallel Operations

```typescript
// Bad - sequential when parallel is possible
const user = await fetchUser(id);
const orders = await fetchOrders(id);
const preferences = await fetchPreferences(id);

// Good - parallel execution
const [user, orders, preferences] = await Promise.all([
  fetchUser(id),
  fetchOrders(id),
  fetchPreferences(id),
]);
```

### Flatten Async Chains

```typescript
// Bad - callback hell with async
async function bad() {
  return fetchUser().then(user => {
    return fetchOrders(user.id).then(orders => {
      return processOrders(orders).then(result => {
        return result;
      });
    });
  });
}

// Good - flat async/await
async function good() {
  const user = await fetchUser();
  const orders = await fetchOrders(user.id);
  return processOrders(orders);
}
```

## 6. Testing and Quality

### Dependency Injection for Testability

```typescript
interface PaymentGateway {
  charge(amount: number): Promise<boolean>;
}

class PaymentProcessor {
  constructor(private gateway: PaymentGateway) {}
  
  async processPayment(amount: number): Promise<boolean> {
    if (amount <= 0) throw new Error('Amount must be positive');
    return this.gateway.charge(amount);
  }
}

// Easy to test with mock
const mockGateway: PaymentGateway = {
  charge: jest.fn().mockResolvedValue(true),
};
const processor = new PaymentProcessor(mockGateway);
```

### Type Guards for Runtime Checking

```typescript
interface Cat {
  meow(): void;
}

interface Dog {
  bark(): void;
}

function isCat(pet: Cat | Dog): pet is Cat {
  return 'meow' in pet;
}

function makeSound(pet: Cat | Dog) {
  if (isCat(pet)) {
    pet.meow(); // TypeScript knows it's Cat
  } else {
    pet.bark(); // TypeScript knows it's Dog
  }
}
```

## 7. Performance Considerations

### Type-Only Imports

```typescript
// Good - type stripped at compile time, better tree-shaking
import type { User, Order } from './types';
import { fetchUser } from './api';

// Also good for re-exports
export type { User, Order };
```

### Const Assertions for Literal Types

```typescript
// Creates readonly tuple with literal types
const colors = ['red', 'green', 'blue'] as const;
type Color = typeof colors[number]; // "red" | "green" | "blue"

// Works for objects too
const config = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```

### Avoid Excessive Type Complexity

```typescript
// Bad - deeply nested mapped types slow compilation
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object
    ? DeepReadonly<T[K]>
    : T[K];
};

// Consider simpler alternatives or use sparingly
```

## 8. Handle Null/Undefined Properly

### Optional Chaining and Nullish Coalescing

```typescript
// Good - safe property access
function getLength(str: string | null): number {
  return str?.length ?? 0;
}

// Good - safe method calls
const result = user?.getProfile?.()?.name ?? 'Anonymous';

// Good - default values only for null/undefined
const port = config.port ?? 3000; // 0 is valid, won't use default
```

### Discriminated Unions for State

```typescript
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function renderState<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'idle':
      return 'Ready';
    case 'loading':
      return 'Loading...';
    case 'success':
      return state.data; // TypeScript knows data exists
    case 'error':
      return state.error.message; // TypeScript knows error exists
  }
}
```

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Overusing `any` | Defeats type checking | Use `unknown`, generics, or proper types |
| Not using strict mode | Misses many errors | Enable `"strict": true` |
| Redundant annotations | Clutters code | Trust type inference |
| Ignoring union types | Runtime errors | Use type guards |
| Not handling null | Crashes | Use `?.` and `??` operators |
| Nested conditionals | Hard to read | Use guard clauses |

## Quick Reference

```typescript
// Type inference - let TS do the work
const name = 'Alice';

// Explicit for APIs
function greet(name: string): string { ... }

// Unknown over any
function safe(data: unknown) { ... }

// Type-only imports
import type { User } from './types';

// Const assertions
const tuple = [1, 2] as const;

// Null safety
const len = str?.length ?? 0;

// Guard clauses
if (!valid) throw new Error();
// main logic...
```

## References

- [W3Schools TypeScript Best Practices](https://www.w3schools.com/typescript/typescript_best_practices.php)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)
- [TypeScript Performance Wiki](https://github.com/microsoft/TypeScript/wiki/Performance)
