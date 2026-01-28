---
name: execute
description: Do the work. Pre-flight, build, detect drift, salvage if needed. Use when you have a clear aim and are ready to implement.
---

# /execute

Do the actual work. Execute is the bridge from Solution Space to shipped code. Pre-flight checks, build, detect drift, salvage if needed.

Execute sits within the larger **Intent -> Execution -> Review** loop. This skill handles the Execution phase, which itself contains an inner loop: build, check alignment, course-correct or salvage.

## When to Use

Invoke `/execute` when:

- **Aim is clear** - you know the outcome you're trying to achieve
- **Solution is chosen** - you've explored options and picked an approach
- **Context is loaded** - you understand the constraints and guardrails
- **Ready to build** - not still exploring or discovering

**Do not use when:**
- Aim is unclear - use `/aim` first
- Still exploring options - use `/solution-space` first
- Problem is ambiguous - use `/problem-space` or `/problem-statement` first

## The Execute Process

### Step 1: Pre-flight Check

Before writing code, verify alignment:

```
Pre-flight Checklist:
[ ] Aim is clear - what outcome am I producing?
[ ] Constraints known - what must I NOT break?
[ ] Context loaded - do I have the codebase understanding I need?
[ ] Scope bounded - what am I specifically doing (and NOT doing)?
[ ] Success criteria - how will I know when I'm done?
```

If any box can't be checked, stop and address it before proceeding. Ask clarifying questions if requirements are ambiguous.

> "The task is [task]. The aim is [aim]. I'm specifically doing [scope]. I will NOT be touching [out of scope]. Success looks like [criteria]."

### Step 2: Build

Do the work. Keep it focused.

**Build principles:**
- Work in small, testable increments
- Commit logical units of change
- Stay within the declared scope
- If scope expands, pause and reassess (see Drift Detection)

**During build:**
1. Make the change
2. Verify it works (tests, manual check, whatever's appropriate)
3. Stage changes
4. Run review if available (`sg review` or equivalent)
5. Handle review findings (fix trivial, create tasks for non-trivial)
6. Commit with clear message

### Step 3: Detect Drift

Periodically check alignment during execution:

**Drift signals:**
- Scope is expanding beyond original task
- You're touching files not mentioned in the plan
- "While I'm here" thoughts keep appearing
- Original estimate is significantly exceeded
- Approach has changed direction multiple times
- You're protecting code you've invested in

**When you notice drift:**

```
Drift Check:
- Original aim: [aim]
- What I'm actually doing now: [current work]
- Gap: [describe the divergence]
- Verdict: [aligned | minor drift | significant drift | lost]
```

**Aligned:** Continue building.

**Minor drift:** Note it, continue if still valuable, or refocus.

**Significant drift:** Pause. Either:
- Refocus on original aim and defer the tangent
- Acknowledge scope change and get confirmation
- Salvage and restart

**Lost:** Invoke `/salvage` immediately.

### Step 4: Salvage if Needed

When to stop and salvage:

- Approach has reversed 3+ times
- Scope keeps expanding while "done" keeps fuzzing
- You're oscillating, not converging
- The finish line keeps moving
- Starting over feels right

Don't fight lost work. Extract the learning and restart clean.

> "Code is cheap now. Learning is the asset."

Invoke `/salvage` to extract what you learned before restarting.

## Output Format

When execution completes successfully:

```
## Execution Complete

**Task:** [what was done]
**Aim achieved:** [how it maps to the original aim]

### Changes
- [file/component]: [what changed and why]
- [file/component]: [what changed and why]

### Verification
- [how it was tested/verified]

### Notes
- [anything relevant for future work]
```

When drift triggers a pause:

```
## Execution Paused - Drift Detected

**Original aim:** [aim]
**Current state:** [where things stand]
**Drift:** [what diverged and why]

### Options
1. [option 1]
2. [option 2]
3. Salvage and restart

Recommendation: [your assessment]
```

## Examples

### Example 1: Clean Execution

```
/execute

Task: Add validation for empty strings in user input
```

**Pre-flight:**
```
Pre-flight Checklist:
[x] Aim is clear - prevent empty strings from causing silent failures
[x] Constraints known - don't break existing validation, maintain API compatibility
[x] Context loaded - reviewed input processing flow, found 3 entry points
[x] Scope bounded - only the 3 input handlers, not the downstream processors
[x] Success criteria - empty strings rejected with clear error message
```

**Output:**
```
## Execution Complete

**Task:** Add empty string validation to user input
**Aim achieved:** Empty strings now rejected at entry points with clear error message

### Changes
- handlers/user.go: Added empty string check before processing
- handlers/profile.go: Added empty string check before processing
- handlers/settings.go: Added empty string check before processing
- lib/validation.go: New isEmpty() helper for consistency

### Verification
- Added unit tests for each handler (empty, whitespace-only, valid)
- Manual test: confirmed error message appears in UI

### Notes
- Downstream processors still accept empty strings (out of scope)
- Consider adding validation to API gateway layer in future
```

### Example 2: Drift Detection Mid-Execution

```
/execute

Task: Fix the timezone bug in calendar display
```

**Mid-execution drift check:**
```
Drift Check:
- Original aim: Fix timezone display bug
- What I'm actually doing now: Refactoring the entire date handling library
- Gap: Went from fixing display to rewriting infrastructure
- Verdict: Significant drift
```

**Output:**
```
## Execution Paused - Drift Detected

**Original aim:** Fix timezone bug in calendar display
**Current state:** Found the bug, but discovered date handling is inconsistent across 12 files

**Drift:** Started fixing the display bug, realized the root cause is a design issue.
Fixing it properly requires touching the date library, which affects everything.

### Options
1. Band-aid fix in display layer only (solves symptom, not cause)
2. Refactor date handling (right fix, but 10x scope)
3. Salvage learning, create proper task for date system redesign

Recommendation: Option 3 - the date system needs intentional redesign, not
accidental refactoring during a bug fix. Salvage what we learned, create a
proper design task, apply band-aid for now.
```

### Example 3: Triggering Salvage

```
/execute

Building the new auth flow
```

**After multiple iterations:**
```
## Execution Paused - Salvaging

**Original aim:** Simplify authentication flow
**Current state:** 4th approach attempted, complexity has increased

The approach has reversed multiple times:
1. Started with unified flow -> broke provider-specific handling
2. Switched to provider adapters -> too much duplication
3. Tried abstract base class -> inheritance nightmare
4. Back to unified flow with exceptions -> where we started, but worse

Invoking /salvage to extract learning before restart.
```

## Session Persistence

When invoked with a session name (`/execute <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read **Aim**, **Problem Statement**, **Solution Space** to understand what we're building and why. This is essential for drift detection.

**Writing:** After pre-flight and during execution, write status to the session file:

```markdown
## Execute
**Updated:** <timestamp>
**Status:** [pre-flight | in-progress | drift-detected | complete]

[execution notes, drift observations, etc.]
```

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Manual pre-flight checklist, drift detection by reasoning. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for aim, constraints, selected solution
- Writes execution status and notes to the session file
- Drift detection compares current work against session aim

### With .wm/ (working memory)
- Also reads/writes `.wm/dive_context.md` and `.wm/sessions/`
- Session file and working memory can coexist

### With Open Horizons MCP
- Queries related past decisions and learnings
- Logs execution decisions to graph database
- Session file serves as local cache

### With task management (ba, GitHub issues)
- Creates subtasks for non-trivial findings
- Updates task status as work progresses
- Links commits to tasks

### With code review (sg, CodeRabbit)
- Runs automated review on staged changes
- Triages findings by severity
- Iterates until review passes

## Leads To

After execute, typically:
- `/review` - Verify the work before committing
- `/ship` - Deploy the change to users
- `/salvage` - If drift was detected and restart needed
- Create new tasks for discovered work

---

**Remember:** Execute is the inner loop. Stay focused on the aim. Code is cheap; thrashing is expensive. Detect drift early. Salvage without shame.
