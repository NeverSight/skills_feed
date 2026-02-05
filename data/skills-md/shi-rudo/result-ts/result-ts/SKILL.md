---
name: result-ts
description: A skill to help integrate, refactor, and guide the proper usage of the `@shirudo/result` library. Use this skill when you want to introduce `@shirudo/result` into a project, refactor existing code to use `Result` types, or get guidance on best practices and common patterns.
version: 1.2
---

# `@shirudo/result` Skill

This skill helps you effectively use the package `@shirudo/result` in your TypeScript projects.

## What is a `Result`?
A `Result<T, E>` is a typed return value that represents **either** success **or** failure:

- `Ok<T>`: the operation succeeded and contains a value of type `T`.
- `Err<E>`: the operation failed and contains an error value of type `E`.

This makes error handling **explicit** in the type system: functions return a `Result` instead of throwing.  
You then **compose** operations (e.g. via `.pipe()` / `.pipeAsync()`), where failures short-circuit and propagate as `Err`.

## When to Use

Use this skill when you need to:

- **Integrate `@shirudo/result`**: Introduce the library into an existing codebase.
- **Refactor Code**: Convert existing code (e.g., `try/catch` blocks, null checks) to use `Result` types.
- **Understand Core Concepts**: Get guidance on the library's functions and best practices.

## How to Use

1.  **Consult the References**: Depending on your needs, refer to the following guides in the `references/` directory:
    *   `api-cheatsheet.md`: A quick reference for all major `@shirudo/result` functions.
    *   `refactoring-patterns.md`: Provides concrete examples of how to refactor your code.
    *   `best-practices.md`: Offers guidance on using the library idiomatically.

2.  **Ask for Refactoring Help**: You can ask me to refactor a specific piece of code. For example: "Refactor this function to use @shirudo/result".

3.  **Ask for Explanations**: You can ask for explanations of specific functions. For example: "Explain how to use `flatMap` in @shirudo/result".