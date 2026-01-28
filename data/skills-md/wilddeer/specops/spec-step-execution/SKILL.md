---
name: Spec Step Execution
description: Execute a single step from a spec. Used by spec-step-executor agent and main process when running steps directly.
version: 1.0.0
---

# spec-step-execution

Execute a single step from a spec with zero ambiguity. Report back with clear result.

## Input

Before starting, you need:
- Spec file path
- Step number/name to execute
- Progress file path (if exists) - context on previous steps
- Research file path (if exists) - contains objective, defined terms, findings, decisions

## Process

### 1. Read the Step

Read the spec and locate the exact step to execute. Note:
- Step description
- Expected outcome
- Verification items (if any)

### 2. Gap Test

A gap is any situation where the spec doesn't tell you what to do.

**Check before and during execution:**
- "Could two reasonable people interpret this differently?" → GAP
- "Something unexpected happened that spec doesn't cover" → GAP
- "Prerequisites not met or unavailable" → GAP
- "I need to make a judgment call" → GAP

| Situation | Action |
|-----------|--------|
| Gap detected | Stop and return GAP result immediately |
| No gap | Proceed with execution |

**Gap examples by domain:**

| Domain | Gap (return GAP) | Not a gap (execute) |
|--------|------------------|---------------------|
| Code | "Improve error handling" | "Add try-catch around parseConfig() that logs error and returns null" |
| Code | API returns unexpected 403 error | API returns expected data |
| Testing | "Test the auth flow" | "Run `npm test -- --grep 'auth'` and verify all pass" |
| Research | "Analyze competitors" | "List pricing tiers for Competitor A, B, C in a table" |
| Research | Stats website is down or data missing | Stats available as expected |
| Content | "Write introduction" | "Write 2-sentence intro: what the tool does, who it's for" |
| Data | "Clean the dataset" | "Remove rows where 'email' column is empty or invalid format" |
| Data | File format differs from spec description | File matches expected format |

### 3. Execute

Do exactly what the step says. No more, no less.

- Follow the spec literally
- Use research file for context (terms, decisions)
- Don't add improvements not in the step
- Don't skip parts that seem unnecessary

### 4. Verify

If the step has verification items, complete each one:

- [ ] Verification item 1
- [ ] Verification item 2
- [ ] ...

If verification fails, the step is FAILED (not SUCCESS).

### 5. Return Result

Return exactly one of:

**SUCCESS**
```
Result: SUCCESS
Step: [step number/name]
Summary: [1-2 sentences of what was done]
Artifacts modified: [list if any]
Verification: [all items passed / N/A if none specified]
Observations: [optional - potential improvements, edge cases noticed, or other relevant notes]
```

**FAILED**
```
Result: FAILED
Step: [step number/name]
Summary: [what was attempted]
Error: [what went wrong]
Artifacts modified: [list if any, even partial]
Verification: [which items failed]
Observations: [optional - context that might help diagnose or fix]
```

**GAP**
```
Result: GAP
Step: [step number/name]
Gap: [what situation the spec doesn't cover]
Context: [what was happening when gap was hit]
Options: [possible interpretations or resolutions, if clear]
Recommendation: [suggested clarification to add to spec]
```

## Available Tools

Use any available tools for implementation:
- Invoke skills (TDD, debugging, etc.) as needed
- Use MCP tools (Context7 for docs, etc.)
- Spawn focused sub-agents for specific sub-tasks (e.g., Explore agent)
- Run commands, tests, builds as needed

## Rules

- Never proceed past a GAP - return immediately (gaps can occur before or during execution)
- Never mark SUCCESS if verification failed
- Never modify artifacts outside the step's scope
- Never make judgment calls - if unsure, it's a GAP
- Observations are optional - include if genuinely useful, skip if nothing notable
