---
name: autonomous-loop
description: Main orchestration loop for autonomous coding. Use when running autonomous sessions, orchestrating feature completion, managing continuous loops, or coordinating agent lifecycle.
version: 1.0.0
category: autonomous-coding
layer: orchestration
---

# Autonomous Loop

Main orchestration loop that runs continuously until all features are complete.

## Quick Start

### Start Autonomous Loop
```python
from scripts.autonomous_loop import AutonomousLoop

loop = AutonomousLoop(project_dir)
result = await loop.run()

print(f"Completed: {result.features_completed}")
print(f"Sessions: {result.sessions_used}")
```

### With Configuration
```python
from scripts.loop_config import LoopConfig

config = LoopConfig(
    max_sessions=10,
    token_budget=500000,
    auto_checkpoint=True
)
result = await loop.run(config)
```

## Autonomous Loop Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                   AUTONOMOUS LOOP                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────┐    │
│  │  INITIALIZE                                         │    │
│  │  ├─ Detect session type (INIT vs CONTINUE)         │    │
│  │  ├─ Load or create feature list                    │    │
│  │  └─ Initialize state tracker                       │    │
│  └────────────────────────────────────────────────────┘    │
│                         │                                   │
│                         ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  FEATURE LOOP                                       │    │
│  │  while (incomplete_features > 0):                   │    │
│  │    ├─ Select next feature                          │    │
│  │    ├─ Create checkpoint                            │    │
│  │    ├─ Implement with TDD                           │    │
│  │    ├─ Run E2E tests                                │    │
│  │    ├─ If pass: mark complete                       │    │
│  │    ├─ If fail: recover or rollback                 │    │
│  │    └─ Check context limits                         │    │
│  └────────────────────────────────────────────────────┘    │
│                         │                                   │
│                         ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  CONTEXT CHECK                                      │    │
│  │  if (approaching_limit):                            │    │
│  │    ├─ Compact context                              │    │
│  │    ├─ Prepare handoff                              │    │
│  │    └─ Request continuation                         │    │
│  └────────────────────────────────────────────────────┘    │
│                         │                                   │
│                         ▼                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │  COMPLETION                                         │    │
│  │  ├─ Generate final report                          │    │
│  │  ├─ Store session memory                           │    │
│  │  └─ Signal completion                              │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Loop Result

```python
@dataclass
class LoopResult:
    success: bool
    features_completed: int
    features_total: int
    sessions_used: int
    total_tokens: int
    errors_recovered: int
    duration_minutes: float
    handoff_reason: Optional[str]
```

## Continuation Modes

| Mode | Description | Trigger |
|------|-------------|---------|
| **Auto** | Loop continues automatically | Context limit |
| **Manual** | User confirms continuation | Session end |
| **Scheduled** | Runs at scheduled times | Cron trigger |
| **Event** | Triggered by events | Git push, CI |

## Integration Points

- **autonomous-session-manager**: Session lifecycle
- **coding-agent**: Feature implementation
- **browser-e2e-tester**: Feature verification
- **error-recoverer**: Handle failures
- **checkpoint-manager**: Safe rollback
- **handoff-coordinator**: Session transitions
- **progress-tracker**: Track and report

## References

- `references/LOOP-LIFECYCLE.md` - Loop details
- `references/CONTINUATION-PROTOCOL.md` - Continuation

## Scripts

- `scripts/autonomous_loop.py` - Main loop
- `scripts/loop_config.py` - Configuration
- `scripts/feature_orchestrator.py` - Feature flow
- `scripts/continuation_handler.py` - Continuations
