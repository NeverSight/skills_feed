---
name: retro
description: 'Extract learnings from completed work. Trigger phrases: "run a retrospective", "extract learnings", "what did we learn", "capture lessons", "create a retro".'
---

# Retro Skill

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Extract learnings from completed work and feed the knowledge flywheel.

## Execution Steps

Given `/retro [topic] [--vibe-results <path>]`:

### Step 1: Identify What to Retrospect

**If vibe results path provided:** Read and incorporate validation findings:
```
Tool: Read
Parameters:
  file_path: <vibe-results-path>
```

This allows post-mortem to pass validation context without re-running vibe.

**If topic provided:** Focus on that specific work.

**If no topic:** Look at recent activity:
```bash
# Recent commits
git log --oneline -10 --since="7 days ago"

# Recent issues closed
bd list --status closed --since "7 days ago" 2>/dev/null | head -5

# Recent research/plans
ls -lt .agents/research/ .agents/plans/ 2>/dev/null | head -5
```

### Step 2: Gather Context

Read relevant artifacts:
- Research documents
- Plan documents
- Commit messages
- Code changes

Use the Read tool and git commands to understand what was done.

### Step 3: Identify Learnings

**If vibe results were provided, incorporate them:**
- Extract learnings from CRITICAL and HIGH findings
- Note patterns that led to issues
- Identify anti-patterns to avoid

Ask these questions:

**What went well?**
- What approaches worked?
- What was faster than expected?
- What should we do again?

**What went wrong?**
- What failed?
- What took longer than expected?
- What would we do differently?
- (Include vibe findings if provided)

**What did we discover?**
- New patterns found
- Codebase quirks learned
- Tool tips discovered
- Debugging insights

### Step 4: Extract Actionable Learnings

For each learning, capture:
- **ID**: L1, L2, L3...
- **Category**: debugging, architecture, process, testing, security
- **What**: The specific insight
- **Why it matters**: Impact on future work
- **Confidence**: high, medium, low

### Step 5: Write Learnings

**Write to:** `.agents/learnings/YYYY-MM-DD-<topic>.md`

```markdown
# Learning: <Short Title>

**ID**: L1
**Category**: <category>
**Confidence**: <high|medium|low>

## What We Learned

<1-2 sentences describing the insight>

## Why It Matters

<1 sentence on impact/value>

## Source

<What work this came from>

---

# Learning: <Next Title>

**ID**: L2
...
```

### Step 6: Write Retro Summary

**Write to:** `.agents/retros/YYYY-MM-DD-<topic>.md`

```markdown
# Retrospective: <Topic>

**Date:** YYYY-MM-DD
**Scope:** <what work was reviewed>

## Summary
<1-2 sentence overview>

## What Went Well
- <thing 1>
- <thing 2>

## What Could Be Improved
- <improvement 1>
- <improvement 2>

## Learnings Extracted
- L1: <brief>
- L2: <brief>

See: `.agents/learnings/YYYY-MM-DD-<topic>.md`

## Action Items
- [ ] <any follow-up needed>
```

### Step 7: Index for Future Discovery (if ao available)

```bash
ao forge index .agents/learnings/YYYY-MM-DD-*.md 2>/dev/null
```

### Step 8: Report to User

Tell the user:
1. Number of learnings extracted
2. Key insights (top 2-3)
3. Location of retro and learnings files
4. Knowledge has been indexed for future sessions

## Key Rules

- **Be specific** - "auth tokens expire" not "learned about auth"
- **Be actionable** - learnings should inform future decisions
- **Cite sources** - reference what work the learning came from
- **Write both files** - retro summary AND detailed learnings
- **Index knowledge** - make it discoverable

## The Flywheel

Learnings feed future research:
```
Work → /retro → .agents/learnings/ → ao forge index → /research finds it
```

Future sessions start smarter because of your retrospective.
