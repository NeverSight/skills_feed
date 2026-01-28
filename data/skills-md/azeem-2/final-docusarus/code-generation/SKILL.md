---
name: code-generation
description: Standards and best practices for generating educational code examples. Ensures consistency, readability, and pedagogical value in all code snippets.
version: 1.0.0
tags: [coding, standards, education, python, best-practices]
---

# Code Generation Skill

This skill defines the standards for generating code examples in educational content. The goal is to produce code that is not just functional, but exemplary—teaching best practices by example.

## Core Philosophy

1.  **Readability First**: Code is read more often than written. Optimize for the reader.
2.  **Pedagogical Clarity**: Avoid "clever" one-liners. Prefer explicit, step-by-step logic.
3.  **Standard Compliance**: Strictly follow language-specific style guides (e.g., PEP 8 for Python).
4.  **Self-Documenting**: Variable names should explain their purpose. Comments should explain *why*, not *what*.

## General Standards

### 1. Naming Conventions
- **Descriptive Names**: Use `user_age` instead of `a`, `total_price` instead of `tp`.
- **No Single Letters**: Exception for loop counters (`i`, `j`) in generic contexts, but prefer `for item in items`.
- **Consistency**: Stick to the language's standard (snake_case for Python, camelCase for JS).

### 2. Comments and Documentation
- **Explain the 'Why'**:
    - ❌ `x = x + 1  # Increment x`
    - ✅ `retry_count += 1  # Track attempts to prevent infinite loop`
- **Docstrings**: All functions and classes must have a docstring explaining inputs, outputs, and purpose.
- **Inline Comments**: Use sparingly for complex logic.

### 3. Error Handling
- **No Silent Failures**: Never use bare `try...except` (Python) or empty catch blocks.
- **Explicit Exceptions**: Catch specific errors (e.g., `ValueError`, `FileNotFoundError`).
- **Educational Value**: Show students how to handle errors gracefully.

### 4. "No Magic Numbers"
- Define constants for literal values.
- ❌ `if status == 4:`
- ✅ `READY_STATUS = 4; if status == READY_STATUS:`

## Language-Specific Rules

### Python
- **Style**: Strict PEP 8.
- **Type Hints**: Use type hints for function arguments and return values.
    ```python
    def calculate_total(price: float, tax_rate: float) -> float:
        """Calculates total price including tax."""
        return price * (1 + tax_rate)
    ```
- **f-strings**: Prefer f-strings over `%` formatting or `.format()`.

### JavaScript / TypeScript
- **Style**: Standard JS style (Airbnb or similar).
- **Variables**: Use `const` by default, `let` only when reassignment is needed. Never `var`.
- **Async/Await**: Prefer `async/await` over raw Promises.

## Pedagogical Patterns

### 1. The "Before and After"
When teaching a better way to do something, show the "naive" approach first (labeled as such), then the "professional" approach.

### 2. Progressive Complexity
Start with a minimal working example. Add complexity (error handling, edge cases) in subsequent steps.

### 3. Runnable Snippets
Ensure code snippets are self-contained and runnable whenever possible. Include necessary imports.

## Quality Checklist

Before finalizing any code snippet, verify:
- [ ] Does it follow the language style guide?
- [ ] Are variable names descriptive?
- [ ] Are "magic numbers" replaced with constants?
- [ ] Is there a docstring/comment explaining the purpose?
- [ ] Is error handling appropriate for the context?
- [ ] If it's a "bad example", is it clearly labeled?
