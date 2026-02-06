---
name: git-bisect-debugging
description: Use when debugging regressions or identifying which commit introduced a bug - provides systematic workflow for git bisect with automated test scripts, manual verification, or hybrid approaches. Can be invoked from systematic-debugging as a debugging technique, or used standalone when you know the issue is historical.
---

# Git Bisect Debugging

## Overview

Systematically identify which commit introduced a bug or regression using git bisect. This skill provides a structured workflow for automated, manual, and hybrid bisect approaches.

**Core principle:** Binary search through commit history to find the exact commit that introduced the issue. Main agent orchestrates, subagents execute verification at each step.

**Announce at start:** "I'm using git-bisect-debugging to find which commit introduced this issue."

## Quick Reference

| Phase | Key Activities | Output |
|-------|---------------|--------|
| **1. Setup & Verification** | Identify good/bad commits, verify clean state | Confirmed commit range |
| **2. Strategy Selection** | Choose automated/manual/hybrid approach | Test script or verification steps |
| **3. Execution** | Run bisect with subagents | First bad commit hash |
| **4. Analysis & Handoff** | Show commit details, analyze root cause | Root cause understanding |

## MANDATORY Requirements

These are **non-negotiable**. No exceptions for time pressure, production incidents, or "simple" cases:

1. **ANNOUNCE skill usage** at start:
   ```
   "I'm using git-bisect-debugging to find which commit introduced this issue."
   ```

2. **CREATE TodoWrite checklist** immediately (before Phase 1):
   - Copy the exact checklist from "The Process" section below
   - Update status as you progress through phases
   - Mark phases complete ONLY when finished

3. **VERIFY safety checks** (Phase 1 - no skipping):
   - Working directory MUST be clean (`git status`)
   - Good commit MUST be verified (actually good)
   - Bad commit MUST be verified (actually bad)
   - If ANY check fails -> abort and fix before proceeding

4. **USE AskUserQuestion** for strategy selection (Phase 2):
   - Present all 3 approaches (automated, manual, hybrid)
   - Don't default to automated without asking
   - User must explicitly choose

5. **LAUNCH subagents** for verification (Phase 3):
   - Main agent: orchestrates git bisect state
   - Subagents: execute verification at each commit (via Task tool)
   - NEVER run verification in main context
   - Each commit tested in isolated subagent

6. **HANDOFF to systematic-debugging** (Phase 4):
   - After finding bad commit, announce handoff
   - Use superpowers:systematic-debugging skill
   - Investigate root cause, not just WHAT changed

## Red Flags - STOP and Follow the Skill

If you catch yourself thinking ANY of these, you're about to violate the skill:

- "User is in a hurry, I'll skip safety checks" -> NO. Run all safety checks.
- "This is simple, no need for TodoWrite" -> NO. Create the checklist.
- "I'll just use automated approach" -> NO. Use AskUserQuestion.
- "I'll run the test in my context" -> NO. Launch subagent.
- "Found the commit, that's enough" -> NO. Handoff to systematic-debugging.
- "Working directory looks clean" -> NO. Run `git status` to verify.
- "I'll verify good/bad commits later" -> NO. Verify BEFORE starting bisect.

**All of these mean: STOP. Follow the 4-phase workflow exactly.**

## The Process

Copy this checklist to track progress:

```
Git Bisect Progress:
- [ ] Phase 1: Setup & Verification (good/bad commits identified)
- [ ] Phase 2: Strategy Selection (approach chosen, script ready)
- [ ] Phase 3: Execution (first bad commit found)
- [ ] Phase 4: Analysis & Handoff (root cause investigation complete)
```

### Phase 1: Setup & Verification

**Purpose:** Ensure git bisect is appropriate and safe to run.

**Steps:**

1. **Verify prerequisites:**
   - Check we're in a git repository
   - Verify working directory is clean (`git status`)
   - If uncommitted changes exist, abort and ask user to commit or stash

2. **Identify commit range:**
   - Ask user for **good commit** (where it worked)
     - Suggestions: last release tag, last passing CI, commit from when it worked
     - Commands to help: `git log --oneline`, `git tag`, `git log --since="last week"`
   - Ask user for **bad commit** (where it's broken)
     - Usually: `HEAD` or a specific commit where issue confirmed
   - Calculate estimated steps: ~log2(commits between good and bad)

3. **Verify the range:**
   - Checkout bad commit and verify issue exists
   - Checkout good commit and verify issue doesn't exist
   - If reversed, offer to swap them
   - Return to original branch/commit

4. **Safety checks:**
   - Warn if range is >1000 commits (ask for confirmation)
   - Verify good commit is ancestor of bad commit
   - Note current branch/commit for cleanup later

**Output:** Confirmed good commit hash, bad commit hash, estimated steps

### Phase 2: Strategy Selection

**Purpose:** Choose the most efficient bisect approach.

**Assessment:** Can we write an automated test script that deterministically identifies good vs bad?

**MANDATORY: Use AskUserQuestion tool** to present these three approaches (do NOT default to automated):

```javascript
AskUserQuestion({
  questions: [{
    question: "Which git bisect approach should we use?",
    header: "Strategy",
    multiSelect: false,
    options: [
      {
        label: "Automated - test script runs automatically",
        description: "Fast, no manual intervention. Best for: test failures, crashes, deterministic behavior. Requires: working test script."
      },
      {
        label: "Manual - you verify each commit",
        description: "Handles subjective issues. Best for: UI/UX changes, complex scenarios. Requires: you can manually check each commit."
      },
      {
        label: "Hybrid - script + manual confirmation",
        description: "Efficient with reliability. Best for: mostly automated but needs judgment. Requires: script for most cases, manual for edge cases."
      }
    ]
  }]
})
```

**Three approaches to present:**

**Approach 1: Automated Bisect**
- **When to use:** Test failure, crash, deterministic behavior
- **How it works:** Script returns exit 0 (good) or 1 (bad), fully automatic
- **Benefits:** Fast, no manual intervention, reproducible
- **Requirements:** Can write a script that runs the test/check

**Approach 2: Manual Bisect**
- **When to use:** UI/UX changes, subjective behavior, complex scenarios
- **How it works:** User verifies at each commit, Claude guides
- **Benefits:** Handles non-deterministic or subjective issues
- **Requirements:** User can manually verify each commit

**Approach 3: Hybrid Bisect**
- **When to use:** Mostly automatable but needs human judgment
- **How it works:** Script narrows range, manual verification for final confirmation
- **Benefits:** Efficiency of automation with reliability of manual check
- **Requirements:** Can automate most checks, manual for edge cases

**If automated or hybrid selected:**

Write test script following this template:

```bash
#!/bin/bash
# Exit codes: 0 = good, 1 = bad, 125 = skip (can't test)

# Setup/build (required for each commit)
npm install --silent 2>/dev/null || exit 125

# Run the actual test
npm test -- path/to/specific-test.js
exit $?
```

**Script guidelines:**
- Make it **deterministic** (no random data, use fixed seeds)
- Make it **fast** (runs ~log2(N) times)
- **Exit codes:** 0 = good, 1 = bad, 125 = skip
- Include build/setup (each commit might need different deps)
- Test ONE specific thing, not entire suite
- Make it **read-only** (no data modification)

**If manual selected:**

Write specific verification steps for subagent:

**Good example:**
```
1. Run `npm start`
2. Open browser to http://localhost:3000
3. Click the "Login" button
4. Check if it redirects to /dashboard
5. Respond 'good' if redirect happens, 'bad' if it doesn't
```

**Bad example:**
```
See if the login works
```

**Output:** Selected approach, test script (if automated/hybrid), or verification steps (if manual)

### Phase 3: Execution

**Architecture:** Main agent orchestrates bisect, subagents verify each commit in isolated context.

**Main agent responsibilities:**
- Manage git bisect state (`start`, `good`, `bad`, `reset`)
- Track progress and communicate remaining steps
- Launch subagents for verification
- Handle errors and cleanup

**Subagent responsibilities:**
- Execute verification in clean context (no bleeding between commits)
- Report result: "good", "bad", or "skip"
- Provide brief reasoning for result

**Execution flow:**

1. **Main agent:** Run `git bisect start <bad> <good>`

2. **Loop until bisect completes:**

   a. Git checks out a commit to test

   b. **Main agent launches subagent** using Task tool:

   **For automated:**
   ```
   Prompt: "Run this test script and report the result:

   <script content>

   Report 'good' if exit code is 0, 'bad' if exit code is 1, 'skip' if exit code is 125.
   Include the output of the script in your response."
   ```

   **For manual:**
   ```
   Prompt: "We're testing commit <hash> (<message>).

   Follow these verification steps:
   <verification steps>

   Report 'good' if the issue doesn't exist, 'bad' if it does exist.
   Explain what you observed."
   ```

   **For hybrid:**
   ```
   Prompt: "Run this test script:

   <script content>

   If exit code is 0 or 1, report that result.
   If exit code is 125 or script is ambiguous, perform manual verification:
   <verification steps>

   Report 'good', 'bad', or 'skip' with explanation."
   ```

   c. **Subagent returns:** Result ("good", "bad", or "skip") with explanation

   d. **Main agent:** Run `git bisect good|bad|skip` based on result

   e. **Main agent:** Update progress
      - Show commit that was tested and result
      - Calculate remaining steps: `git bisect log | grep "# .*step" | tail -1`
      - Example: "Tested commit abc123 (bad). ~4 steps remaining."

   f. Repeat until git bisect identifies first bad commit

3. **Main agent:** Run `git bisect reset` to cleanup

4. **Main agent:** Return to original branch/commit

**Error handling during execution:**

- **Subagent timeout/error:** Allow user to manually mark as "skip"
- **Build failures:** Use `git bisect skip`
- **Too many skips (>5):** Suggest manual investigation, show untestable commits
- **Bisect interrupted:** Ensure `git bisect reset` runs in cleanup

**Output:** First bad commit hash, bisect log showing the path taken

### Phase 4: Analysis & Handoff

**Purpose:** Present findings and analyze root cause.

**Steps:**

1. **Present the identified commit:**
   ```
   Found first bad commit: <hash>

   Author: <author>
   Date: <date>

   <commit message>

   Files changed:
   <list of files from git show --stat>
   ```

2. **Show how to view details:**
   ```
   View full diff: git show <hash>
   View file at that commit: git show <hash>:<file>
   ```

3. **Handoff to root cause analysis:**
   - Announce: "Now that we've found the breaking commit at `<hash>`, I'm using systematic-debugging to analyze why this change caused the issue."
   - Use superpowers:systematic-debugging skill to investigate
   - Focus analysis on the changes in the bad commit
   - Identify the specific line/change that caused the issue
   - Explain WHY it broke (not just WHAT changed)

**Output:** Root cause understanding of why the commit broke functionality

## Safety & Error Handling

### Pre-flight Checks (Phase 1)
- Working directory is clean
- In a git repository
- Good/bad commits exist and are valid
- Good commit is actually good (issue doesn't exist)
- Bad commit is actually bad (issue exists)
- Good is ancestor of bad
- Warn if >1000 commits in range

### During Execution (Phase 3)
- **Subagent fails:** Log error, allow skip or abort
- **Build fails:** Use `git bisect skip`, continue
- **Ambiguous result:** Use `git bisect skip`, max 5 skips
- **Can't determine good/bad:** Ask user for guidance

### Cleanup & Recovery
- **Always** run `git bisect reset` when done (success or failure)
- If interrupted, prompt user to run `git bisect reset`
- Return to original branch/commit
- If bisect is running and skill exits, warn user to cleanup

### Failure Modes
- **Too many skips:** Report untestable commits, suggest narrower range or manual review
- **Good/bad reversed:** Detect pattern (all results opposite), offer to restart with swapped inputs
- **No bad commit found:** Verify bad commit is actually bad, check if issue is environmental

## Best Practices

### Optimizing Commit Range
- **Narrow the range first** if possible:
  - Issue appeared last week? Start from last week, not 6 months ago
  - Use `git log --since="2 weeks ago"` to find starting point
  - Use tags/releases as good commits when possible

### Writing Good Test Scripts
**Do:**
- Test ONE specific thing
- Make it deterministic (fixed seeds, no random data)
- Make it fast (runs log2(N) times)
- Include setup/build in script
- Use proper exit codes (0=good, 1=bad, 125=skip)

**Don't:**
- Run entire test suite (too slow)
- Depend on external state (databases, APIs)
- Use random data or timestamps
- Modify production data

### Manual Verification
**Be specific:**
- "API returns 200 for GET /health"
- "Login button redirects to /dashboard"
- NOT "See if it works"
- NOT "Check if login is broken"

**Give exact steps:**
1. Run server with `npm start`
2. Open browser to http://localhost:3000
3. Click element with id="login-btn"
4. Verify URL changes to /dashboard

### Common Patterns

| Issue Type | Recommended Approach | Script/Steps Example |
|------------|---------------------|---------------------|
| Test failure | Automated | `npm test -- failing-test.spec.js` |
| Crash/error | Automated | `node app.js 2>&1 | grep -q ERROR && exit 1 || exit 0` |
| Performance | Automated | `time npm run benchmark \| awk '{if ($1 > 5.0) exit 1}'` |
| UI/UX change | Manual | "Click X, verify Y appears" |
| Behavior change | Manual or Hybrid | Script to check, manual to confirm subjective aspects |

### Progress Communication
- After each step: "Tested commit abc123 (<result>). ~X steps remaining."
- Show bisect log periodically: `git bisect log`
- Estimate remaining steps: log2(commits in range)
- Example: 100 commits -> ~7 steps, 1000 commits -> ~10 steps

## Common Rationalizations (Resist These!)

| Rationalization | Reality | What to Do Instead |
|----------------|---------|-------------------|
| "User is in a hurry, skip safety checks" | Broken bisect from dirty state wastes MORE time | Run all Phase 1 checks. Always. |
| "This is simple, no need for TodoWrite" | You'll skip phases without tracking | Create checklist immediately |
| "I'll just use automated approach" | User might prefer manual for vague issues | Use AskUserQuestion tool |
| "I'll run the test in my context" | Context bleeding between commits breaks bisect | Launch subagent for each verification |
| "Working directory looks clean" | Assumptions cause failures | Run `git status` to verify |
| "I'll verify good/bad commits later" | Starting with wrong good/bad wastes all steps | Verify BEFORE `git bisect start` |
| "Found the commit, user knows why" | User asked to FIND it, not debug it | Hand off to systematic-debugging |
| "Production incident, no time for process" | Skipping process in incidents causes MORE incidents | Follow workflow. It's faster. |
| "I remember from baseline, no need to test" | Skills evolve, baseline was different session | Test at each commit with subagent |

**If you catch yourself rationalizing, STOP. Go back to MANDATORY Requirements section.**

## Integration with Other Skills

### Called BY systematic-debugging
When systematic-debugging determines an issue is historical:

```
systematic-debugging detects:
- Issue doesn't exist in commit from 2 weeks ago
- Issue exists now
-> Suggests: "This appears to be a regression. I'm using git-bisect-debugging to find when it was introduced."
-> Invokes: git-bisect-debugging skill
-> Returns: First bad commit for analysis
-> Resumes: systematic-debugging analyzes the breaking change
```

### Calls systematic-debugging
In Phase 4, after finding the bad commit:

```
git-bisect-debugging completes:
-> Announces: "Found commit abc123. Using systematic-debugging to analyze root cause."
-> Invokes: superpowers:systematic-debugging
-> Context: "Focus on changes in commit abc123"
-> Goal: Understand WHY the change broke functionality
```

## Limitations (By Design)

This skill focuses on straightforward scenarios. It does NOT handle:

- Complex merge commit issues (would need `--first-parent`)
- Flaky/intermittent test failures (would need statistical approaches)
- Build system failures across many commits (would need advanced skip strategies)

For these scenarios, manual git bisect with user guidance is recommended.

## Example Workflows

### Example 1: Automated Test Failure

```
User: "The login test started failing sometime in the last 50 commits."

Claude: "I'm using git-bisect-debugging to find which commit introduced this issue."

[Phase 1: Setup]
- git status -> clean
- Good commit: v1.2.0 tag (last release)
- Bad commit: HEAD
- Verify: checkout v1.2.0, run test -> passes
- Verify: checkout HEAD, run test -> fails
- Range: 47 commits, ~6 steps estimated

[Phase 2: Strategy Selection]
AskUserQuestion: Which approach?
User selects: Automated

Script created:
#!/bin/bash
npm install --silent 2>/dev/null || exit 125
npm test -- tests/login.spec.js
exit $?

[Phase 3: Execution]
Step 1: Launch subagent for commit abc123
  Subagent: "Test failed. Exit code 1. bad"
  Main: git bisect bad -> ~3 steps remaining

Step 2: Launch subagent for commit def456
  Subagent: "Test passed. Exit code 0. good"
  Main: git bisect good -> ~2 steps remaining

Step 3: Launch subagent for commit ghi789
  Subagent: "Test failed. Exit code 1. bad"
  Main: git bisect bad -> ~1 step remaining

Step 4: Launch subagent for commit jkl012
  Subagent: "Test passed. Exit code 0. good"
  Main: git bisect good

Git bisect identifies: ghi789 is first bad commit

[Phase 4: Analysis]
Found first bad commit: ghi789

Author: John Doe
Date: 2025-11-10

feat: update authentication middleware

Files changed:
  src/auth/middleware.js | 12 ++++---
  tests/login.spec.js    |  3 +-

Using systematic-debugging to analyze why this change broke the test...
[Hands off to systematic-debugging skill]
```

### Example 2: Manual UI Regression

```
User: "The dashboard layout looks wrong, but I'm not sure when it broke."

Claude: "I'm using git-bisect-debugging to find which commit introduced this issue."

[Phase 1: Setup]
- git status -> clean
- Good commit: 2 weeks ago (user remembers it working)
- Bad commit: HEAD
- Range: 89 commits, ~7 steps estimated

[Phase 2: Strategy Selection]
AskUserQuestion: Which approach?
User selects: Manual

Verification steps created:
1. Run `npm run dev`
2. Open browser to http://localhost:3000/dashboard
3. Check if the sidebar and main content are side-by-side
4. Respond 'good' if layout is correct, 'bad' if sidebar overlaps content

[Phase 3: Execution]
Step 1: Checkout commit abc123
  Launch subagent with verification steps
  User verifies: "Layout is correct. good"
  Main: git bisect good -> ~3 steps remaining

Step 2: Checkout commit def456
  Launch subagent with verification steps
  User verifies: "Sidebar overlaps content. bad"
  Main: git bisect bad -> ~2 steps remaining

... continues until first bad commit found

[Phase 4: Analysis]
Found first bad commit: mno345

Author: Jane Smith
Date: 2025-11-08

refactor: migrate to CSS Grid layout

Files changed:
  src/components/Dashboard.css | 25 +++++++++++----------

Using systematic-debugging to analyze the CSS changes...
[Hands off to systematic-debugging skill]
```

### Example 3: Hybrid Performance Regression

```
User: "API response times got slower recently."

Claude: "I'm using git-bisect-debugging to find which commit introduced this issue."

[Phase 1: Setup]
- git status -> clean
- Good commit: last release tag v2.1.0
- Bad commit: HEAD
- Range: 120 commits, ~7 steps estimated

[Phase 2: Strategy Selection]
AskUserQuestion: Which approach?
User selects: Hybrid

Script created:
#!/bin/bash
npm install --silent 2>/dev/null || exit 125

# Run benchmark 3 times, take average
total=0
for i in 1 2 3; do
  time=$(npm run benchmark:api 2>/dev/null | grep "response_time" | awk '{print $2}')
  [ -z "$time" ] && exit 125  # Can't test
  total=$(echo "$total + $time" | bc)
done
avg=$(echo "scale=2; $total / 3" | bc)

# Threshold: 500ms is acceptable
if (( $(echo "$avg > 500" | bc -l) )); then
  exit 1  # bad (too slow)
else
  exit 0  # good (fast enough)
fi

Manual fallback steps:
"If script is ambiguous, manually test API and verify response time is <500ms"

[Phase 3: Execution]
Steps proceed with script automation...
If script returns 125 (can't test), subagent asks user to manually verify

[Phase 4: Analysis]
Found first bad commit: pqr678

Author: Bob Johnson
Date: 2025-11-11

feat: add caching layer for user preferences

Files changed:
  src/api/middleware/cache.js | 45 ++++++++++++++++++++++++++++++++

Using systematic-debugging to analyze the caching implementation...
[Reveals: Cache lookup is synchronous and blocking, causing slowdown]
```

## Troubleshooting

### "Good and bad are reversed"
If early results suggest good/bad are swapped:
- Stop bisect
- Verify issue description is correct
- Swap good/bad commits and restart

### "Too many skips, can't narrow down"
If >5 commits skipped:
- Review skipped commits manually
- Check if builds are broken in that range
- Consider narrowing the range or manual investigation

### "Bisect is stuck/interrupted"
If bisect state is corrupted or interrupted:
```bash
git bisect reset  # Clean up bisect state
git checkout main  # Return to main branch
# Restart bisect with better range/script
```

### "Subagent is taking too long"
- Set reasonable timeout for verification
- If automated: optimize test script
- If manual: simplify verification steps
- Consider marking commit as 'skip'

## Summary

**When to use:** Historical bugs, regressions, "when did this break" questions

**Key strengths:**
- Systematic binary search (efficient)
- Subagent isolation (clean context)
- Automated + manual + hybrid approaches
- Integrates with systematic-debugging

**Remember:**
1. Always verify good is good, bad is bad
2. Keep test scripts deterministic and fast
3. Use subagents for each verification step
4. Clean up with `git bisect reset`
5. Hand off to systematic-debugging for root cause
