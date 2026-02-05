---
name: track-session
description: |
  Track, stop, resume, verify, and save progress on long-running work. Use when asked to "start a work session", "track this work", "save progress", "stop session", "resume work", "continue where we left off", "verify work", "check if we're done", "validate progress", "let's get to work on something big", or when planning multi-phase implementations, complex refactoring, or tasks spanning multiple sessions.
license: MIT
metadata:
  author: Antonin Januska
  version: "3.3.0"
  argument-hint: "[save|resume|verify]"
hooks:
  post_tool_use:
    - Update SESSION_PROGRESS.md after Write/Edit operations
  stop:
    - Verify all plan items are completed before ending
---
# Session Progress

> **🔄 Session tracking activated** - I'll use SESSION_PROGRESS.md to track our work so we can pause and resume anytime.

## Overview

Use SESSION_PROGRESS.md in the project root to track plans and progress. All planned work should be saved to SESSION_PROGRESS.md and updated over time. If the plan changes, update SESSION_PROGRESS.

**Core principle:** Maintain recoverable state so work can pause and resume without losing context.

## Usage Modes

This skill supports four modes via optional arguments:

**No argument (default):** `/track-session`
- Automatically save current session progress to SESSION_PROGRESS.md
- Then immediately resume from that progress and continue work
- Use when you want to create a checkpoint and keep working

**Save only:** `/track-session save`
- Save current session state to SESSION_PROGRESS.md
- Stop and wait for user to continue
- Use when pausing work or reaching a natural stopping point

**Resume only:** `/track-session resume`
- Read existing SESSION_PROGRESS.md
- Load the plan, current status, and failed attempts
- Continue from where work was left off
- Use when starting a new session or returning after a break

**Verify only:** `/track-session verify`
- Read SESSION_PROGRESS.md and verify all work against initial requirements
- Check that completed tasks actually meet their goals
- Validate dependencies are satisfied
- Report gaps, incomplete work, or deviations from plan
- Use when work appears complete or before final delivery

## When to Use

**Always use when:**
- Working on multi-phase implementations
- Planning complex refactoring across multiple files
- Pairing with user on design decisions
- Tasks that might span multiple sessions or context resets
- Long-running debugging sessions with multiple approaches

**Useful for:**
- Feature development with dependencies between tasks
- Large refactoring projects
- Learning new codebases with exploration notes
- Collaborative work sessions with progress tracking

**Avoid when:**
- Quick 1-2 file changes
- Simple bug fixes with obvious solutions
- Read-only exploration without planned changes
- Tasks that complete in under 5 minutes

## When to Update

Update after:
- Completing any checklist item
- Any change in plan
- Any error or failed attempt
- Every 2-3 file modifications
- Before asking user questions

## When to Verify

Run verification:
- Before declaring work complete
- After all planned tasks are checked off
- Before final delivery or handoff
- When returning to work after a long break (verify nothing regressed)
- After major refactoring (verify functionality preserved)
- When user asks "are we done?" or "did we finish everything?"

## Format

```markdown
# Session Progress

## Plan
- [ ] Task 1: Description [dependency: none]
- [x] Task 2: Description [dependency: Task 1]
- [ ] Task 3: Description [dependency: Task 2]

## Current Status
Last updated: [timestamp]
Working on: [current task]
Next: [immediate next step]

## Failed Attempts
- Tried [approach]: Failed because [reason], trying [alternative] instead

## Completed Work
- [timestamp] Task 2: [brief summary of what was done]

## Verification Results
(Added by /track-session verify command)

### ✅ Successfully Verified
- Task/Phase: Evidence of completion and correctness

### ⚠️ Minor Issues Found
- Issue: Description and impact

### ❌ Blocking Issues
- Critical problem: What's broken and why it blocks delivery

### 📋 Recommended Next Steps
1. Specific action to address issues
2. Next action after that
```

## Workflow by Mode

### Mode 1: Save and Resume (Default)

**Command:** `/track-session`

Create/update SESSION_PROGRESS.md with current status, then immediately continue work. Use for checkpoints during active work, before risky changes, or at natural breaking points.

### Mode 2: Save Only

**Command:** `/track-session save`

Save current state to SESSION_PROGRESS.md and stop. Use when ending a work session, pausing work, creating handoff documentation, or before taking a break.

### Mode 3: Resume Only

**Command:** `/track-session resume`

Read SESSION_PROGRESS.md (error if missing), load plan/status/failed attempts, continue from checkpoint. Use when starting new session after break, recovering from context reset, or taking over work.

### Mode 4: Verify Only

**Command:** `/track-session verify`

Validate completed tasks against original requirements. Checks: work actually done, requirements met, dependencies satisfied, no scope gaps. Generates report with ✅ verified, ⚠️ minor issues, ❌ blockers, 📋 next steps. Use before declaring done or delivery.

**See:** [Detailed Verification Guide](./reference/VERIFICATION.md) for full methodology.

## Rules

1. **Never repeat failures** - Log every failed approach with reason
2. **Resume from checkpoint** - Check for existing SESSION_PROGRESS.md at session start
3. **Keep current** - File should always reflect actual state
4. **Be specific** - Include enough detail to resume work after context loss
5. **Verify before declaring done** - Always run `/track-session verify` before claiming work is complete
6. **Verification is not optional** - Checked boxes don't mean work meets requirements; verification does

## Examples

### Example 0: Argument Usage Patterns

<Good>
```bash
# Scenario 1: Starting a big feature
user: "Let's implement user authentication"
assistant: "/track-session"
# Creates SESSION_PROGRESS.md with plan, then starts working immediately

# Scenario 2: Taking a lunch break
user: "Save my progress, I'll be back in an hour"
assistant: "/track-session save"
# Saves current state and stops

# Scenario 3: Coming back from break
user: "I'm back, let's continue"
assistant: "/track-session resume"
# Reads SESSION_PROGRESS.md and continues from checkpoint

# Scenario 4: Creating checkpoint mid-work
assistant: "Completed Phase 2, creating checkpoint before Phase 3"
assistant: "/track-session"
# Updates SESSION_PROGRESS.md with Phase 2 completion, continues to Phase 3

# Scenario 5: Verifying work is complete
user: "Are we done? Did we complete everything?"
assistant: "/track-session verify"
# Reads SESSION_PROGRESS.md, checks all completed tasks against requirements
# Reports: "✅ Phases 1-3 verified. ⚠️ Phase 4 tests not run. Recommend: Run test suite"

# Scenario 6: End of work session verification
assistant: "All tasks appear complete. Let me verify before we finish."
assistant: "/track-session verify"
# Validates all work, generates verification report
```

**Why this is good:** Clear separation of concerns - save for pausing, resume for continuing, no-arg for checkpointing during active work, verify for validation before delivery.
</Good>

<Bad>
```bash
# Always using save even when you want to continue
user: "Let's build authentication"
assistant: "/track-session save"
# Saves and STOPS, now user has to manually ask to resume

# Using resume without a saved session
user: "Start working on the feature"
assistant: "/track-session resume"
# ERROR: No SESSION_PROGRESS.md exists yet

# Marking tasks complete without verification
assistant: "All tasks are checked off, we're done!"
# Never ran verify to confirm work actually meets requirements
```

**Why this is bad:** Using save when you want to continue wastes time. Using resume without prior save fails. Skipping verify means potentially incomplete or incorrect work. Use no-arg mode to save+continue, and always verify before declaring completion.
</Bad>

### Example 1: Complex Feature Implementation

<Good>
```markdown
# Session Progress

## Plan
- [x] Phase 1: Research authentication libraries [dependency: none]
  - Evaluated OAuth.js, Passport.js, Auth0
  - Chose Passport.js for flexibility
- [x] Phase 2: Set up OAuth flow [dependency: Phase 1]
  - Configured Google OAuth provider
  - Added callback routes
- [ ] Phase 3: Add user session management [dependency: Phase 2]
  - Implement Redis session store
  - Add session cleanup job
- [ ] Phase 4: Test authentication flows [dependency: Phase 3]
  - Test login/logout
  - Test session persistence

## Current Status
Last updated: 2025-01-29 14:30
Working on: Phase 3 - Implementing Redis session storage
Next: Add Redis client configuration, then implement session middleware

## Failed Attempts
- Tried in-memory sessions: Failed because sessions not persistent across server restarts, switching to Redis instead
- Attempted express-session default store: Performance issues with concurrent users, Redis solves this

## Completed Work
- 2025-01-29 14:00: Phase 2 completed - OAuth flow working with Google provider
- 2025-01-29 13:30: Phase 1 completed - Selected Passport.js after comparing 3 libraries
```

**Why this is good:** Specific tasks with clear dependencies, documented decisions, failed attempts recorded with reasons, concrete next steps.
</Good>

<Bad>
```markdown
# Session Progress

## Plan
- [ ] Do auth stuff
- [ ] Fix sessions
- [ ] Test it

Working on auth. Tried some things that didn't work.
```

**Why this is bad:** Too vague, no dependencies tracked, no details on what failed or why, impossible to resume without starting over.
</Bad>

### Example 2: Debugging Session

<Good>
```markdown
# Session Progress

## Plan
- [x] Phase 1: Reproduce bug [dependency: none]
- [x] Phase 2: Identify root cause [dependency: Phase 1]
- [ ] Phase 3: Implement fix [dependency: Phase 2]
- [ ] Phase 4: Verify fix with tests [dependency: Phase 3]

## Current Status
Last updated: 2025-01-29 15:00
Working on: Phase 3 - Implementing race condition fix
Next: Add mutex lock around shared resource access in payment processor

## Failed Attempts
- Checked payment API logs: No errors found, bug is client-side
- Added try-catch around payment call: Still crashes, race condition suspected
- Increased timeout values: Made it worse, confirms race condition hypothesis

## Completed Work
- 2025-01-29 14:45: Phase 2 - Root cause identified: race condition in payment state management
- 2025-01-29 14:15: Phase 1 - Bug reproduced consistently with concurrent payment attempts
```

**Why this is good:** Clear progression through debugging phases, failed attempts inform next steps, root cause documented.
</Good>

<Bad>
```markdown
# Session Progress

Debugging payment bug. Tried a few things. Need to fix it.
```

**Why this is bad:** No systematic approach, no record of what was tried, no hypothesis tracking.
</Bad>

### Example 3: Verification Workflow

<Good>
```markdown
# Session Progress

## Plan
- [x] Phase 1: Set up authentication system
- [x] Phase 2: Implement user registration
- [x] Phase 3: Add email verification
- [x] Phase 4: Write tests

## Verification Results
✅ All phases verified with passing tests (23/23)
⚠️ Minor: Email template styling, no rate limiting
📋 Next: Add rate limiting, customize templates
```

**Why this is good:** Verification report shows evidence (test counts, specific issues), separates critical vs. nice-to-have, provides actionable next steps.
</Good>

<Bad>
```markdown
## Plan
- [x] Phase 1: Authentication
- [x] Phase 2: Registration
- [x] Phase 3: Email stuff
- [x] Phase 4: Tests

Everything is done! ✨
```

**Why this is bad:** No verification performed, no evidence work meets requirements, potentially incomplete work.
</Bad>

## Troubleshooting

### Problem: SESSION_PROGRESS.md getting too large (>1000 lines)

**Cause:** Not archiving completed work periodically.

**Solution:**
```bash
# Archive completed phases to separate file
cat SESSION_PROGRESS.md >> SESSION_ARCHIVE_2025-01.md
# Keep only active phases in SESSION_PROGRESS.md
```

Move completed work to archive file monthly or after major milestones.

### Problem: Lost track of what was being worked on

**Cause:** Didn't update "Current Status" before pausing session.

**Solution:**
- Update SESSION_PROGRESS.md before asking user questions
- Update before context resets
- Update every 2-3 file modifications
- Set reminder: "Last updated" timestamp should be recent

### Problem: Can't resume work after long break

**Cause:** Not enough detail in "Next" field.

**Solution:**
Include specific next action with file and function names:
```markdown
Next: Add mutex lock in src/payment/processor.ts:handlePayment()
around lines 45-60 where paymentState is accessed
```

Not just: "Next: Fix the bug"

### Problem: Repeated failed attempts with same approach

**Cause:** Not reading or updating "Failed Attempts" section.

**Solution:**
Before trying new approach:
1. Check "Failed Attempts" section
2. Verify approach is different
3. Document why this attempt should work
4. Add failed attempt immediately when it fails

### Problem: Resume fails with "No SESSION_PROGRESS.md found"

**Cause:** Trying to resume without first saving a session.

**Solution:**
- Use `/track-session` (no argument) to create initial session
- Or use `/track-session save` to create SESSION_PROGRESS.md first
- Resume only works when SESSION_PROGRESS.md already exists

### Problem: Save mode stops work when you wanted to continue

**Cause:** Using `save` argument instead of no argument.

**Solution:**
- Use `/track-session save` ONLY when pausing work
- Use `/track-session` (no arg) to checkpoint and continue
- Default no-arg mode is for active work with checkpoints

### Problem: Unclear which mode to use

**Cause:** Not understanding the difference between modes.

**Solution:**
Quick decision guide:
- **Continuing work?** Use no argument (default)
- **Stopping for a break?** Use `save`
- **Coming back to work?** Use `resume`
- **Think you're done?** Use `verify`

### Problem: Verify reports work incomplete but all tasks are checked

**Cause:** Tasks were marked complete without actually finishing the work, or requirements changed.

**Solution:**
1. Review each flagged item in the verification report
2. Either:
   - Complete the missing work and re-verify, OR
   - Update SESSION_PROGRESS.md if requirements changed
3. Never skip verification - checked boxes don't mean work is actually done

### Problem: Verify mode takes too long

**Cause:** Too many completed tasks to verify at once.

**Solution:**
- Run verify incrementally after each major phase
- Don't wait until the end to verify everything
- Use `/track-session verify` after completing each group of related tasks
- Archive verified phases to SESSION_ARCHIVE.md to reduce scope

### Problem: Verify passes but work still has bugs

**Cause:** Verification wasn't thorough enough (didn't run tests, check edge cases, etc.)

**Solution:**
Verification should include:
- Running test suites (unit, integration, e2e)
- Manual testing of key user flows
- Checking error handling and edge cases
- Validating against original acceptance criteria
- Code review of critical changes

## Integration

**This skill works with:**
- **git-worktree** - Each worktree should have its own SESSION_PROGRESS.md for parallel work tracking
- **All methodology skills** - Track phase completion for TDD, debugging, code review workflows
- **generate-skill** - Use SESSION_PROGRESS.md to track multi-phase skill creation
- **Long-running tasks** - Any task requiring >15 minutes or multiple context resets

**Integration pattern with git-worktree:**
```bash
# Create worktree for feature
git worktree add ../project-feature feature-branch
cd ../project-feature

# Create separate progress tracking
echo "# Session Progress - Feature Branch" > SESSION_PROGRESS.md
# Work on feature with independent progress tracking
```

**Pairs with:**
- Commit workflows - Track progress between commits
- Testing workflows - Track test implementation phases
- Refactoring - Track refactoring phases and rollback points
