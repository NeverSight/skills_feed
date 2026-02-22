---
name: finishing-a-development-branch
description: Use when implementation is complete, all tests pass, and you need to decide how to integrate the work - guides completion of development work by presenting structured options for merge, PR, or cleanup
---

# Finishing a Development Branch

## Overview

Guide completion of development work by presenting clear options and handling chosen workflow.

**Core principle:** Verify tests -> Present options -> Execute choice -> Clean up.

**Announce at start:** "I'm using the finishing-a-development-branch skill to complete this work."

## The Process

### Step 1: Verify Tests

Run project's test suite using `scripts/run-tests` for auto-detection. **If tests fail:** show failures, stop — cannot proceed until tests pass. **If tests pass:** continue.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

### Step 3: Present Options

Present exactly these 4 options:
```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

**Don't add explanation** — keep options concise.

### Step 4: Execute Choice

See [references/option-details.md](references/option-details.md) for detailed execution steps for each option.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping test verification | Always verify tests before offering options |
| Open-ended questions | Present exactly 4 structured options |
| Automatic worktree cleanup | Only cleanup for Options 1 and 4 |
| No confirmation for discard | Require typed "discard" confirmation |

## Red Flags

**Never:** Proceed with failing tests, merge without verifying tests on result, delete work without confirmation, force-push without explicit request.

**Always:** Verify tests first, present exactly 4 options, get typed confirmation for Option 4, clean up worktree for Options 1 & 4 only.

## Integration

**Called by:** plan-execution
**Pairs with:** using-git-worktrees (cleans up worktree created by that skill)
