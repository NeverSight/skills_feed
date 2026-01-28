---
name: Traits
description: This skill should be used when the user asks about "Effect Equal", "Effect Hash", "Equivalence", "Order", "structural equality", "custom equality", "comparing objects", "sorting", "Equal.equals", "Hash.hash", "Equivalence.make", "Order.lessThan", "comparable types", or needs to understand how Effect handles equality, hashing, and ordering of values.
version: 1.0.0
---

# Traits in Effect

## Overview

Effect provides trait-based abstractions for:

- **Equal** - Structural equality comparison
- **Hash** - Hash code generation
- **Equivalence** - Custom equality relations
- **Order** - Ordering and comparison

These enable consistent behavior across Effect's data structures.

## Equal - Structural Equality

### The Equal Interface

```typescript
import { Equal } from "effect"

// Check equality
Equal.equals(a, b) // true if structurally equal

// Values implement Equal automatically with Data
import { Data } from "effect"

class Person extends Data.Class<{
  name: string
  age: number
}> {}

const p1 = new Person({ name: "Alice", age: 30 })
const p2 = new Person({ name: "Alice", age: 30 })

Equal.equals(p1, p2) // true (structural equality)
p1 === p2 // false (reference equality)
```

### Implementing Equal (Recommended: Use Data.Class)

**PREFER Data.Class** which provides Equal and Hash automatically:

```typescript
import { Data, Equal } from "effect"

// Data.Class provides Equal and Hash automatically
class Point extends Data.Class<{ readonly x: number; readonly y: number }> {}

const p1 = new Point({ x: 1, y: 2 })
const p2 = new Point({ x: 1, y: 2 })

Equal.equals(p1, p2) // true - automatic structural equality!
```

For Schema types, use Schema.Class which also provides Equal:

```typescript
import { Schema, Equal } from "effect"

class Point extends Schema.Class<Point>("Point")({
  x: Schema.Number,
  y: Schema.Number
}) {}

const p1 = new Point({ x: 1, y: 2 })
const p2 = new Point({ x: 1, y: 2 })

Equal.equals(p1, p2) // true
```

### Why Equal Matters

Effect's collections (HashMap, HashSet) use Equal for lookups:

```typescript
import { HashMap, Data } from "effect"

class UserId extends Data.Class<{ id: string }> {}

const map = HashMap.make([
  [new UserId({ id: "1" }), "Alice"],
  [new UserId({ id: "2" }), "Bob"]
])

// Works because UserId implements Equal
HashMap.get(map, new UserId({ id: "1" })) // Option.some("Alice")
```

## Hash - Hash Code Generation

### The Hash Interface

```typescript
import { Hash } from "effect"

// Get hash code
Hash.hash(value) // number

// Built-in hash functions
Hash.string("hello")     // hash for string
Hash.number(42)          // hash for number
Hash.combine(h1)(h2)     // combine two hashes
Hash.array([1, 2, 3])    // hash for array
```

### Hash Contract

Objects that are Equal MUST have the same hash:

```typescript
// If Equal.equals(a, b) === true
// Then Hash.hash(a) === Hash.hash(b)

// The reverse is NOT required:
// Same hash does NOT mean equal (hash collisions are allowed)
```

### Hash with Data.Class (Recommended)

**Data.Class provides both Equal and Hash automatically:**

```typescript
import { Data, Hash, Equal } from "effect"

class Rectangle extends Data.Class<{
  readonly width: number
  readonly height: number
}> {}

const r1 = new Rectangle({ width: 10, height: 5 })
const r2 = new Rectangle({ width: 10, height: 5 })

Equal.equals(r1, r2)        // true - automatic
Hash.hash(r1) === Hash.hash(r2)  // true - automatic
```

## Equivalence - Custom Equality Relations

### Creating Equivalences

```typescript
import { Equivalence } from "effect"

// From equality function
const caseInsensitive = Equivalence.make<string>(
  (a, b) => a.toLowerCase() === b.toLowerCase()
)

caseInsensitive("Hello", "hello") // true
caseInsensitive("Hello", "HELLO") // true

// Built-in equivalences
Equivalence.string       // exact string equality
Equivalence.number       // number equality
Equivalence.boolean      // boolean equality
Equivalence.strict       // reference equality (===)
```

### Transforming Equivalences

```typescript
// Map to compare by derived value
const byLength = Equivalence.string.pipe(
  Equivalence.mapInput((s: string) => s.length.toString())
)

// Actually, better approach:
const byLength = Equivalence.make<string>(
  (a, b) => a.length === b.length
)

// Combine equivalences
const userEquivalence = Equivalence.make<User>(
  (a, b) =>
    Equivalence.string(a.name, b.name) &&
    Equivalence.number(a.age, b.age)
)
```

### Using with Collections

```typescript
import { Array as Arr } from "effect"

const users = [
  { name: "Alice", age: 30 },
  { name: "Bob", age: 25 },
  { name: "alice", age: 30 } // Same as Alice?
]

// Dedupe with custom equivalence
const byNameIgnoreCase = Equivalence.make<User>(
  (a, b) => a.name.toLowerCase() === b.name.toLowerCase()
)

const unique = Arr.dedupe(users) // Uses default equality
const uniqueByName = Arr.dedupeWith(users, byNameIgnoreCase)
```

## Order - Comparison and Sorting

### The Order Interface

```typescript
import { Order } from "effect"

// Compare two values
Order.string("a", "b")  // -1 (a < b)
Order.string("b", "a")  // 1 (a > b)
Order.string("a", "a")  // 0 (a === b)

// Comparison helpers
Order.lessThan(Order.number)(5, 10)        // true
Order.greaterThan(Order.number)(5, 10)     // false
Order.lessThanOrEqualTo(Order.number)(5, 5) // true
Order.between(Order.number)({ minimum: 0, maximum: 10 })(5) // true

// Min/max
Order.min(Order.number)(3, 7)  // 3
Order.max(Order.number)(3, 7)  // 7

// Clamp
Order.clamp(Order.number)({ minimum: 0, maximum: 100 })(150) // 100
```

### Built-in Orders

```typescript
Order.string      // Alphabetical
Order.number      // Numeric
Order.boolean     // false < true
Order.bigint      // BigInt comparison
Order.Date        // Date comparison
```

### Creating Custom Orders

```typescript
// From compare function
const byAge = Order.make<Person>((a, b) =>
  a.age < b.age ? -1 : a.age > b.age ? 1 : 0
)

// From mapper (compare by derived value)
const byName = Order.mapInput(Order.string, (p: Person) => p.name)
const byAge = Order.mapInput(Order.number, (p: Person) => p.age)
```

### Combining Orders

```typescript
// Combine orders (first by age, then by name)
const byAgeThenName = Order.combine(
  byAge,
  byName
)

// Reverse order
const byAgeDesc = Order.reverse(byAge)

// All combinators
const sortUsers = Order.combine(
  Order.mapInput(Order.string, (u: User) => u.department),
  Order.combine(
    Order.reverse(Order.mapInput(Order.number, (u: User) => u.salary)),
    Order.mapInput(Order.string, (u: User) => u.name)
  )
)
```

### Sorting with Order

```typescript
import { Array as Arr } from "effect"

const people = [
  { name: "Charlie", age: 35 },
  { name: "Alice", age: 30 },
  { name: "Bob", age: 30 }
]

// Sort by age
const byAge = Arr.sort(people, Order.mapInput(Order.number, (p) => p.age))

// Sort by age then name
const sorted = Arr.sort(people, Order.combine(
  Order.mapInput(Order.number, (p) => p.age),
  Order.mapInput(Order.string, (p) => p.name)
))
// [{ name: "Alice", age: 30 }, { name: "Bob", age: 30 }, { name: "Charlie", age: 35 }]
```

## Data.Class - Automatic Implementation

Using `Data.Class` automatically implements Equal and Hash:

```typescript
import { Data, Equal, Hash } from "effect"

class User extends Data.Class<{
  id: string
  name: string
  email: string
}> {}

const u1 = new User({ id: "1", name: "Alice", email: "a@example.com" })
const u2 = new User({ id: "1", name: "Alice", email: "a@example.com" })

Equal.equals(u1, u2) // true
Hash.hash(u1) === Hash.hash(u2) // true
```

## Best Practices

1. **Use Data.Class for value objects** - Automatic Equal/Hash
2. **Implement both Equal and Hash together** - Required for collections
3. **Use Order.mapInput for simple ordering** - Cleaner than manual comparison
4. **Combine orders for complex sorting** - More composable than custom compare
5. **Consider Equivalence for custom equality** - When default equality isn't enough

## Additional Resources

For comprehensive trait documentation, consult `${CLAUDE_PLUGIN_ROOT}/references/llms-full.txt`.

Search for these sections:
- "Equal" for equality comparison
- "Hash" for hash code generation
- "Equivalence" for custom equality relations
- "Order" for ordering and comparison
