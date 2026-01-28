---
name: ai-native-dev
description: Proactively manage development tasks in TASKS.md. Automatically tracks progress, updates status, prioritizes backlog, and estimates effort. Runs in background during development - no explicit invocation needed.
---

# AI-Native Project Management

**This skill runs automatically.** Update TASKS.md whenever:
- Starting work on a task
- Completing a task or subtask
- Getting blocked
- Planning new work
- Making commits

---

## Task Board Location

Look for `TASKS.md` in the project root. If it doesn't exist and you're doing significant work, create it.

---

## When to Update (Automatic Triggers)

| Event | Action |
|-------|--------|
| Starting a feature/fix | Move task to "In Progress" or create one |
| Committing code | Update progress notes on current task |
| Creating a PR | Move task to "Review" |
| Getting blocked | Move to "Blocked" with clear question |
| Completing work | Move to "Done" with date and PR link |
| User describes new work | Add to Backlog with estimate |
| Session ending | Ensure all in-progress work is captured |

---

## How to Update TASKS.md

### Moving a Task to In Progress
```markdown
## In Progress

- [ ] **TASK-XXX** [Title] `@ai`
  - Branch: `feature/xxx`
  - Progress: [Current status]
  - Next: [What's being done next]
```

### Moving to Review
```markdown
## Review

- [ ] **TASK-XXX** [Title] `@human`
  - PR: #[number]
  - Changes: [Brief summary]
  - Review focus: [What human should check]
```

### Moving to Blocked
```markdown
## Blocked

- [ ] **TASK-XXX** [Title]
  - Blocker: [What's blocking]
  - Question: [Specific question for human]
  - Options: A) ... B) ... C) ...
```

### Moving to Done
```markdown
## Done

- [x] **TASK-XXX** [Title] — PR #[N] — YYYY-MM-DD
```

### Adding New Task
```markdown
## Backlog

### P1 - Current Priority
1. [ ] **TASK-XXX** [Title]
   - Why: [Customer need / problem]
   - Scope: [What's included]
   - Estimate: X AI-hours
```

---

## Effort Estimation

Estimate in **AI-hours** (not human hours). Use this guide:

| Task Type | AI-Hours | Example |
|-----------|----------|---------|
| Trivial | 0.25 | Fix typo, update config |
| Small | 0.5-1 | Bug fix, add field, small UI tweak |
| Medium | 1-2 | New component, API endpoint, feature flag |
| Large | 2-4 | Full feature, integration, refactor |
| XL | 4-8 | Cross-cutting feature, new system |

**Factors that increase estimate:**
- Unfamiliar codebase (+50%)
- No existing patterns to follow (+25%)
- Requires human decisions mid-task (+1-2h for wait time)
- Complex testing requirements (+25%)

---

## Prioritization Rules

When adding to backlog, assign priority:

| Priority | Criteria |
|----------|----------|
| **P1** | Blocking other work, customer-facing bug, current sprint |
| **P2** | Important but not urgent, next sprint |
| **P3** | Nice to have, future consideration |

Within each priority, order by:
1. Dependencies (unblock others first)
2. Customer impact
3. Effort (quick wins before large tasks when equal value)

---

## Task ID Convention

Format: `[PROJECT]-[NUMBER]`

Examples:
- `ACCT-001` for accounting demo
- `PROD-001` for main product
- `SITE-001` for website

Auto-increment by finding highest existing number.

---

## Proactive Behaviors

**At session start:**
- Read TASKS.md to understand current state
- Note any stale "In Progress" items (might need status update)

**During development:**
- When user says "let's work on X" → Create/move task to In Progress
- When committing → Update progress notes
- When hitting a blocker → Move to Blocked immediately
- When PR is ready → Move to Review

**At session end:**
- Ensure TASKS.md reflects current state
- Update "Last Updated" timestamp
- Note any handoff items for next session

**When user describes new work:**
- Immediately add to appropriate priority in Backlog
- Include estimate
- Ask clarifying questions if scope is unclear

---

## Board Health Checks

Periodically verify:
- [ ] No tasks stuck in "In Progress" for multiple sessions
- [ ] "Blocked" items have clear questions
- [ ] Backlog is prioritized (P1 before P2)
- [ ] Done items have dates and PR links
- [ ] Estimates exist for P1 items

---

## Integration with Development

This skill works alongside normal development:

1. **Don't ask permission** to update TASKS.md - just do it
2. **Update incrementally** - small updates as you go, not big batch at end
3. **Keep it current** - the board should reflect reality at all times
4. **Surface blockers immediately** - don't wait to move things to Blocked

---

## Template: New TASKS.md

When creating for a new project:

```markdown
# Tasks

**Project**: [Name]
**Last Updated**: [Today's date]

---

## In Progress

---

## Review

---

## Blocked

---

## Backlog

### P1 - Current Priority

### P2 - Next Up

### P3 - Later

---

## Done

---
```
