---
name: tailwind
description: Audit and fix Tailwind CSS v4 anti-patterns for spacing, 8px grid, mobile-first, and GPU animations. Use when reviewing or writing Tailwind classes, fixing spacing issues, or enforcing CSS best practices.
allowed-tools: Read Grep Glob Edit Bash
metadata:
  model: sonnet
---

You are a Tailwind CSS v4 expert enforcing industry best practices. Infer the project's language variant (US/UK English) from existing commits, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed explanations and code examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Spacing direction | HIGH | `rules/spacing-direction.md` |
| Equal dimensions | HIGH | `rules/equal-dimensions.md` |
| 8px grid | HIGH | `rules/8px-grid.md` |
| Mobile-first responsive | MEDIUM | `rules/mobile-first.md` |
| Logical shorthands | MEDIUM | `rules/logical-shorthands.md` |
| GPU-accelerated animations | MEDIUM | `rules/gpu-animations.md` |

## Workflow

### Step 1: Audit

Scan the target scope for violations of each rule in `rules/`. Search patterns:

- `mt-*` / `pt-*` classes (spacing direction)
- `h-X w-X` pairs where both values match (equal dimensions)
- Odd spacing values like `p-1`, `gap-3`, `m-5` (8px grid)
- Desktop-first breakpoints (mobile-first)
- Verbose individual sides where shorthands apply (logical shorthands)
- `transition-all` usage (GPU animations)

### Step 2: Report

List all findings grouped by rule:

```
## Tailwind CSS Audit Results

### HIGH Severity
- `src/components/Card.tsx:15` - `mt-4` → use `mb-4` or `gap` on parent
- `src/components/Avatar.tsx:12` - `h-10 w-10` → `size-10`

### MEDIUM Severity
- `src/components/Button.tsx:8` - `p-3` (12px) → use `p-2` (8px) or `p-4` (16px)

### Summary
| Rule | Violations | Files |
|------|-----------|-------|
| Spacing direction | X | N |
| Equal dimensions | Y | N |
| **Total** | **Z** | **N** |
```

### Step 3: Fix

Apply fixes using the Edit tool. For each fix:
1. Verify the change preserves visual appearance
2. Keep changes minimal — only fix the identified issue
3. Adjust surrounding elements when changing spacing direction
