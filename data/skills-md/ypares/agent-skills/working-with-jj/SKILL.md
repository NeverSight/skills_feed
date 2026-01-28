---
name: working-with-jj
description: Expert guidance for using JJ (Jujutsu) version control system. Use when working with JJ, whatever the subject. Operations, revsets, templates, debugging change evolution, etc. Covers JJ commands, template system, evolog, operations log, and interoperability with git remotes.
version_target: "0.36.x"
---

# JJ (Jujutsu) Version Control Helper

## Core Principles

- **Change IDs** (immutable) vs **Commit IDs** (content-based hashes that change
  on edit)
- **Operations log** - every operation can be undone (progressive: multiple `jj undo` goes further back, `jj redo` reverses)
- **No staging area** - working copy auto-snapshots
- **Conflicts don't block** - resolve later
- **Commits are lightweight** - edit freely
- **Colocated by default** - Git repos have both `.jj` and `.git` (since v0.34)
- **Three DSLs**:
  - _revsets_: select across revisions - a revision (change) ID is a trivial but fully valid singleton revset
  - _filesets_: select across files in the repository - a regular filepath is a trivial but fully valid singleton fileset
  - _templates_: select which info to log and how to show it
  - Many jj commands expect expressions using either of these DSLs, to select what to show/operate on

## Essential Commands

```bash
jj log -r <revset> [-p]               # View history (--patch/-p: include diffs, --count: just count)
jj log -r <revset> -G                 # -G is short for --no-graph
jj show -r <rev>                      # Show revision details (description + diff)
jj evolog -r <rev> [-p]               # View a revision's evolution
jj new [-A] <base>                    # Create revision and edit it (-A: insert between <base> and its children rather than just on top of base)
jj new --no-edit <base>               # Create without switching
jj edit <rev>                         # Switch to editing revision
jj desc -r <rev> -m "text"            # Set description
jj metaedit -r <rev> -m "text"        # Modify metadata (author, timestamps, description)

jj diff                               # Changes in @
jj diff -r <rev>                      # Changes in revision
jj file show -r <rev> <fileset>       # Show file contents at revision (without switching)
jj file show -r <rev> **/*.md -T '"=== " ++ path ++ " ===\n"'  # Multiple files with path headers
jj restore <fileset>                    # Discard changes to files
jj restore --from <commit-id> <fileset> # Restore from another revision/commit

jj split -r <rev> <paths> -m "text"   # Split into two revisions
jj absorb                             # Auto-squash changes into ancestor commits

jj rebase -s <src> -o <dest>          # Rebase with descendants onto <dest>
jj rebase -r <rev> -o <dest>          # Rebase single revision onto <dest>
# NOTE: -d/--destination is deprecated, use -o/--onto instead

jj file annotate <path>               # Blame: who changed each line
jj bisect run -- <cmd>                # Binary search for bug-introducing commit
```

## Additional Commands

```bash
jj undo                               # Undo last operation (progressive - repeat to go further back)
jj redo                               # Redo undone operation
jj sign -r <rev>                      # Cryptographically sign commit
jj unsign -r <rev>                    # Remove signature
jj revert -r <rev>                    # Create commit that reverts changes (replaces old jj backout)
jj tag set <name> -r <rev>            # Create/update local tag
jj tag delete <name>                  # Delete local tag
jj git colocation enable              # Convert to colocated repo
jj git colocation disable             # Convert to non-colocated
```

## Quick Revset Reference

```bash
@, @-, @--                            # Working copy, parent(s), grandparent(s)
::@                                   # Ancestors
@::                                   # Descendants
mine()                                # Your changes
conflicted()                          # Has conflicts (renamed from conflict() in v0.33)
visible()                             # Visible revisions (built-in alias)
hidden()                              # Hidden revisions (built-in alias)
description(substring-i:"text")       # Match description (partial, case-insensitive)
subject(substring:"text")             # Match first line only
signed()                              # Cryptographically signed commits
A | B, A & B, A ~ B                   # Union, intersection, difference
change_id(prefix)                     # Explicit change ID prefix lookup
parents(x, 2)                         # Parents with depth
exactly(x, 3)                         # Assert exactly N revisions
```

See `references/revsets.md` for comprehensive revset patterns.

## Common Pitfalls

### 1. Use `-r` not `--revisions`

```bash
jj log -r xyz          # ✅
jj log --revisions xyz # ❌
```

### 2. Use `--no-edit` for parallel branches

```bash
jj new parent -m "A"; jj new -m "B"                             # ❌ B is child of A!
jj new --no-edit parent -m "A"; jj new --no-edit parent -m "B"  # ✅ Both children of parent
```

### 3. Quote revsets in shell

```bash
jj log -r 'description(substring:"[todo]")'    # ✅
```

### 4. Use `-o`/`--onto` instead of `-d`/`--destination` (v0.36+)

```bash
jj rebase -s xyz -o main   # ✅ New syntax
jj rebase -s xyz -d main   # ⚠️ Deprecated (still works but warns)
```

### 5. Symbol expressions are stricter (v0.32+)

Revset symbols no longer resolve to multiple revisions:

```bash
jj log -r abc              # ❌ Error if 'abc' matches multiple change IDs
jj log -r 'change_id(abc)' # ✅ Explicitly query by prefix
jj log -r 'bookmarks(abc)' # ✅ For bookmark name patterns
```

### 6. Glob patterns are default in filesets (v0.36+)

```bash
jj diff 'src/*.rs'         # Matches glob pattern by default
jj diff 'cwd:"src/*.rs"'   # Use cwd: prefix for literal path with special chars
```

## Scripts

Helper scripts in `scripts/`. Add to PATH or invoke directly.

| Script                                    | Purpose                                |
| ----------------------------------------- | -------------------------------------- |
| `jj-show-desc [REV]`                      | Print full description only            |
| `jj-desc-transform <REV> <CMD...>`        | Pipe description through command       |
| `jj-batch-desc <SED_FILE> <REV...>`       | Batch transform descriptions           |
| `jj-checkpoint [NAME]`                    | Record op ID before risky operations   |

## Recovery

```bash
jj op log              # Find operation before problem
jj op restore <op-id>  # Restore the WHOLE repository (history included) to that state
```

## References

- The `jj` exe is self-documenting:
  - Run `jj help -k bookmarks` - JJ bookmarks, how they relate to Git branches and how to push/fetch them from Git remotes
  - Run `jj help -k revsets` - Revset DSL syntax and patterns
  - Run `jj help -k filesets` - Filepath selection DSL, ie. how to tell jj commands to operate only on specific files
  - Run `jj help -k templates` - Template language and custom output
  - All jj subcommands have a pretty detailed `--help` page
- `references/command-syntax.md` - Command flag details
- `references/batch-operations.md` - Complex batch transformations on revision descriptions
