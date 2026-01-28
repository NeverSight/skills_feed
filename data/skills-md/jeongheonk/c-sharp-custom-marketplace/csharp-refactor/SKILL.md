---
name: csharp-refactor
description: C# code refactoring skill. Applies SOLID principles, extracts methods/classes, introduces design patterns, and modernizes syntax. Use when improving code maintainability, addressing code smells, or modernizing legacy C# code.
user-invocable: true
argument-hint: "[file_path] [refactor_type]"
context: fork
model: sonnet
allowed-tools:
  - Read
  - Glob
  - Grep
  - Edit
  - Write
---

# C# Refactoring Skill

Systematically refactors C# code to improve maintainability, readability, and adherence to best practices.

## Arguments

- `$ARGUMENTS[0]`: Target file path (optional, will scan for .cs files if not provided)
- `$ARGUMENTS[1]`: Refactor type (optional): `solid`, `pattern`, `modern`, `extract`, `all`

## Execution Steps

### Step 1: Identify Target

If no file specified (`$ARGUMENTS[0]` is empty):
- Scan for recently modified `.cs` files
- Ask user to select target file(s)

### Step 2: Analyze Code

Read and analyze the target code for refactoring opportunities.

### Step 3: Apply Refactoring

Based on `$ARGUMENTS[1]` or analyze all categories:

## Refactoring Categories

### SOLID Refactoring (`solid`)

| Violation | Refactoring |
|-----------|-------------|
| **SRP** | Extract class, Split responsibilities |
| **OCP** | Introduce Strategy/Template Method pattern |
| **LSP** | Fix inheritance hierarchy, Use composition |
| **ISP** | Split interface into smaller ones |
| **DIP** | Extract interface, Inject dependencies |

### Pattern Introduction (`pattern`)

| Code Smell | Suggested Pattern |
|------------|-------------------|
| Complex object creation | Builder, Factory Method |
| Multiple conditionals on type | Strategy, State |
| Global state access | Singleton (cautiously), DI |
| Complex subsystem | Facade |
| Tree/composite structures | Composite |
| Adding features dynamically | Decorator |
| Request handling chain | Chain of Responsibility |

### Modern C# Syntax (`modern`)

| Old Syntax | Modern Alternative |
|------------|-------------------|
| Constructor + field assignment | Primary constructor |
| `new List<T> { ... }` | Collection expressions `[...]` |
| Multiple null checks | Pattern matching, `?.`, `??` |
| Verbose switch statements | Switch expressions |
| Manual INPC implementation | `[ObservableProperty]` (CommunityToolkit.Mvvm) |
| Mutable properties (non-MVVM) | `required`, `init` for immutability |
| Class for simple data | Record types |
| Traditional foreach | LINQ where appropriate |

### Extract Refactoring (`extract`)

- **Extract Method**: Long methods → smaller, focused methods
- **Extract Class**: Large class → multiple cohesive classes
- **Extract Interface**: Concrete dependencies → interface abstraction
- **Extract Base Class**: Duplicate code → shared base
- **Extract Parameter Object**: Many parameters → single object

## Output Format

```markdown
# Refactoring Results

## Target
- File: {file_path}
- Refactor Type: {type}

## Changes Applied

### {Refactoring Name}
- Location: `file.cs:line`
- Before:
```csharp
// old code
```
- After:
```csharp
// refactored code
```
- Benefit: {explanation}

## Summary
- Total refactorings: {N}
- Lines changed: {N}
- New files created: {list if any}

## Recommendations
- Further improvements that could be made
- Related patterns to consider
```

## Guidelines

- Preserve existing functionality (no behavior changes)
- Make incremental changes, not massive rewrites
- Prioritize readability over cleverness
- Consider team familiarity with patterns
- Add comments only where logic is non-obvious
- Run tests after each refactoring if available
