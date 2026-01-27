---
name: autonomous-session-manager
description: Session lifecycle management for autonomous coding. Use when starting new coding sessions, resuming work, detecting session type (init vs continue), or managing auto-continuation between sessions.
version: 1.0.0
category: autonomous-coding
layer: foundation
---

# Autonomous Session Manager

Manages session lifecycle for autonomous coding operations - creation, resumption, detection, and auto-continuation.

## Quick Start

### Detect Session Type
```python
from scripts.session_detector import detect_session_type, SessionType

session_type = detect_session_type(project_dir)
if session_type == SessionType.INIT:
    # First run - need to initialize
    pass
else:
    # Continuation - resume previous work
    pass
```

### Create New Session
```python
from scripts.session_manager import SessionManager

async with SessionManager(project_dir, model="claude-sonnet-4-5-20250929") as session:
    result = await session.run(prompt)
```

### Auto-Continue After Session
```python
from scripts.auto_continue import auto_continue

# Automatically start next session after 3 second delay
await auto_continue(delay_seconds=3)
```

## Session Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DETECT SESSION TYPE                                      │
│     ├─ Check for feature_list.json                          │
│     ├─ If missing → INIT session                            │
│     └─ If exists → CONTINUE session                         │
│                                                              │
│  2. CREATE SESSION                                           │
│     ├─ Initialize SDK client                                │
│     ├─ Configure tools and permissions                      │
│     └─ Set working directory                                │
│                                                              │
│  3. RUN SESSION                                              │
│     ├─ Execute prompt (initializer or coding)               │
│     ├─ Handle tool calls                                    │
│     └─ Capture results                                      │
│                                                              │
│  4. END SESSION                                              │
│     ├─ Save state                                           │
│     ├─ Check completion status                              │
│     └─ Trigger auto-continue or shutdown                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Session Detection** | Automatically determines if INIT or CONTINUE |
| **State Restoration** | Reads progress files at session start |
| **Auto-Continue** | Configurable delay between sessions |
| **Graceful Shutdown** | Saves state before termination |
| **Iteration Tracking** | Counts sessions for limits |

## Configuration

```python
# Session configuration
SESSION_CONFIG = {
    "model": "claude-sonnet-4-5-20250929",
    "max_turns": 1000,
    "continue_delay": 3,  # seconds
    "max_iterations": None,  # None = unlimited
}
```

## Integration Points

- **context-state-tracker**: Provides state persistence
- **security-sandbox**: Provides command validation
- **autonomous-loop**: Uses session manager for continuous operation

## References

- `references/SESSION-LIFECYCLE.md` - Detailed lifecycle documentation
- `references/CONFIGURATION.md` - Configuration options

## Scripts

- `scripts/session_manager.py` - Core SessionManager class
- `scripts/session_detector.py` - Session type detection
- `scripts/auto_continue.py` - Auto-continuation logic
