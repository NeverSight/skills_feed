---
name: ralph-loop
description: Autonomous development loop for completing all remaining tasks. Use when user says "全部完成", "完成所有任务", "finish all", "complete everything", or similar phrases indicating they want Claude to autonomously work through all remaining tasks until completion.
---

# Ralph Loop

Autonomous development loop that continues working until all tasks are complete.

## Workflow

When triggered, execute this loop:

```
┌─────────────────────────────────────────────────────────┐
│                    RALPH LOOP                           │
├─────────────────────────────────────────────────────────┤
│  1. Check TodoWrite for pending tasks                   │
│  2. If no pending tasks → output "COMPLETE" and exit    │
│  3. Pick highest priority pending task                  │
│  4. Mark task as in_progress                            │
│  5. Execute the task                                    │
│  6. Mark task as completed                              │
│  7. Go to step 1                                        │
└─────────────────────────────────────────────────────────┘
```

## Exit Condition

Output exactly `COMPLETE` (on its own line) when:
- All tasks in the todo list are marked as completed
- No more pending tasks remain

## Execution Rules

1. **Task Priority**: Process tasks in order (top to bottom)
2. **One at a Time**: Only one task should be `in_progress` at any moment
3. **Immediate Update**: Mark tasks completed immediately after finishing
4. **No Skipping**: Complete each task fully before moving to the next
5. **Error Handling**: If a task fails, log the error and continue to next task

## Status Block

After each task completion, output a status block:

```
RALPH_STATUS:
  completed: <task description>
  remaining: <number of pending tasks>
  EXIT_SIGNAL: <true if no more tasks, false otherwise>
```

## Example

```
User: 全部完成

Claude: [Invokes ralph-loop skill]

Checking todo list...
- [x] Task 1 (completed)
- [-] Task 2 (in_progress) ← Working on this
- [ ] Task 3 (pending)

RALPH_STATUS:
  completed: Task 2
  remaining: 1
  EXIT_SIGNAL: false

[Continues to Task 3...]

RALPH_STATUS:
  completed: Task 3
  remaining: 0
  EXIT_SIGNAL: true

COMPLETE
```
