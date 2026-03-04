---
name: rename-swarm
description: Parallel bulk rename across many files using a swarm of haiku agents. Use when mechanically renaming identifiers, parameters, or keys across 5+ files.
---

You are an expert at orchestrating parallel mechanical renames across large codebases using swarms of lightweight agents. This skill documents a proven pattern for completing bulk renames in a single batch rather than sequential file-by-file edits.

## When to Use

- Renaming an identifier, parameter, key, or variable across **5+ files**
- The renames are **mechanical** — same find-and-replace logic in each file, no reasoning required
- Files are **independent** — editing file A doesn't affect what needs to change in file B
- Examples: renaming `issue_number` to `plan_number`, renaming `old_func` to `new_func`, updating a key name across config consumers

## When NOT to Use

- **Cross-file cascading refactors** where renaming a shared type changes method signatures, requiring each file to adapt differently
- **Renames requiring judgment** — e.g., "rename this concept" where each call site needs context-aware naming
- **Fewer than 5 files** — sequential edits are simpler and have less overhead
- **Complex AST transforms** — use `libcst-refactor` agent instead

## The Pattern

### Step 1: Identify All Files

Use Grep to find every file containing the target identifier:

```
Grep(pattern="old_name", output_mode="files_with_matches")
```

Partition files into two groups:

- **Source files** (`src/` or library code)
- **Test files** (`tests/`)

### Step 2: Launch Source File Agents in Parallel

Launch one `Task` agent per file (or per small group of 2-3 closely related files):

```python
Task(
    subagent_type='general-purpose',
    model='haiku',
    description='Rename old_name in path/to/file.py',
    prompt="""..."""  # See agent prompt template below
)
```

**Launch ALL source file agents in a single message** so they run concurrently.

### Step 3: Wait for Source Agents to Complete

Collect results from all source file agents. Review for errors.

### Step 4: Launch Test File Agents in Parallel

Same pattern as Step 2, but for test files. This second wave runs after source files because tests import from source — if source renames fail, test renames would be wrong.

### Step 5: Verify

After all agents complete:

1. **Grep check**: Confirm old name no longer appears (except intentional exceptions)
2. **Run CI**: Use devrun agent to run tests, type checking, and linting

## Agent Prompt Template

Each agent receives a focused, self-contained prompt:

```
In the file `{file_path}`:

Rename all occurrences of `{old_name}` to `{new_name}`.

This includes:
- Variable names and assignments
- Function/method parameter names
- Dictionary keys (both definition and access)
- String literals that reference the identifier programmatically
- Type annotations
- Comments that reference the identifier by name

DO NOT rename:
- {boundary_constraints}

Read the file first, then apply all renames using the Edit tool.
```

### Boundary Constraints

Boundary constraints are critical for partial renames. Always specify what should NOT be renamed. Examples:

- `"Do not rename occurrences inside string literals that are user-facing messages"`
- `"Do not rename the GitHub API field 'issue_number' — only rename internal references"`
- `"Do not rename imports from external packages"`

If there are no exceptions, state: `"No exceptions — rename ALL occurrences."`

## Batching Strategy

| Wave | Files                 | Rationale                                                    |
| ---- | --------------------- | ------------------------------------------------------------ |
| 1    | Source files (`src/`) | Core renames, no dependencies on other waves                 |
| 2    | Test files (`tests/`) | Tests import from source; must run after source renames land |

Within each wave, all agents run in parallel. Between waves, wait for completion.

For very large renames (30+ files), consider sub-batching into groups of ~10-15 agents per message to avoid overwhelming the system.

## Key Design Decisions

- **Model: haiku** — mechanical edits need speed, not deep reasoning. Haiku is 10x cheaper and sufficient for find-and-replace tasks.
- **One agent per file** — keeps prompts focused, avoids cross-file edit conflicts, makes failures isolated and retriable.
- **Two waves (source then test)** — tests depend on source; parallel within each wave, sequential between waves.
- **Explicit boundary constraints** — every agent prompt MUST specify what not to rename. Omitting this causes over-eager renames (e.g., renaming API field names that must stay as-is).

## Example: Renaming `issue_number` to `plan_number`

1. Grep found 16 source files and 12 test files containing `issue_number`
2. Wave 1: Launched 16 haiku agents for source files — completed in ~25 seconds
3. Wave 2: Launched 12 haiku agents for test files — completed in ~20 seconds
4. Verification: `Grep(pattern="issue_number")` confirmed only intentional GitHub API references remained
5. CI: All tests passed, type checker clean

Total wall time: ~60 seconds for 28 files, vs ~10+ minutes for sequential edits.
