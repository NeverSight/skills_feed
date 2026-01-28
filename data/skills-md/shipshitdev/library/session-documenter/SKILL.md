---
name: session-documenter
description: Automatically document session work after each task completion. Tracks decisions, file changes, flowcharts, and context for session continuity.
location: project
auto_activate: true
---

# Session Documenter Skill

Automatically document all work, decisions, and context throughout the session for continuity.

## When This Skill Activates

Trigger conditions:

1. When a task from TodoList is marked completed
2. When files are modified/created/deleted
3. When architectural decisions are made
4. When new patterns are established
5. At session end (MANDATORY)

## Critical Rules

### Session File Naming (ONE FILE PER DAY)

```
✅ CORRECT: .agent/SESSIONS/2025-11-15.md
❌ WRONG:   .agent/SESSIONS/2025-11-15-feature-name.md
```

Multiple sessions same day → Same file, Session 1, Session 2, etc.

### Flowcharts (MANDATORY for features)

Include flowchart for:

- New features
- Feature modifications
- Multi-component bug fixes

## Session Entry Structure

1. **Session number and title**
2. **System flow diagram** (mermaid or text)
3. **Affected components** (frontend, backend, data, external)
4. **What was done** (task checklist)
5. **Key decisions** (with rationale)
6. **Files changed**
7. **Mistakes and fixes**
8. **Next steps**

## Related Files to Update

- `.agent/SESSIONS/README.md`
- `.agent/SYSTEM/SUMMARY.md`
- `.agent/TASKS/*/TODO.md`
- `.agent/SYSTEM/ARCHITECTURE.md` (if architectural decisions)

## References

- [Full guide: Phases, automation, validation, examples](references/full-guide.md)
