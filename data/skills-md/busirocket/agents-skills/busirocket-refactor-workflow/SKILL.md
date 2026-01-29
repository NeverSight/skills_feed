---
name: busirocket-refactor-workflow
description:
  Strict refactoring workflow for TypeScript/React codebases. Use when
  refactoring files with multiple exports, splitting components/hooks/utils,
  moving inline types to types/, and enforcing post-refactor quality gates.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Refactor Workflow

Strict, step-by-step refactoring guidance for maintaining code quality.

## When to Use

Use this skill when:

- Refactoring files with multiple exports (use `@file` workflow)
- Splitting components/hooks/utils into smaller files
- Moving inline types to `types/`
- Enforcing post-refactor quality checks

## Non-Negotiables (MUST)

- After any refactor: run the project's standard checks (e.g. `yarn check:all`)
  as a mandatory quality gate.
- If a file has multiple responsibilities, split immediately.
- If a hook/component contains helpers, extract them.
- If a file declares types inline, move them to `types/`.
- Never use index/barrel files; import from concrete modules only.

## @file Refactor Workflow

When referencing `@file` for a one-shot refactor:

- Exactly one exported symbol per file.
- No inline `interface`/`type` declarations in non-type files.
- No helper functions inside components/hooks.

## Rules

### @file Refactor Workflow

- `refactor-file-workflow` - @file refactor workflow (strict constraints)
- `refactor-mandatory-checks` - Mandatory checks after refactor

### Refactoring TypeScript/React

- `refactor-goals` - Goals for refactoring (many small files, one export per
  file)
- `refactor-decision-rules` - Decision rules for when to split files
- `refactor-never-index-files` - Never use index files
- `refactor-post-refactor-checks` - Post-refactor checks (MANDATORY)

### Post-Refactor Checks

- `refactor-golden-path` - Golden path for post-refactor checks
- `refactor-if-something-fails` - What to do if checks fail
- `refactor-when-to-split` - Fast heuristics for when to split files

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/refactor-file-workflow.md
rules/refactor-decision-rules.md
rules/refactor-post-refactor-checks.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
