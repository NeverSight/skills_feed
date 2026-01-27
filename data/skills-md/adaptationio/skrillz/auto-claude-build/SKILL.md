---
name: auto-claude-build
description: Auto-Claude autonomous build system. Use when running builds, understanding agent workflow, managing parallel execution, or troubleshooting build issues.
version: 1.0.0
auto-claude-version: 2.7.2
---

# Auto-Claude Build System

Deep dive into the autonomous build pipeline and agent orchestration.

## Build Architecture

### Agent Pipeline

```
Spec → Planner Agent → Coder Agent → QA Reviewer → QA Fixer → Complete
         │                 │              │            │
         ▼                 ▼              ▼            ▼
    impl_plan.json    Code Changes    QA Report    Fixed Code
```

### Agent Roles

| Agent | Purpose | Model | Thinking Tokens |
|-------|---------|-------|-----------------|
| **Planner** | Creates subtask-based implementation plan | Claude | 5000 |
| **Coder** | Implements subtasks, can spawn subagents | Claude | None |
| **QA Reviewer** | Validates acceptance criteria | Claude | 10000 |
| **QA Fixer** | Fixes QA-reported issues | Claude | None |

## Running Builds

### Basic Build

```bash
cd apps/backend
source .venv/bin/activate

# Run build for spec
python run.py --spec 001

# With iteration limit (for testing)
python run.py --spec 001 --max-iterations 5
```

### Build Options

| Option | Description |
|--------|-------------|
| `--spec SPEC` | Spec to build (number or full name) |
| `--max-iterations N` | Limit build iterations |
| `--skip-qa` | Skip automatic QA validation |
| `--qa` | Run QA validation only |

### Build Flow

1. **Initialization**
   - Creates git worktree for isolation
   - Loads spec and implementation plan
   - Sets up security sandbox

2. **Planning Phase**
   - Planner agent analyzes spec
   - Creates subtask breakdown
   - Assigns dependencies

3. **Implementation Phase**
   - Coder agent implements subtasks
   - Can spawn subagents for parallel work
   - Updates progress in real-time

4. **QA Phase**
   - QA Reviewer validates each acceptance criterion
   - Creates QA report
   - If issues found, QA Fixer applies fixes
   - Loop until approved (max 50 iterations)

## Agent Configuration

### Claude SDK Client

All agents use the Claude Agent SDK configured in `core/client.py`:

```python
from core.client import create_client

client = create_client(
    project_dir=project_dir,
    spec_dir=spec_dir,
    model="claude-opus-4-5-20251101",
    agent_type="coder",  # or "planner", "qa_reviewer", "qa_fixer"
    max_thinking_tokens=None  # or 5000, 10000, 16000
)
```

### Security Layers

1. **Sandbox** - OS-level bash isolation
2. **Filesystem Permissions** - Restricted to project directory
3. **Command Allowlist** - Only approved commands (see `security.py`)

### Available Tools

| Tool | Description | Agents |
|------|-------------|--------|
| Read, Write, Edit | File operations | All |
| Glob, Grep | File search | All |
| Bash | Shell commands (allowlisted) | All |
| Context7 | Documentation lookup | All |
| Linear | Project management | All (if enabled) |
| Graphiti | Memory system | All (if enabled) |
| Electron/Puppeteer | Browser testing | QA only |

## Parallel Execution

### Subagent Spawning

The Coder agent can spawn subagents for parallel work:

```
Main Coder Agent
├── Subagent 1: Frontend work
├── Subagent 2: Backend work
└── Subagent 3: Tests
```

Configuration:
- Up to 12 agent terminals
- Each runs in isolated context
- Results merged automatically

### Git Worktree Strategy

```
main (your branch)
└── auto-claude/{spec-name}  ← isolated worktree
```

Key principles:
- ONE branch per spec
- All work in isolated worktree
- No automatic pushes
- User controls merge timing

## Monitoring Builds

### Real-time Progress

```bash
# Watch build progress
tail -f .auto-claude/specs/001-feature/build-progress.txt

# Check implementation plan status
cat .auto-claude/specs/001-feature/implementation_plan.json | jq '.subtasks[] | {id, title, status}'
```

### Interactive Controls

During build:
- `Ctrl+C` (once) - Pause and add instructions
- `Ctrl+C` (twice) - Exit immediately

File-based control:
```bash
# Pause after current session
touch .auto-claude/specs/001-feature/PAUSE

# Add instructions
echo "Focus on the login flow" > .auto-claude/specs/001-feature/HUMAN_INPUT.md

# Resume
rm .auto-claude/specs/001-feature/PAUSE
```

## Build Artifacts

### Directory Structure

```
.auto-claude/specs/001-feature/
├── spec.md                    # Specification
├── implementation_plan.json   # Subtask plan with status
├── build-progress.txt         # Real-time progress log
├── qa_report.md              # QA validation results
├── QA_FIX_REQUEST.md         # Issues to fix (if rejected)
├── graphiti/                  # Memory data (if enabled)
└── worktree/                  # Git worktree info
```

### Implementation Plan Status

```json
{
  "subtasks": [
    {
      "id": 1,
      "title": "Create data model",
      "status": "complete",  // pending, in_progress, complete, blocked
      "started_at": "2024-01-01T10:00:00Z",
      "completed_at": "2024-01-01T10:05:00Z"
    }
  ]
}
```

## QA Validation

### QA Reviewer

Validates each acceptance criterion:

```markdown
## QA Report

### Acceptance Criteria

- [x] User can log in with email → PASS
- [x] Error shown for invalid credentials → PASS
- [ ] Session persists across page refresh → FAIL: Session not being saved

### Issues Found
1. Session cookie not being set correctly in AuthProvider
```

### QA Fixer

Automatically fixes issues:
1. Reads QA_FIX_REQUEST.md
2. Analyzes root cause
3. Implements fix
4. Triggers re-validation

### QA Loop

```
QA Reviewer → Issues? → No → Complete
                ↓
               Yes
                ↓
           QA Fixer
                ↓
           Re-validate
                ↓
           (Max 50 loops)
```

## Troubleshooting Builds

### Build Stuck

```bash
# Check what's happening
tail -100 .auto-claude/specs/001-feature/build-progress.txt

# Check for errors
grep -i error .auto-claude/specs/001-feature/build-progress.txt

# Force restart
rm .auto-claude/specs/001-feature/PAUSE
python run.py --spec 001
```

### Agent Recovery

If an agent gets stuck:

1. **Recovery Mode**
   - Coder has recovery prompt (`coder_recovery.md`)
   - Activated when subtask fails multiple times

2. **Manual Intervention**
   ```bash
   # Add human input
   echo "Skip the failing test for now" > .auto-claude/specs/001-feature/HUMAN_INPUT.md
   ```

### Common Issues

| Issue | Solution |
|-------|----------|
| Timeout errors | Increase `API_TIMEOUT_MS` in .env |
| Memory errors | Reduce `max_thinking_tokens` |
| Tool failures | Check security allowlist |
| Git conflicts | Run `--review` and resolve manually |

## Advanced Configuration

### Model Override

```bash
# Use different model
AUTO_BUILD_MODEL=claude-sonnet-4-5-20250929 python run.py --spec 001
```

### Extended Thinking

Configure in agent creation:
- `ultrathink`: 16000 tokens (spec creation)
- `high`: 10000 tokens (QA review)
- `medium`: 5000 tokens (planning)
- `None`: disabled (coding)

### Debug Mode

```bash
DEBUG=true DEBUG_LEVEL=3 python run.py --spec 001
```

## Related Skills

- **auto-claude-spec**: Spec creation
- **auto-claude-workspace**: Workspace management
- **auto-claude-memory**: Memory system
- **auto-claude-optimization**: Performance tuning
