---
name: reimplement-branch
description: Reimplement the current branch on a new branch with a clean, narrative-quality git commit history. Use when the user wants to clean up messy commits, create a tutorial-style commit history, or prepare a branch for review with logical, self-contained commits. Triggers on requests like "clean up my commits", "reimplement this branch", "create a clean history", or "make my commits reviewable".
---

# Reimplement Branch

Create a new branch with a clean, narrative-quality commit history from an existing branch's changes.

## Context

- Source branch: !`git branch --show-current`
- Git status: !`git status --short`
- Commits since main: !`git log main..HEAD --oneline`
- Full diff against main: !`git diff main...HEAD --stat`

## Workflow

### 1. Validate source branch

- Ensure no uncommitted changes or merge conflicts
- Confirm branch is up to date with `main`

### 2. Analyze the diff

Study all changes between source branch and `main`. Form a clear understanding of the final intended state.

### 3. Create clean branch

```bash
git checkout main
git checkout -b <new-branch-name>
```

Use the user-provided branch name, or `{source-branch}-clean` if none provided.

### 4. Plan commit storyline

Break the implementation into self-contained logical steps. Each step should reflect a stage of development—as if writing a tutorial.

### 5. Reimplement the work

Recreate changes in the clean branch, committing step by step. Each commit must:

- Introduce a single coherent idea
- Include a clear commit message and description

**Use `git commit --no-verify` for intermediate commits.** Pre-commit hooks check tests, types, and imports that may not pass until full implementation is complete.

### 6. Verify correctness

- Confirm final state exactly matches source branch: `git diff <source-branch>`
- Run final commit **without** `--no-verify` to ensure all checks pass

### 7. Open PR

Use the `/pr` skill to create a pull request. Include a link to the original branch in the PR description.

## Rules

- Never add yourself as author or contributor
- Never include "Generated with Claude Code" or "Co-Authored-By" lines
- End state of clean branch must be identical to source branch
