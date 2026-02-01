---
name: agent-behavior
description: Use at the start of any coding session to establish activity tracking and working patterns. Defines how the agent should document its work and communicate progress.
---

# Agent Behavior

Rules for how the agent operates, tracks work, and communicates during coding sessions.

## Activity Tracking

**Every session must track what was done.**

Log activity to `docs/activity/` using your judgment on hierarchy:

```
docs/activity/
├── 2025-01-15-feature-auth.md      # By date + feature
├── 2025-01-15-bugfix-login.md      # By date + type
└── sessions/
    └── 2025-01-15-session-1.md     # By session
```

### Activity Log Format

```markdown
# [Date] - [Brief Description]

## What Was Done
- Bullet list of changes made
- Files modified
- Decisions made

## Why
- Reasoning behind approach
- Trade-offs considered

## What's Next
- Remaining work
- Known issues
- Questions for human
```

### When to Log

| Situation | Action |
|-----------|--------|
| Starting work | Create/update activity log |
| Completing a task | Summarize what was done |
| Making a decision | Document the reasoning |
| Hitting a blocker | Note the issue and questions |
| Ending session | Final summary of state |

## Working Patterns

### Ask vs. Proceed

| Situation | Action |
|-----------|--------|
| Clear requirements | Proceed |
| Multiple valid approaches | Ask |
| Destructive operation | Ask |
| Unclear scope | Ask |
| Simple fix | Proceed |

### Subagent Usage

Use subagents when:
- Task is independent and parallelizable
- Deep exploration needed without polluting main context
- Multiple files need searching/analysis

Do directly when:
- Simple, quick operation
- Context is already loaded
- Sequential dependency on previous work

### Communication

- **Be concise** - Don't over-explain obvious things
- **Show progress** - Use todo lists for multi-step work
- **Surface blockers early** - Don't spin on problems
- **Summarize at end** - What was done, what's next

## Quality Expectations

Before marking work "done":
- [ ] Code runs without errors
- [ ] Tests pass (if applicable)
- [ ] Activity log updated
- [ ] No obvious issues left unaddressed
