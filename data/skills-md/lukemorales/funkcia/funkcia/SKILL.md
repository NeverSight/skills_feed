---
name: funkcia
description: Adopt Funkcia in TypeScript codebases using Option, Result, OptionAsync, ResultAsync, and module utilities such as Brand, SafeJSON, SafeURI, SafeURL, and TaggedError patterns. Use when migrating from null/throw/promise-rejection flows, designing typed error boundaries, or implementing domain-safe parsing and validation.
---

# Funkcia Adoption

Migrate existing error handling and validation into explicit, typed, chainable flows using Funkcia.

## Workflow

1. Start at boundaries, not internals.
   - Migrate I/O edges first: API handlers, DB repositories, queue consumers, file readers.
   - Keep module internals stable until boundary contracts return `Option`/`Result`.
2. Classify failure shape before coding.
   - Use `Option`/`OptionAsync` for expected absence without an error payload.
   - Use `Result`/`ResultAsync` for expected failure with explicit error semantics.
   - Treat unexpected callback throws/rejections as defects (`Panic`), not domain errors.
3. Define domain errors with `TaggedError` before refactoring call chains.
   - Model application failures (auth, validation, not-found, rate limit, external dependency).
   - Preserve causes when wrapping infrastructure failures.
4. Transform imperative control flow.
   - Replace `try/catch` with `Result.try` or `ResultAsync.try`.
   - Replace null/falsy branching with `fromNullable`/`fromFalsy`.
   - Prefer generator style for multi-step flows; use `map`, `andThen`, `filter`, `or`, `match` for focused one-step transforms.
5. Resolve once at the boundary.
   - Use `match` in handlers/controllers to map outcomes to transport responses.
   - For tagged error unions (`_tag`), prefer `exhaustive(error, { ... })` to enforce full case handling.
   - Avoid `unwrap` in business logic.
6. Verify behavior and type contracts.
   - Add runtime + `expectTypeOf` tests.
   - Run repository checks before completion.

## Defects vs Domain Errors

- Model expected business failures with `Option.none()` or `Result.error(...)`.
- Treat unexpected throws/rejections inside callbacks as defects and let them surface as `Panic`.
- Return expected failures; do not throw them.

| API | Domain behavior | Defect behavior |
| --- | --- | --- |
| `Option` / `Result` | Return `None` / `Error` for expected failures | Throws in combinator callbacks (`map`, `andThen`, `filter`, `or`, `match`, `tap`, etc.) become `Panic` |
| `OptionAsync` | `try` or `let` rejection/nullable resolves to `None` | `tap` throw/reject becomes `Panic` |
| `ResultAsync` | `try` rejection resolves to `Error` (`UnhandledException` or mapped error) | `let`, `tap`, or `tapError` throw/reject becomes `Panic` |

## Migration Strategy

- Migrate incrementally by vertical slices (feature or module), not by type across the whole codebase.
- Keep adapters during migration when legacy callers still expect nullable or throwing APIs.
- Preserve behavior first, then improve ergonomics.
- Recommend wrapping shared dependencies (database clients, API SDKs, queues) with `ResultAsync.resource` and mapping each dependency to pre-defined resource error types before wiring business flows.

## Pattern Transformations

### Throwing parse to `Result`

```ts
import { Result } from 'funkcia';

function parseWebhook(raw: string) {
  return Result.try(
    () => JSON.parse(raw),
    () => new Error('Invalid webhook payload'),
  );
}
```

### Nullable lookup to `Option`

```ts
import { Option } from 'funkcia';

function findPrimaryEmail(user: User) {
  return Option.fromNullable(user.emails.find((x) => x.primary))
    .map((email) => email.value.toLowerCase());
}
```

### Rejecting async call to `ResultAsync`

```ts
import { ResultAsync } from 'funkcia';

function fetchCheckoutSession(sessionId: string) {
  return ResultAsync.try(
    () => payments.getSession(sessionId),
    (cause) => new Error(`Failed to fetch session ${sessionId}: ${String(cause)}`),
  );
}
```

## Callback Hell vs Generators

### Callback hell / nested async handling

```ts
async function buildCheckoutSummary(userId: string): Promise<Result<CheckoutSummary, CheckoutError>> {
  try {
    const user = await usersApi.getById(userId);

    if (!user.defaultPaymentMethodId) {
      return Result.error(new MissingPaymentMethodError(user.id));
    }

    const paymentMethod = await paymentsApi.getMethod(user.defaultPaymentMethodId);
    const cart = await cartApi.getActiveCart(user.id);

    if (!cart) {
      return Result.error(new CartNotFoundError(user.id));
    }

    return Result.ok({
      userEmail: user.email,
      paymentMethod: paymentMethod.brand,
      total: cart.total,
    });
  } catch (cause) {
    return Result.error(new CheckoutInfrastructureError(cause));
  }
}
```

### Preferred generator style

```ts
function buildCheckoutSummary(userId: string): ResultAsync<CheckoutSummary, CheckoutError> {
  return ResultAsync.use(async function* () {
    const user = yield* ResultAsync.try(
      () => usersApi.getById(userId),
      (cause) => new CheckoutInfrastructureError(cause),
    );

    const paymentMethodId = yield* Result.fromNullable(
      user.defaultPaymentMethodId,
      () => new MissingPaymentMethodError(user.id),
    );

    const paymentMethod = yield* ResultAsync.try(
      () => paymentsApi.getMethod(paymentMethodId),
      (cause) => new CheckoutInfrastructureError(cause),
    );

    const cart = yield* Result.fromNullable(
      yield* ResultAsync.try(
        () => cartApi.getActiveCart(user.id),
        (cause) => new CheckoutInfrastructureError(cause),
      ),
      () => new CartNotFoundError(user.id),
    );

    return ResultAsync.ok({
      userEmail: user.email,
      paymentMethod: paymentMethod.brand,
      total: cart.total,
    });
  });
}
```

## Reference Map

- `references/tagged-errors.md`: Model real application failures with `TaggedError`.
- `references/exhaustive.md`: Use `exhaustive` and `corrupt` for type-safe branching.
- `references/brand.md`: Build branded domain primitives and safe parsers.
- `references/exceptions.md`: Use built-in exception types and `panic`.
- `references/safe-functions.md`: Safely parse JSON and normalize URLs/URIs.
- `references/generators.md`: Preferred generator-based style for `Option`/`Result` and async variants.
- `references/do-notation.md`: Context-accumulation style with `Do`, `bind`, `let`, and `bindTo`.
- `references/resources.md`: Wrap shared resources with `ResultAsync.resource` so operations return expected values or pre-defined resource errors.
