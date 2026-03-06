---
name: update-dev-docs
description: Update dev docs before session compaction to capture progress. Use before compacting conversation, ending sessions, or switching tasks.
---

# Update Dev Docs

Updates the dev docs to capture current progress before session compaction or ending a session.

## When to use

- Before using `/compact` to compress conversation
- Before ending a long session
- When switching to a different task
- Periodically during very long implementations

## Usage

```
/update-dev-docs [task-name]
```

If task-name is not provided, will look for active tasks in `dev/active/`.

## Instructions

When this command is invoked:

1. **Find active dev docs**:
   - Check `dev/active/` for existing task folders
   - If multiple found and no task-name provided, list them and ask which to update

2. **Update tasks.md**:
   - Sync with current TodoWrite state
   - Mark completed items as done
   - Add any new tasks discovered during implementation
   - Update complexity estimates if needed

3. **Update context.md**:
   - Add newly discovered key files
   - Document any new decisions made
   - Update code patterns if new ones were identified
   - Add any gotchas or lessons learned

4. **Update plan.md** (if needed):
   - Update progress on objectives
   - Note any strategy changes
   - Update risk assessment based on discoveries

5. **Generate session summary**:
   - What was accomplished this session
   - What's next
   - Any blockers or open questions

## Session Summary Template

Add to the end of context.md:

```markdown
## Session Log

### [Date] Session

**Accomplished:**

- Item 1
- Item 2

**Next Steps:**

- Item 1
- Item 2

**Blockers/Questions:**

- Question 1
```

## Notes

- Keep updates concise but informative
- Focus on capturing context that would be lost after compaction
- Include specific file paths and line numbers where relevant
- Document "why" not only "what" for decisions
