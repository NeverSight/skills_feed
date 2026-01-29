---
name: react-gradual-architecture
description: Incremental React code organization guidelines. Start small, then extract when scanning and responsibilities start to blur. Use when creating features, organizing files, refactoring components, or deciding when to extract hooks, UI, or utils.
license: MIT
compatibility: Works with React.
metadata:
  version: 1.0.0
  author: vandriesh
  categories: [react, architecture, organization, best-practices]
---

# React Gradual Architecture

Lightweight guidance for organizing React code without over-structuring. The core idea: start small, minimum necessary (one file), extract only when it improves clarity or reuse. Contains 12 rules across 5 categories, prioritized by when to apply them in the development lifecycle.

## When to Use This Skill

Reference these guidelines when:

- Creating new React features or components
- Organizing component files and folders
- Refactoring a growing component
- Deciding when to extract hooks, UI, or utils
- Structuring feature directories and shared code
- Creating feature documentation (README.md)

## Rule Categories by Priority

| Priority | Category | When to Apply | Prefix |
|----------|----------|---------------|--------|
| 1 | Foundation | Before starting any feature | `framework-` |
| 2 | Starting | When beginning a new feature | `start-` |
| 3 | Organization & Structure | When organizing files and folders | `organize-` |
| 4 | Extraction | When refactoring or extracting code | `extract-` |
| 5 | Data & State | When managing types and state | `data-`, `state-` |

## Quick Reference

### 1. Foundation (CRITICAL)

- `framework-conventions` - Follow framework conventions and keep domain code framework-agnostic
- `framework-react-router` - Use `.server` suffix for server-only code (React Router / Remix)

### 2. Starting (CRITICAL)

- `start-small` - Begin features in a single file;
- if a file has more that 100 lines of code proceed with organization and extractions accordingly.
- `component-composition` - Prefer composition over configuration; use children instead of many props (exception: variant props)


### 3. Organization & Structure

- `organize-features-folder` - Place features under `src/features/<feature>/` or `app/features/<feature>/`
- `organize-locality` - Keep related files close to the feature
- `organize-reuse-boundaries` - Wait for the second use before extracting shared code
- `organize-feature-readme` - Create README.md for each feature documenting structure and specifications


### 4. Extraction

- `extract-scrolling` - Extract when scanning becomes difficult
- `extract-to-share` - Use hooks for React logic, plain functions for everything else
- `extract-ui-logic-utils` - Extract UI, logic, and utils when concerns diverge
- `extract-container-presentational` - Extract container (data) from presentational (UI) components

### 5. Data & State

- `data-types-placement` - Define types where the data is born. **NEVER create separate `types.ts` files**
- `state-placement` - Keep state local; lift only as high as needed

## Rules Reference

The guidelines are organized into focused rule files. Reference the specific rules when making architectural decisions:

### Foundation
- [`framework-conventions.md`](rules/framework-conventions.md) - Follow framework conventions and keep domain code framework-agnostic
- [`framework-react-router.md`](rules/framework-react-router.md) - Use `.server` suffix for server-only code (React Router / Remix)

### Starting
- [`start-small.md`](rules/start-small.md) - Begin features in a single file
- [`component-composition.md`](rules/component-composition.md) - Prefer composition over configuration; use children instead of many props

### Organization & Structure
- [`organize-features-folder.md`](rules/organize-features-folder.md) - Place features under `src/features/<feature>/` or `app/features/<feature>/`
- [`organize-locality.md`](rules/organize-locality.md) - Keep related files close to the feature
- [`organize-reuse-boundaries.md`](rules/organize-reuse-boundaries.md) - Wait for the second use before extracting shared code
- [`organize-feature-readme.md`](rules/organize-feature-readme.md) - Create README.md for each feature documenting structure and specifications

### Extraction
- [`extract-scrolling.md`](rules/extract-scrolling.md) - Extract when scanning becomes difficult
- [`extract-to-share.md`](rules/extract-to-share.md) - Use hooks for React logic, plain functions for everything else
- [`extract-ui-logic-utils.md`](rules/extract-ui-logic-utils.md) - Extract UI, logic, and utils when concerns diverge
- [`extract-container-presentational.md`](rules/extract-container-presentational.md) - Extract container (data) from presentational (UI) components

### Data & State
- [`data-types-placement.md`](rules/data-types-placement.md) - Define types where the data is born
- [`state-placement.md`](rules/state-placement.md) - Keep state local; lift only as high as needed

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/start-small.md
rules/extract-scrolling.md
rules/organize-features-folder.md
```

Each rule file contains:
- Brief explanation of why it matters
- Examples showing the pattern
- Guidance on when to apply it
- Additional context and references

**Core Principles:**
1. Start with the overview above to understand the incremental approach
2. Reference specific rule files when making architectural decisions
3. Apply the smallest change that restores clarity
4. Extract only when it improves readability or enables reuse

## Full Compiled Document

For the complete guide with all rules expanded and optimized for AI agents: [`AGENTS.md`](AGENTS.md)

## Detailed Rule Documentation

See individual rule files in [`rules/`](rules/) for in-depth explanations and code examples.
