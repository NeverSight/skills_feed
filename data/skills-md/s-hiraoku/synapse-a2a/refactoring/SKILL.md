---
name: refactoring
description: >-
  Guide for safe and effective code refactoring. Focuses on improving code 
  structure without changing external behavior. Covers patterns like 
  extraction, inlining, and naming improvements.
---

# Refactoring Guide Skill

Refactoring is the process of restructuring existing computer code—changing the factoring—without changing its external behavior.

## Core Refactoring Patterns

### 1. Composing Methods
- **Extract Method**: If a method is too long or complex, turn a fragment of it into its own method.
- **Inline Method**: If a method body is as clear as its name, move the body into the callers and delete the method.

### 2. Moving Features Between Objects
- **Move Method/Field**: Relocate logic to the class where it most naturally belongs to reduce coupling.

### 3. Simplifying Expressions
- **Decompose Conditional**: Extract complex conditional logic into clearly named methods.
- **Consolidate Conditional Expression**: Merge multiple conditional checks that lead to the same result.

### 4. Clean Code & Naming
- **Rename**: Use clear, intention-revealing names for variables, methods, and classes.
- **Replace Magic Number with Symbolic Constant**: Use named constants instead of literal numbers.

## Safe Refactoring Workflow

1. **Verify Tests**: Ensure you have a solid test suite that passes before starting.
2. **Small Steps**: Make one tiny change at a time.
3. **Run Tests**: Execute the test suite after every small change to catch regressions immediately.
4. **Commit Often**: Commit your changes once a small refactoring step is complete and verified.

## When to Refactor
- **Rule of Three**: Refactor when you find yourself doing something for the third time.
- **Code Smells**: Refactor when you encounter long methods, large classes, or duplicated code.
- **Adding Features**: Refactor before adding new functionality to make the implementation easier.
