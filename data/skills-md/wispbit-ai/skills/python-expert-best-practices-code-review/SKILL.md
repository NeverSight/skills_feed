---
name: python-expert-best-practices-code-review
description: Python best practices for writing production-grade code. This skill should be used when writing, reviewing, or refactoring Python code. Triggers on tasks involving Python development, error handling patterns, dictionary operations, and code quality improvements.
license: MIT
metadata:
  author: wispbit
  version: "1.0.0"
---

# Python 3.14+ Expert Best Practices

Simple, pragmatic, opinionated. Only what matters for writing production-grade python code.

## When to Apply

Reference these guidelines when:
- Writing Python functions, classes, or modules
- Reviewing Python code for error handling issues
- Refactoring existing Python codebases
- Implementing data validation and API boundaries
- Optimizing error detection and debugging patterns

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Error Handling | CRITICAL | `dict-`, `operators-` |
| 2 | Common Bugs | CRITICAL-HIGH | `no-mutable-`, `no-generic-` |
| 3 | Code Clarity | HIGH-MEDIUM | `listcomp-`, `no-inline-` |
| 4 | Code Style | LOW | `avoid-`, `unnecessary-` |

## Quick Reference

- `dict-required-keys` - Use `d[key]` for required dictionary keys to fail fast with KeyError
- `no-mutable-defaults` - No mutable defaults in function/method parameters
- `operators-return-notimplemented` - Return NotImplemented for unsupported operand types and design + vs += intentionally
- `no-generic-except` - Avoid generic except clauses to prevent hiding unexpected errors
- `listcomp-no-side-effects` - List comprehensions must produce a value you use (no side-effect listcomps)
- `no-inline-imports` - Place all import statements at the top of the file
- `avoid-explanatory-comments` - Avoid unnecessary comments for self-documenting code
- `unnecessary-else-blocks` - Avoid unnecessary else blocks after return/break/continue statements

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/dict-required-keys.md
rules/no-mutable-defaults.md
rules/operators-return-notimplemented.md
rules/no-generic-except.md
rules/listcomp-no-side-effects.md
rules/no-inline-imports.md
rules/avoid-explanatory-comments.md
rules/unnecessary-else-blocks.md
```

Each rule file contains:
- Brief explanation of why it matters
- When to use and when not to use the pattern
- Implementation requirements
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references