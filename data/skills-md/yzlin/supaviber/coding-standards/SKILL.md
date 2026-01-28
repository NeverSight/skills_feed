---
name: coding-standards
description: Guide for writing clean, maintainable code following industry best practices and design principles like DRY, SOLID, and composition patterns. Use when writing any code to ensure consistency, readability, and long-term maintainability across all programming languages.
license: MIT
compatibility: Works with Claude Code and OpenAI Codex. Language-agnostic with specific guidance for Python, TypeScript, Java, Go, Rust.
metadata:
  category: code-quality
  tags: clean-code, SOLID, DRY, best-practices, design-patterns
  version: "1.0.0"
---

# Coding Standards & Design Principles Guide

## Overview

This skill ensures you write high-quality, maintainable code that follows industry best practices. Use this whenever you're writing code, reviewing code, or refactoring existing implementations. The principles here apply across all programming languages, with specific considerations for different contexts.

**Core Philosophy:**

- **Clarity over cleverness** - Code is read more often than written
- **Practical pragmatism** - Apply patterns when they add value, not dogmatically
- **Evolution-friendly** - Design for change and future extension
- **Team-oriented** - Write code others (including future you) can understand

---

# Process

## 🚀 High-Level Workflow

Writing quality code involves three main phases:

### Phase 1: Planning and Design

#### 1.1 Understand Core Design Principles

Before writing code, internalize these fundamental principles:

**DRY (Don't Repeat Yourself):**

- Extract duplicated logic when the same code appears **3+ times**
- Create reusable functions/methods/classes for shared behavior
- **BUT**: Don't abstract prematurely - two instances might just be coincidence
- **Balance**: Readability > DRY for simple, self-explanatory code
- **Example**: If you see identical validation logic in 3 endpoints, extract it

**SOLID Principles:**

**S - Single Responsibility Principle (SRP):**

- Each class/function should do one thing and do it well
- If you can't describe what it does in one sentence without "and", it's doing too much
- **Red flag**: Functions with names like `processAndValidateAndSaveUser()`
- **Good**: Separate `validateUser()`, `processUser()`, `saveUser()`

**O - Open/Closed Principle:**

- Open for extension, closed for modification
- Use interfaces, abstract classes, or composition to allow new behavior without changing existing code
- **Example**: Plugin architecture instead of giant switch statements

**L - Liskov Substitution Principle:**

- Subclasses should be substitutable for their base classes
- Don't break contracts - if parent returns non-null, child shouldn't return null
- **Red flag**: Subclass that throws NotImplementedException for parent methods

**I - Interface Segregation Principle:**

- Many specific interfaces are better than one general-purpose interface
- Clients shouldn't depend on methods they don't use
- **Example**: `IReadable` and `IWritable` instead of `IFileOperations` with unused methods

**D - Dependency Inversion Principle:**

- Depend on abstractions, not concrete implementations
- High-level modules shouldn't depend on low-level modules
- **Use**: Dependency injection, interface-based design

**Composition Over Inheritance:**

- Favor "has-a" relationships over "is-a"
- Inheritance creates tight coupling; composition provides flexibility
- **Example**: Use strategy pattern instead of inheritance hierarchies
- **Guideline**: More than 2-3 inheritance levels is usually a smell

**YAGNI (You Aren't Gonna Need It):**

- Don't build features "just in case" or "for the future"
- Add complexity only when actually needed
- **Balance**: Don't over-engineer, but leave sensible extension points

**KISS (Keep It Simple, Stupid):**

- Simple solutions are easier to understand, test, and maintain
- If a junior developer can't understand it, it's probably too complex
- **Question**: "Is there a simpler way to achieve the same goal?"

#### 1.2 Plan Your Approach

Before writing code, ask yourself:

**Functionality:**

- What is the single responsibility of this code?
- What are the inputs, outputs, and side effects?
- What are the error cases and how should they be handled?

**Reusability:**

- Is there existing code that does something similar?
- Will this logic be needed elsewhere?
- What's the right level of abstraction?

**Dependencies:**

- What external dependencies does this need?
- Can dependencies be injected rather than hard-coded?
- Are we depending on abstractions or concrete implementations?

**Testing:**

- How will this be tested?
- Are we writing testable code (pure functions, dependency injection)?
- What are the edge cases?

#### 1.3 Design the Interface First

**Before implementation, design the public interface:**

- What will consumers of this code need?
- What parameters are required vs optional?
- What does success look like? What about failure?
- How will this be documented?

**Consider:**

- Function/method signatures
- Class constructors and public methods
- Return types and error handling strategy
- Naming conventions

---

### Phase 2: Implementation

#### 2.1 Code Organization

**File Structure:**

- One class per file (for OOP languages)
- Group related functionality in modules/packages
- Keep files under 300-500 lines (guideline, not rule)
- Organize imports: stdlib → third-party → local

**Function/Method Length:**

- Aim for 20-30 lines max per function
- If longer, can you extract helper functions?
- **Exception**: Sometimes a long, linear function is clearer than over-decomposition

**Class Length:**

- Aim for under 200-300 lines per class
- If larger, consider if it has multiple responsibilities
- Extract inner classes or create new classes

#### 2.2 Naming Conventions

**Critical Rules:**

- Names should reveal intent: `getUserById()` not `get()`
- Avoid abbreviations unless universally known: `HTTP` is fine, `usrLst` is not
- Be consistent within the codebase
- Use domain language that business stakeholders understand

**Specific Guidelines:**

**Variables:**

- Use nouns: `userCount`, `activeConnections`, `databasePool`
- Boolean: Prefix with `is`, `has`, `can`: `isValid`, `hasAccess`, `canDelete`
- Avoid single letters except for: `i, j, k` (loop indices), `x, y` (coordinates), `e` (exceptions)

**Functions/Methods:**

- Use verbs: `calculateTotal()`, `fetchUser()`, `validateEmail()`
- Predicates return boolean: `isEmpty()`, `hasPermission()`
- Commands vs Queries: Separate functions that change state from those that return data

**Classes:**

- Use nouns: `UserRepository`, `EmailValidator`, `PaymentProcessor`
- Avoid "Manager", "Helper", "Utility" names - they hide responsibility
- If you need them, be specific: `DatabaseConnectionManager` not `Manager`

**Constants:**

- All caps with underscores: `MAX_RETRY_ATTEMPTS`, `DEFAULT_TIMEOUT`
- Group related constants in enums or dedicated modules

#### 2.3 Function Design

**Parameters:**

- Ideal: 0-2 parameters
- Acceptable: 3 parameters
- Avoid: 4+ parameters (use parameter objects/configs)
- **Example**: Instead of `createUser(name, email, age, country, preferences, settings)`, use `createUser(UserCreateRequest request)`

**Return Values:**

- Be consistent: Don't mix null, undefined, empty arrays, and exceptions for "no data"
- Prefer explicit error handling over null: Result types, Option types, or exceptions
- Return early to avoid deep nesting

**Side Effects:**

- Document all side effects in function documentation
- Separate query operations (read) from command operations (write)
- Minimize hidden side effects (global state, file I/O, etc.)

**Pure Functions When Possible:**

- Same inputs always produce same outputs
- No side effects
- Easier to test, reason about, and parallelize
- **Example**: `calculateTax(amount, rate)` is pure; `updateUserInDatabase(user)` is not

#### 2.4 Error Handling

**General Principles:**

- Fail fast: Validate inputs early
- Provide actionable error messages
- Don't swallow exceptions silently
- Use specific exception types

**Error Handling Strategies:**

**Exceptions (for exceptional situations):**

- Use for truly exceptional conditions, not control flow
- Provide context: What failed, why, and what to do about it
- Clean up resources (use try-finally or context managers)

**Return Values (for expected failures):**

- Use Result/Option types for operations that commonly fail
- Example: `findUser()` returns `Option<User>` or `Result<User, NotFoundError>`
- Avoid null/undefined when possible

**Validation:**

- Validate at system boundaries (API endpoints, database queries)
- Use type systems and schema validation
- Return structured validation errors

**Logging:**

- Log actionable information
- Include context: user ID, request ID, timestamp
- Use appropriate levels: ERROR for failures, WARN for degraded state, INFO for significant events

#### 2.5 Comments and Documentation

**When to Comment:**

- **WHY, not WHAT**: Explain the reasoning, not the obvious
  - ❌ `// Increment counter by 1`
  - ✅ `// Skip first item as it contains headers`
- Complex algorithms: Explain the approach
- Non-obvious business rules
- TODO/FIXME with context and owner

**When NOT to Comment:**

- Self-explanatory code (use better names instead)
- Commented-out code (use version control)
- Obvious statements

**Documentation (Doc Comments):**

- Public APIs: Always document
- Complex internal functions: Document
- Simple, self-explanatory functions: Optional

**Include:**

- Purpose and behavior
- Parameter descriptions with types and constraints
- Return value description
- Exceptions/errors that can be thrown
- Usage examples for complex APIs

#### 2.6 Code Quality Practices

**Avoid Deep Nesting:**

- Maximum 3 levels of indentation
- Use early returns/guards
- Extract complex conditions into well-named functions

**Example:**

```typescript
// ❌ BAD:
if (user !== null) {
  if (user.isActive) {
    if (user.hasPermission("write")) {
      // do something
    }
  }
}

// ✅ GOOD:
if (user === null) return;
if (!user.isActive) return;
if (!user.hasPermission("write")) return;
// do something
```

**Avoid Long Parameter Lists:**

- Use parameter objects/configs for 4+ parameters
- Consider builder pattern for objects with many optional parameters

**Avoid Magic Numbers:**

- Define constants with descriptive names
- ❌ `if (status === 404)`
- ✅ `if (status === HTTP_NOT_FOUND)`

**Consistent Formatting:**

- Use automated formatters (Prettier, Black, gofmt)
- Follow language-specific style guides
- Be consistent within the project

**Minimize Global State:**

- Prefer dependency injection over global singletons
- Use function parameters instead of accessing global variables
- Make mutability explicit and minimal

---

### Phase 3: Review and Refine

#### 3.1 Self-Review Checklist

Before considering code complete, verify:

**Design Principles:**

- [ ] Each function/class has a single, clear responsibility
- [ ] No code duplication (DRY applied where it adds value)
- [ ] Dependencies are injected, not hard-coded
- [ ] Code is open for extension, closed for modification
- [ ] Abstractions don't leak implementation details

**Code Quality:**

- [ ] Names clearly express intent
- [ ] Functions are short and focused (< 30 lines typically)
- [ ] No deep nesting (< 3 levels)
- [ ] No magic numbers or strings
- [ ] Consistent formatting and style

**Error Handling:**

- [ ] Input validation at boundaries
- [ ] Meaningful error messages
- [ ] Resources properly cleaned up
- [ ] No swallowed exceptions

**Testing:**

- [ ] Code is testable (minimal dependencies, pure functions where possible)
- [ ] Edge cases identified
- [ ] Test coverage for critical paths

**Documentation:**

- [ ] Public APIs documented
- [ ] Complex logic has explanatory comments
- [ ] Non-obvious decisions explained

**Performance:**

- [ ] No obvious inefficiencies (N+1 queries, unnecessary loops)
- [ ] Appropriate data structures chosen
- [ ] No premature optimization

**Security:**

- [ ] Input sanitized/validated
- [ ] Sensitive data not logged
- [ ] Authentication/authorization checked

#### 3.2 Refactoring Opportunities

**Code Smells to Watch For:**

**Long Functions/Methods:**

- Extract smaller, well-named functions
- Each function should do one thing

**Large Classes:**

- Consider if class has multiple responsibilities
- Extract collaborating classes

**Long Parameter Lists:**

- Use parameter objects or builder pattern
- Consider if function is doing too much

**Primitive Obsession:**

- Create domain objects instead of passing primitives
- Example: `Email` class instead of raw strings

**Feature Envy:**

- Method uses another class's data more than its own
- Move method to the class whose data it uses

**Data Clumps:**

- Same group of parameters appears together repeatedly
- Extract into a dedicated object

**Switch Statements:**

- Consider polymorphism or strategy pattern
- Especially if same switch appears in multiple places

**Comments:**

- If you need a comment to explain what code does, consider better naming
- If explaining why, the comment is valuable

---

**For language-specific best practices and examples, see [references/LANGUAGE-SPECIFICS.md](references/LANGUAGE-SPECIFICS.md).**

**For detailed code examples demonstrating these principles, see [references/EXAMPLES.md](references/EXAMPLES.md).**

---

# Quick Reference

## When to Apply Each Principle

**Use DRY when:**

- Same logic appears 3+ times
- The abstraction is clear and natural
- Changes to the logic should affect all uses

**Don't use DRY when:**

- Two similar pieces of code serve different purposes
- The abstraction would be more complex than duplication
- Code is unlikely to change together

**Use SRP when:**

- Class/function is hard to name without "and"
- Changes for one reason affect unrelated functionality
- Testing requires mocking many dependencies

**Use Dependency Injection when:**

- Testing with mock dependencies
- Supporting multiple implementations
- Configuration needs to vary by environment

**Use Composition when:**

- Multiple inheritance creates diamond problem
- Behavior needs to be mixed and matched
- Inheritance depth exceeds 2-3 levels

**Keep It Simple when:**

- Always - start simple, add complexity only when needed
- You're tempted to use advanced patterns
- Junior developers will maintain the code

## Common Anti-Patterns to Avoid

- **God Objects**: Classes that do everything
- **Shotgun Surgery**: One change requires editing many files
- **Spaghetti Code**: No clear structure, everything connected
- **Copy-Paste Programming**: Duplicating code instead of abstracting
- **Golden Hammer**: Using favorite pattern everywhere
- **Premature Optimization**: Optimizing before measuring
- **Not Invented Here**: Reimplementing existing solutions
- **Analysis Paralysis**: Over-planning without implementing

---

# Final Notes

**Remember:**

- These are guidelines, not laws - apply them with judgment
- Consistency within a codebase matters more than perfect adherence
- Write code for humans first, machines second
- When in doubt, favor simplicity and clarity
- Refactor continuously - don't let technical debt accumulate

**The Goal:**
Write code that is:

- Easy to understand
- Easy to change
- Easy to test
- Easy to debug
- Easy to extend

If your code achieves these goals, you're on the right track.
