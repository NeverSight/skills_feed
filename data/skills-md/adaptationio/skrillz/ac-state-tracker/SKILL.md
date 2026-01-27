---
name: ac-state-tracker
description: State persistence for autonomous coding. Use when saving progress, loading state, tracking features, managing checkpoints, or persisting data across sessions.
version: 1.0.0
layer: foundation
category: auto-claude-replication
triggers:
  - "save state"
  - "load state"
  - "track progress"
  - "update feature"
  - "checkpoint"
---

# AC State Tracker

Persistent state management for cross-session autonomous coding.

## Overview

Maintains all state across sessions:
- Feature list tracking (passes: false → true)
- Execution state (iteration, cost, status)
- Progress logging
- Handoff packages
- Checkpoint management

## Quick Start

### Initialize State Tracker
```python
from scripts.state_tracker import StateTracker

state = StateTracker(project_dir)
await state.initialize()
```

### Save/Load State
```python
# Save current state
await state.save()

# Load state from files
current_state = await state.load()
```

### Update Feature Status
```python
# Mark feature as passing (IMMUTABLE: false → true only!)
await state.update_feature("auth-001", passes=True)
```

## State Files

### Primary State Files

```
project/
├── feature_list.json        # Feature tracking (immutable passes)
├── claude-progress.txt      # Human-readable log
└── .claude/
    ├── master-state.json    # Orchestrator state
    ├── autonomous-state.json # Execution state
    ├── autonomous-log.jsonl  # Activity log
    ├── handoffs/
    │   └── current.json     # Mid-session handoff
    └── checkpoints/
        └── checkpoint-*.json # Rollback points
```

### feature_list.json Schema

```json
{
  "features": [
    {
      "id": "auth-001",
      "description": "User registration endpoint",
      "category": "authentication",
      "status": "completed",
      "passes": true,
      "test_cases": [
        "User can register with email",
        "Validation errors shown"
      ],
      "dependencies": [],
      "estimated_effort": "4h",
      "actual_effort": "2.5h",
      "started_at": "2025-01-15T10:00:00Z",
      "completed_at": "2025-01-15T12:30:00Z"
    }
  ],
  "total": 50,
  "completed": 25,
  "in_progress": 1,
  "blocked": 0
}
```

**CRITICAL RULE**: Features can ONLY transition `passes: false → true`. Never delete or edit features - this prevents the agent from "solving" by removing tasks.

### autonomous-state.json Schema

```json
{
  "session_id": "session-20250115-100000",
  "iteration": 12,
  "status": "running",
  "estimated_cost": 4.23,
  "consecutive_failures": 0,
  "current_feature": "auth-002",
  "last_task": "Implement login endpoint",
  "started_at": "2025-01-15T10:00:00Z",
  "context_usage": 0.45
}
```

### master-state.json Schema

```json
{
  "project_id": "my-project",
  "objective": "Build chat application",
  "sessions_used": 5,
  "total_features": 50,
  "features_completed": 25,
  "current_phase": "implementation",
  "last_handoff": "2025-01-15T12:00:00Z"
}
```

## Operations

### 1. Initialize State

```python
state = StateTracker(project_dir)
await state.initialize()

# Creates default files if not exist
# Loads existing state if present
```

### 2. Update Feature

```python
# Mark feature complete
await state.update_feature(
    feature_id="auth-001",
    passes=True,
    actual_effort="2.5h"
)

# Mark feature in progress
await state.update_feature(
    feature_id="auth-002",
    status="in_progress"
)
```

### 3. Create Checkpoint

```python
checkpoint = await state.create_checkpoint(
    name="before-refactor",
    git_commit=True
)
# Returns checkpoint ID for rollback
```

### 4. Restore Checkpoint

```python
await state.restore_checkpoint("checkpoint-20250115-100000")
# Restores feature_list.json and git state
```

### 5. Log Activity

```python
await state.log_activity(
    action="CONTINUE",
    details="Implementing login endpoint",
    iteration=12
)
# Appends to autonomous-log.jsonl
```

### 6. Save Handoff

```python
await state.save_handoff({
    "current_feature": "auth-002",
    "context_summary": "Completed auth, starting profile...",
    "next_action": "Implement profile page"
})
```

### 7. Get Progress Summary

```python
progress = await state.get_progress()
# Returns:
#   completed: 25
#   total: 50
#   percentage: 50%
#   current_feature: "auth-002"
#   estimated_remaining: "4 hours"
```

## Progress File Format

### claude-progress.txt
```
=== AUTONOMOUS CODING SESSION ===
Project: my-project
Started: 2025-01-15 10:00:00
Sessions: 5

=== PROGRESS ===
[25/50] 50% complete

=== CURRENT FEATURE ===
auth-002: Login with JWT

=== COMPLETED THIS SESSION ===
- auth-001: User registration [PASS]
- auth-002: Login endpoint [IN PROGRESS]

=== BLOCKERS ===
None

=== LAST UPDATED ===
2025-01-15 12:30:00
```

## Integration Points

- **ac-config-manager**: Loads paths configuration
- **ac-session-manager**: Triggers state save/load
- **ac-autonomous-loop**: Updates feature status
- **ac-checkpoint-manager**: Creates/restores checkpoints
- **ac-handoff-coordinator**: Manages handoff packages

## References

- `references/STATE-SCHEMA.md` - Complete state schemas
- `references/FEATURE-LIFECYCLE.md` - Feature state machine

## Scripts

- `scripts/state_tracker.py` - Core StateTracker class
- `scripts/feature_manager.py` - Feature list operations
- `scripts/checkpoint_store.py` - Checkpoint storage
- `scripts/progress_logger.py` - Progress file generation
