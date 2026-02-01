---
name: typescript-guardian
description:
  Enforces TypeScript strict mode compliance, eliminates any types, ensures type
  safety, and maintains strict linting standards. Use when TypeScript errors
  occur, any types need elimination, or strict mode compliance is required.
---

# TypeScript Guardian

## Quick Start

This skill enforces TypeScript strict mode and type safety:

1. **Strict mode compliance**: Verify all strict flags enabled
2. **Any type elimination**: Replace `any` with specific types, `unknown`, or
   generics
3. **Return type annotations**: Add explicit return types to all functions
4. **Type narrowing**: Implement type guards and predicates

### When to Use

- TypeScript compiler errors need resolution
- `any` types detected in production code
- Missing return type annotations
- Strict mode violations (unchecked index access, null/undefined)

## Strict Mode Configuration

Current `tsconfig.json` requirements (already enforced):

```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "strictNullChecks": true,
    "noImplicitAny": true,
    "strictFunctionTypes": true
  }
}
```

Verification commands:

```bash
# Check for TypeScript errors
npx tsc --noEmit

# Run type-aware linting
npm run lint:ci
```

## Common Violations & Fixes

### 1. Implicit Any

```typescript
// ❌ Implicit any
function process(data) {
  return data.value;
}

// ✅ Explicit types
function process(data: { value: string }): string {
  return data.value;
}
```

### 2. Unchecked Index Access

```typescript
// ❌ No check for undefined
const users = ['Alice', 'Bob'];
const firstUser = users[0]; // string | undefined
console.log(firstUser.toUpperCase()); // Runtime error if empty

// ✅ Check for undefined
const firstUser = users[0];
if (firstUser !== undefined) {
  console.log(firstUser.toUpperCase());
}

// ✅ Or use optional chaining
console.log(users[0]?.toUpperCase());
```

### 3. Null/Undefined Not Checked

```typescript
// ❌ Assuming value exists
interface User {
  profile?: { name: string };
}

function greet(user: User): string {
  return `Hello, ${user.profile.name}`; // Error: profile might be undefined
}

// ✅ Check for existence
function greet(user: User): string {
  if (user.profile === undefined) {
    return 'Hello, stranger';
  }
  return `Hello, ${user.profile.name}`;
}

// ✅ Or use optional chaining
function greet(user: User): string {
  return `Hello, ${user.profile?.name ?? 'stranger'}`;
}
```

## Any Type Elimination

### Detection Strategy

```bash
# Find any types in source code
grep -r ": any" src/ --include="*.ts" --include="*.tsx" --exclude="*.test.ts"

# Find any[] array types
grep -r ": any\\[\\]" src/

# Find type assertions with any
grep -r "as any" src/
```

ESLint enforces these rules (already configured):

- `@typescript-eslint/no-explicit-any`: error
- `@typescript-eslint/no-unsafe-assignment`: error
- `@typescript-eslint/no-unsafe-call`: error

### Replacement Patterns

**Replace Any with Unknown**:

```typescript
// ❌ any (no type safety)
function processData(data: any): void {
  console.log(data.value);
}

// ✅ unknown (requires type narrowing)
function processData(data: unknown): void {
  if (typeof data === 'object' && data !== null && 'value' in data) {
    console.log((data as { value: string }).value);
  }
}

// ✅ Best: specific type
interface Data {
  value: string;
}
function processData(data: Data): void {
  console.log(data.value);
}
```

**Replace Any with Generic**:

```typescript
// ❌ any loses type information
function identity(value: any): any {
  return value;
}

// ✅ Generic preserves type
function identity<T>(value: T): T {
  return value;
}
```

**Replace Any with Union Type**:

```typescript
// ❌ any accepts anything
function format(value: any): string {
  return String(value);
}

// ✅ Union type is specific
function format(value: string | number | boolean): string {
  return String(value);
}
```

**Replace Any with Type Predicate**:

```typescript
// ❌ any in type guard
function isString(value: any): boolean {
  return typeof value === 'string';
}

// ✅ Type predicate with unknown
function isString(value: unknown): value is string {
  return typeof value === 'string';
}
```

## Return Type Annotations

ALWAYS add explicit return types (enforced by ESLint):

```typescript
// ❌ Missing return type
function getUser(id: string) {
  return db.query('SELECT * FROM users WHERE id = ?', [id]);
}

// ✅ Explicit return type
function getUser(id: string): Promise<User | null> {
  return db.query('SELECT * FROM users WHERE id = ?', [id]);
}

// ✅ Void for no return
function logError(error: Error): void {
  console.error('Error:', error.message);
}

// ✅ Never for functions that don't return
function throwError(message: string): never {
  throw new Error(message);
}
```

## Type Narrowing Patterns

### Type Guards

```typescript
// User-defined type guard
function isUser(value: unknown): value is User {
  return (
    typeof value === 'object' &&
    value !== null &&
    'id' in value &&
    'name' in value &&
    typeof (value as User).id === 'string' &&
    typeof (value as User).name === 'string'
  );
}

// Usage
function processData(data: unknown): void {
  if (isUser(data)) {
    console.log(data.name); // data is User here
  }
}
```

### Discriminated Unions

```typescript
// Result type with discriminated union
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

function handleResult<T>(result: Result<T>): T {
  if (result.success) {
    return result.data; // TypeScript knows this is success branch
  } else {
    throw result.error; // TypeScript knows this is error branch
  }
}
```

### Assertion Functions

```typescript
// Assert function (throws if condition fails)
function assertDefined<T>(
  value: T | null | undefined,
  message = 'Value is null or undefined',
): asserts value is T {
  if (value === null || value === undefined) {
    throw new Error(message);
  }
}

// Usage
function process(user: User | null): void {
  assertDefined(user, 'User not found');
  console.log(user.name); // user is User here
}
```

## Generic Constraints

```typescript
// ❌ Unconstrained generic
function merge<T>(obj1: T, obj2: T): T {
  return { ...obj1, ...obj2 }; // Error: Spread requires object
}

// ✅ Constrained to objects
function merge<T extends object>(obj1: T, obj2: T): T {
  return { ...obj1, ...obj2 };
}

// ✅ More specific constraint
function merge<T extends Record<string, unknown>>(
  obj1: T,
  obj2: Partial<T>,
): T {
  return { ...obj1, ...obj2 };
}
```

## Workflow

### Phase 1: Analysis

1. Run `tsc --noEmit` to find errors
2. Scan for `any` types: `grep -r ": any" src/`
3. Identify missing return types
4. Prioritize by severity (compiler errors first)

### Phase 2: Remediation

1. Replace `any` with `unknown` or specific types
2. Add explicit return type annotations
3. Fix null/undefined handling with guards
4. Add type narrowing where needed

### Phase 3: Validation

1. Run `tsc --noEmit` (must pass)
2. Run `npm run lint:ci` (must pass)
3. Verify zero `any` types remain
4. Check all functions have return types

## Common Issues

**Array index flagged as potentially undefined**

- Solution: Check for undefined or use optional chaining

**Object property access on potentially null/undefined**

- Solution: Use optional chaining and nullish coalescing:
  `user?.profile?.name ?? 'Unknown'`

**Function parameters inferred as any**

- Solution: Add explicit type annotations:
  `function process(data: { value: string })`

**Type assertion needed for external library**

- Solution: Create type definition file in `types/` directory

## Best Practices

**Prefer Unknown Over Any**:

```typescript
// ✅ unknown requires type narrowing
function parse(json: string): unknown {
  return JSON.parse(json);
}
```

**Use Type Assertions Sparingly**:

```typescript
// ⚠️ Type assertion (use only when certain)
const user = data as User;

// ✅ Type guard with runtime check
if (isUser(data)) {
  const user = data; // Type narrowed safely
}
```

**Document Complex Types**:

```typescript
/**
 * Result type for async operations
 * @typeParam T - Success value type
 * @typeParam E - Error type (defaults to Error)
 */
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
```

## Success Criteria

- Zero TypeScript compiler errors
- Zero ESLint type errors
- No `any` types in production code
- All functions have explicit return types
- Strict mode compliance: 100%

## References

- TypeScript Strict Mode: https://www.typescriptlang.org/tsconfig#strict
- ESLint TypeScript Plugin: https://typescript-eslint.io/
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/intro.html
