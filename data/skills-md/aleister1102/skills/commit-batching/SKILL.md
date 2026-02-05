---
name: commit-batching
description: Use when a working tree mixes logical changes that need separate conventional commits before pushing.
---

# Multi-Commit Workflow (Conventional)

## Overview
Break a mixed-delta branch into focused conventional commits by planning the sequence, staging deliberate hunks, and reviewing each set before committing.

## When to Use
- The working tree touches multiple features, refactors, or fixes that should not be lumped together.
- Preparing a pull request that must demonstrate ordered, reviewable steps.
- Sharing code where readable history matters for reviewers or downstream owners.

## When NOT to Use
- Single-feature changes that are already isolated.
- Quick typo or documentation fixes that can be handled as one commit.

## Quick Procedure

## Quick Procedure
1) **Inventory**: `git status -sb` → note files; skim `git diff --stat` for clusters.
2) **Plan**: Draft a commit table (order = dependency then narrative): `type(scope?): summary`. Keep commits orthogonal and testable.
3) **Stage per commit**
   - Path-based: `git add path/to/file`.
   - Hunk-based: `git add -p path` (use `s` split; `e` edit).
   - Unstage if needed: `git restore --staged <path>`.
4) **Review staged**: `git diff --cached` (ensure only intended hunks). Add brief inline comments in PR later, not here.
5) **Commit**: `git commit -m "<type>(<scope>): <summary>"` with guidelines below.
6) **Repeat** for remaining commits. End with `git status` (should be clean or only intentional leftovers).
7) **Validate history**: `git log --oneline -5` to check ordering and messages.
8) **Push**: `git push -u origin <branch>` (or `git push` if upstream set).

## Conventional Commit Cheatsheet
- **types**: feat, fix, chore, docs, style, refactor, perf, test, build, ci, revert.
- **scope**: optional; use folder, package, or short noun (e.g., `api`, `ui`, `infra`). No spaces.
- **summary**: max ~72 chars, imperative mood. Avoid trailing period.
- **breaking**: add `!` after type or scope; include `BREAKING CHANGE: ...` in body if needed.

Examples:
- `feat(api): add pagination to reports list`
- `fix(auth): handle expired refresh tokens`
- `chore: update README install steps`

## Planning Tips
- Group by user-facing behavior or deployable unit; avoid mixing refactors with functional changes in one commit.
- Order commits so tests/builds pass at each step; fixes before refactors only when dependency exists.
- If a file belongs in multiple commits, use `git add -p` to separate hunks.

## Safety Nets
- Inspect unstaged leftovers before final push: `git diff`.
- Amend only the most recent commit when it doesn’t affect reviewed history: `git commit --amend` (avoid after sharing).
- To reorder without losing safety, use `git rebase -i HEAD~N` (only if branch is unpublished); otherwise create follow-up fix commits.

## Minimal Body Template (when needed)
```
<type>(<scope>): <summary>

Context: <why this change>
Testing: <commands run or N/A>
```

## Publishing Checklist
- All commits pass tests they touch (run focused commands per commit if feasible).
- `git status` clean; remote set.
- Push and optionally draft PR with concise summary of commit plan.
