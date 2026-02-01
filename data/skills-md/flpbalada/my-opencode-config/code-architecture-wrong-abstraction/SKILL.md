---
name: code-architecture-wrong-abstraction
description: Guides when to abstract vs duplicate code. Use this skill when creating shared utilities, deciding between DRY/WET approaches, or refactoring existing abstractions.
---

# Code Architecture: Avoiding Wrong Abstractions

## Core Principle

**Prefer duplication over the wrong abstraction. Wait for patterns to emerge before abstracting.**

Premature abstraction creates confusing, hard-to-maintain code. Duplication is far cheaper to fix than unwinding a wrong abstraction.

## The Rule of Three

Don't abstract until code appears in **at least 3 places**. This provides enough context to identify genuine patterns vs coincidental similarities.

```jsx
// ✅ Correct: Wait for the pattern to emerge
// First occurrence - just write it
const userTotal = items.reduce((sum, item) => sum + item.price, 0);

// Second occurrence - still duplicate
const cartTotal = products.reduce((sum, p) => sum + p.price, 0);

// Third occurrence - NOW consider abstraction
const calculateTotal = (items, priceKey = 'price') =>
  items.reduce((sum, item) => sum + item[priceKey], 0);
```

## When to Abstract

### ✅ Abstract When

- Same code appears in **3+ places**
- Pattern has **stabilized** (requirements are clear)
- Abstraction **simplifies** understanding
- Use cases share **identical behavior**, not just similar structure

### ❌ Don't Abstract When

- Code only appears in 1-2 places
- Requirements are still evolving
- Use cases need **different behaviors** (even if structure looks similar)
- Abstraction would require parameters/conditionals for variations

## The Wrong Abstraction Pattern

This is how wrong abstractions evolve:

```jsx
// 1️⃣ Developer A spots duplication and extracts it
function processData(data) {
  return data.map(transform).filter(validate);
}

// 2️⃣ New requirement is "almost" compatible
function processData(data, options = {}) {
  let result = data.map(options.customTransform || transform);
  if (options.skipValidation) return result;
  return result.filter(options.customValidate || validate);
}

// 3️⃣ More variations pile up...
function processData(data, options = {}) {
  let result = data;
  if (options.preProcess) result = options.preProcess(result);
  result = result.map(options.customTransform || transform);
  if (!options.skipValidation) {
    result = result.filter(options.customValidate || validate);
  }
  if (options.postProcess) result = options.postProcess(result);
  if (options.sort) result = result.sort(options.sortFn);
  return options.limit ? result.slice(0, options.limit) : result;
}

// ❌ Now it's incomprehensible spaghetti
```

## How to Fix Wrong Abstractions

The fastest way forward is **back**:

1. **Inline** the abstraction back into each caller
2. **Delete** the portions each caller doesn't need
3. **Accept** temporary duplication for clarity
4. **Re-extract** proper abstractions based on current understanding

```jsx
// Before: One bloated function trying to do everything
processData(users, { customTransform: formatUser, skipValidation: true });
processData(orders, { sort: true, sortFn: byDate, limit: 10 });

// After: Inline and simplify each use case
const formattedUsers = users.map(formatUser);
const recentOrders = orders.sort(byDate).slice(0, 10);

// Later: If true patterns emerge, abstract properly
```

## Hidden Costs of Abstraction

| Benefit | Hidden Cost |
|---------|-------------|
| Code reuse | **Accidental coupling** between unrelated modules |
| Single source of truth | **Layers of indirection** obscure bugs |
| DRY compliance | **Organizational inertia** makes refactoring painful |

## Facade Pattern: When It Becomes a Wrong Abstraction

Facades wrap complex subsystems behind a simple interface. They're useful but often become wrong abstractions when overused.

### The Typography Component Trap

```tsx
// ❌ Facade that becomes limiting
<Typography variant="body" size="sm">Hello</Typography>

// What if you need <small> or <mark>?
// Now you must extend the facade first:
<Typography variant="body" size="sm" as="small">Hello</Typography>  // Added prop
<Typography variant="body" size="sm" as="mark">Hello</Typography>   // Another prop

// ❌ Facade keeps growing with every edge case
type TypographyProps = {
  variant: 'h1' | 'h2' | 'body' | 'caption';
  size: 'sm' | 'md' | 'lg';
  as?: 'p' | 'span' | 'small' | 'mark' | 'strong' | 'em';  // Growing...
  weight?: 'normal' | 'bold';
  color?: 'primary' | 'secondary' | 'muted';
  // ... more props for every HTML text feature
};
```

### When Facade Works

```tsx
// ✅ Good: Facade encapsulates complex logic
<DatePicker
  value={date}
  onChange={setDate}
  minDate={today}
/>
// Hides: localization, calendar rendering, keyboard nav, accessibility

// ✅ Good: Facade enforces design system constraints
<Button variant="primary" size="md">Submit</Button>
// Ensures consistent styling, no arbitrary colors
```

### When to Skip the Facade

```tsx
// ✅ Sometimes native HTML is clearer
<small className="text-muted">Fine print</small>
<mark>Highlighted text</mark>

// vs forcing everything through a facade:
<Typography variant="small" highlight>...</Typography>  // ❌ Overengineered
```

### Facade Trade-offs

| Use Facade When | Skip Facade When |
|-----------------|------------------|
| Hiding **complex logic** (APIs, state) | Wrapping **simple HTML elements** |
| Enforcing **design constraints** | One-off styling needs |
| Team needs **consistent patterns** | Juniors need to learn the underlying tech |
| Behavior is **stable and well-defined** | Requirements are still evolving |

### The Junior Developer Test

If a junior must:
1. Learn the facade API
2. Then learn the underlying technology anyway
3. Then extend the facade for edge cases

...the facade adds friction, not value. Sometimes `ctrl+f` and manual updates across files is simpler than maintaining a leaky abstraction.

## Quick Reference

### DO

- Wait for **3+ occurrences** before abstracting
- Let patterns **emerge naturally**
- Optimize for **changeability**, not DRY compliance
- Test **concrete features**, not abstractions
- **Inline bad abstractions** and start fresh

### DON'T

- Abstract based on **structural similarity** alone
- Add parameters/conditionals to **force fit** new use cases
- Preserve abstractions due to **sunk cost fallacy**
- Fear **temporary duplication**

## Key Philosophies

| Approach | Meaning | When to Use |
|----------|---------|-------------|
| **DRY** | Don't Repeat Yourself | After patterns stabilize |
| **WET** | Write Everything Twice | Default starting point |
| **AHA** | Avoid Hasty Abstractions | Guiding principle |

## References

- [The Wrong Abstraction - Sandi Metz](https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction)
- [The Wet Codebase - Dan Abramov](https://www.deconstructconf.com/2019/dan-abramov-the-wet-codebase)
- [AHA Programming - Kent C. Dodds](https://kentcdodds.com/blog/aha-programming)
