---
name: deslop
description: Remove AI-generated code slop from the current branch by analyzing diffs against main and cleaning up unnecessary comments, defensive code, and style inconsistencies.
license: Complete terms in LICENSE.txt
---

This skill identifies and removes AI-generated code slop from changes in the current branch.

## Process

### 1. Get the Diff

Run `git diff main...HEAD` to see all changes introduced in this branch.

### 2. Analyze Each Changed File

For each file with changes, look for these patterns of AI slop:

#### Unnecessary Comments
- Comments explaining obvious code that a human wouldn't add
- Comments inconsistent with the rest of the file's commenting style
- JSDoc or docstrings added to simple internal functions that don't have them elsewhere
- "// TODO" or "// NOTE" comments that aren't actionable

#### Defensive Over-Engineering
- Try/catch blocks in internal code paths that are already validated upstream
- Null/undefined checks on values that are guaranteed to exist by the type system or calling context
- Fallback values that can never be reached
- Type guards on already-typed parameters

#### Type Workarounds
- Casts to `any` to bypass type errors
- `@ts-ignore` or `@ts-expect-error` comments
- Overly broad union types to satisfy the compiler

#### Style Inconsistencies
- Different naming conventions than the rest of the file
- Different formatting patterns (even if valid)
- Excessive blank lines or grouping that doesn't match file style
- Console.log statements left in production code

### 3. Clean Up

For each identified issue:
1. Read the surrounding context to understand the file's existing style
2. Remove or simplify the slop while preserving actual functionality
3. Ensure the code still works correctly

### 4. Report

After all changes, provide a **1-3 sentence summary** of what was changed. Do not enumerate every change—just summarize the types of slop removed and roughly how much.

Example output:
> Removed 12 unnecessary comments explaining obvious code and 3 redundant try/catch blocks in API handlers. Also cleaned up 2 `any` casts that were hiding actual type issues.
