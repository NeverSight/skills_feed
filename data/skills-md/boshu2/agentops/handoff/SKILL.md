---
name: handoff
description: 'Create structured handoff for session continuation. Triggers: handoff, pause, save context, end session, pick up later, continue later.'
---

# Handoff Skill

> **Quick Ref:** Create structured handoff for session continuation. Output: `.agents/handoff/YYYY-MM-DD-<topic>.md` + continuation prompt.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Create a handoff document that enables seamless session continuation.

## Execution Steps

Given `/handoff [topic]`:

### Step 1: Create Output Directory

```bash
mkdir -p .agents/handoff
```

### Step 2: Identify Session Context

**If topic provided:** Use it as the handoff identifier.

**If no topic:** Derive from recent activity:
```bash
# Recent commits
git log --oneline -5 --format="%s" | head -1

# Check current issue
bd current 2>/dev/null | head -1

# Check ratchet state
ao ratchet status 2>/dev/null | head -3
```

Use the most descriptive source as the topic slug.

**Topic slug format:** 2-4 words, lowercase, hyphen-separated (e.g., `auth-refactor`, `api-validation`).
**Fallback:** If no good topic found, use `session-$(date +%H%M)` (e.g., `session-1430`).

### Step 3: Gather Session Accomplishments

**Review what was done this session:**

```bash
# Recent commits this session (last 2 hours)
git log --oneline --since="2 hours ago" 2>/dev/null

# Recent file changes
git diff --stat HEAD~5 2>/dev/null | head -20

# Research produced
ls -lt .agents/research/*.md 2>/dev/null | head -3

# Plans created
ls -lt .agents/plans/*.md 2>/dev/null | head -3

# Issues closed
bd list --status closed --since "2 hours ago" 2>/dev/null | head -5
```

### Step 4: Identify Pause Point

Determine where we stopped:

1. **What was the last thing done?**
2. **What was about to happen next?**
3. **Were we mid-task or between tasks?**
4. **Any blockers or decisions pending?**

Check for in-progress work:
```bash
bd list --status in_progress 2>/dev/null | head -5
```

### Step 5: Identify Key Files to Read

List files the next session should read first:
- Recently modified files (core changes)
- Research/plan artifacts (context)
- Any files mentioned in pending issues

```bash
# Recently modified
git diff --name-only HEAD~5 2>/dev/null | head -10

# Key artifacts
ls .agents/research/*.md .agents/plans/*.md 2>/dev/null | tail -5
```

### Step 6: Write Handoff Document

**Write to:** `.agents/handoff/YYYY-MM-DD-<topic-slug>.md`

```markdown
# Handoff: <Topic>

**Date:** YYYY-MM-DD
**Session:** <brief session description>
**Status:** <Paused mid-task | Between tasks | Blocked on X>

---

## What We Accomplished This Session

### 1. <Accomplishment 1>

<Brief description with file:line citations>

**Files changed:**
- `path/to/file.py` - Description

### 2. <Accomplishment 2>

...

---

## Where We Paused

<Clear description of pause point>

**Last action:** <what was just done>
**Next action:** <what should happen next>
**Blockers (if any):** <anything blocking progress>

---

## Context to Gather for Next Session

1. <Context item 1> - <why needed>
2. <Context item 2> - <why needed>

---

## Questions to Answer

1. <Open question needing decision>
2. <Clarification needed>

---

## Files to Read

```
# Priority files (read first)
path/to/critical-file.py
.agents/research/YYYY-MM-DD-topic.md

# Secondary files (for context)
path/to/related-file.py
```

### Step 7: Write Continuation Prompt

**Write to:** `.agents/handoff/YYYY-MM-DD-<topic-slug>-prompt.md`

```markdown
# Continuation Prompt for New Session

Copy/paste this to start the next session:

---

## Context

<2-3 sentences describing the work and where we paused>

## Read First

1. The handoff doc: `.agents/handoff/YYYY-MM-DD-<topic-slug>.md`
2. <Other critical files>

## What I Need Help With

<Clear statement of what the next session should accomplish>

## Key Files

```
<list of paths to read>
```

## Open Questions

1. <Question 1>
2. <Question 2>

---

<Suggested skill to invoke, e.g., "Use /implement to continue">
```

### Step 8: Extract Learnings (Optional)

If significant learnings occurred this session, also run retro:

```bash
# Check if retro skill should be invoked
# (if >3 commits or major decisions made)
git log --oneline --since="2 hours ago" 2>/dev/null | wc -l
```

**If ≥3 commits:** Suggest running `/retro` to extract learnings.
**If <3 commits:** Handoff alone is sufficient; learnings are likely minimal.

### Step 9: Report to User

Tell the user:
1. Handoff document location
2. Continuation prompt location
3. Summary of what was captured
4. Suggestion: Copy the continuation prompt for next session
5. If learnings detected, suggest `/retro`

**Output completion marker:**
```
<promise>DONE</promise>
```

If no context to capture (no commits, no changes):
```
<promise>EMPTY</promise>
Reason: No session activity found to hand off
```

## Example Output

```
Handoff created:
  .agents/handoff/2026-01-31-auth-refactor.md
  .agents/handoff/2026-01-31-auth-refactor-prompt.md

Session captured:
- 5 commits, 12 files changed
- Paused: mid-implementation of OAuth flow
- Next: Complete token refresh logic

To continue: Copy the prompt from auth-refactor-prompt.md

<promise>DONE</promise>
```

## Key Rules

- **Capture state, not just summary** - next session needs to pick up exactly where we left off
- **Identify blockers clearly** - don't leave the next session guessing
- **List files explicitly** - paths, not descriptions
- **Write the continuation prompt** - make resumption effortless
- **Cite everything** - file:line for all references

## Integration with /retro

Handoff captures *state* for continuation.
Retro captures *learnings* for the flywheel.

For a clean session end:
```bash
/handoff  # Capture state for continuation
/retro    # Extract learnings for future
```

Both should be run when ending a productive session.

## Without ao CLI

If ao CLI not available:
1. Skip the `ao ratchet status` check in Step 2
2. Step 8 retro suggestion still works (uses git commit count)
3. All handoff documents are still written to `.agents/handoff/`
4. Knowledge is captured for future sessions via handoff, just not indexed
