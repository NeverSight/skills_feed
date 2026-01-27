---
name: autonomous-master
description: Master orchestrator for autonomous coding projects. Use when starting autonomous projects, continuing sessions, checking status, or running complete autonomous workflows.
version: 1.0.0
category: autonomous-coding
layer: master-orchestration
triggers:
  - "autonomous start"
  - "autonomous continue"
  - "autonomous status"
  - "start autonomous project"
  - "continue autonomous"
  - "run autonomously"
---

# Autonomous Master

**The single entry point for fully autonomous coding.**

Orchestrates all 16 autonomous coding skills to implement complete projects from specification to working code.

## Quick Start

### Start New Project
```
autonomous start: Build a task management app with user authentication,
project management, and team collaboration features. Use Next.js,
TypeScript, Prisma, and PostgreSQL.
```

### Continue Existing Project
```
autonomous continue
```

### Check Status
```
autonomous status
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    AUTONOMOUS MASTER                             │
│                                                                  │
│  "autonomous start: [spec]"                                     │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 1: INITIALIZATION                                 │    │
│  │  ├─ Parse specification                                  │    │
│  │  ├─ Generate 100+ features → feature_list.json          │    │
│  │  ├─ Create environment → init.sh                        │    │
│  │  ├─ Scaffold project structure                          │    │
│  │  ├─ Initialize git repository                           │    │
│  │  └─ Create master-state.json                            │    │
│  │                                                          │    │
│  │  Skills Used: initializer-agent, context-state-tracker  │    │
│  └─────────────────────────────────────────────────────────┘    │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 2: IMPLEMENTATION LOOP                            │    │
│  │  while (incomplete_features > 0):                        │    │
│  │    │                                                     │    │
│  │    ├─ CHECK CONTEXT                                      │    │
│  │    │   └─ If > 85% used → HANDOFF                       │    │
│  │    │                                                     │    │
│  │    ├─ SELECT FEATURE                                     │    │
│  │    │   └─ Priority + dependency order                   │    │
│  │    │                                                     │    │
│  │    ├─ CREATE CHECKPOINT                                  │    │
│  │    │   └─ Safe rollback point                           │    │
│  │    │                                                     │    │
│  │    ├─ IMPLEMENT (TDD)                                    │    │
│  │    │   ├─ RED: Write failing test                       │    │
│  │    │   ├─ GREEN: Implement to pass                      │    │
│  │    │   └─ REFACTOR: Clean up                            │    │
│  │    │                                                     │    │
│  │    ├─ VERIFY                                             │    │
│  │    │   └─ Run E2E tests                                 │    │
│  │    │                                                     │    │
│  │    ├─ If PASS:                                           │    │
│  │    │   ├─ Mark feature complete                         │    │
│  │    │   ├─ Commit changes                                │    │
│  │    │   └─ Update progress                               │    │
│  │    │                                                     │    │
│  │    └─ If FAIL:                                           │    │
│  │        ├─ Attempt recovery                              │    │
│  │        ├─ If unrecoverable: rollback, skip              │    │
│  │        └─ Store error→solution for learning            │    │
│  │                                                          │    │
│  │  Skills Used: coding-agent, tdd-workflow,               │    │
│  │               browser-e2e-tester, error-recoverer,      │    │
│  │               checkpoint-manager, progress-tracker      │    │
│  └─────────────────────────────────────────────────────────┘    │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 3: HANDOFF (when context limit reached)           │    │
│  │  ├─ Compact context summary                              │    │
│  │  ├─ Serialize full state                                 │    │
│  │  ├─ Save handoff package                                 │    │
│  │  ├─ Generate continuation prompt                         │    │
│  │  └─ Exit cleanly                                         │    │
│  │                                                          │    │
│  │  Skills Used: context-compactor, handoff-coordinator,   │    │
│  │               memory-manager                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│         │                                                        │
│         ▼                                                        │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │  PHASE 4: COMPLETION (when all features pass)            │    │
│  │  ├─ Run full E2E test suite                              │    │
│  │  ├─ Generate completion report                           │    │
│  │  ├─ Final commit                                         │    │
│  │  └─ Clean up temporary files                             │    │
│  │                                                          │    │
│  │  Skills Used: browser-e2e-tester, progress-tracker      │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Commands

### `autonomous start: [specification]`

Initializes a new autonomous coding project.

**Input**: Natural language project specification
**Output**:
- `feature_list.json` with 100+ features
- `init.sh` environment setup script
- `claude-progress.txt` progress file
- `.claude/master-state.json` orchestrator state

**Example**:
```
autonomous start: Create an e-commerce platform with:
- User authentication (email, OAuth)
- Product catalog with search and filters
- Shopping cart and checkout
- Order management
- Admin dashboard
Use React, Node.js, PostgreSQL, Stripe for payments.
```

### `autonomous continue`

Resumes from the last handoff point.

**Detects**:
- Loads `.claude/master-state.json`
- Reads `.claude/handoffs/current.json`
- Resumes at current feature

**Example**:
```
autonomous continue
```

### `autonomous status`

Shows current project status.

**Output**:
```
╔══════════════════════════════════════════════════════════════╗
║                  AUTONOMOUS PROJECT STATUS                    ║
╠══════════════════════════════════════════════════════════════╣
║  Project: e-commerce-platform                                 ║
║  Status:  IMPLEMENTING                                        ║
║                                                               ║
║  Progress: ████████████░░░░░░░░ 45/100 (45%)                 ║
║                                                               ║
║  Sessions: 5                                                  ║
║  Current Feature: cart-012 (Add item to cart)                ║
║                                                               ║
║  Errors Recovered: 8                                          ║
║  Errors Skipped: 2                                            ║
║                                                               ║
║  Context Usage: 62% (within limits)                          ║
╚══════════════════════════════════════════════════════════════╝
```

### `autonomous rollback [checkpoint-id]`

Rolls back to a specific checkpoint.

**Example**:
```
autonomous rollback checkpoint-20250115-143000
```

## State Detection

The master orchestrator automatically detects the project state:

```python
def detect_state():
    if not exists("feature_list.json"):
        return "NEEDS_INITIALIZATION"

    if exists(".claude/handoffs/current.json"):
        return "CONTINUE_FROM_HANDOFF"

    features = load("feature_list.json")
    if all(f["passes"] for f in features):
        return "COMPLETE"

    return "CONTINUE_IMPLEMENTATION"
```

## Files Created

| File | Purpose |
|------|---------|
| `feature_list.json` | All features with pass/fail status |
| `init.sh` | Environment setup script |
| `claude-progress.txt` | Human-readable progress log |
| `.claude/master-state.json` | Orchestrator state |
| `.claude/handoffs/*.json` | Handoff packages |
| `.claude/checkpoints/*.json` | Rollback points |
| `.claude/memory/*.json` | Error→solution chains |

## Multi-Session Workflow

```
SESSION 1                    SESSION 2                    SESSION 3
┌─────────────┐              ┌─────────────┐              ┌─────────────┐
│ autonomous  │              │ autonomous  │              │ autonomous  │
│ start: spec │              │ continue    │              │ continue    │
├─────────────┤              ├─────────────┤              ├─────────────┤
│ Initialize  │              │ Load state  │              │ Load state  │
│ Features    │              │ Resume      │              │ Resume      │
│ 1-15        │──handoff──▶  │ Features    │──handoff──▶  │ Features    │
│             │              │ 16-35       │              │ 36-50       │
│ Context: 85%│              │ Context: 85%│              │ Context: 60%│
└─────────────┘              └─────────────┘              └─────────────┘
                                                                 │
                                                                 ▼
                                                          ┌─────────────┐
                                                          │  COMPLETE   │
                                                          │  50/50 ✓    │
                                                          └─────────────┘
```

## Skill Dependencies

The master orchestrator uses all 16 skills:

```
autonomous-master
├── Layer 1: Session Management
│   ├── autonomous-session-manager
│   ├── context-state-tracker
│   └── security-sandbox
├── Layer 2: Agent Roles
│   ├── initializer-agent
│   ├── coding-agent
│   └── progress-tracker
├── Layer 3: Context Engineering
│   ├── context-compactor
│   ├── memory-manager
│   └── handoff-coordinator
├── Layer 4: Verification & Recovery
│   ├── browser-e2e-tester
│   ├── error-recoverer
│   └── checkpoint-manager
└── Layer 5: Orchestration
    ├── autonomous-loop
    ├── parallel-agent-spawner
    ├── autonomous-cost-optimizer
    └── tdd-workflow
```

## Configuration

Edit `.claude/master-config.json`:

```json
{
  "max_sessions": 20,
  "features_per_session": 15,
  "context_threshold": 0.85,
  "auto_checkpoint": true,
  "parallel_features": false,
  "tdd_strict": true,
  "e2e_required": true
}
```

## Error Recovery

When errors occur:

1. **Transient errors** (network, rate limit): Automatic retry with backoff
2. **Code errors** (syntax, type): Attempt fix, retry
3. **Test failures**: Debug, fix, retry
4. **Unrecoverable**: Rollback to checkpoint, skip feature, continue

All errors are stored in memory for future reference (causal chains).

## Scripts

- `scripts/master_orchestrator.py` - Core orchestration
- `scripts/state_machine.py` - State transitions
- `scripts/command_parser.py` - Parse user commands
- `scripts/session_detector.py` - Detect project state
- `scripts/continuation_generator.py` - Generate handoff prompts

## References

- `references/COMMANDS.md` - Full command reference
- `references/STATE-MACHINE.md` - State transition details
- `references/TROUBLESHOOTING.md` - Common issues and fixes
