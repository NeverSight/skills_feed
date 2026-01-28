---
name: review
description: Check work and detect drift before committing. A second opinion that catches misalignment early. Use at natural pause points, before PRs, or when something feels off.
---

# /review

A second opinion before committing. Review checks alignment between intent and execution, detects drift, and decides: continue, adjust, or salvage.

This is part of the **Intent > Execution > Review** loop that runs at every scale--from a single commit to a multi-week project. Review closes the loop.

## When to Use

Invoke `/review` when:

- **Before committing** - natural checkpoint before code hits the branch
- **At natural pause points** - end of a work session, end of a subtask
- **Something feels off** - you've been coding a while and lost track of where you are
- **Scope seems to have grown** - the task feels bigger than when you started
- **Before PRs** - final check before requesting review from humans

**Do not use when:** You're in deep flow and making progress. Don't interrupt productive work. Review at natural breaks, not arbitrary intervals.

## The Review Process

### Step 1: State the Original Aim

Before reviewing anything, restate what we set out to do:

> "The aim was: [original intent in one sentence]"

If you can't state the aim clearly, that's the first finding. Go find it or clarify with the user before proceeding.

### Step 2: Check Alignment (Five Questions)

Work through these checks against the original aim:

#### 1. Still Necessary?

Is this solving a real, current problem--not a hypothetical future one?

- Are we building something that's actually needed right now?
- Or did scope expand to "future flexibility" or premature optimization?

> If unnecessary work crept in: "This adds [X] which wasn't part of the original aim."

#### 2. Still Aligned?

Is the work still pointed at the original aim?

- Does what we're building actually address the stated problem?
- Are we on the critical path, or did we drift to tangents?

Signs of drift:
- "While I'm at it..."
- Refactoring unrelated code
- Solving problems the user didn't mention

> If misaligned: "The aim was X, but current work addresses Y."

#### 3. Still Sufficient?

Is the approach appropriately sized for the problem?

- Could this be done with less code, fewer files, less abstraction?
- Are we building infrastructure for a one-off task?

Complexity signals:
- RED: 3+ files for simple feature; new patterns for one-offs
- YELLOW: proliferating Manager/Handler/Service classes
- GREEN: direct solution; one file when possible; reuses existing patterns

> If over-complex: "A simpler approach would work. Consider [alternative]."

#### 4. Mechanism Clear?

Can you articulate WHY this approach works?

- Is there a clear "because" statement?
- If the mechanism can't be stated simply, the problem may not be understood

> If unclear: "What's the mechanism? Why will this solve the problem?"

#### 5. Changes Complete?

Are all ripple effects handled?

- New fields initialized everywhere the struct is created?
- Persistence changes have migration paths?
- Contract changes updated in all callers?

> If incomplete: "This adds [X] but doesn't update [related site]."

### Step 3: Detect Drift

Drift is the gap between where you started and where you are. Explicitly name any drift found:

**Scope Drift** - The task grew beyond original boundaries
**Solution Drift** - The approach changed from what was planned
**Goal Drift** - The aim itself shifted without explicit decision

For each drift detected:
```
Drift: [type]
Started as: [original]
Became: [current]
Impact: [what this means]
```

### Step 4: Decide Next Action

Based on the review, choose one:

| Decision | When | Action |
|----------|------|--------|
| **Continue** | Aligned, on track | Proceed with confidence |
| **Adjust** | Minor drift, recoverable | Correct course and continue |
| **Pause** | Unclear aim or major questions | Stop, clarify with user, then resume |
| **Salvage** | Significant drift, restart needed | Extract learning with `/salvage`, then restart |

## Output Format

```
## Review Summary

**Aim:** [original intent]
**Status:** [Continue / Adjust / Pause / Salvage]

### Alignment Check
- Necessary: [Yes/No - brief note]
- Aligned: [Yes/No - brief note]
- Sufficient: [Yes/No - brief note]
- Mechanism clear: [Yes/No - brief note]
- Changes complete: [Yes/No - brief note]

### Drift Detected
[List any drift found, or "None detected"]

### Decision
[Reasoning for the status decision]

### Next Steps
[Concrete actions to take]
```

## Examples

### Example 1: Clean Review (Continue)

```
/review

I've been working on the auth endpoint for 30 minutes.
```

**Output:**
```
## Review Summary

**Aim:** Add JWT validation to the /api/users endpoint
**Status:** Continue

### Alignment Check
- Necessary: Yes - endpoint currently accepts any request
- Aligned: Yes - implementing exactly what was specified
- Sufficient: Yes - using existing auth middleware, minimal new code
- Mechanism clear: Yes - middleware validates token, rejects invalid
- Changes complete: Yes - endpoint updated, tests added

### Drift Detected
None detected

### Decision
Work is aligned and on track. JWT validation implemented using existing patterns.

### Next Steps
1. Run tests
2. Commit
3. Open PR
```

### Example 2: Drift Detected (Adjust)

```
/review

Started adding error handling to the API. Now I'm refactoring the logger.
```

**Output:**
```
## Review Summary

**Aim:** Improve error handling in /api/orders endpoint
**Status:** Adjust

### Alignment Check
- Necessary: Partially - error handling yes, logger refactor no
- Aligned: Drifted - logger refactor wasn't part of the aim
- Sufficient: Over-scoped - touching infrastructure for a single endpoint
- Mechanism clear: Yes for error handling, unclear for logger
- Changes complete: No - error handling incomplete

### Drift Detected
Drift: Scope Drift
Started as: Add try/catch and proper error responses to /api/orders
Became: Refactoring the entire logging system
Impact: Original task incomplete, unrelated system being modified

### Decision
Revert logger changes. Complete the original error handling task. If logger needs work, that's a separate task.

### Next Steps
1. `git stash` the logger changes
2. Complete error handling for /api/orders
3. Commit that work
4. If logger refactor is still needed, create separate task
```

### Example 3: Major Drift (Salvage)

```
/review

Third attempt at fixing the build. Each fix breaks something else.
```

**Output:**
```
## Review Summary

**Aim:** Fix failing CI build (test timeout issue)
**Status:** Salvage

### Alignment Check
- Necessary: Yes - build must pass
- Aligned: No - now touching unrelated config
- Sufficient: No - complexity increasing with each fix
- Mechanism clear: No - unclear why tests timeout
- Changes complete: No - in unstable state

### Drift Detected
Drift: Solution Drift
Started as: Increase test timeout
Became: Modifying test infrastructure, CI config, and mock setup
Impact: Build in worse state than when started, root cause unknown

### Decision
Stop. The approach has reversed multiple times. Extract what was learned about the test infrastructure and restart with better understanding.

### Next Steps
1. Run `/salvage` to capture learnings
2. Revert to known-good state
3. Investigate root cause before attempting fix
4. Start fresh with clear hypothesis
```

## Session Persistence

When invoked with a session name (`/review <session>`), this skill reads and writes to `.oh/<session>.md`.

**Reading:** Check for existing session file. Read **Aim** (what outcome we wanted), **Problem Statement**, **Solution Space** (approach taken), and **Execute** status. This is essential for detecting drift.

**Writing:** After review, write the assessment:

```markdown
## Review
**Updated:** <timestamp>
**Verdict:** [ALIGNED | DRIFTED | BLOCKED]

[review findings, drift analysis, recommendations]
```

## Adaptive Enhancement

### Base Skill (prompt only)
Works anywhere. Produces review summary based on conversation context. No persistence.

### With .oh/ session file
- Reads `.oh/<session>.md` for aim, constraints, selected solution
- Compares actual work against session aim
- Writes review verdict and findings to the session file

### With git diff
- Compares actual changes against stated aim
- Detects file count, complexity signals
- Identifies incomplete changes

### With .wm/ (working memory)
- Also reads `.wm/dive_context.md`
- Session file and working memory can coexist

### With CI Integration
- Checks if tests pass before marking complete
- Verifies linting, type checking
- Confirms PR checks would pass

### With Open Horizons MCP
- Pulls related past decisions for context
- Logs review outcomes to graph
- Session file serves as local cache

## Completion Gate (Before "Done")

When the user or agent claims work is complete, verify:

1. **PR Intent Clear?** - Can you state what the PR delivers in one sentence?
2. **Changes Reviewed?** - Has the branch diff been reviewed against intent?
3. **CI Passing?** - Have automated checks been run and passed?
4. **Feedback Addressed?** - Have reviewer comments been resolved?

If incomplete:
> "Completion gate: [missing step]. Run the check before marking complete."

## Leads To

After review, typically:
- **Continue** - Proceed to commit, PR, or next task
- **Adjust** - Make corrections, then continue
- **Salvage** - Run `/salvage` to extract learning before restart
- **Clarify** - Return to `/aim` or `/problem-statement` if fundamentals unclear

---

**Remember:** Review is not bureaucracy. It's the moment you catch drift before it compounds. Five minutes of review saves hours of wrong-direction work.
