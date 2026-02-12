---
name: git-commit-plan
description: Plan commits from the current working tree. Use when asked how to split changes into commits, what to stage together, how to handle untracked files, or to propose commit messages and an execution plan (stage/commit) based on `git status`/diffs.
---

# Git Commit Plan

## Goal

Turn the current repo state into a small set of clean, reviewable commits:
- Group changes by intent (feature/fix/refactor/docs/chore) and scope.
- Keep commits as independent as possible.
- Propose Conventional Commit messages and the exact files per commit.
- Ask for explicit confirmation before staging/committing (and pushing).

## Workflow

### 1) Gather signals (read-only)

Run:
- `git status --porcelain=v2`
- `git diff --stat`
- `git diff`
- `git diff --staged` (if anything is already staged)

If there are untracked files, list them explicitly.

### 2) Decide commit boundaries

Use these heuristics:
- **One intent per commit**: do not mix unrelated changes.
- **Keep mechanical changes separate**: formatting-only or purely generated output should be isolated unless the repo convention says otherwise.
- **Keep dependency changes coherent**: e.g., `package.json` with its lockfile; do not mix with functional changes unless unavoidable.
- **Prefer minimal blast radius**: if a commit requires changes across many areas, consider splitting into preparatory refactor + behavior change (ask first).
- **Untracked files**: decide whether each should be committed, gitignored, or deleted (ask if unclear).

### 3) Propose a concrete plan

Output a numbered list of commits. For each commit, include:
- **Commit message** (Conventional Commits)
- **Files** to include
- **Notes** (why grouped this way, anything risky)

Also propose the exact commands to execute the plan, favoring:
- `git add -p` when changes are mixed
- `git add <paths...>` when the grouping is clean

### 4) Ask to execute

End with a clear question before making changes:

“Do you want me to execute this plan?”
- Option A: stage only
- Option B: stage + commit
- Option C: stage + commit + push (only if you explicitly request push)

If anything about grouping, naming, or inclusion is ambiguous, ask short questions with options.
