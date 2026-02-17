---
name: coding
description: "General coding best practices and software engineering principles to build robust, maintainable, and scalable software."
---

# General Coding Best Practices

## Overview
This skill provides a set of core principles and practices for software development. Use this when implementing new features, refactoring existing code, or reviewing code to ensure high quality and maintainability.

## Core Principles
- **DRY (Don't Repeat Yourself):** Avoid logic duplication. If you find yourself writing the same code twice, abstract it.
- **KISS (Keep It Simple, Stupid):** Prefer simple, straightforward solutions over complex ones. Avoid over-engineering.
- **YAGNI (You Ain't Gonna Need It):** Don't implement features or abstractions until they are actually needed.
- **SOLID Principles:**
    - Single Responsibility: A class/function should have one reason to change.
    - Open/Closed: Software entities should be open for extension but closed for modification.
    - Liskov Substitution: Subtypes must be substitutable for their base types.
    - Interface Segregation: Many client-specific interfaces are better than one general-purpose interface.
    - Dependency Inversion: Depend on abstractions, not concretions.

## Implementation Guidelines
- **Clean Code:** Use descriptive names for variables, functions, and classes. Write code that is easy to read and understand.
- **Small Functions:** Keep functions small and focused on a single task.
- **Error Handling:** Use proactive error handling. Validate inputs and handle exceptions gracefully.
- **Documentation:** Document the *why*, not the *what*. Use self-documenting code where possible.
- **Security:** Sanitize inputs, avoid hardcoding secrets, and follow the principle of least privilege.
- **Performance:** Be mindful of time and space complexity, but avoid premature optimization.

## Automated Analysis & Quality Control
- **Static Analysis & Linting:** Every project MUST have automated linting, formatting and static analysis (e.g., ESLint, Prettier, Ruff, Sonar). 
    - **Check:** Identify if these tools are configured.
    - **Propose:** If missing, immediately propose adding them (e.g., `npm install --save-dev eslint`).
- **Automated Tests:** Ensure there is a test runner configured (e.g., Jest, Pytest).
    - **Check:** Look for `tests/` directory or test configurations in `package.json`/`pyproject.toml`.
    - **Propose:** If missing, propose a testing framework and initial setup.

## Verifying Code Changes
Before completing any task, you MUST perform the following verification loop:
1.  **Simplification:** Use the code-simplifier plugin to make the code cleaner and more maintainable.
2.  **Self-Code Review:**
    - Review the changes against the task requirements.
    - Ensure compliance with this `coding` skill (DRY, KISS, SOLID).
    - Check for potential security vulnerabilities or performance regressions.
3.  **Static Analysis & Linting:**
    - Run the project's linting/format commands (e.g., `npm run lint`, `prettier --check .`).
    - Fix all reported issues.
4.  **Unit Testing:**
    - **Add Missing Tests:** If new logic was added, write concise unit tests covering the happy path and edge cases.
    - **Run Tests:** Execute the test suite (e.g., `npm test`, `pytest`).
    - **Verification:** Ensure all tests pass. If they fail, fix the implementation or the test.

## Key Principles
- **Clarity over Cleverness:** Write code for humans first, machines second.
- **Consistency:** Follow the established patterns and style of the existing codebase.
- **Composition over Inheritance:** Prefer combining simple objects to build complex ones rather than creating deep inheritance hierarchies.
