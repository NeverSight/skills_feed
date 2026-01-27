---
name: ac-session-manager
description: Session lifecycle management for autonomous coding. Use when starting sessions, resuming work, detecting session type (init vs continue), or managing auto-continuation between sessions.
version: 1.0.0
layer: foundation
category: auto-claude-replication
triggers:
  - "start session"
  - "continue session"
  - "session status"
  - "detect session"
  - "auto continue"
---

# AC Session Manager

Complete session lifecycle management for autonomous coding operations.

## Overview

Manages the full session lifecycle:
- Session type detection (INIT vs CONTINUE)
- Session creation and configuration
- Auto-continuation between sessions
- Graceful shutdown with state preservation

## Quick Start

### Detect Session Type
```python
from scripts.session_manager import SessionManager

manager = SessionManager(project_dir)
session_type = await manager.detect_type()

if session_type == "INIT":
    # First run - initialize project
    await manager.run_initializer()
elif session_type == "CONTINUE":
    # Resume work
    await manager.run_continuation()
elif session_type == "COMPLETE":
    print("All features complete!")
```

### Run Session
```python
async with SessionManager(project_dir) as session:
    result = await session.run(prompt)
    print(f"Status: {result.status}")
```

## Session Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DETECT SESSION TYPE                                      │
│     ├─ Check for feature_list.json                          │
│     ├─ If missing → INIT session                            │
│     ├─ If handoff exists → CONTINUE_FROM_HANDOFF            │
│     ├─ If all pass → COMPLETE                               │
│     └─ Otherwise → CONTINUE_IMPLEMENTATION                  │
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

## Session Types

| Type | Condition | Action |
|------|-----------|--------|
| `INIT` | No feature_list.json | Run initializer agent |
| `CONTINUE_FROM_HANDOFF` | handoffs/current.json exists | Resume from handoff |
| `CONTINUE_IMPLEMENTATION` | Features incomplete | Continue coding |
| `COMPLETE` | All features pass | Generate report, exit |

## Detection Logic

```python
def detect_session_type(project_dir: Path) -> SessionType:
    # Check for initialization
    if not (project_dir / "feature_list.json").exists():
        return SessionType.INIT

    # Check for handoff
    if (project_dir / ".claude/handoffs/current.json").exists():
        return SessionType.CONTINUE_FROM_HANDOFF

    # Check completion
    features = load_features(project_dir)
    if all(f["passes"] for f in features):
        return SessionType.COMPLETE

    return SessionType.CONTINUE_IMPLEMENTATION
```

## Operations

### 1. Create Session

```python
session = await SessionManager.create(
    project_dir=project_dir,
    model="claude-opus-4-5-20251101",
    max_turns=1000,
    tools=["Read", "Write", "Edit", "Bash", "Glob", "Grep"]
)
```

### 2. Run Initializer

```python
result = await session.run_initializer(
    spec="Build a task management app with auth..."
)
# Creates:
#   - feature_list.json (100+ features)
#   - init.sh (environment setup)
#   - Project scaffold
```

### 3. Run Continuation

```python
result = await session.run_continuation()
# Loads state, resumes at current feature
```

### 4. Auto-Continue

```python
# Configure auto-continuation
session.configure_auto_continue(
    enabled=True,
    delay_seconds=3
)

# After session ends, automatically starts next
await session.run()
# ... session completes ...
# [3 second delay]
# Next session starts automatically
```

### 5. Graceful Shutdown

```python
await session.shutdown(
    save_state=True,
    create_handoff=True
)
# Saves state, creates handoff for next session
```

## Session Configuration

```python
@dataclass
class SessionConfig:
    model: str = "claude-opus-4-5-20251101"
    max_turns: int = 1000
    timeout_ms: int = 600000
    continue_delay: int = 3
    max_sessions: int = None  # Unlimited

    # Tool configuration
    tools: list = field(default_factory=lambda: [
        "Read", "Write", "Edit", "Bash", "Glob", "Grep"
    ])

    # Permissions
    sandbox_enabled: bool = True
    allowed_paths: list = field(default_factory=lambda: ["./**"])
```

## Multi-Session Flow

```
SESSION 1: Initialize + Features 1-15
    │
    ▼ (context 85% → handoff)

SESSION 2: Resume + Features 16-30
    │
    ▼ (context 85% → handoff)

SESSION 3: Resume + Features 31-50
    │
    ▼

COMPLETE: All features pass!
```

### Session State Persistence

```json
// .claude-session-state.json
{
  "id": "session-20250115-100000",
  "type": "CONTINUE_IMPLEMENTATION",
  "status": "running",
  "iteration": 5,
  "started_at": "2025-01-15T10:00:00Z",
  "features_this_session": ["auth-001", "auth-002"],
  "context_usage": 0.65
}
```

## Prompts

### Initializer Prompt
```markdown
You are initializing an autonomous coding project.

SPECIFICATION:
{spec}

Your tasks:
1. Analyze the specification
2. Generate feature_list.json with 100+ testable features
3. Create init.sh for environment setup
4. Scaffold initial project structure
5. Initialize git repository
6. Commit initial state

Output MUST include:
- feature_list.json (all features passes: false)
- init.sh (executable setup script)
- Project files (scaffold)
```

### Continuation Prompt
```markdown
You are continuing autonomous development.

Current state:
- Features completed: {completed}/{total}
- Current feature: {current_feature}
- Last action: {last_action}

Resume implementing features following TDD:
1. Select next incomplete feature
2. Write failing test (RED)
3. Implement to pass (GREEN)
4. Refactor as needed
5. Commit changes

Work on ONE feature at a time.
Update feature_list.json when feature passes.
```

## Integration Points

- **ac-config-manager**: Gets session configuration
- **ac-state-tracker**: Saves/loads session state
- **ac-hooks-manager**: Registers Stop hook
- **ac-handoff-coordinator**: Creates handoff packages
- **ac-autonomous-loop**: Orchestrates sessions

## References

- `references/SESSION-LIFECYCLE.md` - Detailed lifecycle
- `references/PROMPTS.md` - Session prompts
- `references/MULTI-SESSION.md` - Multi-session patterns

## Scripts

- `scripts/session_manager.py` - Core SessionManager
- `scripts/session_detector.py` - Session type detection
- `scripts/auto_continue.py` - Auto-continuation logic
- `scripts/prompts.py` - Prompt templates
