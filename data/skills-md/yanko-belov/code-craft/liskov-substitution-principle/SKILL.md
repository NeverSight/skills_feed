---
name: liskov-substitution-principle
description: Use when creating subclasses or implementing interfaces. Use when tempted to override methods with exceptions or no-ops. Use when inheritance hierarchy feels wrong.
---

# Liskov Substitution Principle (LSP)

## Overview

**Subtypes must be substitutable for their base types without altering program correctness.**

If S is a subtype of T, objects of type T can be replaced with objects of type S without breaking the program. Subclasses must honor the contracts of their parent classes.

## When to Use

- Creating a class that extends another class
- Overriding methods from a parent class
- Implementing an interface
- Feeling like you need to throw exceptions in overridden methods
- Inheritance hierarchy feels "forced"

## The Iron Rule

```
NEVER create a subclass that breaks the expectations of the parent class.
```

**No exceptions:**
- Not for "it's the standard approach"
- Not for "I'll note it as an anti-pattern"
- Not for "the requirements say to extend"
- Not throwing exceptions in overridden methods
- Not making overridden methods no-ops

**Providing violating code "with a caveat" is still providing violating code.**

## Detection: The Substitution Test

Ask: "Can I replace every instance of Parent with Child without breaking anything?"

```typescript
function processRectangle(rect: Rectangle): void {
  rect.setWidth(5);
  rect.setHeight(10);
  assert(rect.getArea() === 50); // Always true for Rectangle
}

// If Square extends Rectangle:
const square = new Square(5);
processRectangle(square); // FAILS! Area is 100, not 50
```

If substitution breaks code, you have an LSP violation.

## Detection: Override Smells

These overrides indicate LSP violations:

```typescript
// ❌ VIOLATION: Throwing in override
class Penguin extends Bird {
  fly(): void {
    throw new Error("Penguins can't fly"); // Breaks callers expecting fly()
  }
}

// ❌ VIOLATION: No-op override
class ReadOnlyStorage extends FileStorage {
  write(path: string, content: string): void {
    // Silently does nothing - breaks caller expectations
  }
}

// ❌ VIOLATION: Changing behavior semantics
class Square extends Rectangle {
  setWidth(w: number): void {
    this.width = w;
    this.height = w; // Changes height too - breaks expectations
  }
}
```

## The Correct Pattern: Composition & Interfaces

**Don't force inheritance. Use interfaces to define capabilities.**

### Square/Rectangle Problem

```typescript
// ✅ CORRECT: Separate types, shared interface
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  getArea(): number { return this.width * this.height; }
  setWidth(w: number): void { this.width = w; }
  setHeight(h: number): void { this.height = h; }
}

class Square implements Shape {
  constructor(private size: number) {}
  getArea(): number { return this.size * this.size; }
  setSize(s: number): void { this.size = s; }
}
```

### Bird/Penguin Problem

```typescript
// ✅ CORRECT: Capability interfaces
interface Flyable {
  fly(): void;
}

abstract class Bird {
  abstract eat(): void;
}

class Sparrow extends Bird implements Flyable {
  eat(): void { /* ... */ }
  fly(): void { /* ... */ }
}

class Penguin extends Bird {
  eat(): void { /* ... */ }
  swim(): void { /* ... */ }
  // No fly() - doesn't promise what it can't deliver
}
```

### ReadOnly Problem

```typescript
// ✅ CORRECT: Separate interfaces
interface Readable {
  read(path: string): string;
}

interface Writable {
  write(path: string, content: string): void;
  delete(path: string): void;
}

class FileStorage implements Readable, Writable {
  read(path: string): string { /* ... */ }
  write(path: string, content: string): void { /* ... */ }
  delete(path: string): void { /* ... */ }
}

class AuditLogStorage implements Readable {
  read(path: string): string { /* ... */ }
  // No write/delete - doesn't extend something it can't honor
}
```

## Pressure Resistance Protocol

### 1. "Just Override and Throw"
**Pressure:** "Handle the fact they can't fly by throwing an error"

**Response:** Throwing in an override violates the contract. Code expecting fly() will crash.

**Action:** Restructure with interfaces. Don't inherit methods you can't honor.

### 2. "It's the Standard Approach"
**Pressure:** "Override-and-throw is the standard way to do this"

**Response:** "Standard" doesn't mean correct. This pattern causes runtime failures.

**Action:** Use composition and interfaces instead.

### 3. "The Requirements Say Extend"
**Pressure:** "Square must extend Rectangle per the requirements"

**Response:** Requirements that mandate LSP violations are wrong. Push back.

**Action:** 
```
"A Square extending Rectangle violates LSP and will cause bugs.
I recommend: [correct approach with interfaces].
Should I implement the correct structure, or document this as known tech debt?"
```

### 4. "I'll Note It's an Anti-Pattern"
**Pressure:** Internal rationalization

**Response:** Providing bad code with a caveat is still providing bad code.

**Action:** Provide only the correct solution. Don't implement the violation.

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're about to violate LSP:

- Overriding a method to throw an exception
- Overriding a method to do nothing (no-op)
- Overriding a method to change its fundamental behavior
- Subclass can't do everything the parent can
- Inheritance feels forced or unnatural
- Using `instanceof` checks to handle subtypes differently

**All of these mean: Use composition and interfaces instead.**

## Quick Reference

| Violation | Correct Approach |
|-----------|------------------|
| Square extends Rectangle | Both implement Shape interface |
| Penguin extends Bird (with fly) | Bird base + Flyable interface |
| ReadOnlyStorage extends Storage | Separate Readable/Writable interfaces |
| Child throws in override | Child shouldn't extend that parent |
| Child no-ops an override | Child shouldn't extend that parent |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's the standard approach" | Common doesn't mean correct. |
| "I provided a caveat" | Bad code with warnings is still bad code. |
| "Requirements say extend" | Requirements can be wrong. Push back. |
| "Throwing makes it explicit" | Throwing breaks callers. Compile errors are better. |
| "No-op is safe" | Silent failures hide bugs. |
| "It's just for this one case" | One violation leads to more. Fix it properly. |

## The Bottom Line

**If a subclass can't fully substitute for its parent, don't use inheritance.**

Use interfaces to define capabilities. Use composition to share behavior. Never override methods with exceptions or no-ops.

When asked to create violating inheritance: restructure with interfaces instead. Don't provide the violation "with a caveat."
