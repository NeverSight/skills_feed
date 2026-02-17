---
name: juniors-best-practice
description: Juniors-focused React and TypeScript best practices. Use this skill when writing or reviewing code to enforce clear, consistent, and maintainable patterns across common scopes like React, TypeScript, styling, devtools, assets, and Git.
license: MIT
metadata:
  author: siberiacancode
  version: "1.0.0"
---

# Juniors Best Practice

Juniors-focused best practices for React and TypeScript projects. The rules are short, practical, and organized by scope to guide consistent code reviews, refactoring, and new feature work.

## When to Apply

Reference these guidelines when:
- Writing or reviewing React/TypeScript code for clarity and consistency
- Teaching junior developers or establishing baseline team conventions
- Refactoring code to align with simple, maintainable patterns
- Standardizing project-wide practices (imports, tooling, naming, commits)

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Beginner Foundations | HIGH | `beginner-` |
| 2 | TypeScript | MEDIUM | `typescript-` |
| 3 | React | MEDIUM | `react-` |
| 4 | Styling | MEDIUM | `styling-` |
| 5 | Devtools | MEDIUM | `devtools-` |
| 6 | Assets | LOW-MEDIUM | `assets-` |
| 7 | Git | LOW | `git-` |

## Quick Reference

### 1. Beginner Foundations (HIGH)
- `beginner-early-return` - Prefer early returns to reduce nesting
- `beginner-double-negation` - Avoid `!isNotX` patterns
- `beginner-unnecessary-destructuring` - Keep objects intact for clarity
- `beginner-const-vs-let` - Default to const
- `beginner-nullish-vs-or` - Use ?? for defaults
- `beginner-useless-return-arrow` - Remove redundant return
- `beginner-uppercase-constants` - Use UPPER_CASE only for stable constants

### 2. TypeScript (MEDIUM)
- `typescript-alias-naming` - Use safe path alias prefixes

### 3. React (MEDIUM)
- `react-string-props` - Use string literals when possible
- `react-children-prop` - Use children for composition
- `react-extends-component` - Extend native element props
- `react-props-typing` - Keep props typing readable

### 4. Styling (MEDIUM)
- `styling-classnames-function` - Use clsx for conditional classes
- `styling-css-states` - Prefer CSS selectors for component states

### 5. Devtools (MEDIUM)
- `devtools-formatter-linter` - Use formatter and linter
- `devtools-sorting-imports` - Keep imports ordered and grouped
- `devtools-package-manager-lock` - Use a single package manager

### 6. Assets (LOW-MEDIUM)
- `assets-svg-files` - Use SVGs as components

### 7. Git (LOW)
- `git-commit-convention` - Use consistent commit conventions

## How to Use

Read individual rule files for detailed explanations and examples:

```
rules/beginner-early-return.md
rules/react-props-typing.md
```

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
