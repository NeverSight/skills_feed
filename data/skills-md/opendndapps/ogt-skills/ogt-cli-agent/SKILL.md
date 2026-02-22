---
name: ogt-cli-agent
description: Run Codex CLI, Claude Code, OpenCode, Gemini CLI, or Pi Coding Agent via background process for programmatic control. Balance load across providers.
metadata: {"moltbot":{"emoji":"🧩","requires":{"anyBins":["claude","codex","opencode","gemini","pi"]}}}
---

# Coding Agent (bash-first)

Use **bash** (with optional background mode) for all coding agent work.

## ⚠️ Load Balancing Required!

**Distribute work across multiple CLI tools** to balance API usage and costs.

| CLI | Auth | Best For | Spawn Weight |
|-----|------|----------|--------------|
| `gemini` | Google OAuth | Fast tasks, bulk work, 1M context | 35% |
| `claude` | Anthropic OAuth | Complex reasoning, code review | 35% |
| `opencode` | Configurable | Flexible backends | 20% |
| `codex` | GitHub Copilot | General coding | 10% |

**Why balance?** Claude/Gemini OAuth = included in Pro memberships. Don't overload one provider.

### Quick Selection Guide

```bash
# Fast generation, bulk content (use gemini)
gemini -p "Generate 10 creature files"

# Complex reasoning, architecture (use claude)
echo "Review this codebase architecture" | claude -p

# TypeScript fixes, simple edits (rotate between all)
# Batch of 6? → 2 gemini, 2 claude, 1 opencode, 1 codex
```

---

## ⚠️ PTY Mode Required!

Coding agents are **interactive terminal applications** that need a pseudo-terminal.

**Always use `pty:true`** when running coding agents:

```bash
# ✅ Correct - with PTY
bash pty:true command:"codex exec 'Your prompt'"

# ❌ Wrong - no PTY
bash command:"codex exec 'Your prompt'"
```

---

## Quick Reference by Tool

### Gemini CLI (fast, 1M context, Google Search)
```bash
# One-shot
gemini -p "Your task"

# With model selection
gemini -p "Complex task" -m gemini-2.5-pro
gemini -p "Quick task" -m gemini-2.5-flash

# Background
bash pty:true background:true workdir:~/project command:"gemini -p 'Your task'"
```

### Claude CLI (deep reasoning, extended thinking)
```bash
# One-shot (pipe preferred)
echo "Your task" | claude -p

# With model
echo "Complex analysis" | claude -p --model opus
echo "Standard task" | claude -p --model sonnet

# Background
bash pty:true background:true workdir:~/project command:"claude 'Your task'"
```

### OpenCode CLI (flexible backends)
```bash
# One-shot
opencode run "Your task"

# Background
bash pty:true background:true workdir:~/project command:"opencode run 'Your task'"
```

### Codex CLI (GitHub Copilot)
```bash
# Needs git repo!
bash pty:true workdir:~/project command:"codex exec 'Your task'"

# Full-auto mode
bash pty:true workdir:~/project command:"codex exec --full-auto 'Build feature X'"
```

---

## Spawning Balanced Sub-Agents

When spawning multiple sub-agents, distribute across providers:

```bash
# Example: 6 TypeScript fix tasks
# Assign: 2 to gemini, 2 to claude, 1 to opencode, 1 to codex

# Task 1-2: Gemini
bash pty:true background:true workdir:~/project command:"gemini -p 'Fix TS errors in file1.ts file2.ts'"

# Task 3-4: Claude  
bash pty:true background:true workdir:~/project command:"claude -p 'Fix TS errors in file3.ts file4.ts'"

# Task 5: OpenCode
bash pty:true background:true workdir:~/project command:"opencode run 'Fix TS errors in file5.ts'"

# Task 6: Codex
bash pty:true background:true workdir:~/project command:"codex exec 'Fix TS errors in file6.ts'"
```

---

## Bash Tool Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | string | Shell command to run |
| `pty` | boolean | **Required for coding agents!** |
| `workdir` | string | Working directory |
| `background` | boolean | Run in background |
| `timeout` | number | Timeout in seconds |

## Process Tool Actions

| Action | Description |
|--------|-------------|
| `list` | List all sessions |
| `poll` | Check if running |
| `log` | Get output |
| `write` | Send raw data |
| `submit` | Send data + Enter |
| `kill` | Terminate |

---

## Rules

1. **Balance load** — distribute across gemini/claude/opencode/codex
2. **Always use pty:true** — coding agents need a terminal
3. **Respect tool choice** — if user asks for specific tool, use it
4. **Be patient** — don't kill slow sessions
5. **Monitor with process:log** — check progress without interfering
