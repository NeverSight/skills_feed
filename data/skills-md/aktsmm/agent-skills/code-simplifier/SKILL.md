---
name: code-simplifier
description: Guide for simplifying and refining code after coding sessions. Use when cleaning up complex code, reviewing PRs for readability, or applying consistent refactoring patterns.
metadata:
  author: yamapan (https://github.com/aktsmm)
---

# Code Simplifier

A guide for simplifying and refining code while preserving functionality.

## When to Use

- After completing a coding task or writing a logical chunk of code
- Cleaning up complex PRs before review
- Refactoring code for better readability and maintainability
- Applying consistent coding standards across a codebase

## Core Principles

### 1. Preserve Functionality

**Never change what the code does - only how it does it.**

- All original features, outputs, and behaviors must remain intact
- Test before and after to verify no regressions
- If unsure, ask before refactoring

### 2. Apply Project Standards

Follow established coding standards from project configuration (CLAUDE.md, .editorconfig, ESLint, etc.):

- Consistent import sorting and organization
- Preferred function styles (arrow vs function keyword)
- Explicit type annotations where required
- Component patterns and naming conventions

### 3. Enhance Clarity

Simplify code structure by:

- Reducing unnecessary complexity and nesting
- Eliminating redundant code and abstractions
- Improving readability through clear variable and function names
- Consolidating related logic
- Removing unnecessary comments that describe obvious code

**Critical Rules:**

- ❌ **Avoid nested ternary operators** - prefer switch statements or if/else chains
- ❌ **Avoid overly compact one-liners** - explicit code is often better
- ✅ **Choose clarity over brevity**

### 4. Maintain Balance

Avoid over-simplification that could:

- Reduce code clarity or maintainability
- Create overly clever solutions that are hard to understand
- Combine too many concerns into single functions
- Remove helpful abstractions that improve organization
- Make the code harder to debug or extend

### 5. Focus Scope

Only refine code that has been recently modified or touched, unless explicitly instructed to review a broader scope.

## Refinement Process

```
1. Identify the recently modified code sections
2. Analyze for opportunities to improve elegance and consistency
3. Apply project-specific best practices and coding standards
4. Ensure all functionality remains unchanged
5. Verify the refined code is simpler and more maintainable
6. Document only significant changes that affect understanding
```

## Refactoring Patterns

See [references/refactoring-patterns.md](references/refactoring-patterns.md) for common patterns.

## Quick Checklist

Before submitting refactored code:

- [ ] All tests pass
- [ ] No functionality changed
- [ ] Code follows project standards
- [ ] No nested ternaries introduced
- [ ] Variable names are clear and descriptive
- [ ] No unnecessary abstractions added
- [ ] Comments updated if logic changed
- [ ] Import statements organized

## Example Usage

**Trigger phrases:**

- "Simplify this code"
- "Make this clearer"
- "Refine this implementation"
- "Clean up this function"
- "Review this PR for readability"

**Workflow:**

1. Write code → Complete feature
2. Run tests → Verify functionality
3. Apply code-simplifier → Improve clarity
4. Run tests again → Confirm no regressions
5. Submit PR → Ready for review
