---
name: mr-description-generator
description: Generate comprehensive MR/PR descriptions based on branch changes. Use when creating merge requests or pull requests.
---

# MR/PR Description Generator

Generate comprehensive merge request descriptions by analyzing branch changes against the target branch.

## When to Use

- When user asks to create an MR/PR description
- When user wants to document branch changes for review
- Before creating a merge request to develop or main

## Process

### Step 1: Gather Branch Information

Run these commands to understand the changes:

```bash
# Get commits in current branch (not in target)
git log develop..HEAD --oneline

# Get file change statistics
git diff develop...HEAD --stat

# Get detailed diff for analysis
git diff develop...HEAD
```

### Step 2: Analyze Changes

Review the diff output and categorize:

1. **What type of changes?**
   - Feature addition/change
   - Bug fix
   - Refactoring
   - Documentation update
   - Configuration change

2. **What components are affected?**
   - Which apps (web-main, api-server, etc.)
   - Which packages
   - Which features

3. **What is the impact?**
   - New functionality
   - Fixed behavior
   - Performance improvements
   - Breaking changes

### Step 3: Generate Description

Use this template:

```markdown
## Description

Brief description of what this MR accomplishes.

## Changes Made

-   [ ] Feature addition/change
-   [ ] Bug fix
-   [ ] Refactoring
-   [ ] Documentation update
-   [ ] Configuration change

### Summary of Changes

**[Component/Feature Name] Improvements:**
- Change 1
- Change 2
- Change 3

**[Another Component] Changes:**
- Change 1
- Change 2

## Rules Pattern Compliance Checklist

This checklist ensures all merge requests follow the established patterns and conventions for `apps/web-main`.

### File Structure & Naming

-   [ ] Files/dirs are kebab-case and placed per conventions
-   [ ] **Suffix conventions strictly followed:**
    -   [ ] Hook files: `use-*.hook.ts` (not `.tsx`)
    -   [ ] Service files: `*.service.ts`
    -   [ ] Schema files: `*.schema.ts`
    -   [ ] Context files: `*.context.tsx`
    -   [ ] Provider files: `*.provider.tsx`
    -   [ ] Store files: `*.store.ts`

### Data Fetching

-   [ ] Data fetching via TanStack Query (client) or RSC (server) with prefetch/dehydrate as appropriate
-   [ ] Central QueryProvider used and configured

### Forms

-   [ ] Forms: Zod schema + react-hook-form integration

### Documentation

-   [ ] Docs updated if patterns changed or extended

### Code Quality

-   [ ] TypeScript compilation passes without errors
-   [ ] ESLint passes without violations
-   [ ] No cross-route imports from private co-located folders (`component`, `hooks`)

## Additional Notes

**Files Changed:**
- `path/to/file1.ts` - Description of change
- `path/to/file2.tsx` - Description of change
```

## Best Practices

1. **Be specific** - Describe actual changes, not generic statements
2. **Group related changes** - Organize by feature or component
3. **Include file paths** - Help reviewers navigate the changes
4. **Check the boxes** - Mark applicable items in the checklist
5. **Note breaking changes** - Call out anything that might affect other developers
6. **Mention removed code** - If significant code was deleted, explain why

## Output Format

Always provide the MR description in a markdown code block so users can easily copy-paste it.

## Version History

- v1.0.0 (2025-12-01): Initial release
