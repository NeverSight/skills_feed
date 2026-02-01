---
name: react-key-prop
description: Guides proper usage of the key prop in React lists. Use this skill when rendering lists, mapping arrays to components, or troubleshooting list-related state bugs.
---

# React: Key Prop Best Practices

## Core Principle

**Use stable, unique IDs from your data. Never use array index for dynamic lists.**

The `key` prop provides stable identity to list elements during React's reconciliation process.

## When to Use What

### Use Data IDs (Preferred)

Always use unique, stable identifiers directly from your data:

```jsx
// ✅ Correct
{todos.map((todo) => (
  <li key={todo.id}>{todo.text}</li>
))}
```

Ideal keys are:
- **Unique** - No two items share the same key
- **Stable** - Never changes during component lifetime
- **Predictable** - Directly tied to the data item

### Generate IDs on Data Load

When data lacks IDs, create them **once** when receiving data:

```jsx
import { nanoid } from 'nanoid';

useEffect(() => {
  fetch('/api/items')
    .then(res => res.json())
    .then(data => {
      const itemsWithIds = data.map(item => ({
        ...item,
        _tempId: nanoid() // Stable ID generated once
      }));
      setItems(itemsWithIds);
    });
}, []);
```

### When Index Is Acceptable (Rare)

Index as key is acceptable ONLY when ALL conditions are met:
- List is absolutely static
- Items never added/removed (except at the end)
- Order never changes
- Items have no internal state

## Anti-Patterns to Avoid

### Never Generate Keys During Render

```jsx
// ❌ WRONG: Creates new key every render
{items.map(item => (
  <li key={Math.random()}>{item.name}</li>
))}
```

This forces React to destroy and recreate all components on every render.

### Don't Use Index for Dynamic Lists

```jsx
// ❌ WRONG for dynamic lists
{items.map((item, index) => (
  <li key={index}>{item.name}</li>
))}
```

Index fails when:
- Items are added/removed from beginning or middle
- List order changes (sorting, filtering)
- Items have internal state (like form inputs)

**The bug:** Index represents position, not data identity. When positions change but indexes stay the same, React incorrectly "mutates" existing components instead of creating new ones, causing state mismatch.

### Don't Use `useId()` for List Keys

React's `useId()` hook is for accessibility (linking labels to inputs), not for generating list keys.

## Quick Reference

### DO
- Always use `key` when rendering lists
- Prefer unique, stable `id` from your data
- Generate IDs once at data load time (`nanoid`/`uuid`)

### DON'T
- Never generate `key` during render (`Math.random()`, `Date.now()`)
- Avoid `index` as `key` for dynamic lists
- Don't use `useId()` for list keys

## References

- [React Docs - Rendering Lists](https://react.dev/learn/rendering-lists#keeping-list-items-in-order-with-key)
- [nanoid - Tiny ID generator](https://github.com/ai-cookie/nanoid)
