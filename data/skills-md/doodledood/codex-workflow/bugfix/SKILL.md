---
name: bugfix
description: "Systematic bug investigation and fix workflow. Gathers symptoms, forms hypotheses, investigates root cause, implements fix, and verifies. Use for debugging, fixing errors, or troubleshooting. Triggers: debug, fix bug, troubleshoot, why is this broken."
---

**User request**: $ARGUMENTS

Systematic bug investigation and fix workflow. Follows: Understand → Hypothesize → Investigate → Fix → Verify.

**Investigation log**: `/tmp/bugfix-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md` - external memory for findings.

## Phase 1: Understand the Bug

### 1.1 Create Todo List

```
- [ ] Gather bug symptoms and context
- [ ] Form initial hypotheses
- [ ] (expand as investigation reveals new areas)
- [ ] Implement and verify fix
```

### 1.2 Create Investigation Log

Path: `/tmp/bugfix-{YYYYMMDD-HHMMSS}-{name-kebab-case}.md`

```markdown
# Bug Investigation: {description}
Started: {timestamp}

## Symptoms
(populated below)

## Hypotheses
(populated in Phase 2)

## Investigation Log
(populated during investigation)

## Root Cause
(populated when identified)

## Fix Applied
(populated after fix)
```

### 1.3 Gather Symptoms

If `$ARGUMENTS` contains sufficient context (error message, steps to reproduce, expected vs actual behavior), extract and document in log.

Otherwise, ask user for missing information:

```
Bug Report Details Needed

To investigate effectively, please provide:

1. **What happened?** (Error message, unexpected behavior)
2. **What did you expect?** (Expected behavior)
3. **Steps to reproduce** (If known)
4. **When did it start?** (Recent change, always broken, intermittent)
5. **Environment** (Browser, OS, versions - if relevant)

Provide what you know - I can investigate the rest.
```

Document all symptoms in investigation log immediately.

### 1.4 Locate Relevant Code

Search codebase for:
- Files mentioned in error messages
- Functions/components referenced
- Recent changes (if "started after X" was mentioned)
- Related test files

Update log with located files.

## Phase 2: Form Hypotheses

### 2.1 Generate Hypotheses

Based on symptoms and located code, form 2-4 hypotheses ranked by likelihood:

```markdown
## Hypotheses

### H1: [Most likely] {Description}
- Evidence for: {what supports this}
- Evidence against: {what contradicts}
- Test: {how to verify/falsify}

### H2: {Description}
- Evidence for: {what supports}
- Evidence against: {what contradicts}
- Test: {how to verify/falsify}

### H3: [Least likely] {Description}
...
```

### 2.2 Update Todos

```
- [x] Gather bug symptoms and context
- [ ] Form initial hypotheses
- [ ] Investigate H1: {description}
- [ ] Investigate H2: {description}
- [ ] (expand as investigation reveals new areas)
- [ ] Implement and verify fix
```

## Phase 3: Investigate

### Investigation Loop

For each hypothesis (in likelihood order):

1. Mark todo `in_progress`
2. Read relevant code files fully
3. Trace execution paths
4. Look for conditions that match symptoms
5. **Write findings immediately** to investigation log
6. Update hypothesis status: CONFIRMED | REFUTED | NEEDS MORE DATA
7. If confirmed → proceed to Phase 4
8. If refuted → mark completed, investigate next hypothesis
9. If all refuted → expand hypotheses based on new learnings

### 3.1 Investigation Techniques

| Symptom Type | Investigation Approach |
|--------------|----------------------|
| Error thrown | Read stack trace, trace to origin, check error handlers |
| Wrong output | Trace data flow, check transformations, validate inputs |
| Performance | Profile execution, check loops/recursion, memory patterns |
| Race condition | Check async operations, state mutations, timing |
| Intermittent | Look for external dependencies, caching, timing |

**General techniques:**
- Read error messages and stack traces carefully
- Check logs and debugging output
- Examine data flow and state changes
- Consider environmental factors (OS, versions, config)
- Review recent commits for related changes (`git log --oneline -20`)

### 3.2 Log Format

After each investigation step:

```markdown
### {timestamp} - Investigating H{N}
**Files examined**: {list}
**Findings**: {what discovered}
**Status**: CONFIRMED | REFUTED | NEEDS MORE DATA
**Next**: {what to check next or "proceed to fix"}
```

### 3.3 Root Cause Identified

When root cause is found:

```markdown
## Root Cause

**Hypothesis confirmed**: H{N}
**Location**: {file}:{line}
**Cause**: {clear explanation}
**Evidence**: {code showing the bug}
```

If no hypothesis was confirmed but investigation revealed the actual cause, document the unexpected finding and proceed.

## Phase 4: Test-First (When Applicable)

Before fixing, create a test that reproduces the bug when practical:

### 4.1 Create Reproducing Test

```
- Find the most appropriate existing test file for the component
- Create a minimal, focused test that reproduces the bug
- Run the test to verify it fails as expected
- If test passes, refine until it properly reproduces the issue
```

**Why test-first?**
- Proves you understand the bug
- Provides automatic verification when fix is applied
- Prevents regression in the future
- Documents the bug behavior

**Skip test-first when:**
- Bug is in UI/visual layer without existing test infrastructure
- Environment-specific issue that can't be unit tested
- Urgent hotfix where manual verification is sufficient (note in log)

### 4.2 Document Test in Log

```markdown
## Reproducing Test

**Test file**: {path}
**Test name**: {description}
**Status**: FAILS AS EXPECTED | SKIPPED (reason)
```

## Phase 5: Fix

### 5.1 Plan the Fix

Before implementing, document:

```markdown
## Planned Fix

**Approach**: {what will change}
**Files to modify**: {list}
**Risk assessment**: {potential side effects}
**Test strategy**: {how to verify}
```

### 5.2 Implement Fix

Apply the minimal fix:
- Change only what's necessary
- Follow existing code patterns
- Don't refactor unrelated code
- Add comments if the fix isn't obvious

### 5.3 Run Quality Gates

```bash
# TypeScript: tsc --noEmit
# Tests: npm test (or project-specific)
# Lint: npm run lint (or project-specific)
```

### 5.4 Handle Gate Failures

If gates fail after fix:
1. Analyze if failure is related to fix or pre-existing
2. If related: adjust fix, re-run gates (max 5 attempts)
3. If pre-existing: note in log, continue
4. If stuck after 5 attempts: escalate with findings

## Phase 6: Verify

### 6.1 Run Reproducing Test

If test was created in Phase 4:
- Run the test that previously failed
- If it passes → fix is verified
- If it still fails → return to Phase 5 to adjust fix

Attempt to reproduce the original bug:
- If bug no longer reproduces → fix likely successful
- If bug still reproduces → fix incomplete, return to Phase 3

### 6.2 Manual Verification

If no reproducing test exists:
- Attempt to reproduce the original bug
- If bug no longer reproduces → fix likely successful
- If bug still reproduces → fix incomplete, return to Phase 3

### 6.3 Check for Regression

Verify the fix didn't break related functionality:
- Run related tests
- Check adjacent code paths
- Consider edge cases

### 6.4 Document Fix

Update investigation log:

```markdown
## Fix Applied

**Files modified**: {list with changes}
**Verification**: {how verified}
**Gates**: PASS | FAIL (reason)

## Summary

**Bug**: {description}
**Root cause**: {explanation}
**Fix**: {what was changed}
**Status**: FIXED | PARTIALLY FIXED | ESCALATED
```

### 6.5 Report to User

```
## Bug Fix Complete

**Bug**: {description}
**Root cause**: {one sentence}
**Fix**: {what was changed}
**Files modified**: {list}
**Verification**: All gates pass, bug no longer reproduces

**Investigation log**: /tmp/bugfix-{...}.md
```

## Edge Cases

| Case | Action |
|------|--------|
| Cannot reproduce bug | Ask user for more details, check environment differences |
| All hypotheses refuted | Form new hypotheses based on learnings, expand investigation |
| Fix would require major refactor | Document scope, escalate to user for decision |
| Multiple bugs discovered | Focus on reported bug, note others in log for later |
| Bug is in third-party code | Document workaround options, escalate |
| Intermittent bug | Add logging/instrumentation to gather more data |

## Principles

- **Write findings immediately** — investigation log is external memory
- **Test-first when possible** — a reproducing test proves understanding
- **One bug at a time** — don't fix unrelated issues
- **Minimal fix** — change only what's necessary
- **Verify thoroughly** — ensure fix works and doesn't regress
- **Escalate when stuck** — don't spin indefinitely

## Quality Standards

- Tests must be deterministic and reliable
- Fixes should be clean and maintainable
- No introduction of new bugs or regressions
- Clear comments explaining non-obvious fixes
- Follow project coding standards and patterns
