---
name: handoff-coordinator
description: Clean transitions between agents and sessions. Use when preparing handoffs, serializing state, bridging context between agents, or coordinating multi-agent workflows.
version: 1.0.0
category: autonomous-coding
layer: context-engineering
---

# Handoff Coordinator

Manages clean transitions between agents and sessions with state serialization and context bridging.

## Quick Start

### Prepare Handoff
```python
from scripts.handoff_coordinator import HandoffCoordinator

coordinator = HandoffCoordinator(project_dir)
package = await coordinator.prepare_handoff(
    source_agent="coding-agent",
    summary="Completed auth-001, starting auth-002"
)
```

### Execute Handoff
```python
await coordinator.execute_handoff(
    package=package,
    target_agent="coding-agent"
)
```

## Handoff Process

```
┌─────────────────────────────────────────────────────────────┐
│                    HANDOFF WORKFLOW                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  SOURCE AGENT                                                │
│  ├─ Complete current work                                   │
│  ├─ Save state to files                                    │
│  ├─ Create handoff package                                  │
│  └─ Signal ready for handoff                               │
│                                                              │
│  COORDINATOR                                                 │
│  ├─ Validate state consistency                             │
│  ├─ Serialize handoff package                              │
│  ├─ Store in handoff file                                  │
│  └─ Trigger target agent                                   │
│                                                              │
│  TARGET AGENT                                                │
│  ├─ Load handoff package                                   │
│  ├─ Restore context                                        │
│  ├─ Verify state                                           │
│  └─ Continue work                                          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Handoff Package

```json
{
  "id": "handoff-20250115-103000",
  "source_agent": "coding-agent",
  "target_agent": "coding-agent",
  "timestamp": "2025-01-15T10:30:00",
  "state": {
    "current_feature": "auth-002",
    "completed_features": ["auth-001"],
    "blockers": [],
    "next_steps": ["Implement logout endpoint"]
  },
  "context": {
    "recent_files": ["src/auth/login.ts"],
    "git_hash": "abc1234",
    "session_number": 5
  },
  "summary": "Completed auth-001, starting auth-002"
}
```

## Handoff Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Session** | Same agent, new session | Context limit reached |
| **Agent** | Different agent | Specialized task |
| **Parallel** | Multiple targets | Split work |
| **Recovery** | After failure | Error recovery |

## Integration Points

- **autonomous-session-manager**: Triggers session handoffs
- **context-compactor**: Compacts before handoff
- **memory-manager**: Stores handoff summaries

## References

- `references/HANDOFF-PROTOCOL.md` - Protocol details
- `references/AGENT-TRANSITIONS.md` - Transition patterns

## Scripts

- `scripts/handoff_coordinator.py` - Core coordinator
- `scripts/state_serializer.py` - State serialization
- `scripts/context_bridge.py` - Context bridging
- `scripts/handoff_protocol.py` - Protocol implementation
