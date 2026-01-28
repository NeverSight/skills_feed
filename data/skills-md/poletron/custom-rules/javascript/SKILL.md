---
name: javascript
description: >
  Modern JavaScript ES6+ patterns and best practices.
  Trigger: When writing JavaScript for web applications.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with javascript"

## When to Use

Use this skill when:
- Writing modern ES6+ JavaScript
- Working with async/await patterns
- Using modules and imports
- Implementing functional patterns

---

## Critical Patterns

### Async/Await (REQUIRED)

```javascript
// ✅ ALWAYS: Use async/await over .then() chains
async function fetchUserData(userId) {
  try {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) throw new Error('User not found');
    return await response.json();
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}

// ❌ NEVER: Nested .then() chains
fetch(`/api/users/${userId}`)
  .then(res => res.json())
  .then(user => fetch(`/api/orders/${user.id}`))
  .then(res => res.json())
  .then(orders => { ... });
```

### Destructuring (REQUIRED)

```javascript
// ✅ ALWAYS: Use destructuring for cleaner code
const { name, email, role = 'user' } = user;
const [first, second, ...rest] = items;

// Function parameters
function createUser({ name, email, role = 'user' }) {
  return { id: uuid(), name, email, role };
}
```

### Optional Chaining (REQUIRED)

```javascript
// ✅ ALWAYS: Use optional chaining for safe access
const street = user?.address?.street ?? 'Unknown';

// ❌ NEVER: Long && chains
const street = user && user.address && user.address.street;
```

---

## Decision Tree

```
Need default value?        → Use ?? (nullish coalescing)
Need safe property?        → Use ?. (optional chaining)
Need array transform?      → Use map/filter/reduce
Need unique values?        → Use Set
Need key-value pairs?      → Use Map
Need immutable update?     → Use spread operator
```

---

## Code Examples

### Array Methods

```javascript
// Map, filter, reduce
const activeUsers = users
  .filter(u => u.active)
  .map(u => ({ id: u.id, name: u.name }));

const total = items.reduce((sum, item) => sum + item.price, 0);

// Find and includes
const admin = users.find(u => u.role === 'admin');
const hasAdmin = users.some(u => u.role === 'admin');
```

### Object Patterns

```javascript
// Spread for immutable updates
const updated = { ...user, name: 'New Name' };

// Computed property names
const key = 'dynamicKey';
const obj = { [key]: 'value' };

// Object shorthand
const name = 'John';
const user = { name, active: true };
```

---

## Commands

```bash
node script.js               # Run script
npm init -y                   # Initialize package.json
npm install package           # Install dependency
npx eslint .                  # Lint code
```

---

## Resources

- **Express API**: [express-api.md](express-api.md)
