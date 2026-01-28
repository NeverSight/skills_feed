---
name: recursive-handoff
description: "Execute the same task repeatedly with clean context via handoff. Triggers on: recursive loop, repeat until, keep doing until, loop until done. REQUIRES a finish condition to stop."
---

# Recursive Handoff

Run the same prompt repeatedly with fresh context until a finish condition is met.

---

## When to Use

- Long-running tasks that would exhaust context
- Repetitive operations (process items one by one, migrate in batches)
- Polling/waiting for external state changes
- Any task where "keep doing X until Y" applies

---

## Required Parameters

### 1. Finish Condition

**You MUST get a finish condition from the user before starting.**

The condition must be **verifiable programmatically** (file check, command output, grep result, API response, etc.)

Examples:
- "All files in `src/legacy/` have been processed"
- "No more TODO comments exist in the codebase"
- "The API returns status 200"
- "The queue is empty"

### 2. Hard Limit (default: 20)

Maximum iterations before stopping. Prevents runaway loops.

---

## How It Works

```
┌─────────────────────────────────────────┐
│  Thread 1: Check condition → not met    │
│            Do work → handoff            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  Thread 2: Check condition → not met    │
│            Do work → handoff            │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│  Thread 3: Check condition → MET        │
│            STOP (no handoff)            │
└─────────────────────────────────────────┘
```

Each iteration:
1. **Check iteration count** - stop if limit reached
2. **Check finish condition**
3. If met → stop, report completion
4. If not met → do one unit of work → handoff to continue

---

## The Handoff Prompt Template

```
RECURSIVE TASK - Iteration [N] of [LIMIT]

## Finish Condition
[CONDITION]

## How to Check
[COMMAND OR METHOD TO VERIFY CONDITION]

## If Limit Reached or Condition Met
Stop. Report: "✅ Complete: [summary]" or "⚠️ Limit reached after [N] iterations"
Do NOT handoff.

## If Condition NOT Met

### Task
[WHAT TO DO THIS ITERATION]

### After Completing Work
Handoff with follow: true, incrementing iteration count:

[PASTE THIS PROMPT WITH N+1]
```

---

## Example: Generic Processing Loop

**User:** "Process all items in the queue"

**Finish condition:** Queue is empty

**Handoff prompt:**
```
RECURSIVE TASK - Iteration 1 of 20

## Finish Condition
Queue is empty

## How to Check
[command to check queue length]
If result is 0, condition is met.

## If Limit Reached or Condition Met
Stop. Report completion status.
Do NOT handoff.

## If Condition NOT Met

### Task
1. Get next item from queue
2. Process it
3. Remove from queue

### After Completing Work
Handoff with follow: true, goal:

[THIS PROMPT WITH ITERATION 2 of 20]
```

---

## Starting the Loop

Once setup is complete, invoke handoff with `follow: true`:

```
handoff
  goal: [THE FULL HANDOFF PROMPT]
  follow: true
```

The loop continues autonomously until finish condition is met or limit is reached.
