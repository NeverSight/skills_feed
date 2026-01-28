---
name: typescript-best-practices
description: Apply TypeScript best practices when writing or reviewing TypeScript code, including strict typing, generics, error handling, and common patterns.
---

# TypeScript Best Practices

## When to Apply

Apply these rules when:
- Writing new TypeScript code
- Reviewing TypeScript code
- Refactoring JavaScript to TypeScript
- Fixing type errors
- Optimizing type definitions

## Core Rules

### 1. Avoid `any` - Use Proper Types

**Never use `any`** unless absolutely necessary. Instead:
- Use `unknown` for truly unknown types
- Use generics for flexible typing
- Use union types for multiple possibilities

```typescript
// BAD
function parse(data: any): any { ... }

// GOOD
function parse<T>(data: unknown): T | null { ... }
```

### 2. Enable Strict Mode

Always use strict TypeScript configuration:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noImplicitReturns": true
  }
}
```

### 3. Use Type Guards for Runtime Checks

```typescript
// Type guard function
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value
  );
}

// Usage
if (isUser(data)) {
  console.log(data.name); // TypeScript knows it's User
}
```

### 4. Prefer Interfaces for Objects, Types for Unions

```typescript
// Use interface for object shapes
interface User {
  id: string;
  name: string;
  email: string;
}

// Use type for unions and complex types
type Status = 'pending' | 'active' | 'inactive';
type Result<T> = { success: true; data: T } | { success: false; error: Error };
```

### 5. Use Readonly for Immutable Data

```typescript
interface Config {
  readonly apiUrl: string;
  readonly timeout: number;
}

// Or use Readonly utility
type ImmutableUser = Readonly<User>;
```

### 6. Leverage Utility Types

```typescript
// Partial - all properties optional
type UserUpdate = Partial<User>;

// Pick - select specific properties
type UserPreview = Pick<User, 'id' | 'name'>;

// Omit - exclude properties
type UserWithoutEmail = Omit<User, 'email'>;

// Record - typed object maps
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;
```

### 7. Type-Safe Error Handling

```typescript
// Define error types
class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number
  ) {
    super(message);
    this.name = 'AppError';
  }
}

// Result pattern
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function divide(a: number, b: number): Result<number> {
  if (b === 0) {
    return { ok: false, error: new Error('Division by zero') };
  }
  return { ok: true, value: a / b };
}
```

### 8. Use Generics for Reusable Code

```typescript
// Generic function
function first<T>(array: T[]): T | undefined {
  return array[0];
}

// Generic with constraints
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Generic interface
interface Repository<T> {
  find(id: string): Promise<T | null>;
  save(entity: T): Promise<T>;
  delete(id: string): Promise<boolean>;
}
```

### 9. Const Assertions for Literal Types

```typescript
// Without as const - type is string[]
const colors = ['red', 'green', 'blue'];

// With as const - type is readonly ['red', 'green', 'blue']
const colors = ['red', 'green', 'blue'] as const;
type Color = typeof colors[number]; // 'red' | 'green' | 'blue'
```

### 10. Discriminated Unions for State

```typescript
type AsyncState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

function render<T>(state: AsyncState<T>) {
  switch (state.status) {
    case 'idle':
      return 'Ready';
    case 'loading':
      return 'Loading...';
    case 'success':
      return `Data: ${state.data}`; // TypeScript knows data exists
    case 'error':
      return `Error: ${state.error.message}`; // TypeScript knows error exists
  }
}
```

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Interface | PascalCase | `UserProfile` |
| Type alias | PascalCase | `RequestConfig` |
| Enum | PascalCase | `HttpStatus` |
| Enum member | UPPER_SNAKE or PascalCase | `HTTP_OK` or `HttpOk` |
| Generic | Single uppercase letter or descriptive | `T`, `TData`, `TResponse` |
| Function | camelCase | `getUserById` |
| Variable | camelCase | `userList` |
| Constant | UPPER_SNAKE or camelCase | `MAX_RETRIES` or `maxRetries` |

## Anti-Patterns to Avoid

1. **Don't use `any` as escape hatch** - Use `unknown` and narrow the type
2. **Don't use `!` non-null assertion** - Check for null/undefined properly
3. **Don't use `@ts-ignore`** - Fix the type error instead
4. **Don't export everything** - Only export what's needed
5. **Don't use `Function` type** - Use specific function signatures
