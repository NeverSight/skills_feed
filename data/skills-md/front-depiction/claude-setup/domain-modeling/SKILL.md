---
name: domain-modeling
description: Create production-ready Effect domain models using Schema.TaggedStruct for ADTs, Schema.Data for automatic equality, with comprehensive predicates, orders, guards, and match functions. Use when modeling domain entities, value objects, or any discriminated union types.
---

# Effect Domain Modeling Skill

Use this skill when creating domain models, entities, value objects, or any types that represent core business concepts. This skill covers the complete lifecycle from type definition to runtime utilities.

## Core Pattern: Schema.TaggedStruct + Schema.Data

The foundation of Effect domain modeling combines three key features:

1. **Schema.TaggedStruct** - Automatic `_tag` discriminator for union types
2. **Schema.Data** - Automatic `Equal` implementation for structural equality
3. **Schema.decodeSync** - Type-safe constructors with validation

```typescript
import { Schema, Equal } from "effect"

// Define each variant with TaggedStruct
export const Pending = Schema.TaggedStruct("pending", {
  id: Schema.String,
  createdAt: Schema.DateTimeUtcFromSelf,
}).pipe(
  Schema.Data, // Automatic Equal.Symbol implementation
  Schema.annotations({
    identifier: "Pending",
    title: "Pending Task",
    description: "A task that has been created but not yet started",
  })
)

export const Active = Schema.TaggedStruct("active", {
  id: Schema.String,
  createdAt: Schema.DateTimeUtcFromSelf,
  startedAt: Schema.DateTimeUtcFromSelf,
}).pipe(
  Schema.Data,
  Schema.annotations({
    identifier: "Active",
    title: "Active Task",
    description: "A task that is currently being worked on",
  })
)

export const Completed = Schema.TaggedStruct("completed", {
  id: Schema.String,
  createdAt: Schema.DateTimeUtcFromSelf,
  completedAt: Schema.DateTimeUtcFromSelf,
}).pipe(
  Schema.Data,
  Schema.annotations({
    identifier: "Completed",
    title: "Completed Task",
    description: "A task that has been finished",
  })
)

// Union type
export const Task = Schema.Union(Pending, Active, Completed).pipe(
  Schema.annotations({
    identifier: "Task",
    title: "Task",
    description: "A task can be pending, active, or completed",
  })
)

export type Task = Schema.Schema.Type<typeof Task>

// Export member types for refinements
export type Pending = Schema.Schema.Type<typeof Pending>
export type Active = Schema.Schema.Type<typeof Active>
export type Completed = Schema.Schema.Type<typeof Completed>
```

## Why This Pattern?

**Schema.TaggedStruct Benefits:**
- Automatically adds `_tag` discriminator (no manual `Schema.Literal`)
- The `_tag` is applied automatically in constructors
- Cleaner than `Schema.Struct` with manual tag fields
- Enables exhaustive pattern matching

**Schema.Data Benefits:**
- Implements `Equal.Symbol` automatically
- Enables `Equal.equals(a, b)` for structural equality
- No manual equality implementation needed
- Works correctly with nested structures

**Schema.annotations Benefits:**
- Self-documenting schemas with identifier, title, description
- Better error messages in validation failures
- Enables schema introspection

## Mandatory Module Exports

Every domain model module MUST include:

### 1. Type Definition with Schemas

```typescript
import { Schema } from "effect"

// Export both schema and type for each variant
export const Admin = Schema.TaggedStruct("Admin", {
  id: Schema.String,
  name: Schema.String,
  permissions: Schema.Array(Schema.String),
}).pipe(Schema.Data)

export type Admin = Schema.Schema.Type<typeof Admin>

export const Customer = Schema.TaggedStruct("Customer", {
  id: Schema.String,
  name: Schema.String,
  tier: Schema.Union(
    Schema.Literal("free"),
    Schema.Literal("premium")
  ),
}).pipe(Schema.Data)

export type Customer = Schema.Schema.Type<typeof Customer>

// Union schema
export const User = Schema.Union(Admin, Customer).pipe(
  Schema.annotations({
    identifier: "User",
    title: "User",
    description: "A user can be an admin or a customer",
  })
)

export type User = Schema.Schema.Type<typeof User>
```

### 2. Constructors Using Schema.decodeSync

```typescript
import { Schema } from "effect"
import * as DateTime from "effect/DateTime"

// Assume we have these schemas from previous section
declare const Pending: Schema.Schema<any, any, never>
declare const Active: Schema.Schema<any, any, never>
declare const Completed: Schema.Schema<any, any, never>

/**
 * Create a pending task.
 *
 * Note: _tag is automatically applied by TaggedStruct.
 *
 * @category Constructors
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as DateTime from "effect/DateTime"
 *
 * const task = Task.makePending({
 *   id: "task-123",
 *   createdAt: DateTime.unsafeNow()
 * })
 * // Result: { _tag: "pending", id: "task-123", createdAt: ... }
 *
 * // Structural equality from Schema.Data:
 * const another = Task.makePending({
 *   id: "task-123",
 *   createdAt: DateTime.unsafeNow()
 * })
 * Equal.equals(task, another) // true if all fields match
 */
export const makePending = Schema.decodeSync(Pending)

/**
 * Create an active task.
 *
 * @category Constructors
 * @since 0.1.0
 */
export const makeActive = Schema.decodeSync(Active)

/**
 * Create a completed task.
 *
 * @category Constructors
 * @since 0.1.0
 */
export const makeCompleted = Schema.decodeSync(Completed)
```

**Why decodeSync?**
- `Schema.Data` returns a schema that needs decoding
- `decodeSync` creates a validated constructor
- Automatically applies the `_tag` discriminator
- Throws on invalid input (use `decodeUnknownSync` for unknown data)

### 3. Guards and Type Predicates

```typescript
import { Schema } from "effect"

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: any }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: any; readonly startedAt: any }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: any; readonly completedAt: any }

declare type Pending = Extract<Task, { readonly _tag: "pending" }>
declare type Active = Extract<Task, { readonly _tag: "active" }>
declare type Completed = Extract<Task, { readonly _tag: "completed" }>

declare const Task: Schema.Schema<Task, any, never>

/**
 * Type guard for Task union.
 *
 * @category Guards
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 *
 * if (Task.isTask(value)) {
 *   // value is Task
 * }
 */
export const isTask = Schema.is(Task)

/**
 * Refine to Pending variant.
 *
 * @category Guards
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 *
 * if (Task.isPending(task)) {
 *   // task is Pending, access startedAt safely
 *   console.log(task.createdAt)
 * }
 */
export const isPending = (self: Task): self is Pending => self._tag === "pending"

/**
 * Refine to Active variant.
 *
 * @category Guards
 * @since 0.1.0
 */
export const isActive = (self: Task): self is Active => self._tag === "active"

/**
 * Refine to Completed variant.
 *
 * @category Guards
 * @since 0.1.0
 */
export const isCompleted = (self: Task): self is Completed => self._tag === "completed"
```

### 4. Match Function (Pattern Matching)

```typescript
import * as Match from "effect/Match"

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: any }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: any; readonly startedAt: any }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: any; readonly completedAt: any }

/**
 * Pattern match on Task using Match.typeTags.
 *
 * @category Pattern Matching
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 *
 * const status = Task.match({
 *   pending: (t) => `Pending: ${t.id}`,
 *   active: (t) => `Active since ${t.startedAt}`,
 *   completed: (t) => `Completed at ${t.completedAt}`
 * })
 *
 * const result = status(task)
 */
export const match = Match.typeTags<Task>()
```

**Match.typeTags Usage:**
- Primary pattern for discriminated unions
- Type-safe and exhaustive
- Works with any `_tag` discriminator

### 5. Equivalence (Usually Automatic via Schema.Data)

```typescript
import { Schema } from "effect"
import * as Equal from "effect/Equal"
import * as Equivalence from "effect/Equivalence"

// Assume Task type and schema from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: any }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: any; readonly startedAt: any }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: any; readonly completedAt: any }

declare const Task: Schema.Schema<Task, any, never>

/**
 * Primary approach: Use Equal.equals() from Schema.Data
 *
 * @example
 * import * as Equal from "effect/Equal"
 *
 * const task1 = Task.makePending({ ... })
 * const task2 = Task.makePending({ ... })
 *
 * // Structural equality (automatic from Schema.Data)
 * if (Equal.equals(task1, task2)) {
 *   // Tasks are structurally equal
 * }
 */

/**
 * Field-based equivalence using Equivalence.mapInput
 *
 * Compare by specific fields when structural equality isn't appropriate.
 *
 * @category Equivalence
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 *
 * // Compare by ID only
 * const areTasksSame = Task.EquivalenceById(task1, task2)
 */
export const EquivalenceById = Equivalence.mapInput(
  Equivalence.string,
  (task: Task) => task.id
)
```

**When to Export Custom Equivalence:**
- You need multiple comparison strategies (by ID, by group, etc.)
- Field-based equality is semantically meaningful
- Business logic requires custom equality checks

**When NOT to Export Custom Equivalence:**
- You only need structural equality (use `Equal.equals()` directly)
- No custom comparison logic is needed

## Conditional Module Exports

Include these when semantically appropriate:

### Identity Values

When the type has a natural "zero" or "empty" value:

```typescript
// Assume Cents and List types exist
declare type Cents = bigint
declare function make(value: bigint): Cents
declare type List<T> = ReadonlyArray<T>
declare function makeEmpty<T>(): List<T>

/**
 * Zero value for monetary amounts.
 *
 * @category Identity
 * @since 0.1.0
 */
export const zero: Cents = make(0n)

/**
 * Empty list.
 *
 * @category Identity
 * @since 0.1.0
 */
export const empty: List<never> = makeEmpty()
```

### Combinators

Functions that combine or transform values:

```typescript
import { dual } from "effect/Function"

// Assume Cents type exists
declare type Cents = bigint
declare function make(value: bigint): Cents

/**
 * Add two monetary values.
 *
 * @category Combinators
 * @since 0.1.0
 * @example
 * import * as Cents from "@/schemas/Cents"
 * import { pipe } from "effect/Function"
 *
 * const total = pipe(price, Cents.add(tax))
 */
export const add: {
  (that: Cents): (self: Cents) => Cents
  (self: Cents, that: Cents): Cents
} = dual(2, (self: Cents, that: Cents): Cents => make(self + that))

/**
 * Get minimum of two values.
 *
 * @category Combinators
 * @since 0.1.0
 */
export const min = (a: Cents, b: Cents): Cents => a < b ? a : b

/**
 * Get maximum of two values.
 *
 * @category Combinators
 * @since 0.1.0
 */
export const max = (a: Cents, b: Cents): Cents => a > b ? a : b
```

### Order Instances

Provide sorting capabilities using `Order.mapInput`:

```typescript
import * as Order from "effect/Order"
import * as DateTime from "effect/DateTime"

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: DateTime.DateTime.Utc }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: DateTime.DateTime.Utc; readonly startedAt: DateTime.DateTime.Utc }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: DateTime.DateTime.Utc; readonly completedAt: DateTime.DateTime.Utc }

/**
 * Order by tag (pending < active < completed).
 *
 * Uses Order.mapInput to compose from Order.number.
 *
 * @category Orders
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as Array from "effect/Array"
 * import { pipe } from "effect/Function"
 *
 * const sorted = pipe(tasks, Array.sort(Task.OrderByTag))
 */
export const OrderByTag: Order.Order<Task> = Order.mapInput(
  Order.number,
  (task) => {
    const priorities = { pending: 0, active: 1, completed: 2 }
    return priorities[task._tag]
  }
)

/**
 * Order by ID.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderById: Order.Order<Task> =
  Order.mapInput(Order.string, (task) => task.id)

/**
 * Order by creation date.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByCreatedAt: Order.Order<Task> =
  Order.mapInput(DateTime.Order, (task) => task.createdAt)

/**
 * Combine multiple orders for multi-criteria sorting.
 *
 * Sorts by tag first, then by creation date.
 *
 * @category Orders
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as Array from "effect/Array"
 *
 * const sorted = Array.sort(tasks, Task.OrderByTagThenDate)
 */
export const OrderByTagThenDate: Order.Order<Task> = Order.combine(
  OrderByTag,
  OrderByCreatedAt
)
```

**Key Pattern: Order.mapInput**
- Compose orders from simpler base orders
- Map domain type to comparable value
- Signature: `Order.mapInput(baseOrder, (value) => extractField)`

**Key Pattern: Order.combine**
- Combine multiple orders for multi-criteria sorting
- First order takes precedence, then second, etc.

### Destructors (Getters)

Safe extraction of inner values:

```typescript
import * as DateTime from "effect/DateTime"

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: DateTime.DateTime.Utc }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: DateTime.DateTime.Utc; readonly startedAt: DateTime.DateTime.Utc }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: DateTime.DateTime.Utc; readonly completedAt: DateTime.DateTime.Utc }

/**
 * Get the ID from any Task variant.
 *
 * @category Destructors
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 *
 * const id = Task.getId(task) // Works for any variant
 */
export const getId = (self: Task): string => self.id

/**
 * Get creation date.
 *
 * @category Destructors
 * @since 0.1.0
 */
export const getCreatedAt = (self: Task): DateTime.DateTime.Utc =>
  self.createdAt
```

### Setters (Immutable Updates)

```typescript
import { dual } from "effect/Function"

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: any }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: any; readonly startedAt: any }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: any; readonly completedAt: any }

/**
 * Update a field immutably.
 *
 * @category Setters
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import { pipe } from "effect/Function"
 *
 * const updated = pipe(task, Task.setId("new-id"))
 */
export const setId: {
  (id: string): (self: Task) => Task
  (self: Task, id: string): Task
} = dual(2, (self: Task, id: string): Task => ({ ...self, id }))
```

## Advanced Patterns

### Recursive Schemas with Schema.suspend

Use for self-referencing types (trees, graphs, nested structures):

```typescript
import { Schema } from "effect"

/**
 * Recursive domain type: Category with subcategories.
 */

// Separate base fields from recursive field
const baseFields = {
  id: Schema.String,
  name: Schema.String,
}

// Define the recursive type
interface Category extends Schema.Struct.Type<typeof baseFields> {
  readonly subcategories: ReadonlyArray<Category>
}

// Create schema with Schema.suspend for recursion
export const Category = Schema.Struct({
  ...baseFields,
  subcategories: Schema.Array(
    Schema.suspend((): Schema.Schema<Category> => Category)
  ),
}).pipe(
  Schema.Data,
  Schema.annotations({
    identifier: "Category",
    title: "Category",
    description: "A category that can contain nested subcategories",
  })
)

export type Category = Schema.Schema.Type<typeof Category>
export const make = Schema.decodeSync(Category)

/**
 * Example usage:
 *
 * const root = Category.make({
 *   id: "1",
 *   name: "Electronics",
 *   subcategories: [
 *     Category.make({ id: "2", name: "Phones", subcategories: [] }),
 *     Category.make({ id: "3", name: "Laptops", subcategories: [] })
 *   ]
 * })
 */
```

**Key Pattern: Schema.suspend**
- Use for self-referencing types
- Separate base fields for clarity
- Define interface first, then schema with `Schema.suspend`

### Branded Types

For types that need additional runtime guarantees:

```typescript
import * as Brand from "effect/Brand"
import { Schema } from "effect"

/**
 * Email branded type with validation.
 */
export type Email = Brand.Branded<string, "Email">

export const Email = Brand.refined<Email>(
  (s) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(s),
  (s) => Brand.error(`"${s}" is not a valid email`)
)

/**
 * Schema for Email serialization/deserialization.
 */
export const EmailSchema: Schema.BrandSchema<Email, string> =
  Schema.String.pipe(Schema.fromBrand(Email))

/**
 * @example
 * const email = Email("user@example.com")
 * const decoded = Schema.decodeSync(EmailSchema)("user@example.com")
 */
```

### Typeclass Instances

**Only implement typeclasses that are semantically appropriate.**

Check the project's `@/typeclass/` directory for available typeclasses:

```typescript
// Assume Schedulable typeclass exists
declare namespace Schedulable$ {
  function make<A>(
    get: (self: A) => any,
    set: (self: A, date: any) => A
  ): any
  function isScheduledBefore(instance: any): (a: any, b: any) => boolean
  function OrderByScheduledDate(instance: any): any
}

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: any }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: any; readonly startedAt: any }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: any; readonly completedAt: any }

/**
 * Schedulable instance for Task.
 *
 * @category Typeclasses
 * @since 0.1.0
 */
export const Schedulable = Schedulable$.make<Task>(
  (self) => self.createdAt,
  (self, date) => ({ ...self, createdAt: date })
)

// Re-export derived predicates
export const isScheduledBefore = Schedulable$.isScheduledBefore(Schedulable)

// Re-export derived orders
export const OrderByScheduledDate = Schedulable$.OrderByScheduledDate(Schedulable)
```

**Common typeclass examples:**
- **Schedulable**: For types with date/time properties
- **Durable**: For types with duration properties
- **Priceable**: For types with price properties
- **Identifiable**: For types with ID properties

## Import Patterns

**CRITICAL**: Always use namespace imports:

```typescript
// CORRECT
import * as Task from "@/schemas/Task"
import * as DateTime from "effect/DateTime"
import * as Array from "effect/Array"
import * as Order from "effect/Order"
import * as Equal from "effect/Equal"

declare const tasks: ReadonlyArray<Task.Task>
declare const task1: Task.Task
declare const task2: Task.Task

const task = Task.makePending({
  id: "123",
  createdAt: DateTime.unsafeNow()
})
const isPending = Task.isPending(task)
const sorted = Array.sort(tasks, Task.OrderByTag)
const areEqual = Equal.equals(task1, task2)
```

**NEVER** do this:

```typescript
// WRONG - loses context, causes name clashes
import { makePending, isPending } from "@/schemas/Task"
```

**Namespace Import Benefits:**
- Clear context for all functions
- Prevents name clashes
- Enables `Task.Pending`, `Task.Active` schema access
- Natural organization: `Task.makePending`, `Task.isPending`

## Temporal Data

Always use DateTime and Duration, never Date or number:

```typescript
// CORRECT
import { Schema } from "effect"
import * as DateTime from "effect/DateTime"
import * as Duration from "effect/Duration"

export const Task = Schema.TaggedStruct("task", {
  createdAt: Schema.DateTimeUtcFromSelf,  // UTC datetime
  duration: Schema.Duration,               // Duration type
}).pipe(Schema.Data)

// WRONG
export const TaskBad = Schema.TaggedStruct("task", {
  createdAt: Schema.Date,        // Native Date
  duration: Schema.Number,       // Number milliseconds
})
```

## Immutability

Use the Data module for immutable operations:

```typescript
import { Data } from "effect"

// Assume Task type from previous section
declare type Task =
  | { readonly _tag: "pending"; readonly id: string; readonly createdAt: any }
  | { readonly _tag: "active"; readonly id: string; readonly createdAt: any; readonly startedAt: any }
  | { readonly _tag: "completed"; readonly id: string; readonly createdAt: any; readonly completedAt: any }

/**
 * Immutable update.
 *
 * @category Setters
 * @since 0.1.0
 */
export const updateStatus = (self: Task, newTag: Task["_tag"]): Task =>
  Data.struct({ ...self, _tag: newTag })
```

## Documentation Standards

Every exported member MUST have:

- JSDoc with description
- `@category` tag (Constructors, Guards, Pattern Matching, Orders, etc.)
- `@since` tag (version number)
- `@example` with fully working code including all imports

```typescript
import { Schema } from "effect"
import * as DateTime from "effect/DateTime"

declare const Pending: Schema.Schema<any, any, never>

/**
 * Create a pending task.
 *
 * Note: _tag is automatically applied by TaggedStruct.
 *
 * @category Constructors
 * @since 0.1.0
 * @example
 * import * as Task from "@/schemas/Task"
 * import * as DateTime from "effect/DateTime"
 *
 * const task = Task.makePending({
 *   id: "task-123",
 *   createdAt: DateTime.unsafeNow()
 * })
 */
export const makePending = Schema.decodeSync(Pending)
```

## Quality Checklist

### Mandatory - Every Domain Model

- [ ] Type definition using `Schema.TaggedStruct` for each variant
- [ ] `.pipe(Schema.Data)` for automatic `Equal` implementation
- [ ] Schema annotations (identifier, title, description) on all schemas
- [ ] Constructor functions using `Schema.decodeSync`
- [ ] Type guard using `Schema.is` for union
- [ ] Refinement predicates for each variant (e.g., `isPending`)
- [ ] Match function using `Match.typeTags`
- [ ] Export all union member schemas and types
- [ ] All exports use namespace pattern (`import * as`)
- [ ] Full JSDoc with @category, @since, @example
- [ ] DateTime/Duration for temporal data (not Date/number)
- [ ] Data module for immutability
- [ ] Examples compile and run
- [ ] Format and typecheck pass

### Conditional - Include When Appropriate

- [ ] Identity values (`zero`, `empty`, `unit`)
- [ ] Combinators (`add`, `min`, `max`, `combine`)
- [ ] Order instances using `Order.mapInput` for common sorting needs
- [ ] `Order.combine` for multi-criteria sorting
- [ ] Custom Equivalence via `Schema.equivalence()` or `Equivalence.mapInput`
- [ ] Destructors (getters for common fields)
- [ ] Setters (immutable update helpers)
- [ ] Recursive schemas with `Schema.suspend` (for self-referencing types)
- [ ] Branded types for validation constraints
- [ ] Typeclass instances (check `@/typeclass/` directory first)
- [ ] Derived predicates from typeclasses
- [ ] Derived orders from typeclasses

## Complete Example

```typescript
/**
 * User domain model demonstrating all patterns.
 *
 * @since 0.1.0
 */
import { Schema, Equal, Match, Data } from "effect"
import * as DateTime from "effect/DateTime"
import * as Order from "effect/Order"
import * as Equivalence from "effect/Equivalence"
import { dual } from "effect/Function"

// =============================================================================
// Models
// =============================================================================

export const Admin = Schema.TaggedStruct("Admin", {
  id: Schema.String,
  name: Schema.String,
  createdAt: Schema.DateTimeUtcFromSelf,
  permissions: Schema.Array(Schema.String),
}).pipe(
  Schema.Data,
  Schema.annotations({
    identifier: "Admin",
    title: "Administrator",
    description: "A user with administrative privileges",
  })
)

export type Admin = Schema.Schema.Type<typeof Admin>

export const Customer = Schema.TaggedStruct("Customer", {
  id: Schema.String,
  name: Schema.String,
  createdAt: Schema.DateTimeUtcFromSelf,
  tier: Schema.Union(Schema.Literal("free"), Schema.Literal("premium")),
}).pipe(
  Schema.Data,
  Schema.annotations({
    identifier: "Customer",
    title: "Customer",
    description: "A customer user",
  })
)

export type Customer = Schema.Schema.Type<typeof Customer>

export const User = Schema.Union(Admin, Customer).pipe(
  Schema.annotations({
    identifier: "User",
    title: "User",
    description: "A user can be an admin or a customer",
  })
)

export type User = Schema.Schema.Type<typeof User>

// =============================================================================
// Constructors
// =============================================================================

/**
 * Create an admin user.
 *
 * @category Constructors
 * @since 0.1.0
 * @example
 * import * as User from "@/schemas/User"
 * import * as DateTime from "effect/DateTime"
 *
 * const admin = User.makeAdmin({
 *   id: "admin-1",
 *   name: "Alice",
 *   createdAt: DateTime.unsafeNow(),
 *   permissions: ["read", "write"]
 * })
 */
export const makeAdmin = Schema.decodeSync(Admin)

/**
 * Create a customer user.
 *
 * @category Constructors
 * @since 0.1.0
 */
export const makeCustomer = Schema.decodeSync(Customer)

// =============================================================================
// Guards
// =============================================================================

/**
 * Type guard for User.
 *
 * @category Guards
 * @since 0.1.0
 */
export const isUser = Schema.is(User)

/**
 * Refine to Admin.
 *
 * @category Guards
 * @since 0.1.0
 */
export const isAdmin = (self: User): self is Admin => self._tag === "Admin"

/**
 * Refine to Customer.
 *
 * @category Guards
 * @since 0.1.0
 */
export const isCustomer = (self: User): self is Customer => self._tag === "Customer"

// =============================================================================
// Pattern Matching
// =============================================================================

/**
 * Pattern match on User.
 *
 * @category Pattern Matching
 * @since 0.1.0
 * @example
 * import * as User from "@/schemas/User"
 *
 * const greeting = User.match({
 *   Admin: (u) => `Hello Admin ${u.name}`,
 *   Customer: (u) => `Hello ${u.tier} customer ${u.name}`
 * })
 *
 * const message = greeting(user)
 */
export const match = Match.typeTags<User>()

// =============================================================================
// Equivalence
// =============================================================================

/**
 * Compare users by ID only.
 *
 * @category Equivalence
 * @since 0.1.0
 */
export const EquivalenceById = Equivalence.mapInput(
  Equivalence.string,
  (user: User) => user.id
)

// =============================================================================
// Orders
// =============================================================================

/**
 * Order by name.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByName: Order.Order<User> =
  Order.mapInput(Order.string, (user) => user.name)

/**
 * Order by creation date.
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByCreatedAt: Order.Order<User> =
  Order.mapInput(DateTime.Order, (user) => user.createdAt)

/**
 * Order by tag (Admin < Customer).
 *
 * @category Orders
 * @since 0.1.0
 */
export const OrderByTag: Order.Order<User> = Order.mapInput(
  Order.number,
  (user) => (user._tag === "Admin" ? 0 : 1)
)

// =============================================================================
// Destructors
// =============================================================================

/**
 * Get user ID.
 *
 * @category Destructors
 * @since 0.1.0
 */
export const getId = (self: User): string => self.id

/**
 * Get user name.
 *
 * @category Destructors
 * @since 0.1.0
 */
export const getName = (self: User): string => self.name

/**
 * Get creation date.
 *
 * @category Destructors
 * @since 0.1.0
 */
export const getCreatedAt = (self: User): DateTime.DateTime.Utc => self.createdAt

// =============================================================================
// Setters
// =============================================================================

/**
 * Update user name immutably.
 *
 * @category Setters
 * @since 0.1.0
 */
export const setName: {
  (name: string): (self: User) => User
  (self: User, name: string): User
} = dual(2, (self: User, name: string): User => ({ ...self, name }))
```

## When to Use This Skill

- Creating domain entities (User, Product, Order)
- Modeling value objects (Email, Money, Address)
- Defining discriminated unions (states, events, commands)
- Implementing ADTs (algebraic data types)
- Building type-safe domain models with validation
- Ensuring structural equality with automatic Equal
- Creating self-documenting schemas

## Key Principles Summary

1. **Schema.TaggedStruct** - Use for all tagged union variants
2. **Schema.Data** - Apply for automatic Equal implementation
3. **Schema.decodeSync** - Create type-safe constructors
4. **Schema.annotations** - Document all schemas
5. **Order.mapInput** - Compose orders from base orders
6. **Match.typeTags** - Pattern match on discriminated unions
7. **Schema.suspend** - Handle recursive types
8. **Namespace imports** - Always use `import * as`
9. **DateTime/Duration** - Never use Date/number for temporal data
10. **Equal.equals()** - Primary equality check (from Schema.Data)

Your domain models should be production-ready, type-safe, and provide excellent developer experience.
