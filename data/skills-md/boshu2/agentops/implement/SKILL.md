---
name: implement
description: 'Execute a single beads issue with full lifecycle. Triggers: "implement", "work on task", "fix bug", "start feature", "pick up next issue".'
---

# Implement Skill

> **Quick Ref:** Execute single issue end-to-end. Output: code changes + commit + closed issue.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Execute a single issue from start to finish.

**Requires:** bd CLI (beads) for issue tracking. Falls back to plain descriptions if unavailable.

## Execution Steps

Given `/implement <issue-id-or-description>`:

### Step 0: Check Issue State (Resume Logic)

Before starting implementation, check if resuming:

1. **Check if issue is in_progress:**
```bash
bd show <issue-id> --json 2>/dev/null | jq -r '.status'
```

2. **If status = in_progress AND assigned to you:**
   - Look for checkpoint in issue notes: `bd show <id> --json | jq -r '.notes'`
   - Resume from last checkpoint step
   - Announce: "Resuming issue from Step N"

3. **If status = in_progress AND assigned to another agent:**
   - Report: "Issue claimed by <agent> - use `bd update <id> --assignee self --force` to override"
   - Do NOT proceed without explicit override

4. **Store checkpoints after each major step:**
```bash
bd update <issue-id> --append-notes "CHECKPOINT: Step N completed at $(date -Iseconds)" 2>/dev/null
```

### Step 0a: Check Ratchet Status (RPI Workflow)

**Before implementation, verify prior workflow gates passed:**

```bash
# Check if ao CLI is available
if command -v ao &>/dev/null; then
  # Check if research and plan phases completed
  RATCHET_STATUS=$(ao ratchet status --json 2>/dev/null || echo '{}')
  RESEARCH_DONE=$(echo "$RATCHET_STATUS" | jq -r '.research.completed // false')
  PLAN_DONE=$(echo "$RATCHET_STATUS" | jq -r '.plan.completed // false')

  if [ "$RESEARCH_DONE" = "true" ] && [ "$PLAN_DONE" = "true" ]; then
    echo "Ratchet: Prior gates passed (research + plan complete)"
  elif [ "$RESEARCH_DONE" = "false" ] || [ "$PLAN_DONE" = "false" ]; then
    echo "WARNING: Prior gates not complete. Run /research and /plan first."
    echo "  Research: $RESEARCH_DONE"
    echo "  Plan: $PLAN_DONE"
    echo ""
    echo "Override with: ao ratchet skip <gate> --reason 'manual override'"
  fi

  # Get current spec path for reference
  SPEC_PATH=$(ao ratchet spec 2>/dev/null || echo "")
  if [ -n "$SPEC_PATH" ]; then
    echo "Ratchet: Current spec at $SPEC_PATH"
  fi
else
  echo "Ratchet: ao CLI not available - skipping gate check"
fi
```

**Fallback:** If ao is not available, proceed without ratchet checks. The skill continues normally.

### Step 1: Get Issue Details

**If beads issue ID provided** (e.g., `gt-123`):
```bash
bd show <issue-id> 2>/dev/null
```

**If plain description provided:** Use that as the task description.

**If no argument:** Check for ready work:
```bash
bd ready 2>/dev/null | head -3
```

### Step 2: Claim the Issue

```bash
bd update <issue-id> --status in_progress 2>/dev/null
```

### Step 3: Gather Context

**USE THE TASK TOOL** to explore relevant code:

```
Tool: Task
Parameters:
  subagent_type: "Explore"
  description: "Gather context for: <issue title>"
  prompt: |
    Find code relevant to: <issue description>

    1. Search for related files (Glob)
    2. Search for relevant keywords (Grep)
    3. Read key files to understand current implementation
    4. Identify where changes need to be made

    Return:
    - Files to modify (paths)
    - Current implementation summary
    - Suggested approach
    - Any risks or concerns
```

### Step 4: Implement the Change

Based on the context gathered:

1. **Edit existing files** using the Edit tool (preferred)
2. **Write new files** only if necessary using the Write tool
3. **Follow existing patterns** in the codebase
4. **Keep changes minimal** - don't over-engineer

### Step 5: Verify the Change

**Success Criteria (all must pass):**
- [ ] All existing tests pass (no new failures introduced)
- [ ] New code compiles/parses without errors
- [ ] No new linter warnings (if linter available)
- [ ] Change achieves the stated goal

Check for test files and run them:
```bash
# Find tests
ls *test* tests/ test/ __tests__/ 2>/dev/null | head -5

# Run tests (adapt to project type)
# Python: pytest
# Go: go test ./...
# Node: npm test
# Rust: cargo test
```

**If tests exist:** All tests must pass. Any failure = verification failed.

**If no tests exist:** Manual verification required:
- [ ] Syntax check passes (file compiles/parses)
- [ ] Imports resolve correctly
- [ ] Can reproduce expected behavior manually
- [ ] Edge cases identified during implementation are handled

**If verification fails:** Do NOT proceed to Step 5a. Fix the issue first.

### Step 5a: Verification Gate (MANDATORY)

**THE IRON LAW:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE

Before reporting success, you MUST:

1. **IDENTIFY** - What command proves this claim works?
2. **RUN** - Execute the FULL command (fresh, not cached output)
3. **READ** - Check full output AND exit code
4. **VERIFY** - Does output actually confirm the claim?
5. **ONLY THEN** - Make the completion claim

**Forbidden phrases without fresh verification evidence:**
- "should work", "probably fixed", "seems to be working"
- "Great!", "Perfect!", "Done!" (without output proof)
- "I just ran it" (must run it AGAIN, fresh)

#### Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Too simple to verify" | Simple code breaks. Verification takes 10 seconds. |
| "I just ran it" | Run it AGAIN. Fresh output only. |
| "Tests passed earlier" | Run them NOW. State changes. |
| "It's obvious it works" | Nothing is obvious. Evidence or silence. |
| "The edit looks correct" | Looking != working. Run the code. |

**Store checkpoint:**
```bash
bd update <issue-id> --append-notes "CHECKPOINT: Step 5a verification passed at $(date -Iseconds)" 2>/dev/null
```

### Step 6: Commit the Change

If the change is complete and verified:
```bash
git add <modified-files>
git commit -m "<descriptive message>

Implements: <issue-id>"
```

### Step 7: Close the Issue

```bash
bd update <issue-id> --status closed 2>/dev/null
```

### Step 7a: Record Implementation in Ratchet Chain

**After successful issue closure, record in ratchet:**

```bash
# Check if ao CLI is available
if command -v ao &>/dev/null; then
  # Get the commit hash as output artifact
  COMMIT_HASH=$(git rev-parse HEAD 2>/dev/null || echo "")
  CHANGED_FILES=$(git diff --name-only HEAD~1 2>/dev/null | tr '\n' ',' | sed 's/,$//')

  if [ -n "$COMMIT_HASH" ]; then
    # Record successful implementation
    ao ratchet record implement \
      --output "$COMMIT_HASH" \
      --files "$CHANGED_FILES" \
      --issue "<issue-id>" \
      2>&1 | tee -a .agents/ratchet.log

    if [ $? -eq 0 ]; then
      echo "Ratchet: Implementation recorded (commit: ${COMMIT_HASH:0:8})"
    else
      echo "Ratchet: Failed to record - chain.jsonl may need repair"
    fi
  else
    echo "Ratchet: No commit found - skipping record"
  fi
else
  echo "Ratchet: ao CLI not available - implementation NOT recorded"
  echo "  Run manually: ao ratchet record implement --output <commit>"
fi
```

**On failure/blocker:** Record the blocker in ratchet:

```bash
if command -v ao &>/dev/null; then
  ao ratchet record implement \
    --status blocked \
    --reason "<blocker description>" \
    2>/dev/null
fi
```

**Fallback:** If ao is not available, the issue is still closed via bd but won't be tracked in the ratchet chain. The skill continues normally.

### Step 8: Report to User

Tell the user:
1. What was changed (files modified)
2. How it was verified (with actual command output)
3. Issue status (closed)
4. Any follow-up needed
5. **Ratchet status** (implementation recorded or skipped)

**Output completion marker:**
```
<promise>DONE</promise>
```

If blocked or incomplete:
```
<promise>BLOCKED</promise>
Reason: <why blocked>
```

```
<promise>PARTIAL</promise>
Remaining: <what's left>
```

## Key Rules

- **Explore first** - understand before changing
- **Edit, don't rewrite** - prefer Edit tool over Write tool
- **Follow patterns** - match existing code style
- **Verify changes** - run tests or sanity checks
- **Commit with context** - reference the issue ID
- **Close the issue** - update status when done

## Without Beads

If bd CLI not available:
1. Skip the claim/close status updates
2. Use the description as the task
3. Still commit with descriptive message
4. Report completion to user
