---
name: go-error-handling
description: Best practices for error handling in Go applications, including error wrapping, domain errors, sentinel vs typed errors, and gRPC error mapping.
---

# Go Error Handling Skill

This skill provides guidelines for implementing robust error handling in Go applications. Apply these practices when writing, reviewing, or refactoring Go code that involves error creation, propagation, or handling.

## When to Use This Skill

Use this skill when:

- Creating new functions or methods that return errors
- Implementing repository or service layers that interact with databases or external services
- Building gRPC or HTTP handlers that need to translate errors to status codes
- Reviewing code for proper error handling patterns
- Debugging error propagation issues

## Core Principles

## Error Handling Decision Flowchart

```
Error Occurs
    │
    ▼
Is it from an external dependency (DB, API, etc)?
    │
    ├── YES → Map to domain error + wrap with %w
    │
    └── NO → Is it a business rule violation?
              │
              ├── YES → Return appropriate domain error
              │
              └── NO → Wrap and propagate with context

At Handler Layer:
    │
    ▼
Log full error, return safe message to client
```

## References

| Document                                                  | Description                                       | When to Use                                                                                                                                                              |
| --------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [error-wrapping.md](references/error-wrapping.md)         | How to wrap errors with `%w` for chain inspection | Use when returning errors from functions to preserve the error chain. Essential if callers need to use `errors.Is()` or `errors.As()`.                                   |
| [error-types.md](references/error-types.md)               | When to use sentinel vs typed errors              | Use when deciding between `var ErrXxx = errors.New()` and custom error structs. Prefer typed errors when you need to attach metadata like resource IDs or permissions.   |
| [error-domain-error.md](references/error-domain-error.md) | Defining and using domain-specific errors         | Use when building repository or service layers. Maps technology-specific errors (e.g., `sql.ErrNoRows`) to domain errors to decouple business logic from infrastructure. |
| [server-grpc-error.md](references/server-grpc-error.md)   | gRPC error handling and status codes              | Use when implementing gRPC handlers. Covers mapping domain errors to gRPC status codes and adding rich error details like field violations.                              |
