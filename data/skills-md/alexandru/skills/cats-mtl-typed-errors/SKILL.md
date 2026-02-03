---
name: cats-mtl-typed-errors
description: Scala typed errors with Cats MTL Raise/Handle and allow/rescue. Use for designing custom domain error types without EitherT, while keeping Cats Effect and ecosystem composition. Covers Scala 2/3 syntax and IO-only or F[_] usage.
---

# Cats MTL Typed Errors (Scala)

## Quick start
- Define a domain error type; it may or may not extend Throwable depending on context.
- Use Cats MTL `Raise[F, E]` in functions that can raise errors.
- Use `Handle.allow`/`rescue` (Scala 3) or `Handle.allowF` (Scala 2) to introduce a scoped error capability and handle it like try/catch.
- Prefer Cats MTL over `IO[Either[E, A]]` and avoid `EitherT[IO, E, A]`; pure functions returning `Either[E, A]` are fine at API boundaries.
- `F[_]` is optional: you can write `IO`-specific code or keep `F[_]` for polymorphism, depending on the project.

## Workflow
1. Model domain errors as sealed ADTs (Scala 2) or enums (Scala 3)
2. For effectful code that can raise errors, require `Raise[F, E]` (and `Monad[F]` or `Applicative[F]`).
3. Raise errors with `.raise` and return successful values with `pure`.
4. At a boundary, use `Handle.allow` (Scala 3) or `Handle.allowF` (Scala 2) to create a scope where raises are valid.
5. Close the scope with `.rescue` to handle each error case explicitly.
6. Keep Cats Effect resource and concurrency semantics intact by staying in the monofunctor error channel.

## Patterns to apply
- **Typed errors in signatures**: treat the error type parameter `E` as the checked-exception channel in the function signature.
- **Scoped error capabilities**: require `Raise[F, E]` in functions that can fail; use `Handle[F, E]` when you also need to recover.
- **Scala 3 ergonomics**: prefer `using` and context functions with `allow`; type inference is significantly better.
- **Scala 2 compatibility**: use `allowF` and explicit implicit parameters; expect more braces and explicit types.
- **Interop with pure code**: use pure `Either[E, A]` for parsing/validation and lift into `F` where needed.
- **Avoid transformer stacks**: do not reach for `EitherT` just to get a typed error channel; Cats MTL provides the capability without the stack.
- **Avoid sealed-on-sealed inheritance**: model error hierarchies with composition (wrapper case classes), not sealed inheritance chains.

## References
- Load `references/custom-error-types.md` for detailed guidance, Scala 2/3 syntax, and rationale from the Typelevel article.
