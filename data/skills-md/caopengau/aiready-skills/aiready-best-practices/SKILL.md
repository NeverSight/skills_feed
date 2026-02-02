---
name: aiready-best-practices
description: Guidelines for writing AI-friendly code. Detects semantic duplicates, context fragmentation, naming inconsistencies. Use when writing new code, reviewing PRs, refactoring for AI adoption, or debugging AI assistant confusion. Helps minimize context waste and improve AI comprehension.
license: MIT
metadata:
  author: aiready
  version: "0.1.0"
---

# AIReady Best Practices

Guidelines for writing code that AI coding assistants can understand and maintain effectively. Based on analysis of thousands of repositories and common AI model failure patterns.

## When to Apply

Reference these guidelines when:

- **Writing new features** - Apply patterns from the start
- **Reviewing pull requests** - Check for AI-unfriendly patterns
- **Refactoring code** - Improve AI comprehension
- **Debugging AI confusion** - Fix when assistants give wrong suggestions
- **Preparing for AI adoption** - Modernize codebase structure

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Pattern Detection | CRITICAL | `patterns-` |
| 2 | Context Optimization | HIGH | `context-` |
| 3 | Consistency Checking | MEDIUM | `consistency-` |
| 4 | Documentation | MEDIUM | `docs-` |
| 5 | Dependencies | LOW | `deps-` |

## Quick Reference

### 1. Pattern Detection (CRITICAL)

- `patterns-semantic-duplicates` - Consolidate duplicate implementations
- `patterns-consistent-naming` - Use consistent names for similar concepts
- `patterns-interface-fragmentation` - Unify similar interfaces

### 2. Context Optimization (HIGH)

- `context-import-depth` - Keep import chains shallow (max 3 levels)
- `context-cohesion` - Group related functionality together
- `context-file-size` - Split oversized files

### 3. Consistency Checking (MEDIUM)

- `consistency-naming-conventions` - Follow project-wide naming patterns
- `consistency-error-handling` - Use consistent error patterns
- `consistency-api-design` - Maintain consistent API shapes

### 4. Documentation (MEDIUM)

- `docs-code-sync` - Keep docs in sync with code changes
- `docs-ai-context` - Document non-obvious AI context needs

### 5. Dependencies (LOW)

- `deps-circular` - Avoid circular dependencies
- `deps-freshness` - Keep dependencies up to date

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/patterns-semantic-duplicates.md
rules/context-import-depth.md
rules/consistency-naming-conventions.md
```

Each rule file contains:

- Brief explanation of why it matters for AI
- Incorrect code example with explanation
- Correct code example with explanation
- Impact metrics and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`

## Context Efficiency

This skill is designed for efficient context usage:

- **Lazy loading**: Only relevant rules are loaded when needed
- **Progressive disclosure**: Detailed examples are in separate files
- **Focused rules**: Each rule addresses one specific pattern
- **Measurable impact**: Clear metrics for each improvement

## Related Tools

These guidelines complement the AIReady CLI tools:

- **@aiready/pattern-detect** - Automated semantic duplicate detection
- **@aiready/context-analyzer** - Context window cost analysis
- **@aiready/consistency** - Naming convention checking
- **@aiready/cli** - Unified analysis tool

Learn more: [https://getaiready.dev](https://getaiready.dev)
