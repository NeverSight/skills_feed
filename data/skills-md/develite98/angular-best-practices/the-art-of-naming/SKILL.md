---
name: the-art-of-naming
description: Comprehensive naming convention guide for TypeScript and Angular applications. Covers casing rules (camelCase, PascalCase, UPPER_CASE), prefix conventions (I for interfaces, _ for private, T for generics), boolean naming, the S-I-D principle (Short, Intuitive, Descriptive), context duplication, and structured naming patterns (P/HC/LC for variables, A/HC/LC for functions). Use when writing, reviewing, or refactoring TypeScript code. Triggers on tasks involving naming, variables, functions, interfaces, or code style.
license: MIT
metadata:
  author: community
  version: "1.0.0"
---

# The Art of Naming

Naming things is hard. This guide provides a structured methodology for naming variables, functions, classes, interfaces, and everything in between — producing code that is self-documenting, consistent, and readable.

## When to Apply

Reference these guidelines when:
- Naming new variables, functions, classes, interfaces, or types
- Reviewing code for naming consistency
- Refactoring code to improve readability
- Setting up linting rules for a new project
- Onboarding new team members to the codebase conventions

## Core Principles

- **S-I-D** — Every name must be **S**hort, **I**ntuitive, and **D**escriptive
- **No Contractions** — `onItemClick`, never `onItmClk`
- **Correct Casing** — camelCase for members, PascalCase for types, UPPER_CASE for constants
- **Meaningful Prefixes** — `I` for interfaces, `_` for private, `is/has/should` for booleans
- **No Context Duplication** — `MenuItem.handleClick()`, not `MenuItem.handleMenuItemClick()`
- **Structured Patterns** — P/HC/LC for variables, A/HC/LC for functions
- **Correct Action Verbs** — `get` (sync), `fetch` (async), `remove` (collection), `delete` (permanent)

## Rule Categories by Priority

| Priority | Rule | Impact | File |
|----------|------|--------|------|
| 1 | Casing Convention | CRITICAL | `naming-casing-convention` |
| 2 | S-I-D + No Contractions | CRITICAL | `naming-sid` |
| 3 | Prefix Conventions | HIGH | `naming-prefix-convention` |
| 4 | Boolean Naming | HIGH | `naming-boolean` |
| 5 | Context Duplication | HIGH | `naming-context-duplication` |
| 6 | Function Naming (A/HC/LC) | HIGH | `naming-function-pattern` |
| 7 | Variable Naming (P/HC/LC) | MEDIUM | `naming-variable-pattern` |

## Quick Reference

### 1. Casing Convention (CRITICAL)

- `naming-casing-convention` - camelCase for variables/functions, PascalCase for classes/enums/types, UPPER_CASE for exported constants

### 2. S-I-D + No Contractions (CRITICAL)

- `naming-sid` - Names must be Short, Intuitive, Descriptive — never use contractions

### 3. Prefix Conventions (HIGH)

- `naming-prefix-convention` - `I` for interfaces, `_` for private members, `T`/`R`/`U`/`V`/`K` for generics

### 4. Boolean Naming (HIGH)

- `naming-boolean` - Prefix booleans with `is`/`has`/`should`/`can`, keep names positive

### 5. Context Duplication (HIGH)

- `naming-context-duplication` - Don't repeat class/component name in member names

### 6. Function Naming (HIGH)

- `naming-function-pattern` - A/HC/LC pattern + correct action verbs (get/set/fetch/remove/delete/compose/handle)

### 7. Variable Naming (MEDIUM)

- `naming-variable-pattern` - P/HC/LC pattern for structured, predictable variable names

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/naming-casing-convention.md
rules/naming-sid.md
rules/naming-prefix-convention.md
rules/naming-boolean.md
rules/naming-context-duplication.md
rules/naming-function-pattern.md
rules/naming-variable-pattern.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code examples with explanation
- Correct code examples with explanation
- Summary tables and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
