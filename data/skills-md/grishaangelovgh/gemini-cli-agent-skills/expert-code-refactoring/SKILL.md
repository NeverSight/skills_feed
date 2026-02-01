---
name: expert-code-refactoring
description: "Expert code refactoring for Java, JavaScript, and React projects. Focuses on SOLID principles, design patterns, and idiomatic improvements while ensuring test stability."
---

# Refactoring Skill

This skill guides the agent in refactoring codebases by identifying technical debt and applying industry-standard patterns tailored to the specific technology stack.

## General Refactoring Workflow

1.  **Analyze Context:** Read the file and its associated tests. Identify dependencies and usage patterns.
2.  **Verify Tests:** Before any changes, run existing tests to ensure a stable baseline.
3.  **Identify Smells:** Look for long methods, deep nesting, duplicate code, or tight coupling.
4.  **Incremental Changes:** Apply transformations in small, verifiable steps.
5.  **Re-verify:** Run tests after each significant change.

## Architecture & Clean Code (Global)

- **Naming:** Rename variables, functions, and classes to be descriptive and reveal intent. Avoid abbreviations.
- **AHA Programming:** Avoid Hasty Abstractions. Only abstract code when the duplication is clear and the abstraction doesn't make the code harder to follow.
- **Functions:** Keep functions small. Aim for a low number of parameters (prefer objects/records for many parameters).
- **Cognitive Load:** Reduce nesting levels (aim for max 2-3 deep). Use early returns to keep the "happy path" aligned to the left.

## Refactoring for Testability

- **Dependency Injection (DI):** Replace hardcoded instances or static calls with injected dependencies (via constructor or parameters).
- **Interface Segregation:** If a class depends on a large interface but only uses one method, extract a smaller interface.
- **Pure Functions:** Extract business logic into pure functions that don't depend on external state or side effects, making them trivial to unit test.
- **Mocking Boundaries:** Identify "seams" where you can inject mocks (e.g., Database, Network, System Clock).

## Legacy Code Techniques (Safe Changes)

- **Characterization Tests:** If tests are missing, write "Golden Master" tests that record the current behavior *before* changing it.
- **Sprout Method:** When adding a feature to a messy method, write the new logic in a new, clean method and call it from the old one.
- **Wrap Method:** Add new behavior by creating a new method with the same signature that calls the old method and then adds the new logic.
- **Break Dependencies:** Use the "Extract and Override" pattern to isolate untestable static calls or constructors in a protected method that can be overridden in a test subclass.

## Common Code Smells & Solutions

| Smell | Description | Refactoring Pattern |
| :--- | :--- | :--- |
| **Magic Literals** | Hardcoded numbers/strings. | **Extract Constant** or **Enum**. |
| **Long Method** | Method does too many things. | **Extract Method**. |
| **Large Class** | Too many responsibilities. | **Extract Class** or **Extract Interface**. |
| **Feature Envy** | Method uses another object's data more. | **Move Method**. |
| **Primitive Obsession** | Using primitives for domain concepts. | **Introduce Value Object**. |
| **Multi‑File Change Requirement** | One change affects many files. | **Move Field** or **Inline Class** to centralize. |

## Language Specifics

### Java
- **SOLID & Modern Features:** Use `record` (Java 14+), `sealed` classes (Java 17+), and **Switch Pattern Matching**.
- **Streams & Optional:** Replace imperative loops with `Stream`. Use `Optional` to eliminate null checks.
- **Immutability:** Use `final` and immutable collections (`List.of`, `Map.of`).
- **Exception Handling:** Use try-with-resources. Avoid catching `Throwable` or `Exception` generically.

### JavaScript / TypeScript
- **Modern Syntax:** `const` by default, destructuring, spread/rest, arrow functions.
- **TypeScript Advanced:** **Discriminated Unions**, **Utility Types** (`Pick`, `Omit`), and **Custom Type Guards**.
- **Data Integrity:** Use Zod or similar for runtime validation at API/IO boundaries.
- **Async Patterns:** Prefer `Promise.all` for concurrency; avoid "async-await" inside loops where possible.

### React
- **Component Design:** Decompose large components. Extract logic into **Custom Hooks**.
- **State Management:** **Principle of Least Privilege** (keep state local). Avoid **Prop Drilling** with Context or Composition.
- **Performance:** Use `useMemo`/`useCallback` for stable references. Avoid inline function definitions in props of memoized children.
- **Testing:** Focus on user behavior and accessible roles (`getByRole`) via **React Testing Library**.

## Security & Reliability
- **Input Validation:** Sanitize and validate all external input.
- **Secrets:** Never hardcode keys; use environment variables.
- **Dependencies:** Update deprecated/vulnerable packages discovered during refactoring.

## Constraints
- Never change external APIs or public interfaces without explicit user permission.
- Always maintain or improve test coverage.
- Adhere to the project's existing linting and formatting rules.
