---
name: ac-task-executor
description: Execute implementation tasks in autonomous coding. Use when running feature implementations, executing build tasks, processing feature queue, or orchestrating task completion.
---

# AC Task Executor

Execute implementation tasks for autonomous coding features.

## Purpose

Orchestrates the execution of feature implementations, managing the task queue and coordinating between planning, implementation, and verification phases.

## Quick Start

```python
from scripts.task_executor import TaskExecutor

executor = TaskExecutor(project_dir)
result = await executor.execute_next_feature()
```

## Execution Modes

### Single Feature
Execute one feature at a time:
```python
result = await executor.execute_feature("auth-001")
```

### Queue Mode
Process feature queue continuously:
```python
await executor.execute_queue(max_features=10)
```

### Batch Mode
Execute multiple features in a batch:
```python
results = await executor.execute_batch(["auth-001", "auth-002"])
```

## Task Lifecycle

```
1. SELECT   → Choose next feature from queue
2. PREPARE  → Load context, generate tests (RED)
3. IMPLEMENT → Write code to pass tests (GREEN)
4. REFACTOR → Clean up while tests pass
5. VALIDATE → Run criteria validation
6. COMMIT   → Git commit changes
7. UPDATE   → Mark feature as passes: true
8. NEXT     → Continue to next feature
```

## Execution Result

```json
{
  "feature_id": "auth-001",
  "status": "completed",
  "phases": {
    "prepare": {"success": true, "duration_ms": 1500},
    "implement": {"success": true, "duration_ms": 45000},
    "validate": {"success": true, "duration_ms": 5000},
    "commit": {"success": true, "commit_hash": "abc123"}
  },
  "tests": {
    "total": 5,
    "passed": 5,
    "failed": 0
  },
  "metrics": {
    "tokens_used": 15000,
    "estimated_cost": 0.23
  }
}
```

## Error Handling

- **Validation Failure**: Retry implementation up to 3 times
- **Test Failure**: Analyze failures, adjust approach
- **Timeout**: Save state, create handoff for continuation
- **Critical Error**: Rollback to last checkpoint

## Integration

- Uses: `ac-state-tracker`, `ac-test-generator`, `ac-criteria-validator`
- Triggers: `ac-commit-manager`, `ac-qa-reviewer`
- Reports to: `ac-session-manager`

## API Reference

See `scripts/task_executor.py` for full implementation.
