---
name: branded-types
description: Use when primitive types need semantic distinction. Use when string or number types have different meanings. Use when you need nominal typing.
---

# Consider Brands for Nominal Typing

## Overview

**Add phantom types to distinguish semantically different values.**

TypeScript uses structural typing, but sometimes you need nominal typing - values that are distinct because you SAY they are, not because they have different shapes. Brands let you do this without runtime overhead.

## When to Use This Skill

- Distinguishing paths (absolute vs relative)
- Attaching units to numbers (meters, seconds)
- Preventing 2D/3D vector mix-ups
- Marking validated/sanitized strings
- Creating type-safe identifiers

## The Iron Rule

```
ALWAYS use brands when primitive types have different semantic meanings.
```

**Remember:**
- Brands are phantom types (exist only in type system)
- No runtime overhead
- Force explicit conversion/validation
- Make invalid states unrepresentable

## Detection: The "Wrong Primitive" Problem

When different primitives can be confused:

```typescript
// ❌ Any string can be passed
function readFile(path: string) { ... }

readFile('foo.txt');        // Relative path - might fail
readFile('/home/foo.txt');  // Absolute path - works
// TypeScript can't tell the difference!
```

## The Branding Pattern

### Basic Brand Structure

```typescript
type AbsolutePath = string & { _brand: 'abs' };

function isAbsolutePath(path: string): path is AbsolutePath {
  return path.startsWith('/');
}

function listAbsolutePath(path: AbsolutePath) {
  // Can only be called with validated paths
}
```

### Using Branded Types

```typescript
function f(path: string) {
  // Must check before using
  if (isAbsolutePath(path)) {
    listAbsolutePath(path);  // OK: path is now AbsolutePath
  }
  
  listAbsolutePath(path);
  //               ~~~~ Error: string not assignable to AbsolutePath
}
```

## Why Brands Work

You can't actually create a value that is both a `string` and has a `_brand` property:

```typescript
type AbsolutePath = string & { _brand: 'abs' };

// This intersection is "impossible" at runtime
// But TypeScript still uses it for type checking
```

The only way to get an `AbsolutePath` is to:
1. Be given one (from a function that returns it)
2. Use a type guard to validate and narrow
3. Use a type assertion (escape hatch)

## Common Brand Patterns

### Units of Measurement

```typescript
type Meters = number & { _brand: 'meters' };
type Seconds = number & { _brand: 'seconds' };
type MetersPerSecond = number & { _brand: 'm/s' };

const meters = (m: number) => m as Meters;
const seconds = (s: number) => s as Seconds;

function calculateSpeed(distance: Meters, time: Seconds): MetersPerSecond {
  return (distance / time) as MetersPerSecond;
}

const d = meters(100);
const t = seconds(10);
const speed = calculateSpeed(d, t);  // OK

calculateSpeed(100, 10);  // Error: number not assignable to Meters
calculateSpeed(t, d);     // Error: can't swap distance and time!
```

**Caveat:** Arithmetic operations lose the brand:

```typescript
const doubled = d * 2;
//    ^? const doubled: number  (brand lost)
```

### Validated Strings

```typescript
type SanitizedHTML = string & { _brand: 'sanitized' };
type UserId = string & { _brand: 'userId' };
type Email = string & { _brand: 'email' };

function sanitize(html: string): SanitizedHTML {
  // Actually sanitize the HTML
  return html.replace(/<script>/g, '') as SanitizedHTML;
}

function setInnerHTML(el: Element, html: SanitizedHTML) {
  el.innerHTML = html;  // Safe: we know it's sanitized
}

// Can't pass unsanitized strings
setInnerHTML(el, '<script>alert("xss")</script>');
//               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Error!

// Must sanitize first
setInnerHTML(el, sanitize(userInput));  // OK
```

### Type-Safe IDs

```typescript
type UserId = string & { _brand: 'userId' };
type PostId = string & { _brand: 'postId' };

function getUser(id: UserId): User { ... }
function getPost(id: PostId): Post { ... }

declare const userId: UserId;
declare const postId: PostId;

getUser(userId);  // OK
getUser(postId);  // Error: PostId not assignable to UserId
```

### Sorted Arrays

```typescript
type SortedList<T> = T[] & { _brand: 'sorted' };

function isSorted<T>(xs: T[]): xs is SortedList<T> {
  for (let i = 0; i < xs.length - 1; i++) {
    if (xs[i] > xs[i + 1]) return false;
  }
  return true;
}

function binarySearch<T>(xs: SortedList<T>, x: T): boolean {
  // Can assume xs is sorted
  let low = 0, high = xs.length - 1;
  while (high >= low) {
    const mid = low + Math.floor((high - low) / 2);
    const v = xs[mid];
    if (v === x) return true;
    [low, high] = x > v ? [mid + 1, high] : [low, mid - 1];
  }
  return false;
}

const nums = [1, 3, 5, 7, 9];
if (isSorted(nums)) {
  binarySearch(nums, 5);  // OK: nums is SortedList<number>
}
```

## Alternative Branding Techniques

### Using Unique Symbol (Stronger)

```typescript
declare const brand: unique symbol;

type Meters = number & { [brand]: 'meters' };

// Can't be faked because brand isn't exported
```

### Using Private Fields in Classes

```typescript
class ValidatedEmail {
  private readonly _brand!: 'email';
  constructor(public readonly value: string) {
    if (!value.includes('@')) throw new Error('Invalid email');
  }
}
```

## Preventing Vector Mix-ups

```typescript
interface Vector2D {
  x: number;
  y: number;
  z?: never;  // Explicitly prevent z
}

function norm(v: Vector2D) {
  return Math.sqrt(v.x ** 2 + v.y ** 2);
}

const v3d = { x: 3, y: 4, z: 5 };
norm(v3d);  // Error: z is incompatible with never
```

Or use brands:

```typescript
type Vector2D = { x: number; y: number } & { _brand: '2d' };
type Vector3D = { x: number; y: number; z: number } & { _brand: '3d' };
```

## Pressure Resistance Protocol

### 1. "Just Use Type Aliases"

**Pressure:** "Type alias is simpler: `type UserId = string`"

**Response:** Type aliases don't prevent mixing up different string types.

**Action:** Use brands when semantic distinction matters.

### 2. "It's Just Runtime Overhead"

**Pressure:** "Adding properties to primitives costs memory"

**Response:** Brands are phantom types - they don't exist at runtime.

**Action:** Use brands freely; there's no runtime cost.

## Red Flags - STOP and Reconsider

- Multiple string/number types that could be confused
- Functions that accept "any string" but expect specific formats
- Validation that happens but isn't tracked in the type system
- Bugs from swapping similarly-typed arguments

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "We'll be careful" | Mistakes happen, especially in large codebases |
| "Type alias is enough" | Aliases don't prevent cross-assignment |
| "Too much ceremony" | Prevents bugs that are hard to track down |

## Quick Reference

```typescript
// Basic brand pattern
type Brand<T, B extends string> = T & { _brand: B };

type UserId = Brand<string, 'userId'>;
type Meters = Brand<number, 'meters'>;

// Type guard pattern
function isX(val: T): val is BrandedT { ... }

// Factory pattern
const meters = (n: number) => n as Meters;
```

## The Bottom Line

**Use brands to give semantic meaning to primitives.**

Brands add no runtime overhead but prevent mixing up values that happen to have the same underlying type. Use them for IDs, paths, units, validated strings, and any primitive where semantic distinction matters.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 64: Consider Brands for Nominal Typing.
