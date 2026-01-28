---
name: codify-learning
description: |
  Transform session learnings into permanent, executable improvements.
  Invoke at end of any session that involved debugging, fixing, or learning something.
  Default: Codify everything. Exception: Justify not codifying.
---

# /codify-learning

Transform ephemeral learnings into durable system improvements.

## Philosophy

**Default codify, justify exceptions.** Every correction, feedback, or "I should have known" moment represents a gap in the system. Codification closes that gap.

The "3+ occurrences" threshold is a myth - we have no cross-session memory. If you learned something, codify it.

## Process

### 1. Identify Learnings

Scan the session for:
- Errors encountered and how they were fixed
- PR feedback received
- Debugging insights ("the real problem was...")
- Workflow improvements discovered
- Patterns that should be enforced

### 2. Brainstorm Codification Targets

For each learning, consider:
- **Hook** - Should this be guaranteed/blocked? (most deterministic)
- **Agent** - Should a reviewer catch this pattern?
- **Skill** - Is this a reusable workflow?
- **CLAUDE.md** - Is this philosophy/convention?

Choose the target that provides the most leverage. Hooks > Agents > Skills > CLAUDE.md for enforcement. Skills > CLAUDE.md for workflows.

### 3. Implement

For each codification:
1. Read the target file
2. Add the learning in appropriate format
3. Wire up if needed (hooks need settings.json entry)
4. Verify no duplication

### 4. Report

```
CODIFIED:
- [learning] → [file]: [summary of change]

NOT CODIFIED:
- [learning]: [justification - must be specific]
```

## Anti-Patterns

❌ "No patterns detected" - One occurrence is enough
❌ "First time seeing this" - No cross-session memory exists
❌ "Seems too minor" - Minor issues compound into major friction
❌ "Not sure where to put it" - Brainstorm, ask, don't skip
❌ "Already obvious" - If it wasn't codified, the system didn't know it

See CLAUDE.md "Continuous Learning Philosophy" for valid exceptions and the full codification philosophy.
