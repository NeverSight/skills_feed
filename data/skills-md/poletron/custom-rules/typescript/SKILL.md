---
name: typescript
description: >
  TypeScript strict patterns, type safety, and best practices.
  Trigger: When writing TypeScript code with types, interfaces, or generics.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with typescript"

## When to Use

Use this skill when:
- Writing TypeScript in .ts/.tsx files
- Defining types, interfaces, or generics
- Removing `any` types or tightening `unknown`
- Using utility types or type guards

---

## Critical Patterns

### Const Types Pattern (REQUIRED)

```typescript
// ✅ ALWAYS: Create const object first, then extract type
const STATUS = {
  ACTIVE: "active",
  INACTIVE: "inactive",
  PENDING: "pending",
} as const;

type Status = (typeof STATUS)[keyof typeof STATUS];

// ❌ NEVER: Direct union types
type Status = "active" | "inactive" | "pending";
```

### Flat Interfaces (REQUIRED)

```typescript
// ✅ ALWAYS: One level depth, nested objects → dedicated interface
interface UserAddress {
  street: string;
  city: string;
}

interface User {
  id: string;
  name: string;
  address: UserAddress;  // Reference, not inline
}

// ❌ NEVER: Inline nested objects
interface User {
  address: { street: string; city: string };  // NO!
}
```

### Never Use `any` (REQUIRED)

```typescript
// ✅ Use unknown for truly unknown types
function parse(input: unknown): User {
  if (isUser(input)) return input;
  throw new Error("Invalid input");
}

// ✅ Use generics for flexible types
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

// ❌ NEVER
function parse(input: any): any { }
```

---

## Decision Tree

```
Need a set of constants?    → Use const object + typeof
Need optional fields?       → Use Partial<T>
Need to pick fields?        → Use Pick<T, K>
Need to exclude fields?     → Use Omit<T, K>
Need runtime type check?    → Create type guard function
Need to extract type?       → Use ReturnType<typeof fn>
```

---

## Code Examples

### Type Guards

```typescript
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value
  );
}
```

### Utility Types

```typescript
Pick<User, "id" | "name">     // Select fields
Omit<User, "id">              // Exclude fields
Partial<User>                 // All optional
Required<User>                // All required
Record<string, User>          // Object type
NonNullable<T | null>         // Remove null/undefined
ReturnType<typeof fn>         // Function return type
```

### Import Types

```typescript
import type { User } from "./types";
import { createUser, type Config } from "./utils";
```

---

## Commands

```bash
npx tsc --noEmit              # Type check without emit
npx tsc --init                # Initialize tsconfig.json
npx tsc -w                    # Watch mode
```

---

## Resources

Specialized TypeScript documentation:
- **Best Practices**: [best-practices.md](best-practices.md)
- **Type Safety**: [type-safety.md](type-safety.md)
- **NestJS Integration**: [nestjs.md](nestjs.md)
- **Node.js Patterns**: [node.md](node.md)
