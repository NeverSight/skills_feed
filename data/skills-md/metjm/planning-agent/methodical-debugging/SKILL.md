---
name: methodical-debugging
description: Systematic debugging approach using parallel investigation and test-driven validation. Use when debugging issues, when stuck in a loop of trying different fixes, or when facing complex bugs that resist standard debugging approaches.
---

# Methodical Debugging

Expert debugging specialist that uses parallel investigation and test-driven validation to systematically identify and fix bugs. This approach breaks free from unproductive fix-attempt cycles by casting a wide net of investigation, then using real integration tests to invalidate hypotheses one by one.

## When to Use This Skill

- When you're stuck in a loop trying different fixes that don't work
- When a bug resists standard debugging approaches
- When the root cause is unclear despite multiple investigation attempts
- When you need to systematically rule out possibilities
- When dealing with complex interactions between components

## Core Philosophy

**Stop guessing. Start investigating systematically.**

The typical debugging anti-pattern:
1. Guess what's wrong
2. Try a fix
3. It doesn't work
4. Guess again
5. Repeat until frustrated

The methodical approach:
1. Cast a wide net with parallel investigation
2. Gather evidence from multiple angles
3. Form ranked hypotheses based on evidence
4. Create integration tests to invalidate each hypothesis
5. Let the tests tell you what's actually wrong

## Code Quality Principles

When fixing bugs, maintain the highest code quality standards:

### Strong Types Catch Bugs

Many bugs stem from weak typing. When investigating and fixing:

- Look for String where a domain type should exist
- Look for HashMap<String, Value> where structs should exist
- Consider whether stronger types would have prevented the bug
- Propose type improvements as part of the fix

### Clean Fixes Only

Fixes must be clean, not band-aids:

- **DO**: Fix the root cause, even if it requires significant refactoring
- **DO**: Update all affected code paths
- **DO NOT**: Add special-case handling that works around the bug
- **DO NOT**: Leave the broken code "for backwards compatibility"
- **DO NOT**: Add flags or conditions to switch between old and new behavior
- **DO NOT**: Claim "too risky to change" - proper testing makes changes safe

### Linter Rules - Prevent Recurrence

When fixing a bug, always ask: "Could a linter rule have caught this?"

- **DO**: Identify the class of bugs this represents
- **DO**: Research if a linter rule exists that catches this pattern
- **DO**: Propose enabling the rule (or a custom rule) as part of the fix
- **DO**: Ensure the rule is added to CI/pre-commit hooks

**Examples of bug-to-rule mappings:**
- Off-by-one errors → bounds checking lints
- Null pointer dereference → strict null checks, `unwrap_used` clippy lint
- Resource leaks → `must_use` attributes, leak detection lints
- Concurrency issues → thread safety lints, `Send`/`Sync` enforcement
- SQL injection → parameterized query enforcement lints

A fix is not complete until the linter rule (if applicable) is proposed and configured.

## Phase 1: Parallel Investigation (Use 10 Sub-Agents)

Launch up to 10 sub-agents simultaneously, each investigating a different angle:

### Investigation Angles

1. **Code Path Analysis**
   - Trace the exact code path where the bug manifests
   - Identify all functions, methods, and components involved
   - Look for recent changes in these areas (git blame/log)

2. **State Inspection**
   - Examine state at various points in the execution
   - Look for unexpected state mutations
   - Check for race conditions or timing issues

3. **Dependency Analysis**
   - Review dependencies involved in the bug area
   - Check for version mismatches or known issues
   - Verify dependency configuration

4. **Similar Bugs Search**
   - Search codebase for similar patterns that might have bugs
   - Look for related bug fixes in git history
   - Search issues/PRs for related problems

5. **Library/Framework Investigation**
   - Read library source code for relevant methods
   - Check library documentation for edge cases
   - Search for known issues in the library's issue tracker

6. **Configuration Review**
   - Examine all configuration affecting the bug area
   - Look for environment-specific settings
   - Check for misconfiguration or missing config

7. **Data Flow Analysis**
   - Trace data from source to where the bug manifests
   - Look for data transformation errors
   - Check for null/undefined handling issues

8. **Error Message Analysis**
   - Parse exact error messages and stack traces
   - Search codebase for error origins
   - Look for error handling that might mask root cause

9. **Internet Search**
   - Search for the exact error message
   - Look for similar issues in Stack Overflow, GitHub issues
   - Check framework/library community forums

10. **Edge Case Exploration**
    - Consider unusual inputs or states
    - Think about timing and concurrency issues
    - Consider resource limits (memory, connections, etc.)

### Sub-Agent Instructions Template

For each sub-agent, provide clear focus:

```
Investigate [ANGLE] for the following bug:

Bug description: [DESCRIPTION]
Symptoms: [WHAT'S HAPPENING]
Expected behavior: [WHAT SHOULD HAPPEN]
Context: [RELEVANT CODE PATHS, FILES, ETC.]

Your task:
1. Investigate specifically from the perspective of [ANGLE]
2. Gather concrete evidence (code references, logs, documentation)
3. Form a hypothesis if you find something relevant
4. Rate your confidence (high/medium/low) with reasoning
5. Suggest what integration test could validate or invalidate your hypothesis

Return findings in this format:
- Investigation area: [ANGLE]
- Evidence found: [SPECIFIC FINDINGS WITH FILE AND FUNCTION/TYPE REFERENCES]
- Hypothesis: [WHAT MIGHT BE CAUSING THE BUG]
- Confidence: [HIGH/MEDIUM/LOW] - [REASONING]
- Suggested test: [HOW TO VALIDATE THIS HYPOTHESIS]
```

## Phase 2: Evidence Synthesis

After all sub-agents complete, synthesize findings:

1. **Collect All Hypotheses**
   - Gather hypotheses from all investigation angles
   - Note the confidence level and supporting evidence for each
   - Identify overlapping or reinforcing findings

2. **Rank Hypotheses**
   - Sort by likelihood based on:
     - Confidence of the investigating sub-agent
     - Quality of supporting evidence
     - How well it explains all observed symptoms
     - Consistency with other findings
   - The most likely hypothesis goes first

3. **Document the Investigation**
   - Create a summary of all investigation findings
   - Map relationships between findings
   - Note any angles that found nothing (also useful information)

## Phase 3: Test-Driven Validation Plan

Create a plan to systematically invalidate hypotheses using **integration tests only** (no unit tests).

### Why Real Integration Tests? (No Mocks - Ever)

Mocks are debugging poison. They hide the exact interactions where bugs live.

**Why mocks fail for debugging:**
- Mocks encode assumptions about behavior - bugs often violate those assumptions
- Mocks pass when real systems fail - giving false confidence
- Integration boundaries are where bugs hide - mocks remove those boundaries
- Mocks test your assumptions, not reality

**Real tests reveal truth:**
- Real databases expose connection, query, and transaction issues
- Real APIs expose timeout, retry, and format issues
- Real file systems expose permission, path, and encoding issues
- Real message queues expose ordering, acknowledgment, and failure issues

**Non-negotiable requirements:**
- Use real databases (Postgres, Redis, etc. in containers)
- Use real HTTP calls (to actual services or staging)
- Use real file systems (actual files, not in-memory)
- Use real message queues (actual brokers, not fakes)

**Explicitly forbidden:**
- Mocking libraries (mockito, mockall, unittest.mock, jest.mock)
- Test doubles, fakes, stubs, or spies
- In-memory implementations of external services
- Any abstraction whose sole purpose is testability via mocking

### Test Plan Structure

For each hypothesis, starting with the most likely:

```markdown
### Hypothesis [N]: [DESCRIPTION]

**Confidence:** [HIGH/MEDIUM/LOW]
**Evidence:** [SUMMARY OF SUPPORTING EVIDENCE]

**Integration Test to Invalidate:**

Test Name: `test_[descriptive_name]`

Setup:
- [Required database state]
- [Required service state]
- [Any other prerequisites]

Test Steps:
1. [Action that triggers the suspected bug path]
2. [Verification of expected vs actual behavior]
3. [Cleanup if needed]

Expected Result if Hypothesis is CORRECT:
- [What the test should show]

Expected Result if Hypothesis is WRONG:
- [What the test should show]

How to Proceed:
- If correct: [Next steps to fix]
- If wrong: [Move to next hypothesis]
```

### Test Execution Order

1. Start with the highest-confidence hypothesis
2. Run the integration test
3. If it invalidates the hypothesis, move to the next
4. If it validates the hypothesis, you've found the root cause
5. Continue until root cause is identified

## Phase 4: Execute and Iterate

1. **Run Tests Sequentially**
   - Execute integration tests one at a time
   - Carefully observe results
   - Document what each test revealed

2. **Update Understanding**
   - As tests run, update your understanding
   - Some tests may reveal new investigation angles
   - Be prepared to add new hypotheses

3. **Fix When Found**
   - Once root cause is identified via test
   - Implement the fix
   - Verify with the same integration test
   - Run additional tests to check for regressions

## Output Format

**Note:** All plan sections define ordering and sequencing only. Do not include time estimates, durations, or scheduling information.

Generate debugging analysis in this structure:

```markdown
# Methodical Debugging: [Bug Description]

## Bug Summary
- **Symptoms:** [What's happening]
- **Expected:** [What should happen]
- **Affected areas:** [Files, components, features]

## Investigation Results

### Sub-Agent 1: Code Path Analysis
- **Findings:** [Summary]
- **Evidence:** [File and function/type references]
- **Hypothesis:** [If any]
- **Confidence:** [Level]

### Sub-Agent 2: State Inspection
[...]

### Sub-Agent N: [Angle]
[...]

## Ranked Hypotheses

| Rank | Hypothesis | Confidence | Key Evidence |
|------|------------|------------|--------------|
| 1 | [Most likely] | HIGH | [Brief evidence] |
| 2 | [Second likely] | MEDIUM | [Brief evidence] |
| ... | ... | ... | ... |

## Integration Test Plan

### Test 1: Validate Hypothesis 1
[Full test specification as above]

### Test 2: Validate Hypothesis 2
[Full test specification as above]

[...]

## Execution Log

### Test 1 Results
- **Outcome:** [HYPOTHESIS CONFIRMED / INVALIDATED]
- **Observations:** [What was observed]
- **Next step:** [What to do next]

[Continue for each test executed]

## Resolution

- **Root Cause:** [What was actually wrong]
- **Fix Applied:** [What was changed]
- **Verification:** [How fix was verified]
- **Regression Check:** [Additional tests run]
```

## Constraints

- DO NOT jump to fixes without systematic investigation
- DO NOT use mocks of any kind - only real integration tests with real infrastructure
- DO NOT use unit tests for hypothesis validation - integration tests only
- DO NOT abandon the process when frustrated - trust the methodology
- DO NOT propose "safe" workarounds - fix the actual problem
- DO NOT leave backwards-compatibility code - update all callers
- DO NOT include timelines, schedules, dates, durations, or time estimates in debugging plans.
  Examples to reject: "in two weeks", "Phase 1: Week 1-2", "Q1 delivery", "Sprint 1", "by end of day".
- ALWAYS use sub-agents for parallel investigation
- ALWAYS document findings and reasoning
- ALWAYS start with the most likely hypothesis when testing
- ALWAYS consider if stronger types would prevent the bug class
- ALWAYS propose linter rules that would prevent the bug class from recurring
- Be thorough - a bug that escapes this process will be very hard to find

## Thinking Mode

- Stay disciplined - follow the process even when you think you know the answer
- Be skeptical of "obvious" causes - obvious bugs usually get fixed quickly
- Look for non-obvious interactions and edge cases
- Consider that the bug might be in multiple places
- Remember: the goal is to INVALIDATE hypotheses, not confirm biases
