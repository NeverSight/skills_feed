---
name: law-of-demeter
description: Use when accessing nested object properties. Use when chaining method calls. Use when reaching through objects to get data.
---

# Law of Demeter (Don't Talk to Strangers)

## Overview

**Only talk to your immediate friends, not strangers.**

A method should only call methods on: itself, its parameters, objects it creates, or its direct components. Never reach through an object to access another object's internals.

## When to Use

- Accessing nested properties: `obj.a.b.c`
- Chaining method calls: `obj.getA().getB().getC()`
- Reaching through objects for data
- Long dot chains in your code

## The Iron Rule

```
NEVER chain through objects. Ask, don't reach.
```

**No exceptions:**
- Not for "it's simpler"
- Not for "it's just one chain"
- Not for "the data is there"
- Not for "fewer lines of code"

## Detection: The Chain Smell

If you see multiple dots, you're violating LoD:

```typescript
// ❌ VIOLATION: Reaching through objects
function getEmployeeCity(company: Company, employeeId: string): string {
  return company.employees
    .find(e => e.id === employeeId)
    ?.address.city;  // Reaching into employee, then into address
}

// More violations:
user.getProfile().getAddress().getZipCode();
order.getCustomer().getPaymentMethod().getLast4();
```

## The Correct Pattern: Ask, Don't Reach

Let objects expose what's needed:

```typescript
// ✅ CORRECT: Ask the object directly
class Employee {
  constructor(
    private name: string,
    private address: Address
  ) {}
  
  getCity(): string {
    return this.address.city;  // Employee asks its own address
  }
}

class Company {
  getEmployeeCities(): Map<string, string> {
    return new Map(
      this.employees.map(e => [e.id, e.getCity()])
    );
  }
  
  getEmployeeCity(employeeId: string): string | undefined {
    return this.employees.find(e => e.id === employeeId)?.getCity();
  }
}

// Usage: Ask company, don't reach through it
const city = company.getEmployeeCity(employeeId);
```

## Why Chains Are Bad

| Problem | Impact |
|---------|--------|
| **Tight coupling** | Caller knows internal structure |
| **Fragile code** | Structure changes break all callers |
| **Hidden dependencies** | Not obvious what's needed |
| **Hard to test** | Must mock entire chain |
| **Null danger** | Each `.` is a potential null |

## Allowed Method Calls

A method `m` of class `C` should only call methods on:

1. **`this`** - C's own methods
2. **Parameters** - Objects passed to `m`
3. **Created objects** - Objects `m` creates
4. **Components** - C's direct instance variables
5. **Globals** - Accessible global objects (sparingly)

```typescript
class OrderProcessor {
  constructor(private logger: Logger) {}  // Component

  process(order: Order): Receipt {         // Parameter
    this.validate(order);                  // this
    const receipt = new Receipt(order);    // Created
    this.logger.log('Processed');          // Component
    return receipt;
  }

  // ❌ NOT ALLOWED: order.customer.address.city
  // ✅ ALLOWED: order.getShippingCity()
}
```

## Pressure Resistance Protocol

### 1. "It's Simpler"
**Pressure:** "One line with dots is simpler than adding methods"

**Response:** Simple to write ≠ simple to maintain. Chains create fragile code.

**Action:** Add methods that expose needed data.

### 2. "It's Just One Chain"
**Pressure:** "It's only two dots, not a big deal"

**Response:** Two dots = two objects you're coupled to. Both can change and break you.

**Action:** Even short chains should be eliminated.

### 3. "The Data Is Right There"
**Pressure:** "The structure has the data, why wrap it?"

**Response:** Structure changes. Wrapping isolates you from changes.

**Action:** Ask the owner for the data.

### 4. "It's Read-Only"
**Pressure:** "I'm just reading, not modifying"

**Response:** Reading through chains still couples you to structure.

**Action:** Ask for what you need.

## Red Flags - STOP and Reconsider

If you notice ANY of these, refactor:

- Multiple dots: `a.b.c.d`
- Chained getters: `getA().getB().getC()`
- Optional chains: `a?.b?.c?.d`
- Null checks for nested access
- Structure knowledge in calling code
- Mocking chains in tests

**All of these mean: Add a method to ask directly.**

## Refactoring Chains

```typescript
// ❌ BEFORE: Chain
const zip = user.getProfile().getAddress().getZipCode();

// ✅ AFTER: Ask
// In User class:
getZipCode(): string {
  return this.profile.getZipCode();
}

// In Profile class:
getZipCode(): string {
  return this.address.zipCode;
}

// Usage:
const zip = user.getZipCode();
```

## Quick Reference

| Chain (Bad) | Ask (Good) |
|-------------|------------|
| `company.employees[0].address.city` | `company.getEmployeeCity(id)` |
| `order.customer.paymentMethod.last4` | `order.getPaymentLast4()` |
| `user.profile.settings.theme` | `user.getTheme()` |
| `car.engine.fuel.level` | `car.getFuelLevel()` |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's simpler" | Chains are simpler to write, harder to maintain. |
| "Just one chain" | One chain = multiple couplings. |
| "Data is right there" | Expose it properly through methods. |
| "It's read-only" | Reading chains still couples you. |
| "Fewer lines" | Lines don't matter. Maintainability does. |
| "It's obvious what it does" | Obvious coupling is still coupling. |

## The Bottom Line

**Ask objects for what you need. Don't reach through them.**

When you need data from nested objects: add a method on the owner that returns it. Never chain through multiple objects. Each dot is a dependency you're taking on.
