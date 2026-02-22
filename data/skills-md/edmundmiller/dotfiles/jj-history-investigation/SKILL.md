---
name: jj-history-investigation
description: Investigate jj commit history, split commits, annotate file changes, and clean up redundant commits. Use when debugging history, splitting large commits, or rewriting shared history.
---

# Jujutsu (jj) History Investigation and Manipulation

## Overview

When working with complex jj repositories, you may need to investigate historical commits, split monolithic changes into focused commits, or clean up messy history. This skill documents efficient techniques for:

- **Investigating commit history**: Finding when changes were made and why
- **Using jj annotate**: Tracking down who/when specific lines were added
- **Splitting commits**: Breaking large commits into focused, reviewable pieces
- **Handling immutability**: Overriding protections when rewriting shared history
- **Cleaning up redundancy**: Removing duplicate or empty commits
- **Resolving conflicts**: Fixing merge conflicts after rebases

## Core Commands

| Command            | Purpose                      | Example                                    |
| ------------------ | ---------------------------- | ------------------------------------------ |
| `jj log`           | View commit history          | `jj log -r 'ancestors(@, 10)'`             |
| `jj show`          | Display commit details       | `jj show abc123`                           |
| `jj file annotate` | Line-by-line change tracking | `jj file annotate src/main.tex`            |
| `jj edit`          | Start editing a commit       | `jj edit abc123 --ignore-immutable`        |
| `jj split`         | Split a commit into pieces   | `jj split --ignore-immutable path/to/file` |
| `jj abandon`       | Remove commits from history  | `jj abandon abc123`                        |
| `jj rebase`        | Move commits to new base     | `jj rebase -b main -d new-base`            |

## Investigation Techniques

### 1. Finding When a Change Was Made

When you know a file changed but not when, use these approaches:

**Check recent commit messages:**

```bash
# Search for commits mentioning "copyright"
jj log -r 'description(copyright)' --no-graph

# Output:
# trsozpwy feat(frontmatter): Add post-defense required sections
# (shows commits with "copyright" in the message)
```

**View commit details:**

```bash
# Show full commit with statistics
jj show trsozpwy --stat

# Show just the files changed
jj show trsozpwy --summary
```

**Check specific file history:**

```bash
# See who/when each line was added
jj file annotate src/main.tex | grep "copyrightpage"

# Output:
# trsozpwy edmund.m 2025-11-09 00:13:05   49: \copyrightpage{2025}
```

### 2. Understanding Commit Lineage

**Check what's built on top of a commit:**

```bash
# View descendants of commit abc123
jj log -r 'abc123::@' --limit 20

# Check ancestors of current commit
jj log -r 'ancestors(@, 10)'
```

**Find relationships between branches:**

```bash
# See where main and feature branches diverged
jj log -r 'ancestors(main) & ancestors(feature)'

# Check if commit is ancestor of main
jj log -r 'abc123::main'
```

### 3. Extracting Specific Commit Information

**Get commit metadata:**

```bash
# Show commit ID, author, date
jj show abc123 | head -10

# Get just the change ID
jj log -r abc123 --no-graph -T 'change_id'
```

**Check file changes:**

```bash
# See what changed in a commit
jj diff -r abc123

# See specific file diff
jj diff -r abc123 src/main.tex
```

## Splitting Commits

### When to Split

Split a commit when it contains multiple logical changes that should be reviewed separately:

- ✅ **Good candidates**: "Add frontend + backend + tests + docs"
- ✅ **Mixed concerns**: Copyright page + acknowledgments + CV in one commit
- ❌ **Already focused**: "Fix typo in README"

### Basic Split Workflow

**1. Check if commit is immutable:**

```bash
jj edit abc123

# If error: "Commit abc123 is immutable"
# Then use --ignore-immutable flag
```

**2. Edit the commit:**

```bash
jj edit abc123 --ignore-immutable

# Working copy now at abc123
# File system shows state at that commit
```

**3. Split by file/directory:**

```bash
# Split out specific files
jj split --ignore-immutable src/main.tex

# jj will prompt for commit messages for:
# - Selected changes (what you specified)
# - Remaining changes (everything else)
```

**4. Split incrementally:**

```bash
# After first split, you're at "remaining changes"
# Split again to extract more pieces
jj split --ignore-immutable src/chapters/appendix.tex
```

**5. Update commit messages:**

```bash
# Update the commit you just split
jj describe @- -m "feat(frontmatter): Enable copyright page"

# Continue until all pieces are separated
```

### Advanced Split Techniques

**Split and update TODO in same commit:**

```bash
# 1. Split out the main change
jj split --ignore-immutable src/main.tex

# 2. In the split commit, also update TODO.org
# Edit TODO.org to mark item as DONE
jj describe -m "feat(frontmatter): Enable copyright page

Enable copyright on page ii as recommended by UTD.
Mark as complete in TODO.org."
```

**Split multiple files into one commit:**

```bash
# Save final state
cp src/main.tex /tmp/main.tex.final

# Restore to parent
jj restore --from @- src/main.tex

# Apply changes incrementally
# Make change 1, commit
# Make change 2, commit
# etc.
```

## Handling Immutability

### Why Commits Become Immutable

Commits are immutable when:

- They have descendants (other commits built on top)
- They're in shared history (pushed to remote)
- They're marked explicitly in config

### Overriding Immutability

**When it's safe:**

- ✅ Local-only history (not pushed)
- ✅ You own all descendant commits
- ✅ No collaborators affected

**How to override:**

```bash
# Edit immutable commit
jj edit abc123 --ignore-immutable

# Split immutable commit
jj split --ignore-immutable src/main.tex

# Note: This will rewrite ALL descendant commits
```

**What happens:**

```bash
# Before split:
# abc123 (monolithic commit)
#   ↓
# def456 (descendant 1)
#   ↓
# ghi789 (descendant 2)

# After split:
# abc123 (piece 1)
#   ↓
# xyz111 (piece 2)
#   ↓
# def456' (rewritten descendant 1)
#   ↓
# ghi789' (rewritten descendant 2)
```

## Cleaning Up History

### Identifying Redundant Commits

**Find empty commits:**

```bash
# Show commit stats
jj show abc123 --stat

# If output shows "0 files changed", it's empty
```

**Find conflicting commits:**

```bash
# Check for conflicts
jj log -r 'all()' | grep conflict

# Output:
# ×  abc123 (conflict) feat: Add something
```

### Abandoning Commits

**Remove redundant commits:**

```bash
# Abandon single commit
jj abandon abc123

# Abandon multiple commits
jj abandon abc123 def456 ghi789

# What happens:
# - Commit is removed from history
# - Descendants are rebased onto parent
# - Changes are preserved in descendants
```

**Abandon empty commits automatically:**

```bash
# After rebasing, jj may create empty commits
# Abandon them to clean up
jj log -r 'all()' --summary | grep "(empty)"
jj abandon empty-commit-id
```

### Cleaning Up After Split

**Common pattern:**

```bash
# 1. Split monolithic commit
jj edit old-commit --ignore-immutable
jj split src/file1.txt
jj split src/file2.txt
# (repeat for each logical piece)

# 2. Check for redundant descendants
jj log -r 'old-commit::@' --limit 30

# 3. Abandon redundant commits
jj abandon redundant-commit-1 redundant-commit-2

# 4. Verify history
jj log -r 'old-commit::@' --no-graph
```

## Resolving Conflicts

### After Rebase/Split

**1. Identify conflicts:**

```bash
jj status

# Output:
# Warning: There are unresolved conflicts at these paths:
# TODO.org    2-sided conflict
```

**2. Create commit to resolve:**

```bash
# Create new commit on top of conflict
jj new conflicted-commit-id
```

**3. Read conflict markers:**

```bash
cat TODO.org

# Output:
# <<<<<<< Conflict 1 of 1
# +++++++ Contents of side #1
# ** DONE Add something
# %%%%%%% Changes from base to side #2
# ** TODO Add something
# >>>>>>> Conflict 1 of 1 ends
```

**4. Choose resolution:**

```bash
# Edit file to pick side #1, side #2, or merge both
# Remove conflict markers

# Or use editor with conflict resolution
jj resolve TODO.org
```

**5. Squash resolution:**

```bash
# Merge resolution into parent
jj squash

# This resolves the conflict in the parent commit
```

## Verifying History

### After Major Changes

**1. Check commit lineage:**

```bash
# View commits from base to current
jj log -r 'base-commit::@' --limit 50

# Check all commits are present
jj log -r 'commit1 | commit2 | commit3' --no-graph
```

**2. Verify each commit is focused:**

```bash
# For each commit in your split:
jj show commit-id --stat

# Should show:
# - Small number of files changed
# - Logical grouping of changes
# - Clear commit message
```

**3. Check for conflicts:**

```bash
# List all commits with conflicts
jj log -r 'all()' | grep conflict

# Should be empty after cleanup
```

**4. Verify bookmarks:**

```bash
# Check where main/feature branches point
jj log -r 'bookmarks()'

# Ensure they're at correct positions
```

### History Health Checklist

After split/rebase/cleanup:

- [ ] No conflict markers in `jj status`
- [ ] No `(conflict)` labels in `jj log`
- [ ] No empty `(empty)` commits (unless intentional)
- [ ] Commit messages are clear and descriptive
- [ ] Each commit has focused changes
- [ ] Bookmarks (main, feature, etc.) point correctly
- [ ] TODO.org or similar files are consistent

## Real-World Example

**Scenario:** Historical commit `trsozpwy` contains 6 different changes mixed together. Need to split for review.

**Investigation phase:**

```bash
# 1. Find the commit
jj log -r 'description(post-defense)' --no-graph
# Found: trsozpwy

# 2. Check what's in it
jj show trsozpwy --stat
# Shows: 10 files changed

# 3. Check if immutable
jj edit trsozpwy
# Error: Commit is immutable (16 descendants)

# 4. Verify we can override
jj log -r 'trsozpwy::@' --limit 20
# Shows descendant commits, all owned by us
```

**Split phase:**

```bash
# 1. Override immutability
jj edit trsozpwy --ignore-immutable

# 2. Split out Python scripts
jj split --ignore-immutable src/figures/modules/
jj describe @- -m "feat(ch3): Add core overlap Venn diagram scripts"

# 3. Split out appendix fix
jj split --ignore-immutable src/chapters/appendix-*.tex
jj describe @- -m "fix(appendix): Remove 'A' label from solo appendix"

# 4. Split frontmatter pieces incrementally
# (Copyright page)
# Edit src/main.tex to add only copyright
jj commit -m "feat(frontmatter): Enable copyright page (2025)"

# (Acknowledgments)
# Edit src/main.tex to add acknowledgments
jj commit -m "feat(frontmatter): Add acknowledgments section"

# (And so on for biographical sketch, CV)
```

**Cleanup phase:**

```bash
# 1. Check for redundant descendants
jj log -r 'trsozpwy::@' | grep "Mark post-defense"
# Found: kqkm (redundant - duplicates our split work)

# 2. Abandon redundant commits
jj abandon kqkm lkto qqkq srls

# 3. Rebase main branch onto splits
jj rebase -b main -d last-split-commit

# 4. Resolve conflicts
jj new conflicted-commit
# Edit TODO.org to pick correct side
jj squash
```

**Verification phase:**

```bash
# 1. Check final structure
jj log -r 'first-split::@' --limit 30

# 2. Verify each split commit
jj show trso --stat  # Core overlap scripts
jj show nlnr --stat  # Appendix fix
jj show zspm --stat  # Copyright page
jj show mrpk --stat  # Acknowledgments
jj show wqrn --stat  # Biographical sketch
jj show ynom --stat  # CV

# 3. Confirm no conflicts
jj status
# (should be clean)

# 4. Check bookmarks
jj log -r 'bookmarks()'
# main and Cleanup should be on correct commits
```

**Result:** Successfully split 1 monolithic commit into 6 focused commits, each with clear intent and proper TODO.org updates.

## Tips and Tricks

### Speed Up Investigation

**Use aliases for common queries:**

```bash
# In ~/.jjconfig.toml
[aliases]
recent = ["log", "-r", "ancestors(@, 20)", "--no-graph"]
conflicts = ["log", "-r", "conflicts()"]
empty = ["log", "-r", "empty()"]
```

**Search commit messages efficiently:**

```bash
# Case-insensitive search
jj log -r 'description("(?i)copyright")'

# Multiple terms
jj log -r 'description(frontmatter) & description(copyright)'
```

### Avoid Common Pitfalls

1. **Don't split without investigation**: Always `jj show` first to understand what's in a commit
2. **Save state before split**: `cp important-file /tmp/` before major history rewrites
3. **Split incrementally**: Don't try to split everything at once; do one logical piece at a time
4. **Update TODO immediately**: Mark TODO items in the same commit that does the work
5. **Verify after each step**: Check `jj log` frequently during split/rebase operations

### When NOT to Split

- Commit is already pushed and shared with others
- Changes are truly atomic (e.g., "Fix typo + its test")
- Split would make history harder to understand
- Commit is ancient and rarely viewed

## References

- [jj Documentation](https://jj-vcs.github.io/jj/)
- [jj Revset Language](https://jj-vcs.github.io/jj/latest/revsets/)
- [jj Conflict Resolution](https://jj-vcs.github.io/jj/latest/conflicts/)

## Related Skills

- `jj:jj-workflow` - Basic jj operations and workflow
- `jj:commit-messages` - Writing good commit messages
- `jj:commit-curation` - Organizing commits for sharing
