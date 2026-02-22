---
name: clean-code-principles
description: Enforce clean code principles when writing or reviewing code. Use when writing new functions, refactoring existing code, or reviewing code for readability and maintainability. Covers guard clauses, modularization, naming conventions, and more.
---

# Clean Code Principles

A collection of principles and patterns for writing clean, readable, and maintainable code.

## When to Use This Skill

- Writing new functions or methods
- Refactoring nested or complex code
- Reviewing code for readability
- Discussing code quality improvements

> **Note:** The principles and rules in each document apply to all programming languages. Examples are shown in a specific language for concreteness, but the patterns themselves are language-agnostic.
>
> **Important:** When refactoring, remove comments that are no longer relevant to the changed code. However, comments that are still valid and provide useful context (e.g., *why* a decision was made, business rules, workarounds, warnings) must be preserved.

## Principles Overview

| Principle | Description | Reference |
| --- | --- | --- |
| Guard Clause Pattern | Fail fast with early returns, keep code flat | `guard-clause-pattern.md` |
| Function Decomposition | Break large functions into small, focused units | `function-decomposition.md` |
| Magic Numbers & Strings | Replace unexplained literals with named constants or enums | `magic-numbers-and-strings.md` |
| DRY Principle | Eliminate duplicated logic with shared abstractions | `dry-principle.md` |
| Conditional Simplification | Reduce complex branching into clear, readable conditions | `conditional-simplification.md` |
| Boolean & Flag Parameters | Replace boolean params with enums, methods, or option objects | `boolean-and-flag-parameters.md` |

## Core Philosophy

1. **Readability First** — Code is read far more often than it is written
2. **Fail Fast** — Handle errors and edge cases early, keep the happy path clear
3. **Single Responsibility** — Each function/class should do one thing well
4. **Minimal Nesting** — Flat code is easier to follow than deeply nested code
5. **Meaningful Names** — Names should reveal intent without needing comments
6. **DRY, but not at the cost of clarity** — Avoid premature abstraction
