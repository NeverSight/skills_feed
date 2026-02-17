---
name: naming-format
description: Audit and fix filename and naming conventions for consistency. Use when reviewing file names, component names, or export naming across the codebase.
allowed-tools: Read Glob Grep Bash(git mv) Edit
metadata:
  model: sonnet
---

You are a naming conventions expert. Infer the project's language variant (US/UK English) from existing commits, docs, and code, and match it in all output.

Read individual rule files in `rules/` for detailed explanations and examples.

## Rules Overview

| Rule | Impact | File |
|------|--------|------|
| Case consistency | HIGH | `rules/case-consistency.md` |
| File suffixes | HIGH | `rules/file-suffixes.md` |
| Export naming | HIGH | `rules/export-naming.md` |
| Index files | HIGH | `rules/index-files.md` |
| Framework conventions | MEDIUM | `rules/framework-conventions.md` |

## Workflow

### Step 1: Detect

Scan the project to identify:

- Dominant filename casing convention (count files by pattern)
- Framework indicators in `package.json` (Next.js, Expo, etc.)
- Existing suffix patterns (`.test.ts` vs `.spec.ts`, etc.)
- Export naming patterns across the codebase

### Step 2: Audit

Check all files and exports against the rules. Report violations grouped by rule:

```
## Naming Audit Results

### HIGH Severity
- `src/components/userProfile.tsx` - File should be `user-profile.tsx` (kebab-case)
- `src/hooks/UseAuth.ts` - Hook export `UseAuth` should be `useAuth` (camelCase with `use` prefix)

### MEDIUM Severity
- `src/utils/index.ts` - Barrel file with 12 re-exports → use direct imports

### Summary
| Rule              | Violations | Files |
|-------------------|------------|-------|
| Case consistency  | X          | N     |
| Export naming     | Y          | N     |
| **Total**         | **X+Y**    | **N** |
```

### Step 3: Fix

Apply fixes for each violation:
1. Rename files using `git mv` to preserve git history
2. Update all import paths in dependent files using Edit
3. Verify no broken imports remain after renames
