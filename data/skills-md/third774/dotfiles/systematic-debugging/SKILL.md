---
name: systematic-debugging
description: Four-phase debugging framework with root cause tracing - understand the source before proposing fixes. Use when investigating bugs, errors, unexpected behavior, or failed tests.
---

# Systematic Debugging

## Overview

Random fixes waste time and create new bugs. Quick patches mask underlying issues.

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

**Violating the letter of this process is violating the spirit of debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## When to Use

Use for ANY technical issue:

- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**

- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**

- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Manager wants it fixed NOW (systematic is faster than thrashing)

## The Four Phases

You MUST complete each phase before proceeding to the next.

Copy this checklist and track your progress:

```
Debugging Progress:
- [ ] Phase 1: Root Cause Investigation
  - [ ] Read error messages carefully
  - [ ] Reproduce consistently
  - [ ] Check recent changes
  - [ ] Gather evidence at component boundaries
  - [ ] Trace data flow backward to source
- [ ] Phase 2: Pattern Analysis
  - [ ] Find working examples
  - [ ] Compare against references
  - [ ] Identify differences
- [ ] Phase 3: Hypothesis and Testing
  - [ ] Form single hypothesis
  - [ ] Test minimally (one change)
  - [ ] Verify before continuing
- [ ] Phase 4: Implementation
  - [ ] Create failing test case
  - [ ] Implement single fix at root cause
  - [ ] Apply defense-in-depth
  - [ ] Remove all // debug-shim markers
  - [ ] Verify fix and tests pass
```

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

#### 1. Read Error Messages Carefully

- Don't skip past errors or warnings
- They often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

#### 2. Reproduce Consistently

- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data, don't guess

#### 3. Check Recent Changes

- What changed that could cause this?
- Git diff, recent commits
- New dependencies, config changes
- Environmental differences

#### 4. Gather Evidence in Multi-Component Systems

**WHEN system has multiple components (CI → build → signing, API → service → database):**

**For log-heavy investigations:** When errors appear in application logs, use the `reading-logs` skill for efficient analysis. Never load entire log files into context - use targeted grep and filtering.

**BEFORE proposing fixes, add diagnostic instrumentation:**

```
For EACH component boundary:
  - Log what data enters component
  - Log what data exits component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify failing component
THEN investigate that specific component
```

**Example (multi-layer system):**

```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3: Signing script
echo "=== Keychain state: ==="
security list-keychains
security find-identity -v

# Layer 4: Actual signing
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

**This reveals:** Which layer fails (secrets → workflow ✓, workflow → build ✗)

#### 5. Trace Data Flow (Root Cause Tracing)

**WHEN error is deep in call stack or unclear where invalid data originated:**

Don't fix symptoms. Trace backward through the call chain to find the original trigger, then fix at the source.

**Use Five Whys + Backward Tracing:**

```
Symptom: git init creates .git in source code directory
Why? → cwd parameter is empty string, defaults to process.cwd()
Why? → projectDir variable passed to git init is ''
Why? → Session.create() received empty tempDir
Why? → Test accessed context.tempDir before beforeEach initialized it
Why? → setupCoreTest() returns object with tempDir: '' initially
Root Cause: Top-level variable initialization accessing uninitialized value
```

**Trace the Call Chain backward:**

```typescript
execFileAsync('git', ['init'], { cwd: projectDir })  // Symptom
  ← WorktreeManager.createSessionWorktree(projectDir, sessionId)
  ← Session.initializeWorkspace()
  ← Session.create(tempDir)
  ← Test: Project.create('name', context.tempDir)  // Root trigger
```

**Adding Instrumentation when call chain is unclear:**

```typescript
async function gitInit(directory: string) {
  // debug-shim
  const stack = new Error().stack;
  console.error("DEBUG:", { directory, cwd: process.cwd(), stack });
  // end debug-shim
  await execFileAsync("git", ["init"], { cwd: directory });
}
```

Key points:
- Use `console.error()` in tests (logger may be suppressed)
- Log before the operation, not after it fails
- Include context: directory, cwd, environment variables

### Debug Instrumentation Markers

**ALL temporary debug code MUST include the `// debug-shim` marker:**

```typescript
console.error("DEBUG:", { value, context }); // debug-shim
```

This enables reliable cleanup via grep. Before completing Phase 4:
1. Search: `grep -r "debug-shim" .`
2. Remove all marked instrumentation
3. Verify tests still pass

For language-specific variants (Python, Bash, JSX), see `references/debugging-techniques.md#debug-shim-markers`.

**Verify the Root Cause:**
- If you fix at the source, does the symptom disappear?
- Does the fix prevent recurrence across all code paths?
- Can you add validation to catch it early?

## Tactical Debugging Techniques

When executing the four phases, use these techniques to gather evidence:

- **Binary Search / Code Bisection**: Systematically narrow down the problem area
- **Minimal Reproduction**: Strip away everything non-essential
- **Strategic Logging & Instrumentation**: Add diagnostic output at key points
- **Runtime Assertions**: Make assumptions explicit and fail fast
- **Differential Analysis**: Compare working vs broken states
- **Multi-Component System Debugging**: Add instrumentation at each boundary

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples**
   - Locate similar working code in same codebase
   - What works that's similar to what's broken?

2. **Compare Against References**
   - If implementing pattern, read reference implementation COMPLETELY
   - Don't skim - read every line
   - Understand the pattern fully before applying

3. **Identify Differences**
   - What's different between working and broken?
   - List every difference, however small
   - Don't assume "that can't matter"

4. **Understand Dependencies**
   - What other components does this need?
   - What settings, config, environment?
   - What assumptions does it make?

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis**
   - State clearly: "I think X is the root cause because Y"
   - Write it down
   - Be specific, not vague

2. **Test Minimally**
   - Make the SMALLEST possible change to test hypothesis
   - One variable at a time
   - Don't fix multiple things at once

3. **Verify Before Continuing**
   - Did it work? Yes → Phase 4
   - Didn't work? Form NEW hypothesis
   - DON'T add more fixes on top

4. **When You Don't Know**
   - Say "I don't understand X"
   - Don't pretend to know
   - Ask for help
   - Research more

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

#### 1. Create Failing Test Case

- Simplest possible reproduction
- Automated test if possible
- One-off test script if no framework
- MUST have before fixing

#### 2. Implement Single Fix

- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

#### 3. Apply Defense-in-Depth

Don't just fix the root cause - add validation at each layer:

1. **Root fix:** Prevent the bug at its source
2. **Layer 1:** Entry point validates inputs
3. **Layer 2:** Core logic validates preconditions
4. **Layer 3:** Environment guards (NODE_ENV checks, directory restrictions)

Result: Bug impossible to reintroduce, even with future code changes.

#### 4. Verify Fix

- Test passes now?
- No other tests broken?
- Issue actually resolved?

#### 5. If Fix Doesn't Work

- STOP
- Count: How many fixes have you tried?
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (step 6 below)**
- DON'T attempt Fix #4 without architectural discussion

#### 6. If 3+ Fixes Failed: Question Architecture

**Pattern indicating architectural problem:**

- Each fix reveals new shared state/coupling/problem in different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**

- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

**Discuss with your human partner before attempting more fixes**

This is NOT a failed hypothesis - this is a wrong architecture.

## Red Flags - STOP and Follow Process

If you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- **"One more fix attempt" (when already tried 2+)**
- **Each fix reveals new problem in different place**

**ALL of these mean: STOP. Return to Phase 1.**

**If 3+ fixes failed:** Question the architecture (see Phase 4.6)

## Partner Signals You're Doing It Wrong

**Watch for these redirections:**

- "Is that not happening?" - You assumed without verifying
- "Will it show us...?" - You should have added evidence gathering
- "Stop guessing" - You're proposing fixes without understanding
- "Ultrathink this" - Question fundamentals, not just symptoms
- "We're stuck?" (frustrated) - Your approach isn't working

**When you see these:** STOP. Return to Phase 1.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|----------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, trace data flow | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix with defense-in-depth, verify | Bug resolved, tests pass |

## Reporting Your Findings

After completing the debugging process:

```markdown
## Root Cause

[Explain the underlying issue in 1-3 sentences]
Located in: `file.ts:123`

## What Was Wrong

[Describe the specific problem - mutation, race condition, missing validation,
incorrect assumption, etc. Be technical and specific.]

## The Fix

[Describe the changes made and why they address the root cause]

Changes in:
- `file.ts:123-125` - [what changed and why]
- `test.ts:45` - [added regression test]

## Verification

- [x] Bug reproduced and confirmed fixed
- [x] Existing tests pass
- [x] Added regression test
- [x] Checked for similar issues in related code
- [x] No new errors or warnings introduced
```

## When Process Reveals "No Root Cause"

If systematic investigation reveals issue is truly environmental, timing-dependent, or external:

1. You've completed the process
2. Document what you investigated
3. Implement appropriate handling (retry, timeout, error message)
4. Add monitoring/logging for future investigation

**But:** 95% of "no root cause" cases are incomplete investigation.

## Integration

**Complementary skills:**
- `writing-tests` - For creating failing test case in Phase 4
- `condition-based-waiting` - Replace arbitrary timeouts identified in Phase 2
- `verification-before-completion` - Verify fix worked before claiming success
- `reading-logs` - Efficient log analysis for evidence gathering in Phases 1-2

## Real-World Impact

From debugging sessions:

- Systematic approach: 15-30 minutes to fix
- Random fixes approach: 2-3 hours of thrashing
- First-time fix rate: 95% vs 40%
- New bugs introduced: Near zero vs common

**Remember:** Fixing symptoms creates technical debt. Finding root causes eliminates entire classes of bugs.
