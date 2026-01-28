---
name: pattern-matching
description: Master Effect pattern matching using Data.TaggedEnum, $match, $is, Match.typeTags, and Effect.match. Avoid manual _tag checks and Effect.either patterns. Use this skill when working with discriminated unions, ADTs, or conditional logic based on tagged types.
---

# Effect Pattern Matching Skill

Use this skill when working with discriminated unions, ADTs, conditional logic, or any type that uses `_tag` discrimination. Pattern matching provides exhaustive, type-safe alternatives to imperative conditionals.

## Core Philosophy

**Pattern matching over imperative conditionals**:
- Exhaustive by default (compiler enforces all cases)
- Type-safe refinement in each branch
- Declarative, not imperative
- Pipeline-friendly composition

## Pattern 1: Data.TaggedEnum for ADTs

Use `Data.TaggedEnum` instead of manual tagged unions.

### The Problem: Manual Tagged Unions

```typescript
// ❌ WRONG - Manual tagged union
type WalletState =
  | { readonly _tag: "Disconnected" }
  | { readonly _tag: "Connecting" }
  | { readonly _tag: "Connected"; readonly address: string }
  | { readonly _tag: "Error"; readonly message: string }

// Manual constructors - verbose and error-prone
const disconnected = (): WalletState => ({ _tag: "Disconnected" })
const connecting = (): WalletState => ({ _tag: "Connecting" })
const connected = (address: string): WalletState =>
  ({ _tag: "Connected", address })
const error = (message: string): WalletState =>
  ({ _tag: "Error", message })

// No built-in pattern matching
// No type guards
// No exhaustiveness checking
```

### The Solution: Data.TaggedEnum

```typescript
// ✅ CORRECT - TaggedEnum with constructors + $match + $is
import { Data } from "effect"

type WalletState = Data.TaggedEnum<{
  Disconnected: {}
  Connecting: {}
  Connected: { readonly address: string }
  Error: { readonly message: string }
}>

const WalletState = Data.taggedEnum<WalletState>()

/**
 * WalletState now provides:
 * - WalletState.Disconnected() - Constructor
 * - WalletState.Connecting() - Constructor
 * - WalletState.Connected({ address }) - Constructor
 * - WalletState.Error({ message }) - Constructor
 * - WalletState.$match(state, { ... }) - Pattern matching
 * - WalletState.$is("Connected")(state) - Type guard
 */

// Usage
const state = WalletState.Connected({ address: "0x123" })

// Pattern match
const display = WalletState.$match(state, {
  Disconnected: () => "Please connect wallet",
  Connecting: () => "Connecting...",
  Connected: ({ address }) => `Connected: ${address}`,
  Error: ({ message }) => `Error: ${message}`
})

// Type guard
if (WalletState.$is("Connected")(state)) {
  console.log(state.address) // Type-safe access
}
```

### Benefits of Data.TaggedEnum

1. **Automatic constructors** - No manual factory functions
2. **Automatic $match** - Exhaustive pattern matching built-in
3. **Automatic $is** - Type-safe guards for each variant
4. **Type inference** - Compiler knows all variants
5. **Compile-time exhaustiveness** - Forget a case? Compiler error

### When to Use Data.TaggedEnum

- **State machines**: Connection states, loading states, workflow states
- **Domain events**: UserLoggedIn, UserLoggedOut, SessionExpired
- **Command types**: CreateUser, UpdateUser, DeleteUser
- **Result types**: Success, Failure, Pending
- **Any discriminated union** with multiple variants

## Pattern 2: Avoid Effect.either + _tag Checks

Use `Effect.match` instead of `Effect.either` with manual tag checks.

### The Problem: Effect.either with Manual Checks

```typescript
// ❌ WRONG - Effect.either with manual _tag checks
import { Effect, Either, Data } from "effect"

declare const User: { name: string; id: string }
type User = typeof User

class NotFound extends Data.TaggedError("NotFound")<{
  readonly id: string
}> {}

const getUser = (id: string): Effect.Effect<User, NotFound> => Effect.fail(new NotFound({ id }))

const program = Effect.gen(function* () {
  const result = yield* Effect.either(getUser("123"))

  // Manual tag checking - not exhaustive
  if (result._tag === "Left") {
    console.error(`User not found: ${result.left.id}`)
    return null
  }

  return result.right
})
```

**Problems:**
- Not exhaustive (could forget Right case)
- Verbose and imperative
- Breaks pipeline style
- Manual unwrapping of Either

### The Solution: Effect.match

```typescript
// ✅ CORRECT - Effect.match for declarative error handling
import { Effect, Data } from "effect"

declare const User: { name: string; id: string }
type User = typeof User

class NotFound extends Data.TaggedError("NotFound")<{
  readonly id: string
}> {}

const getUser = (id: string): Effect.Effect<User, NotFound> => Effect.fail(new NotFound({ id }))

const program = getUser("123").pipe(
  Effect.match({
    onFailure: (error) => {
      console.error(`User not found: ${error.id}`)
      return null
    },
    onSuccess: (user) => user
  })
)
```

**Benefits:**
- Exhaustive (must handle both cases)
- Declarative and pipeline-friendly
- No manual Either unwrapping
- Type-safe refinement in each branch

### Effect.match Variants

```typescript
import { Effect, Cause } from "effect"

declare const effect: Effect.Effect<unknown, unknown, unknown>
declare function handleError(error: unknown): unknown
declare function handleSuccess(value: unknown): unknown
declare function handleCause(cause: Cause.Cause<unknown>): unknown

// Basic match - transform both success and failure
Effect.match(effect, {
  onFailure: (error) => handleError(error),
  onSuccess: (value) => handleSuccess(value)
})

// matchEffect - return Effects from handlers
Effect.matchEffect(effect, {
  onFailure: (error) => Effect.logError(error).pipe(Effect.as(null)),
  onSuccess: (value) => Effect.succeed(value)
})

// matchCause - match on full Cause (errors + defects + interrupts)
Effect.matchCause(effect, {
  onFailure: (cause) => handleCause(cause),
  onSuccess: (value) => value
})

// matchCauseEffect - Cause matching with Effect handlers
Effect.matchCauseEffect(effect, {
  onFailure: (cause) => Effect.logError(cause).pipe(Effect.as(null)),
  onSuccess: (value) => Effect.succeed(value)
})
```

## Pattern 3: Use $match for Exhaustive Pattern Matching

Use `TaggedEnum.$match` for exhaustive, type-safe pattern matching.

### The Problem: if/else Chains

```typescript
// ❌ WRONG - if/else chains, not exhaustive
import { Data } from "effect"

type Status = Data.TaggedEnum<{
  Active: {}
  Expired: {}
  Revoked: {}
}>
const Status = Data.taggedEnum<Status>()

const getColor = (status: Status): string => {
  if (status._tag === "Active") {
    return "green"
  } else if (status._tag === "Expired") {
    return "yellow"
  }
  // Forgot "Revoked" - no compiler error!
  return "gray"
}
```

**Problems:**
- Not exhaustive (easy to forget cases)
- Compiler doesn't enforce completeness
- Imperative style
- Hard to refactor when adding variants

### The Solution: $match

```typescript
// ✅ CORRECT - $match with exhaustive checking
import { Data } from "effect"

type Status = Data.TaggedEnum<{
  Active: {}
  Expired: {}
  Revoked: {}
}>
const Status = Data.taggedEnum<Status>()

const getColor = (status: Status): string =>
  Status.$match(status, {
    Active: () => "green",
    Expired: () => "yellow",
    Revoked: () => "red"
    // Compiler error if any case is missing!
  })
```

**Benefits:**
- **Exhaustive** - Compiler enforces all cases
- **Type-safe** - Each handler gets refined type
- **Declarative** - Clear mapping from variant to result
- **Refactor-safe** - Add variant? Compiler finds all matches to update

### $match with Data Access

```typescript
type AsyncState = Data.TaggedEnum<{
  Idle: {}
  Loading: {}
  Success: { readonly data: string }
  Failure: { readonly error: string }
}>
const AsyncState = Data.taggedEnum<AsyncState>()

const display = (state: AsyncState): string =>
  AsyncState.$match(state, {
    Idle: () => "Not started",
    Loading: () => "Loading...",
    Success: ({ data }) => `Loaded: ${data}`,
    Failure: ({ error }) => `Error: ${error}`
  })
```

### Nested Pattern Matching

```typescript
type Request = Data.TaggedEnum<{
  Pending: {}
  Approved: { readonly by: string }
  Rejected: { readonly reason: string }
}>
const Request = Data.taggedEnum<Request>()

type Workflow = Data.TaggedEnum<{
  Draft: { readonly request: Request }
  Submitted: { readonly request: Request }
  Completed: {}
}>
const Workflow = Data.taggedEnum<Workflow>()

const getStatus = (workflow: Workflow): string =>
  Workflow.$match(workflow, {
    Draft: ({ request }) =>
      Request.$match(request, {
        Pending: () => "Draft - Pending",
        Approved: ({ by }) => `Draft - Approved by ${by}`,
        Rejected: ({ reason }) => `Draft - Rejected: ${reason}`
      }),
    Submitted: ({ request }) =>
      Request.$match(request, {
        Pending: () => "Submitted - Awaiting approval",
        Approved: ({ by }) => `Submitted - Approved by ${by}`,
        Rejected: ({ reason }) => `Submitted - Rejected: ${reason}`
      }),
    Completed: () => "Completed"
  })
```

## Pattern 4: Use $is for Single-Case Type Guards

Use `TaggedEnum.$is` instead of manual `_tag` checks.

### The Problem: Manual _tag Checks

```typescript
// ❌ WRONG - Manual tag checking
import { Data } from "effect"

type Status = Data.TaggedEnum<{
  Active: {}
  Expired: {}
}>
const Status = Data.taggedEnum<Status>()

// Verbose and repetitive
const status = Status.Active()
if (status._tag === "Active") {
  console.log("Active!")
}

// Hard to use in Array methods
const items: Status[] = [Status.Active(), Status.Expired()]
const activeItems = items.filter(item => item._tag === "Active")
```

### The Solution: $is Type Guards

```typescript
// ✅ CORRECT - $is for type-safe guards
import { Data, Array, pipe } from "effect"

type Status = Data.TaggedEnum<{
  Active: {}
  Expired: {}
}>
const Status = Data.taggedEnum<Status>()

const status = Status.Active()

// Clean, declarative guard
if (Status.$is("Active")(status)) {
  console.log("Active!")
}

// Perfect for Array methods
const items: Status[] = [Status.Active(), Status.Expired()]
const activeItems = items.filter(Status.$is("Active"))

// Pipeline-friendly
const hasActive = pipe(
  items,
  Array.some(Status.$is("Active"))
)

// Multiple guards
const activeOrExpired = items.filter(
  item => Status.$is("Active")(item) || Status.$is("Expired")(item)
)
```

### $is in Effect Pipelines

```typescript
import { Data, pipe } from "effect"

type LoadState = Data.TaggedEnum<{
  Loading: {}
  Ready: { readonly data: string[] }
  Error: { readonly message: string }
}>
const LoadState = Data.taggedEnum<LoadState>()

const getData = (state: LoadState): string[] =>
  pipe(
    state,
    // Type guard refines to Ready
    LoadState.$is("Ready"),
    // Now can access .data safely
    ready => ready ? ready.data : []
  )
```

## Pattern 5: Use Option.match Instead of _tag Checks

Use `Option.match` instead of manual `._tag` checks on Options.

### The Problem: Manual Option Tag Checks

```typescript
// ❌ WRONG - Manual Option._tag checks
import { Option } from "effect"

type User = { name: string; id: string }

const maybeUser: Option.Option<User> = Option.some({ name: "Alice", id: "123" })

// Imperative and verbose
if (maybeUser._tag === "Some") {
  console.log(maybeUser.value.name)
} else {
  console.log("No user")
}
```

### The Solution: Option.match

```typescript
// ✅ CORRECT - Option.match
import { Option, pipe } from "effect"

type User = { name: string; id: string }

const maybeUser: Option.Option<User> = Option.some({ name: "Alice", id: "123" })

const display = Option.match(maybeUser, {
  onNone: () => "No user",
  onSome: (user) => user.name
})

// In pipelines
const name = pipe(
  maybeUser,
  Option.match({
    onNone: () => "Guest",
    onSome: (user) => user.name
  })
)
```

### Option Pattern Matching Variants

```typescript
import { Option, pipe } from "effect"

declare const option: Option.Option<string>
declare const defaultValue: string
declare function transform(value: string): string
declare function predicate(value: string): boolean

// Basic match
Option.match(option, {
  onNone: () => defaultValue,
  onSome: (value) => transform(value)
})

// getOrElse - simpler for just default value
Option.getOrElse(option, () => defaultValue)

// map + getOrElse pattern
pipe(
  option,
  Option.map(transform),
  Option.getOrElse(() => defaultValue)
)

// filter + match
pipe(
  option,
  Option.filter(predicate),
  Option.match({
    onNone: () => "Filtered out or was None",
    onSome: (value) => `Matched: ${value}`
  })
)
```

## Pattern 6: Use Match.typeTags for Schema Unions

For Schema-based unions, use `Match.typeTags` for pattern matching.

### Schema Union Pattern Matching

```typescript
import { Schema, Match } from "effect"

// Schema-based tagged structs
const Admin = Schema.TaggedStruct("Admin", {
  id: Schema.String,
  permissions: Schema.Array(Schema.String)
}).pipe(Schema.Data)

const Customer = Schema.TaggedStruct("Customer", {
  id: Schema.String,
  tier: Schema.Literal("free", "premium")
}).pipe(Schema.Data)

const User = Schema.Union(Admin, Customer)
type User = Schema.Schema.Type<typeof User>

// Match.typeTags for Schema unions
const getPermissions = Match.typeTags<User>()({
  Admin: ({ permissions }) => permissions,
  Customer: ({ tier }) => tier === "premium" ? ["read"] : []
})

const user: User = {
  _tag: "Admin" as const,
  id: "1",
  permissions: ["read", "write"]
}

const perms = getPermissions(user) // ["read", "write"]
```

### Match.typeTags Pattern

```typescript
import { Match, Data } from "effect"

type UnionType = Data.TaggedEnum<{
  VariantA: { field: string }
  VariantB: { other: number }
}>

declare const value: UnionType
declare function handleA(data: { field: string }): string
declare function handleB(data: { other: number }): string

// Create matcher function
const match = Match.typeTags<UnionType>()

// Use with handlers object
const result = match({
  VariantA: (data) => handleA(data),
  VariantB: (data) => handleB(data)
})(value)

// Or create matcher and apply later
const matcher = match({
  VariantA: (data) => handleA(data),
  VariantB: (data) => handleB(data)
})
const result2 = matcher(value)
```

## Pattern 7: Loadable.match for Async State

Use `Loadable.match` for async state pattern matching.

### Loadable Pattern

```tsx
import { Loadable } from "@/typeclass/Loadable"

type User = { name: string; id: string }

declare const Spinner: () => JSX.Element
declare const UserProfile: (props: { user: User }) => JSX.Element
declare const ErrorDisplay: (props: { error: Error }) => JSX.Element

type UserData = Loadable.Loadable<User>

const display = (data: UserData): JSX.Element =>
  Loadable.match(data, {
    onPending: () => <Spinner />,
    onReady: (user) => <UserProfile user={user} />
  })

// With error state
type UserDataWithError = Loadable.LoadableWithError<User, Error>

const displayWithError = (data: UserDataWithError): JSX.Element =>
  Loadable.matchWithError(data, {
    onPending: () => <Spinner />,
    onReady: (user) => <UserProfile user={user} />,
    onError: (error) => <ErrorDisplay error={error} />
  })
```

## Testability: Effect Services

When pattern matching involves non-deterministic operations, use Effect services.

### The Problem: Untestable Direct Calls

```typescript
// ❌ WRONG - untestable
import { Data } from "effect"

type State = Data.TaggedEnum<{
  Active: {}
  Expired: {}
}>
const State = Data.taggedEnum<State>()

const processState = (state: State): string =>
  State.$match(state, {
    Active: () => `Active at ${Date.now()}`,
    Expired: () => `Expired at ${Date.now()}`
  })
```

### The Solution: Effect Services

```typescript
// ✅ CORRECT - testable with Clock service
import { Clock, Effect, Data, TestClock } from "effect"

type State = Data.TaggedEnum<{
  Active: {}
  Expired: {}
}>
const State = Data.taggedEnum<State>()

const processState = (state: State): Effect.Effect<string> =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis

    return State.$match(state, {
      Active: () => `Active at ${now}`,
      Expired: () => `Expired at ${now}`
    })
  })

// In tests, use TestClock for deterministic time
const testProgram = processState(State.Active()).pipe(
  Effect.provide(TestClock.make())
)
```

### Random Values in Pattern Matching

```typescript
// ❌ WRONG - untestable
import { Data } from "effect"

type User = Data.TaggedEnum<{
  Admin: {}
  Customer: {}
}>
const User = Data.taggedEnum<User>()

const assignColor = (user: User): string =>
  User.$match(user, {
    Admin: () => "red",
    Customer: () => Math.random() > 0.5 ? "blue" : "green"
  })

// ✅ CORRECT - testable with Random service
import { Random, Effect } from "effect"

const assignColorTestable = (user: User): Effect.Effect<string> =>
  User.$match(user, {
    Admin: () => Effect.succeed("red"),
    Customer: () =>
      Effect.gen(function* () {
        const rand = yield* Random.next
        return rand > 0.5 ? "blue" : "green"
      })
  })
```

## Complete Example: Wallet Connection State Machine

```typescript
import { Data, Effect, Clock } from "effect"

// Define state machine with TaggedEnum
type WalletState = Data.TaggedEnum<{
  Disconnected: {}
  Connecting: { readonly startedAt: number }
  Connected: {
    readonly address: string
    readonly connectedAt: number
  }
  Error: {
    readonly message: string
    readonly occurredAt: number
  }
}>

const WalletState = Data.taggedEnum<WalletState>()

// State transitions
const connect = (): Effect.Effect<WalletState> =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis
    return WalletState.Connecting({ startedAt: now })
  })

const completeConnection = (
  address: string
): Effect.Effect<WalletState> =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis
    return WalletState.Connected({
      address,
      connectedAt: now
    })
  })

const fail = (message: string): Effect.Effect<WalletState> =>
  Effect.gen(function* () {
    const now = yield* Clock.currentTimeMillis
    return WalletState.Error({
      message,
      occurredAt: now
    })
  })

// Pattern match for display
const displayState = (state: WalletState): string =>
  WalletState.$match(state, {
    Disconnected: () => "Please connect your wallet",
    Connecting: ({ startedAt }) =>
      `Connecting... (started at ${startedAt})`,
    Connected: ({ address, connectedAt }) =>
      `Connected: ${address} (at ${connectedAt})`,
    Error: ({ message, occurredAt }) =>
      `Error: ${message} (at ${occurredAt})`
  })

// Type-safe state queries using $is
const isConnected = WalletState.$is("Connected")
const canDisconnect = (state: WalletState): boolean =>
  isConnected(state) || WalletState.$is("Error")(state)

// Filter connected states
const getConnectedStates = (
  states: WalletState[]
): Array<Extract<WalletState, { _tag: "Connected" }>> =>
  states.filter(isConnected)
```

## Quality Checklist

Before completing pattern matching implementation:

- [ ] Use `Data.TaggedEnum` for ADTs (not manual tagged unions)
- [ ] Use `TaggedEnum.$match` for exhaustive matching
- [ ] Use `TaggedEnum.$is` for type guards (not `._tag === `)
- [ ] Use `Effect.match` instead of `Effect.either` + if checks
- [ ] Use `Option.match` instead of `Option._tag` checks
- [ ] Use `Match.typeTags` for Schema union matching
- [ ] All pattern matches are exhaustive (compiler-checked)
- [ ] Use `Clock` service instead of `Date.now()` in matches
- [ ] Use `Random` service instead of `Math.random()` in matches
- [ ] Pattern matching is declarative (no imperative conditionals)
- [ ] Pipeline-friendly composition
- [ ] Type-safe refinement in each branch

## Common Patterns Summary

### ADT Definition
```typescript
import { Data } from "effect"

type State = Data.TaggedEnum<{
  VariantA: { field: string }
  VariantB: { other: number }
}>
const State = Data.taggedEnum<State>()
```

### Exhaustive Matching
```typescript
import { Data } from "effect"

type State = Data.TaggedEnum<{
  VariantA: { field: string }
  VariantB: { other: number }
}>
const State = Data.taggedEnum<State>()

declare const state: State
declare function handleA(field: string): void
declare function handleB(other: number): void

State.$match(state, {
  VariantA: ({ field }) => handleA(field),
  VariantB: ({ other }) => handleB(other)
})
```

### Type Guards
```typescript
import { Data } from "effect"

type State = Data.TaggedEnum<{
  VariantA: { field: string }
  VariantB: { other: number }
}>
const State = Data.taggedEnum<State>()

declare const state: State
declare const items: State[]

if (State.$is("VariantA")(state)) {
  // state is refined to VariantA
}

// In filters
items.filter(State.$is("VariantA"))
```

### Effect Matching
```typescript
import { Effect } from "effect"

declare const effect: Effect.Effect<unknown, unknown, unknown>
declare function handleError(error: unknown): unknown
declare function handleSuccess(value: unknown): unknown

effect.pipe(
  Effect.match({
    onFailure: (error) => handleError(error),
    onSuccess: (value) => handleSuccess(value)
  })
)
```

### Option Matching
```typescript
import { Option } from "effect"

declare const option: Option.Option<string>
declare const defaultValue: string
declare function transform(value: string): string

Option.match(option, {
  onNone: () => defaultValue,
  onSome: (value) => transform(value)
})
```

Your pattern matching implementations should be exhaustive, type-safe, declarative, and testable.
