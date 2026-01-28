---
name: typescript-effect
type: simple
depth: extended
description: >-
  Enforces functional TypeScript patterns with Effect ecosystem. Use when
  (1) writing TypeScript functions or modules, (2) defining types or schemas,
  (3) handling errors or async operations, (4) structuring files with section
  separators, or (5) creating factories, dispatch tables, or Effect pipelines.
---

# [H1][TYPESCRIPT-EFFECT]
>**Dictum:** *Six pillars govern TypeScript generation—algorithmic, parametric, polymorphic, functional, expressive, typed.*

<br>

Generate TypeScript code adhering to Effect ecosystem patterns.

**Pillars:**
1. **Algorithmic** — Derive values from frozen `B` constant
2. **Parametric** — Expose tuning via factory parameters
3. **Polymorphic** — Select implementation via dispatch tables
4. **Functional-Monadic** — Chain via Effect/Option pipelines
5. **Expression-Centric** — Ternaries, implicit returns, no blocks
6. **Strong-Typed** — Branded types via `@effect/schema`

**File Structure:**
```typescript
// --- [TYPES] -----------------------------------------------------------------
// --- [SCHEMA] ----------------------------------------------------------------
// --- [CONSTANTS] -------------------------------------------------------------
// --- [PURE_FUNCTIONS] --------------------------------------------------------
// --- [DISPATCH_TABLES] -------------------------------------------------------
// --- [EFFECT_PIPELINE] -------------------------------------------------------
// --- [ENTRY_POINT] -----------------------------------------------------------
// --- [EXPORT] ----------------------------------------------------------------
```

[CRITICAL]:
- [NEVER] `any` — use branded types.
- [NEVER] `let`/`var` — use `const` only.
- [NEVER] `if/else` — use dispatch tables or ternaries.
- [NEVER] `for`/`while` — use `.map`, `.filter`, Effect.
- [NEVER] `try`/`catch` — use Effect error channel.
- [NEVER] Default exports — use named exports (except `*.config.ts`).

---
## [1][ALGORITHMIC]
>**Dictum:** *Derive values from base constant via formula—zero hardcoded literals.*

<br>

Single frozen `B` constant per file. ALL values derive from `B` properties.

```typescript
const B = Object.freeze({
  fontSize: 16,
  ratio: 1.333,
} as const);

const derive = (step: number): number => B.fontSize * B.ratio ** step;

const scale = Object.freeze({
  sm: derive(-1),  // 12px = 16 * 1.333^-1
  md: derive(0),   // 16px = 16 * 1.333^0
  lg: derive(1),   // 21px = 16 * 1.333^1
} as const);
```

[IMPORTANT]:
- [ALWAYS] Define ONE `B` constant with `Object.freeze()`.
- [ALWAYS] Express derivations as inline calculations—formula IS the code.
- [ALWAYS] Trace every value to `B` through visible arithmetic.
- [NEVER] Numeric literals outside `B` constant.

---
## [2][PARAMETRIC]
>**Dictum:** *Expose tuning at call-site via factory parameters—zero buried controls.*

<br>

Factory functions accept partial config; merge with `B` defaults.

```typescript
const B = Object.freeze({
  timeoutMs: 5000,
  maxAttempts: 3,
} as const);

const createRetry = (overrides: Partial<typeof B> = {}) =>
  Object.freeze({
    config: { ...B, ...overrides },
    execute: <T>(fn: () => Promise<T>): Promise<T> => fn(),
  });

// Call-site tuning
const fast = createRetry({ timeoutMs: 1000 });
const resilient = createRetry({ maxAttempts: 5 });
```

[IMPORTANT]:
- [ALWAYS] Defaults in `B`; overrides at call-site.
- [ALWAYS] Factory returns frozen object.
- [NEVER] Hardcode tunable values in implementation.

---
## [3][POLYMORPHIC]
>**Dictum:** *Select implementation via keyed dispatch—zero conditional branching.*

<br>

Dispatch tables replace `if`/`else`/`switch`. Discriminated unions enable exhaustiveness.

```typescript
import { Schema } from 'effect';

const Shape = Schema.Union(
  Schema.Struct({ kind: Schema.Literal('circle'), radius: Schema.Number }),
  Schema.Struct({ kind: Schema.Literal('rect'), width: Schema.Number, height: Schema.Number }),
);
type Shape = typeof Shape.Type;

const handlers = {
  circle: (s: Extract<Shape, { kind: 'circle' }>) => Math.PI * s.radius ** 2,
  rect: (s: Extract<Shape, { kind: 'rect' }>) => s.width * s.height,
} as const satisfies Record<Shape['kind'], (s: never) => number>;

const area = (shape: Shape): number => handlers[shape.kind](shape as never);
```

[IMPORTANT]:
- [ALWAYS] Route via `handlers[discriminant](data)`.
- [ALWAYS] Enforce exhaustiveness with `satisfies Record<Discriminant, Handler>`.
- [NEVER] `if`/`else` for type-based dispatch.
- [NEVER] `switch`/`case` statements.

---
## [4][FUNCTIONAL-MONADIC]
>**Dictum:** *Chain operations via typed channels—Effect for async/failable, Option for nullable.*

<br>

Effect pipelines replace `try`/`catch`. Option wraps nullable values.

```typescript
import { Effect, Option, pipe } from 'effect';

class ValidationError {
  readonly _tag = 'ValidationError';
  constructor(readonly reason: string) {}
}

const processUser = (raw: { name?: string }) =>
  pipe(
    Option.fromNullable(raw.name),
    Option.map((name) => name.trim().toUpperCase()),
    Option.match({
      onNone: () => Effect.fail(new ValidationError('Missing name')),
      onSome: (name) => Effect.succeed({ name }),
    }),
  );
// Effect<{ name: string }, ValidationError, never>
```

[IMPORTANT]:
- [ALWAYS] Wrap nullable with `Option.fromNullable()`.
- [ALWAYS] Sequence via `pipe()` and `Effect.flatMap()`.
- [ALWAYS] Track outcomes in type parameters: `Effect<A, E, R>`.
- [NEVER] `try`/`catch` or `throw` in Effect code.
- [NEVER] Null checks or optional chaining in logic.

---
## [5][EXPRESSION-CENTRIC]
>**Dictum:** *Write code as value-producing expressions—zero statement blocks.*

<br>

Ternaries for conditionals. Implicit returns for arrows. Chain expressions.

```typescript
// Expression: ternary + implicit return
const classify = (age: number): string =>
  age < 18 ? 'minor' : age < 65 ? 'adult' : 'senior';

// Expression: chained transforms
const processUsers = (users: ReadonlyArray<{ name: string; age: number }>) =>
  users
    .filter((u) => u.age >= 18)
    .map((u) => ({ ...u, name: u.name.toUpperCase() }))
    .sort((a, b) => a.name.localeCompare(b.name));
```

[IMPORTANT]:
- [ALWAYS] Ternary `? :` over `if`/`else`.
- [ALWAYS] Arrow with implicit return: `x => x * 2`.
- [ALWAYS] Compose via `.map()`, `.filter()`, `pipe()`.
- [NEVER] Curly braces `{}` in single-expression contexts.
- [NEVER] Intermediate `let` bindings.

---
## [6][STRONG-TYPED]
>**Dictum:** *Brand domain primitives via @effect/schema—zero raw primitives in domain logic.*

<br>

Branded types enforce semantic boundaries. Schema validates at system edges.

```typescript
import { Schema } from 'effect';

// Branded primitive
const UserId = Schema.String.pipe(Schema.brand('UserId'));
type UserId = typeof UserId.Type;

// Validated struct
const UserSchema = Schema.Struct({
  id: UserId,
  email: Schema.String.pipe(Schema.pattern(/@/)),
  age: Schema.Number.pipe(Schema.positive()),
});
type User = typeof UserSchema.Type;

// Decode at boundary
const parseUser = Schema.decodeUnknownSync(UserSchema);
```

[IMPORTANT]:
- [ALWAYS] Brand domain primitives: `UserId`, `Email`, `IsoDate`.
- [ALWAYS] Validate at system boundaries (API input, external data).
- [ALWAYS] Derive type from schema: `typeof Schema.Type`.
- [NEVER] `any` or unbranded primitives in domain logic.

---
## [7][VALIDATION]
>**Dictum:** *Gates prevent non-compliant code generation.*

<br>

[VERIFY] Before completing any TypeScript generation:
- [ ] **B Constant:** Single frozen `B` with all tunable values.
- [ ] **Derivation:** All computed values trace to `B` via visible arithmetic.
- [ ] **Factory:** `createX` pattern with partial config merging `B`.
- [ ] **Dispatch:** Handlers object with `satisfies Record<K, Handler>`.
- [ ] **Effect:** Async/failable operations use Effect pipelines.
- [ ] **Option:** Nullable values wrapped with `Option.fromNullable()`.
- [ ] **Expression:** No `if`/`else` blocks; ternaries and implicit returns.
- [ ] **Branded:** Domain primitives use `Schema.brand()`.
- [ ] **Sections:** File uses canonical section separators.
- [ ] **Exports:** Named exports only (except `*.config.ts`).

[CRITICAL] Violation detected → Refactor before completion.
