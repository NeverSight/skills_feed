---
name: dont-repeat-yourself
description: Use when writing similar code in multiple places. Use when copy-pasting code. Use when making the same change in multiple locations.
---

# DRY (Don't Repeat Yourself)

## Overview

**Every piece of knowledge must have a single, unambiguous representation in the system.**

If you find yourself writing the same logic twice, extract it. Duplication is a bug waiting to happen.

## When to Use

- Writing code similar to existing code
- Copy-pasting and modifying
- Making the same change in multiple files
- Validation logic repeated across forms
- Same calculations in different places

## The Iron Rule

```
NEVER duplicate logic. Extract and reuse.
```

**No exceptions:**
- Not for "it's faster to copy"
- Not for "they're slightly different"
- Not for "I'll refactor later"
- Not for "it's just a few lines"

## Detection: The Copy-Paste Smell

If you're about to copy code and modify it, STOP:

```typescript
// ❌ VIOLATION: Duplicated validation
function validateRegistrationEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function validateProfileEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email); // Same logic!
}

// ✅ CORRECT: Single source of truth
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Reuse everywhere
const isValidRegistration = validateEmail(regEmail);
const isValidProfile = validateEmail(profileEmail);
```

## Detection: The "Change in Multiple Places" Test

If fixing a bug requires changing multiple locations, you have duplication:

```typescript
// ❌ Bug in tax calculation requires changes in 3 files
// cart.ts:      const tax = price * 0.08;
// checkout.ts:  const tax = price * 0.08;
// invoice.ts:   const tax = price * 0.08;

// ✅ Single source of truth
// tax.ts:       export const calculateTax = (price: number) => price * TAX_RATE;
```

## The Correct Pattern: Extract and Parameterize

When code is "almost the same", extract the common part and parameterize the differences:

```typescript
// ❌ VIOLATION: Similar functions with minor differences
function formatUserName(user: User): string {
  return `${user.firstName} ${user.lastName}`;
}

function formatAdminName(admin: Admin): string {
  return `${admin.firstName} ${admin.lastName} (Admin)`;
}

// ✅ CORRECT: Parameterized
function formatName(person: { firstName: string; lastName: string }, suffix?: string): string {
  const name = `${person.firstName} ${person.lastName}`;
  return suffix ? `${name} (${suffix})` : name;
}
```

## Pressure Resistance Protocol

### 1. "It's Faster to Copy"
**Pressure:** "I'll just copy this and modify it"

**Response:** Copying creates two places to maintain. Bugs will diverge.

**Action:** Extract shared logic first, then use it in both places.

### 2. "They're Slightly Different"
**Pressure:** "The functions are almost the same but not quite"

**Response:** "Almost the same" = extract common part, parameterize differences.

**Action:** Identify what's shared, extract it, make differences parameters.

### 3. "It's Just a Few Lines"
**Pressure:** "It's only 3 lines, not worth extracting"

**Response:** 3 lines duplicated 5 times = 15 lines to maintain. Bugs multiply.

**Action:** Extract even small duplications. Name them well.

### 4. "I'll Refactor Later"
**Pressure:** "Ship now, DRY it up later"

**Response:** You won't. Duplication spreads. DRY now takes 2 minutes.

**Action:** Extract before committing the duplication.

## Red Flags - STOP and Reconsider

If you notice ANY of these, you're about to violate DRY:

- Ctrl+C / Ctrl+V in your workflow
- "This is similar to that other function"
- Same regex/validation in multiple places
- Identical error handling patterns repeated
- Same data transformation logic duplicated
- Constants defined in multiple files

**All of these mean: Extract to a shared location.**

## Types of Duplication

| Type | Example | Solution |
|------|---------|----------|
| **Code** | Same function body twice | Extract function |
| **Logic** | Same algorithm, different names | Extract and parameterize |
| **Data** | Same constant in multiple files | Centralize constants |
| **Structure** | Same class shape repeated | Extract interface/base |
| **Knowledge** | Business rule in multiple places | Single source of truth |

## Quick Reference

| Symptom | Action |
|---------|--------|
| Copy-pasting code | Extract shared function |
| Same validation twice | Create validator module |
| Same constant in files | Create constants file |
| Similar functions | Extract + parameterize |
| Bug fix needs multiple changes | Consolidate to one place |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's faster to copy" | It's slower to maintain duplicates. |
| "They're slightly different" | Extract common, parameterize differences. |
| "Just a few lines" | Few lines × many places = many bugs. |
| "I'll refactor later" | You won't. Extract now. |
| "Different contexts" | Same logic = same code, regardless of context. |
| "More readable as copies" | Named, extracted functions are more readable. |

## The Bottom Line

**One piece of knowledge. One place in code.**

When writing similar code: stop, find the existing code, extract if needed, reuse. Duplication is the root of maintenance nightmares.
