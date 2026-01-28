---
name: multi-agent-coordination
description: Synchronize work between Antigravity and Claude Code agents
allowed_tools:
  - git
  - Read
  - Write
  - Edit
denied_patterns:
  - rm
  - del
  - Remove-Item
---

# Multi-Agent Coordination Skill

Use this skill to keep work synchronized between Antigravity and Claude Code.

## When to Use

- Starting a new session (check current handoff state)
- Completing a task (update status and next steps)
- Switching agents (write handoff note)
- Logging significant decisions or actions

## Coordination File

- **Template** (public): `multi_agent_coord.template.md`
- **Working file** (local): `docs/MULTI_AGENT_COORD.md`

The working file is gitignored. It contains sensitive task context that should not be public.

## Session Start Protocol

1. Read the working coordination file
2. Check `git status` for any conflicts
3. Note the current handoff state
4. If another agent was active, acknowledge the handoff

## Handoff Protocol

When ending a session or switching agents, update the working file:

```markdown
## Current Handoff State

**Last Updated**: [YYYY-MM-DD HH:MM TZ]
**Active Agent**: [Your agent name]
**Status**: [What you just completed]
**Next Steps**: [What the next agent should do]
**Blockers**: [Any issues or "None"]
```

## Task Queue Management

Add tasks with priority:
```markdown
| Priority | Task | Assigned To | Status |
|----------|------|-------------|--------|
| 1 | [High priority task] | Claude Code | in_progress |
| 2 | [Medium priority task] | Antigravity | pending |
```

## Session Logging

Log significant actions:
```markdown
| Date | Agent | Action | Outcome |
|------|-------|--------|---------|
| 2026-01-10 | Claude Code | Refactored auth module | Complete |
```

## Conflict Resolution

If `git status` shows changes from both agents:
1. Do NOT overwrite the other agent's work
2. Run `git stash` to save your changes
3. Report the conflict to Rob
4. Wait for resolution before continuing

## One Owner Rule

Only ONE agent should edit the coordination file per session. If you see recent edits from the other agent, read but don't write until handoff is complete.
