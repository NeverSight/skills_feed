---
name: interface-segregation-principle
description: Use when designing interfaces. Use when implementing interfaces with methods you don't need. Use when forced to implement throw/no-op for interface methods.
---

# Interface Segregation Principle (ISP)

## Overview

**Clients should not be forced to depend on interfaces they don't use.**

Many small, focused interfaces are better than one large "fat" interface. If an implementer must throw exceptions or provide no-ops for interface methods, the interface is too large.

## When to Use

- Designing a new interface
- Implementing an interface with unused methods
- Forced to implement methods that don't apply
- Interface has more than 5-7 methods
- Different implementers use different subsets of methods

## The Iron Rule

```
NEVER implement an interface method with throw or no-op.
```

**No exceptions:**
- Not for "it's what the interface requires"
- Not for "I'll provide both approaches"
- Not for "the caller can check capabilities"
- Not for "it's clearly documented as unsupported"

**Providing both the violation and the correct approach is still providing a violation.**

## Detection: The "Throw/No-op" Smell

If your implementation looks like this, the interface is wrong:

```typescript
// ❌ FAT INTERFACE
interface MultiFunctionDevice {
  print(doc: string): void;
  scan(): string;
  fax(doc: string): void;
}

// ❌ VIOLATION: Forced to implement unusable methods
class BasicPrinter implements MultiFunctionDevice {
  print(doc: string): void { /* works */ }
  scan(): string { throw new Error("Not supported"); }  // ← ISP violation
  fax(doc: string): void { /* no-op */ }                // ← ISP violation
}
```

## The Correct Pattern: Segregated Interfaces

Split the fat interface into focused capabilities:

```typescript
// ✅ CORRECT: Segregated interfaces
interface Printer {
  print(doc: string): void;
}

interface Scanner {
  scan(): string;
}

interface Fax {
  fax(doc: string): void;
}

// Implement only what you support
class BasicPrinter implements Printer {
  print(doc: string): void { /* works */ }
  // No scan or fax - doesn't promise what it can't deliver
}

class AllInOne implements Printer, Scanner, Fax {
  print(doc: string): void { /* works */ }
  scan(): string { /* works */ }
  fax(doc: string): void { /* works */ }
}

// Combined type for callers who need everything
type MultiFunctionDevice = Printer & Scanner & Fax;
```

## Pressure Resistance Protocol

### 1. "The Interface Already Exists"
**Pressure:** "Implement this existing interface, handle unsupported methods"

**Response:** The interface is wrong. Propose splitting it.

**Action:**
```
"This interface forces implementers to provide throw/no-op for methods they don't support.
I recommend splitting into: [list focused interfaces].
Should I refactor the interface, or document this as tech debt?"
```

### 2. "Just Throw an Error"
**Pressure:** "Handle unsupported methods by throwing"

**Response:** Runtime errors for expected interface methods is a design failure.

**Action:** Split the interface so implementers only promise what they can deliver.

### 3. "I'll Provide Both Options"
**Pressure:** "Here's the violation you asked for AND here's the better way"

**Response:** Providing the violation at all enables bad code to ship.

**Action:** Provide ONLY the correct approach. Don't implement the fat interface.

### 4. "Callers Can Check First"
**Pressure:** "Add a `supports(method)` check"

**Response:** This is a workaround for bad design. Type system should enforce capabilities.

**Action:** Split interfaces so the type system does the checking at compile time.

## Red Flags - STOP and Reconsider

If you notice ANY of these, the interface needs splitting:

- Implementing a method with `throw new Error`
- Implementing a method as no-op (empty body)
- Interface has 7+ methods
- Different implementers use different subsets
- Adding `supportsX()` capability checks
- Implementers have large blocks of unused methods

**All of these mean: Split the interface.**

## Interface Design Guidelines

### Size
- **Ideal:** 1-3 methods per interface
- **Acceptable:** 4-5 methods if highly cohesive
- **Too large:** 6+ methods - look for split opportunities

### Cohesion Test
Ask: "Do ALL implementers need ALL these methods?"
- Yes → Keep together
- No → Split

### Common Splits

| Fat Interface | Segregated Interfaces |
|---------------|----------------------|
| `Repository<T>` | `Readable<T>`, `Writable<T>` |
| `Worker` | `Workable`, `Eatable`, `Meetable` |
| `MultiFunctionDevice` | `Printer`, `Scanner`, `Fax` |
| `FileSystem` | `FileReader`, `FileWriter`, `FileDeleter` |
| `UserService` | `UserReader`, `UserWriter`, `UserAuth` |

## Quick Reference

| Symptom | Action |
|---------|--------|
| Method implemented as throw | Split interface |
| Method implemented as no-op | Split interface |
| 7+ methods in interface | Look for split |
| `supports()` capability checks | Split interface |
| Implementers ignore methods | Split interface |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "The interface already exists" | Interfaces can be refactored. |
| "Throwing makes it explicit" | Compile errors are better than runtime errors. |
| "I provided both approaches" | Providing the violation enables bad code. |
| "It's documented as unsupported" | Documentation doesn't fix design flaws. |
| "Many interfaces is complex" | Many small interfaces is simpler than one broken one. |
| "Callers can check capabilities" | Type system should do this, not runtime checks. |

## The Bottom Line

**No client should be forced to depend on methods it doesn't use.**

When asked to implement a fat interface:
1. Identify which methods are actually needed
2. Propose segregated interfaces
3. Implement only the focused interfaces

Never provide throw/no-op implementations. Never provide "both options." The fat interface is the problem - fix it.
