---
name: session-handoff
description: Prepare context for new conversations when session is lost or ending. Creates handoff documents that capture current state, progress, and next steps for seamless continuation.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Glob, Grep]
best_practices:
  - Create handoff before long sessions end
  - Include concrete next steps, not vague descriptions
  - Reference specific files and line numbers
  - Capture decisions made and rationale
  - Store handoffs in persistent memory location
error_handling: graceful
streaming: supported
---

<identity>
Session Handoff Specialist - Creates comprehensive context documents for seamless conversation continuity.
</identity>

<capabilities>
- Capturing current session state and progress
- Documenting decisions made and their rationale
- Creating actionable next steps
- Preserving context for future sessions
- Generating resumable task descriptions
</capabilities>

<instructions>

## When to Use

Invoke this skill:

- Before ending a long work session
- When user explicitly asks to prepare for continuation
- When context window is filling up
- Before switching to a different task
- When work is blocked and will resume later

## Handoff Document Workflow

### Step 1: Assess Current State

Gather information about the current session:

1. **What was the original goal?**
2. **What has been accomplished?**
3. **What is in progress?**
4. **What is blocked or pending?**

### Step 2: Document Progress

Create a progress summary:

```markdown
## Session Progress

### Original Goal

[What was requested]

### Completed

- [x] Task 1 - Description
- [x] Task 2 - Description

### In Progress

- [ ] Task 3 - Description (current state: ...)

### Not Started

- [ ] Task 4 - Description
- [ ] Task 5 - Description
```

### Step 3: Capture Context

Document important context that would be lost:

```markdown
## Important Context

### Decisions Made

| Decision        | Rationale       | Alternatives Considered          |
| --------------- | --------------- | -------------------------------- |
| Used approach A | Because X, Y, Z | Approach B (rejected because...) |

### Key Files

| File               | Relevance  | State                   |
| ------------------ | ---------- | ----------------------- |
| `src/auth.ts`      | Main focus | Modified, needs testing |
| `src/auth.test.ts` | Tests      | Partially updated       |

### Discoveries

- Found that X depends on Y
- The config in `.env` requires Z
- Performance bottleneck in function W

### Blockers

- Waiting for: [API credentials / user decision / review]
- Issue: [Description of blocking problem]
```

### Step 4: Create Next Steps

Write concrete, actionable next steps:

```markdown
## Next Steps (In Order)

### Immediate (Must Do First)

1. **Finish auth refactor**
   - File: `src/auth.ts`
   - Remaining: Implement token refresh logic (line 145-160)
   - Reference: See decision about JWT expiry above

2. **Add tests**
   - File: `src/auth.test.ts`
   - Add tests for: `refreshToken()`, `validateSession()`

### After That

3. **Update dependent components**
   - Files: `src/middleware/auth.ts`, `src/api/login.ts`
   - What: Update to use new auth interface

### Nice to Have

4. **Documentation**
   - Update README with new auth flow
```

### Step 5: Generate Resume Prompt

Create a prompt that can be used to resume work:

```markdown
## Resume Prompt

Copy this to start the next session:

---

**Continuing previous work on: [Task Name]**

**Context**: I was working on [brief description].

**Progress so far**:

- Completed: [list]
- In progress: [current state]

**Handoff document**: `.claude/context/memory/handoff-[date].md`

**Immediate next step**: [Specific action to take]

Please read the handoff document and continue from where we left off.

---
```

### Step 6: Save to Persistent Location

Save the handoff document:

```
Location: .claude/context/memory/handoff-YYYY-MM-DD-[task].md
```

## Handoff Document Template

```markdown
# Session Handoff: [Task Name]

**Date**: YYYY-MM-DD HH:MM
**Session Duration**: ~X hours

## Summary

[One paragraph describing what this session was about]

## Original Goal

[What was requested]

## Progress

### Completed

- [x] [Task with details]

### In Progress

- [ ] [Task] - Current state: [description]

### Not Started

- [ ] [Task]

## Important Context

### Decisions Made

1. **[Decision]**: [Rationale]

### Key Files Modified

- `path/to/file.ts` - [What was changed]

### Discoveries & Notes

- [Important finding]

### Blockers

- [Blocker if any]

## Next Steps

### Immediate

1. [Concrete action with file/line references]

### After That

2. [Next action]

## Resume Instructions

To continue this work:

1. Read this handoff document
2. Check status of files mentioned above
3. Start with: [First concrete action]

## Files to Read First

- `.claude/context/memory/learnings.md` - Project knowledge
- `[key file]` - Current implementation
```

</instructions>

<examples>
<usage_example>
**User**: "I need to stop for today, prepare a handoff"

**Agent Response**:

```markdown
# Session Handoff: Authentication System Refactor

**Date**: 2024-01-15 17:30
**Session Duration**: ~3 hours

## Summary

Refactoring authentication from custom implementation to NextAuth.js.
Made good progress on the core auth module but tests are incomplete.

## Original Goal

Replace custom JWT auth with NextAuth.js for better security and maintainability.

## Progress

### Completed

- [x] Installed NextAuth.js and dependencies
- [x] Created base configuration (`src/auth.config.ts`)
- [x] Migrated login endpoint to NextAuth
- [x] Updated session type definitions

### In Progress

- [ ] Migrate protected routes - 60% done
  - Completed: `/dashboard`, `/profile`
  - Remaining: `/settings`, `/admin/*`

### Not Started

- [ ] Migrate logout flow
- [ ] Add OAuth providers (Google, GitHub)
- [ ] Update tests

## Important Context

### Decisions Made

1. **Kept custom user table**: Didn't use NextAuth's built-in user model because we have existing user data with custom fields.

2. **JWT strategy over database sessions**: Better for our stateless API architecture.

### Key Files Modified

- `src/auth.config.ts` - New file, NextAuth configuration
- `src/middleware.ts` - Updated to use NextAuth
- `src/app/api/auth/[...nextauth]/route.ts` - NextAuth API route

### Discoveries

- The old `validateToken()` function is still called by 3 API routes that need updating
- Found hardcoded secret in `.env.local` - needs to be rotated

### Blockers

- Need OAuth credentials for Google/GitHub (user to provide)

## Next Steps

### Immediate

1. **Finish protected route migration**
   - File: `src/middleware.ts` line 45-60
   - Add `/settings` and `/admin/*` to protected patterns

2. **Update remaining API routes using old auth**
   - `src/app/api/user/route.ts` line 12
   - `src/app/api/orders/route.ts` line 8
   - `src/app/api/admin/route.ts` line 15

### After That

3. **Write tests for new auth**
   - Create `src/__tests__/auth.test.ts`
   - Test cases: login, logout, session refresh, protected routes

4. **Add OAuth providers** (once credentials provided)

## Resume Instructions

To continue this work:

1. Read this handoff document
2. Run `npm run dev` to verify current state works
3. Start with: Update middleware.ts to protect `/settings` route

## Files to Read First

- `src/auth.config.ts` - Current NextAuth setup
- `src/middleware.ts` - Route protection logic
```

**Saved to**: `.claude/context/memory/handoff-2024-01-15-auth-refactor.md`

When you resume, use this prompt:

> "Continuing auth refactor. Read `.claude/context/memory/handoff-2024-01-15-auth-refactor.md` and continue from step 1 of Next Steps."

</usage_example>
</examples>

<integration>
**Related Skills**:
- `project-onboarding` - Use when starting fresh on unfamiliar code
- `thinking-tools` - Use think-about-whether-you-are-done before handoff
- `summarize-changes` - Include summary in handoff document
</integration>

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern discovered -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
