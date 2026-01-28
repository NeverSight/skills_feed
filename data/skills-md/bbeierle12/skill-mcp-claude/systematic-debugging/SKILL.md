---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes. Implements scientific method for debugging with root cause analysis.
---

# Systematic Debugging

## Core Principle

**Don't guess. Investigate systematically.**

After 3 failed fix attempts, STOP and question the architecture.

## Phase 1: Understand the Problem

### Gather Information
1. What is the expected behavior?
2. What is the actual behavior?
3. When did it start failing?
4. What changed recently?

### Reproduce Consistently
- Create minimal reproduction case
- Document exact steps to reproduce
- Identify if it's deterministic or intermittent

### Check the Obvious First
- Is it plugged in? (Services running, dependencies installed)
- Are you in the right environment?
- Did you save the file?
- Is the cache cleared?

## Phase 2: Root Cause Tracing

### Backward Tracing Technique
1. Where does the bad value appear?
2. What called this with the bad value?
3. Keep tracing up until you find the source
4. **Fix at source, not at symptom**

### Find Working Examples
- Locate similar working code in same codebase
- What works that's similar to what's broken?
- Compare against references

### Identify Differences
- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

## Phase 3: Form Hypothesis

### Scientific Method
1. Form a SINGLE hypothesis
2. Predict what you'd see if hypothesis is true
3. Design a test to verify
4. Run the test
5. If wrong, form new hypothesis based on new data

### Don't Multi-Hypothesis
- One hypothesis at a time
- Test it completely before moving on
- Don't mix debugging approaches

## Phase 4: Implement Fix

### Write Failing Test First
- Test that reproduces the bug
- Test should fail before fix
- Test should pass after fix

### Single Fix at a Time
- ONE change only
- No "while I'm here" improvements
- No bundled refactoring

### Verify Completely
- Original test passes
- No other tests broken
- Issue actually resolved
- Edge cases covered

## Phase 5: If Fix Doesn't Work

### After Each Failed Attempt
1. STOP
2. Count: How many fixes have you tried?
3. If < 3: Return to Phase 1, re-analyze with new information
4. If ≥ 3: STOP and question the architecture

### After 3+ Failed Fixes
Pattern indicating architectural problem:
- Each fix reveals new problems elsewhere
- Fixes require "massive refactoring"
- Each fix creates new symptoms

**STOP and ask:**
- Is this pattern fundamentally sound?
- Is this the right abstraction?
- Should this be redesigned?

## Debugging Tools

### Logging Strategy
```
// Add context to logs
console.log('[ComponentName] methodName:', {
  input,
  state: relevantState,
  timestamp: Date.now()
});
```

### Binary Search Debugging
1. Add log at midpoint of suspect code
2. Determine if bug is before or after
3. Repeat until isolated

### Rubber Duck Debugging
Explain the problem out loud:
- What should happen?
- What actually happens?
- What did I try?
- What assumptions am I making?

## Common Pitfalls

### Avoid These Mistakes
- Changing multiple things at once
- Assuming you know the cause
- Fixing symptoms instead of root cause
- Not verifying the fix actually works
- Not adding regression tests

### Red Flags
- "It works on my machine"
- "It was working yesterday"
- "I didn't change anything"
- "That can't be the problem"
