---
name: healtests
description: Iteratively fix test failures until all tests pass. Use when tests are failing and you want Claude to automatically plan and fix them in a loop.
disable-model-invocation: true
---

# Heal Tests Loop

You are in a test-healing loop. Goal: make all tests pass.

## Step 1: Run Tests

```bash
just testq
```

## Step 2: Evaluate Results

**If tests pass**: Report success. The healing loop is complete.

**If tests fail**: Continue to Step 3.

## Step 3: Plan the Fix

1. Analyze the test failure output
2. Enter plan mode using `EnterPlanMode` tool
3. Write your fix plan to the plan file

**CRITICAL**: Your plan file MUST end with this exact section:

```markdown
## Verification (Healing Loop)

This fix is part of a `/healtests` healing loop. After implementing:

1. Run `just testq`
2. If tests pass, the healing loop is complete
3. If tests fail, use `EnterPlanMode` to plan the next fix

The loop continues until all tests pass.
```

This ensures the loop context survives context clearing.
