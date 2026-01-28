---
name: stuck
description: Get unstuck when blocked on a problem. Use when you've tried multiple approaches without success, or when debugging has hit a wall.
---

# Stuck Helper

Systematic approaches for getting unstuck on hard problems.

## When to Use

- You've tried multiple approaches without success
- The same error keeps appearing despite fixes
- You don't understand why something isn't working
- Debugging has hit a dead end

## Quick Unstuck

```bash
gemini -m pro -o text -e "" "I'm stuck on this problem:

PROBLEM: [describe what you're trying to do]
TRIED: [what you've already attempted]
ERROR/SYMPTOM: [what's happening]
EXPECTED: [what should happen]

Help me get unstuck. Consider:
1. Am I solving the right problem?
2. What assumptions might be wrong?
3. What haven't I tried?
4. What would an expert check first?"
```

## Structured Debugging

### Rubber Duck Protocol

```bash
gemini -m pro -o text -e "" "I need to rubber duck debug this issue:

I'm trying to: [goal]
The code does: [behavior]
I expected: [expected behavior]
The relevant code is:

\`\`\`
[paste code]
\`\`\`

Walk through the code step by step with me, questioning each assumption."
```

### Assumption Audit

```bash
gemini -m pro -o text -e "" "Audit my assumptions about this problem:

PROBLEM: [description]
MY ASSUMPTIONS:
1. [assumption 1]
2. [assumption 2]
3. [assumption 3]

For each assumption:
- Is it definitely true?
- How would I verify it?
- What if it's wrong?"
```

### Fresh Perspective

```bash
gemini -m pro -o text -e "" "I've been stuck on this for a while. Give me a completely fresh approach:

PROBLEM: [description]
WHAT I'VE TRIED:
- [approach 1]
- [approach 2]
- [approach 3]

Suggest approaches from a different angle. What would someone with no context try?"
```

## Common Stuck Scenarios

### Async/Promise Issues

```bash
gemini -m pro -o text -e "" "Debug this async code issue:

CODE:
\`\`\`
[paste async code]
\`\`\`

SYMPTOM: [what's happening]

Check for:
- Missing await
- Race conditions
- Unhandled rejections
- Callback timing
- Promise chain issues"
```

### State Management

```bash
gemini -m pro -o text -e "" "Debug this state management issue:

FRAMEWORK: [React/Vue/etc]
CODE:
\`\`\`
[paste code]
\`\`\`

SYMPTOM: State not updating / Stale state / Infinite loop

Check for:
- Mutation vs immutable update
- Dependency arrays
- Closure over stale values
- Re-render triggers"
```

### Type Errors

```bash
gemini -m pro -o text -e "" "Help me understand this TypeScript error:

ERROR:
\`\`\`
[paste error]
\`\`\`

CODE:
\`\`\`
[paste code]
\`\`\`

Explain:
1. What the error means in plain English
2. Why TypeScript is complaining
3. How to fix it properly (not just any)"
```

### Build/Config Issues

```bash
gemini -m pro -o text -e "" "Debug this build/config issue:

TOOL: [webpack/vite/esbuild/etc]
ERROR:
\`\`\`
[paste error]
\`\`\`

CONFIG:
\`\`\`
[paste config]
\`\`\`

Common causes and solutions for this type of error."
```

## Escalation Ladder

When simple debugging fails, escalate systematically:

### Level 1: Verify Environment
```bash
# Check versions
node --version
npm --version
# Check dependencies
npm ls
# Clean and reinstall
rm -rf node_modules package-lock.json && npm install
```

### Level 2: Minimal Reproduction
```bash
# Create minimal test case
mkdir /tmp/test-issue
cd /tmp/test-issue
# Create smallest code that reproduces issue
```

### Level 3: Git Bisect
```bash
# Find when it broke
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Test each commit git suggests
```

### Level 4: Search for Similar Issues
```bash
# GitHub issues
gh search issues "[error message]" --limit 10

# With specific repo
gh search issues "[error]" --repo package/repo
```

### Level 5: Ask for Help
```bash
# Prepare a good question
gemini -m pro -o text -e "" "Help me write a good Stack Overflow question for:

PROBLEM: [description]
CODE: [minimal reproduction]
ERROR: [full error]
TRIED: [what I've attempted]

Format as a clear, answerable question."
```

## Prevention Checklist

After getting unstuck, prevent recurrence:

```bash
gemini -m pro -o text -e "" "I just solved this issue:

PROBLEM: [what was wrong]
SOLUTION: [how I fixed it]

Suggest:
1. Test to prevent regression
2. Documentation to add
3. Linting/tooling to catch this earlier
4. Pattern to follow in future"
```

## Best Practices

1. **State the problem clearly** - Writing it out often reveals the issue
2. **List what you've tried** - Prevents repeating failed approaches
3. **Question assumptions** - Often the issue is a wrong assumption
4. **Simplify** - Remove code until you find the minimal case
5. **Take breaks** - Fresh eyes see what tired ones miss
6. **Ask for help early** - Don't spend hours on a 5-minute question
7. **Document the solution** - Future you will thank present you
