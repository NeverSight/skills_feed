---
name: context-audit
description: Audit context window composition and identify optimization targets.
  Use when performance feels sluggish, context warnings appear, after installing
  new skills, or for periodic context health checks.
allowed-tools: Read, Grep, Glob, Bash
---

# Context Audit

Analyzes what's consuming your context window and recommends optimizations. Three audit modes can run independently or together.

## Quick Start

- `/context-audit` or "audit my context" — runs all three audits
- "static audit" or "context inventory" — file inventory only
- "session analysis" — JSONL token parsing only
- "context score" — scoring and recommendations only

## Audit Modes

### 1. Static Inventory

Run `scripts/audit-context` to automate the static inventory. Supports `--json` for structured output, `--flagged` for problems only, `--top N` for largest items.

The script scans all context-contributing sources:
- Skills (SKILL.md, rules/, references/)
- CLAUDE.md files (global + project + subdirectories)
- Auto-memory files (`~/.claude/projects/*/memory/*.md`)
- Plugins with per-plugin tool count estimates
- MCP servers

**Thresholds:** Flag SKILL.md > 500 words, any rules/ directory, CLAUDE.md > 2KB, 5+ MCP servers, plugins with 10+ tools.

### 2. Live Context Window (`/context`)

After running the static inventory, tell the user about the built-in `/context` command:
- It shows real-time token usage: current tokens, max capacity, and percentage used
- It breaks down what's in the context window right now (system prompt, conversation, tool results)
- Recommend the user run `/context` themselves for live token data — it complements the static inventory
- If the user shares `/context` output, incorporate it into the scoring (Session Efficiency component)

### 3. Session Token Analysis

Parse the current session's JSONL to track context growth:

1. Find the active session JSONL in `~/.claude/projects/`
2. Extract `usage.input_tokens` and `usage.cache_read_input_tokens` per turn
3. Identify the 5 largest token jumps between consecutive turns
4. Correlate jumps with tool calls from preceding turns
5. Report what triggered each spike

Read `references/audit-procedures.md` for the full JSONL parsing procedure.

### 4. Recommendations & Scoring

Generate actionable recommendations and a letter grade (A-F, 0-100).

**Scoring weights:**
| Component | Weight |
|-----------|--------|
| Skills health | 30% |
| CLAUDE.md health | 25% |
| Plugin/MCP health | 25% |
| Session efficiency | 20% |

## Output Format

Produce a single report with sections:
1. Static Inventory table (from `audit-context` script output)
2. `/context` note — remind the user to run `/context` for live token breakdown
3. Session Analysis (if JSONL available)
4. Top Recommendations
5. Score

Read `references/audit-procedures.md` for detailed procedures, scoring rubric, and recommendation rules.
