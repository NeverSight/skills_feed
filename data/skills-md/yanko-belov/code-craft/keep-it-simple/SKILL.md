---
name: keep-it-simple
description: Use when tempted to write clever code. Use when solution feels complex. Use when showing off skills instead of solving problems.
---

# KISS (Keep It Simple, Stupid)

## Overview

**The simplest solution that works is the best solution.**

Clever code impresses no one. Simple code ships faster, breaks less, and others can maintain it.

## When to Use

- Solution feels complex
- Writing "elegant" or "clever" code
- Multiple approaches exist
- Tempted to show off skills
- Using advanced patterns for simple problems

## The Iron Rule

```
NEVER choose clever over clear. Simple wins.
```

**No exceptions:**
- Not for "it's more elegant"
- Not for "it shows advanced skills"
- Not for "it's technically better"
- Not for "it's a nice one-liner"

## Detection: The "Clever" Smell

If you're proud of how clever your code is, simplify it:

```typescript
// ❌ VIOLATION: Clever one-liner
const isPalindrome = (s: string): boolean =>
  (s = s.toLowerCase().replace(/[^a-z0-9]/g, '')) === [...s].reverse().join('');

// ✅ CORRECT: Simple and clear
function isPalindrome(str: string): boolean {
  const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
  
  for (let i = 0; i < cleaned.length / 2; i++) {
    if (cleaned[i] !== cleaned[cleaned.length - 1 - i]) {
      return false;
    }
  }
  
  return true;
}
```

## The Cost of Complexity

| Complex Code | Impact |
|--------------|--------|
| Clever one-liners | Unreadable, hard to debug |
| Nested ternaries | Logic becomes opaque |
| Over-abstraction | Indirection hides intent |
| Premature optimization | Complexity without measured benefit |
| Design pattern overuse | Patterns for patterns' sake |

## Correct Pattern: Obvious Code

Write code that a junior developer can understand in 30 seconds:

```typescript
// ❌ COMPLEX: "Elegant" functional chain
const result = data
  .filter(Boolean)
  .map(x => transform(x))
  .reduce((acc, x) => ({ ...acc, [x.id]: x }), {})
  .values()
  .filter(x => x.active)
  .sort((a, b) => b.date - a.date)
  .slice(0, 10);

// ✅ SIMPLE: Clear steps with names
const validItems = data.filter(Boolean);
const transformed = validItems.map(transform);
const activeItems = transformed.filter(item => item.active);
const sorted = activeItems.sort((a, b) => b.date - a.date);
const topTen = sorted.slice(0, 10);
```

## Pressure Resistance Protocol

### 1. "It's More Elegant"
**Pressure:** "This one-liner is more elegant than the verbose version"

**Response:** Elegance is clarity, not brevity. Simple code is more elegant than clever code.

**Action:** Use the clear version. Name intermediate variables.

### 2. "It Shows Advanced Skills"
**Pressure:** "I want to demonstrate I know advanced patterns"

**Response:** Senior engineers are recognized for simple solutions, not complex ones.

**Action:** Solve the problem simply. Save cleverness for where it's needed.

### 3. "It's Technically Better"
**Pressure:** "The complex version is O(n) vs O(n log n)"

**Response:** Premature optimization. Is this actually a bottleneck?

**Action:** Write simple code. Optimize only when profiling shows need.

### 4. "Let Me Show Multiple Approaches"
**Pressure:** "I'll provide two implementations to show versatility"

**Response:** One clear solution is better than multiple options.

**Action:** Pick the simplest approach. Provide only that.

## Red Flags - STOP and Reconsider

If you notice ANY of these, simplify:

- Code requires explanation comments
- Nested ternaries `? : ? :`
- Multiple chained operations (5+)
- Regex that needs decoding
- Proud of how clever it is
- "One-liner" implementations
- Junior couldn't understand in 30 seconds
- Multiple solutions "for versatility"

**All of these mean: Rewrite simply.**

## Simplification Techniques

| Complex | Simple |
|---------|--------|
| Nested ternaries | if/else statements |
| Long chains | Named intermediate variables |
| Clever regex | Multiple simple checks |
| One-liner | Multi-line with comments |
| Implicit | Explicit |
| Magic numbers | Named constants |

## Quick Reference

| Symptom | Action |
|---------|--------|
| "Elegant" one-liner | Expand to clear multi-line |
| Nested ternary | Convert to if/else |
| Complex chain | Break into named steps |
| Multiple approaches | Pick simplest one |
| Pride in cleverness | Rewrite simply |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "It's more elegant" | Clear code is more elegant than clever code. |
| "Shows advanced skills" | Simple solutions show more skill. |
| "It's a nice one-liner" | One-liners are often unreadable. |
| "Technically better" | Premature optimization is bad. |
| "Multiple options show versatility" | One clear solution is better. |
| "It's how experts do it" | Experts write simple code. |

## The Bottom Line

**Simple beats clever. Clear beats concise. Obvious beats elegant.**

When solving a problem: find the simplest solution that works. If a junior dev can't understand it in 30 seconds, simplify it.
