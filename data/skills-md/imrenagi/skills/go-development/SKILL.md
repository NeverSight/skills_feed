---
name: go-development
description: Best practices for Go development, covering domain-driven design, context usage, and structured logging.
---

# Go Development

This skill provides best practices for building robust Go applications. It focuses on domain-driven design, proper context propagation, and structured logging.

## When to Apply

Reference these guidelines when:

- **Implementing Business Logic**: Developing domain models and domain enums.
- **Managing Context**: Propagating context correctly through your application layers.
- **Implementing Logging**: Using structured, contextual logging with zerolog.
- **Refactoring**: Improving code structure and consistency across the codebase.

## Quick Reference

| Rule                                                     | Impact   | Description                                                           |
| :------------------------------------------------------- | :------- | :-------------------------------------------------------------------- |
| [Favor Rich Domain Models](references/domain-driven.md)  | **HIGH** | Encapsulate business logic in domain entities; includes enum patterns |
| [Proper Context Usage](references/context-usage.md)      | **HIGH** | Propagate deadlines, cancellation, and metadata correctly             |
| [Pass Context to Loggers](references/logging-context.md) | **HIGH** | Use zerolog with context for request-scoped logging                   |

## How to Use

1.  **Read the Rules**: Before starting a new feature or refactor, browse the relevant rule files in `references/`.
2.  **Follow the Examples**: Use the provided code patterns as templates for your implementation.
3.  **Ensure Consistency**: Apply the same patterns (e.g., context propagation, logging) across all layers of the application.

For any specific questions on implementation, refer to the individual rule files which contain detailed explanations and code snippets.
