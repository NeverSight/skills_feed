---
name: avoid-unnecessary-type-params
description: Use when writing generic functions or types. Use when reviewing type signatures. Use when a type parameter only appears once. Use when tempted to add generics for "flexibility".
---

# Avoid Unnecessary Type Parameters

## Overview

The "Golden Rule of Generics" states that type parameters should appear twice or more in a function signature. If a type parameter only appears once, it's not relating anything and is likely unnecessary. Unnecessary type parameters create a false sense of type safety and can make inference less successful.

This skill helps you identify and eliminate superfluous type parameters, resulting in cleaner, more maintainable code that TypeScript can infer more effectively.

## When to Use This Skill

- Writing generic functions or types
- Reviewing type signatures for clarity
- A type parameter appears only once (besides its declaration)
- Tempted to add generics for "flexibility"
- Debugging poor type inference

## The Iron Rule

**Type parameters must appear twice or more to establish a relationship. If a type parameter only appears once, strongly reconsider if you need it.**

## Detection

Watch for these patterns:

```typescript
// RED FLAGS - Unnecessary type parameters
function parseYAML<T>(input: string): T;  // Return-only generic
type Fn = <T>(x: T) => void;  // T only used once
function third<A, B, C>(a: A, b: B, c: C): C;  // A and B appear once
function getLength<T extends Lengthy>(x: T): number;  // T only in parameter
```

## The Golden Rule

Type parameters are for relating types. If a type parameter only appears once, it's not relating anything:

```typescript
// GOOD: T appears twice, relating input and output
function identity<T>(arg: T): T {
  return arg;
}

// BAD: T only appears once (in return type)
function parseYAML<T>(input: string): T;
// Equivalent to: function parseYAML(input: string): any

// Usage shows the problem:
const data: User = parseYAML('...');  // Looks safe, but T can be anything
const bad: Banana = parseYAML('...');  // Also "valid" - no error!
```

## Return-Only Generics

Return-only generics are dangerous because they're equivalent to type assertions without the explicit `as`:

```typescript
// BAD: Return-only generic
declare function parseYAML<T>(input: string): T;
const user: User = parseYAML('...');  // No error, but no validation either

// GOOD: Return unknown, force explicit assertion
declare function parseYAML(input: string): unknown;
const user = parseYAML('...') as User;  // Explicit about the assertion

// Or use validation:
const user = parseYAML('...');
if (isUser(user)) {  // Type guard
  // user is User here
}
```

## Simplifying Unnecessary Generics

```typescript
// BEFORE: Unnecessary type parameters
function third<A, B, C>(a: A, b: B, c: C): C {
  return c;
}

// AFTER: Only keep C which appears twice
function third<C>(a: unknown, b: unknown, c: C): C {
  return c;
}
```

## When Generics ARE Needed

```typescript
// GOOD: K appears twice, relating parameter to return type
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

// K appears in: parameter type (key: K) and return type (T[K])
// This IS a good use of generics
```

## Class Generics

```typescript
// GOOD: T appears multiple times, relating class properties
class Container<T> {
  private items: T[] = [];
  add(item: T): void { this.items.push(item); }
  getAll(): T[] { return this.items; }
}

// BAD: T only used in one method
class Joiner<T extends string | number> {
  join(els: T[]): string {
    return els.map(String).join(',');
  }
}
// Better: Move T to method or use concrete type
class Joiner {
  join(els: (string | number)[]): string {
    return els.map(String).join(',');
  }
}
// Best: Just a function
function join(els: (string | number)[]): string {
  return els.map(String).join(',');
}
```

## Pressure Resistance Protocol

When pressured to add "flexible" generics:

1. **Count appearances**: Does the type parameter appear twice or more?
2. **Check relationships**: Is it relating multiple values' types?
3. **Consider unknown**: Would `unknown` work just as well?
4. **Test inference**: Does the generic improve or hurt type inference?

## Red Flags

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| `function f<T>(): T` | Return-only, no type safety |
| `type Fn = <T>(x: T) => void` | T not used in return, unnecessary |
| Generics for single-use types | Adds complexity without benefit |
| `T extends X` where T only appears once | Constraint doesn't help |

## Common Rationalizations

### "It makes the API more flexible"

**Reality**: Unnecessary generics create a false sense of safety. They don't add real flexibility, just confusion.

### "I'll need it later"

**Reality**: Add generics when you need them, not in anticipation. You can always add them later.

### "It looks more professional"

**Reality**: Simple, correct types are more professional than complex, unnecessary ones.

## Quick Reference

| Pattern | Verdict | Fix |
|---------|---------|-----|
| `function f<T>(x: T): T` | ✓ Good | T relates input to output |
| `function f<T>(x: string): T` | ✗ Bad | Use `unknown` or concrete type |
| `function f<T>(x: T): void` | ✗ Bad | Use `unknown` or `any` |
| `class C<T> { method(x: T): T }` | ✓ Good | T relates multiple uses |
| `class C<T> { method(x: T): void }` | ✗ Bad | Move T to method or remove |

## The Bottom Line

The first rule of generics is "don't." Only add type parameters when they establish relationships between types. If a type parameter appears only once, eliminate it. This results in cleaner code and better type inference.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 51: Avoid Unnecessary Type Parameters
