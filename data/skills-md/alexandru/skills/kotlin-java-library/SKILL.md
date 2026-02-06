---
name: kotlin-java-library
description: Kotlin design for Java libraries and Java consumers. Use when building Kotlin code intended for Java callers, aligning with Java interop, JVM annotations, records, and backward/binary compatibility rules.
---

# Kotlin Java Library Design

## Quick start
- Design Kotlin APIs as if the primary caller is Java: explicit overloads, stable names, and predictable nullability.
- Use JVM interop annotations (`@JvmOverloads`, `@JvmStatic`, `@JvmField`, `@JvmName`) to shape the Java surface.
- Prefer Java-friendly top-level functions with `@file:JvmName`, and use `@file:JvmMultifileClass` when splitting across files.
- Use `fun interface` for Java callbacks; avoid function types that return `Unit`.
- Document checked exceptions with `@Throws` and return defensive copies for read-only collections.
- Follow binary compatibility rules; add overloads instead of changing signatures.
- Read `references/kotlin-java-library.md` for examples, recipes, and checklists.

## Workflow
1. Identify which public APIs must be Java-friendly (constructors, factories, utilities).
2. Shape the Java surface with JVM annotations and explicit overloads.
3. Audit public signatures for Java stability (names, nullability, overload sets, and collection exposure).
4. Apply backward-compatibility rules before publishing.
5. Validate with Java call-site examples.

## Rules of thumb
- Avoid Kotlin-only surface features in public API: default args without overloads, extension-only entry points, and name clashes.
- Use `@JvmOverloads` for Java-callable optional parameters, and provide explicit overloads when behavior differs.
- Use `@JvmStatic` for companion/object members meant to be static in Java.
- Use `@JvmField` only for constants or immutable fields you want exposed as fields.
- Use `@JvmName` to resolve signature clashes or to provide a stable Java name.
- Avoid `Nothing` in public generic signatures; it becomes raw types in Java.

## Output expectations
- Offer Java-call-site examples when proposing API changes.
- Call out binary compatibility risks and safer alternatives.

## References
- Load `references/kotlin-java-library.md` for interop details, examples, and testing prompts.
