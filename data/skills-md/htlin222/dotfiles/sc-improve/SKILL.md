---
name: sc-improve
description: Apply systematic improvements to code quality, performance, and maintainability. Use when refactoring code, cleaning up technical debt, or optimizing performance.
---

# Code Improvement

Apply systematic improvements to code quality, performance, maintainability, and best practices.

## When to use

- Refactoring existing code for better quality
- Optimizing performance bottlenecks
- Cleaning up technical debt
- Applying consistent coding style
- Improving code maintainability

## Instructions

### Usage

```
/sc:improve [target] [--type quality|performance|maintainability|style] [--safe]
```

### Arguments

- `target` - Files, directories, or project to improve
- `--type` - Improvement type (quality, performance, maintainability, style)
- `--safe` - Apply only safe, low-risk improvements
- `--preview` - Show improvements without applying them

### Execution

1. Analyze code for improvement opportunities
2. Identify specific improvement patterns and techniques
3. Create improvement plan with risk assessment
4. Apply improvements with appropriate validation
5. Verify improvements and report changes

### Claude Code Integration

- Uses Read for comprehensive code analysis
- Leverages MultiEdit for batch improvements
- Applies TodoWrite for improvement tracking
- Maintains safety and validation mechanisms
