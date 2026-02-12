---
name: unslop
description: Remove AI-generated "slop" from codebases by deleting redundant comments and unused code, tightening formatting, and normalizing styling patterns (e.g., Tailwind class consistency, Nuxt UI color tokens). Use when a user asks to clean up code, remove unnecessary comments, reduce unused imports/variables, or align Tailwind/Nuxt UI conventions.
---

# Unslop

## Overview
Eliminate low-signal artifacts from AI-generated code while preserving behavior and intent.

## Workflow

1. **Triage the files**
   - Scan each file for redundancy, dead code, and style inconsistencies.
   - Identify the UI framework (Vue/Nuxt) and styling system (Tailwind, Nuxt UI, plain CSS).

2. **Remove redundant commentary**
   - Delete comments that restate the obvious (function names, prop names, component names).
   - Remove template comments in `.vue`/HTML/JSX unless they explain non-obvious UX or business logic.
   - Drop TODOs that add no actionable information (e.g., "TODO: add logic").

3. **Delete unused code paths**
   - Remove unused imports, variables, props, computed values, watchers, and helpers.
   - Delete commented-out code blocks unless the user asks to keep them.
   - Prune branches that are never reached or are placeholders.

4. **Normalize styling conventions**
   - Consolidate duplicated Tailwind utilities; prefer `size-*` over `w-* h-*` when equal.
   - Align class order and grouping with nearby components.
   - In Nuxt UI, prefer semantic tokens (e.g., `color-success`) over raw color classes.

5. **Validate output**
   - Confirm behavior and UI output remain unchanged except for cleanup.
   - Keep any "why" commentary that preserves intent or constraints.

## Decision Checklist

- **Is the comment telling me *why*?** Keep.
- **Is the comment just paraphrasing code?** Remove.
- **Is this code referenced anywhere?** If not, delete it.
- **Would removing this change behavior or test expectations?** If yes, keep or re-evaluate.

## Comment Removal Heuristics

- Remove: "Handle click", "Render header", "Fetch user" when the code is explicit.
- Keep: "Workaround for Safari focus bug", "Required by backend contract", "Do not reorder due to animation timing".
- Shorten: Replace a paragraph with a single line explaining the non-obvious constraint.

## Tailwind & UI Normalization

- Replace paired width/height with size utilities:
  - `w-10 h-10` → `size-10`
  - `w-6 h-6` → `size-6`
- Keep consistent axis usage:
  - Use `px-*` + `py-*` or `p-*` consistently within the same component.
- Favor semantic UI tokens in Nuxt UI:
  - `color-green-500 dark:color-green-400` → `color-success`
  - Align with `variant`/`color` props when available.

## File-Type Guidance

### Vue/Nuxt (`.vue`)
- Remove HTML comments inside templates unless they explain layout constraints.
- Drop unused `defineProps`, `defineEmits`, or computed properties.
- Remove unused `ref`/`computed` imports from Vue.

### TypeScript/JavaScript
- Remove unused imports and variables; collapse trivial one-use helpers.
- Prefer direct inlining when helpers only wrap a single line.

### CSS
- Remove unused classes if not referenced in templates/components.
- Consolidate duplicated declarations.

## Output Expectations

- Provide a clean diff that focuses solely on removal/normalization.
- Avoid unrelated refactors or renames.
- If behavior might change, explain the risk and avoid the change.

## Examples

- "Remove all useless comments in these components and trim unused imports."
- "Clean up this Vue file: remove template comments and align Tailwind classes."
- "Normalize Nuxt UI button colors to semantic tokens."
- "Delete dead code and placeholders, but keep any workaround comments."

## Guardrails

- Keep comments that encode constraints, historical context, or known bugs.
- Preserve references to tickets/issues if they explain a workaround.
- Do not change runtime behavior, data flow, or UI output beyond cleanup.
