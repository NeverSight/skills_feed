---
name: autonomous-opus-loop
description: Autonomous Claude Code operation using Opus 4.5 for intelligent continuation decisions. Use when running long tasks, multi-step implementations, overnight development, or any workflow requiring continuous autonomous operation without human intervention.
---

# Autonomous Opus Loop

> **Transform Claude Code from interactive to fully autonomous** using an external Opus 4.5 instance to analyze progress and decide continuation.

## Overview

This skill enables Claude Code to run autonomously by using another Claude instance (Opus 4.5) to:
- Analyze work progress after each response
- Decide whether to continue or stop
- Provide specific next-step instructions
- Maintain momentum until objectives are achieved

**Key Innovation**: The Stop hook's `reason` field becomes Claude's next instruction, creating a fully autonomous loop where two Claude instances collaborate.

## Architecture

```
┌─────────────────────────────────────┐
│  Claude Code (Executor)             │
│  - Executes tasks                   │
│  - Writes code, runs tests          │
│  - Triggers Stop hook when done     │
└─────────────────┬───────────────────┘
                  │
                  ▼ (Stop hook fires)
        ┌─────────────────────────────┐
        │  autonomous-loop.sh         │
        │  - Reads transcript         │
        │  - Checks safety limits     │
        │  - Calls Opus analyzer      │
        └──────────┬──────────────────┘
                   │
                   ▼
   ┌───────────────────────────────────┐
   │  Claude Opus 4.5 (Analyzer)       │
   │  - Reviews all work done          │
   │  - Checks against objectives      │
   │  - Decides: CONTINUE or COMPLETE  │
   │  - If CONTINUE: specific next task│
   └──────────┬────────────────────────┘
              │
              ▼
        ┌─────────────────────────────┐
        │  Loop Controller            │
        │  - Tracks iterations        │
        │  - Monitors cost            │
        │  - Prevents doom loops      │
        │  - Returns decision to CC   │
        └──────────┬──────────────────┘
                   │
                   ▼
    Claude Code receives "reason" as next instruction
            (loop repeats until COMPLETE)
```

## Quick Start

### 1. Install the Hook

```bash
# Run the installation script
.claude/skills/autonomous-opus-loop/scripts/install.sh
```

Or manually add to `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [{
      "matcher": {},
      "hooks": [{
        "type": "command",
        "command": ".claude/skills/autonomous-opus-loop/scripts/autonomous-loop.sh"
      }],
      "timeout": 120
    }]
  }
}
```

### 2. Configure Your Objective

Create `.claude/autonomous-config.json`:

```json
{
  "enabled": true,
  "objective": "Implement user authentication with JWT tokens",
  "success_criteria": [
    "All tests pass",
    "Code coverage > 80%",
    "No security vulnerabilities"
  ],
  "max_iterations": 30,
  "max_cost_usd": 15.00,
  "analyzer_model": "claude-sonnet-4-20250514",
  "verbose": true
}
```

### 3. Start Claude Code

```bash
# Start with initial task
claude -p "Begin implementing user authentication per the objective in .claude/autonomous-config.json"
```

Claude Code will now run autonomously until:
- All success criteria are met
- Max iterations reached
- Cost limit exceeded
- You manually interrupt (Ctrl+C)

## Configuration Reference

### Required Settings

| Setting | Type | Description |
|---------|------|-------------|
| `enabled` | boolean | Enable/disable autonomous mode |
| `objective` | string | High-level goal to achieve |
| `success_criteria` | string[] | Conditions that define "done" |

### Safety Limits

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `max_iterations` | number | 50 | Maximum loop iterations |
| `max_cost_usd` | number | 20.00 | Maximum estimated cost |
| `max_consecutive_failures` | number | 3 | Failures before escalation |
| `max_runtime_minutes` | number | 480 | 8-hour maximum runtime |

### Analyzer Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `analyzer_model` | string | claude-sonnet-4-20250514 | Model for analysis |
| `analyzer_max_tokens` | number | 1024 | Max tokens for analysis |
| `include_full_transcript` | boolean | false | Send full vs. recent context |
| `recent_messages_count` | number | 10 | Messages to include if not full |

### Behavior Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `verbose` | boolean | false | Log detailed progress |
| `notify_on_complete` | boolean | true | System notification on completion |
| `save_session_log` | boolean | true | Save iteration history |
| `escalation_mode` | string | "pause" | Action on escalation: pause/notify/abort |

## Operations

### 1. Enable Autonomous Mode

```bash
# Enable with default config
.claude/skills/autonomous-opus-loop/scripts/enable.sh

# Enable with specific objective
.claude/skills/autonomous-opus-loop/scripts/enable.sh \
  --objective "Refactor the payment module" \
  --max-iterations 20
```

### 2. Disable Autonomous Mode

```bash
.claude/skills/autonomous-opus-loop/scripts/disable.sh
```

### 3. Check Status

```bash
.claude/skills/autonomous-opus-loop/scripts/status.sh
```

Output:
```
Autonomous Loop Status
======================
Enabled: true
Objective: Implement user authentication with JWT tokens
Iterations: 12/30
Estimated Cost: $4.23/$15.00
Runtime: 45m/480m
Last Action: Implemented login endpoint
Next Action: Add password reset functionality
Status: RUNNING
```

### 4. View Session Log

```bash
.claude/skills/autonomous-opus-loop/scripts/view-log.sh
```

### 5. Emergency Stop

```bash
.claude/skills/autonomous-opus-loop/scripts/emergency-stop.sh
```

## Safety Features

### 1. Doom Loop Prevention

The hook checks `stop_hook_active` flag to prevent infinite recursion:

```bash
if [ "$STOP_ACTIVE" == "true" ]; then
  # Already in a stop hook - allow termination
  exit 0
fi
```

### 2. Iteration Limits

Hard cap on iterations prevents runaway execution:

```bash
if [ "$ITERATION" -ge "$MAX_ITERATIONS" ]; then
  log "Max iterations ($MAX_ITERATIONS) reached"
  exit 0  # Allow stop
fi
```

### 3. Cost Tracking

Estimated cost monitoring based on token usage:

```bash
if (( $(echo "$TOTAL_COST > $MAX_COST" | bc -l) )); then
  log "Cost limit ($MAX_COST USD) exceeded"
  exit 0  # Allow stop
fi
```

### 4. Failure Detection

Consecutive failure tracking triggers escalation:

```bash
if [ "$CONSECUTIVE_FAILURES" -ge "$MAX_FAILURES" ]; then
  escalate "Doom loop detected: $CONSECUTIVE_FAILURES consecutive failures"
fi
```

### 5. Circular Work Detection

Semantic analysis detects repeated work patterns:

```bash
# Analyzer prompt includes:
"Detect if the same work is being repeated. If circular pattern detected, respond with ESCALATE."
```

## Analyzer Prompts

### Default Analyzer System Prompt

```
You are an autonomous development coordinator analyzing Claude Code progress.

OBJECTIVE: {objective}

SUCCESS CRITERIA:
{success_criteria}

Your task:
1. Analyze the recent work done
2. Check progress against success criteria
3. Decide: CONTINUE, COMPLETE, or ESCALATE

Response format:
- If more work needed: "CONTINUE: [specific next task with clear instructions]"
- If all criteria met: "COMPLETE: [summary of what was achieved]"
- If stuck/looping: "ESCALATE: [description of the problem]"

Be specific in CONTINUE responses. Give actionable next steps.
Do not repeat tasks that have already been completed.
Track what's done vs. what remains.
```

### Custom Analyzer Prompts

Create custom prompts in `.claude/autonomous-prompts/`:

```
.claude/autonomous-prompts/
├── refactoring.txt      # For refactoring tasks
├── feature-build.txt    # For new features
├── bug-fix.txt          # For bug fixing
└── testing.txt          # For test writing
```

Reference in config:

```json
{
  "analyzer_prompt_file": ".claude/autonomous-prompts/feature-build.txt"
}
```

## Integration with Other Skills

### With hooks-manager

The autonomous loop works alongside other hooks:

```json
{
  "hooks": {
    "Stop": [{
      "hooks": [{
        "type": "command",
        "command": ".claude/skills/autonomous-opus-loop/scripts/autonomous-loop.sh"
      }]
    }],
    "PostToolUse": [{
      "tools": ["Write", "Edit"],
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$FILE\""
      }]
    }]
  }
}
```

### With agent-memory-system

Enable persistent learning across autonomous sessions:

```json
{
  "integrations": {
    "agent_memory": true,
    "save_episodes": true,
    "learn_patterns": true
  }
}
```

### With momentum-keeper

Combine for enhanced progress tracking:

```json
{
  "integrations": {
    "momentum_keeper": true,
    "stall_detection": true,
    "energy_management": false
  }
}
```

### With observability stack

Send metrics to your observability stack:

```json
{
  "observability": {
    "enabled": true,
    "endpoint": "http://localhost:4317",
    "metrics": ["iterations", "cost", "duration", "success_rate"]
  }
}
```

## Example Configurations

### Overnight Feature Development

```json
{
  "enabled": true,
  "objective": "Build complete user dashboard with charts, filters, and export",
  "success_criteria": [
    "Dashboard component renders without errors",
    "All 5 chart types implemented",
    "Filter functionality works",
    "Export to CSV and PDF works",
    "Unit tests pass with >80% coverage",
    "E2E tests pass"
  ],
  "max_iterations": 100,
  "max_cost_usd": 50.00,
  "max_runtime_minutes": 480,
  "analyzer_model": "claude-sonnet-4-20250514",
  "notify_on_complete": true,
  "escalation_mode": "notify"
}
```

### Quick Refactoring Task

```json
{
  "enabled": true,
  "objective": "Refactor utils/ to use TypeScript strict mode",
  "success_criteria": [
    "All files converted to .ts",
    "No 'any' types remain",
    "TypeScript compiles without errors",
    "All existing tests pass"
  ],
  "max_iterations": 20,
  "max_cost_usd": 10.00,
  "analyzer_model": "claude-sonnet-4-20250514"
}
```

### Bug Hunting Session

```json
{
  "enabled": true,
  "objective": "Find and fix the memory leak in the WebSocket handler",
  "success_criteria": [
    "Memory leak identified",
    "Root cause documented",
    "Fix implemented",
    "Memory usage stable over 1000 connections",
    "No regression in existing tests"
  ],
  "max_iterations": 30,
  "max_cost_usd": 15.00,
  "analyzer_prompt_file": ".claude/autonomous-prompts/bug-fix.txt"
}
```

## Troubleshooting

### Hook Not Firing

1. Check hook is installed:
   ```bash
   cat .claude/settings.json | jq '.hooks.Stop'
   ```

2. Verify script is executable:
   ```bash
   chmod +x .claude/skills/autonomous-opus-loop/scripts/*.sh
   ```

3. Check for syntax errors:
   ```bash
   bash -n .claude/skills/autonomous-opus-loop/scripts/autonomous-loop.sh
   ```

### Immediate Stop (Not Continuing)

1. Check `enabled` is true in config
2. Verify API key is set: `echo $ANTHROPIC_API_KEY`
3. Check iteration/cost limits aren't exceeded
4. Review logs: `.claude/autonomous-log.jsonl`

### Infinite Loop / Runaway

1. Emergency stop: `Ctrl+C` or run `emergency-stop.sh`
2. Check `stop_hook_active` handling in script
3. Verify max_iterations is reasonable
4. Check for doom loop detection in logs

### API Errors

1. Verify API key: `echo $ANTHROPIC_API_KEY | head -c 10`
2. Check model availability
3. Review error in `.claude/autonomous-log.jsonl`
4. Try with `verbose: true` for detailed output

## Session Logs

All autonomous sessions are logged to `.claude/autonomous-log.jsonl`:

```json
{"timestamp": "2024-01-15T10:30:00Z", "iteration": 1, "action": "START", "objective": "..."}
{"timestamp": "2024-01-15T10:31:00Z", "iteration": 1, "action": "CONTINUE", "task": "..."}
{"timestamp": "2024-01-15T10:35:00Z", "iteration": 2, "action": "CONTINUE", "task": "..."}
{"timestamp": "2024-01-15T11:00:00Z", "iteration": 15, "action": "COMPLETE", "summary": "..."}
```

View formatted:
```bash
.claude/skills/autonomous-opus-loop/scripts/view-log.sh --format pretty
```

## Best Practices

### 1. Clear Objectives

Bad: "Make the code better"
Good: "Refactor auth module to use dependency injection, add unit tests for all public methods"

### 2. Measurable Success Criteria

Bad: "Code should be clean"
Good: "ESLint passes with no warnings, all functions have JSDoc comments"

### 3. Reasonable Limits

- Start with lower iteration limits (20-30)
- Increase based on task complexity
- Set cost limits slightly above expected

### 4. Monitor First Runs

- Use `verbose: true` initially
- Watch the first few iterations
- Adjust prompts based on behavior

### 5. Use Appropriate Models

- `claude-sonnet-4-20250514`: Good balance of speed/quality (recommended)
- `claude-opus-4-5-20250929`: Better analysis, higher cost
- `claude-3-5-haiku-20241022`: Fast/cheap for simple tasks

## Cost Estimation

Approximate costs per iteration (analyzer call):

| Model | Input (10k tokens) | Output (1k tokens) | Total |
|-------|-------------------|-------------------|-------|
| Sonnet 4 | $0.03 | $0.015 | ~$0.045 |
| Opus 4.5 | $0.15 | $0.075 | ~$0.225 |
| Haiku 3.5 | $0.008 | $0.004 | ~$0.012 |

**Example**: 30 iterations with Sonnet = ~$1.35 for analyzer alone
(Plus Claude Code usage costs)

## References

- `references/hook-mechanics.md` - Deep dive into Stop hook behavior
- `references/analyzer-prompts.md` - Prompt engineering for analyzers
- `references/safety-patterns.md` - Comprehensive safety documentation
- `references/integration-guide.md` - Integrating with other skills

## Scripts

- `scripts/autonomous-loop.sh` - Main Stop hook handler
- `scripts/opus-analyzer.py` - Python analyzer (alternative)
- `scripts/install.sh` - Install hooks to settings
- `scripts/enable.sh` - Enable autonomous mode
- `scripts/disable.sh` - Disable autonomous mode
- `scripts/status.sh` - Check current status
- `scripts/view-log.sh` - View session logs
- `scripts/emergency-stop.sh` - Emergency termination

## Version History

- **v1.0.0** (2024-01): Initial release with Stop hook support
- Supports bash and Python analyzers
- Integration with observability stack
- Comprehensive safety features
