---
name: smart-revert
description: Git-aware smart revert for tracks, phases, and tasks. Handles rewritten history, finds related commits, and provides safe rollback with multiple confirmation gates.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Bash, Glob, Grep, Write, Edit]
best_practices:
  - Always require user confirmation before any destructive action
  - Handle ghost commits (rewritten history) gracefully
  - Find ALL related commits (implementation + plan updates)
  - Present clear execution plan before reverting
  - Verify plan state after revert completes
error_handling: strict
streaming: supported
---

# Smart Revert

Git-aware intelligent revert system for reverting logical work units (tracks, phases, tasks) while handling complex Git histories.

## When to Use

- Reverting completed tasks that need to be redone
- Rolling back entire phases that didn't meet requirements
- Undoing track changes after failed review
- Recovering from implementation mistakes
- Cleaning up after interrupted work

## Core Concepts

### Logical vs Physical Revert

| Type         | Description                                     | Example                 |
| ------------ | ----------------------------------------------- | ----------------------- |
| **Logical**  | Revert a track/phase/task as defined in plan.md | "Revert Task 2.1"       |
| **Physical** | Revert specific Git commits                     | "Revert commit abc1234" |

This skill bridges the gap: given a logical target, it finds all physical commits.

## 4-Phase Protocol

### Phase 1: Interactive Target Selection

1. **Check for explicit target**: Did user specify what to revert?
2. **If no target**: Present guided menu of candidates:
   - First: In-progress items (`[~]`)
   - Fallback: Recently completed items (`[x]`)
3. **Confirm intent**: Verify understanding before proceeding

**Menu Format:**

```
I found the following items to potentially revert:

Track: user-auth_20250115
  1) [Phase] Phase 2: Core Logic
  2) [Task] Task 2.1: Implement validation

3) A different Track, Task, or Phase

Which would you like to revert?
```

### Phase 2: Git Reconciliation

**Goal**: Find ALL commits related to the logical unit.

1. **Find implementation commits**:
   - Extract SHAs from plan.md (`[x] Task: Description \`abc1234\``)
   - Handle "ghost commits" (rebased/squashed)

2. **Find plan-update commits**:
   - For each implementation SHA, find the following plan.md update

3. **Find track creation commit** (if reverting entire track):
   - Search git log for when track entry was added to tracks.md

**Handling Ghost Commits:**

```
SHA abc1234 from plan.md not found in git history.
This may have been rewritten by rebase/squash.

Searching for similar commits...
Found: def5678 "feat(user): implement validation"

Is this the correct commit? (yes/no)
```

### Phase 3: Execution Plan Confirmation

Present clear summary before any action:

```
## Revert Execution Plan

**Target**: Task 2.1 "Implement user validation"
**Commits to Revert**: 2

1. `abc1234` - "feat(user): implement validation"
2. `def5678` - "conductor(plan): mark task 2.1 complete"

**Action**: Run `git revert --no-edit` on each commit (newest first)

Do you want to proceed?
A) Yes - execute the revert
B) No - cancel and review
```

### Phase 4: Execution & Verification

1. **Execute reverts** (newest to oldest):

   ```bash
   git revert --no-edit <sha>
   ```

2. **Handle conflicts**: If conflict occurs, provide guidance:

   ```
   Merge conflict detected. Please resolve manually:
   1. Edit conflicted files
   2. Run: git add .
   3. Run: git revert --continue
   ```

3. **Verify plan state**: Re-read plan.md to confirm status reset

4. **Announce completion**: Confirm revert succeeded

## Commit Identification Strategies

### Finding Implementation Commits

```bash
# Extract SHA from plan.md
grep -oP '\[x\].*`\K[a-f0-9]{7}' plan.md

# Verify SHA exists
git cat-file -t <sha>
```

### Finding Plan Update Commits

```bash
# Find commits that modified plan.md after implementation
git log --oneline -- path/to/plan.md | head -5
```

### Handling Rebased History

```bash
# Search by commit message similarity
git log --oneline --all | grep -i "implement validation"

# Search by file changes
git log --oneline --all -- src/models/user.py
```

### Finding Track Creation

```bash
# Find when track was added to registry
git log -p -- conductor/tracks.md | grep -B5 "Track: user-auth"
```

## Safety Features

### Multiple Confirmation Gates

| Gate                  | Purpose                       | When                      |
| --------------------- | ----------------------------- | ------------------------- |
| Target confirmation   | Verify correct item selected  | After selection           |
| Execution plan review | Show exactly what will happen | Before any git operation  |
| Final go/no-go        | Last chance to cancel         | Immediately before revert |

### Conflict Handling

If `git revert` fails:

1. **Do NOT** force or continue automatically
2. **Explain** what happened
3. **Provide** manual resolution steps
4. **Offer** to help after user resolves

### Post-Revert Verification

Always verify the plan file reflects the revert:

```markdown
Before: [x] Task 2.1: Implement validation `abc1234`
After: [ ] Task 2.1: Implement validation
```

If plan state is inconsistent, offer to fix it.

## Example Scenarios

### Scenario 1: Revert Single Task

```
User: "Revert the last task I completed"

Agent:
1. Read plan.md, find most recent [x] task
2. Extract SHA: abc1234
3. Find plan-update commit: def5678
4. Present: "Revert Task 2.1? Will undo abc1234, def5678"
5. User confirms
6. Execute: git revert --no-edit def5678 && git revert --no-edit abc1234
7. Verify plan.md shows [ ] for task
8. Report success
```

### Scenario 2: Revert Entire Phase

```
User: "/smart-revert phase 2"

Agent:
1. Find all tasks in Phase 2 with [x] status
2. Collect all implementation SHAs
3. Collect all plan-update SHAs
4. Find phase checkpoint SHA
5. Present comprehensive plan
6. User confirms
7. Execute reverts in reverse order
8. Verify all Phase 2 tasks show [ ]
9. Report success
```

### Scenario 3: Handle Ghost Commit

```
Agent: "Looking for SHA abc1234..."
Agent: "SHA not found. Checking for rebased commits..."
Agent: "Found similar commit def5678: 'feat(user): validation'"
Agent: "Is def5678 the correct replacement? (yes/no)"
User: "yes"
Agent: [continues with def5678]
```

## Integration Points

### With track-management

Read plan.md and tracks.md to understand work structure.

### With workflow-patterns

Follow established commit conventions when creating revert commits.

### With context-driven-development

Update context files if revert affects product features.

## Anti-Patterns

### Do NOT:

- Revert without confirmation
- Ignore ghost commits (fail silently)
- Leave plan.md in inconsistent state
- Force-push after revert
- Revert merge commits without special handling

### Do:

- Always verify target before action
- Handle rewritten history gracefully
- Verify plan state after revert
- Provide clear conflict resolution guidance
- Document what was reverted in commit message

## Related Skills

- `track-management` - Understand track/phase/task structure
- `workflow-patterns` - Git commit conventions
- `git-expert` - Advanced git operations
- `debugging` - When revert is needed due to bugs

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
