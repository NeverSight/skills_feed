---
name: slop
description: Removes AI-generated code slop from git diffs to maintain code quality
license: MIT
compatibility: claude, opencode, amp, codex, gemini
hint: Use when cleaning up AI-generated code slop in git diffs
user-invocable: true
metadata:
  audience: all
  workflow: code-quality
---

# Remove AI Code Slop

Check the diff against a branch and remove all AI-generated slop introduced in this branch. Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality.

## Usage

`/slop [branch-name]`

- If no branch is provided, compare against main: `/slop main`

## What is AI Code Slop?

This includes:
- Extra comments that a human wouldn't add or is inconsistent with the rest of the file
- Extra defensive checks or try/catch blocks that are abnormal for that area of the codebase
- Casts to `any` to get around type issues
- Any other style that is inconsistent with the file

## Core Principles

### 1. Preserve Functionality
Never change what the code does - only how it does it. All original features, outputs, and behaviors must remain intact.

### 2. Apply Project Standards
Follow the established coding standards from the project's CLAUDE.md or conventions:
- Use proper import sorting and file organization
- Follow language-specific patterns (ES modules, proper TypeScript types, etc.)
- Maintain consistent naming conventions
- Use proper error handling patterns

### 3. Enhance Clarity
Simplify code structure by:
- Reducing unnecessary complexity and nesting
- Eliminating redundant code and abstractions
- Improving readability through clear variable and function names
- Consolidating related logic
- Removing unnecessary comments that describe obvious code
- **IMPORTANT**: Avoid nested ternary operators - prefer switch statements or if/else chains
- Choose clarity over brevity - explicit code is often better than overly compact code

### 4. Maintain Balance
Avoid over-simplification that could:
- Reduce code clarity or maintainability
- Create overly clever solutions that are hard to understand
- Combine too many concerns into single functions
- Remove helpful abstractions that improve code organization
- Prioritize "fewer lines" over readability

## Process

### 1. Get the diff

```bash
# Compare against main branch
git diff main...HEAD --stat

# Or against specific branch
git diff $1 --stat
```

### 2. Review each changed file

For each changed file:
- Read the current content
- Compare with original (before changes)
- Identify AI-generated slop patterns
- Check for opportunities to improve elegance and consistency

### 3. Remove slop and refine

- Remove unnecessary comments
- Simplify overly defensive code
- Remove `any` casts where possible
- Restore natural code style
- Apply project-specific best practices
- Ensure all functionality remains unchanged

### 4. Verify

```bash
# Show remaining changes
git diff --stat

# Check tests still pass
npm test
```

## Common Slop Patterns

1. **Over-commenting**: Comments explaining obvious code
2. **Verbose error handling**: Try/catch blocks where not needed
3. **Unnecessary type casts**: `x as any` to bypass TypeScript
4. **Defensive programming**: Checks for already-validated inputs
5. **Redundant validation**: Duplicate null/undefined checks
6. **Nested ternaries**: Complex nested ternary operators
7. **Overly compact code**: Dense one-liners that sacrifice readability

## Refinement Guidelines

When refining code:

1. **Identify the modified sections** - Only refine code that changed in the diff
2. **Analyze for improvement opportunities** - Look for ways to enhance elegance and consistency
3. **Apply project standards** - Follow established conventions and patterns
4. **Preserve functionality** - Ensure behavior remains unchanged
5. **Verify improvements** - The refined code should be simpler and more maintainable
6. **Document significant changes** - Only document changes that affect understanding

### Code Style Preferences

- Prefer explicit over compact - readable code beats clever code
- Use descriptive names - clarity over brevity
- Avoid deep nesting - flatten structure when possible
- Remove redundant code - eliminate duplicates
- Use language-appropriate patterns - follow idiomatic practices
