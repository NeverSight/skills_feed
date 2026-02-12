---
name: open-closed-principle
description: Use when adding new functionality to existing code. Use when tempted to add if/else or switch branches. Use when extending behavior of existing classes.
---

# Open/Closed Principle (OCP)

## Overview

**Software entities should be open for extension, but closed for modification.**

When new functionality is needed, extend the system with new code rather than modifying existing code. If adding a feature requires changing existing if/else chains, you're violating OCP.

## When to Use

- Adding a new payment method, notification channel, export format, etc.
- Tempted to add another `if/else` or `switch` case
- Existing code works but needs new variants
- Feature request: "add support for X"

## The Iron Rule

```
NEVER add another branch to an existing if/else or switch statement.
```

**No exceptions:**
- Not for "it's just one more case"
- Not for "we'll refactor later"
- Not for "the pattern is already established"
- Not for "it's faster this way"

**Noting the problem while doing it anyway is still a violation.**

## Detection: The "Add Branch" Smell

If your solution involves this pattern, STOP:

```typescript
// ❌ VIOLATION: Adding branches
if (type === 'existing') {
  // existing logic
} else if (type === 'new') {  // ← Adding this = OCP violation
  // new logic
}
```

Every `else if` you add is a modification to existing code that works.

## The Correct Pattern: Strategy/Plugin

Instead of modifying, extend:

```typescript
// ✅ CORRECT: Define interface, implement separately
interface PaymentMethod {
  process(amount: number): boolean;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number): boolean { /* ... */ }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number): boolean { /* ... */ }
}

// Processor doesn't change when adding new methods
class PaymentProcessor {
  constructor(private methods: Map<string, PaymentMethod>) {}
  
  process(type: string, amount: number): boolean {
    const method = this.methods.get(type);
    if (!method) throw new Error(`Unknown: ${type}`);
    return method.process(amount);
  }
  
  register(type: string, method: PaymentMethod): void {
    this.methods.set(type, method);
  }
}
```

Adding Apple Pay? Create `ApplePayPayment`, call `register()`. **Zero modifications to PaymentProcessor.**

## Pressure Resistance Protocol

### 1. "Just Add Another Case"
**Pressure:** "The quickest approach: add more if/else branches"

**Response:** Adding branches takes the same time as creating a new class. The "quick" approach creates unmaintainable code.

**Action:** Create interface + implementation. Register the new variant.

### 2. "The Pattern Is Already There"
**Pressure:** "The code already uses if/else, just extend it"

**Response:** Existing violations don't justify more violations. This is the moment to refactor.

**Action:** 
1. Extract interface from existing branches
2. Convert branches to implementations
3. Add your new implementation

### 3. "We'll Refactor Later"
**Pressure:** "Add it now, we'll clean up later"

**Response:** You won't. The if/else will grow to 15 cases. Technical debt compounds.

**Action:** Refactor now. It takes 10 minutes. Adding to the mess takes the same time.

### 4. "I'll Note It But Do It Anyway"
**Pressure:** Internal rationalization that awareness = compliance

**Response:** **Noting the problem while violating the principle is still a violation.**

**Action:** Don't add the branch. Refactor instead. Comments about "should use strategy pattern" are not acceptable.

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're about to violate OCP:

- Adding `else if` to existing conditional
- Adding `case` to existing switch
- Typing the same `if/else` structure that's already there
- Thinking "I'll mention this should be refactored"
- Method has more than 3 type-based branches

**All of these mean: Create an interface and implementation instead.**

## Refactoring Existing Violations

When you encounter existing if/else chains:

```typescript
// BEFORE: 5 branches in processPayment
if (type === 'card') { ... }
else if (type === 'paypal') { ... }
else if (type === 'apple') { ... }
else if (type === 'google') { ... }
else if (type === 'crypto') { ... }

// AFTER: Strategy pattern
interface PaymentMethod { process(amount: number): boolean; }
class CardPayment implements PaymentMethod { ... }
class PayPalPayment implements PaymentMethod { ... }
// etc.
```

**Refactor on touch:** When asked to add the 6th branch, refactor instead.

## Quick Reference

| Situation | Wrong | Right |
|-----------|-------|-------|
| Add payment method | Add `else if (type === 'new')` | Create `NewPayment implements PaymentMethod` |
| Add notification channel | Add `else if (channel === 'slack')` | Create `SlackNotifier implements Notifier` |
| Add export format | Add `case 'xlsx':` | Create `XlsxExporter implements Exporter` |
| Add discount type | Add `else if (discount === 'bogo')` | Create `BogoDiscount implements DiscountStrategy` |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's just one more case" | That's what they said about the previous 5 cases. |
| "I noted it should be refactored" | Notes don't count. Refactor or don't, but don't pretend awareness is action. |
| "The code already uses if/else" | Existing violations don't justify more violations. |
| "Strategy pattern is overkill" | 3+ branches = strategy pattern is correct engineering. |
| "It's faster to add a branch" | It's not. You type the same code either way. |
| "We can refactor later" | You won't. The branch count will double. |

## The Bottom Line

**Open for extension. Closed for modification.**

When adding new functionality:
1. Create an interface (if none exists)
2. Implement the interface for the new variant
3. Register/inject the new implementation

Never add branches. Never "note it but do it anyway." Awareness without action is not compliance.
