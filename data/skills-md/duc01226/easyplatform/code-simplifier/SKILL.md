---
name: code-simplifier
description: Simplifies and refines code for clarity, consistency, and maintainability while preserving all functionality. Focuses on recently modified code unless instructed otherwise.
allowed-tools: Read, Edit, Glob, Grep, Task
infer: true
---

# Code Simplifier Skill

Simplify and refine code for clarity, consistency, and maintainability.

## Usage

```
/code-simplifier                    # Simplify recently modified files
/code-simplifier path/to/file.ts    # Simplify specific file
/code-simplifier --scope=function   # Focus on function-level simplification
```

## What It Does

1. **Analyzes** code for unnecessary complexity
2. **Identifies** opportunities to simplify without changing behavior
3. **Applies** KISS, DRY, and YAGNI principles
4. **Preserves** all existing functionality

## Simplification Targets

- Redundant code paths
- Over-engineered abstractions
- Unnecessary comments (self-documenting code preferred)
- Complex conditionals that can be flattened
- Verbose patterns that have simpler alternatives

## Execution

Use the `code-simplifier:code-simplifier` subagent:

```
Task(subagent_type="code-simplifier:code-simplifier", prompt="Review and simplify [target files]")
```

## Complexity Thresholds

| Metric          | Threshold      | Action                           |
| --------------- | -------------- | -------------------------------- |
| Nesting depth   | > 3 levels     | Flatten with guard clauses       |
| Method length   | > 20 lines     | Extract focused methods          |
| Duplicated code | 2+ occurrences | Apply DRY, use platform patterns |
| Naming clarity  | Unclear intent | Make self-documenting            |

## EasyPlatform Patterns to Apply

### Backend (C#)

- Extract to `Entity.XxxExpr()` static expressions
- Use fluent helpers: `.With()`, `.Then()`, `.PipeIf()`
- Move mapping to DTO `MapToObject()` / `MapToEntity()`
- Use `PlatformValidationResult` fluent API

### Frontend (TypeScript)

- Use `PlatformVmStore` for state management
- Apply `untilDestroyed()` to all subscriptions
- Ensure BEM class naming on all elements
- Use `observerLoadingErrorState()` for loading states

## Simplification Actions

| Action                | Description                                    |
| --------------------- | ---------------------------------------------- |
| Reduce nesting        | Flatten deep if/else chains with guard clauses |
| Extract methods       | Break long methods into focused units          |
| Simplify conditionals | Use early returns, named booleans              |
| Remove duplication    | Apply DRY, use platform patterns               |
| Improve naming        | Make code self-documenting                     |

## Workflow

1. **Identify targets**
   - If no arguments: `git diff --name-only HEAD~1` for recent changes
   - If arguments provided: use specified files/patterns
   - Skip: generated code, migrations, vendor files

2. **Analyze each file**
   - Identify complexity hotspots (nesting > 3, methods > 20 lines)
   - Find duplicated code patterns
   - Check naming clarity

3. **Apply simplifications**
   - One refactoring type at a time
   - Preserve all functionality
   - Follow platform patterns

4. **Verify**
   - Run related tests if available
   - Confirm no behavior changes

## Examples

**Generic Example:**

**Before:**

```typescript
function getData() {
  const result = fetchData();
  if (result !== null && result !== undefined) {
    return result;
  } else {
    return null;
  }
}
```

**After:**

```typescript
function getData() {
  return fetchData() ?? null;
}
```

**Concrete Example Output:**

```
User: /code-simplifier src/Domain/Entities/Employee.cs

Claude:
1. Analyzed Employee.cs (145 lines)
2. Found: 2 nested conditionals, 1 duplicated expression
3. Applied:
   - Extracted IsActiveInCompanyExpr() static expression
   - Replaced nested if with guard clause in Validate()
   - Renamed `x` to `employee` in lambda
4. Tests: All passing
5. Complexity reduced: 145 -> 128 lines
```

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
