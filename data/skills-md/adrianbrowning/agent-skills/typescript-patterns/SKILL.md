---
name: typescript-patterns
description: Best practices for TypeScript types, interfaces, assertions, and type safety. Use when writing or reviewing TypeScript code.
---

# TypeScript Patterns Skill

Best practices for types, interfaces, assertions, and type safety.

## Type Inference Over Explicit Returns
```typescript
// ✅ Inferred return type
function calculateTotal(items: OrderItem[]) {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// ❌ Explicit return type
function calculateTotal(items: OrderItem[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

**Why:** Inference catches implicit type coercion bugs.

## Runtime Type Assertions

Never hard cast from `JSON.parse`. Validate at runtime.
```typescript
// ❌ Hard cast
const value: MyType = JSON.parse(message);

// ✅ Runtime assertion
function isMyType(value: unknown): value is MyType {
    return typeof value === 'object' &&
        value !== null &&
        typeof (<MyType>value).prop === 'string';
}

const value = JSON.parse(message);
assert(isMyType(value), 'Invalid message format');
```

## Type Assertion Functions
```typescript
// Parameter: 'value' with 'unknown' type
// Always return boolean, never throw
function isStrategy(value: unknown): value is Strategy {
    return typeof value === 'object' &&
        value !== null &&
        typeof (<Strategy>value).name === 'string';
}

// Use with assert
assert(isStrategy(value), 'Value is not a valid Strategy');
```

## Types vs Interfaces

**Always prefer types unless explicitly told otherwise.**

```typescript
// ✅ Type for object shapes
export type Product = {
    id: string;
    name: string;
    price: number;
};

// ✅ Type for local function-scoped types
function validate(input: unknown) {
    type Result = { errors: string[]; valid: boolean };
    const output: Result = { errors: [], valid: true };
    // ...
}

// ✅ Type for unions
type Status = 'pending' | 'active' | 'inactive';

// ❌ Interface (only use when explicitly requested)
export interface Product {
    id: string;
    name: string;
}
```

## Casting Syntax
```typescript
// ✅ Angle bracket syntax
const x = <number>y;
const config = <ConfigType>JSON.parse(json);

// ❌ 'as' syntax
const x = y as number;
```

## Interface Conventions (Only When Explicitly Using Interfaces)

**Note:** Only apply these when explicitly told to use interfaces instead of types.

- No `I` prefix or `Data` suffix
- Properties in alphabetical order
- Think of interfaces as nouns or adjectives (Shippable, Refundable)
- When extending, inherit ALL properties (no `Omit`)
```typescript
// Adjective interfaces
interface Shippable {
    shipping_address: string;
    shipping_cost: number;
}

// Concrete interface
interface Order extends Shippable {
    id: string;
    total: number;
}
```

## Constants Over Enums

**Never use enums. Use const objects with `as const` instead.**

```typescript
// ✅ Const object with as const
export const TenantModel = {
    USER: 'user',
    ORGANIZATION: 'organization',
    EMPLOYER: 'employer'
} as const;

// Extract type from const
export type TenantModel = typeof TenantModel[keyof typeof TenantModel];

// ✅ Union type for simple cases
type Status = 'active' | 'inactive';

// ❌ Enum (never use)
export enum TenantModel {
    USER = 'user',
    ORGANIZATION = 'organization'
}

// Validate with Object.values
if (!Object.values(TenantModel).includes(model)) {
    throw new Error('Invalid model');
}
```

## Iteration
```typescript
// ✅ for...of loop
for (const item of items) {
    processItem(item);
}

// ❌ forEach
items.forEach((item) => {
    processItem(item);
});
```

**Why:** `for...of` works with `break`, `continue`, `return`, `await`, and has better debugging/stack traces.

Use `map`/`filter`/`reduce` for transformations, not side effects.

## Import Style
```typescript
// ✅ Namespace imports
import * as mongodb from 'mongodb';
import * as Types from './types/index.js';

// ❌ Default imports
import MongoDB from 'mongodb';
```

## Organization

- Keep types with related code (not in `types/` directories)
- Only export types that are part of public API
- Use `ReturnType` and `Parameters` to access private types