---
name: refactor
description: Refactor code for quality, reduce technical debt, and improve maintainability. Use for cleanup tasks and code improvements.
---

# Code Refactoring

Improve code quality without changing behavior.

## When to Use

- Code is hard to understand or modify
- Duplicated logic across files
- Functions/classes are too large
- Technical debt reduction
- Before adding new features

## Refactoring Process

1. **Ensure tests exist** - Add tests before refactoring
2. **Small steps** - Make incremental changes
3. **Run tests** - Verify after each change
4. **Commit often** - Keep changes reversible

## Common Refactorings

### Extract Function

```javascript
// Before
function processOrder(order) {
  // 50 lines of validation
  // 30 lines of calculation
  // 20 lines of notification
}

// After
function processOrder(order) {
  validateOrder(order);
  const total = calculateTotal(order);
  notifyCustomer(order, total);
}
```

### Replace Conditionals with Polymorphism

```javascript
// Before
function getPrice(type) {
  if (type === "regular") return basePrice;
  if (type === "premium") return basePrice * 1.5;
  if (type === "vip") return basePrice * 0.8;
}

// After
const pricingStrategies = {
  regular: (base) => base,
  premium: (base) => base * 1.5,
  vip: (base) => base * 0.8,
};
const getPrice = (type) => pricingStrategies[type](basePrice);
```

### Remove Duplication

```javascript
// Before
function getUserName(user) {
  return user?.profile?.name ?? "Unknown";
}
function getOrderName(order) {
  return order?.customer?.name ?? "Unknown";
}

// After
const getName = (obj, path) => path.reduce((o, k) => o?.[k], obj) ?? "Unknown";
const getUserName = (user) => getName(user, ["profile", "name"]);
const getOrderName = (order) => getName(order, ["customer", "name"]);
```

## Code Smells

| Smell               | Symptom                 | Refactoring          |
| ------------------- | ----------------------- | -------------------- |
| Long Function       | >20 lines               | Extract Function     |
| Large Class         | >200 lines              | Extract Class        |
| Duplicate Code      | Same logic repeated     | Extract and reuse    |
| Long Parameter      | >3 params               | Use object/builder   |
| Feature Envy        | Uses other class's data | Move method          |
| Primitive Obsession | Strings for everything  | Create value objects |

## Quality Metrics

- **Cyclomatic Complexity** - Keep under 10 per function
- **Nesting Depth** - Max 3 levels
- **Function Length** - Under 20 lines preferred
- **File Length** - Under 300 lines preferred

## Safety Checklist

- [ ] Tests exist and pass
- [ ] No behavior changes intended
- [ ] Changes are incremental
- [ ] Each step is committed
- [ ] Code review requested

## Examples

**Input:** "This function is too long"
**Action:** Identify logical sections, extract into focused functions, verify tests pass

**Input:** "Reduce duplication in these files"
**Action:** Find common patterns, extract shared utilities, update call sites
