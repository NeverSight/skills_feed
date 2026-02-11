---
name: diff-check
description: Author's cleanup checklist before committing or submitting a PR. Use before any commit or PR to ensure code is clean, focused, and ready for review. Checks for debug code, secrets, redundant changes, and scope creep.
---

# Diff Check

Perform routine cleanup and validation before committing code or submitting a PR.

## When to Use

- Before any `git commit`
- Before marking a PR ready for review
- After implementing changes, before requesting review

## Checklist

### 1. Scope & Focus
- [ ] Changes are within the scope of the task/PR
- [ ] No redundant or unnecessary code changes
- [ ] No unrelated formatting or whitespace changes

### 2. Code Cleanup
- [ ] No debugging code left in (console.log, print, dbg!, etc.)
- [ ] No testing stubs or mock data in production code
- [ ] No commented-out code blocks (unless intentionally preserved)
- [ ] No self-explanatory comments that clutter code

### 3. Security
- [ ] No secrets, API keys, or credentials exposed
- [ ] No hardcoded local file paths (e.g., /home/user1/...)
- [ ] No sensitive information in comments or logs

### 4. Consistency
- [ ] Code follows project lint/format rules
- [ ] Naming conventions are consistent
- [ ] Import statements are organized

### 5. Plan Alignment
- [ ] Relevant checkboxes in plan.md are marked complete
- [ ] Commit message is clear and follows conventions

### 6. Branch Health (PR only)
- [ ] Synced with main/target branch
- [ ] No merge conflicts
- [ ] CI checks pass (if applicable)

## Process

1. Review all staged/modified files
2. Walk through checklist above
3. Report any issues found with recommended fixes
4. Do NOT make changes automatically—report for human confirmation

## Output Format

```
[DIFF CHECK COMPLETE]

Files reviewed: [N]
Issues found: [M]

Critical:
- [file:line] [issue description]

Warnings:
- [file:line] [issue description]

Suggestions:
- [recommendation]

Status: [READY / NEEDS FIXES]
```
