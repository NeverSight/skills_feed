---
name: codemap
description: Analyze codebase structure, dependencies, and changes. Use when user asks about project structure, where code is located, how files connect, what changed, or before starting any coding task. Provides instant architectural context.
---

# Codemap

Codemap gives you instant architectural context about any codebase. Use it proactively before exploring or modifying code.

## Commands

```bash
codemap .                     # Project structure and top files
codemap --deps                # Dependency flow (imports/functions)
codemap --diff                # Changes vs main branch
codemap --diff --ref <branch> # Changes vs specific branch
```

## When to Use

### ALWAYS run `codemap .` when:
- Starting any new task or feature
- User asks "where is X?" or "what files handle Y?"
- User asks about project structure or organization
- You need to understand the codebase before making changes
- Exploring unfamiliar code

### ALWAYS run `codemap --deps` when:
- User asks "how does X work?" or "what uses Y?"
- Refactoring or moving code
- Need to trace imports or dependencies
- Evaluating impact of changes
- Finding hub files (most-imported)

### ALWAYS run `codemap --diff` when:
- User asks "what changed?" or "what did I modify?"
- Reviewing changes before commit
- Summarizing work done on a branch
- Assessing what might break
- Use `--ref <branch>` when comparing against something other than main

## Output Interpretation

### Tree View (`codemap .`)
- Shows file structure with language detection
- Stars (★) indicate top 5 largest source files
- Directories are flattened when empty (e.g., `src/main/java`)

### Dependency Flow (`codemap --deps`)
- External dependencies grouped by language
- Internal import chains showing how files connect
- HUBS section shows most-imported files
- Function counts per file

### Diff Mode (`codemap --diff`)
- `(new)` = untracked file
- `✎` = modified file
- `(+N -M)` = lines added/removed
- Warning icons show files imported by others (impact analysis)

## Examples

**User asks:** "Where is the authentication handled?"
**Action:** Run `codemap .` then `codemap --deps` to find auth-related files and trace their connections.

**User asks:** "What have I changed on this branch?"
**Action:** Run `codemap --diff` to see all modifications with impact analysis.

**User asks:** "How does the API connect to the database?"
**Action:** Run `codemap --deps` to trace the import chain from API to database files.

**User asks:** "I want to refactor the utils module"
**Action:** Run `codemap --deps` first to see what depends on utils before making changes.
