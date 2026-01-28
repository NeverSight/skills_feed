---
name: codeagent
description: Execute codeagent-wrapper for multi-backend AI code tasks. Supports Codex, Claude, and Gemini backends with file references (@syntax) and structured output.
---

# Codeagent Wrapper Integration

## Overview

Execute codeagent-wrapper commands with pluggable AI backends (Codex, Claude, Gemini). Supports file references via `@` syntax, parallel task execution with backend selection, and configurable security controls.

## When to Use

- Complex code analysis requiring deep understanding
- Large-scale refactoring across multiple files
- Automated code generation with backend selection
- Multi-agent orchestration workflows (codex for code, gemini for UI, codex-review for review)

## Usage

**HEREDOC syntax** (recommended):
```bash
codeagent-wrapper - [working_dir] <<'EOF'
<task content here>
EOF
```

**Sanity check (verify CLI is current):**
```bash
codeagent-wrapper --version
codeagent-wrapper --help
```

**With backend selection**:
```bash
codeagent-wrapper --backend claude - <<'EOF'
<task content here>
EOF
```

**Simple tasks**:
```bash
codeagent-wrapper "simple task" [working_dir]
codeagent-wrapper --backend gemini "simple task"
```

## Backends

| Backend | Command | Description | Best For |
|---------|---------|-------------|----------|
| codex | `--backend codex` | OpenAI Codex (default) | Code implementation, code review, complex analysis, orchestration |
| claude | `--backend claude` | Anthropic Claude | Simple tasks, documentation, prompts |
| gemini | `--backend gemini` | Google Gemini | UI/UX development, frontend components |
| opencode | `--backend opencode` | OpenCode CLI (`opencode run`) | Agent-driven runs, inner-loop orchestration decisions |

⚠️ `opencode` backend does **NOT** support stdin input; prompts are passed as CLI args. Prefer short prompts + `@path` file references.

### Backend Selection Guide

**Codex** (default, recommended for code + review):
- Deep code understanding and complex logic analysis
- Code review and quality assessment
- Orchestration and coordination tasks
- Example: "Review the implementation in @src/api for security issues and suggest improvements"

**Claude**:
- Quick feature implementation with clear requirements
- Technical documentation, API specs, README generation
- Professional prompt engineering (e.g., product requirements, design specs)
- Example: "Generate a comprehensive README for @package.json with installation, usage, and API docs"

**Gemini** (recommended for UI):
- UI component scaffolding and layout prototyping
- Design system implementation with style consistency
- Interactive element generation with accessibility support
- Frontend development (React, Vue, HTML/CSS)
- Example: "Create a responsive dashboard layout with sidebar navigation and data visualization cards"

### Multi-Agent Orchestration Pattern

For orchestrated workflows, use this backend assignment:

| Task Type | Backend | Reason |
|-----------|---------|--------|
| Code Implementation | `codex` | Primary code implementation agent |
| UI/Frontend | `gemini` | Specialized for visual components |
| Code Review | `codex` | Deep analysis, quality assessment |

**Backend Switching**:
- Use codex for code implementation, gemini for UI, codex for review
- Use per-task backend selection in parallel mode to optimize for each task's strengths

## Parameters

- `task` (required): Task description, supports `@file` references
- `working_dir` (optional): Working directory (default: current)
- `--backend` (optional): Select AI backend (codex/claude/gemini, default: codex)
  - **Note**: Claude backend only adds `--dangerously-skip-permissions` when explicitly enabled
- `--skip-permissions` / `--dangerously-skip-permissions`: For Claude backend only; disables permission prompts (use sparingly)
- `--tmux-session` (optional): Enable tmux visualization mode for parallel execution
- `--tmux-attach` (optional): Attach to tmux session after completion
- `--tmux-no-main-window` (optional): Remove default `main` window in tmux sessions
- `--window-for` (optional): Single-task mode only; route output to an existing task window
- `--state-file` (optional): Path to AGENT_STATE.json for real-time status updates
- `--review` (optional): Mark tasks as review tasks for state updates
- `--cleanup`: Remove old wrapper logs

## Return Format

```
Agent response text here...

---
SESSION_ID: 019a7247-ac9d-71f3-89e2-a823dbd8fd14
```

## Resume Session

```bash
# Resume with default backend
codeagent-wrapper resume <session_id> - <<'EOF'
<follow-up task>
EOF

# Resume with specific backend
codeagent-wrapper --backend claude resume <session_id> - <<'EOF'
<follow-up task>
EOF
```

## Parallel Execution

**Default (summary mode - context-efficient):**
```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: task1
backend: codex
workdir: /path/to/dir
---CONTENT---
task content
---TASK---
id: task2
dependencies: task1
---CONTENT---
dependent task
EOF
```

**Full output mode (for debugging):**
```bash
codeagent-wrapper --parallel --full-output <<'EOF'
...
EOF
```

**Output Modes:**
- **Summary (default)**: Structured report with changes, output, verification, and review summary.
- **Full (`--full-output`)**: Complete task messages. Use only when debugging specific failures.

**With per-task backend (orchestration pattern)**:
```bash
codeagent-wrapper --parallel --tmux-session orch-session --state-file AGENT_STATE.json <<'EOF'
---TASK---
id: task1
backend: codex
workdir: /path/to/dir
target_window: backend
---CONTENT---
Implement user authentication module
---TASK---
id: task2
backend: gemini
workdir: /path/to/dir
target_window: frontend
---CONTENT---
Create login form component with validation
---TASK---
id: task3
backend: codex
dependencies: task1, task2
target_window: review
---CONTENT---
Review implementation for security issues
EOF
```

**Task metadata fields**:
- `id`: Unique task identifier (required)
- `backend`: AI backend to use (codex/claude/gemini)
- `workdir`: Working directory for the task
- `dependencies`: Comma-separated task IDs that must complete first
- `target_window`: tmux window name for grouping related tasks

**Concurrency Control**:
Set `CODEAGENT_MAX_PARALLEL_WORKERS` to limit concurrent tasks (default: unlimited).

## Environment Variables

- `CODEX_TIMEOUT`: Override timeout in milliseconds (default: 7200000 = 2 hours)
- `CODEAGENT_ASCII_MODE`: Use ASCII symbols instead of Unicode (PASS/WARN/FAIL)
- `CODEAGENT_SKIP_PERMISSIONS`: Control Claude CLI permission checks
  - For **Claude** backend: Set to `true`/`1` to add `--dangerously-skip-permissions` (default: disabled)
  - For **Codex/Gemini** backends: Currently has no effect
- `CODEAGENT_OPENCODE_AGENT`: OpenCode agent name (used by `--backend opencode`)
- `CODEAGENT_OPENCODE_MODEL`: OpenCode model name (used by `--backend opencode`)
- `CODEAGENT_MAX_PARALLEL_WORKERS`: Limit concurrent tasks in parallel mode (default: unlimited, recommended: 8)

🔒 `CODEX_BYPASS_SANDBOX=true` (Codex backend): bypasses approvals/sandbox in Codex CLI. Use only in trusted environments.

## Invocation Pattern

**Single Task**:
```
Bash tool parameters:
- command: codeagent-wrapper --backend <backend> - [working_dir] <<'EOF'
  <task content>
  EOF
- timeout: 7200000
- description: <brief description>
```

**Parallel Tasks**:
```
Bash tool parameters:
- command: codeagent-wrapper --parallel --backend <backend> <<'EOF'
  ---TASK---
  id: task_id
  backend: <backend>  # Optional, overrides global
  workdir: /path
  dependencies: dep1, dep2
  ---CONTENT---
  task content
  EOF
- timeout: 7200000
- description: <brief description>
```

## Security Best Practices

- **Claude Backend**: Permission checks enabled by default
  - To skip checks: set `CODEAGENT_SKIP_PERMISSIONS=true` or pass `--skip-permissions`
- **Concurrency Limits**: Set `CODEAGENT_MAX_PARALLEL_WORKERS` in production to prevent resource exhaustion
- **Automation Context**: This wrapper is designed for AI-driven automation where permission prompts would block execution

## Recent Updates

- **tmux integration**: `--tmux-session` flag for visual parallel execution
- **State file support**: `--state-file` flag for AGENT_STATE.json real-time updates
- Multi-backend support for all modes (workdir, resume, parallel)
- Security controls with configurable permission checks
- Concurrency limits with worker pool and fail-fast cancellation

## Integration with Multi-Agent Orchestration

This skill integrates with the `multi-agent-orchestrator` skill for full orchestration workflows:

```
multi-agent-orchestrator
       │
       │ dispatch_batch.py
       ▼
codeagent-wrapper --parallel --tmux-session <session> --state-file AGENT_STATE.json
       │
       ├── codex (code tasks)
       ├── gemini (UI tasks)
       └── codex (review tasks)
```

See `multi-agent-orchestrator` skill for complete orchestration workflow.
