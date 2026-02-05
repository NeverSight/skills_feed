---
name: code-optimizer
description: Analyze code for performance issues and suggest optimizations. Use when users ask to "optimize this code", "find performance issues", "improve performance", "check for memory leaks", "review code efficiency", or want to identify bottlenecks, algorithmic improvements, caching opportunities, or concurrency problems.
---

# Code Optimization

Analyze code for performance issues following this priority order:

## Analysis Priorities

1. **Performance bottlenecks** - O(n²) operations, inefficient loops, unnecessary iterations
2. **Memory leaks** - unreleased resources, circular references, growing collections
3. **Algorithm improvements** - better algorithms or data structures for the use case
4. **Caching opportunities** - repeated computations, redundant I/O, memoization candidates
5. **Concurrency issues** - race conditions, deadlocks, thread safety problems

## Workflow

1. Read the target code file(s)
2. Identify language and framework context
3. Analyze for each priority category
4. Report findings with severity and fixes

## Response Format

For each issue found:

```
### [Severity] Issue Title
**Location**: file:line_number
**Category**: Performance | Memory | Algorithm | Caching | Concurrency

**Problem**: Brief explanation of the issue

**Impact**: Why this matters (performance cost, resource usage, etc.)

**Fix**:
[Code example showing the optimized version]
```

## Severity Levels

- **Critical**: Causes crashes, severe memory leaks, or O(n³)+ complexity
- **High**: Significant performance impact (O(n²), blocking operations, resource exhaustion)
- **Medium**: Noticeable impact under load (redundant operations, suboptimal algorithms)
- **Low**: Minor improvements (micro-optimizations, style improvements with perf benefit)

## Language-Specific Checks

### JavaScript/TypeScript
- Array methods inside loops (map/filter/find in forEach)
- Missing async/await causing blocking
- Event listener leaks
- Unbounded arrays/objects

### Python
- List comprehensions vs generator expressions for large data
- Global interpreter lock considerations
- Context manager usage for resources
- N+1 query patterns

### General
- Premature optimization warnings (only flag if genuinely impactful)
- Database query patterns (N+1, missing indexes)
- I/O in hot paths
