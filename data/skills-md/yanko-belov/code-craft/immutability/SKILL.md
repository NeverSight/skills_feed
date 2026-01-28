---
name: immutability
description: Use when modifying objects or arrays. Use when tempted to mutate function parameters. Use when state changes cause unexpected bugs.
---

# Immutability

## Overview

**Never mutate. Always return new objects.**

Mutation causes bugs that are hard to track - when objects change unexpectedly, debugging becomes a nightmare. Immutability makes state changes explicit and predictable.

## When to Use

- Modifying objects or arrays
- Updating state in React/Redux
- Function receives object as parameter
- Data shared between multiple parts of code

## The Iron Rule

```
NEVER mutate objects or arrays. ALWAYS return new copies with changes.
```

**No exceptions:**
- Not for "it's more efficient"
- Not for "it's simpler"
- Not for "it's just one property"
- Not for "no one else uses this object"

## Detection: Mutation Smell

If you're modifying an object directly, STOP:

```typescript
// ❌ VIOLATION: Direct mutation
function updateUserAddress(user: User, newCity: string): User {
  user.address.city = newCity;  // Mutates original!
  return user;
}

// ❌ VIOLATION: Array mutation
function addItem(cart: CartItem[], item: CartItem): CartItem[] {
  cart.push(item);  // Mutates original!
  return cart;
}

// ❌ VIOLATION: Nested mutation
function updateSettings(config: Config): Config {
  config.settings.theme = 'dark';  // Deep mutation!
  return config;
}
```

Problems:
- Original object changed unexpectedly
- React won't detect changes (same reference)
- Debugging nightmare - "who changed this?"
- Undo/redo impossible

## The Correct Pattern: Return New Objects

```typescript
// ✅ CORRECT: Return new object
function updateUserAddress(user: User, newCity: string): User {
  return {
    ...user,
    address: {
      ...user.address,
      city: newCity
    }
  };
}

// ✅ CORRECT: Return new array
function addItem(cart: CartItem[], item: CartItem): CartItem[] {
  return [...cart, item];
}

// ✅ CORRECT: Deep immutable update
function updateSettings(config: Config): Config {
  return {
    ...config,
    settings: {
      ...config.settings,
      theme: 'dark'
    }
  };
}

// Usage - originals unchanged
const user = { name: 'Alice', address: { city: 'Boston' } };
const updatedUser = updateUserAddress(user, 'Cambridge');

console.log(user.address.city);        // 'Boston' - unchanged!
console.log(updatedUser.address.city); // 'Cambridge' - new object
```

## Immutable Operations

### Objects
```typescript
// Update property
const updated = { ...obj, property: newValue };

// Remove property
const { removed, ...rest } = obj;

// Merge objects
const merged = { ...obj1, ...obj2 };
```

### Arrays
```typescript
// Add item
const added = [...arr, newItem];
const prepended = [newItem, ...arr];

// Remove item
const removed = arr.filter(item => item.id !== idToRemove);

// Update item
const updated = arr.map(item => 
  item.id === id ? { ...item, ...changes } : item
);

// Sort (creates new array)
const sorted = [...arr].sort((a, b) => a.value - b.value);
```

### Nested Updates
```typescript
// Deep update helper
const updated = {
  ...state,
  users: {
    ...state.users,
    [userId]: {
      ...state.users[userId],
      name: newName
    }
  }
};

// Or use immer for complex updates
import { produce } from 'immer';

const updated = produce(state, draft => {
  draft.users[userId].name = newName;  // Looks mutable, but isn't
});
```

## Pressure Resistance Protocol

### 1. "It's More Efficient"
**Pressure:** "Creating new objects is wasteful"

**Response:** Modern JS engines optimize this. The bugs from mutation cost more than the memory.

**Action:** Use immutable patterns. Profile if you suspect performance issues.

### 2. "It's Simpler"
**Pressure:** "Direct mutation is easier to read"

**Response:** Simple to write, hard to debug. Immutability is simpler in the long run.

**Action:** Spread operators are not complex. Use them.

### 3. "It's Just One Property"
**Pressure:** "I'm only changing one field"

**Response:** One mutation sets a precedent. Others follow. Bugs multiply.

**Action:** All updates return new objects. No exceptions.

### 4. "No One Else Uses This"
**Pressure:** "This object is local, mutation is safe"

**Response:** Code evolves. Local becomes shared. Build the habit now.

**Action:** Always immutable, regardless of current usage.

## Red Flags - STOP and Reconsider

- `obj.property = value` (direct assignment)
- `array.push()`, `array.pop()`, `array.splice()`
- `array.sort()` without spreading first
- Modifying function parameters
- `delete obj.property`

**All of these mean: Rewrite immutably.**

## Quick Reference

| Mutable (Bad) | Immutable (Good) |
|---------------|------------------|
| `obj.x = y` | `{ ...obj, x: y }` |
| `arr.push(x)` | `[...arr, x]` |
| `arr.pop()` | `arr.slice(0, -1)` |
| `arr.splice(i, 1)` | `arr.filter((_, idx) => idx !== i)` |
| `arr.sort()` | `[...arr].sort()` |
| `delete obj.x` | `const { x, ...rest } = obj` |

## Common Rationalizations (All Invalid)

| Excuse | Reality |
|--------|---------|
| "More efficient" | Bugs cost more than memory. |
| "Simpler" | Simpler to write, harder to debug. |
| "Just one property" | One exception leads to many. |
| "No one else uses it" | Code changes. Be consistent. |
| "Too verbose" | Spread syntax is concise. |
| "React handles it" | React needs new references to detect changes. |

## The Bottom Line

**Never mutate. Spread and return new objects.**

Every modification returns a new object. Original data stays unchanged. This enables debugging, undo/redo, React change detection, and sanity.
