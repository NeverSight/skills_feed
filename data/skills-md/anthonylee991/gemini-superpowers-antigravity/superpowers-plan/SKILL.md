---
name: superpowers-plan
description: Writes an implementation plan with small steps, exact files to touch, and verification commands. Use before making non-trivial changes.
---

# Planning Skill

## When to use this skill
- any multi-file change
- any change that impacts behavior, data, auth, billing, or production workflows
- any debugging that needs systematic isolation

## Planning rules
- Steps should be **small** (2–10 minutes each).
- Every step must include **verification**.
- Prefer **incremental deliverables** (avoid “big bang” edits).
- Identify **rollback** and **risk controls** early.

## Plan format (use this exact structure)
### Goal
### Assumptions
### Plan
1. Step name
   - Files: `path/to/file.ext`, `...`
   - Change: (1–2 bullets)
   - Verify: (exact commands or checks)
2. ...

### Risks & mitigations
### Rollback plan
