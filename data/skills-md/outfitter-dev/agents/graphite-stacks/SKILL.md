---
name: graphite-stacks
description: This skill should be used when the user asks to "create a stack", "submit stacked PRs", "gt submit", "gt create", "reorganize branches", "fix stack corruption", or mentions Graphite, stacked PRs, gt commands, or trunk-based development workflows.
metadata:
  version: "1.0.0"
  author: outfitter
  category: version-control
---

# Graphite Stacks

Trunk-based development with stacked PRs using Graphite CLI.

<when_to_use>

- Creating or managing branch stacks
- Submitting stacked PRs
- Reorganizing branch relationships
- Addressing PR feedback across a stack
- Recovering from stack corruption
- Any `gt` command usage

</when_to_use>

## Core Principle

**Use `gt` commands exclusively.** Mixing `git` and `gt` causes sync issues and divergent stacks. The only exception: `git add` for staging (or use `-a` flags).

## This, Not That

| Task | This | Not That |
| ---- | ---- | -------- |
| Create branch | `gt create 'name' -am "msg"` | `git checkout -b name` |
| Commit changes | `gt modify -acm "msg"` | `git commit -m "msg"` |
| Push to remote | `gt submit` | `git push` |
| Rebase stack | `gt restack` | `git rebase` |
| View stack | `gt status` or `gt ls` | `git log --graph` |
| Switch branches | `gt checkout` | `git checkout` |
| Amend commit | `gt modify -a` | `git commit --amend` |
| Multi-PR feedback | `gt top && gt absorb -a` | Cherry-pick commits manually |

## Stack Lifecycle

```
Create stack → Implement features → Submit PRs → Address feedback → Merge
     │              │                  │               │            │
     ▼              ▼                  ▼               ▼            ▼
 gt create     gt modify -acm     gt submit      gt absorb     gt sync
```

## Creating Stacks

```bash
# New branch with staged changes
gt create 'feature/step-1' -am "feat: first step"

# Continue stacking
gt create 'feature/step-2' -am "feat: second step"
gt create 'feature/step-3' -am "feat: third step"

# Insert branch between current and child
gt create 'feature/step-1.5' --insert -am "feat: inserted step"
```

## Navigation

| Command | Action |
| ------- | ------ |
| `gt up` | Move up the stack (toward children) |
| `gt down` | Move down the stack (toward parent) |
| `gt top` | Jump to stack top |
| `gt bottom` | Jump to stack bottom |
| `gt checkout` | Interactive branch picker |

## Modifying Branches

```bash
# Amend current branch (stages all)
gt modify -a

# New commit within same branch
gt modify -acm "fix: address review feedback"

# Commit to a different branch in the stack
git add path/to/file.ts
gt modify --into target-branch -m "feat: add file"
```

<rules>

**ALWAYS:**
- Use `gt create` for new branches
- Use `gt modify` for commits
- Use `gt submit` to push
- Use `gt restack` after parent changes
- Check `gt status` when uncertain

**NEVER:**
- Mix `git commit/push/rebase` with `gt` workflows
- Force push without understanding stack state
- Use `git rebase -i` (breaks Graphite metadata)

</rules>

## Addressing Review Feedback

**Single PR**: Navigate to branch, modify directly

```bash
gt checkout target-branch
gt modify -acm "fix: address review comment"
gt submit
```

**Multiple PRs in stack**: Use absorb from top

```bash
gt top
git add .
gt absorb -a
gt submit --stack
```

Graphite routes changes to correct branches based on file history.

## Reorganizing Stacks

```bash
# Move branch to different parent
gt move --onto new-parent

# Move specific branch
gt move --source branch-name --onto target

# After reorganization
gt restack
```

## Submitting

```bash
# Current branch + downstack
gt submit

# Entire stack
gt submit --stack

# Non-interactive (automation)
gt submit --no-interactive
```

## Stack Visualization

```bash
# JSON with parent relationships (preferred for scripts)
gt status

# Visual tree
gt ls

# Recent history
gt log
```

## Sync and Maintenance

```bash
# Pull trunk, rebase stacks, clean merged
gt sync

# Rebase branches onto updated parents
gt restack

# Undo last gt operation
gt undo
```

## When Things Go Wrong

Stack corruption symptoms:
- Branches appear as siblings instead of parent-child
- PRs contain wrong files
- `gt status` shows unexpected structure

See [recovery.md](references/recovery.md) for step-by-step recovery procedures.

<references>

- [commands.md](references/commands.md) - Quick command reference
- [recovery.md](references/recovery.md) - Stack corruption recovery

</references>
