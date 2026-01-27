---
name: checkpoint-manager
description: State snapshots and rollback for safe experimentation. Use when creating checkpoints, rolling back changes, managing recovery points, or implementing safe experimentation.
version: 1.0.0
category: autonomous-coding
layer: verification-recovery
---

# Checkpoint Manager

Creates and manages state checkpoints for safe rollback during autonomous coding.

## Quick Start

### Create Checkpoint
```python
from scripts.checkpoint_manager import CheckpointManager

manager = CheckpointManager(project_dir)
checkpoint = await manager.create_checkpoint(
    name="before-refactor",
    description="State before major refactoring"
)
```

### Rollback to Checkpoint
```python
await manager.rollback(checkpoint.id)
# or rollback to latest
await manager.rollback_to_latest()
```

## Checkpoint Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                 CHECKPOINT WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  CREATE CHECKPOINT                                           │
│  ├─ Capture git state (commit hash, dirty files)           │
│  ├─ Snapshot feature list                                   │
│  ├─ Save progress file state                               │
│  ├─ Record context (session, tokens)                       │
│  └─ Store checkpoint metadata                               │
│                                                              │
│  RISKY OPERATION                                             │
│  ├─ Attempt operation                                       │
│  ├─ If success → Continue                                   │
│  └─ If failure → Rollback to checkpoint                    │
│                                                              │
│  ROLLBACK                                                    │
│  ├─ Load checkpoint data                                    │
│  ├─ Git reset to checkpoint commit                         │
│  ├─ Restore feature list                                   │
│  ├─ Restore progress file                                  │
│  └─ Clean up temporary files                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Checkpoint Structure

```json
{
  "id": "checkpoint-20250115-103000",
  "name": "before-refactor",
  "description": "State before major refactoring",
  "timestamp": "2025-01-15T10:30:00",
  "git_state": {
    "commit_hash": "abc1234",
    "branch": "main",
    "dirty_files": ["src/app.ts"]
  },
  "feature_state": {
    "current": "auth-003",
    "completed": ["auth-001", "auth-002"],
    "snapshot_path": ".claude/checkpoints/checkpoint-xxx/feature_list.json"
  },
  "context": {
    "session_number": 5,
    "token_usage": 45000
  }
}
```

## Checkpoint Types

| Type | Trigger | Retention |
|------|---------|-----------|
| **Automatic** | Before risky operations | Last 5 |
| **Manual** | User/agent request | Until deleted |
| **Feature** | After feature complete | Permanent |
| **Session** | Start of session | Last 3 |

## Integration Points

- **error-recoverer**: Triggers rollback on failures
- **coding-agent**: Creates checkpoints before changes
- **autonomous-loop**: Manages checkpoint lifecycle
- **context-state-tracker**: Provides state to checkpoint

## References

- `references/CHECKPOINT-STRATEGY.md` - Strategy guide
- `references/ROLLBACK-PROCEDURES.md` - Rollback details

## Scripts

- `scripts/checkpoint_manager.py` - Core manager
- `scripts/git_snapshot.py` - Git state capture
- `scripts/state_snapshot.py` - Feature/progress capture
- `scripts/rollback_handler.py` - Rollback execution
