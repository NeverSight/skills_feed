---
name: excess-property-checking
description: Use when assigning object literals to typed variables. Use when confused by "unknown property" errors. Use when extra properties are flagged on object literals but not variables.
---

# Distinguish Excess Property Checking from Type Checking

## Overview

**Object literals get special treatment: TypeScript flags unknown properties.**

This catches typos and mistakes that structural typing would miss. But it only applies to object literals - understanding this distinction prevents confusion.

## When to Use This Skill

- Assigning object literals to typed variables
- Confused why extra properties cause errors sometimes
- Error disappears when using intermediate variable
- Working with optional properties where typos are likely
- Designing interfaces with many optional fields

## The Iron Rule

```
ALWAYS remember: Excess property checking only applies to OBJECT LITERALS.
```

**Remember:**
- Object literal → extra properties flagged
- Variable assignment → structural typing applies
- Type assertions → bypass excess property checking

## Detection: The "Extra Property" Error

When you see "Object literal may only specify known properties", you've triggered excess property checking.

```typescript
interface Room {
  numDoors: number;
  ceilingHeightFt: number;
}

// Excess property checking: Error!
const r: Room = {
  numDoors: 1,
  ceilingHeightFt: 10,
  elephant: 'present',
  // ~~~~~~~ Object literal may only specify known properties,
  //         and 'elephant' does not exist in type 'Room'
};

// Same value via intermediate variable: No error!
const obj = {
  numDoors: 1,
  ceilingHeightFt: 10,
  elephant: 'present',
};
const r2: Room = obj;  // OK - structural typing allows this
```

## Why Excess Property Checking Exists

Structural typing is powerful but permissive. It allows extra properties, which can hide bugs:

```typescript
interface Options {
  title: string;
  darkMode?: boolean;
}

function createWindow(options: Options) {
  if (options.darkMode) {
    setDarkMode();
  }
}

// Without excess property checking, this typo would be silent:
createWindow({
  title: 'Spider Solitaire',
  darkmode: true  // lowercase 'm' - TYPO!
  // ~~~~~~~ Object literal may only specify known properties,
  //         but 'darkmode' does not exist in type 'Options'.
  //         Did you mean to write 'darkMode'?
});
```

## When Excess Property Checking Applies

| Context | Excess Property Checking? |
|---------|---------------------------|
| Object literal assigned to typed variable | Yes |
| Object literal as function argument | Yes |
| Object literal as return value | Yes |
| Variable assigned to typed variable | No |
| Type assertion | No |

```typescript
interface Point { x: number; y: number; }

// Object literal - checking applies
const p1: Point = { x: 1, y: 2, z: 3 };  // Error: 'z' not in Point

// Variable - checking does NOT apply
const temp = { x: 1, y: 2, z: 3 };
const p2: Point = temp;  // OK

// Type assertion - checking does NOT apply
const p3 = { x: 1, y: 2, z: 3 } as Point;  // OK (but bad practice)
```

## When Excess Property Checking Helps

### Catching Typos in Optional Properties

```typescript
interface Config {
  logLevel?: 'debug' | 'info' | 'warn' | 'error';
  timeout?: number;
  retries?: number;
}

const config: Config = {
  loglevel: 'debug',  // Error: Did you mean 'logLevel'?
  timeout: 5000,
};
```

### Preventing Wrong Property Names

```typescript
interface User {
  firstName: string;
  lastName: string;
}

const user: User = {
  first_name: 'John',  // Error: Did you mean 'firstName'?
  last_name: 'Doe',    // Error: Did you mean 'lastName'?
};
```

## Bypassing Excess Property Checking (When Intentional)

### Use Index Signature for Known Extra Properties

```typescript
interface Options {
  darkMode?: boolean;
  [otherOptions: string]: unknown;
}

const o: Options = { darkmode: true };  // OK now
```

### Use Intermediate Variable

```typescript
const options = { title: 'Game', extraProp: true };
createWindow(options);  // OK - excess checking skipped
```

## Weak Types: A Related Check

"Weak" types have only optional properties. TypeScript adds a special check:

```typescript
interface LineChartOptions {
  logscale?: boolean;
  invertedYAxis?: boolean;
  areaChart?: boolean;
}

const opts = { logScale: true };  // Note: capital 'S'
setOptions(opts);
// ~~~~ Type '{ logScale: boolean; }' has no properties in common
//      with type 'LineChartOptions'
```

This check applies even through intermediate variables (unlike regular excess property checking).

## Common Mistakes

### Mistake 1: Expecting Structural Typing to Catch Typos

```typescript
// ❌ Typo passes silently because no excess property checking
const options = { darkmode: true };  // lowercase 'm'
const config: Options = options;     // No error!

// ✅ Use object literal for catching typos
const config: Options = { darkmode: true };  // Error caught!
```

### Mistake 2: Using Type Assertion to Silence Errors

```typescript
// ❌ Assertion bypasses the check
const config = { darkmode: true } as Options;

// ✅ Fix the typo instead
const config: Options = { darkMode: true };
```

### Mistake 3: Confusion About Why Error Disappears

```typescript
// This has an error
const p: Point = { x: 1, y: 2, z: 3 };

// Why doesn't this?
const temp = { x: 1, y: 2, z: 3 };
const p: Point = temp;

// Answer: Excess property checking only applies to object literals!
```

## Pressure Resistance Protocol

### 1. "Just Add `as Type`"

**Pressure:** "The type assertion makes the error go away"

**Response:** Assertions bypass safety checks. Fix the actual issue.

**Action:** Correct the property name or update the type definition.

### 2. "TypeScript Is Being Too Strict"

**Pressure:** "Extra properties shouldn't matter"

**Response:** This catches real bugs like typos in optional fields.

**Action:** If you truly need extra properties, use an index signature.

### 3. "It Works With a Variable"

**Pressure:** "Just use an intermediate variable to avoid the error"

**Response:** That hides bugs. The error exists for a reason.

**Action:** Investigate why the extra property exists.

## Red Flags - STOP and Reconsider

- Using type assertion to silence excess property errors
- Creating intermediate variables just to avoid checks
- Confused why some assignments error and others don't
- Thinking TypeScript is inconsistent about extra properties

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's just an extra property" | Extra properties often indicate typos |
| "Structural typing allows this" | Object literals have stricter rules for good reason |
| "The assertion fixes it" | Assertions hide bugs, they don't fix them |

## Quick Reference

| Scenario | Excess Property Check? | Example |
|----------|----------------------|---------|
| Object literal to typed var | Yes | `const x: T = { ... }` |
| Object literal as argument | Yes | `fn({ ... })` |
| Variable to typed var | No | `const temp = {...}; const x: T = temp;` |
| Type assertion | No | `{ ... } as T` |
| Weak type (via variable) | Checks for common props | Special case |

## The Bottom Line

**Excess property checking catches bugs that structural typing would miss.**

It only applies to object literals, not variables. This is intentional - it catches typos in property names, especially for optional properties. Don't bypass it with assertions or intermediate variables; instead, fix the underlying issue.

## Reference

Based on "Effective TypeScript" by Dan Vanderkam, Item 11: Distinguish Excess Property Checking from Type Checking.
