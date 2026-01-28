---
name: composition-over-inheritance
description: Use when tempted to use class inheritance. Use when creating class hierarchies. Use when subclass needs only some parent behavior.
---

# Composition Over Inheritance

## Overview

**Favor object composition over class inheritance.**

Inheritance creates tight coupling and rigid hierarchies. Composition creates flexible, reusable components that can be mixed and matched.

## When to Use

- Designing relationships between classes
- Tempted to use `extends`
- Class needs behavior from multiple sources
- Creating "is-a" relationships
- Building class hierarchies

## The Iron Rule

```
NEVER use inheritance when composition would work.
```

**No exceptions:**
- Not for "it's the OOP way"
- Not for "is-a relationship"
- Not for "code reuse via extends"
- Not for "polymorphism"

**Default to composition. Use inheritance only for true type hierarchies.**

## Detection: The Inheritance Smell

If inheritance feels awkward or forced, use composition:

```typescript
// ❌ VIOLATION: Inheritance hierarchy
class Animal {
  eat(): void { console.log('Eating'); }
}

class FlyingAnimal extends Animal {
  fly(): void { console.log('Flying'); }
}

class SwimmingAnimal extends Animal {
  swim(): void { console.log('Swimming'); }
}

// Duck needs both fly AND swim - inheritance can't do this cleanly
class Duck extends FlyingAnimal {
  swim(): void { console.log('Swimming'); } // Duplicated!
}
```

## Correct Pattern: Composition with Interfaces

Define capabilities as interfaces, compose them:

```typescript
// ✅ CORRECT: Composition
interface Flyable {
  fly(): void;
}

interface Swimmable {
  swim(): void;
}

interface Eatable {
  eat(): void;
}

// Reusable behaviors
const flyingBehavior: Flyable = {
  fly() { console.log('Flying'); }
};

const swimmingBehavior: Swimmable = {
  swim() { console.log('Swimming'); }
};

const eatingBehavior: Eatable = {
  eat() { console.log('Eating'); }
};

// Compose what you need
class Duck implements Flyable, Swimmable, Eatable {
  fly = flyingBehavior.fly;
  swim = swimmingBehavior.swim;
  eat = eatingBehavior.eat;
}

class Fish implements Swimmable, Eatable {
  swim = swimmingBehavior.swim;
  eat = eatingBehavior.eat;
}

class Bird implements Flyable, Eatable {
  fly = flyingBehavior.fly;
  eat = eatingBehavior.eat;
}
```

## Why Inheritance Fails

| Problem | Example |
|---------|---------|
| **Diamond problem** | Duck needs Flying AND Swimming |
| **Tight coupling** | Child knows parent internals |
| **Rigid hierarchy** | Can't change parent without breaking children |
| **Forced inheritance** | Gets methods it doesn't need |
| **Fragile base class** | Parent changes break all children |

## Why Composition Wins

| Benefit | Example |
|---------|---------|
| **Flexible** | Mix any behaviors together |
| **Loose coupling** | Components don't know each other |
| **Easy testing** | Mock individual behaviors |
| **Runtime changes** | Swap behaviors dynamically |
| **No hierarchy lock-in** | Add new combinations freely |

## Pressure Resistance Protocol

### 1. "It's the OOP Way"
**Pressure:** "Object-oriented programming uses inheritance"

**Response:** Modern OOP favors composition. Inheritance is overused.

**Action:** Use interfaces + composition. It's still OOP.

### 2. "It's an Is-A Relationship"
**Pressure:** "A Duck IS-A Bird, so it should extend Bird"

**Response:** "Is-a" often becomes "has-a" when requirements change. Composition handles both.

**Action:** Model as "has behaviors" not "is a type".

### 3. "Code Reuse via Extends"
**Pressure:** "I need the parent's methods"

**Response:** Composition provides better code reuse without coupling.

**Action:** Extract shared behavior into composable units.

### 4. "Polymorphism Requires Inheritance"
**Pressure:** "I need to treat different types uniformly"

**Response:** Interfaces provide polymorphism without inheritance.

**Action:** Define interface, have classes implement it.

## Red Flags - STOP and Reconsider

If you notice ANY of these, use composition instead:

- `extends` keyword in your code
- Class hierarchy deeper than 2 levels
- Child class overriding parent methods
- "Diamond problem" - needs multiple parents
- Subclass doesn't use all parent methods
- Changing parent breaks children
- Hard to test without instantiating parent

**All of these mean: Refactor to composition.**

## When Inheritance IS Appropriate

Use inheritance only when:
- True type hierarchy (rarely)
- Framework requires it (React class components, etc.)
- Extending library classes you don't control

Even then, keep hierarchy shallow (max 2 levels).

## Quick Reference

| Inheritance | Composition |
|-------------|-------------|
| `class Dog extends Animal` | `class Dog implements Animal` + behavior injection |
| Rigid hierarchy | Flexible composition |
| Single parent only | Multiple behaviors |
| Tight coupling | Loose coupling |
| Changes cascade | Changes isolated |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's the OOP way" | Modern OOP prefers composition. |
| "It's an is-a relationship" | "Has behavior" is more flexible. |
| "Need parent's methods" | Compose the behavior instead. |
| "Polymorphism needs it" | Interfaces provide polymorphism. |
| "Less code with extends" | More flexibility with composition. |
| "I noted it's problematic" | Don't do it if it's problematic. |

## The Bottom Line

**Compose behaviors. Don't inherit them.**

When designing classes: define interfaces for capabilities, create composable behaviors, inject what each class needs. Use `extends` only as last resort.
