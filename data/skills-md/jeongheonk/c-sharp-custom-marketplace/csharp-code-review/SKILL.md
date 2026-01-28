---
name: csharp-code-review
description: C# code review skill. Analyzes code quality from OOP, SOLID, GoF design pattern, modern C# features, and performance perspectives. Use before pull requests, when optimizing code, or auditing legacy codebases.
user-invocable: true
argument-hint: "[file_path]"
context: fork
model: sonnet
allowed-tools:
  - Read
  - Glob
  - Grep
---

# C# Code Review Skill

Systematically reviews C# code from OOP principles, SOLID principles, GoF design patterns, modern C# features, and performance perspectives.

## Arguments

- `$ARGUMENTS[0]`: Target file or directory path (optional, will scan for recently modified .cs files if not provided)

## Execution Steps

### Step 1: Identify Review Target
If the user hasn't specified a file:
- Check recently modified `.cs` files
- Or ask the user to specify files/directories to review

### Step 2: Code Analysis
Read the target code and analyze from the following perspectives.

## Review Checklist

### OOP Four Pillars
| Principle | Review Items |
|-----------|--------------|
| **Encapsulation** | Private fields, property access, hidden implementation details |
| **Inheritance** | Proper inheritance hierarchy, composition over inheritance |
| **Polymorphism** | Interface/abstract class usage, virtual method appropriateness |
| **Abstraction** | Appropriate abstraction level, unnecessary detail exposure |

### SOLID Principles
| Principle | Review Items | Violation Signs |
|-----------|--------------|-----------------|
| **SRP** | Does the class have single responsibility? | Class changes for multiple reasons, too many methods |
| **OCP** | Open for extension, closed for modification? | Existing code requires modification for new features, switch/if-else chains |
| **LSP** | Can subtypes substitute base types? | Exceptions in subclasses, empty method overrides |
| **ISP** | Are interfaces segregated per client? | NotImplementedException in implementations, unused methods |
| **DIP** | Depending on abstractions? | Direct instantiation with new, concrete class type dependencies |

### GoF Design Pattern Opportunities
Identify areas in the code where these patterns could be applied:

**Creational Patterns**
- Complex object creation → Builder
- Separate object creation logic → Factory Method / Abstract Factory
- Global single instance → Singleton (caution: avoid overuse)

**Structural Patterns**
- Incompatible interface connection → Adapter
- Dynamic feature addition → Decorator
- Simplify complex subsystems → Facade
- Object tree structures → Composite

**Behavioral Patterns**
- Interchangeable algorithms → Strategy
- State-dependent behavior changes → State
- Object communication → Observer / Mediator
- Request processing chain → Chain of Responsibility
- Undo/Redo → Command + Memento

### Modern C# Features (C# 12/13)
| Feature | When to Recommend |
|---------|-------------------|
| **Primary constructors** | Classes with simple initialization |
| **Collection expressions** | Array/List initialization `[1, 2, 3]` |
| **required properties** | Required initialization without constructor |
| **init-only setters** | Immutable objects |
| **record types** | Value-based equality, DTOs |
| **Pattern matching** | Complex conditionals, type checking |
| **File-scoped namespaces** | Reduce indentation |
| **Raw string literals** | Multiline strings, JSON, SQL |

### Performance Review
| Category | Review Items |
|----------|--------------|
| **Memory Allocation** | Unnecessary allocations in hot paths, Large Object Heap (>= 85KB) |
| **Async/Await** | Blocking calls (.Result, .Wait()), missing ConfigureAwait |
| **Collections** | Wrong collection type, multiple LINQ enumerations |
| **Strings** | String concatenation in loops, missing StringBuilder |
| **Boxing** | Unnecessary value type boxing |
| **Span/Memory** | Buffer operations without Span<T>, Memory<T> |

### Async Code Review
- [ ] No `.Result` or `.Wait()` calls (deadlock risk)
- [ ] `ConfigureAwait(false)` in library code
- [ ] Proper cancellation token propagation
- [ ] `ValueTask` for hot paths with cached results
- [ ] `IAsyncEnumerable` for streaming data
- [ ] No async void except event handlers

### Code Quality Review
- [ ] Naming conventions (PascalCase, camelCase, _privateField, Async suffix)
- [ ] Null safety (nullable reference types, `?.`, `??`, `??=`)
- [ ] Exception handling (specific exceptions, `when` filters, proper logging)
- [ ] IDisposable pattern compliance (using statements, Dispose implementation)
- [ ] Collection usage (appropriate type selection, efficient LINQ)
- [ ] Magic numbers/strings should be constants
- [ ] Duplicate code elimination
- [ ] Proper use of `sealed` for non-inheritable classes

### Security Review
- [ ] Input validation (SQL injection, XSS, path traversal)
- [ ] Sensitive data handling (no hardcoded secrets, proper encryption)
- [ ] Authentication/Authorization checks
- [ ] Secure randomness (avoid `Random` for security)
- [ ] XML external entity (XXE) prevention

## Step 3: Output Review Results

### Output Format

```markdown
# Code Review Results

## Summary
- File: {file path}
- Overall Assessment: {Excellent/Good/Needs Improvement/Critical}
- Major Issues: {N} items
- .NET Version Compliance: {.NET 8/9 features utilization}

## SOLID Principles Analysis

### SRP Violation (Severity: High/Medium/Low)
- Location: `ClassName.cs:line`
- Problem: {description}
- Suggestion: {improvement with code example}

### OCP Violation
...

## Modern C# Opportunities

### {Feature Name} Recommendation
- Location: `file.cs:line`
- Current: {old syntax}
- Improved: {modern C# syntax}
- Benefit: {explanation}

## Performance Issues

### {Issue Title} (Severity: High/Medium/Low)
- Location: `file.cs:line`
- Problem: {description with impact}
- Current: {problematic code}
- Improved: {optimized code}
- Impact: {expected improvement}

## Async Code Issues

### {Issue Title}
- Location: `file.cs:line`
- Problem: {description}
- Risk: {deadlock/performance/etc}
- Solution: {code fix}

## Applicable Design Patterns

### {Pattern Name} Pattern Recommended
- Current code: {problem}
- Benefits of applying: {description}
- Example code: {brief example}

## Security Concerns

### {Issue Title} (Severity: Critical/High/Medium/Low)
- Location: `file.cs:line`
- Vulnerability: {description}
- Remediation: {fix with code}

## Code Quality Issues

### {Issue Title}
- Location: `file.cs:line`
- Current: {code}
- Improved: {code}

## Positive Aspects
- {mention well-written parts}
- {good patterns already in use}

## Prioritized Improvements
1. [Critical] {security issues}
2. [High] {SOLID violations, performance issues}
3. [Medium] {code quality, modern features}
4. [Low] {style improvements}
```

## Guidelines
- Don't just criticize; mention positive aspects too.
- Provide improvements with concrete code examples.
- Don't recommend over-engineering.
- Make practical suggestions considering context.
- Prioritize security issues first.
- Consider the target .NET version when suggesting features.
- Balance between modern features and team familiarity.
