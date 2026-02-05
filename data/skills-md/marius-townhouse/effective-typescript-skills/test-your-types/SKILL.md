---
name: test-your-types
description: Use when writing type declarations. Use when authoring libraries. Use when refactoring type utilities. Use when types and implementation are separate. Use when types contain complex logic.
---

# Write Tests for Your Types

## Overview

Just as you write tests for runtime code, you should write tests for your types. Type-level code can have bugs too, and type declarations can drift out of sync with implementations. Testing types ensures your declarations work correctly and catch the errors they should.

Type testing is particularly important for library authors, complex type utilities, and whenever types are defined separately from implementations.

## When to Use This Skill

- Writing type declarations for libraries
- Creating complex type utilities
- Types and implementation are in separate files
- Refactoring type-level code
- Types contain conditional logic or recursion

## The Iron Rule

**Write tests for your types. Test that valid types work, invalid types fail, and the error messages are helpful.**

## Detection

Watch for these situations:

```typescript
// RED FLAGS - Untested type logic
type ComplexTransform<T> = /* 10 lines of conditional types */;
// No tests - how do you know it works?

declare function libraryFn<T>(input: T): SomeTransform<T>;
// Implementation in JS, types in d.ts - can drift apart
```

## What to Test

Test three things:
1. **Valid types work** - Expected types are produced
2. **Invalid types fail** - Type errors occur where expected
3. **Error messages help** - Errors guide users to fixes

## Testing with @ts-expect-error

Use `@ts-expect-error` to assert that a line should produce a type error:

```typescript
// myFunction.test.ts
import { myFunction } from './myFunction';

// Test 1: Valid types work
const result1 = myFunction('hello');
type Test1 = typeof result1;  // Should be string

// Test 2: Invalid types fail
// @ts-expect-error - number not assignable to string
const result2 = myFunction(42);

// Test 3: Error message is helpful
// When the error goes away, TypeScript warns:
// "Unused '@ts-expect-error' directive"
```

## Testing Type Utilities

```typescript
// type-utils.ts
export type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object 
    ? DeepReadonly<T[K]> 
    : T[K];
};

// type-utils.test.ts
import type { DeepReadonly } from './type-utils';

// Test: Simple object
type Case1 = DeepReadonly<{ x: number }>;
const test1: Case1 = { x: 1 };
// @ts-expect-error - readonly
test1.x = 2;

// Test: Nested object
type Case2 = DeepReadonly<{ nested: { value: string } }>;
const test2: Case2 = { nested: { value: 'hi' } };
// @ts-expect-error - deeply readonly
// @ts-expect-error - deeply readonly
test2.nested.value = 'bye';

// Test: Arrays
type Case3 = DeepReadonly<string[]>;
const test3: Case3 = ['a', 'b'];
// @ts-expect-error - readonly array
test3.push('c');
```

## Testing with expect-type

The `expect-type` library provides type assertion helpers:

```typescript
import { expectType, expectError } from 'expect-type';

// Test return types
const result = myFunction('input');
expectType<string>(result);

// Test that errors occur
expectError(myFunction(42));

// Test complex types
interface User { name: string; }
const user = fetchUser();
expectType<User>(user);
```

## Testing with tsd

`tsd` is a CLI tool for testing type definitions:

```typescript
// index.test-d.ts
import { expectType, expectError } from 'tsd';
import { concat } from '.';

// Test: string + string = string
expectType<string>(concat('foo', 'bar'));

// Test: number + number = number  
expectType<number>(concat(1, 2));

// Test: mixed types = error
expectError(concat('foo', 1));
```

Run with: `npx tsd`

## Testing with Vitest

Vitest has built-in type testing:

```typescript
// test/types.test-d.ts
import { describe, expectTypeOf, it } from 'vitest';
import { pick } from './utils';

describe('pick', () => {
  it('should pick specified keys', () => {
    const obj = { a: 1, b: 2, c: 3 };
    const picked = pick(obj, 'a', 'b');
    
    expectTypeOf(picked).toEqualTypeOf<{ a: number; b: number }>();
  });
  
  it('should not allow unpicked keys', () => {
    const obj = { a: 1, b: 2 };
    const picked = pick(obj, 'a');
    
    // @ts-expect-error - 'b' was not picked
    picked.b;
  });
});
```

Run with: `npx vitest typecheck`

## Testing Error Messages

Good error messages are part of the API:

```typescript
// Test that error messages are helpful
type Check<T> = T extends string ? T : never;

// Bad: Error is just "Type 'number' is not assignable to type 'never'"
type Bad = Check<number>;

// Better: Use meaningful type names
type CheckWithMessage<T> = T extends string 
  ? T 
  : 'Error: Expected string, received something else';
```

## Testing Edge Cases

```typescript
// Test with unions
type UnionTest = MyType<string | number>;
// Should distribute: MyType<string> | MyType<number>

// Test with never
type NeverTest = MyType<never>;
// Should handle never gracefully

// Test with any
type AnyTest = MyType<any>;
// Should not crash or produce unexpected results

// Test with complex objects
type ComplexTest = MyType<{ a: { b: { c: string } } }>;
// Should handle nesting correctly
```

## Pressure Resistance Protocol

When pressured to skip type tests:

1. **Show the risk**: Untested types can have subtle bugs
2. **Start simple**: `@ts-expect-error` tests are easy to add
3. **Automate**: Add type tests to CI pipeline
4. **Document**: Tests serve as documentation for complex types

## Red Flags

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| No type tests for complex utilities | Bugs go unnoticed |
| Only testing happy paths | Edge cases break |
| Types in separate file from tests | Can drift apart |
| Manual testing in IDE | Not reproducible |

## Common Rationalizations

### "The type checker will catch errors"

**Reality**: The type checker validates against your types, but doesn't validate that your types are correct. Only tests can do that.

### "It's just types, not real code"

**Reality**: Types are code that runs at compile time. Complex type logic needs testing just like runtime logic.

### "I'll notice if something breaks"

**Reality**: Type bugs are subtle. You might not notice until users report issues.

## Quick Reference

| Tool | Best For | Command |
|------|----------|---------|
| @ts-expect-error | Quick tests, inline | Built-in |
| expect-type | Unit test style | `npm test` |
| tsd | Library definitions | `npx tsd` |
| Vitest | Full test suite | `npx vitest typecheck` |
| dtslint | DefinitelyTyped | `npx dtslint` |

## The Bottom Line

Types are code and need tests. Use `@ts-expect-error` for quick checks, dedicated libraries for comprehensive testing. Test valid cases, invalid cases, and error messages.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 55: Write Tests for Your Types
