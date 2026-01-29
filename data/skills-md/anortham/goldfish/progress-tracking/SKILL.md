---
name: progress-tracking
description: Proactively checkpoint work progress at key moments without asking permission. Use when completing tasks, fixing bugs, making discoveries, or reaching milestones. Builds persistent memory across sessions.
allowed-tools: mcp__goldfish__checkpoint, mcp__goldfish__plan, Bash
---

# Progress Tracking Skill

## Purpose
Build persistent memory by **proactively checkpointing** important moments in development. This creates a detailed history that survives crashes, context resets, and time away from the project.

## When to Activate
Checkpoint automatically at these **key moments**:

### 🎯 Task Completion
- Feature implemented and tested
- Bug fixed and verified
- Refactoring completed
- Tests written and passing

### 🔍 Important Discoveries
- Found root cause of a bug
- Identified architecture pattern
- Discovered unexpected behavior
- Located critical code sections

### 📋 Planning Decisions
- Architecture decision made
- Approach selected
- Design pattern chosen
- Trade-offs evaluated

### 🚧 Before Major Changes
- Before large refactoring
- Before risky edits
- Before experimental work
- Before switching context

### ⚡ Milestones
- All tests passing
- Build successful
- First working prototype
- PR ready for review

**DO NOT ask permission to checkpoint** - Just do it when the moment is right.

## Orchestration Steps

### 1. Recognize Checkpoint Moments
Monitor for completion signals:
- "All tests passing"
- "Bug fixed"
- "Feature implemented"
- "Found the issue"
- User says "done", "finished", "working", "fixed", etc.

### 2. Craft Meaningful Description
Good checkpoint descriptions:
- **Specific:** "Fixed JWT expiration timeout in auth middleware"
- **Action-oriented:** "Implemented refresh token rotation"
- **Context-rich:** "Added fuzzy search with 15ms performance"

Bad checkpoint descriptions:
- "Made changes"
- "Updated code"
- "Fixed stuff"

### 3. Add Relevant Tags
Choose 2-4 tags that aid future search:
- **Category:** bug-fix, feature, refactor, test, docs, perf
- **Domain:** auth, api, database, ui, testing
- **Importance:** critical, major, minor, experimental

### 4. Execute Checkpoint
```
Call: checkpoint({
  description: "Implemented JWT refresh token rotation with Redis cache",
  tags: ["feature", "auth", "security"]
})
```

Goldfish auto-captures:
- Timestamp (UTC)
- Git branch and commit
- Changed files
- Workspace context

### 5. Update Plans (If Applicable)
If this checkpoint completes a plan item:
```
Call: plan({
  action: "update",
  id: "auth-redesign",
  content: "[Updated plan with progress...]"
})
```

## Checkpointing Patterns

### Pattern 1: After Test Success
```
[Tests pass]
→ checkpoint({
    description: "Completed payment integration with 100% test coverage",
    tags: ["feature", "payments", "tests"]
  })
```

### Pattern 2: Bug Fix
```
[Bug fixed and verified]
→ checkpoint({
    description: "Fixed race condition in websocket reconnection logic",
    tags: ["bug-fix", "websocket", "critical"]
  })
```

### Pattern 3: Discovery
```
[Found root cause]
→ checkpoint({
    description: "Isolated authentication bug: JWT validation fails with expired refresh tokens",
    tags: ["bug-hunt", "auth", "discovery"]
  })
```

### Pattern 4: Before Risky Change
```
[About to refactor]
→ checkpoint({
    description: "Pre-refactoring checkpoint: auth system working but needs cleanup",
    tags: ["refactor", "auth", "checkpoint"]
  })
```

## Frequency Guidance

**Good checkpoint frequency:**
- Major work: Every 30-60 minutes
- Bug hunting: After each discovery
- TDD: After each green test phase
- Experiments: Before and after

**Too frequent:**
- Every small edit
- Every file save
- Every minor fix

**Too rare:**
- Only at end of day
- Only when asked
- Only when "everything is done"

## Plan Integration

When checkpointing work related to an active plan:

1. **Reference the plan** in tags
2. **Update plan** if milestone reached
3. **Complete plan** if work finished
4. **Create new plan** if discovering larger scope

Example:
```
checkpoint({
  description: "Completed OAuth2 Google provider integration",
  tags: ["feature", "auth", "oauth", "plan:auth-redesign"]
})

plan({
  action: "update",
  id: "auth-redesign",
  content: "...mark OAuth2 integration as complete..."
})
```

## Key Behaviors

### ✅ DO
- Checkpoint proactively without asking
- Write specific, meaningful descriptions
- Tag thoughtfully for future search
- Checkpoint before risky changes
- Update related plans

### ❌ DON'T
- Ask permission to checkpoint
- Use vague descriptions
- Over-checkpoint (every tiny edit)
- Under-checkpoint (only when asked)
- Forget to capture discoveries

## Success Criteria

This skill succeeds when:
- Checkpoints create useful breadcrumbs
- Future recall shows clear work narrative
- Discoveries aren't lost to context resets
- Plan progress is accurately tracked
- Users can reconstruct recent work from checkpoints

## Example Checkpoint Sequence

```
Session: Implementing payment processing

1. checkpoint: "Added Stripe SDK and configured API keys"
   Tags: [setup, payments]

2. checkpoint: "Created PaymentService with charge and refund methods"
   Tags: [feature, payments, architecture]

3. checkpoint: "Wrote comprehensive payment integration tests (8 test cases)"
   Tags: [tests, payments, tdd]

4. checkpoint: "Implemented payment webhook handlers for Stripe events"
   Tags: [feature, payments, webhooks]

5. checkpoint: "All payment tests passing, ready for review"
   Tags: [milestone, payments, tests]
```

This sequence tells a clear story that's valuable during recall.

---

**Remember:** Proactive checkpointing builds memory. Don't wait to be asked. Checkpoint meaningful moments as they happen.
