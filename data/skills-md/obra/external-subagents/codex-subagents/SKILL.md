---
name: codex-subagents
description: Spawn background subagents for parallel or long-running tasks. Use when you need research threads, context isolation, or detached execution.
---

# Codex Subagents

## Overview

`codex-subagent` offloads work to background threads so your main context stays lean. Threads run detached by default; use `wait`/`peek` to check results.

**Critical rules**:
1. You cannot send to a running thread. Always wait before sending follow-ups.
2. Use `--permissions read-only` or `--permissions workspace-write` (not `workspace-read`)

For detailed workflow documentation, see [reference/workflow.md](reference/workflow.md).

## When to Use

| Situation | Why subagents help |
|-----------|-------------------|
| Parallel research tasks | Multiple threads run simultaneously |
| Context would bloat | Research stays in separate thread |
| Long-running work | Detached execution, check later |

**Don't use for**: Quick inline questions, tightly-coupled work needing your current state.

## Core Workflow

```
1. start with --prompt    (inline text or stdin)
2. wait/peek → check result
3. send → resume with follow-up (ONLY after thread stops)
4. archive/clean → lifecycle management
```

## The Running Thread Rule

**You CANNOT send to a running thread.** This is the #1 mistake.

```bash
# WRONG - thread might still be running
echo "followup" | codex-subagent send thread-abc --prompt -

# RIGHT - wait first, then send
codex-subagent wait --threads thread-abc
echo "followup" | codex-subagent send thread-abc --prompt -
```

Resumable statuses: `completed`, `failed`, `stopped`, `waiting`

## Quick Reference

| Command | Purpose | Key flags |
|---------|---------|-----------|
| `start` | Launch new thread | `--role`, `--permissions`, `--prompt`, `--label`, `-w` |
| `send` | Resume stopped thread | `<thread-id>`, `--prompt`, `-w` |
| `peek` | Read newest unseen message | `<thread-id>`, `--save-response` |
| `log` | Full history | `<thread-id>`, `--tail`, `--json` |
| `status` | Thread summary | `<thread-id>` |
| `wait` | Block until threads stop | `--threads`, `--labels`, `--all`, `--follow-last` |
| `list` | Show threads | `--status`, `--label`, `--role` |
| `archive` | Move completed to archive | `--completed`, `--yes`, `--dry-run` |
| `clean` | Delete old archives | `--older-than-days`, `--yes` |

**Prompt input**: `--prompt "text"` for simple prompts, `--prompt -` reads from stdin (for multi-line), `-f`/`--prompt-file` for files

**Positional thread IDs**: `peek abc123` works like `peek -t abc123`

## Common Patterns

### Simple inline prompt
```bash
codex-subagent start --role researcher --permissions read-only \
  --label "quick-task" --prompt "List all exported functions in src/lib/"
```

### Multi-line prompt (heredoc)
```bash
cat <<'EOF' | codex-subagent start --role researcher --permissions read-only --label "auth-research" --prompt -
Research authentication patterns in this codebase:
1. Find all auth-related files
2. Document the auth flow
3. Note any security concerns
EOF
```

### Parallel research
```bash
# Launch multiple researchers
cat <<'EOF' | codex-subagent start --role researcher --permissions read-only --label "API: Stripe" --prompt -
Research Stripe API authentication methods and best practices
EOF

cat <<'EOF' | codex-subagent start --role researcher --permissions read-only --label "API: Twilio" --prompt -
Research Twilio API authentication methods and best practices
EOF

# Wait for all, see results
codex-subagent wait --labels "API:" --follow-last
```

### Blocking task
```bash
# -w blocks until complete (may take minutes)
cat <<'EOF' | codex-subagent start --role researcher --permissions read-only --prompt - -w --save-response result.txt
Analyze error handling patterns in src/
EOF
cat result.txt
```

**Warning**: `-w` blocks for as long as the agent runs. For long tasks, prefer detached mode with `wait --follow-last`.

### Cleanup old work
```bash
# Two-phase: archive completed, then clean old archives
codex-subagent archive --completed --yes
codex-subagent clean --older-than-days 30 --yes
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| "profile does not exist" | Wrong permissions | Use `read-only` or `workspace-write` (not `workspace-read`) |
| "not resumable" error | Thread still running | `wait` first, then `send` |
| "different controller" | Wrong session | Use `--controller-id` or check `list` |
| Thread disappeared | Was archived | Check archive dir or re-run task |

## Checklist

- [ ] `start` has `--role`, `--permissions`, `--prompt`, and `--label`
- [ ] Permissions are `read-only` or `workspace-write`
- [ ] `wait` before `send` (never send to running thread)
- [ ] Results captured with `--save-response` or `peek`
