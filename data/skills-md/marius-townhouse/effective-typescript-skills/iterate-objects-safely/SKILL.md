---
name: iterate-objects-safely
description: Use when iterating over object keys and values. Use when for...in loops produce type errors. Use when Object.entries returns any types. Use when dealing with prototype pollution concerns. Use when considering Map vs object.
---

# Know How to Iterate Over Objects

## Overview

Iterating over objects in TypeScript is surprisingly tricky. The `for...in` loop infers keys as `string` rather than the object's keys, leading to indexing errors. This happens because objects can have additional properties beyond their declared type (structural typing), and `for...in` includes inherited properties.

Understanding safe iteration patterns helps you avoid `any` types and type assertions while correctly handling object traversal.

## When to Use This Skill

- Iterating over object keys and values
- `for...in` loops produce "Element implicitly has 'any' type" errors
- `Object.entries` returns `any` value types
- Need to handle both known and unknown object properties
- Considering Map vs object for data storage

## The Iron Rule

**Use `Object.entries` for safe iteration over any object. Use `for...in` with `keyof` assertions only when you know the exact shape. Consider Map for guaranteed type safety.**

## Detection

Watch for these errors:

```typescript
// ERROR: Element implicitly has 'any' type
for (const k in obj) {
  const v = obj[k];  // Error!
}

// ERROR: Type 'string' cannot be used to index type 'ABC'
function foo(abc: ABC) {
  for (const k in abc) {
    const v = abc[k];  // Error!
  }
}
```

## The Problem

```typescript
interface ABC {
  a: string;
  b: string;
  c: number;
}

function foo(abc: ABC) {
  for (const k in abc) {
    // k is string, not 'a' | 'b' | 'c'
    const v = abc[k];
    //     ^? any - TypeScript gives up
  }
}

// Why? Structural typing allows extra properties:
const x = { a: 'a', b: 'b', c: 2, d: new Date() };
foo(x);  // Valid! x has at least ABC's properties

// k could be 'd', which isn't in ABC
```

## Safe Iteration with Object.entries

```typescript
function foo(abc: ABC) {
  for (const [k, v] of Object.entries(abc)) {
    // k: string (honest about what it is)
    // v: any (honest about unknown values)
    console.log(k, v);
  }
}
```

**Pros**: Always safe, no type assertions needed
**Cons**: Values are `any`, keys are `string`

## Iterating with Known Keys

When you know exactly what keys exist:

```typescript
const obj = { one: 'uno', two: 'dos', three: 'tres' };

// Explicitly list keys
const keys = ['one', 'two', 'three'] as const;
for (const k of keys) {
  // k: 'one' | 'two' | 'three'
  const v = obj[k];  // string - precise!
}
```

## Type Assertion for Closed Objects

When you're sure about the object's shape:

```typescript
const obj = { one: 'uno', two: 'dos', three: 'tres' };

for (const kStr in obj) {
  const k = kStr as keyof typeof obj;
  // k: 'one' | 'two' | 'three'
  const v = obj[k];  // OK
}
```

**Warning**: Only safe when you control object creation and know it has no extra properties.

## Map: The Type-Safe Alternative

```typescript
const m = new Map([
  ['one', 'uno'],
  ['two', 'dos'],
  ['three', 'tres'],
]);

for (const [k, v] of m) {
  // k: string (known type)
  // v: string (known type)
  console.log(k, v);
}
```

**Pros**: Guaranteed types, no prototype pollution
**Cons**: Less convenient for JSON data, different API

## Real-World Example

```typescript
interface Config {
  host: string;
  port: number;
  ssl: boolean;
}

// Safe iteration with Object.entries
function printConfig(config: Config) {
  for (const [key, value] of Object.entries(config)) {
    console.log(`${key}: ${value}`);
  }
}

// Type-safe with known keys
function validateConfig(config: Config): string[] {
  const errors: string[] = [];
  const requiredKeys = ['host', 'port', 'ssl'] as const;
  
  for (const key of requiredKeys) {
    if (!(key in config)) {
      errors.push(`Missing: ${key}`);
    }
  }
  
  return errors;
}
```

## Pressure Resistance Protocol

When object iteration causes type issues:

1. **Try Object.entries**: Safest option, works with any object
2. **Consider Map**: If you control the data structure
3. **List keys explicitly**: When keys are known at compile time
4. **Use type assertions sparingly**: Only when you're certain about object shape

## Red Flags

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `obj[k]` in for...in | k is string, unsafe index | Use Object.entries |
| `as keyof T` on parameters | Object might have extra keys | Object.entries or Map |
| Ignoring inherited properties | Prototype pollution risk | Object.entries excludes these |

## Common Rationalizations

### "I'll just use `as any`"

**Reality**: `Object.entries` gives you the same `any` but honestly. No need to bypass type safety.

### "This object will never have extra properties"

**Reality**: TypeScript's structural typing means it could. Be explicit about your assumptions.

### "Map is too verbose"

**Reality**: It's more verbose but also more type-safe. Worth it for critical code.

## Quick Reference

| Approach | Key Type | Value Type | Safety |
|----------|----------|------------|--------|
| `for...in` | `string` | `any` (error) | Unsafe |
| `Object.entries` | `string` | `any` | Safe |
| Known keys array | Specific | Specific | Safe |
| `keyof` assertion | Specific | Specific | Risky |
| Map | Specific | Specific | Safe |

## The Bottom Line

Object iteration is tricky due to structural typing and prototype pollution. Use `Object.entries` for safety, explicit key arrays for precision, or Map for guaranteed type safety.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 60: Know How to Iterate Over Objects
