---
name: gemini-cli
description: Ask Gemini via the local `gemini` CLI (no MCP). Use when the user says "ask gemini" / "use gemini", wants a second opinion, needs large-context `@path` analysis, sandbox runs, or structured change-mode edits.
---

# Gemini CLI Skill

Use Google’s `gemini` CLI as an external “second brain” when you need a very large context window, a second opinion, or safe sandbox execution. This skill does **not** use MCP; it runs the local CLI directly.

## When To Use

Use this skill when the user asks to:

- “Ask Gemini” / “Use Gemini”
- Analyze or summarize large files or directories (especially with `@path` references)
- Brainstorm options with a specific framework (SCAMPER, design thinking, etc.)
- Generate structured edit suggestions (“change mode”) that can be applied deterministically

## Prerequisites

- `gemini` CLI is installed and configured (e.g. `gemini --version` works)
- You are allowed to run local shell commands in this environment
- For sandbox execution, Gemini CLI supports `-s/--sandbox` (see `gemini --help`)

## Core Commands

### One-shot query (plain)

```bash
gemini "Explain what this code does: @src/main.ts"
```

### Choose a model

```bash
gemini -m gemini-2.5-pro "..."
gemini -m gemini-2.5-flash "..."
```

### Sandbox mode

```bash
gemini -s "Safely test @scripts/example.py and explain the results."
```

## Helper Script (Recommended)

This skill ships with a dependency-free wrapper that mirrors the core behavior of `gemini-mcp-tool` without MCP:

`skills/gemini-cli/scripts/gemini-tool.mjs`

Important: Gemini CLI can only read files under its current “project directory” (typically the process working directory). Run the wrapper from the repo you want Gemini to read, or pass `--cwd`.

```bash
node skills/gemini-cli/scripts/gemini-tool.mjs help
```

### Ask Gemini (wrapper)

```bash
node skills/gemini-cli/scripts/gemini-tool.mjs ask --prompt "Summarize @. in 5 bullets."
node skills/gemini-cli/scripts/gemini-tool.mjs ask --cwd /path/to/project --prompt "Summarize @. in 5 bullets."
node skills/gemini-cli/scripts/gemini-tool.mjs ask --prompt "..." --model gemini-2.5-pro
node skills/gemini-cli/scripts/gemini-tool.mjs ask --prompt "..." --sandbox
```

### Brainstorm (wrapper)

```bash
node skills/gemini-cli/scripts/gemini-tool.mjs brainstorm --prompt "How should we design onboarding?" --methodology scamper --ideaCount 12
```

### Change Mode (structured edits + chunk caching)

Use change mode when you want Gemini to output **deterministic** OLD/NEW blocks that can be applied by exact string matching.

```bash
node skills/gemini-cli/scripts/gemini-tool.mjs ask --changeMode --prompt "In @src/foo.ts, rename Foo to Bar and update call sites."
```

If the response is chunked, the output includes a `cacheKey`. Fetch the next chunk:

```bash
node skills/gemini-cli/scripts/gemini-tool.mjs fetch-chunk --cacheKey <key> --chunkIndex 2
```

## Safety Rules

- Never execute destructive commands from Gemini output without explicit user approval.
- In change mode, the `OLD` block must match the file content **exactly**; otherwise, do not apply the edit.
- Prefer read-only analysis unless the user explicitly requests changes.
