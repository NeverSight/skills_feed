---
name: code-cleanup
description: Delegate repetitive tasks to specialized agent to preserve context. Use when user asks to fix linting errors, fix diagnostics, rename variables across files, update imports, fix formatting issues, or perform other mechanical bulk changes across multiple files.
---

# Delegate to Code Janitor

When you encounter **repetitive, mechanical code tasks**, launch the `code-janitor` agent instead of doing the work yourself to preserve context.

## Delegate When:

- Fixing multiple linting errors across files
- Renaming variables/functions consistently across codebase
- Updating import statements in multiple files
- Fixing formatting or style violations throughout project
- Resolving IDE diagnostics in batch
- Bulk refactoring that doesn't require design decisions

## Keep in Main When:

- Task requires architectural decisions
- Single file with 1-2 changes
- User explicitly wants you to do it

## How:

Use Task tool with `subagent_type: "essentials:code-janitor"` providing task description and scope.

The code-janitor agent uses TodoWrite to track work, iterates until complete, and verifies with linters.
