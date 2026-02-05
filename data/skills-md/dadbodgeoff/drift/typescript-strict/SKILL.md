---
name: typescript-strict
description: Configure TypeScript strict mode with additional safety flags. Catch bugs at compile time instead of production. Includes branded types, exhaustive switches, and Result types.
license: MIT
compatibility: TypeScript
metadata:
  category: foundations
  time: 1h
  source: drift-masterguide
---

# TypeScript Strict Mode

Catch errors at build time, not in production.

## When to Use This Skill

- Starting a new TypeScript project
- Tightening an existing codebase
- Preventing `any` types from leaking through
- Want compile-time guarantees for runtime safety

## Core Concepts

1. **Strict mode** - Enables all strict type checks
2. **Index safety** - Array access returns `T | undefined`
3. **Exhaustiveness** - Compiler ensures all cases handled
4. **Branded types** - Prevent mixing up IDs and primitives

## TypeScript Implementation

### tsconfig.json (Strict Configuration)

```json
{
  "compilerOptions": {
    // Target modern JS
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    
    // STRICT MODE - The important part
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "exactOptionalPropertyTypes": true,
    
    // Additional safety
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    
    // Interop
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    
    // Output
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  }
}
```

### What Each Flag Does

| Flag | Effect |
|------|--------|
| `strict` | Enables all strict type checks |
| `noUncheckedIndexedAccess` | `arr[0]` returns `T \| undefined` |
| `noImplicitOverride` | Must use `override` keyword |
| `exactOptionalPropertyTypes` | `undefined` ≠ missing property |
| `noImplicitReturns` | All code paths must return |
| `noFallthroughCasesInSwitch` | Require break/return in switch |

### Path Aliases

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/lib/*": ["./src/lib/*"],
      "@/types/*": ["./src/types/*"]
    }
  }
}
```

```typescript
// Before (fragile)
import { Button } from '../../../components/ui/Button';

// After (clean)
import { Button } from '@/components/ui/Button';
```

## Type Patterns

### Branded Types (Prevent ID Mixups)

```typescript
// types/branded.ts
declare const brand: unique symbol;

type Brand<T, B> = T & { [brand]: B };

export type UserId = Brand<string, 'UserId'>;
export type OrderId = Brand<string, 'OrderId'>;
export type ProductId = Brand<string, 'ProductId'>;

// Helper to create branded values
export const UserId = (id: string) => id as UserId;
export const OrderId = (id: string) => id as OrderId;

// Usage - compiler prevents mixing IDs
function getOrder(id: OrderId): Promise<Order>;
function getUser(id: UserId): Promise<User>;

const userId = UserId('user_123');
const orderId = OrderId('order_456');

getUser(userId);   // ✅ OK
getOrder(orderId); // ✅ OK
getOrder(userId);  // ❌ Type error! Can't use UserId as OrderId
```

### Exhaustive Switch

```typescript
// Ensure all enum cases handled
type Status = 'pending' | 'active' | 'completed' | 'failed';

function getStatusColor(status: Status): string {
  switch (status) {
    case 'pending':
      return 'yellow';
    case 'active':
      return 'blue';
    case 'completed':
      return 'green';
    case 'failed':
      return 'red';
    default:
      // This line ensures exhaustiveness
      const _exhaustive: never = status;
      throw new Error(`Unhandled status: ${_exhaustive}`);
  }
}

// If you add a new status, TypeScript will error until you handle it
```

### Result Type (No Exceptions)

```typescript
// types/result.ts
export type Result<T, E = Error> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

export function ok<T>(value: T): Result<T, never> {
  return { ok: true, value };
}

export function err<E>(error: E): Result<never, E> {
  return { ok: false, error };
}

// Usage
type FetchError = 'NOT_FOUND' | 'NETWORK_ERROR' | 'UNAUTHORIZED';

async function fetchUser(id: string): Promise<Result<User, FetchError>> {
  try {
    const response = await fetch(`/api/users/${id}`);
    
    if (response.status === 404) return err('NOT_FOUND');
    if (response.status === 401) return err('UNAUTHORIZED');
    if (!response.ok) return err('NETWORK_ERROR');
    
    const user = await response.json();
    return ok(user);
  } catch {
    return err('NETWORK_ERROR');
  }
}

// Caller must handle both cases
const result = await fetchUser('123');

if (!result.ok) {
  // TypeScript knows: result.error is FetchError
  switch (result.error) {
    case 'NOT_FOUND':
      return notFound();
    case 'UNAUTHORIZED':
      return redirect('/login');
    case 'NETWORK_ERROR':
      return serverError();
  }
}

// TypeScript knows: result.value is User
console.log(result.value.name);
```

### Type Guards

```typescript
// Type guard function
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'email' in value &&
    typeof (value as User).id === 'string' &&
    typeof (value as User).email === 'string'
  );
}

// Usage with unknown data
function handleWebhook(body: unknown) {
  if (isUser(body)) {
    // TypeScript knows body is User here
    console.log(body.email);
  }
}
```

### Zod for Runtime Validation

```typescript
// schemas/user.ts
import { z } from 'zod';

export const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(['admin', 'user', 'guest']),
  createdAt: z.string().datetime(),
});

// Infer TypeScript type from schema
export type User = z.infer<typeof UserSchema>;

// Validate external data
function handleWebhook(body: unknown): User {
  return UserSchema.parse(body); // Throws ZodError if invalid
}

// Safe parse (no throw)
const result = UserSchema.safeParse(body);
if (!result.success) {
  console.error(result.error.issues);
  return;
}
// result.data is User
```

## Common Strict Mode Fixes

### Fix 1: Array Index Access

```typescript
// ❌ Error with noUncheckedIndexedAccess
const items = ['a', 'b', 'c'];
const first = items[0].toUpperCase(); // items[0] is string | undefined

// ✅ Fix: Optional chaining
const first = items[0]?.toUpperCase();

// ✅ Fix: Check first
const first = items[0];
if (first) {
  console.log(first.toUpperCase());
}

// ✅ Fix: Non-null assertion (when you're certain)
const first = items[0]!.toUpperCase();

// ✅ Fix: Use .at() with check
const first = items.at(0);
if (first !== undefined) {
  console.log(first.toUpperCase());
}
```

### Fix 2: Optional Properties

```typescript
// ❌ Error with exactOptionalPropertyTypes
interface Config {
  timeout?: number;
}
const config: Config = { timeout: undefined }; // Error!

// ✅ Fix: Omit the property
const config: Config = {};

// ✅ Fix: Explicitly allow undefined
interface Config {
  timeout?: number | undefined;
}
```

### Fix 3: Object Index Signature

```typescript
// ❌ Error with noPropertyAccessFromIndexSignature
interface Cache {
  [key: string]: string;
}
const cache: Cache = {};
const value = cache.someKey; // Error: use bracket notation

// ✅ Fix: Use bracket notation
const value = cache['someKey'];
```

### Fix 4: Override Keyword

```typescript
// ❌ Error with noImplicitOverride
class Animal {
  speak() { console.log('...'); }
}

class Dog extends Animal {
  speak() { console.log('Woof!'); } // Error: missing override
}

// ✅ Fix: Add override keyword
class Dog extends Animal {
  override speak() { console.log('Woof!'); }
}
```

## Best Practices

1. **Start strict** - Enable strict mode from day one
2. **No `any`** - Use `unknown` + type guards instead
3. **Validate boundaries** - Use Zod for external data (API, forms)
4. **Branded types** - Prevent ID mixups in domain logic
5. **Result types** - Make error handling explicit

## Common Mistakes

- Using `any` to silence errors (use `unknown` instead)
- Ignoring `noUncheckedIndexedAccess` warnings
- Not validating data at system boundaries
- Mixing up IDs without branded types
- Using `!` non-null assertion without certainty

## Related Skills

- [Environment Config](../environment-config/)
- [Request Validation](../request-validation/)
- [Error Handling](../error-handling/)
