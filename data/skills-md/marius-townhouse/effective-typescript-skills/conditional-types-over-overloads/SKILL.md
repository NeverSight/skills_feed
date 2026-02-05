---
name: conditional-types-over-overloads
description: Use when typing functions with multiple return types. Use when function behavior depends on input type. Use when dealing with union type inputs. Use when considering function overloads.
---

# Prefer Conditional Types to Overload Signatures

## Overview

When a function's return type depends on its input type, you might reach for overload signatures. However, conditional types often provide a better solution. Unlike overloads, which are checked independently, conditional types distribute over unions and can be analyzed as a single expression. This makes them more powerful for handling union inputs and results in more maintainable type declarations.

Understanding when to use conditional types versus overloads is key to writing flexible, correct type signatures.

## When to Use This Skill

- Function return type depends on input type
- Function accepts union types
- Considering multiple overload signatures
- Need precise return types based on inputs
- Building type utilities that transform types

## The Iron Rule

**Prefer conditional types to overloaded signatures. Conditional types distribute over unions and provide more precise, maintainable type declarations.**

## Detection

Watch for these patterns:

```typescript
// RED FLAGS - Overloads that should be conditionals
declare function process(x: string): string;
declare function process(x: number): number;
declare function process(x: boolean): boolean;
// Missing union case!

// Or: Multiple overloads for what should be one conditional type
declare function transform(input: A): X;
declare function transform(input: B): Y;
declare function transform(input: C): Z;
```

## The Problem with Overloads

Overloads are checked independently and don't handle unions well:

```typescript
// Overload approach
declare function double(x: number): number;
declare function double(x: string): string;

// Works for individual types
const n = double(12);  // number
const s = double('x'); // string

// FAILS for unions
function f(x: string | number) {
  return double(x);
  //     ~~~~~~~~~
  // Error: No overload matches this call
}
```

## Conditional Type Solution

Conditional types distribute over unions automatically:

```typescript
// Conditional type approach
declare function double<T extends string | number>(
  x: T
): T extends string ? string : number;

// Works for individual types
const n = double(12);  // number
const s = double('x'); // string

// ALSO works for unions!
function f(x: string | number) {
  return double(x);  // string | number - correct!
}
```

## How Distribution Works

When `T` is `string | number`, TypeScript evaluates:

```typescript
(string | number) extends string ? string : number
→ (string extends string ? string : number) |
  (number extends string ? string : number)
→ string | number
```

## Real-World Example

```typescript
// Event handler with different payloads
type EventMap = {
  click: { x: number; y: number };
  keypress: { key: string; code: string };
  load: { timestamp: number };
};

// BAD: Multiple overloads needed
declare function onEvent(
  type: 'click',
  handler: (payload: { x: number; y: number }) => void
): void;
declare function onEvent(
  type: 'keypress',
  handler: (payload: { key: string; code: string }) => void
): void;
// ... more overloads for each event type

// GOOD: Single conditional type
declare function onEvent<T extends keyof EventMap>(
  type: T,
  handler: (payload: EventMap[T]) => void
): void;

// Usage
onEvent('click', (e) => {
  console.log(e.x, e.y);  // e is { x: number; y: number }
});

onEvent('keypress', (e) => {
  console.log(e.key);  // e is { key: string; code: string }
});
```

## Implementation Strategy

When implementing functions with conditional return types, use a single overload:

```typescript
// External signature with conditional type
declare function double<T extends string | number>(
  x: T
): T extends string ? string : number;

// Implementation with simpler type
function double(x: string | number): string | number {
  return typeof x === 'string' ? x + x : x + x;
}
```

## When Overloads Are Appropriate

Overloads may still be clearer when:
- The function acts as two completely distinct functions
- Union cases are implausible
- Different parameter counts or shapes

```typescript
// Node's readFile - distinct use cases
// Using callbacks vs Promises are truly different patterns
readFile(path, callback);      // callback version
readFile(path, options);       // Promise version
// Better as separate functions or clear overloads
```

## Pressure Resistance Protocol

When pressured to use overloads for simplicity:

1. **Test union cases**: Will the function ever receive union inputs?
2. **Consider distribution**: Do you want the type to distribute over unions?
3. **Check maintainability**: Will you need to add more overloads later?
4. **Use single overload**: For implementation, use simpler type internally

## Red Flags

| Anti-Pattern | Why It's Bad |
|--------------|--------------|
| Many overloads for related types | Hard to maintain, misses union cases |
| Overloads that should distribute | Union inputs fail to type check |
| Copy-paste overloads | Violates DRY principle |
| No union overload | Forces users to use type assertions |

## Common Rationalizations

### "Overloads are simpler to read"

**Reality**: A single conditional type is often simpler than 5+ overloads. The complexity is in the number of signatures, not the conditional expression.

### "I don't need to handle unions"

**Reality**: Union types are common in TypeScript. Users will pass unions to your function, and overloads will fail them.

### "I'll add a union overload if needed"

**Reality**: A conditional type handles unions automatically. Adding union overloads manually is error-prone and verbose.

## Quick Reference

| Approach | Handles Unions | Maintainability | Use When |
|----------|---------------|-----------------|----------|
| Overloads | No (manual) | Poor (many signatures) | Truly distinct functions |
| Conditional types | Yes (automatic) | Good (single signature) | Related return types |
| Union return | Yes | Simple | Don't need precision |

## The Bottom Line

Conditional types distribute over unions and provide more correct, maintainable type declarations than overloads. Use overloads only when the function represents truly distinct operations.

## Reference

- Effective TypeScript, 2nd Edition by Dan Vanderkam
- Item 52: Prefer Conditional Types to Overload Signatures
