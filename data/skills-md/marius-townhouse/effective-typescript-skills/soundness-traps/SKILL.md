---
name: soundness-traps
description: Use when types don't match runtime values. Use when TypeScript misses errors. Use when understanding type system limits.
---

# Avoid Soundness Traps

## Overview

**TypeScript is not sound - runtime values can diverge from static types.**

"Soundness" means static types always match runtime values. TypeScript intentionally trades some soundness for convenience. Know the common traps.

## When to Use This Skill

- Debugging "impossible" runtime errors
- Understanding TypeScript's limitations
- Writing defensive code
- Evaluating trade-offs of strict options

## The Iron Rule

```
TypeScript types are NOT runtime guarantees.
Know the common soundness traps and avoid them.
```

**Remember:**
- Array access doesn't check bounds
- Type assertions bypass checking
- Functions can mutate their parameters
- External data may not match declared types

## Soundness vs Convenience

TypeScript chooses convenience over soundness in many cases:

```typescript
const xs = [1, 2, 3];
const x = xs[10];
//    ^? number (but actually undefined!)
```

This is unsound but convenient. Checking bounds at every access would be tedious.

## Common Soundness Traps

### 1. Unchecked Array Access

```typescript
const arr = [1, 2, 3];
const item = arr[5];  // undefined at runtime
//    ^? number (wrong!)

item.toFixed(2);  // Crashes!
```

**Fix:** Use `noUncheckedIndexedAccess` or check explicitly:

```typescript
const item = arr[5];
if (item !== undefined) {
  item.toFixed(2);  // OK
}
```

### 2. Type Assertions

```typescript
const hour = (new Date()).getHours() || null;
//    ^? number | null

// Assertion removes null
const definitelyHour = hour as number;
//    ^? number (but might be null!)
```

**Fix:** Use conditionals instead of assertions:

```typescript
if (hour !== null) {
  hour.toFixed(1);  // TypeScript knows it's number
}
```

### 3. any Types

```typescript
function log(x: number) {
  console.log(x.toFixed(1));
}

const val: any = 'not a number';
log(val);  // No error, crashes at runtime
```

**Fix:** Avoid `any`. Use `unknown` with narrowing:

```typescript
function log(x: unknown) {
  if (typeof x === 'number') {
    console.log(x.toFixed(1));
  }
}
```

### 4. Object Index Access

```typescript
type Dict = { [key: string]: string };
const dict: Dict = { a: 'apple' };
const val = dict['b'];
//    ^? string (but actually undefined!)
```

**Fix:** Include undefined in the type:

```typescript
type Dict = { [key: string]: string | undefined };
const val = dict['b'];
//    ^? string | undefined
```

### 5. Function Parameter Mutation

```typescript
function addFox(animals: Animal[]) {
  animals.push(new Fox());
}

const hens: Hen[] = [new Hen()];
addFox(hens);  // Fox in the henhouse!
```

**Fix:** Use readonly to prevent mutation:

```typescript
function addFox(animals: readonly Animal[]) {
  animals.push(new Fox());
  //      ~~~~ Property 'push' does not exist
}
```

### 6. Refinements Invalidated by Callbacks

```typescript
interface Data {
  value?: string;
}

function process(data: Data, callback: (d: Data) => void) {
  if (data.value) {
    callback(data);
    console.log(data.value.toUpperCase());  // Might crash!
    //          ^? string (but callback might have deleted it!)
  }
}

process({ value: 'hello' }, d => delete d.value);
```

**Fix:** Capture the value before the callback:

```typescript
function process(data: Data, callback: (d: Data) => void) {
  const value = data.value;
  if (value) {
    callback(data);
    console.log(value.toUpperCase());  // Safe!
  }
}
```

### 7. Inaccurate Type Declarations

```typescript
// Library types might be wrong
declare function getUser(): { name: string; email: string };

const user = getUser();
user.email.toLowerCase();  // Might crash if email is undefined!
```

**Fix:** Validate external data at runtime:

```typescript
const user = getUser();
if (user.email) {
  user.email.toLowerCase();
}
```

### 8. Optional Properties and Assignability

```typescript
interface Person { name: string; }
interface AgePerson { name: string; age?: number; }

const p: Person = { name: 'Bob', age: '30' };  // age is string
const ap: AgePerson = p;  // No error!
console.log(ap.age?.toFixed());  // toFixed on string!
```

This is a subtle unsoundness from TypeScript's structural typing.

## Compiler Options for Soundness

| Option | What It Catches |
|--------|-----------------|
| `strictNullChecks` | null/undefined assignments |
| `noUncheckedIndexedAccess` | Array/object access returning undefined |
| `strictFunctionTypes` | Function parameter contravariance |

Enable these for more safety (at cost of convenience).

## General Strategies

1. **Validate external data** (APIs, JSON, user input)
2. **Use readonly for parameters** you don't mutate
3. **Prefer unknown to any**
4. **Avoid type assertions**; use narrowing instead
5. **Enable strict compiler options**
6. **Test edge cases** (empty arrays, missing properties)

## Pressure Resistance Protocol

### 1. "TypeScript Should Catch This"

**Pressure:** "Why didn't TypeScript catch this bug?"

**Response:** TypeScript is intentionally unsound in many cases.

**Action:** Know the traps; write defensive code.

### 2. "It's Too Strict"

**Pressure:** "noUncheckedIndexedAccess is annoying"

**Response:** It catches real bugs. The friction is worth it.

**Action:** Enable strict options; handle the edge cases.

## Red Flags - STOP and Reconsider

- Accessing array elements without bounds checking
- Type assertions to "fix" type errors
- Mutating function parameters
- Trusting external data matches declared types

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "TypeScript will catch it" | TypeScript is not sound |
| "It always has a value" | Until it doesn't |
| "The API is well-documented" | Docs lie; validate |

## Quick Reference

```typescript
// TRAP: Array access
const x = arr[10];  // Might be undefined

// TRAP: Type assertion
const y = val as number;  // Might not be number

// TRAP: any type
const z: any = 'string';
z.toFixed();  // Crashes

// TRAP: Index signature
const v = dict['missing'];  // Undefined

// SAFE: Narrowing
if (typeof val === 'number') { val.toFixed(); }

// SAFE: Optional chaining
arr[10]?.toFixed();

// SAFE: undefined in type
type Dict = { [k: string]: string | undefined };
```

## The Bottom Line

**TypeScript is convenient, not sound.**

Know where types can diverge from runtime values. Enable strict options. Validate external data. Write defensive code. Don't trust types blindly.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 48: Avoid Soundness Traps.
