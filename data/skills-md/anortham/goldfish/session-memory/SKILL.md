---
name: session-memory
description: Automatically restore session context from persistent memory at the start of every coding session. Use this skill IMMEDIATELY when starting work to recall previous checkpoints, active plans, and git context. MANDATORY for context restoration.
allowed-tools: mcp__goldfish__recall, mcp__goldfish__plan, Read, Bash
---

# Session Memory Skill

## Purpose
Restore full working context from persistent memory **automatically at session start**. This prevents loss of context from previous sessions, crashes, or context window resets.

## When to Activate
**MANDATORY at session start** - This skill should activate automatically when:
- User starts a new coding session
- Context has been reset or compacted
- User returns to a project after time away
- User asks "what was I working on?" or similar

**DO NOT ask permission** - Just use it. The user expects context restoration.

## Orchestration Steps

### 1. Immediate Context Recall (First Action)
```
Call: recall({ days: 7, limit: 20 })
```

This returns:
- Recent checkpoints (last 7 days)
- Active plan (if any)
- Git context (branches, files changed)
- Work summary

### 2. Analyze Recalled Context
Examine the results to understand:
- What was the last task being worked on?
- Is there an active plan? What's its status?
- Were there any blockers or discoveries?
- What files were being modified?

### 3. Present Context to User
Provide a **concise summary** (2-3 sentences):
```
"Welcome back! You were working on [task] in the [branch] branch.
Your last checkpoint was [description].
[Active plan status if present]."
```

### 4. Offer Next Steps
Based on the context, suggest:
- Resume the previous task
- Review the active plan
- Start a new task
- Address any blockers mentioned

## Example Session Start

```markdown
**Context Restored:**

Last session (2 hours ago):
- Fixed JWT authentication timeout bug
- Added refresh token rotation
- Branch: feature/auth-improvements
- All tests passing

**Active Plan:** "Auth System Redesign" (75% complete)

**Suggested next steps:**
1. Continue with OAuth2 integration (next plan item)
2. Review test coverage
3. Start something new
```

## Error Handling

**If recall returns empty:**
- This is a new workspace or first session
- Explain that Goldfish will track work going forward
- Encourage checkpointing at key moments

**If recall fails:**
- Fall back to git status to understand workspace
- Explain memory system may need setup
- Continue without restored context

## Key Behaviors

### ✅ DO
- Call recall() as THE FIRST action in a session
- Present findings concisely
- Use recalled context to inform next actions
- Checkpoint new work to build memory

### ❌ DON'T
- Ask permission to recall (just do it)
- Overwhelm user with all checkpoint details
- Ignore active plans in the recall results
- Forget to use recalled git context

## Success Criteria

This skill succeeds when:
- User feels continuity between sessions
- No "what was I doing?" confusion
- Active plans are automatically resumed
- Git context matches recalled work

## Performance

- Recall operation: ~30-150ms
- Should complete before user notices
- Non-blocking, graceful degradation

---

**Remember:** Memory restoration is MANDATORY. Users expect it. Don't ask, just recall and present context naturally.
