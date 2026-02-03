---
name: plan-feature
description: Plan features and complex changes. Use when the user requests a plan/spec, says "detailed plan please", or when changes span multiple files/systems.
---

# Feature Planning

Create concrete, implementation-ready plans for features and complex changes.

DO NOT WRITE CODE during planning. Only explore, analyse, and document.

## Scope

Use this skill when:
- User explicitly requests a plan or says "detailed plan please"
- Changes affect 3+ files or multiple systems
- Multiple valid approaches exist and user input is needed
- Requirements are unclear and discovery is needed
- Architectural decisions are required

Skip planning for:
- Single-file changes with clear requirements
- Obvious bug fixes
- Simple additions with no architectural impact

## Planning workflow

### 1. Discovery
Ask targeted questions to uncover intent. For each question:
- Present 2-3 concrete options with tradeoffs
- Give your recommended option with clear reasoning
- One question at a time; wait for user response

Critical questions:
- What problem are you solving? (user pain point, business goal)
- What should happen? (expected behaviour, success criteria)
- What should NOT happen? (constraints, edge cases to avoid)
- Who is this for? (user type, environment, scale)
- How will you verify it works? (testing approach, validation)

### Speed-to-learning reference
- Use `ship-fast-loop.md` for a lightweight shipping loop and feedback cadence.

### 2. Analysis
Explore the codebase systematically:
- Locate relevant files (use Glob/Grep, document paths with line numbers)
- Map existing patterns (architecture, naming, data flow)
- Identify dependencies (what will be affected by changes)
- Find similar implementations (to maintain consistency)
- Note relevant standards (from `implement-frontend`, `define-architecture`, etc)

Document findings:
- File: `path/to/file.ts:123` - what it does, how it's relevant
- Pattern: existing approach for similar features
- Constraint: technical limitation or requirement

### 3. Planning
Create a concrete, ordered plan with:

**For each change, specify:**
- File path and approximate line number
- Exact function/component/class to modify
- What to add/remove/change (be specific)
- Why this change (how it fits the goal)
- Dependencies (what must happen first)

**Plan structure:**
```
## Goal
[One sentence: what we're building and why]

## Changes

### 1. [Description]
- File: `path/to/file.ts:45`
- Action: Add `functionName()` that does X
- Reasoning: Needed because Y
- Dependencies: None

### 2. [Description]
- File: `path/to/other.ts:89`
- Action: Modify `existingFunction()` to handle Z
- Reasoning: Integrates with change #1
- Dependencies: #1 must complete first

## Validation
- [ ] Tests pass
- [ ] Feature works for case A
- [ ] Edge case B is handled
- [ ] Follows `implement-frontend` (if frontend)
- [ ] No console logs or debug code
```

### 4. Standards reference
Explicitly note which standards apply:
- Frontend changes: reference `implement-frontend`, `audit-ui`
- UI changes: reference `design-ui`
- Motion: reference `ui-animation`
- Backend: reference `define-architecture`
- Typography: reference `audit-ui`

Format: "This plan must follow `implement-frontend` for forms and type safety."

### 5. Validation checklist
Before finalizing, verify the plan includes:
- [ ] Clear goal statement
- [ ] Specific file paths with line numbers
- [ ] Ordered steps (dependencies clear)
- [ ] Acceptance criteria
- [ ] Edge cases considered
- [ ] Relevant skill standards referenced
- [ ] No ambiguous language ("update", "improve", "enhance" without specifics)

## Anti-patterns

Avoid vague plans:
- ❌ "Update the authentication system"
- ✅ "Modify `auth/middleware.ts:34` to add `validateSession()` that checks token expiry"

Avoid missing context:
- ❌ "Add error handling"
- ✅ "Wrap API call in `auth/api.ts:67` with try/catch, show toast on error per `audit-ui`"

Avoid assuming knowledge:
- ❌ "Use the standard pattern"
- ✅ "Follow the existing DAO pattern from `user/dao.ts:12-45` (class-based with explicit types)"

Avoid incomplete acceptance criteria:
- ❌ "Make sure it works"
- ✅ "Verify: (1) form submits on Enter, (2) shows inline errors, (3) disables submit during request"

Avoid ignoring standards:
- ❌ Plan uses `any` types and manual form state
- ✅ Plan enforces `implement-frontend`: no `any`, uses React Hook Form

## Quick checks

Before handing off the plan:
- Can someone implement this without asking questions?
- Are all file paths valid and line numbers approximate?
- Are dependencies between steps clear?
- Are acceptance criteria testable?
- Are relevant skill standards explicitly referenced?
- Is every decision justified (the "why")?

## Output format

Deliver the plan as a formatted markdown document that serves as a complete implementation specification. The implementer should not need to make architectural decisions.
