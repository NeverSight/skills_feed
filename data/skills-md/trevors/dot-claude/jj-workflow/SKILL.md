---
name: jj-workflow
description: Jujutsu (jj) version control, load skill when hook output shows vcs=jj-colocated or vcs=jj in the system-reminder.
---

# jj Workflow

## CRITICAL: Avoid Interactive Mode

**Always use `-m` flag** to prevent jj from opening an editor:

```bash
# WRONG - opens editor, blocks AI
jj new
jj describe
jj squash

# CORRECT - non-interactive
jj new -m "message"
jj describe -m "message"
jj squash -m "message"
```

**Never use these interactive commands:**

- `jj split` - inherently interactive, no non-interactive mode

## Mental Model

**No staging area.** Your working directory is always a commit. Every save is tracked.

- `@` = your current change (the working copy)
- `@-` = parent of current change
- Changes are mutable until pushed

## When to Use What

| Situation                   | Do This                                                   |
| --------------------------- | --------------------------------------------------------- |
| Starting new work           | `jj new -m "what I'm trying"`                             |
| Forgot to start with jj new | `jj describe -m "what I'm doing"` (do this immediately)   |
| Work is done, move on       | `jj new -m "next task"`                                   |
| Annotate what you did       | `jj describe -m "feat: auth"`                             |
| Broke something             | `jj op log` → `jj op restore <id>`                        |
| Undo one file               | `jj restore --from @- <path>`                             |
| Combine messy commits       | `jj squash -m "combined message"`                         |
| Try something risky         | `jj new -m "experiment"`, then `jj abandon @` if it fails |

## AI Coding Pattern

**Always have a description.** The working copy should never stay "(no description set)".

```bash
# BEFORE starting work - declare intent
jj new -m "feat: add user logout button"
# Now implement... jj tracks everything automatically

# FORGOT to start with jj new? Describe immediately
jj describe -m "feat: what I'm working on"
```

**Why this matters:**

- `jj log` shows meaningful history while working
- Easier to understand what each change does
- Simpler to curate/squash later
- Teammates can follow progress

```bash
# Checkpoint before risky changes
jj describe -m "checkpoint: auth works"
jj new -m "trying OAuth integration"

# If it breaks
jj op log              # Find good state
jj op restore <id>     # Go back

# When done, curate history
jj squash -m "feat: OAuth support"
```

## Push to GitHub

**Pushed commits are immutable.** You can't squash into or modify them. The safe pattern:

```bash
# 1. Abandon empty checkpoint commits cluttering history
jj log -r '::@'                      # Find checkpoints
jj abandon <change-ids>              # Remove empty ones

# 2. Describe your work (don't try to squash into immutable parent)
jj describe -m "feat: what you did"

# 3. Move bookmark to your commit and push
jj bookmark set master -r @
jj git push
```

**For feature branches (new):**

```bash
jj bookmark create feature-x -r @
jj git push --bookmark feature-x
# If refused, configure auto-tracking once:
jj config set --user 'remotes.origin.auto-track-bookmarks' 'glob:*'
# Then retry: jj git push --bookmark feature-x
```

**For feature branches (updating):**

```bash
jj bookmark set feature-x -r @
jj git push
```

Teammates see clean git. They don't know you used jj.

## Recovery

The oplog records every operation. Nothing is lost.

```bash
jj op log                      # See all operations
jj undo                        # Undo last operation
jj op restore <id>             # Jump to any past state
```

## Bail Out

```bash
rm -rf .jj    # Delete jj, keep git unchanged
```
