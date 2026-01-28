---
name: clean-history
description: Reimplement the current branch on a new branch with a clean, narrative-quality git commit history suitable for reviewer comprehension. Use when the user wants to clean up messy commit history before opening a PR.
argument-hint: [new-branch-name]
allowed-tools: Bash(git:*), Bash(gh pr create:*)
model: opus
---

# Clean History

Reimplement the current branch on a new branch with a clean, narrative-quality git commit history.

## Context

- Source branch: !`git branch --show-current`
- Git status: !`git status --short`
- Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@' || git config init.defaultBranch || echo main`
- Remote branches: !`git branch -r --list 'origin/main' 'origin/master' 2>/dev/null | head -1 | sed 's/.*origin\///'`

## Task

Reimplement the current branch on a new branch with a clean, narrative-quality git commit history suitable for reviewer comprehension.

**New Branch Name**: Use `$ARGUMENTS` if provided, otherwise `{source_branch}-clean`.

**Base Branch**: Determine the base branch using this priority:
1. The "Default branch" from context above (if available)
2. The first available branch from "Remote branches" (`origin/main` or `origin/master`)
3. Fall back to `main` if neither is available

### Steps

1. **Validate the source branch**
   - Ensure no uncommitted changes or merge conflicts
   - Confirm the source branch is not the same as the base branch (error if so)
   - Run `git log {base}..HEAD --oneline` to see commits to clean
   - Run `git diff {base}...HEAD --stat` to see the full diff
   - Confirm source branch is up to date with the base branch

2. **Analyze the diff**
   - Study all changes between source branch and the base branch
   - Form a clear understanding of the final intended state

3. **Create the clean branch**
   - Create a new branch off of the base branch using the new branch name

4. **Plan the commit storyline**
   - Break the implementation into self-contained logical steps
   - Each step should reflect a stage of development—as if writing a tutorial

5. **Reimplement the work**
   - Recreate changes in the clean branch, committing step by step
   - Each commit must:
     - Introduce a single coherent idea
     - Include a clear commit message and description
   - **Use `git commit --no-verify` for all intermediate commits.** Pre-commit hooks check tests, types, and imports that may not pass until the full implementation is complete. Do not waste time fixing issues in intermediate commits that will be resolved by later commits.

6. **Verify correctness**
   - Confirm the final state exactly matches the source branch
   - Run the final commit **without** `--no-verify` to ensure all checks pass

7. **Open a pull request**
   - Create a PR with a summary of the changes
   - Include a link to the original branch in the PR description

### Rules

- Never add yourself as an author or contributor
- Never include "Generated with Claude Code" or "Co-Authored-By" lines in commits
- The end state of the clean branch must be identical to the source branch
