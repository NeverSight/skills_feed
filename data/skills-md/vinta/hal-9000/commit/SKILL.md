---
name: commit
description: Creates git commits. Use this skill whenever the user asks to commit, or whenever you need to commit changes as part of a task.
context: fork
user-invocable: true
model: sonnet
allowed-tools:
  - Grep
  - Glob
  - Bash(git status:*)
  - Bash(git diff:*)
  - Bash(git branch:*)
  - Bash(git log:*)
  - Bash(git stash:*)
  - Bash(git add:*)
  - Bash(git restore:*)
  - Bash(git mv:*)
  - Bash(git rm:*)
  - Bash(git apply:*)
  - Bash(git commit:*)
  - Read(//tmp/**)
  - Write(//tmp/**)
  - Edit(//tmp/**)
---

# Overview

Creating clean, atomic commits that follow best practices for version control hygiene. The core principle is **one logical change per commit** - each commit should represent a single, coherent, easily revertable modification that can stand alone.

## Instructions

**ALWAYS `cd` to project root before git commands. NEVER use `git -C`.** Execute git commands directly without explanatory preamble. Commit immediately without confirmation prompts (never use interactive mode).

1. **Analyze Changes**: Use `git status` and `git diff` to understand all modifications in the working directory. Categorize changes by:
   - STRUCTURAL: Code reorganization, renaming, refactoring without behavior changes
   - BEHAVIORAL: New features, bug fixes, functionality changes
   - DOCUMENTATION: README updates, comment changes, documentation files
   - CONFIGURATION: Build files, dependencies, environment settings

2. **Group Logically**: Organize changes into logical units where each unit:
   - Addresses a single purpose or problem
   - Structure changes to be atomic and easily revertable for safe rollback
   - Would make sense to revert as a unit

3. **Stage Changes**: Use appropriate staging strategy:
   - Whole file: `git add <file>`
   - Hunk-by-hunk: `git diff <file> > /tmp/patch.diff`, edit the patch to keep only specific hunks, then `git apply --cached /tmp/patch.diff`
   - NEVER use `git reset --hard`. To unstage, use `git restore --staged`
   - Fallback: If `git apply --cached` fails (malformed patch), stage the whole file with `git add <file>` instead

4. **Handle Pre-commit Hooks**: If hooks complain about unstaged changes:
   - Stash unstaged changes first: `git stash push -p -m "temp: unstaged changes"` (select hunks to stash)
   - Or stash all unstaged: `git stash push --keep-index -m "temp: unstaged changes"`
   - Commit, then restore: `git stash pop`
   - If hooks modify staged files (auto-formatting), re-add the modified files and retry the commit

5. **Create Atomic Commits**: For each logical group:
   - Write clear, descriptive commit messages following conventional format
   - Keep first line under 72 characters (aim for 50)
   - Include context in body when necessary
   - IMPORTANT: DO NOT run any linter/formatter before committing. Commit exactly what the user changed
