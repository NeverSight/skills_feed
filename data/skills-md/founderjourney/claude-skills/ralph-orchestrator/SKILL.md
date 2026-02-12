---
name: ralph-orchestrator
description: Autonomous AI agent orchestration using the "Ralph Wiggum technique"—continuously running agents until task completion. Multi-agent support with state persistence.
original_source: https://github.com/mikeyobrien/ralph-orchestrator
author: mikeyobrien
license: MIT
---

# Ralph Orchestrator

An autonomous AI agent orchestration system that implements the "Ralph Wiggum technique"—continuously running AI agents in a loop until tasks complete.

## When to Use This Skill

- Automating complex multi-step development tasks
- Running agents autonomously until completion
- Orchestrating multiple AI backends
- Long-running automated workflows
- Tasks requiring persistent state across iterations

## How It Works

### The Core Loop

```
1. Read task from PROMPT.md
2. Execute AI agent with current prompt
3. Check for completion signals
4. Repeat until success or limits reached
```

### Completion Signals

The loop ends when:
- Task explicitly marked complete
- Maximum iterations reached
- Runtime limit exceeded
- Token/cost limits hit
- Manual interruption

## Supported Agents

- **Claude** (via Claude SDK)
- **Gemini**
- **Q Chat**
- **Kiro CLI**
- **ACP-compliant agents** (extensible)

Auto-detection identifies installed agents.

## Setup

### 1. Install
```bash
pip install ralph-orchestrator
```

### 2. Create Task File
Create `PROMPT.md` with your task:
```markdown
# Task: Implement User Authentication

## Requirements
- JWT-based authentication
- Password hashing with bcrypt
- Login/logout endpoints
- Token refresh mechanism

## Completion Criteria
- All tests passing
- Documentation updated
- Security review complete
```

### 3. Configure (ralph.yml)
```yaml
agent: claude          # Preferred agent
max_iterations: 50     # Iteration limit
max_runtime: 3600      # Seconds
checkpoint_interval: 5  # Git commits every N iterations

permissions:
  allow_web_search: true
  allow_file_write: true
```

### 4. Run
```bash
ralph run
```

## Key Features

### State Persistence
- Git-based checkpointing
- Progress saved at intervals
- Recovery from interruptions
- Full history tracking

### Agent Scratchpad
Maintains context across iterations:
```markdown
# Scratchpad

## Progress
- [x] Set up project structure
- [x] Implemented JWT generation
- [ ] Password hashing
- [ ] API endpoints

## Notes
- Using bcrypt library for hashing
- Token expiry set to 24 hours
```

### Error Recovery
- Exponential backoff on failures
- Automatic retries
- Graceful degradation
- Clear error reporting

### Security
- API key masking in logs
- Sensitive data protection
- Sandboxed execution options
- Audit logging

## Example Workflow

### Task: Build REST API

**PROMPT.md:**
```markdown
Build a REST API for a todo list application.

Requirements:
- CRUD operations for todos
- User authentication
- PostgreSQL database
- FastAPI framework
- Full test coverage

Mark complete when:
- All endpoints working
- Tests passing
- README updated
```

**Execution:**
```bash
$ ralph run

[Iteration 1/50] Agent: claude
> Setting up project structure...
> Created: main.py, requirements.txt, tests/

[Iteration 2/50] Agent: claude
> Implementing database models...
> Created: models.py, database.py

[Iteration 3/50] Agent: claude
> Building CRUD endpoints...
...

[Iteration 12/50] Agent: claude
> All tests passing. Task complete!

✓ Completed in 12 iterations (23 minutes)
```

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `agent` | auto | Preferred agent |
| `max_iterations` | 100 | Iteration limit |
| `max_runtime` | 3600 | Seconds |
| `max_tokens` | null | Token budget |
| `max_cost` | null | Cost limit ($) |
| `checkpoint_interval` | 10 | Git save frequency |

## Best Practices

1. **Clear Completion Criteria**: Define explicit success conditions
2. **Reasonable Limits**: Set appropriate iteration/time bounds
3. **Incremental Tasks**: Break large tasks into stages
4. **Regular Checkpoints**: Enable git-based recovery
5. **Monitor Progress**: Watch iterations for stuck loops

## Troubleshooting

**Agent stuck in loop:**
- Add clearer completion criteria
- Reduce task complexity
- Check for contradictory requirements

**Rate limiting:**
- Increase delay between iterations
- Use multiple agent backends
- Set token budgets

**Recovery needed:**
- Checkpoints auto-restore
- Use `ralph resume` to continue
- Check `.ralph/` for state
