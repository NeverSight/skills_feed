---
name: typescript-master
description: TypeScript language expert specializing in type system, generics, conditional types, and advanced patterns. Use when writing complex types, debugging type errors, or designing type-safe APIs.
---

# TypeScript Language Expert

Expert assistant for TypeScript type system mastery including generics, conditional types, mapped types, type inference, and advanced patterns.

## How It Works

1. Analyzes TypeScript code or type requirements
2. Designs type-safe solutions
3. Provides solutions with minimal type annotations (prefer inference)
4. Uses `unknown` over `any`
5. Leverages discriminated unions for safety

## Usage

### Run Type Check

```bash
bash /mnt/skills/user/typescript-master/scripts/type-check.sh [project-dir] [strict-mode]
```

**Arguments:**
- `project-dir` - Project directory (default: current directory)
- `strict-mode` - Enable strict checks: true/false (default: true)

**Examples:**
```bash
bash /mnt/skills/user/typescript-master/scripts/type-check.sh
bash /mnt/skills/user/typescript-master/scripts/type-check.sh ./my-project
bash /mnt/skills/user/typescript-master/scripts/type-check.sh ./my-project false
```

**Checks:**
- TypeScript compilation (noEmit)
- Strict type checking
- Unused variables/imports
- tsconfig recommendations

## Documentation Resources

**Official Documentation:**
- TypeScript Handbook: `https://www.typescriptlang.org/docs/handbook/`
- Type Challenges: `https://github.com/type-challenges/type-challenges`

## Type System Fundamentals

### Utility Types

```typescript
// Built-in utilities
type Partial<T> = { [P in keyof T]?: T[P] };
type Required<T> = { [P in keyof T]-?: T[P] };
type Readonly<T> = { readonly [P in keyof T]: T[P] };
type Pick<T, K extends keyof T> = { [P in K]: T[P] };
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;
type Record<K extends keyof any, T> = { [P in K]: T };
```

### Custom Utility Types

```typescript
// Deep Partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Strict Omit (only known keys)
type StrictOmit<T, K extends keyof T> = Pick<T, Exclude<keyof T, K>>;

// Make specific keys required
type RequireKeys<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Nullable
type Nullable<T> = T | null;
```

## Generics Patterns

### Constrained Generics

```typescript
// Key constraint
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// Type constraint
function merge<T extends object, U extends object>(a: T, b: U): T & U {
  return { ...a, ...b };
}
```

### Inference with infer

```typescript
// Extract return type
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;

// Extract promise value
type Awaited<T> = T extends Promise<infer U> ? Awaited<U> : T;

// Extract array element
type ArrayElement<T> = T extends (infer E)[] ? E : never;

// Extract function parameters
type Parameters<T> = T extends (...args: infer P) => any ? P : never;
```

## Conditional Types

### Basic Conditional

```typescript
type IsString<T> = T extends string ? true : false;
type IsArray<T> = T extends any[] ? true : false;
```

### Distributive Conditional

```typescript
// Distributes over union
type ToArray<T> = T extends any ? T[] : never;
type Result = ToArray<string | number>; // string[] | number[]

// Prevent distribution
type ToArrayNonDist<T> = [T] extends [any] ? T[] : never;
type Result2 = ToArrayNonDist<string | number>; // (string | number)[]
```

## Discriminated Unions

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>): T | null {
  if (result.success) {
    return result.data; // TypeScript knows data exists
  } else {
    console.error(result.error); // TypeScript knows error exists
    return null;
  }
}
```

## Type Guards

```typescript
// Custom type guard
function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    typeof (obj as User).id === 'string'
  );
}

// Assertion function
function assertNonNull<T>(
  value: T,
  message?: string
): asserts value is NonNullable<T> {
  if (value === null || value === undefined) {
    throw new Error(message ?? 'Value is null or undefined');
  }
}
```

## Template Literal Types

```typescript
type EventName = 'click' | 'focus' | 'blur';
type Handler = `on${Capitalize<EventName>}`;
// "onClick" | "onFocus" | "onBlur"

type PropKey<T extends string> = `get${Capitalize<T>}` | `set${Capitalize<T>}`;
type NameProps = PropKey<'name'>; // "getName" | "setName"
```

## Recommended tsconfig

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noPropertyAccessFromIndexSignature": true,
    "moduleResolution": "bundler",
    "verbatimModuleSyntax": true
  }
}
```

## Present Results to User

When providing TypeScript solutions:
- Prefer type inference over explicit annotations
- Use `unknown` instead of `any`
- Leverage discriminated unions
- Provide type test examples
- Note TypeScript version features (5.0+: const type parameters)

## Troubleshooting

**"Type 'X' is not assignable to type 'Y'"**
- Check for missing properties
- Verify nullability handling
- Look for literal vs widened types

**"Property does not exist on type"**
- Add type guard before access
- Check if property is optional
- Verify union type narrowing

**"Excessive type complexity"**
- Break into smaller types
- Use intermediate type aliases
- Consider simplifying generics
