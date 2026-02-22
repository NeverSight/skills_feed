---
name: session-reset
description: >-
  Reset the session while preserving context. Commits changes, writes a PROMPT.md
  capturing current work state, tears down any active team if present, then guides the
  user through /clear and context restoration. Supports a `new` parameter
  (`/session-reset new`) to write only key institutional knowledge without current
  task/progress — for starting a different task while preserving learnings. Use when the
  context window is getting large, the session needs a fresh start, or when switching
  focus. Also use when user says "reset", "fresh start", "save and clear", or "write
  prompt".
---

# Session reset

Preserve session context across a /clear by writing state to PROMPT.md, teardown, and restoring afterwards.

## Parameters

| Arg        | Behaviour                                                                                                                                                                                          |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| _(none)_   | **Full reset** — write all four sections (task, method, key things, progress)                                                                                                                          |
| `new`      | **New-task reset** — write only the "Key things to remember" section, omitting current task, method, and progress. Use this when starting a different task but carrying over institutional knowledge.   |

## Workflow

### 1. Commit and push

Check `git status` for uncommitted changes. If there are any:

**Security check** — before staging, scan changed files for secrets. Flag and exclude any files matching
common sensitive patterns (`.env*`, `*.key`, `*.pem`, `credentials.*`, `*secret*`, `*.token`). Warn
the user if any are found and never stage them without explicit confirmation.

Then ask the user:

- **Commit and push** — stage safe changes, commit with a concise message, and push to the current branch
- **Commit only** — stage and commit without pushing
- **Skip** — leave changes as-is

If the user chooses to commit, use `/commit`. If they also want to push, push after the commit succeeds.

If the working tree is already clean, tell the user "Working tree is clean — nothing to commit." and move on.

### 2. Write PROMPT.md

Generate PROMPT.md at the **project root** by reviewing the current session state. PROMPT.md is ephemeral and must **never** be committed.

#### Default mode (no args)

```markdown
# PROMPT.md

## Current task
<!-- What we're working on - the goal, feature, or fix -->

## Method
<!-- Which workflow/approach is active (e.g. OpenSpec, manual, etc.) -->
<!-- Include any active change IDs, branch names, or tracking references -->

## Key things to remember
<!-- Important decisions made, constraints, user preferences, gotchas -->
<!-- Architectural choices, rejected approaches, edge cases discovered -->

## Progress
<!-- Where we are in the process -->
<!-- What's done, what's in flight, what's next -->
<!-- Any blocking issues or open questions -->
```

#### `new` mode (`/session-reset new`)

```markdown
# PROMPT.md

## Key things to remember
<!-- Important decisions made, constraints, user preferences, gotchas -->
<!-- Architectural choices, rejected approaches, edge cases discovered -->
<!-- Codebase patterns, conventions, and quirks worth preserving -->
```

Guidelines:

- Be specific and actionable — the next session has zero prior context
- Include file paths, branch names, change IDs, and concrete references
- Capture _why_ decisions were made, not just _what_ was decided
- In `new` mode, focus on reusable knowledge: architecture decisions, codebase quirks, user preferences, tooling setup, and gotchas — anything valuable regardless of which task comes next
- Keep it concise but complete enough to be useful without re-investigation

### 3. Tear down team (if active)

If a team is active (check for team config in `$CONFIG_DIR/teams/`):

1. Read the team config to discover all active members
2. List the active members to the user and confirm they want to tear down the team
3. Send `shutdown_request` to each teammate
4. Wait for confirmations
5. Delete the team with `TeamDelete`

If no team is active, tell the user "No active team — skipping teardown." and move on.

### 4. Guide the user

After teardown, output this message exactly:

```
Session state saved to PROMPT.md. All agents shut down.

Run `/clear` now, then tell me: **read PROMPT.md**
```

### 5. Restore (post-clear)

When the user says "read PROMPT.md" after a /clear:

1. Read PROMPT.md from the project root
2. Summarise the restored context to the user
3. Resume work based on the progress section
