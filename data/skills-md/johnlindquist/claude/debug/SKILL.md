---
name: debug
description: Unified debugging workflow enforcing root cause protocol. Investigate → Understand → Reason → Fix. Use when debugging bugs, errors, or unexpected behavior.
---

# Debug - Root Cause Debugging Workflow

Complete debugging workflow that enforces root cause analysis: Investigate → Understand → Reason → Fix.

## Overview

Debug combines multiple debugging approaches:
- **Codebase investigation** - Search for relevant code
- **GitHub issues search** - Find known issues and workarounds
- **Multi-framework reasoning** - Apply systematic thinking
- **Fix generation** - Specific recommendations with code

## Prerequisites

```bash
# Gemini CLI for AI analysis
pip install google-generativeai
export GEMINI_API_KEY=your_api_key

# gh CLI for GitHub issue search
brew install gh
gh auth login
```

## Debugging Workflows

### Full Debug (Recommended for Complex Issues)

```bash
# Phase 1: Investigate codebase
rg -l "error pattern" --type ts
rg "relevant_function" -A 10 -B 5

# Phase 2: Search GitHub for known issues
gh search issues "error message" --repo owner/repo --limit 10
gh issue view 123 --repo owner/repo

# Phase 3: Reason about root cause
gemini -m pro -o text -e "" "Given this error and code context, what is the root cause?

Error: [error message]

Code:
\$(cat src/file.ts)

Investigation findings:
- [finding 1]
- [finding 2]

Apply first principles, systematic, and critical thinking frameworks."

# Phase 4: Generate fix
gemini -m pro -o text -e "" "Based on root cause: [cause]

Provide:
1. Specific code fix
2. Before/after code
3. How to verify
4. How to prevent"
```

### Quick Debug (Simple Issues)

```bash
# Skip deep reasoning, focus on investigation + fix
rg "error pattern" --type ts -A 5 -B 5

gemini -m pro -o text -e "" "Debug this quickly:

Problem: [description]
Error: [message]

Code:
\$(cat src/problematic-file.ts)

Give me the root cause and fix in 3 sentences."
```

### Debug with Context (Known Files)

```bash
# When you already know which files are involved
gemini -m pro -o text -e "" "Debug using these files:

Problem: [description]

File 1:
\$(cat src/file1.ts)

File 2:
\$(cat src/file2.ts)

Provide:
1. Root cause
2. Specific fix with line numbers
3. Verification steps"
```

### Comprehensive Diagnosis (Complex Issues)

```bash
# Parallel investigation of multiple sources

# Terminal 1: Codebase search
rg "error" --type ts --stats > /tmp/codebase.txt &

# Terminal 2: GitHub issues
gh search issues "error" --limit 20 > /tmp/github.txt &

# Terminal 3: Git history
git log --oneline --all -S "problematic_function" > /tmp/history.txt &

wait

# Synthesize findings
gemini -m pro -o text -e "" "Synthesize these diagnostic findings:

Codebase:
\$(cat /tmp/codebase.txt)

GitHub Issues:
\$(cat /tmp/github.txt)

Git History:
\$(cat /tmp/history.txt)

Provide unified diagnosis with:
1. Most likely root cause
2. Confidence level
3. Key evidence
4. Differential diagnosis
5. Recommended action"
```

## Root Cause Protocol

**Always follow this hierarchy:**

1. **INVESTIGATE** - Search for evidence first
2. **UNDERSTAND** - Read relevant code
3. **REASON** - Apply systematic thinking
4. **FIX** - Only then propose changes

### Forbidden Shortcuts

| Symptom | BANNED Fix | REQUIRED Fix |
|---------|-----------|--------------|
| Null error | `if (x) { x.y }` | Find why x is null |
| Timeout | Increase timeout | Find what's slow |
| Flaky test | Skip test | Find race condition |
| Type error | `as any` | Fix type hierarchy |

## Investigation Commands

### Codebase Search

```bash
# Find error patterns
rg "throw.*Error" --type ts -A 3

# Find function definitions
rg "function functionName|const functionName" --type ts

# Find usages
rg "functionName\(" --type ts

# Find recent changes
git log --oneline -20 --all -- src/problematic/
git diff HEAD~5 -- src/problematic/
```

### GitHub Issue Search

```bash
# Search issues
gh search issues "error message" --repo owner/repo --state all

# View issue details
gh issue view 123 --repo owner/repo --comments

# Search across multiple repos
for repo in repo1 repo2 repo3; do
  gh search issues "error" --repo owner/$repo --limit 5
done
```

### Log Analysis

```bash
# Find logs first
find . -name "*.log" -type f

# Tail recent logs
tail -100 logs/app.log | grep -i error

# Search logs for patterns
grep -n "ERROR\|WARN" logs/*.log | tail -50
```

## Framework-Based Reasoning

### First Principles

```bash
gemini -m pro -o text -e "" "Apply first principles to this bug:

Problem: [description]

Questions:
1. What is this code supposed to do?
2. What is it actually doing?
3. What assumptions are being made?
4. Which assumption is wrong?"
```

### Systematic Analysis

```bash
gemini -m pro -o text -e "" "Systematically analyze:

Problem: [description]

Walk through:
1. Input → What data enters?
2. Processing → What transformations?
3. State → What state changes?
4. Output → What comes out?
5. Where does expected diverge from actual?"
```

### Critical Thinking

```bash
gemini -m pro -o text -e "" "Challenge assumptions:

Problem: [description]

For each potential cause:
- What evidence supports it?
- What evidence contradicts it?
- What would we expect to see if true?
- Can we rule it out?"
```

## Output Format

A debug session should produce:

```markdown
## ROOT CAUSE
Single sentence identifying the actual cause.

## CONFIDENCE
high | medium | low

## FIX
Specific code changes:
- File: src/file.ts
- Line: 42
- Before: `oldCode()`
- After: `newCode()`

## VERIFICATION
How to verify the fix works:
1. Run test: `npm test -- specific.test.ts`
2. Manual check: [steps]

## PREVENTION
How to prevent this in the future:
- Add validation at boundary
- Add regression test
```

## Best Practices

1. **Logs first** - Read logs before reading code
2. **Evidence required** - No fix without citing specific evidence
3. **One cause** - Find THE root cause, not symptoms
4. **Verify hypothesis** - Test your theory before fixing
5. **Prevent recurrence** - Add tests for the failure mode
6. **Document findings** - Capture what you learned
