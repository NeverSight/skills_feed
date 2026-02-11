---
name: coding-best-practices
description: General coding principles for writing clean, maintainable code. Use for development work, code reviews, refactoring, dependency changes, and design discussions about code structure, performance, and reliability.
---

# Coding Best Practices

## Core Principles

### Fix Root Causes

- Fix from first principles; find the source instead of applying bandaids
- If a fix feels like a workaround, it probably is—dig deeper

### Simplicity

- Write idiomatic, simple, maintainable code
- Prefer the most straightforward solution to the problem
- Prefer small helpers or state-driven flow to keep cyclomatic complexity low

### Quality Bar

- Update tests (or add coverage) when behavior changes
- Handle errors intentionally; avoid silent failures
- Remove unintended debug logs; keep logs actionable and low-noise

### Clean Up Ruthlessly

- Leave each repo better than you found it
- Delete unused code immediately—don't let junk linger (but keep cleanup local to what you touched unless the user asks for a wider refactor)
- If a function no longer needs a parameter, remove it and update callers
- If a helper is dead, delete it

### No Breadcrumbs

- When deleting or moving code, do not leave comments in the old location
- No `// moved to X`, no `// relocated`—just remove it
- Describe changes in your response, not in the code

### Scope Control

- Prefer small, reviewable changes over sweeping refactors
- Avoid “drive-by” rewrites in unrelated areas
- If a larger refactor is warranted, propose it explicitly and ask before proceeding

## Code Organization

### File Length

- Use judgment based on complexity rather than strict line limits
- Split files when they become difficult to navigate or understand
- If a file has multiple distinct concerns, split it
- Aim for files that can be read and understood in a single sitting

### UI Component Files

- For React: keep one primary component per file
- Small helper components (variants, icon sets, button sizes) can coexist if they're tightly coupled
- Group related components into folder structures (e.g., `components/` for primary, `components/Button/` with sub-components)

### Separation Principles

- Separate concerns when they can be used independently or tested in isolation
- Types/interfaces that are shared across multiple files → `types/` or `@types`
- Utility functions used in multiple places → `utils/` organized by domain
- Custom hooks used by multiple components → `hooks/`
- Constants and config → `config/` or `constants/`
- Keep things together that change together

### Directory Structure

- Organize by feature/domain, not by file type (e.g., `auth/` not `components/auth/`, `hooks/auth/`)
- Flatten directories when possible—avoid deep nesting
- Use index/barrel files only when the repo already uses them and they don’t introduce dependency cycles or tooling issues

## Dependencies

Before adding a new dependency:
- Quick health check: recent releases/commits?
- Reasonable adoption/community?
- Actively maintained?
- Does it solve a problem we can't easily solve ourselves?

## When Unsure

1. Read more code, documents, or files
2. If still stuck, ask with short options
3. If there are conflicts or ambiguity, call them out and take the safer path

## Context Awareness

- If project or repo-specific guidance conflicts with these rules, follow project guidance first
- Assume other agents or the user might land commits mid-run; refresh context before summarizing or editing
- If changes look unrecognized and continuing is problematic, stop and ask
