---
name: cats-effect-io
description: Scala functional programming with Cats Effect IO and typeclasses. Use for wrapping side effects, modeling purity, choosing Sync/Async/Temporal/Concurrent, handling blocking I/O, and composing resources, fibers, and concurrency safely.
---

# Cats Effect IO (Scala)

## Quick start
- Treat every side effect as an effect value: return `IO[A]`, `SyncIO[A]`, or `F[A]` with `F[_]: Sync`/`Async`/`Temporal` as needed.
- Wrap Java blocking calls with `IO.blocking` or `IO.interruptible` (or `Sync[F].blocking`/`interruptible`).
- Use `Resource` to acquire/release resources and `IOApp` for program entry points.
- Prefer structured concurrency (`parTraverse`, `parMapN`, `background`, `Supervisor`) over manual fiber management.
- Read `references/cats-effect-io.md` for concepts, recipes, and FAQ guidance.
- For deeper `Resource` guidance, use the `cats-effect-resource` skill (install: `npx skills add https://github.com/alexandru/skills --skill cats-effect-resource`).

## Workflow
1. Classify side effects and choose the effect type: `IO` directly or polymorphic `F[_]` with the smallest required Cats Effect typeclass (`Sync`, `Async`, `Temporal`, `Concurrent`).
2. Wrap side-effectful code using `IO(...)`, `IO.blocking`, `IO.interruptible`, or `IO.async` (or their `Sync`/`Async` equivalents).
3. Manage resources with `Resource` or `bracket` and keep acquisition/release inside effects.
4. Compose effects with `flatMap`/for-comprehensions and collection combinators (`traverse`, `parTraverse`).
5. Use concurrency primitives (`Ref`, `Deferred`, `Queue`, `Semaphore`, `Supervisor`) and structured concurrency to avoid fiber leaks.

## Side-effect rules (apply to `IO`, `SyncIO`, and to `F[_]: Sync/Async`)
- All side-effectful functions must return results wrapped in `IO` (or `F[_]` with Cats Effect typeclasses).
- Side-effects include all non-determinism (call sites are not referentially transparent):
  - Any I/O (files, sockets, console, databases).
  - `Instant.now()`, `Random.nextInt()`.
  - Any read from shared mutable state (the read itself is the side effect).
  - Returning mutable data structures (for example, `Array[Int]`).

## Blocking I/O rules
- Java blocking methods must be wrapped in `IO.blocking` or `IO.interruptible` (or `Sync[F].blocking`/`interruptible`) so they run on the blocking pool.
- Prefer `IO.interruptible` for methods that may throw `InterruptedException` or `IOException`, but not for resource disposal.
- Use `IO.blocking` for cleanup/disposal (`Closeable#close`, `AutoCloseable#close`).

## Output expectations
- Make side effects explicit in signatures (`IO`/`SyncIO` or `F[_]: Sync/Async`); the guidance here applies equally to concrete `IO` and polymorphic `F[_]`.
- Use the smallest typeclass constraint that supports the needed operations.
- Keep effects as values; do not execute effects in constructors or top-level vals.

## References
- Load `references/cats-effect-io.md` for documentation summary and patterns.
- For concrete samples, read `references/cats-effect-io.md`.
- Use the `cats-effect-resource` skill for Resource-specific workflows and patterns (install: `npx skills add https://github.com/alexandru/skills --skill cats-effect-resource`).
