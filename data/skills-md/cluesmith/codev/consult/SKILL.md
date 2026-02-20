---
name: consult
description: AI consultation CLI quick reference. Use when running consult commands to check syntax for general queries, protocol reviews, and stats across Gemini, Codex, and Claude.
disable-model-invocation: false
---

# consult - AI Consultation CLI

## Synopsis

```bash
consult -m <model> [options]
consult stats [options]
```

The `-m` / `--model` flag is **always required** (except for stats).

## Models

| Model | Alias | Speed | Approach |
|-------|-------|-------|----------|
| `gemini` | `pro` | ~120-150s | File access via --yolo, fast |
| `codex` | `gpt` | ~200-250s | Shell command exploration, thorough |
| `claude` | `opus` | ~60-120s | Agent SDK with tool use |

## Modes

### General Mode
```bash
consult -m gemini --prompt "What's the best way to structure auth?"
consult -m codex --prompt-file review-checklist.md
```

### Protocol Mode
```bash
consult -m gemini --protocol spir --type spec       # Review a specification
consult -m codex --protocol spir --type plan        # Review a plan
consult -m claude --protocol spir --type impl       # Review implementation
consult -m gemini --protocol spir --type pr         # Review a PR
consult -m codex --protocol spir --type phase       # Phase-scoped review
consult -m gemini --type integration                # Integration review
```

### Stats Mode
```bash
consult stats                     # 30-day summary
consult stats --days 7 --json     # Last 7 days as JSON
```

## Options

```bash
-m, --model <model>         # Model to use (required except stats)
--prompt <text>              # Inline prompt (general mode)
--prompt-file <path>         # Prompt from file (general mode)
--protocol <name>            # Protocol: spir, bugfix, tick, maintain
-t, --type <type>            # Review type: spec, plan, impl, pr, phase, integration
--issue <number>             # Issue number (architect context)
```

## Review Types (--type with --protocol)

| Type | Use Case |
|------|----------|
| `spec` | Review specification completeness |
| `plan` | Review implementation plan |
| `impl` | Review code implementation |
| `pr` | Review pull request before merge |
| `phase` | Phase-scoped review (builder only) |
| `integration` | Architect's integration review |

Protocol-specific prompts live in `codev/protocols/<protocol>/consult-types/`.

## Context Resolution

- **Builder context** (cwd in `.builders/`): auto-detects project from porch state
- **Architect context** (cwd outside `.builders/`): requires `--issue <N>`

## Parallel Consultation (3-Way / cmap)

Run all three models in parallel for thorough reviews:

```bash
consult -m gemini --protocol spir --type spec &
consult -m codex --protocol spir --type spec &
consult -m claude --protocol spir --type spec &
wait
```

Or from Claude Code, use **cmap** pattern: three parallel background Bash calls.

## Common Mistakes

- The `-m` flag is **required** — `consult --type spec` will fail without it
- Cannot combine `--prompt` with `--type` (mode conflict)
- Cannot use `--prompt` and `--prompt-file` together
- `--protocol` requires `--type` — cannot use alone
- General mode: `--prompt` text is passed directly, not as a positional arg
