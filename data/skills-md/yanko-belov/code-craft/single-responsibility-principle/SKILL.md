---
name: single-responsibility-principle
description: Use when creating or modifying classes, modules, or functions. Use when feeling pressure to add functionality to existing code. Use when class has multiple reasons to change.
---

# Single Responsibility Principle (SRP)

## Overview

**A class should have only one reason to change.**

Every module, class, or function should have responsibility over a single part of functionality. If you can describe what a class does using "AND", it has too many responsibilities.

## When to Use

- Creating any new class, module, or service
- Adding methods to existing classes
- Reviewing code that "does multiple things"
- Feeling pressure to "just add it here"

## The Iron Rule

```
NEVER add functionality that introduces a second reason to change.
```

**No exceptions:**
- Not for "it's faster this way"
- Not for "it's just one more method"
- Not for "refactoring would take too long"
- Not for "my tech lead said so"
- Not for "it's already in production"

**Violating SRP under pressure is still violating SRP.**

## Detection: The "AND" Test

Describe your class in one sentence. If it contains "AND", split it.

| Description | Verdict |
|-------------|---------|
| "Handles user authentication" | ✅ Single responsibility |
| "Handles authentication AND sends emails" | ❌ Two responsibilities |
| "Manages orders AND processes payments AND tracks inventory" | ❌ Three responsibilities |

## Detection: Reasons to Change

List why this class might need to change:

```typescript
// ❌ BAD: UserManager - 4 reasons to change
class UserManager {
  login() {}           // Auth logic changes
  updateProfile() {}   // Profile requirements change  
  sendEmail() {}       // Email provider changes
  trackAnalytics() {}  // Analytics requirements change
}

// ✅ GOOD: Split by responsibility
class AuthService { login() {} }
class ProfileService { updateProfile() {} }
class NotificationService { sendEmail() {} }
class AnalyticsService { track() {} }
```

## Pressure Resistance Protocol

When pressured to violate SRP, follow this:

### 1. Time Pressure
"Just make it work quickly"

**Response:** Creating a god class takes the same time as creating focused classes. The "quick" solution creates technical debt that costs 10x more later.

**Action:** Create separate classes. It's not slower.

### 2. Sunk Cost Pressure  
"The class already exists, just add to it"

**Response:** Adding to a bloated class makes it worse. The fact that it's already wrong doesn't justify making it more wrong.

**Action:** Create a new focused class. Refactor the existing one if time permits.

### 3. Authority Pressure
"My tech lead said put it all in one class"

**Response:** Respectfully push back with evidence. If overruled, document your concern and comply—but NEVER silently create god classes.

**Action:** 
```
"I'd recommend splitting this because [specific reason]. 
If we keep it together, we'll likely need to refactor when [consequence].
Should I proceed with the split, or document this as tech debt?"
```

### 4. Scope Creep
"While you're in there, also add X"

**Response:** New functionality = new class (or existing appropriate class).

**Action:** "X belongs in its own service. I'll create XService."

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're about to violate SRP:

- Adding a method unrelated to the class's core purpose
- Class file exceeds 200 lines
- Class has more than 5-7 public methods
- You need section comments to navigate the class
- Multiple developers would edit this class for unrelated features
- Class name contains "Manager", "Handler", "Processor", "Service" with no specific domain

**All of these mean: Split the class.**

## Refactoring Existing Violations

When you encounter an existing god class:

1. **Don't make it worse** - Never add more responsibilities
2. **Extract on touch** - When modifying, extract the part you're touching
3. **Document debt** - If you can't refactor now, create a ticket

```typescript
// Found: OrderService with 500 lines handling orders, payments, inventory, emails

// ❌ WRONG: Add shipping logic to OrderService
// ✅ RIGHT: Create ShippingService, note that OrderService needs refactoring
```

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's faster to put it in one class" | It's not. You type the same code either way. |
| "Small classes are over-engineering" | Small classes are correct engineering. |
| "It's just one more method" | That's how god classes start. Every time. |
| "We can refactor later" | You won't. Tech debt compounds. |
| "The class is already big" | That's a reason to stop, not continue. |
| "It's related functionality" | Related ≠ same responsibility. |
| "Section comments help navigate" | If you need navigation, class is too big. |

## Quick Reference

| Symptom | Action |
|---------|--------|
| Class does X AND Y | Split into XService and YService |
| Adding unrelated method | Create new class |
| File > 200 lines | Look for extraction opportunities |
| Multiple reasons to change | One class per reason |
| "Manager/Handler/Processor" name | Be more specific or split |

## The Bottom Line

**One class. One responsibility. One reason to change.**

When pressured to violate this: push back, document, or create the right structure anyway. 

God classes are never the answer, regardless of time pressure, existing code, or authority demands.
