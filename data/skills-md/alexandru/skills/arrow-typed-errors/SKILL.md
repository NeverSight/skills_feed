---
name: arrow-typed-errors
description: Kotlin + Arrow typed error handling using Raise DSL and wrapper types (Either/Option/Ior/Result/nullable), including validation with accumulation, interop with exceptions, and custom error wrappers. Use for designing or refactoring error modeling, converting exception-based flows, building smart constructors, accumulating validation errors, or integrating Outcome/Progress-style wrappers with Arrow.
---

# Arrow Typed Errors (Kotlin)

## Quick start
- Classify the failure first: logical failure (typed error) vs exceptional failure (exception).
- Pick the surface type:
  - `Raise<E>` + builder (`either {}`/`option {}`/`nullable {}`) for composable logic.
  - Wrapper type (`Either`/`Option`/`Ior`/`Result`/nullable) for API boundaries.
- Read `references/typed-errors.md` for API details and patterns before coding if unsure.

## Workflow
1. Model errors as sealed types.
2. Implement happy-path logic with Raise DSL (prefer `either {}` or `nullable {}` depending on output).
3. Guard invariants with `ensure` / `ensureNotNull`.
4. Interop with external code:
   - Use `catch`/`Either.catchOrThrow` to convert expected exceptions into typed errors.
5. Compose with `.bind()` and transform errors with `withError` or `recover`.
6. For validation across fields or lists, use accumulation (`zipOrAccumulate`, `mapOrAccumulate`, or `accumulate`).
7. Expose wrapper types at module boundaries; keep Raise internally when possible.

## Patterns to apply
- **Smart constructors (parse, don't validate)**: make constructors private; expose `invoke` returning `Either`.
- **Validation accumulation**: use `EitherNel` and `zipOrAccumulate`/`mapOrAccumulate`.
- **Wrapper choice**:
  - Prefer nullable for optional values unless nested nullability issues exist; then use `Option`.
  - Use `Either` for disjoint success/failure; `Ior` only when success + warning is meaningful.
  - Use `Result` only when errors are `Throwable` and interop with stdlib APIs is required.
- **Error translation across layers**: use `withError` to map inner errors to outer domain errors.
- **Drop error types explicitly**: wrap `bind` with `ignoreErrors` when moving from informative error types to `Option`/nullable flows.
- **Avoid sealed-on-sealed inheritance**: model error hierarchies with composition (wrapper data classes), not sealed inheritance chains.

## References
- Load `references/typed-errors.md` for API details, error accumulation, wrapper-specific guidance, and sample snippets.
